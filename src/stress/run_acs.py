"""Run the ACS household stress test across the scenario grid. Writes data/processed/stress/.

Grid: construct x scenario target x incidence variant, at rho central and omega central,
plus a rho and omega sensitivity at the central target under uniform incidence.

Reports, for every cell, the share of obligated households crossing DSTI 30, 40 and 50
percent and the dollars of mortgage service and rent those households owe. Replicate
intervals for the headline cells only.

The BASELINE row (no displacement) is produced first, because every crossing share has to be
read as an increment over a population that already has high DSTI for reasons unrelated to
AI. Reporting the post-shock level alone would be the same class of error as A6.
"""
import json, pathlib, sys, time
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
from src.stress import scenarios as SC
from src.stress import acs_engine as AE

OUT = pathlib.Path(__file__).parents[2] / "data" / "processed" / "stress"
OUT.mkdir(parents=True, exist_ok=True)

CONSTRUCTS = ["cognitive_AIOE", "cognitive_GPT", "embodied", "robot_reachable",
              "driving", "gated", "manipulation"]
HEADLINE = [("cognitive_AIOE", "central_10pct", "uniform"),
            ("cognitive_GPT", "central_10pct", "uniform"),
            ("embodied", "central_10pct", "uniform")]


def main():
    t0 = time.time()
    print("loading ACS ...")
    P, H = AE.load_acs()
    P, hh_idx = AE.link(P, H)
    print(f"  {len(P):,} workers, {len(H):,} households, "
          f"{H['wgtp'].sum()/1e6:.2f}m weighted, {time.time()-t0:.0f}s")

    B = SC.occupation_scores()
    pocc = {}
    occ = P["occp"].to_numpy()
    wq = P["wage_pctile_in_occ"].to_numpy(np.float64)
    pw = P["pwgtp"].to_numpy(np.float64)

    core = H["working_core"].to_numpy(bool)
    rows, prob_rows = [], []

    # ---------- baseline, no displacement ----------
    base = AE.simulate(P, H, hh_idx, np.zeros(len(P)), 0.0, 1.0, r_draws=1)
    for lab, mask in [("all", None), ("working_core", core.astype(float)),
                      ("non_working", (~core).astype(float))]:
        s = AE.weighted_stats(H, base, mask)
        rows.append({"construct": "BASELINE", "target": "none", "incidence": "none",
                     "rho": np.nan, "omega": np.nan, "sample": lab, **s})

    # ---------- grid ----------
    for construct in CONSTRUCTS:
        for tname, tshare in SC.TARGETS.items():
            PO = SC.occupation_probabilities(B, construct, tshare)
            prob_rows.append({"construct": construct, "target": tname,
                              "in_scope_employment": float(PO["in_scope_employment"].iloc[0]),
                              "capped": bool(PO["capped"].iloc[0]),
                              "scale_a": float(PO["scale_a"].iloc[0]),
                              "mean_p_in_scope": float(
                                  (PO["p_occ"] * PO["employment"]).sum()
                                  / PO["employment"].sum())})
            pm = dict(zip(PO["occp"].astype(int), PO["p_occ"]))
            p_occ_worker = pd.Series(occ).map(pm).fillna(0.0).to_numpy(np.float64)
            for inc in SC.INCIDENCE:
                pw_worker = SC.apply_incidence(p_occ_worker, wq, pw, inc)
                acc = AE.simulate(P, H, hh_idx, pw_worker,
                                  SC.RHO_GRID[1], SC.OMEGA["central"])
                for lab, mask in [("all", None), ("working_core", core.astype(float))]:
                    s = AE.weighted_stats(H, acc, mask)
                    rows.append({"construct": construct, "target": tname,
                                 "incidence": inc, "rho": SC.RHO_GRID[1],
                                 "omega": SC.OMEGA["central"], "sample": lab, **s})
                print(f"  {construct:16s} {tname:14s} {inc:18s} "
                      f"dsti50 {rows[-1]['share_dsti_50']*100:5.2f}%  "
                      f"[{time.time()-t0:.0f}s]")

    # ---------- rho and omega sensitivity, central target, uniform ----------
    for construct in ["cognitive_AIOE", "embodied"]:
        PO = SC.occupation_probabilities(B, construct, SC.TARGETS["central_10pct"])
        pm = dict(zip(PO["occp"].astype(int), PO["p_occ"]))
        p_occ_worker = pd.Series(occ).map(pm).fillna(0.0).to_numpy(np.float64)
        pw_worker = SC.apply_incidence(p_occ_worker, wq, pw, "uniform")
        for rho in SC.RHO_GRID:
            for oname, om in SC.OMEGA.items():
                acc = AE.simulate(P, H, hh_idx, pw_worker, rho, om)
                s = AE.weighted_stats(H, acc, core.astype(float))
                rows.append({"construct": construct, "target": "central_10pct",
                             "incidence": "uniform_sensitivity", "rho": rho,
                             "omega": om, "sample": "working_core", **s})

    T = pd.DataFrame(rows)
    T.to_csv(OUT / "acs_stress_grid.csv", index=False)
    pd.DataFrame(prob_rows).to_csv(OUT / "acs_scenario_calibration.csv", index=False)

    # ---------- replicate intervals, headline cells only ----------
    iv = []
    mort = H["mort"].to_numpy(np.float64); rent = H["rent"].to_numpy(np.float64)
    has = (mort + rent) > 0
    for construct, tname, inc in HEADLINE:
        PO = SC.occupation_probabilities(B, construct, SC.TARGETS[tname])
        pm = dict(zip(PO["occp"].astype(int), PO["p_occ"]))
        p_occ_worker = pd.Series(occ).map(pm).fillna(0.0).to_numpy(np.float64)
        pw_worker = SC.apply_incidence(p_occ_worker, wq, pw, inc)
        acc = AE.simulate(P, H, hh_idx, pw_worker, SC.RHO_GRID[1], SC.OMEGA["central"])
        for t in AE.DSTI_THRESHOLDS:
            k = f"dsti_{int(t*100)}"
            ind = acc[k]
            fn = lambda w, ind=ind: float((ind * w * core)[has].sum() / (w * core)[has].sum())
            th, se, lo, hi = AE.replicate_interval(H, acc, fn)
            iv.append({"construct": construct, "target": tname, "incidence": inc,
                       "statistic": f"share_{k}_working_core", "estimate": th,
                       "replicate_se": se, "ci95_low": lo, "ci95_high": hi,
                       "simulation_sd_across_draws": acc["_sim_sd"][k]})
        for t in AE.DSTI_THRESHOLDS:
            k = f"dsti_{int(t*100)}"
            ind = acc[k]
            fn = lambda w, ind=ind: float((ind * w * core * mort).sum())
            th, se, lo, hi = AE.replicate_interval(H, acc, fn)
            iv.append({"construct": construct, "target": tname, "incidence": inc,
                       "statistic": f"mortgage_dollars_{k}_working_core", "estimate": th,
                       "replicate_se": se, "ci95_low": lo, "ci95_high": hi,
                       "simulation_sd_across_draws": np.nan})
    IV = pd.DataFrame(iv)
    IV.to_csv(OUT / "acs_stress_intervals.csv", index=False)
    (OUT / "scenario_definition.json").write_text(json.dumps(SC.describe(), indent=2))

    pd.set_option("display.width", 250)
    print("\n=== BASELINE, no displacement ===")
    b = T[T["construct"] == "BASELINE"]
    print(b[["sample", "obligated_households_weighted", "share_dsti_30", "share_dsti_40",
             "share_dsti_50"]].round(4).to_string(index=False))
    print("\n=== INCIDENCE SPREAD, central target, working core, share crossing DSTI 50 ===")
    g = T[(T["target"] == "central_10pct") & (T["sample"] == "working_core")
          & T["incidence"].isin(SC.INCIDENCE)]
    piv = g.pivot_table(index="construct", columns="incidence", values="share_dsti_50")
    piv["max_over_min"] = piv.max(axis=1) / piv.min(axis=1)
    print((piv * 100).round(3).to_string())
    print(f"\ntotal {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
