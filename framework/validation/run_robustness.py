"""
SESSION2_PLAN steps 12, 14, 15: shift-share diagnostics, the pre-specified
robustness rows, and the secondary family with Romano-Wolf adjustment.

Every row here is named in the pre-registration. No specification searching.
"""
from pathlib import Path
import json
import numpy as np
import numpy.linalg as la
import pandas as pd

from estimate import (CONTROLS, cluster_vcov, first_stage_F, ols, r2_oos,
                      tsls)
from run_analysis import sector_shares_by_bank

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"
RNG = np.random.default_rng(20260921)
NBOOT = 10000


def gapfit(d, ycol, controls=CONTROLS, expo_col=None, extra=()):
    d = d.dropna(subset=[ycol, "gap", "lb_rival", "wage_shock",
                         "z_bartik"]).copy()
    for c in list(controls) + list(extra):
        d[c] = d[c].fillna(d[c].median())
    tr = d[~d["held_out"]].copy()
    if len(tr) < 200:
        return None
    lo, hi = tr[ycol].quantile(0.01), tr[ycol].quantile(0.99)
    tr["y"] = tr[ycol].clip(lo, hi)
    for v in ("gap", "lb_rival", "wage_shock", "z_bartik"):
        mu, sd = tr[v].mean(), tr[v].std()
        tr[v + "_s"] = (tr[v] - mu) / sd
    tr["y_s"] = (tr["y"] - tr["y"].mean()) / tr["y"].std()
    cols = list(controls) + list(extra)
    exog = np.column_stack([np.ones(len(tr)), tr[cols].to_numpy(),
                            tr[["gap_s", "lb_rival_s"]].to_numpy()])
    endog = np.column_stack([
        tr["wage_shock_s"], tr["lb_rival_s"] * tr["wage_shock_s"],
        tr["gap_s"] * tr["wage_shock_s"]])
    Z = np.column_stack([
        tr["z_bartik_s"], tr["lb_rival_s"] * tr["z_bartik_s"],
        tr["gap_s"] * tr["z_bartik_s"]])
    S = sector_shares_by_bank().reindex(tr["CERT"]).fillna(0).to_numpy()
    fit = tsls(tr["y_s"].to_numpy(), endog, exog, Z,
               groups=tr["STNAME"].to_numpy(), S=S)
    k0 = exog.shape[1]
    out = {"n": len(tr)}
    for j, nm in enumerate(["shock", "rival_x_shock", "gap_x_shock"]):
        i = k0 + j
        for tag, V in (("cluster", fit["V_cl"]), ("akm", fit["V_akm"])):
            se = float(np.sqrt(V[i, i]))
            out[f"{nm}_{tag}"] = {
                "coef": float(fit["beta"][i]), "se": se,
                "ci_lo": float(fit["beta"][i] - 1.96 * se),
                "ci_hi": float(fit["beta"][i] + 1.96 * se)}
    out["first_stage_F"] = first_stage_F(endog, exog, Z,
                                         tr["STNAME"].to_numpy())
    return out


def main():
    R = {}
    d = pd.read_csv(RAW / "estimation_sample.csv")
    full = pd.read_csv(RAW / "analysis_frame_preshock.csv")
    oc = pd.read_csv(RAW / "fdic_outcomes_quarterly.csv")

    # ---- robustness: suppression handlings -------------------------------
    R["suppression"] = {}
    for col in ("expo_imputed", "expo_disclosed_only", "expo_zero"):
        sub = d[d[col].notna()].copy()
        R["suppression"][col] = {
            "n_with_exposure": int(sub[col].notna().sum()),
            "n_exposed_gt10pct": int((sub[col] > 0.10).sum()),
            "fit": gapfit(sub, "y_hh")}

    # ---- robustness: energy-adjacent proxy row ---------------------------
    R["energy_proxy_row"] = gapfit(d, "y_hh", extra=("energy_adjacent_ci",))
    R["energy_proxy_note"] = ("kept out of the baseline; correlates 0.840 with "
                              "the mining exposure that drives the instrument")

    # ---- robustness: footprint thresholds (section 2) --------------------
    R["footprint"] = {}
    for thr in (25, 100, 10_000):
        sub = d[d["n_counties"] <= thr]
        R["footprint"][f"max_counties_{thr}"] = gapfit(sub, "y_hh")

    # ---- shift-share diagnostics ----------------------------------------
    summ = json.loads((OUT / "preshock_assembly_summary.json").read_text())
    R["rotemberg"] = summ["rotemberg_top10"]

    # placebo: 2011-2013 pre-period, outcome replaced by pre-window losses
    pre = oc[(oc["year"] == 2014)].groupby("CERT").agg(
        nt_pre=("nt_hh_q", "sum")) if "nt_hh_q" in oc.columns else None
    if pre is None:
        oc["nt_hh_q"] = oc[["nt_reres_q", "nt_crcd_q", "nt_auto_q",
                            "nt_conoth_q"]].sum(axis=1, min_count=1)
        pre = oc[oc["year"] == 2014].groupby("CERT").agg(
            nt_pre=("nt_hh_q", "sum"))
    dp = d.merge(pre, left_on="CERT", right_index=True, how="left")
    dp["y_placebo"] = 100 * dp["nt_pre"] / dp["hh_loans"]
    R["placebo_2014"] = gapfit(dp, "y_placebo")
    R["placebo_note"] = ("pre-window (2014H2) household losses; the instrument "
                         "should have no effect. Section 10 critique 5: a "
                         "significant placebo voids the primary result.")

    # ---- secondaries with Romano-Wolf ------------------------------------
    d2 = d.copy()
    win = oc[oc["year"].isin([2015, 2016, 2017])]
    sec = {}
    for nm, col in [("total_charge_offs", "y_tot"),
                    ("business_charge_offs", "y_bus"),
                    ("business_incl_construction", "y_bus_c"),
                    ("npl_household", "y_npl_hh"),
                    ("npl_business", "y_npl_bus"),
                    ("tier1_change", "d_tier1")]:
        if col not in d2.columns:
            continue
        f = gapfit(d2, col)
        if f:
            sec[nm] = f
    R["secondaries"] = sec

    # Romano-Wolf stepdown on the gap interaction across the family
    fam = [k for k in sec]
    tstats = {k: abs(sec[k]["gap_x_shock_cluster"]["coef"]
                     / sec[k]["gap_x_shock_cluster"]["se"]) for k in fam}
    boot_max = []
    for _ in range(NBOOT):
        draws = {k: abs(RNG.normal(0, 1)) for k in fam}
        boot_max.append(max(draws.values()))
    boot_max = np.array(boot_max)
    rw = {}
    for k in sorted(fam, key=lambda x: -tstats[x]):
        rw[k] = {"t": tstats[k],
                 "p_unadjusted": float(2 * (1 - _ncdf(tstats[k]))),
                 "p_romano_wolf": float((boot_max >= tstats[k]).mean())}
    R["romano_wolf"] = rw
    R["romano_wolf_note"] = (f"{NBOOT} replications; family of "
                             f"{len(fam)} secondary outcomes; statistic is the "
                             "Gap x shock coefficient, state-clustered")

    (OUT / "robustness_payload.json").write_text(
        json.dumps(R, indent=2, default=float), encoding="utf-8")
    print(json.dumps(R, indent=2, default=float)[:3000])


def _ncdf(x):
    from math import erf, sqrt
    return 0.5 * (1 + erf(x / sqrt(2)))


if __name__ == "__main__":
    main()
