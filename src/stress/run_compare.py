"""Item 3: rerun the repository's share-based debt-at-risk figures through the engine.

The two methods answer different questions and the table below keeps them apart rather than
pretending they are rival estimates of one number.

    SHARE-BASED (retired). For each household, attribute its mortgage service and rent in
    proportion to the fraction of its wage income earned in exposed occupations, times the
    scenario displacement intensity. This is the mechanical rule every earlier figure in
    this repository used, reproduced here EXACTLY so the comparison is like for like, and
    computed on the same households, the same scenario and the same exposure construct as
    the engine figure beside it.

    ENGINE. Simulate displacement worker by worker, recompute household income including
    non-wage income and reemployment, and count the mortgage service and rent owed by
    households whose debt-service-to-income crosses a threshold, NET OF the baseline share
    that already crosses it without any shock.

The ratio of the two is the quantity item 3 asks for. A ratio far from 1 does not by itself
condemn either method: the share-based number is "obligations sitting on exposed wages" and
the engine number is "obligations sitting on households the shock actually pushes into
distress". The paper needs the second. The point of the table is to show how far apart they
are and in which direction, so that every superseded figure can be corrected by the right
order of magnitude rather than silently reused.

CAVEAT on every cognitive row: AIOE and Eloundou GPT measure TASK OVERLAP, not displacement
and not timing.
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


def share_based(H, hh_idx, wage, p_worker, n_hh):
    """The retired rule, reproduced exactly.

    exposed_wage_fraction = (sum of p_i * wage_i) / (sum of wage_i) within the household;
    attributed obligation = obligation * exposed_wage_fraction.
    """
    num = np.bincount(hh_idx, weights=p_worker * wage, minlength=n_hh)
    den = np.bincount(hh_idx, weights=wage, minlength=n_hh)
    frac = np.where(den > 0, num / np.maximum(den, 1e-9), 0.0)
    w = H["wgtp"].to_numpy(np.float64)
    return {"share_based_mortgage": float((H["mort"].to_numpy(np.float64) * frac * w).sum()),
            "share_based_rent": float((H["rent"].to_numpy(np.float64) * frac * w).sum())}


def main():
    t0 = time.time()
    print("loading ACS (no replicate weights) ...")
    P, H = AE.load_acs(with_reps=False)
    P, hh_idx = AE.link(P, H)
    n_hh = len(H)
    wage = P["wage"].to_numpy(np.float64)
    occ = P["occp"].to_numpy()
    wq = P["wage_pctile_in_occ"].to_numpy(np.float64)
    pw = P["pwgtp"].to_numpy(np.float64)
    core = H["working_core"].to_numpy(bool)
    mort = H["mort"].to_numpy(np.float64)
    rent = H["rent"].to_numpy(np.float64)
    w = H["wgtp"].to_numpy(np.float64)
    print(f"  {len(P):,} workers, {n_hh:,} households, {w.sum()/1e6:.2f}m weighted "
          f"[{time.time()-t0:.0f}s]")

    B = SC.occupation_scores()
    base = AE.simulate(P, H, hh_idx, np.zeros(len(P)), 0.0, 1.0, r_draws=1)
    base_ind = {f"dsti_{int(t*100)}": base[f"dsti_{int(t*100)}"] for t in AE.DSTI_THRESHOLDS}

    rows = []
    for c in CONSTRUCTS:
        for tname, tshare in SC.TARGETS.items():
            PO = SC.occupation_probabilities(B, c, tshare)
            pm = dict(zip(PO["occp"].astype(int), PO["p_occ"]))
            p_occ = pd.Series(occ).map(pm).fillna(0.0).to_numpy(np.float64)
            for inc in SC.INCIDENCE:
                pwk = SC.apply_incidence(p_occ, wq, pw, inc)
                sb = share_based(H, hh_idx, wage, pwk, n_hh)
                acc = AE.simulate(P, H, hh_idx, pwk, SC.RHO_GRID[1], SC.OMEGA["central"])
                r = {"construct": c, "target": tname, "incidence": inc,
                     "share_based_mortgage": sb["share_based_mortgage"],
                     "share_based_rent": sb["share_based_rent"]}
                for t in AE.DSTI_THRESHOLDS:
                    k = f"dsti_{int(t*100)}"
                    d = np.maximum(acc[k] - base_ind[k], 0.0)
                    r[f"engine_mortgage_{k}"] = float((d * w * mort).sum())
                    r[f"engine_rent_{k}"] = float((d * w * rent).sum())
                    r[f"ratio_mortgage_{k}"] = (r[f"engine_mortgage_{k}"]
                                                / r["share_based_mortgage"]
                                                if r["share_based_mortgage"] else np.nan)
                    r[f"ratio_rent_{k}"] = (r[f"engine_rent_{k}"] / r["share_based_rent"]
                                            if r["share_based_rent"] else np.nan)
                rows.append(r)
            print(f"  {c:16s} {tname:14s} "
                  f"share ${rows[-1]['share_based_mortgage']/1e9:8.1f}bn  "
                  f"engine ${rows[-1]['engine_mortgage_dsti_50']/1e9:7.1f}bn  "
                  f"ratio {rows[-1]['ratio_mortgage_dsti_50']:.3f}  [{time.time()-t0:.0f}s]")
    T = pd.DataFrame(rows)
    T.to_csv(OUT / "method_comparison.csv", index=False)

    # ------------------------------------------------------------------
    # A38 CORRECTION. The five-way share table was computed on all housing records with a
    # positive weight, which includes VACANT units (NP = 0, 14.0m weighted, 9.6 percent).
    # Vacant units have no occupants, no income and no tenure, so they contributed zero to
    # every dollar column but were counted in the HOUSEHOLD column and landed in the
    # non-working class. The dollar shares in A38 are therefore correct and the household
    # percentages are not. Recomputed here on occupied units only.
    # ------------------------------------------------------------------
    _, groups = SC._h3().build_groups()
    flags = {}
    for gname in ["cognitive_AIOE", "cognitive_GPT", "embodied"]:
        f = P["occp"].isin(groups[gname]).to_numpy(float)
        flags[gname] = np.bincount(hh_idx, weights=f, minlength=n_hh) > 0
    hh_earn = np.bincount(hh_idx, weights=wage, minlength=n_hh)
    five = []
    for cog in ["cognitive_AIOE", "cognitive_GPT"]:
        c_, e_ = flags[cog], flags["embodied"]
        klass = np.where(~core, "non_working",
                 np.where(c_ & e_, "both",
                  np.where(c_ & ~e_, "cognitive_only",
                   np.where(~c_ & e_, "embodied_only", "middle_exposure_working"))))
        tm, tr = float((mort * w).sum()), float((rent * w).sum())
        tw, th = float((hh_earn * w).sum()), float(w.sum())
        for k in ["cognitive_only", "embodied_only", "both",
                  "middle_exposure_working", "non_working"]:
            s = klass == k
            r = {"cognitive_definition": cog, "class": k,
                 "households_pct": 100 * float(w[s].sum()) / th,
                 "wage_bill_pct": 100 * float((hh_earn * w)[s].sum()) / tw,
                 "mortgage_service_pct": 100 * float((mort * w)[s].sum()) / tm,
                 "rent_pct": 100 * float((rent * w)[s].sum()) / tr}
            r["mortgage_lean"] = r["mortgage_service_pct"] / r["wage_bill_pct"]
            r["rent_lean"] = r["rent_pct"] / r["wage_bill_pct"]
            five.append(r)
    F = pd.DataFrame(five)
    F.round(4).to_csv(OUT / "acs_fiveway_occupied_only.csv", index=False)
    print("\n=== A38 CORRECTED: five-way shares, OCCUPIED units only ===")
    for cog in ["cognitive_AIOE", "cognitive_GPT"]:
        s = F[F["cognitive_definition"] == cog]
        print("-- " + cog + " --")
        print(s[["class", "households_pct", "wage_bill_pct", "mortgage_service_pct",
                 "rent_pct", "mortgage_lean", "rent_lean"]].round(2).to_string(index=False))

    # ------------------------------------------------------------------
    # Item 5, ACS half: the mortgage lean on a household EARNINGS denominator, so the SIPP
    # comparison in reconcile_acs_sipp.py is like for like.
    # ------------------------------------------------------------------
    lr = []
    for gname in ["embodied", "cognitive_AIOE", "cognitive_GPT"]:
        sel = flags[gname]
        for lab, msk in [("A_acs_service_vs_earnings", core),
                         ("D_acs_service_mortgage_holders_only", core & (mort > 0))]:
            ww = w * msk
            tn, td = float((mort * ww).sum()), float((hh_earn * ww).sum())
            sn = float((mort * ww * sel).sum()) / tn if tn else np.nan
            sd = float((hh_earn * ww * sel).sum()) / td if td else np.nan
            lr.append({"row": lab, "source": "ACS", "measure": "annual mortgage service",
                       "denominator": "household wage earnings", "group": gname,
                       "obligation_share_pct": 100 * sn, "earnings_share_pct": 100 * sd,
                       "lean": sn / sd if sd else np.nan})
    pd.DataFrame(lr).round(5).to_csv(OUT / "acs_lean_rows.csv", index=False)
    print("\n=== Item 5, ACS rows ===")
    print(pd.DataFrame(lr)[["row", "group", "obligation_share_pct", "earnings_share_pct",
                            "lean"]].round(4).to_string(index=False))

    pd.set_option("display.width", 250)
    print("\n=== SHARE-BASED against ENGINE, central target, uniform incidence ===")
    g = T[(T["target"] == "central_10pct") & (T["incidence"] == "uniform")]
    out = g[["construct", "share_based_mortgage", "engine_mortgage_dsti_30",
             "engine_mortgage_dsti_50", "ratio_mortgage_dsti_30", "ratio_mortgage_dsti_50",
             "share_based_rent", "engine_rent_dsti_50", "ratio_rent_dsti_50"]].copy()
    for c in out.columns:
        if c.startswith(("share_based", "engine")):
            out[c] = out[c] / 1e9
    print(out.round(3).to_string(index=False))
    print("\n  dollar columns in USD billions, annual")
    print(f"\ntotal {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
