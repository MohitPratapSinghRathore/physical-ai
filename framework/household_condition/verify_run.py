"""
Run step 1. Verify the specification is unchanged and assert the survey
invariants and plausibility preconditions BEFORE any result is computed.

Exits non-zero if any assertion fails.
"""
from pathlib import Path
import hashlib
import io
import json
import sys
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "household_condition"
OUT = ROOT / "framework" / "household_condition"

SPEC_SHA = "476e093703da92d8eacf85332f2d6f637851b2e925b5a34bcb441d1e35f21f9b"
HH_2022, HH_2019 = 131.31, 128.64      # millions, from FEASIBILITY section 1
TOL_HH = 0.01                          # millions
WEALTH_EDGES = [0, .25, .50, .75, .90, .99, 1.0]
WEALTH_SHARES = [.25, .25, .25, .15, .09, .01]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def load(year):
    z = zipfile.ZipFile(RAW / f"scfp{year}s.zip")
    return pd.read_stata(io.BytesIO(z.read(z.namelist()[0])))


def wpct(x, w):
    """Weighted cumulative percentile of each observation."""
    o = np.argsort(np.asarray(x), kind="stable")
    cw = np.cumsum(w.to_numpy()[o]) / w.sum()
    pct = np.empty(len(x))
    pct[o] = cw
    return pd.Series(pct, index=x.index)


