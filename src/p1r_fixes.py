"""P1r fixes: conditional default probability, common time basis, rho* grid, labour share.

FIX 1. Default probability conditional on job loss, not population delinquency.
  Gerardi, Herkenhoff, Ohanian and Willen, "Can't Pay or Won't Pay? Unemployment, Negative
  Equity, and Strategic Default", Review of Financial Studies 31(3), 2018, 1098-1131 (NBER
  WP 21630), PSID-based. Verified from the working paper PDF. Two usable facts:
    - "the most risky subsample, 'can't pay' households with high LTV ratios have a default
      rate approaching 20 percent"
    - "the effect of involuntary job loss on the default probability is equivalent to a 37
      percentage point drop in equity"
  The 20 percent figure is a default rate CONDITIONAL on inability to pay and high LTV,
  which is the population this paper cares about. It anchors the upper end.
  The lower end (job loss WITHOUT negative equity) is an interpolation, not a GHOW estimate,
  and is labelled as such.
  AUTO and RENT: no verified conditional-on-job-loss source was obtained. Those channels are
  bracketed crudely and flagged; see notes.

FIX 2. Common time basis. Fiscal loss is a RECURRING ANNUAL FLOW that accrues as
  displacement accrues. Credit loss is a ONE-TIME STOCK loss on each displaced cohort. Over
  a horizon H with displacement ramping linearly to d:
    fiscal, year t        L * W * d * (t/H)
    fiscal, cumulative    sum over t of that, discounted at r
    credit, cumulative    balance_at_risk * d * PD * LGD, incurred once as cohorts displace,
                          discounted at r
  Both are also reported annualised (cumulative divided by H). The asymmetry between a flow
  and a stock is the substantive point and was hidden in the previous comparison.

FIX 3. Wording: the closed-economy corollary says the loss per displaced dollar is
  independent of the ROBOT COST RATIO s under uniform capital taxation. It says nothing
  about adoption speed. Corrected throughout.

FIX 4. rho* = (1 - tau_k/tau_l) / omega, gridded, with infeasible cells marked.

FIX 5. rho remains STIPULATED. BLS returns HTTP 403 to this environment.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}
TAU_K = {"equipment_0.05": 0.05, "net_capital_0.10": 0.10, "statutory_upper_0.21": 0.21}
OMEGA = {"JLS_central_0.75": 0.75, "JLS_low_loss_0.82": 0.82}
DISCOUNT = 0.03
HORIZONS = (10, 20)
DISPLACEMENTS = (0.10, 0.25, 0.50)

# conditional on involuntary job loss
PD_JOBLOSS = {"with_negative_equity_GHOW": 0.20,      # GHOW 2018, verbatim
              "without_negative_equity_interpolated": 0.05}
LGD = {"mortgage_low": 0.10, "mortgage_high": 0.25,
       "consumer_low": 0.20, "consumer_high": 0.40}


def labour_share_machinery():
    """Labour share of value added in machinery manufacturing, NBER-CES (in the 114030 pkg)."""
    f = RAW / "manual" / "114030" / "naics5811.dta"
    d = pd.read_stata(f)
    d = d[d["naics"].notna()].copy()
    d["n3"] = (d["naics"].astype(int).astype(str).str[:3])
    recent = d[(d["year"] >= 2005) & d["n3"].isin(["333"])]
    ls = float((recent["pay"].sum()) / (recent["vadd"].sum()))
    return {"naics_333_machinery_labour_share_of_value_added": ls,
            "years": "2005 onward", "source": "NBER-CES, naics5811.dta"}


def main():
    res = {}

    # ---------- FIX 4: rho* grid ----------
    rows = []
    for ln, tl in TAU_L.items():
        for kn, tk in TAU_K.items():
            for on, om in OMEGA.items():
                rstar = (1 - tk / tl) / om
                rows.append({"tau_l": ln, "tau_k": kn, "omega": on,
                             "rho_star": rstar, "feasible": rstar <= 1.0})
    R = pd.DataFrame(rows)
    R.round(4).to_csv(OUT / "p1r_rho_star_grid.csv", index=False)

    # labour share adjustment: a share ls of robot-sector income is wages, taxed at tau_l
    lsm = labour_share_machinery()
    ls = lsm["naics_333_machinery_labour_share_of_value_added"]
    rows2 = []
    for ln, tl in TAU_L.items():
        for kn, tk in TAU_K.items():
            for on, om in OMEGA.items():
                # closed economy, g=0, robot cost (1-s) split: ls taxed at tau_l, rest at tau_k
                # tau_k*s + tau_l*rho*om + (1-s)*(ls*tau_l + (1-ls)*tau_k) >= tau_l
                # at s -> 0 (adoption margin), worst case:
                eff = ls * tl + (1 - ls) * tk
                rstar = (tl - eff) / (tl * om)
                rows2.append({"tau_l": ln, "tau_k": kn, "omega": on,
                              "labour_share_robot_sector": ls,
                              "rho_star_with_labour_share": max(rstar, 0.0),
                              "feasible": rstar <= 1.0})
    R2 = pd.DataFrame(rows2)
    R2.round(4).to_csv(OUT / "p1r_rho_star_labour_share.csv", index=False)

    # ---------- FIX 1 and 2: channel comparison on a common time basis ----------
    w = json.loads((OUT / "legW_us_derived.json").read_text())
    P = pd.read_csv(OUT / "pathway_totals.csv")
    B = pd.read_csv(OUT / "pathway_bounds.csv")
    mort_balance = 14010.9
    cons_balance = 5120.3

    def pv_ramp(annual_full, H, r):
        """PV of a flow ramping linearly to annual_full over H years, then held."""
        return sum(annual_full * (t / H) / (1 + r) ** t for t in range(1, H + 1))

    def pv_onetime_ramp(total, H, r):
        """PV of a one-time loss incurred in equal cohorts over H years."""
        return sum((total / H) / (1 + r) ** t for t in range(1, H + 1))

    comp = []
    for _, r in P.iterrows():
        p = r["pathway"]
        W = r["wage_bill_usd_bn"]
        bb = B[B["group"] == p].iloc[0]
        share = bb["mortgage_CENTRAL_pct"] / 100
        for d in DISPLACEMENTS:
            for H in HORIZONS:
                dW_full = W * d
                for lname, Lpd in [("low_AMR_g0_s1", 0.155), ("high_bu_g0.1_s0", 0.418)]:
                    fis_full = dW_full * Lpd
                    fis_pv = pv_ramp(fis_full, H, DISCOUNT)
                    mb = mort_balance * share * d
                    cb = cons_balance * share * d
                    for pdn, pdv in PD_JOBLOSS.items():
                        for lg in ("low", "high"):
                            el_total = (mb * pdv * LGD[f"mortgage_{lg}"]
                                        + cb * pdv * LGD[f"consumer_{lg}"])
                            el_pv = pv_onetime_ramp(el_total, H, DISCOUNT)
                            comp.append({
                                "pathway": p, "displacement": d, "horizon": H,
                                "fiscal_case": lname, "pd_case": pdn, "lgd_case": lg,
                                "fiscal_annual_at_full_usd_bn": fis_full,
                                "fiscal_cumulative_pv_usd_bn": fis_pv,
                                "fiscal_annualised_usd_bn": fis_pv / H,
                                "credit_total_usd_bn": el_total,
                                "credit_cumulative_pv_usd_bn": el_pv,
                                "credit_annualised_usd_bn": el_pv / H,
                                "ratio_cumulative": fis_pv / el_pv if el_pv else np.nan,
                                "ratio_annualised": (fis_pv / H) / (el_pv / H) if el_pv else np.nan})
    C = pd.DataFrame(comp)
    C.round(3).to_csv(OUT / "p1r_channel_comparison_timed.csv", index=False)

    res["labour_share"] = lsm
    res["discount_rate"] = DISCOUNT
    res["PD_conditional_on_job_loss"] = PD_JOBLOSS
    res["ratio_range_cumulative"] = {
        "min": float(C["ratio_cumulative"].min()),
        "max": float(C["ratio_cumulative"].max())}
    res["rho_star_feasible_share"] = float(R["feasible"].mean())
    (OUT / "p1r_fixes_summary.json").write_text(json.dumps(res, indent=2, default=str))

    pd.set_option("display.width", 240)
    print("=== FIX 4: rho* = (1 - tau_k/tau_l)/omega ===")
    pv = R.pivot_table(index=["tau_l", "omega"], columns="tau_k", values="rho_star")
    print(pv.round(3).to_string())
    print(f"\n  feasible cells (rho* <= 1): {int(R['feasible'].sum())} of {len(R)}")
    inf = R[~R["feasible"]]
    if len(inf):
        print("  INFEASIBLE cells (require reemployment above 100 percent):")
        print(inf[["tau_l", "tau_k", "omega", "rho_star"]].round(3).to_string(index=False))

    print(f"\n=== FIX 4 caveat: robot-sector labour share, NAICS 333 = {ls:.3f} ===")
    pv2 = R2.pivot_table(index=["tau_l", "omega"], columns="tau_k",
                         values="rho_star_with_labour_share")
    print(pv2.round(3).to_string())

    print("\n=== FIX 1 and 2: channel comparison, 25 percent displacement, 10 years ===")
    v = C[np.isclose(C["displacement"], 0.25) & (C["horizon"] == 10)]
    agg = v.groupby("pathway").agg(
        fiscal_pv_lo=("fiscal_cumulative_pv_usd_bn", "min"),
        fiscal_pv_hi=("fiscal_cumulative_pv_usd_bn", "max"),
        credit_pv_lo=("credit_cumulative_pv_usd_bn", "min"),
        credit_pv_hi=("credit_cumulative_pv_usd_bn", "max"),
        ratio_lo=("ratio_cumulative", "min"), ratio_hi=("ratio_cumulative", "max"))
    print(agg.round(2).to_string())
    print(f"\n  ratio across ALL cases: {C['ratio_cumulative'].min():.2f}x to "
          f"{C['ratio_cumulative'].max():.2f}x")


if __name__ == "__main__":
    main()
