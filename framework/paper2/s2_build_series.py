"""
Session 2. Builds the per-class, per-year panel and from it:

  1. the CENTRAL sovereign-share series, rebuilt (a check against the accounts)
  2. the ALTERNATIVE-CLASSIFICATION series: agency pools not federal
  3. the SECOND-ROUND series: the one-step rule relaxed

Reads the accounts' own loaders and config. WRITES NOTHING outside
framework/paper2/ and changes nothing in framework/labor_backing/.

Definitions, taken from the accounts so the series are comparable:

  central            holder leg = federal share of every class, from Z.1 sectors;
                     sectors 40 (GSEs) and 41 (agency and GSE pools) map to federal,
                     as does 71 (monetary authority)
  agency pools not   the accounts' own robustness definition: remove the federal
  federal            holder leg of home_mortgage and multifamily_mortgage entirely
  second round       business classes carry the B2 indirect coefficient for that year
                     instead of zero; available from 1959

Union = holder + obligor - overlap, exactly as build_direct.py computes it.
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

import config as C                                            # noqa: E402
from z1_loader import load_all, annual, catalog               # noqa: E402
from build_direct import (backing_table, receipts_shares,     # noqa: E402
                          holder_shares, series_of)

POOL_CLASSES = ["home_mortgage", "multifamily_mortgage"]
BUSINESS_CLASSES = ["corporate_bonds", "corporate_loans",
                    "noncorporate_business_debt", "commercial_mortgage",
                    "corporate_equity"]


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

    levels = {cl["key"]: lvl(cl["liab"]) for cl in C.CLASSES}
    L = pd.DataFrame(levels).dropna(how="all")
    years = [int(y) for y in L.index
             if L.loc[y].notna().all() and y in rec.index]
    print(f"years with complete class levels and receipts: "
          f"{min(years)}-{max(years)}  n={len(years)}")

    def bshare(cl, y):
        kind = cl["backing"]
        if kind == "federal_receipts":
            return float(rec.loc[y, "federal_receipts_labour_share"])
        if kind == "state_local_receipts":
            return float(rec.loc[y, "state_local_receipts_labour_share"])
        return back[kind][0]

    ind = pd.read_csv(LB / "indirect_extension_timeseries.csv").set_index("year")
    ind_beta = ind["indirect_labour_backing_of_business_revenue"]

    rows = []
    for y in years:
        for cl in C.CLASSES:
            k = cl["key"]
            lev = float(L.loc[y, k]) / 1000.0          # $bn
            # Follow build_direct.py exactly: the holder lookup uses
            # CLASS_HOLDER_INSTRUMENT, consumer credit (3066000) carries a
            # federal share of zero, and student loans are overridden by the
            # federal government's own direct holding FL313066220.
            instr = C.CLASS_HOLDER_INSTRUMENT[k]
            try:
                shares, _ = holder_shares(A, cat, instr, y)
                fed = shares.get("federal_government", np.nan)
            except Exception:
                fed = np.nan
            if k == "student_loan":
                s = series_of(A, "FL313066220")
                fed = (float(s[y]) / float(L.loc[y, "student_loan"])
                       if (y in s.index and L.loc[y, "student_loan"] > 0)
                       else np.nan)
            elif instr == "3066000":
                fed = 0.0
            if np.isnan(fed):
                fed = 0.0
            rows.append(dict(year=y, claim_class=k, level_bn=lev,
                             beta_central=bshare(cl, y),
                             beta_second_round=(float(ind_beta.loc[y])
                                                if (k in BUSINESS_CLASSES
                                                    and y in ind_beta.index)
                                                else bshare(cl, y)),
                             federal_holder_share=fed,
                             obligor=C.OBLIGOR_OF_CLASS[k]))
    P = pd.DataFrame(rows)
    P.to_csv(OUT / "s2_panel.csv", index=False)
    print(f"panel: {len(P)} rows, "
          f"federal holder share missing in {int(P.federal_holder_share.isna().sum())}")

    def series(beta_col, drop_pool_holder=False):
        out = []
        for y, g in P.groupby("year"):
            g = g.dropna(subset=["federal_holder_share"])
            lb = g["level_bn"] * g[beta_col]
            tot = float(lb.sum())
            if tot <= 0:
                continue
            fed_hold = float((lb * g["federal_holder_share"]).sum())
            if drop_pool_holder:
                m = g["claim_class"].isin(POOL_CLASSES)
                fed_hold -= float((lb[m] * g.loc[m, "federal_holder_share"]).sum())
            fedm = g["obligor"] == "federal_government"
            fed_oblig = float(lb[fedm].sum())
            # build_direct.py nets the overlap on TREASURY only
            tm = g["claim_class"] == "treasury"
            overlap = float((lb[tm] * g.loc[tm,
                                            "federal_holder_share"]).sum())
            union = fed_hold + fed_oblig - overlap
            out.append(dict(year=int(y), labour_backed_bn=tot,
                            holder=fed_hold / tot, obligor=fed_oblig / tot,
                            overlap=overlap / tot, union=union / tot))
        return pd.DataFrame(out).set_index("year")

    central = series("beta_central")
    altcls = series("beta_central", drop_pool_holder=True)
    second = series("beta_second_round")

    S = pd.DataFrame({
        "central_union": central["union"],
        "central_holder": central["holder"],
        "central_obligor": central["obligor"],
        "agency_not_federal_union": altcls["union"],
        "agency_not_federal_holder": altcls["holder"],
        "second_round_union": second["union"],
        "second_round_holder": second["holder"],
        "second_round_obligor": second["obligor"],
        "labour_backed_bn_central": central["labour_backed_bn"],
        "labour_backed_bn_second": second["labour_backed_bn"],
    })
    S["agency_gap"] = S["central_union"] - S["agency_not_federal_union"]
    S.to_csv(OUT / "s2_series.csv")

    # check against the accounts' own published series
    pub = pd.read_csv(LB / "direct_ratio_timeseries.csv").set_index("year")
    chk = S.join(pub["sovereign_share_union"], how="inner")
    d = (chk["central_union"] - chk["sovereign_share_union"]).abs()
    print(f"\nrebuild check against direct_ratio_timeseries.csv: "
          f"max abs diff {d.max():.6f}, mean {d.mean():.6f}")

    print("\nSERIES, selected years")
    cols = ["central_union", "agency_not_federal_union", "agency_gap",
            "second_round_union"]
    show = [y for y in (1947, 1965, 1980, 1990, 2000, 2007, 2008, 2010,
                        2013, 2021, 2025) if y in S.index]
    print(S.loc[show, cols].round(4).to_string())

    json.dump({"years": [int(S.index.min()), int(S.index.max())],
               "rebuild_max_abs_diff": float(d.max())},
              open(OUT / "s2_meta.json", "w"), indent=2)


if __name__ == "__main__":
    main()
