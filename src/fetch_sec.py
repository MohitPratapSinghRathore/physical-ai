"""Pull Leg A primitives (capex, operating cash flow, debt, leases) from SEC XBRL company facts.
Tier 2 of the Leg A definition: capex split by funding source, from filings only."""
import json, pathlib, sys, time, datetime
import requests
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sources import SEC_COMPANIES, SEC_TAGS

RAW = pathlib.Path(__file__).parents[1] / "data" / "raw" / "sec"
RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "physical-ai-research/0.1 (github.com/MohitPratapSinghRathore/physical-ai)"}
URL = "https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json"

def main():
    log = {}
    for tic, (cik, name, cls) in SEC_COMPANIES.items():
        for key, tag in SEC_TAGS.items():
            u = URL.format(cik=cik, tag=tag)
            r = requests.get(u, headers=UA, timeout=60)
            ok = r.status_code == 200
            if ok:
                (RAW / f"{tic}_{key}.json").write_bytes(r.content)
            log[f"{tic}_{key}"] = {"ticker": tic, "name": name, "class": cls, "cik": cik,
                                   "tag": tag, "ok": ok, "status": r.status_code, "url": u,
                                   "retrieved": datetime.date.today().isoformat()}
            time.sleep(0.12)  # SEC fair-access limit: 10 req/s
        got = [k for k, t in SEC_TAGS.items() if log[f'{tic}_{k}']['ok']]
        print(f"{tic:6s} {name[:28]:28s} {len(got)}/{len(SEC_TAGS)} tags: {','.join(got)}")
    (RAW / "_manifest.json").write_text(json.dumps(log, indent=2))
    print(f"\n{sum(v['ok'] for v in log.values())}/{len(log)} concept series retrieved")

if __name__ == "__main__":
    main()
