"""Pull Leg W, tax base and context series from FRED (Z.1 / NIPA / BIS). No API key needed."""
import json, pathlib, sys, datetime, re
import requests
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sources import FRED_SERIES

RAW = pathlib.Path(__file__).parents[1] / "data" / "raw" / "fred"
RAW.mkdir(parents=True, exist_ok=True)
CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
META = "https://fred.stlouisfed.org/data/{}.txt"

def field(h, label):
    m = re.search(rf'{label}</th>\s*<td>(.*?)</td>', h, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else "?"

def main():
    log = {}
    for sid, leg in FRED_SERIES.items():
        r = requests.get(CSV.format(sid), timeout=60)
        ok = r.status_code == 200 and r.text.lstrip().lower().startswith(("observation_date", "date"))
        if ok:
            (RAW / f"{sid}.csv").write_bytes(r.content)
        h = requests.get(META.format(sid), timeout=60).text
        t = re.search(r"<title>Table Data - (.*?) \| FRED", h, re.S)
        log[sid] = {"leg": leg, "ok": ok, "status": r.status_code,
                    "title": re.sub(r"\s+", " ", t.group(1)).strip() if t else "?",
                    "units": field(h, "Units"), "freq": field(h, "Frequency"),
                    "seas": field(h, "Seasonal Adjustment"), "source": field(h, "Source"),
                    "release": field(h, "Release"), "last_updated": field(h, "Last Updated"),
                    "date_range": field(h, "Date Range"),
                    "url": CSV.format(sid), "retrieved": datetime.date.today().isoformat()}
        print(f"{sid:18s} {'OK ' if ok else 'FAIL'} | {log[sid]['units'][:22]:22s} | {log[sid]['title'][:62]}")
    (RAW / "_manifest.json").write_text(json.dumps(log, indent=2))
    bad = [k for k, v in log.items() if not v["ok"]]
    print(f"\n{len(log)-len(bad)}/{len(log)} retrieved. Failed: {bad}")

if __name__ == "__main__":
    main()
