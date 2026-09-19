"""Run the SIPP household stress test. Writes data/processed/stress/sipp_*.

Smaller sample than ACS, so the grid is narrower: three constructs, three targets, three
incidence variants, at rho central and omega central. Fay intervals for the headline cells.

What SIPP adds over ACS: liquid buffers and runway, vehicle and unsecured balances held by
distressed households, and a second measurement of the same DSTI question on an independent
survey, which the claims checklist requires.
"""
import json, pathlib, sys, time
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
from src.stress import scenarios as SC
from src.stress import sipp_engine as SE

OUT = pathlib.Path(__file__).parents[2] / "data" / "processed" / "stress"
OUT.mkdir(parents=True, exist_ok=True)
CONSTRUCTS = ["cognitive_AIOE", "cognitive_GPT", "embodied", "driving", "manipulation"]


def main():
    t0 = time.time()
    print("loading SIPP ...")
    P, hh, RW = SE.load()
    core = hh["any_employed"].to_numpy(bool) & hh["ref_age"].between(25, 64).to_numpy(bool)
    okrw = np.isfinite(RW).all(axis=1)
    print(f"  {len(P):,} workers, {len(hh):,} households, working core {core.sum():,}, "
          f"with replicate weights {(core & okrw).sum():,}  [{time.time()-t0:.0f}s]")

    B = SC.occupation_scores()
    occ = P["occ"].to_numpy()
    wq = P["wage_pctile_in_occ"].to_numpy(float)
    pw = P["pwgt"].to_numpy(float)
    w0 = hh["wgt"].to_numpy(float)

    rows = []
    base = SE.simulate(P, hh, np.zeros(len(P)), 0.0, 1.0, r_draws=1)
    for lab, msk in [("all", np.ones(len(hh), bool)), ("working_core", core),
                     ("non_working", ~core)]:
        rows.append({"construct": "BASELINE", "target": "none", "incidence": "none",
                     "sample": lab, **SE.stats(hh, base, w0 * msk)})

    for c in CONSTRUCTS:
        for tname, tshare in SC.TARGETS.items():
            PO = SC.occupation_probabilities(B, c, tshare)
            pm = dict(zip(PO["occp"].astype(int), PO["p_occ"]))
            p_occ = pd.Series(occ).map(pm).fillna(0.0).to_numpy(float)
            for inc in SC.INCIDENCE:
                pwk = SC.apply_incidence(p_occ, wq, pw, inc)
                acc = SE.simulate(P, hh, pwk, SC.RHO_GRID[1], SC.OMEGA["central"])
                rows.append({"construct": c, "target": tname, "incidence": inc,
                             "sample": "working_core", **SE.stats(hh, acc, w0 * core)})
            print(f"  {c:16s} {tname:14s} dsti50 {rows[-1]['share_dsti_50']*100:5.2f}%  "
                  f"runway<3m {rows[-1]['share_runway_short_under_3']*100:5.2f}%  "
                  f"[{time.time()-t0:.0f}s]")
    T = pd.DataFrame(rows)
    T.to_csv(OUT / "sipp_stress_grid.csv", index=False)

    # Fay intervals, headline cells
    iv = []
    msk = core & okrw
    RWm = RW[msk]
    for c in ["cognitive_AIOE", "embodied"]:
        PO = SC.occupation_probabilities(B, c, SC.TARGETS["central_10pct"])
        pm = dict(zip(PO["occp"].astype(int), PO["p_occ"]))
        p_occ = pd.Series(occ).map(pm).fillna(0.0).to_numpy(float)
        pwk = SC.apply_incidence(p_occ, wq, pw, "uniform")
        acc = SE.simulate(P, hh, pwk, SC.RHO_GRID[1], SC.OMEGA["central"])
        housing = hh["housing_m"].to_numpy(float) * 12.0
        has = housing > 0
        for key in ["dsti_50", "runway_short_under_3", "runway_house_under_3"]:
            ind = acc[key][msk]
            if key.startswith("dsti"):
                h = has[msk]
                fn = lambda w, ind=ind, h=h: float((ind * w)[h].sum() / w[h].sum())
            else:
                fn = lambda w, ind=ind: float((ind * w).sum() / w.sum())
            th, se, lo, hi = SE.fay_interval(fn, w0[msk], RWm)
            iv.append({"construct": c, "statistic": key, "estimate": th,
                       "fay_se": se, "ci95_low": lo, "ci95_high": hi})
    pd.DataFrame(iv).to_csv(OUT / "sipp_stress_intervals.csv", index=False)

    pd.set_option("display.width", 250)
    print("\n=== BASELINE ===")
    print(T[T["construct"] == "BASELINE"][
        ["sample", "share_dsti_50", "share_runway_house_under_3",
         "share_runway_house_under_6"]].round(4).to_string(index=False))
    print("\n=== central target, working core ===")
    g = T[(T["target"] == "central_10pct")]
    print(g[["construct", "incidence", "share_dsti_50", "share_runway_short_under_3",
             "share_runway_short_under_6", "vehicle_balance_dsti_50",
             "housing_dollars_dsti_50"]].round(4).to_string(index=False))
    print(f"\ntotal {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
