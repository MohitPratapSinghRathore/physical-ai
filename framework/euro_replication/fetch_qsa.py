"""
Option 2: euro-area claim stock from the ECB Quarterly Sector Accounts.

QSA gives claim LEVELS by issuing sector and instrument. It does NOT carry
issuer-counterpart detail: the counterpart sector is S1 (total economy) for
every series, so QSA alone is not a holder map. That limitation is recorded in
LIMITATIONS and governs what can be concluded.

Dimension order, verified from the API header:
FREQ.ADJUSTMENT.REF_AREA.COUNTERPART_AREA.REF_SECTOR.COUNTERPART_SECTOR.
CONSOLIDATION.ACCOUNTING_ENTRY.STO.INSTR_ASSET.MATURITY.EXPENDITURE.
UNIT_MEASURE.CURRENCY_DENOM.VALUATION.PRICES.TRANSFORMATION.CUST_BREAKDOWN
"""
from pathlib import Path
import io
import json
import urllib.request
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "euro_replication"
OUT = Path(__file__).resolve().parent
BASE = "https://data-api.ecb.europa.eu/service/data/QSA"
RAW.mkdir(parents=True, exist_ok=True)

# euro area (I9), counterpart world (W0), non-consolidated, levels (LE),
# liabilities (L) = claims OWED by that sector
SERIES = {
    # claim class                     ref sector, entry, instrument, maturity
    "govt_debt_securities":          ("S13", "L", "F3", "T"),
    "govt_loans":                    ("S13", "L", "F4", "T"),
    "household_loans_total":         ("S1M", "L", "F4", "T"),
    "household_loans_long":          ("S1M", "L", "F4", "L"),
    "household_loans_short":         ("S1M", "L", "F4", "S"),
    "nfc_debt_securities":           ("S11", "L", "F3", "T"),
    "nfc_loans":                     ("S11", "L", "F4", "T"),
    "nfc_equity":                    ("S11", "L", "F51", "T"),
    # holder-side totals, for the holder leg
    "cb_holdings_debt_securities":   ("S121", "A", "F3", "T"),
    "govt_holdings_debt_securities": ("S13", "A", "F3", "T"),
    "govt_holdings_loans":           ("S13", "A", "F4", "T"),
    "cb_holdings_loans":             ("S121", "A", "F4", "T"),
}


def key(ref, entry, instr, mat):
    return (f"Q.N.I9.W0.{ref}.S1.N.{entry}.LE.{instr}.{mat}"
            f"._Z.XDC._T.S.V.N._T")


def fetch(k, n=1):
    url = f"{BASE}/{k}?lastNObservations={n}"
    req = urllib.request.Request(url, headers={"Accept": "text/csv"})
    with urllib.request.urlopen(req, timeout=120) as r:
        txt = r.read().decode("utf-8")
    if not txt.strip() or txt.count("\n") < 2:
        return None
    return pd.read_csv(io.StringIO(txt))


def main():
    out = {}
    for name, (ref, entry, instr, mat) in SERIES.items():
        k = key(ref, entry, instr, mat)
        try:
            df = fetch(k)
        except Exception as exc:
            print(f"  {name:32s} ERROR {exc}")
            out[name] = None
            continue
        if df is None or df.empty:
            print(f"  {name:32s} NO DATA  ({k})")
            out[name] = None
            continue
        row = df.iloc[-1]
        val = float(row["OBS_VALUE"])
        out[name] = {"value_mn_eur": val, "period": str(row["TIME_PERIOD"]),
                     "key": k}
        print(f"  {name:32s} {val/1e6:10,.1f} bn EUR   {row['TIME_PERIOD']}")

    (OUT / "qsa_levels.json").write_text(json.dumps(out, indent=2),
                                         encoding="utf-8")
    print("\nwritten qsa_levels.json")


if __name__ == "__main__":
    main()
