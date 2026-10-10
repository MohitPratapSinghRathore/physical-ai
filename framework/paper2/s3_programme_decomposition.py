"""
Session 3. Decompose the federal holder leg by PROGRAMME, 1947-2025, under both
the central and the second-round backing rules.

Z.1 supports a SECTOR decomposition, not a programme one directly. The sectors
mapped to federal_government in config.HOLDER_OF_SECTOR are:

  41  agency- and GSE-backed mortgage pools   the guarantee: GNMA, FNMA, FHLMC
  40  government-sponsored enterprises        retained portfolios, FHLBs
  31  federal government                      direct holdings, incl. direct student
  71  monetary authority                      Federal Reserve
  34  federal government retirement funds
  36  federal plus state and local (fallback) only where 31/21 are absent

LIMITATION, stated rather than worked around: Z.1 does not split sector 41 into
Ginnie Mae and the two GSEs. "Agency and GSE pools" is therefore reported as one
programme, and the Ginnie share of it cannot be separated from this source.

Student lending is handled as build_direct.py does: the federal share of the
student class is FL313066220 over the class level, which is sector 31 direct
holding, so direct student lending is separable even though consumer credit as an
instrument carries a federal share of zero.
"""
from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
LB = ROOT / "framework" / "labor_backing"
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(LB))

import config as C                                             # noqa: E402
from z1_loader import load_all, catalog                        # noqa: E402
from build_direct import (backing_table, receipts_shares,      # noqa: E402
                          _sector_series, holder_shares, series_of)

# Sectors 40 and 41 are COMBINED. In 2010 the GSEs consolidated their
# securitisation trusts on balance sheet (FAS 166/167), moving mortgages from
# sector 41 to sector 40: pools fall 0.2425 to 0.0498 and retained rises 0.0303
# to 0.2196, while the COMBINED figure is smooth, 0.2727 to 0.2694. Reporting
# them separately would report an accounting reclassification as a programme
# shift. Ginnie Mae sits inside sector 41 and Z.1 does not separate it.
FED_SECTORS = {"41": "gse_agency_guarantee", "40": "gse_agency_guarantee",
               "31": "federal_direct", "71": "federal_reserve",
               "34": "federal_retirement_funds", "36": "federal_fallback"}
BUSINESS = ["corporate_bonds", "corporate_loans", "noncorporate_business_debt",
            "commercial_mortgage", "corporate_equity"]


