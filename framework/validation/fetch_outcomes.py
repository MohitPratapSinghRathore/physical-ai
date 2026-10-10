"""
SESSION2_PLAN step 8: open the outcome files. FIRST SCRIPT IN THIS PROJECT THAT DOES.

Applies the section 14.4 call-report rule exactly:
  - where a quarterly (Q-suffixed) field exists, use it;
  - otherwise the field is YEAR-TO-DATE within the calendar year, so the quarterly
    flow is Q1 = Q1ytd, Q2 = Q2ytd - Q1ytd, Q3 = Q3ytd - Q2ytd, Q4 = Q4ytd - Q3ytd;
  - YTD values are NEVER summed across quarters;
  - a negative constructed quarter (recoveries exceeding charge-offs) is kept as a
    negative, not floored at zero, and such cases are counted and reported.
"""
from pathlib import Path
import json
import time
import urllib.parse
import urllib.request
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"
API = "https://banks.data.fdic.gov/api"

# flow fields: (ytd_name, quarterly_name_or_None)
FLOWS = {
    "nt_reres":  ("NTRERES", "NTRERESQ"),
    "nt_crcd":   ("NTCRCD", "NTCRCDQ"),
    "nt_auto":   ("NTAUTO", "NTAUTOQ"),
    "nt_conoth": ("NTCONOTH", None),       # no Q field: difference YTD
    "nt_ci":     ("NTCI", "NTCIQ"),
    "nt_renres": ("NTRENRES", None),       # no Q field: difference YTD
    "nt_recons": ("NTRECONS", None),
    "nt_total":  ("NTLNLS", "NTLNLSQ"),
}
STOCKS = ["P9RERES", "NARERES", "P9CI", "NACI", "NACRCD", "RBC1AAJ",
          "LNLSGR", "ASSET", "ROA"]

REPDTES = [f"{y}{m}" for y in range(2014, 2019)
           for m in ("0331", "0630", "0930", "1231")
           if not (y == 2014 and m in ("0331", "0630"))]


def fetch(fields, repdte):
    out, offset = [], 0
    while True:
        q = urllib.parse.urlencode({
            "filters": f"REPDTE:{repdte}", "fields": ",".join(fields),
            "limit": 10000, "offset": offset, "format": "json"})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(f"{API}/financials?{q}",
                                            timeout=180) as r:
                    p = json.load(r)
                break
            except Exception as exc:
                if attempt == 4:
                    raise
                time.sleep(3 * (attempt + 1))
        rows = [d["data"] for d in p.get("data", [])]
        out.extend(rows)
        offset += 10000
        if offset >= p["meta"]["total"] or not rows:
            break
    return pd.DataFrame(out)


def main():
    wanted = ["CERT", "REPDTE"] + STOCKS
    for ytd, qf in FLOWS.values():
        wanted.append(ytd)
        if qf:
            wanted.append(qf)

    frames = []
    for rep in REPDTES:
        d = fetch(wanted, rep)
        d["REPDTE"] = rep
        frames.append(d)
        print(f"  {rep}: {len(d)} rows")
    raw = pd.concat(frames, ignore_index=True)
    raw.to_csv(RAW / "fdic_outcomes_raw.csv", index=False)

    raw["year"] = raw["REPDTE"].str[:4].astype(int)
    raw["q"] = raw["REPDTE"].str[4:].map({"0331": 1, "0630": 2,
                                          "0930": 3, "1231": 4})
    for c in raw.columns:
        if c not in ("REPDTE",):
            raw[c] = pd.to_numeric(raw[c], errors="coerce")
    raw = raw.sort_values(["CERT", "year", "q"])

    # ---- section 14.4 construction ---------------------------------------
    report = {}
    for name, (ytd, qf) in FLOWS.items():
        if qf and qf in raw.columns and raw[qf].notna().any():
            raw[f"{name}_q"] = raw[qf]
            report[name] = {"source": "quarterly field", "field": qf}
        else:
            g = raw.groupby(["CERT", "year"])[ytd]
            raw[f"{name}_q"] = raw[ytd] - g.shift(1).fillna(0)
            # Q1 has no prior quarter in the calendar year: YTD is the flow
            raw.loc[raw["q"] == 1, f"{name}_q"] = raw.loc[raw["q"] == 1, ytd]
            report[name] = {"source": "YTD differenced within calendar year",
                            "field": ytd}
        neg = int((raw[f"{name}_q"] < 0).sum())
        report[name]["negative_quarters"] = neg
        report[name]["negative_pct"] = round(
            100 * neg / raw[f"{name}_q"].notna().sum(), 3)

    (OUT / "ytd_construction_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
    raw.to_csv(RAW / "fdic_outcomes_quarterly.csv", index=False)
    print("\nCONSTRUCTION")
    for k, v in report.items():
        print(f"  {k:10s} {v['source']:38s} ({v['field']:9s})  "
              f"negative quarters {v['negative_quarters']:6d} "
              f"({v['negative_pct']}%)")


if __name__ == "__main__":
    main()