def main():
    rep, fail = {}, []

    got = sha256(OUT / "SPECIFICATION.md")
    rep["specification_sha256"] = got
    rep["specification_unchanged"] = got == SPEC_SHA
    print(f"SPECIFICATION.md sha256 {got}")
    print(f"  expected              {SPEC_SHA}")
    print(f"  UNCHANGED: {got == SPEC_SHA}")
    if got != SPEC_SHA:
        fail.append("SPECIFICATION.md has changed")

    print("\nINVARIANT 1: weights sum to the household count over all five "
          "implicates")
    for yr, expect in ((2022, HH_2022), (2019, HH_2019)):
        df = load(yr)
        tot = float(df["wgt"].sum() / 1e6)
        n_imp = int(len(df) / df["yy1"].nunique())
        per = float(df.loc[df["y1"] % 10 == 1, "wgt"].sum() / 1e6)
        ok = abs(tot - expect) < TOL_HH and n_imp == 5
        rep[f"invariant1_{yr}"] = {
            "weighted_households_m": round(tot, 4),
            "expected_m": expect, "implicates": n_imp,
            "single_implicate_m": round(per, 4),
            "ratio_full_to_single": round(tot / per, 4), "pass": ok}
        print(f"  {yr}: {tot:.2f}m over {n_imp} implicates "
              f"(one implicate {per:.2f}m, ratio {tot/per:.2f})  "
              f"{'OK' if ok else 'FAIL'}")
        if not ok:
            fail.append(f"weight invariant failed for {yr}")

    print("\nINVARIANT 2: weighted rank cuts give the documented population "
          "shares")
    df = load(2022)
    i1 = df[df["y1"] % 10 == 1].copy()
    i1["wgt5"] = i1["wgt"] * 5
    W = i1["wgt5"].sum()

    q = wpct(i1["wageinc"], i1["wgt5"])
    qcut = pd.cut(q, [0, .2, .4, .6, .8, 1.0], labels=[1, 2, 3, 4, 5],
                  include_lowest=True)
    qshare = (i1.groupby(qcut, observed=True)["wgt5"].sum() / W)
    ok_q = bool(np.allclose(qshare.to_numpy(), 0.20, atol=0.01))
    print(f"  wage quintiles: {[round(v,4) for v in qshare]}  "
          f"{'OK' if ok_q else 'FAIL'}")
    rep["invariant2_wage_quintile_shares"] = [round(float(v), 4)
                                              for v in qshare]

    wl = wpct(i1["networth"], i1["wgt5"])
    wcut = pd.cut(wl, WEALTH_EDGES,
                  labels=["p0-25", "p25-50", "p50-75", "p75-90", "p90-99",
                          "top1"], include_lowest=True)
    wshare = (i1.groupby(wcut, observed=True)["wgt5"].sum() / W)
    ok_w = bool(np.allclose(wshare.to_numpy(), WEALTH_SHARES, atol=0.01))
    print(f"  wealth groups : {[round(v,4) for v in wshare]}  "
          f"{'OK' if ok_w else 'FAIL'}")
    rep["invariant2_wealth_group_shares"] = [round(float(v), 4)
                                             for v in wshare]
    if not (ok_q and ok_w):
        fail.append("weighted rank cuts do not reproduce population shares")

    print("\nPLAUSIBILITY PRECONDITIONS (baseline, before any shift)")
    pre = {}
    neg_inc = int((df["income"] < 0).sum())
    zero_inc = int((df["income"] <= 0).sum())
    pre["rows_income_negative"] = neg_inc
    pre["rows_income_nonpositive"] = zero_inc
    pre["rows_total"] = int(len(df))
    print(f"  rows with income < 0: {neg_inc}")
    print(f"  rows with income <= 0: {zero_inc} "
          f"({100*zero_inc/len(df):.2f}%) -- excluded from ratios and counted")

    for c in ("wageinc", "intdivinc", "kginc", "bussefarminc"):
        pre[f"{c}_min"] = float(df[c].min())
        pre[f"{c}_max"] = float(df[c].max())
    neg_w = int((df["wageinc"] < 0).sum())
    pre["rows_wageinc_negative"] = neg_w
    print(f"  rows with wageinc < 0: {neg_w}")
    print(f"  bussefarminc min {df['bussefarminc'].min():,.0f} "
          f"(business losses are real and are kept)")

    pti = df["pirtotal"]
    pre["pirtotal_min"] = float(pti.min())
    pre["pirtotal_max"] = float(pti.max())
    pre["pirtotal_above_1"] = int((pti > 1).sum())
    print(f"  pirtotal range [{pti.min():.4f}, {pti.max():.4f}]; "
          f"{int((pti>1).sum())} rows above 1.0 (PTI is not a share and is "
          f"not bounded above)")

    # Balances and payments must be non-negative. Business equity is the one
    # exception in the data: a household may report a business of negative net
    # value. Section 9 bound 1 requires ownership shares in [0,1], which forces
    # such weights to be floored at zero when used as an allocation base.
    # Recorded, not treated as a failure. See DEVIATIONS.md D1.
    neg_ok = {"bus", "actbus"}
    for c in ("debt", "tpay", "mrthel", "ccbal", "install", "stocks", "nmmf",
              "retqliq", "annuit", "bus"):
        n_neg = int((df[c] < 0).sum())
        pre[f"{c}_min"] = float(df[c].min())
        pre[f"{c}_rows_negative"] = n_neg
        if n_neg and c not in neg_ok:
            fail.append(f"{c} has {n_neg} negative values")
        elif n_neg:
            agg_neg = float((df.loc[df[c] < 0, c]
                             * df.loc[df[c] < 0, "wgt"]).sum() / 1e9)
            pre[f"{c}_negative_aggregate_bn"] = round(agg_neg, 4)
            print(f"  {c}: {n_neg} negative rows, min {df[c].min():,.0f}, "
                  f"aggregate {agg_neg:,.4f}bn -- floored at zero as an "
                  f"allocation weight per section 9 bound 1 (D1)")
    print("  all other balance and payment variables non-negative: "
          f"{'OK' if not fail else 'see failures'}")

    pre["pir40_is_binary"] = sorted(df["pir40"].unique().tolist())
    rep["plausibility_preconditions"] = pre

    aggW = float((df["wageinc"] * df["wgt"]).sum() / 1e9)
    aggI = float((df["income"] * df["wgt"]).sum() / 1e9)
    rep["aggregate_wage_bill_bn"] = round(aggW, 1)
    rep["aggregate_income_bn"] = round(aggI, 1)
    print(f"\n  aggregate wage bill W = {aggW:,.1f}bn")
    print(f"  aggregate income      = {aggI:,.1f}bn")

    zrw = zipfile.ZipFile(RAW / "scf2022rw1s.zip")
    rw = pd.read_stata(io.BytesIO(zrw.read(zrw.namelist()[0])))
    rcols = [c for c in rw.columns if c.lower().startswith("wt1b")]
    rep["replicate_weights"] = {"rows": int(len(rw)),
                                "replicates": len(rcols)}
    print(f"  replicate weights: {len(rw)} rows x {len(rcols)} replicates")

    (OUT / "run_verification.json").write_text(
        json.dumps(rep, indent=2, default=float), encoding="utf-8")

    print()
    if fail:
        print("VERIFICATION FAILED")
        for f in fail:
            print("  " + f)
        sys.exit(1)
    print("VERIFICATION PASSED. The run may proceed.")


if __name__ == "__main__":
    main()
