"""
Fetch the bank-year panel. Constructs and controls at June 30 of t (2001-2021),
outcomes from December 31 YTD charge-offs (2002-2024).

Using December 31 YTD avoids the year-to-date differencing trap entirely: the
Q4 value IS the calendar-year flow.
"""
from pathlib import Path
import json
import time
import urllib.parse
import urllib.request
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "predictive"
RAW.mkdir(parents=True, exist_ok=True)
API = "https://banks.data.fdic.gov/api"

CONSTRUCT_FIELDS = [
    "CERT", "REPDTE", "NAMEFULL", "STNAME", "ASSET", "DEP", "SC", "SCMUNI",
    "LNLSGR", "LNRECONS", "LNRENRES", "LNREMULT", "LNRERES", "LNREAG", "LNCI",
    "LNAG", "LNCRCD", "LNAUTO", "LNCONOTH", "BRO", "RBC1AAJ", "RBCT1J",
    "NTLNLS", "NTRERES", "NTCRCD", "NTAUTO", "NTCONOTH", "NTCI", "NTRENRES",
]
OUTCOME_FIELDS = [
    "CERT", "REPDTE", "ASSET", "LNLSGR", "RBC1AAJ", "ROA",
    "NTLNLS", "NTRERES", "NTCRCD", "NTAUTO", "NTCONOTH", "NTCI", "NTRENRES",
    "P9RERES", "NARERES", "P9CI", "NACI",
]
SOD_FIELDS = ["CERT", "YEAR", "STCNTYBR", "DEPSUMBR"]


def fetch(endpoint, filters, fields, limit=10000):
    out, offset = [], 0
    while True:
        q = urllib.parse.urlencode({
            "filters": filters, "fields": ",".join(fields),
            "limit": limit, "offset": offset, "format": "json"})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(f"{API}/{endpoint}?{q}",
                                            timeout=180) as r:
                    p = json.load(r)
                break
            except Exception as exc:
                if attempt == 4:
                    raise
                time.sleep(2 * (attempt + 1))
        rows = [d["data"] for d in p.get("data", [])]
        out.extend(rows)
        offset += limit
        if offset >= p["meta"]["total"] or not rows:
            break
    return pd.DataFrame(out)


def main():
    # constructs and controls, June 30, 2001-2021
    fr = []
    for y in range(2001, 2022):
        d = fetch("financials", f"REPDTE:{y}0630", CONSTRUCT_FIELDS)
        d["origin_year"] = y
        fr.append(d)
        print(f"  constructs {y}: {len(d)}")
    pd.concat(fr, ignore_index=True).to_csv(
        RAW / "fin_june.csv", index=False)

    # outcomes, December 31 YTD, 2002-2024
    fr = []
    for y in range(2002, 2025):
        d = fetch("financials", f"REPDTE:{y}1231", OUTCOME_FIELDS)
        d["out_year"] = y
        fr.append(d)
        print(f"  outcomes {y}: {len(d)}")
    pd.concat(fr, ignore_index=True).to_csv(
        RAW / "fin_dec.csv", index=False)

    # summary of deposits, 2001-2021
    fr = []
    for y in range(2001, 2022):
        d = fetch("sod", f"YEAR:{y}", SOD_FIELDS)
        fr.append(d)
        print(f"  sod {y}: {len(d)}")
    pd.concat(fr, ignore_index=True).to_csv(RAW / "sod.csv", index=False)
    print("done")


if __name__ == "__main__":
    main()