def main():
    A = load_all()
    cat = catalog()
    back, _, _ = backing_table()
    rec = receipts_shares()

    def lvl(codes):
        out = None
        for c in codes:
            s = series_of(A, c)
            out = s if out is None else out.add(s, fill_value=0.0)
        return out

    L = pd.DataFrame({cl["key"]: lvl(cl["liab"])
                      for cl in C.CLASSES}).dropna(how="all")
    years = [int(y) for y in L.index
             if L.loc[y].notna().all() and y in rec.index]

    def bshare(cl, y):
        k = cl["backing"]
        if k == "federal_receipts":
            return float(rec.loc[y, "federal_receipts_labour_share"])
        if k == "state_local_receipts":
            return float(rec.loc[y, "state_local_receipts_labour_share"])
        return back[k][0]

    ind = pd.read_csv(LB / "indirect_extension_timeseries.csv"
                      ).set_index("year")["indirect_labour_backing_of_business_revenue"]

    rows = []
    for y in years:
        for cl in C.CLASSES:
            k = cl["key"]
            lev = float(L.loc[y, k]) / 1000.0
            b_c = bshare(cl, y)
            b_s = (float(ind.loc[y]) if (k in BUSINESS and y in ind.index)
                   else b_c)
            instr = C.CLASS_HOLDER_INSTRUMENT[k]

            # programme split of the FEDERAL holder share of this class
            prog = {v: 0.0 for v in set(FED_SECTORS.values())}
            fed_total = 0.0
            if k == "student_loan":
                s = series_of(A, "FL313066220")
                f = (float(s[y]) / float(L.loc[y, "student_loan"])
                     if (y in s.index and L.loc[y, "student_loan"] > 0) else 0.0)
                prog["federal_direct"] = f
                fed_total = f
            elif instr == "3066000":
                fed_total = 0.0            # consumer credit: federal share zero
            else:
                sec = _sector_series(A, cat, instr)
                present = {c for c, (ser, _, _) in sec.items()
                           if y in ser.index}
                # mirror holder_shares: skip aggregates, skip fallbacks whose
                # components are present, and normalise on the same control total
                hs, _ = holder_shares(A, cat, instr, y)
                fed_total = 0.0 if np.isnan(hs["federal_government"]) \
                    else hs["federal_government"]
                raw = {}
                for c in present:
                    if c in C.AGGREGATE_SECTORS:
                        continue
                    if c in C.SECTOR_FALLBACK and any(
                            x in present for x in C.SECTOR_FALLBACK[c]):
                        continue
                    if c in FED_SECTORS:
                        raw[c] = float(sec[c][0][y])
                tot_raw = sum(raw.values())
                if tot_raw > 0:
                    for c, v in raw.items():
                        prog[FED_SECTORS[c]] += fed_total * v / tot_raw

            rows.append(dict(year=y, claim_class=k, level_bn=lev,
                             beta_central=b_c, beta_second=b_s,
                             fed_total=fed_total, **prog))
    P = pd.DataFrame(rows)
    P.to_csv(OUT / "s3_programme_panel.csv", index=False)

    # check the split reconstructs the federal holder share
    sp = P[sorted(set(FED_SECTORS.values()))].sum(axis=1)
    err = (sp - P["fed_total"]).abs().max()
    print(f"programme split reconstructs fed_total: max abs err {err:.2e}")

    out = []
    for y, g in P.groupby("year"):
        row = {"year": int(y)}
        for rule, bcol in (("central", "beta_central"),
                           ("second", "beta_second")):
            lb = (g["level_bn"] * g[bcol])
            tot = float(lb.sum())
            row[f"{rule}_lb_bn"] = tot
            row[f"{rule}_holder"] = float((lb * g["fed_total"]).sum()) / tot
            for p in sorted(set(FED_SECTORS.values())):
                row[f"{rule}_{p}"] = float((lb * g[p]).sum()) / tot
        out.append(row)
    S = pd.DataFrame(out).set_index("year")
    S.to_csv(OUT / "s3_programme_series.csv")

    progs = [p for p in sorted(set(FED_SECTORS.values()))
             if S[f"central_{p}"].abs().max() > 1e-6]
    print(f"\nprogrammes with non-trivial holdings: {progs}")

    for rule in ("central", "second"):
        print(f"\n=== {rule.upper()} RULE, holder leg by programme")
        cols = [f"{rule}_holder"] + [f"{rule}_{p}" for p in progs]
        show = [y for y in (1947, 1965, 1980, 1990, 2000, 2007, 2013, 2021,
                            2025) if y in S.index]
        d = S.loc[show, cols].round(4)
        d.columns = ["TOTAL"] + progs
        print(d.to_string())

    print("\n\nCONTRIBUTION TO EACH PHASE, both rules")
    for a, b, lab in [(1965, 2000, "guarantee phase 1965-2000"),
                      (2007, 2025, "borrowing phase 2007-2025"),
                      (2013, 2025, "post-2013")]:
        print(f"\n  {lab}")
        for rule in ("central", "second"):
            parts = " ".join(
                f"{p.split('_')[0][:6]}:{S.loc[b, f'{rule}_{p}'] - S.loc[a, f'{rule}_{p}']:+.4f}"
                for p in progs)
            tot = S.loc[b, f"{rule}_holder"] - S.loc[a, f"{rule}_holder"]
            print(f"    {rule:8s} holder total {tot:+.4f}   {parts}")

    json.dump({"programmes": progs,
               "split_reconstruction_max_err": float(err)},
              open(OUT / "s3_meta.json", "w"), indent=2)


if __name__ == "__main__":
    main()
