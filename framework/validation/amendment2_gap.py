"""
Amendment 2: the Gap decomposition, its power implications, and the structural
calibration test's predicted-loss term.

NO OUTCOME VARIABLE IS READ HERE. Realised charge-offs are not touched; only the
PREDICTED loss is constructed, from pre-shock balance sheets, the engine's own
coefficients, and the treatment-side wage-bill shock.

    LB          = sum_c  w_c * beta_c * wageshare(bank counties)
    LB_rival    = [sum_c w_c * beta_c] * wageshare_population
    LB_debtor   = sum_c  w_c * beta_c * wageshare_debtor(group(c))
    Gap         = LB_debtor - LB_rival
                = sum_c w_c * beta_c * (wageshare_debtor(c) - wageshare_population)
"""
from pathlib import Path
import io
import json
import zipfile
import numpy as np
import numpy.linalg as la
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"

# ---- engine constants, recorded in PREREGISTRATION 13.3 --------------------
# Source: data/processed/verify/hand_check_credit.csv on origin/master @ 0b5f2b8
# blob 233e413becfec072b4a5f4cc6357f9f6e7499f79
# sha256 a70b6ca41a4bb57dde30393428e41f27cb340c9316f7e614ce4a37c09ef37726
ENGINE_LGD = {"mortgage": (0.25, 0.40), "card": (0.80, 1.00),
              "auto": (0.45, 0.65), "student": (0.75, 1.00)}
# effective default uplift per unit dose, = (EAD/balance at dose 0.05) / 0.05
ENGINE_EAD = {  # (exposure_at_default_bn, total_balance_bn) at dose 0.05
    "mortgage": (35.4385, 8535.4276), "card": (1.6246, 399.1782),
    "auto": (2.8624, 696.2587), "student": (4.1003, 1023.9207)}
BASE_DOSE = 0.05

# FDIC item -> (claim class for beta, engine class for loss sensitivity)
ITEM_MAP = {
    "LNRERES":  ("home_mortgage", "mortgage"),
    "LNREMULT": ("multifamily_mortgage", "mortgage"),   # property-secured proxy
    "LNCRCD":   ("credit_card", "card"),
    "LNAUTO":   ("auto_loan", "auto"),
    "LNCONOTH": ("other_consumer", "student"),          # residual incl. student
}
CONTROLS = ["sh_resre", "sh_consumer", "sh_cre", "sh_constr", "sh_ci", "sh_ag",
            "sh_sec", "tier1_lev", "cre_conc", "log_assets", "dep_assets",
            "brokered", "loans_assets"]


def engine_sensitivities():
    s = {}
    for k, (ead, bal) in ENGINE_EAD.items():
        uplift_per_dose = (ead / bal) / BASE_DOSE
        lo, hi = ENGINE_LGD[k]
        s[k] = {"uplift_per_unit_dose": uplift_per_dose,
                "lgd_lo": lo, "lgd_hi": hi,
                "s_lo": uplift_per_dose * lo, "s_hi": uplift_per_dose * hi,
                "s_mid": uplift_per_dose * (lo + hi) / 2}
    return s


def county_wage_shock():
    """Fractional change in the county wage bill, 2014-2016. Treatment side."""
    bea = pd.read_csv(RAW / "bea_cainc4_all_areas.csv", dtype=str)
    bea["GeoFIPS"] = bea["GeoFIPS"].str.strip().str.replace('"', "", regex=False)
    w = bea[bea["LineCode"] == "50"].set_index("GeoFIPS")
    w = w[~w.index.str.endswith("000")]
    a = pd.to_numeric(w["2014"], errors="coerce")
    b = pd.to_numeric(w["2016"], errors="coerce")
    return ((b - a) / a).replace([np.inf, -np.inf], np.nan).dropna()


