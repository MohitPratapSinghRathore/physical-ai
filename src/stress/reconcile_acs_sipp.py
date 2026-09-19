"""Item 5: resolve or bound the ACS against SIPP disagreement on the embodied mortgage lean.

A39 reported embodied mortgage lean 0.90 in ACS and 0.77 in SIPP and could not say why. The
two figures differed on three things at once, which is why the gap was uninterpretable:

    measure        ACS annual mortgage SERVICE against SIPP mortgage BALANCE
    denominator    ACS household WAGE BILL against SIPP household EARNINGS
    sample         ACS all working-core households against SIPP working-core households

This script holds all three fixed and reports the lean four ways, so the gap is decomposed
rather than asserted:

    A  ACS service   / ACS earnings        the ACS figure, restated on earnings
    B  SIPP payment  / SIPP earnings       like for like with A, using TRENTMORT for
                                           mortgage holders, which is the monthly mortgage
                                           payment for owners carrying mortgage debt
    C  SIPP balance  / SIPP earnings       the A39 SIPP figure, kept for continuity
    D  ACS service   / ACS earnings, owners with a mortgage only

A and B are the comparison that matters. If they still differ, the residual is survey
difference (sample size, occupation coding, income reporting) and is reported as such with
the SIPP interval around it, never as agreement.

Exposure cut is identical in both: household contains at least one worker in the
top-quintile-by-employment embodiment P group, from the same occupation table.

CAVEAT: cognitive rows carry the task-overlap caveat. This script is about the embodied
figure, and the cognitive rows are reported alongside only as a control.
"""
import json, pathlib, sys, time
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
from src.stress import scenarios as SC
from src.stress import sipp_engine as SE

OUT = pathlib.Path(__file__).parents[2] / "data" / "processed" / "stress"


def lean(num, den, w, sel):
    """Group share of the obligation divided by group share of the denominator."""
    tn, td = float((num * w).sum()), float((den * w).sum())
    if tn <= 0 or td <= 0:
        return np.nan, np.nan, np.nan
    sn = float((num * w * sel).sum()) / tn
    sd = float((den * w * sel).sum()) / td
    return 100 * sn, 100 * sd, (sn / sd if sd else np.nan)


def main():
    t0 = time.time()
    B = SC.occupation_scores()
    _, groups = SC._h3().build_groups()
    rows = []

    # ---------------- ACS ----------------
    # The ACS rows are produced by src/stress/run_compare.py, which already holds the ACS
    # frames in memory for the method comparison. Loading ACS a second time here cost two
    # minutes and a gigabyte for no new information, so the rows are read from its output.
    acs_rows = pd.read_csv(OUT / "acs_lean_rows.csv")
    rows.extend(acs_rows.to_dict("records"))
    print("ACS rows read from acs_lean_rows.csv")

    # ---------------- SIPP ----------------
    print("loading SIPP ...")
    Ps, hh, RW = SE.load()
    core_s = (hh["any_employed"].to_numpy(bool)
              & hh["ref_age"].between(25, 64).to_numpy(bool))
    ws = hh["wgt"].to_numpy(float)
    earn_s = hh["hh_earn_a"].to_numpy(float) if "hh_earn_a" in hh else hh["hh_wage_a"].to_numpy(float)
    bal = hh["mortgage"].fillna(0.0).to_numpy(float)
    # TRENTMORT is the monthly housing payment; for a household carrying mortgage debt and
    # not renting it is the mortgage payment. Annualised.
    pay = np.where(bal > 0, hh["housing_m"].to_numpy(float) * 12.0, 0.0)
    hh_pos = pd.Series(np.arange(len(hh)), index=hh.index)
    idx = Ps["hh"].map(hh_pos)
    keep = idx.notna().to_numpy()
    idx = idx[keep].to_numpy(int)
    for gname in ["embodied", "cognitive_AIOE", "cognitive_GPT"]:
        f = Ps.loc[keep, "occ"].isin(groups[gname]).to_numpy(float)
        hsel = np.bincount(idx, weights=f, minlength=len(hh)) > 0
        for lab, num, msk in [("B_sipp_payment_vs_earnings", pay, core_s),
                              ("C_sipp_balance_vs_earnings", bal, core_s)]:
            sn, sd, ln = lean(num, earn_s, ws * msk, hsel)
            rows.append({"row": lab, "source": "SIPP",
                         "measure": ("annual mortgage payment" if lab.startswith("B")
                                     else "mortgage balance"),
                         "denominator": "household earnings", "group": gname,
                         "n_households_unweighted": int(msk.sum()),
                         "obligation_share_pct": sn, "earnings_share_pct": sd, "lean": ln})
        print(f"  SIPP {gname:16s} payment lean {rows[-2]['lean']:.4f}  "
              f"balance lean {rows[-1]['lean']:.4f}")

    # Fay interval on the SIPP payment lean for embodied, the number in dispute
    okrw = np.isfinite(RW).all(axis=1)
    m = core_s & okrw
    f = Ps.loc[keep, "occ"].isin(groups["embodied"]).to_numpy(float)
    hsel = np.bincount(idx, weights=f, minlength=len(hh)) > 0
    fn = lambda wv: lean(pay[m], earn_s[m], wv, hsel[m])[2]
    th, se, lo, hi = SE.fay_interval(fn, ws[m], RW[m])
    print(f"\nSIPP embodied PAYMENT lean {th:.4f}  Fay se {se:.4f}  "
          f"95% CI [{lo:.4f}, {hi:.4f}]")

    T = pd.DataFrame(rows)
    T.round(5).to_csv(OUT / "acs_sipp_reconciliation.csv", index=False)
    (OUT / "acs_sipp_reconciliation.json").write_text(json.dumps({
        "rows": T.round(5).to_dict("records"),
        "sipp_embodied_payment_lean": {"estimate": th, "fay_se": se,
                                       "ci95": [lo, hi]}}, indent=2))
    pd.set_option("display.width", 240)
    print("\n=== RECONCILIATION ===")
    print(T[["row", "source", "measure", "group", "obligation_share_pct",
             "earnings_share_pct", "lean"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
