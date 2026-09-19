"""Pull Leg A primitives (capex, operating cash flow, debt, leases) from SEC XBRL company facts.
Tier 2 of the Leg A definition: capex split by funding source, from filings only."""
import json, pathlib, sys, time, datetime
import requests
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sources import SEC_COMPANIES, SEC_TAGS
from config import SEC_USER_AGENT, SEC_REQUEST_DELAY_SECONDS

RAW = pathlib.Path(__file__).parents[1] / "data" / "raw" / "sec"
RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": SEC_USER_AGENT}   # see src/config.py
URL = "https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json"

def main():
    log = {}
    for tic, (cik, name, cls) in SEC_COMPANIES.items():
        for key, tags in SEC_TAGS.items():
            for tag in tags:
                u = URL.format(cik=cik, tag=tag)
                r = requests.get(u, headers=UA, timeout=60)
                ok = r.status_code == 200
                if ok:
                    (RAW / f"{tic}_{key}__{tag}.json").write_bytes(r.content)
                log[f"{tic}_{key}__{tag}"] = {"ticker": tic, "name": name, "class": cls,
                                              "cik": cik, "concept": key, "tag": tag,
                                              "ok": ok, "status": r.status_code, "url": u,
                                              "retrieved": datetime.date.today().isoformat()}
                time.sleep(SEC_REQUEST_DELAY_SECONDS)  # SEC limit: 10 req/s
        got = [k for k in SEC_TAGS if any(v["ok"] for kk, v in log.items()
               if v["ticker"] == tic and v["concept"] == k)]
        print(f"{tic:6s} {name[:28]:28s} {len(got)}/{len(SEC_TAGS)} tags: {','.join(got)}")
    (RAW / "_manifest.json").write_text(json.dumps(log, indent=2))
    print(f"\n{sum(v['ok'] for v in log.values())}/{len(log)} concept series retrieved")

if __name__ == "__main__":
    main()
