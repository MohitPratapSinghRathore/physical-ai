"""
Fetch PRE-SHOCK predictors only. No outcome variable for any shock period is
touched here: this pulls 2014-06-30 balance-sheet composition and 2014 branch
deposits, both dated before the oil-price collapse begins (2014Q4).

Sources, all public, no key required:
  FDIC BankFind Suite API, /financials  (Call Report / FFIEC 051-041-031 derived)
  FDIC BankFind Suite API, /sod         (Summary of Deposits, June 30 annual)
  BEA Regional CAINC4                   (county personal income by source)

Outputs land in data/raw/validation/.
"""
import io, json, time, zipfile, urllib.request, urllib.parse
from pathlib import Path
import pandas as pd

RAW = Path(__file__).resolve().parents[2] / "data" / "raw" / "validation"
RAW.mkdir(parents=True, exist_ok=True)
API = "https://banks.data.fdic.gov/api"

FIN_FIELDS = [
    "CERT", "REPDTE", "NAMEFULL", "STNAME", "ASSET", "DEP", "EQ", "SC", "SCMUNI",
    "LNLSGR", "LNLSNET", "LNRECONS", "LNRENRES", "LNREMULT", "LNRERES", "LNRELOC",
    "LNREAG", "LNCI", "LNAG", "LNCRCD", "LNAUTO", "LNCONOTH", "BRO", "RBC1AAJ",
    "RBCT1J",
]
SOD_FIELDS = ["CERT", "YEAR", "STCNTYBR", "DEPSUMBR"]


def fetch(endpoint, filters, fields, limit=10000):
    """Page through a BankFind endpoint and return a DataFrame."""
    out, offset = [], 0
    while True:
        q = urllib.parse.urlencode({
            "filters": filters, "fields": ",".join(fields),
            "limit": limit, "offset": offset, "format": "json",
        })
        url = f"{API}/{endpoint}?{q}"
        for attempt in range(5):
            try:
                with urllib.request.urlopen(url, timeout=180) as r:
                    payload = json.load(r)
                break
            except Exception as exc:                       # transient API errors
                if attempt == 4:
                    raise
                print(f"    retry {attempt+1} ({exc})")
                time.sleep(3 * (attempt + 1))
        rows = [d["data"] for d in payload.get("data", [])]
        out.extend(rows)
        total = payload["meta"]["total"]
        print(f"  {endpoint}: {len(out)}/{total}")
        offset += limit
        if offset >= total or not rows:
            break
    return pd.DataFrame(out)


def main():
    print("FDIC financials, 2014-06-30 (pre-shock balance sheet)")
    fin = fetch("financials", "REPDTE:20140630", FIN_FIELDS)
    fin.to_csv(RAW / "fdic_financials_20140630.csv", index=False)

    print("FDIC Summary of Deposits, 2014")
    sod = fetch("sod", "YEAR:2014", SOD_FIELDS)
    sod.to_csv(RAW / "fdic_sod_2014.csv", index=False)

    print("BEA CAINC4 (county personal income by source)")
    zpath = RAW / "CAINC4.zip"
    if not zpath.exists():
        urllib.request.urlretrieve(
            "https://apps.bea.gov/regional/zip/CAINC4.zip", zpath)
    with zipfile.ZipFile(zpath) as z:
        name = "CAINC4__ALL_AREAS_1969_2024.csv"
        bea = pd.read_csv(io.BytesIO(z.read(name)), encoding="latin-1", dtype=str)
    bea.to_csv(RAW / "bea_cainc4_all_areas.csv", index=False)
    print("done")


if __name__ == "__main__":
    main()
