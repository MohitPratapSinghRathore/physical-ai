"""P1 repairs: feasibility, retained tax streams, rate ranges, payroll split, and a
like-for-like comparison of the fiscal and household-credit channels.

Everything is led in SCALE-FREE per-dollar-of-displaced-wages form. Dollar magnitudes appear
only under the named adoption scenarios, at the end.

DERIVATION (P1 restated).

Displace dW of wage bill. Under output neutrality the robot performs the same task at
all-in cost c_r against wage w, so the cost saving per dollar of displaced wages is

    s = 1 - c_r/w,    with 0 < s <= 1   (adoption requires c_r < w; s -> 1 only as c_r -> 0)

Public revenue per dollar displaced:
    lost labour tax            -tau_l
    added outlays              -g          (per dollar displaced, net of reemployment)
    tax on the surplus         +tau_k * s
    tax on retained labour     +tau_l * rho * omega
    tax on robot cost income   +tau_r * (1 - m) * (1 - s)

where rho is the share of displaced workers reemployed, omega their wage ratio on
reemployment, m the imported share of the robot capital, and tau_r the effective rate on
robot-producer income.

GENERAL CONDITION for fiscal neutrality:

    tau_k*s + tau_l*rho*omega + tau_r*(1-m)*(1-s)  >=  tau_l + g*(1-rho)

FEASIBILITY. With no reemployment and no domestic robot income (rho = 0, m = 1), the
condition collapses to tau_k*s >= tau_l + g. Since s <= 1, this is UNATTAINABLE whenever
tau_k < tau_l + g. At tau_k = 0.10 and tau_l = 0.255 it is unattainable for every g >= 0.

So the correct statement is not "s must exceed 2.55". It is: **output-neutral automation is
never fiscally neutral.** The public loss per dollar of displaced wages is

    L(s) = tau_l + g - tau_k*s,   bounded by   tau_l + g - tau_k  <=  L  <=  tau_l + g

Fiscal neutrality requires additional taxable OUTPUT y (beyond the substitution itself) of

    y >= (tau_l + g)/tau_k - s,   and with s <= 1,   y >= (tau_l + g - tau_k)/tau_k

CLOSED-ECONOMY COROLLARY. With m = 0 and tau_r = tau_k, the s terms cancel: whether a dollar
goes to surplus or to robot cost, it is taxed at tau_k either way. The condition becomes

    tau_k + tau_l*rho*omega >= tau_l + g*(1-rho)

which is independent of s. Automation speed does not matter; only the tax wedge and the
reemployment margin do.

IMPORTED-ROBOT COROLLARY (the emerging-market case). With m = 1 the robot cost leaves the
country untaxed and only the surplus is domestically taxable:

    tau_k*s + tau_l*rho*omega >= tau_l + g*(1-rho)

Near the adoption margin s is close to zero, so the entire labour tax base is lost with
almost no offsetting domestic capital base. This is the brief's India contrast case.

RELATION TO THE BRIEF. PROJECT_BRIEF.md Section 2.3 states tau*s >= 1 as the condition for
full income replacement. That is the REDISTRIBUTION condition and it sits downstream of P1:
it asks whether collected revenue can replace lost income, taking collection for granted.
P1 asks whether revenue is collected at all.

SOURCES
  tau_l = 0.255, tau_k = 0.10 (net capital income), tau_k = 0.05 (equipment and software
    post-2017): Acemoglu, Manera and Restrepo, Brookings Papers 2020(1), 231-300, read from
    the published PDF.
  Bottom-up tau_l = 0.301 to 0.318: NIPA and IRS SOI, this repository.
  omega: Jacobson, LaLonde and Sullivan, "Earnings Losses of Displaced Workers", American
    Economic Review 83(4), 1993, 685-709. Long-term losses average about 25 percent for
    high-tenure displaced workers, with a reported range of 18 to 35 percent, so
    omega = 0.75 central, 0.65 to 0.82 range.
  rho: NOT SOURCED. The BLS Displaced Worker Survey reemployment rate was not obtained.
    rho is therefore a stipulated scenario parameter and is labelled as such.
  Payroll split: statutory OASDI 12.4 percent, HI 2.9 percent of covered earnings.
  OASDI payroll income 1,323.2bn (91.3 percent of 1,449.3bn combined income, 2025 Trustees).
  HI payroll income about 406.9bn (88 percent of 462.4bn Part A revenue, 2024).
  Default rates: FRED DRSFRMACBS and CORCACBS, measured, in this repository.
  LGD: indicative industry ranges, mortgage 10 to 25 percent, auto 20 to 40 percent. These
    are NOT authoritative estimates and are labelled as brackets.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

TAU_L = {"AMR": 0.255, "bottom_up_low": 0.301, "bottom_up_high": 0.318}
TAU_K = {"net_capital": 0.10, "equipment_software": 0.05}
# OMEGA IS NOW SOURCED from the BLS Displaced Workers Summary Table 7, see src/bls_dws.py.
# The stipulated Jacobson, LaLonde and Sullivan values are retained as sensitivity only:
# JLS measures long-run earnings loss INCLUDING non-employment, while this formula needs
# the ratio CONDITIONAL ON REEMPLOYMENT, which is what DWS Table 7 prices.
OMEGA = {"low": 0.9050, "central": 0.9554, "high": 1.0103}
OMEGA_STIPULATED = {"low": 0.65, "central": 0.75, "high": 0.82}
RHO_OBSERVED = 0.6616
RHO = [0.0, 0.5, 0.7, 0.9]
G = [0.0, 0.10, 0.25]

OASDI_PAYROLL_INCOME, HI_PAYROLL_INCOME = 1323.2, 406.9
OASDI_STAT, HI_STAT = 0.124, 0.029


def main():
    res = {}

    # ---------- (1) feasibility, per dollar of displaced wages ----------
    rows = []
    for lname, tl in TAU_L.items():
        for kname, tk in TAU_K.items():
            for g in G:
                Lmax = tl + g                      # s -> 0, at the adoption margin
                Lmin = tl + g - tk                 # s -> 1, free robots
                feasible = tk >= tl + g
                y_req = (tl + g - tk) / tk         # extra taxable output needed at s = 1
                rows.append({"tau_l_source": lname, "tau_l": tl, "tau_k_source": kname,
                             "tau_k": tk, "g": g,
                             "loss_per_dollar_at_s0": Lmax,
                             "loss_per_dollar_at_s1": Lmin,
                             "fiscal_neutrality_feasible_under_output_neutrality": feasible,
                             "extra_taxable_output_required_at_s1": y_req})
    F = pd.DataFrame(rows)
    F.round(4).to_csv(OUT / "p1_feasibility.csv", index=False)
    res["any_feasible"] = bool(F["fiscal_neutrality_feasible_under_output_neutrality"].any())

    # ---------- (2) general condition with retained streams ----------
    gen = []
    for lname, tl in TAU_L.items():
        tk = TAU_K["net_capital"]
        for m in (0.0, 1.0):
            tr = tk
            for rho in RHO:
                for g in G:
                    for s in (0.05, 0.50, 1.00):
                        om = OMEGA["central"]
                        lhs = tk * s + tl * rho * om + tr * (1 - m) * (1 - s)
                        rhs = tl + g * (1 - rho)
                        gen.append({"tau_l_source": lname, "import_share_m": m,
                                    "rho": rho, "g": g, "s": s, "omega": om,
                                    "revenue_retained": lhs, "revenue_required": rhs,
                                    "net_per_dollar": lhs - rhs,
                                    "fiscally_neutral": lhs >= rhs})
    GEN = pd.DataFrame(gen)
    GEN.round(4).to_csv(OUT / "p1_general_condition.csv", index=False)

    # break-even reemployment share, closed economy, per rate set
    be = {}
    for lname, tl in TAU_L.items():
        tk = TAU_K["net_capital"]
        for g in G:
            om = OMEGA["central"]
            # tk + tl*rho*om >= tl + g*(1-rho)  ->  rho*(tl*om + g) >= tl + g - tk
            denom = tl * om + g
            be[f"{lname}_g{g}"] = (tl + g - tk) / denom if denom else np.nan
    res["breakeven_rho_closed_economy"] = be

    # ---------- (4) payroll split ----------
    w = json.loads((OUT / "legW_us_derived.json").read_text())
    wage_bill = w["wage_bill_usd_bn"]
    r_payroll = w["fed_social_insurance_contrib_usd_bn"] / wage_bill
    share_oasdi = OASDI_STAT / (OASDI_STAT + HI_STAT)
    share_hi = HI_STAT / (OASDI_STAT + HI_STAT)
    res["payroll"] = {"effective_payroll_rate_on_wage_bill": r_payroll,
                      "statutory_split_OASDI": share_oasdi, "statutory_split_HI": share_hi,
                      "OASDI_payroll_income_usd_bn": OASDI_PAYROLL_INCOME,
                      "HI_payroll_income_usd_bn": HI_PAYROLL_INCOME}

    # ---------- (5)(6)(7) scenario magnitudes and the channel comparison ----------
    P = pd.read_csv(OUT / "pathway_totals.csv")
    B = pd.read_csv(OUT / "pathway_bounds.csv")
    mort_balance = w["hh_debt_usd_bn"] * (14010.9 / 21377.8)   # 1-4 family mortgages
    cons_balance = 5120.3                                       # consumer credit, Z.1

    # measured default rates, FRED, in-repo
    PD = {"mortgage_base": 0.0186, "mortgage_stress_2010": 0.1148,
          "consumer_base": 0.0266, "consumer_stress_2010": 0.0660}
    LGD = {"mortgage_low": 0.10, "mortgage_high": 0.25,
           "consumer_low": 0.20, "consumer_high": 0.40}
    PD_DISPLACED = {"low": 0.05, "high": 0.20}   # bracket, labelled scenario

    comp = []
    for _, r in P.iterrows():
        p = r["pathway"]
        W = r["wage_bill_usd_bn"]
        bb = B[B["group"] == p].iloc[0]
        for d in (0.10, 0.25, 0.50):
            dW = W * d
            # fiscal, per dollar then scaled
            fis_lo = dW * (TAU_L["AMR"] - TAU_K["net_capital"])
            fis_hi = dW * (TAU_L["bottom_up_high"] + 0.10)   # with g = 0.10, s -> 0 side
            # credit: balances at risk via the CENTRAL debt-service share
            mb = mort_balance * bb["mortgage_CENTRAL_pct"] / 100 * d
            cb = cons_balance * bb["mortgage_CENTRAL_pct"] / 100 * d  # share proxy
            el_lo = mb * PD_DISPLACED["low"] * LGD["mortgage_low"] + \
                cb * PD_DISPLACED["low"] * LGD["consumer_low"]
            el_hi = mb * PD_DISPLACED["high"] * LGD["mortgage_high"] + \
                cb * PD_DISPLACED["high"] * LGD["consumer_high"]
            comp.append({"pathway": p, "displacement": d,
                         "displaced_wage_bill_usd_bn": dW,
                         "fiscal_loss_low_usd_bn": fis_lo,
                         "fiscal_loss_high_usd_bn": fis_hi,
                         "mortgage_balance_at_risk_usd_bn": mb,
                         "consumer_balance_at_risk_usd_bn": cb,
                         "expected_credit_loss_low_usd_bn": el_lo,
                         "expected_credit_loss_high_usd_bn": el_hi,
                         "fiscal_to_credit_ratio_low": fis_lo / el_hi if el_hi else np.nan,
                         "fiscal_to_credit_ratio_high": fis_hi / el_lo if el_lo else np.nan})
    C = pd.DataFrame(comp)
    C.round(3).to_csv(OUT / "p1_channel_comparison.csv", index=False)

    (OUT / "p1_repairs_summary.json").write_text(json.dumps(
        {**res, "PD": PD, "LGD": LGD, "PD_displaced_bracket": PD_DISPLACED,
         "mortgage_balance_base_usd_bn": mort_balance,
         "consumer_balance_base_usd_bn": cons_balance}, indent=2, default=str))

    pd.set_option("display.width", 240)
    print("=== (1) FEASIBILITY, per dollar of displaced wages ===")
    print(F[F["tau_k_source"] == "net_capital"][
        ["tau_l_source", "tau_l", "g", "loss_per_dollar_at_s0", "loss_per_dollar_at_s1",
         "fiscal_neutrality_feasible_under_output_neutrality",
         "extra_taxable_output_required_at_s1"]].round(3).to_string(index=False))
    print(f"\n  ANY parameterisation fiscally neutral under output neutrality: "
          f"{res['any_feasible']}")

    print("\n=== (2) break-even reemployment share, closed economy, omega = 0.75 ===")
    for k, v in be.items():
        print(f"  {k:24s} rho* = {v:.3f}" + ("  (infeasible, rho > 1)" if v > 1 else ""))

    print("\n=== (2) imported-robot corollary, m = 1, net per dollar displaced ===")
    q = GEN[(GEN["import_share_m"] == 1.0) & (GEN["g"] == 0.0)
            & (GEN["tau_l_source"] == "AMR")]
    print(q[["rho", "s", "revenue_retained", "revenue_required",
             "net_per_dollar", "fiscally_neutral"]].round(3).to_string(index=False))

    print("\n=== (6) LIKE-FOR-LIKE CHANNEL COMPARISON, 25 percent displacement ===")
    v = C[np.isclose(C["displacement"], 0.25)]
    print(v[["pathway", "displaced_wage_bill_usd_bn", "fiscal_loss_low_usd_bn",
             "fiscal_loss_high_usd_bn", "expected_credit_loss_low_usd_bn",
             "expected_credit_loss_high_usd_bn", "fiscal_to_credit_ratio_low",
             "fiscal_to_credit_ratio_high"]].round(2).to_string(index=False))


if __name__ == "__main__":
    main()