def main():
    eng = engine_sensitivities()
    beta = pd.read_csv(ROOT / "framework" / "labor_backing" /
                       "claim_class_rules.csv")
    beta = {r.claim_class: float(r.labour_backing_share)
            for r in beta.itertuples()}

    panel = pd.read_csv(RAW / "preshock_debtor_panel_2014.csv")
    base = pd.read_csv(RAW / "preshock_panel_2014.csv")
    p = panel.merge(base[["CERT"] + [c for c in CONTROLS
                                     if c in base.columns]],
                    on="CERT", how="left", suffixes=("", "_b"))

    fin = pd.read_csv(RAW / "fdic_financials_20140630.csv")
    num = [c for c in fin.columns
           if c not in ("NAMEFULL", "STNAME", "ID", "REPDTE")]
    fin[num] = fin[num].apply(pd.to_numeric, errors="coerce")
    fin["SCOTHER"] = (fin["SC"].fillna(0) - fin["SCMUNI"].fillna(0)).clip(lower=0)
    fin["book"] = fin["LNLSGR"].fillna(0) + fin["SC"].fillna(0)
    p = p.merge(fin[["CERT", "book", "LNLSGR", "ASSET"] + list(ITEM_MAP)],
                on="CERT", how="left")
    p = p[(p["book"] > 0) & (p["LNLSGR"] > 0)].copy()

    # ---- 1. the Gap ------------------------------------------------------
    p["gap"] = p["lb_debtor"] - p["lb_rival"]

    # ---- bank-level wage-bill shock and mining exposure ------------------
    sod = pd.read_csv(RAW / "fdic_sod_2014.csv").dropna(subset=["STCNTYBR"])
    sod["fips"] = (sod["STCNTYBR"].astype(float).astype(int)
                   .astype(str).str.zfill(5))
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"], errors="coerce").fillna(0)
    shock = county_wage_shock()
    sod["sh"] = sod["fips"].map(shock)
    s2 = sod.dropna(subset=["sh"])
    bank_shock = s2.groupby("CERT").apply(
        lambda d: np.average(d["sh"], weights=d["DEPSUMBR"])
        if d["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)
    p["wage_shock"] = p["CERT"].map(bank_shock)

    expo = pd.read_csv(RAW / "bank_mining_exposure_2014.csv")
    expo.columns = ["CERT", "mining_expo"]
    p = p.merge(expo, on="CERT", how="left")
    p["exposed"] = p["mining_expo"] > 0.10

    p = p.dropna(subset=["gap", "lb_rival", "wage_shock"]).copy()

    ctl = [c for c in CONTROLS if c in p.columns]
    rows = []
    for c in ["lb_rival"] + ctl:
        s = p[["gap", c]].dropna()
        rows.append({"variable": c, "n": len(s),
                     "corr_with_gap": s["gap"].corr(s[c])})
    corr = pd.DataFrame(rows).sort_values("corr_with_gap",
                                          key=abs, ascending=False)
    corr.to_csv(OUT / "gap_correlations.csv", index=False)

    ex = p[p["exposed"]]
    dist = {
        "n_banks": int(len(p)),
        "n_exposed_banks": int(len(ex)),
        "gap_mean": float(p["gap"].mean()),
        "gap_variance": float(p["gap"].var()),
        "gap_sd": float(p["gap"].std()),
        "lb_rival_sd": float(p["lb_rival"].std()),
        "lb_debtor_sd": float(p["lb_debtor"].std()),
        "gap_sd_over_debtor_sd": float(p["gap"].std() / p["lb_debtor"].std()),
        "gap_var_share_of_debtor_var": float(p["gap"].var()
                                             / p["lb_debtor"].var()),
        "corr_gap_rival": float(p["gap"].corr(p["lb_rival"])),
        "gap_p10": float(p["gap"].quantile(.10)),
        "gap_p50": float(p["gap"].quantile(.50)),
        "gap_p90": float(p["gap"].quantile(.90)),
        "gap_exposed_mean": float(ex["gap"].mean()),
        "gap_exposed_sd": float(ex["gap"].std()),
        "gap_exposed_p10": float(ex["gap"].quantile(.10)),
        "gap_exposed_p50": float(ex["gap"].quantile(.50)),
        "gap_exposed_p90": float(ex["gap"].quantile(.90)),
        "wage_shock_mean": float(p["wage_shock"].mean()),
        "wage_shock_sd": float(p["wage_shock"].std()),
        "wage_shock_exposed_mean": float(ex["wage_shock"].mean()),
    }

    # ---- 2. minimum detectable effect for the Gap interaction ------------
    g = (p["gap"] - p["gap"].mean()) / p["gap"].std()
    sh = (p["wage_shock"] - p["wage_shock"].mean()) / p["wage_shock"].std()
    X_int = (g * sh).to_numpy()

    C = p[ctl].fillna(p[ctl].median()).to_numpy()
    C = np.column_stack([np.ones(len(C)), C,
                         ((p["lb_rival"] - p["lb_rival"].mean())
                          / p["lb_rival"].std()).to_numpy() * sh.to_numpy()])
    bh, *_ = la.lstsq(C, X_int, rcond=None)
    resid = X_int - C @ bh
    r2_x = 1 - (resid ** 2).sum() / ((X_int - X_int.mean()) ** 2).sum()
    sd_x_resid = float(np.std(resid))

    n = len(p)
    n_states = p["STNAME"].nunique() if "STNAME" in p.columns else 50
    # design effect from clustering by state, at a stated intra-cluster
    # correlation; this is an assumption, declared, not a measurement
    ICC = 0.05
    m_bar = n / n_states
    deff = 1 + (m_bar - 1) * ICC
    # outcome residual SD assumed as a fraction of outcome SD, declared
    RESID_FRAC = np.sqrt(1 - 0.30)

    se = RESID_FRAC * np.sqrt(deff) / (sd_x_resid * np.sqrt(n))
    mde = (1.959964 + 0.8416212) * se

    # MDE is dominated by the clustering design effect, which rests on an
    # assumed intra-cluster correlation. Report the whole surface, so the
    # power verdict cannot be smuggled in through one convenient assumption.
    grid = []
    for icc in (0.0, 0.02, 0.05, 0.10, 0.20):
        d = 1 + (m_bar - 1) * icc
        for r2m in (0.10, 0.30, 0.50):
            se_g = np.sqrt(1 - r2m) * np.sqrt(d) / (sd_x_resid * np.sqrt(n))
            grid.append({"icc": icc, "model_R2": r2m,
                         "design_effect": d,
                         "MDE_outcome_SD": (1.959964 + 0.8416212) * se_g,
                         "powered_at_0.10": (1.959964 + 0.8416212) * se_g <= 0.10})
    pd.DataFrame(grid).to_csv(OUT / "gap_mde_grid.csv", index=False)

    power = {
        "n": int(n), "n_states": int(n_states),
        "sd_of_gap_x_shock_interaction": float(np.std(X_int)),
        "R2_of_interaction_on_controls_and_rival_interaction": float(r2_x),
        "residual_sd_of_interaction": sd_x_resid,
        "assumed_model_R2": 0.30,
        "assumed_intra_cluster_correlation": ICC,
        "design_effect": float(deff),
        "implied_SE_of_theta_in_outcome_SD": float(se),
        "MDE_80pct_power_5pct_two_sided_in_outcome_SD": float(mde),
        "prespecified_threshold": 0.10,
        "powered_for_threshold": bool(mde <= 0.10),
    }

    # ---- 3. structural predicted loss ------------------------------------
    dose = (-p["wage_shock"]).clip(lower=0)        # share of wage bill lost
    for tag, wscol in (("rival", "ws_pop"), ("debtor", None)):
        pred_lo = np.zeros(len(p))
        pred_hi = np.zeros(len(p))
        pred_mid = np.zeros(len(p))
        for item, (cls, ecls) in ITEM_MAP.items():
            loans = p[item].fillna(0).to_numpy()
            if tag == "rival":
                ws = p["ws_pop"].to_numpy()
            else:
                grp = {"home_mortgage": "ws_mortgage",
                       "multifamily_mortgage": "ws_renter"}.get(cls, "ws_all")
                ws = p[grp].to_numpy() if grp in p.columns \
                    else p["ws_all"].to_numpy()
            common = loans * beta[cls] * ws * dose.to_numpy()
            pred_lo += common * eng[ecls]["s_lo"]
            pred_hi += common * eng[ecls]["s_hi"]
            pred_mid += common * eng[ecls]["s_mid"]
        p[f"pred_loss_{tag}_lo"] = pred_lo / p["LNLSGR"]
        p[f"pred_loss_{tag}_hi"] = pred_hi / p["LNLSGR"]
        p[f"pred_loss_{tag}_mid"] = pred_mid / p["LNLSGR"]

    pred_stats = {}
    for tag in ("rival", "debtor"):
        for b in ("lo", "mid", "hi"):
            c = f"pred_loss_{tag}_{b}"
            pred_stats[c] = {
                "mean_pct_of_loans": float(100 * p[c].mean()),
                "sd_pct": float(100 * p[c].std()),
                "p90_pct": float(100 * p[c].quantile(.90)),
                "max_pct": float(100 * p[c].max()),
                "nonzero_banks": int((p[c] > 0).sum()),
                "exposed_mean_pct": float(100 * p.loc[p["exposed"], c].mean()),
            }
    pred_stats["corr_pred_rival_vs_debtor_mid"] = float(
        p["pred_loss_rival_mid"].corr(p["pred_loss_debtor_mid"]))

    blob = {"engine_sensitivities": eng, "gap_distribution": dist,
            "power": power, "predicted_loss": pred_stats}
    (OUT / "amendment2_diagnostics.json").write_text(
        json.dumps(blob, indent=2), encoding="utf-8")
    p.to_csv(RAW / "amendment2_panel.csv", index=False)

    print("ENGINE LOSS SENSITIVITIES (per unit dose)")
    for k, v in eng.items():
        print(f"  {k:9s} uplift/dose {v['uplift_per_unit_dose']:.6f}  "
              f"LGD {v['lgd_lo']:.2f}-{v['lgd_hi']:.2f}  "
              f"s_lo {v['s_lo']:.6f}  s_hi {v['s_hi']:.6f}")
    print("\nGAP DISTRIBUTION")
    for k, v in dist.items():
        print(f"  {k}: {v:.6f}" if isinstance(v, float) else f"  {k}: {v}")
    print("\nGAP CORRELATIONS")
    print(corr.to_string(index=False))
    print("\nPOWER")
    for k, v in power.items():
        print(f"  {k}: {v}")
    print("\nPREDICTED LOSS (percent of pre-shock gross loans)")
    for k, v in pred_stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
