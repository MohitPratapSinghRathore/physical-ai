"""Item 4: the SECOND-ROUND MODULE, governed by notes/prereg_second_round.md and its
addendum 4f to 4j, and amendment (c), the sovereign consolidation.

EVERYTHING HERE IS SCENARIO. The first-round table (src/dose_response.py) is an accounting
exercise on measured balances: displaced households, their obligations, their default
uplift. This module is not. It maps a dose onto a macroeconomic severity and then borrows
the Federal Reserve's own loss rates at that severity. Every number below is LABELLED
SCENARIO and reported as a BAND, and none of it is an estimate of what will happen.

THE REGISTERED EXPECTATIONS, written before running (notes/prereg_second_round.md):

  (i)  At moderate displacement, under about 25 percent of the total wage bill, only the
       public budget and the trust funds cross, in both columns. At large displacement the
       first-round column still shows little bank stress while the second-round column
       crosses through house prices, spending and business credit.

  (ii) Under NO POLICY RESPONSE, large displacement produces losses on bank books and public
       debt paths comparable to or beyond the Fed's severely adverse scenario, driven mainly
       by demand, house prices and business credit rather than by displaced borrowers' own
       loans. WITH RESPONSE most of that is avoided.

  (iii, amendment c) The federal government bears the majority of losses at every dose in
       both columns.

VERIFIED INPUTS, each read from the publisher this session.

  MPC          Mian, Straub and Sufi, "The Saving Glut of the Rich", NBER Working Paper
               26941, April 2020 revised July 2025, local copy in data/raw/manual/. From
               the paper: "the top 1% save at an exceptionally high rate, averaging well
               over 40% of their disposable income. The saving rate drops to 20% for the
               next 9%, falls to 12% for households in the 51st to 90th percentile, and is
               effectively zero for the bottom 50%, who live hand-to-mouth." The MPCs used
               here are ONE MINUS those saving rates, which is a derivation from the paper's
               numbers and not a figure the paper states. Labour income accrues across the
               distribution and capital income accrues overwhelmingly to the top, so the
               bands are MPC out of labour income 0.80 to 1.00 and MPC out of capital income
               0.35 to 0.55.

  House price  Harter-Dreiman, "Drawing Inferences about Housing Supply Elasticity from
               House Price Responses to Income Shocks", OFHEO Working Paper 03-2, December
               2003, local copy in data/raw/manual/. "The elasticity of price with respect
               to income in the national sample is 0.27; that is, a 10 percent increase in
               the level of real personal income increases the long-run equilibrium real
               price of housing by about 3 percent." And: "the income coefficient for the
               constrained MSAs is larger than the coefficient for the unconstrained MSAs
               (0.38 versus 0.21)". The constrained figure is what the prereg means by a
               larger response in cognitive-heavy high-cost metros; A36 established that
               cognitive exposure sits in high-home-value, high-wage areas. FLAGGED: this is
               a LONG-RUN equilibrium elasticity estimated on 1980 to 1998 data, so it
               describes where prices settle, not the path, and it is far below the
               peak-to-trough falls of an actual bust.

  Fed          2026 DFAST: severely adverse unemployment peaks at 10.0 percent, a rise of
               5.5 points; real GDP falls 4.6 percent peak to trough; house prices fall 30
               percent; CRE falls 39 percent. Total loan losses 624.9bn.

  Federal      FRED FGCCSAQ027S, Federal Government student loan assets, 1,605.1bn at
  student      2026:Q2 against 1,650bn of total student debt (NY Fed): 97.3 percent of the
               student loan book is federally held.

  Debt         FRED GFDEBTN total public debt and GDP.

WHAT IS NOT SOURCED AND IS THEREFORE A STATED ASSUMPTION, not a finding:

  Okun          the employment response to the demand shortfall uses a coefficient of 0.5,
                the textbook Okun relation. STATED ASSUMPTION.
  Credit supply the 4h contraction is a labelled sensitivity of 5, 10 and 20 percent extra
                house price decline in high-exposure metros. No verified elasticity of house
                prices to a credit supply contraction was obtained. STATED ASSUMPTION.
  r minus g     the debt paths use stated interest and growth assumptions, below.
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
sys.path.insert(0, str(ROOT))

WB_LEVELS = [0.05, 0.10, 0.25, 0.50, 0.75]
TYPES = ["embodied", "cognitive_AIOE", "cognitive_GPT"]

MPC_LABOUR = (0.80, 1.00)         # derived from MSS saving rates, see the docstring
MPC_CAPITAL = (0.35, 0.55)
HP_ELASTICITY = {"national": 0.27, "constrained_high_cost": 0.38, "unconstrained": 0.21}
OKUN = 0.5                        # STATED ASSUMPTION

FED = {
    "unemployment_peak": 0.100, "unemployment_rise_pp": 5.5,
    "gdp_fall": 0.046, "house_prices": -0.30, "cre_prices": -0.39,
    "total_loan_losses_bn": 624.9,
    "losses_bn": {"first_lien_mortgage": 22.5, "junior_heloc": 5.5, "credit_card": 203.0,
                  "other_consumer": 54.1, "cre": 76.5, "business_credit": 158.2,
                  "other": 105.0},
}
FEDERAL_STUDENT_SHARE = 1605.134 / 1650.0     # FRED FGCCSAQ027S over NY Fed total
CREDIT_SUPPLY_EXTRA_HP_FALL = (0.05, 0.10, 0.20)   # STATED ASSUMPTION, 4h
DEFLATION_LEVELS = (0.05, 0.10, 0.20)              # 4g
# 4i, STATED ASSUMPTIONS for the debt paths
RATE_GROWTH = {"reserve_currency": {"r": 0.040, "g": 0.040},
               "reserve_currency_adverse": {"r": 0.050, "g": 0.035},
               "emerging_market": {"r": 0.090, "g": 0.030}}


def fred_last(series, scale=1.0):
    d = pd.read_csv(RAW / "fred" / f"{series}.csv")
    d.columns = ["date", "v"]
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    d = d.dropna()
    return float(d["v"].iloc[-1]) * scale, str(d["date"].iloc[-1])


# ---------------------------------------------------------------- 4a, 4f: severity
def severity(cap, fx):
    """Map each dose onto a macro severity: the fall in aggregate wage income, the demand
    shortfall after the shift from labour to capital income, the rise in prime-age
    nonemployment, and the long-run house price response."""
    gdp = cap["gdp_bn"]
    # THE BASE, corrected in the replication-repair session. A dose is a SHARE of the total
    # wage bill; the dollars are that share of the NATIONAL wage bill (FRED WASCUR), not of
    # this project's occupational grid, which covers 73.9 percent of it. The old code used
    # the grid and understated every macro dollar in this module by a factor of 1.354.
    # src/consistency.py and src/fiscal_extended_axis.py now use the same base.
    wb = cap["national_wage_bill_bn"]
    rows = []
    for t in TYPES:
        g = fx[fx["type"] == t]
        for d in WB_LEVELS:
            up = g[g["share_of_total_wage_bill"] >= d]
            src = up.nsmallest(1, "share_of_total_wage_bill") if len(up) \
                else g.nlargest(1, "share_of_total_wage_bill")
            key = src.iloc[0]
            sel = g[(g["group"] == key["group"])
                    & (g["level_of_exposed"] == key["level_of_exposed"])
                    & (g["rho_mode"] == "fitted") & (g["horizon"] == 10)]
            R = float(sel["R"].mean())
            delivered = float(key["share_of_total_wage_bill"])
            nonemp = float(sel["nonemployment_terminal"].mean())
            inside = not bool(sel["outside_data"].any())
            # net fall in aggregate wage income after reemployment at omega
            dW = delivered * (1 - R) * wb
            for lab, (ml, mk) in [("low", (MPC_LABOUR[0], MPC_CAPITAL[1])),
                                  ("high", (MPC_LABOUR[1], MPC_CAPITAL[0]))]:
                dC = (ml - mk) * dW
                rows.append({
                    "exposure_type": t, "dose": d, "delivered": delivered,
                    "band": lab, "R": R, "inside_observed_data_range": inside,
                    "wage_income_fall_bn": dW,
                    "wage_income_fall_pct": 100 * dW / wb,
                    "consumption_fall_bn": dC,
                    "consumption_fall_pct_gdp": 100 * dC / gdp,
                    "prime_age_nonemployment_terminal_pct": nonemp,
                    "hp_fall_national_pct": -100 * HP_ELASTICITY["national"] * dW / wb,
                    "hp_fall_high_cost_metro_pct":
                        -100 * HP_ELASTICITY["constrained_high_cost"] * dW / wb,
                    "hp_fall_low_cost_metro_pct":
                        -100 * HP_ELASTICITY["unconstrained"] * dW / wb,
                    # 4b: where this sits against the Fed severely adverse scenario
                    "severity_vs_fed_on_demand": (dC / gdp) / FED["gdp_fall"],
                    "severity_vs_fed_on_house_prices":
                        (HP_ELASTICITY["national"] * dW / wb) / abs(FED["house_prices"]),
                    # 4f: second-round job losses, Okun, STATED ASSUMPTION
                    "second_round_job_losses_pct_of_employment":
                        100 * OKUN * (dC / gdp),
                })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- 4c, 4e: Fed mapping
def fed_mapping(S):
    """At or beyond the Fed's severity, apply the Fed's own loss rates to the WHOLE books,
    scaled by the severity ratio, with bands beyond. Business credit, CRE and cards enter
    ONLY through this mapping, per the prereg."""
    rows = []
    for _, r in S.iterrows():
        s = r["severity_vs_fed_on_demand"]
        # the mapping is the Fed's loss at Fed severity; below it, scaled linearly; beyond
        # it, scaled linearly and reported as a band because the Fed publishes no rates
        # beyond its own scenario
        row = {k: r[k] for k in ["exposure_type", "dose", "delivered", "band",
                                 "inside_observed_data_range"]}
        row["severity_ratio"] = s
        row["at_or_beyond_fed_severity"] = s >= 1.0
        for book, loss in FED["losses_bn"].items():
            row[f"{book}_bn"] = loss * s
        row["total_second_round_bank_losses_bn"] = FED["total_loan_losses_bn"] * s
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- 4g: debt deflation
def debt_deflation():
    """Prices and wages fall while nominal debt does not. The debt service to income ratio
    rises by 1/(1-x) - 1. The implied change in the share of obligated working-core
    households above a 50 percent DSTI is computed from the ACS distribution directly."""
    from src.stress import acs_engine as AE
    P, H = AE.load_acs(with_reps=False)
    P, j = AE.link(P, H)
    oblig = H["mort"].to_numpy(np.float64) + H["rent"].to_numpy(np.float64)
    inc = H["hincp"].to_numpy(np.float64)
    wt = H["wgtp"].to_numpy(np.float64)
    core = H["working_core"].to_numpy(bool)
    m = core & (oblig > 0) & (inc > 0)
    dsti = oblig[m] / inc[m]
    w = wt[m]
    base = float((w * (dsti > 0.50)).sum() / w.sum())
    rows = [{"price_and_wage_fall": 0.0, "dsti_multiplier": 1.0,
             "share_above_dsti_50": base, "increment_pp": 0.0,
             "implied_default_uplift_pp": 0.0}]
    for x in DEFLATION_LEVELS:
        mult = 1.0 / (1.0 - x)
        sh = float((w * (dsti * mult > 0.50)).sum() / w.sum())
        # GHOW exchange rate: job loss, worth +5.0pp of default probability, is equivalent
        # to a 35 percent equity decline. A fall of x in prices is x/0.35 of that unit.
        rows.append({"price_and_wage_fall": x, "dsti_multiplier": mult,
                     "share_above_dsti_50": sh, "increment_pp": 100 * (sh - base),
                     "implied_default_uplift_pp": 5.0 * x / 0.35})
    return pd.DataFrame(rows), base


# ---------------------------------------------------------------- 4i: debt dynamics
def debt_paths(S, cap):
    gdp = cap["gdp_bn"]
    debt_bn, debt_date = fred_last("GFDEBTN", 1e-3)      # millions to billions
    b0 = debt_bn / gdp
    fx = pd.read_csv(OUT / "fiscal_extended_axis.csv")
    fx["type"] = fx["group"].str.replace(r"_top\d+", "", regex=True)
    rows = []
    for _, r in S[S.band == "high"].iterrows():
        g = fx[(fx["type"] == r.exposure_type)
               & np.isclose(fx["share_of_total_wage_bill"], r.delivered)
               & (fx["rho_mode"] == "fitted") & (fx["tau_l"] == "bottom_up_0.301")
               & (fx["tau_k_reading"] == "barkai_rent_0.351") & (fx["horizon"] == 10)]
        for outl in ["no_outlays", "with_outlays"]:
            gg = g[g["outlays"] == outl]
            if not len(gg):
                continue
            loss = float(gg["terminal_year_loss_bn"].mean())
            for reg, p in RATE_GROWTH.items():
                for H_ in (10, 20):
                    b, r_, gr = b0, p["r"], p["g"]
                    for _ in range(H_):
                        b = b * (1 + r_) / (1 + gr) + loss / gdp
                    rows.append({"exposure_type": r.exposure_type, "dose": r.dose,
                                 "outlays": outl, "regime": reg, "horizon": H_,
                                 "annual_fiscal_loss_bn": loss,
                                 "debt_to_gdp_start": b0, "debt_to_gdp_end": b,
                                 "interest_cost_pct_gdp_end": r_ * b,
                                 "r": r_, "g": gr})
    return pd.DataFrame(rows), b0, debt_date


# ---------------------------------------------------------------- 4j and (c)
def consolidate(D, F, cap):
    """Amendment (c), the SOVEREIGN CONSOLIDATION. Sum every loss that ultimately lands on
    the federal government and compare it with the sum landing on private balance sheets.

    WHAT COUNTS AS FEDERAL, and why.

      general revenue      the public budget row
      OASDI and HI         payroll-funded federal trust funds
      federal student      97.3 percent of the student book is a federal asset, FRED
                           FGCCSAQ027S against the NY Fed total
      FHA                  the Mutual Mortgage Insurance Fund is a federal fund; a loss
                           there is a federal loss on the first dollar
      GSE beyond capacity  the Enterprises are in conservatorship. Losses are absorbed
                           FIRST by the credit risk transferred to private investors and by
                           private mortgage insurance, THEN by Enterprise capital and one
                           year of pre-provision earnings, and only BEYOND that does the
                           Treasury senior preferred agreement bind. Only that last layer is
                           counted as federal.

    WHAT COUNTS AS PRIVATE: bank mortgage portfolios, CRT and private mortgage insurance
    investors, the residual mortgage holders, auto lenders, card lenders, the private slice
    of the student book, and in the second-round column the whole of the Fed-mapped bank
    loss.

    NOT COUNTED ANYWHERE: scenario outlays, which are reported on their own line because
    they are a policy choice rather than a loss, and VA, which has no separate fund and
    whose losses are federal on the first dollar but whose book size was not sourced.
    """
    C = cap["sheets"]
    gse_cap = C["mortgage_agency"]["capacity_bn"]
    L = C["mortgage_agency"]["layers"]
    gse_first_loss = L["crt_risk_in_force_bn"] + L["pmi_total_bn"]
    gse_equity_layer = gse_cap + L["annual_pre_provision_pre_tax_earnings_bn"]
    rows = []
    for _, d in D.iterrows():
        f = F[(F.exposure_type == d.exposure_type)
              & np.isclose(F.dose, d.dose_share_of_total_wage_bill) & (F.band == "high")]
        second = f.iloc[0] if len(f) else None

        student_bank = d.student_loan_holders_loss_hi_bn
        student_total = student_bank / 0.449          # the bank share used upstream
        student_fed = student_total * FEDERAL_STUDENT_SHARE

        gse_loss = d.mortgage_agency_loss_hi_bn
        transferred = min(gse_loss, gse_first_loss)
        gse_retained = gse_loss - transferred
        gse_beyond = max(0.0, gse_retained - gse_equity_layer)
        gse_absorbed = gse_retained - gse_beyond

        fha_loss = d.get("mortgage_FHA_loss_hi_bn", 0.0)

        fed1 = (d.public_budget_loss_hi_bn + d.oasdi_loss_hi_bn + d.hi_loss_hi_bn
                + student_fed + fha_loss + gse_beyond)
        priv1 = (d.mortgage_bank_held_loss_hi_bn
                 + d.get("mortgage_residual_holders_loss_hi_bn", 0.0)
                 + d.auto_lenders_loss_hi_bn + d.card_consumer_lenders_loss_hi_bn
                 + (student_total - student_fed) + transferred + gse_absorbed)

        row = {"exposure_type": d.exposure_type, "dose": d.dose_share_of_total_wage_bill,
               "horizon": d.horizon_years, "incidence": d.incidence,
               "inside_observed_data_range": d.inside_observed_data_range,
               "general_revenue_bn": d.public_budget_loss_hi_bn,
               "oasdi_bn": d.oasdi_loss_hi_bn, "hi_bn": d.hi_loss_hi_bn,
               "federal_student_bn": student_fed, "fha_bn": fha_loss,
               "gse_loss_bn": gse_loss,
               "gse_transferred_to_CRT_and_PMI_bn": transferred,
               "gse_absorbed_by_capital_and_earnings_bn": gse_absorbed,
               "gse_beyond_capacity_federal_bn": gse_beyond,
               "federal_first_round_bn": fed1, "private_first_round_bn": priv1,
               "federal_share_first_round": fed1 / max(fed1 + priv1, 1e-9)}
        if second is not None:
            sec_priv = float(second["total_second_round_bank_losses_bn"])
            # The federal side also grows in the second round: the demand shortfall is
            # itself taxed income, so general revenue falls again. It is charged at the
            # same effective labour tax rate used throughout, 0.301.
            sec_fed = 0.301 * float(second["severity_ratio"]) * FED["gdp_fall"] \
                * cap["gdp_bn"]
            row.update({
                "second_round_private_bn": sec_priv,
                "second_round_federal_bn": sec_fed,
                "severity_ratio": float(second["severity_ratio"]),
                "federal_share_with_second_round":
                    (fed1 + sec_fed) / max(fed1 + sec_fed + priv1 + sec_priv, 1e-9),
                "total_with_second_round_bn": fed1 + sec_fed + priv1 + sec_priv,
            })
        rows.append(row)
    return pd.DataFrame(rows)


def two_worlds(K, S, cap):
    """4j. NO POLICY RESPONSE against WITH RESPONSE.

    THE INSTRUMENTS, from framework/architecture_spec.md. NOTE that framework/architecture.md
    itself is NOT YET BUILT: it is gated on the owner approving a thesis statement. What is
    modelled here is the specification's three named instruments, not a built table.

      1. Tax the surplus at the break-even rate. P1r gives the condition directly: the
         capital tax rate that holds the fiscal position neutral is tau_k = tau_l * (1 - R),
         where R is the retained wage share. Revenue raised equals the general revenue loss
         by construction, because that is what break-even means.
      2. Replacement income funded from it. Wage income is restored to the displaced, so
         the demand shortfall and everything that follows from it does not occur.
      3. Displacement-contingent debt relief, which removes the first-round credit losses
         on displaced borrowers.

    WHAT THE RESPONSE DOES NOT REMOVE, and this is the point of reporting it:

      a. The PAYROLL-FUNDED trust funds. Replacement income financed from a capital tax is
         not covered wages, so OASDI and HI lose their base whether or not the household is
         made whole. Unless the replacement is itself made payroll-taxable, which is a
         design choice with its own incidence, the trust fund loss survives in full.
      b. The share of the surplus that the capital tax cannot reach. Torslov, Wier and
         Zucman find a large share of multinational profit booked in tax havens; the capital
         tax base is therefore smaller than the surplus, and the shortfall is reported as a
         band rather than assumed away.
      c. Nothing about output. Output is held constant in every scenario here, so the
         losses the response removes were never resource losses. They were distributional.
    """
    rows = []
    for _, k in K.iterrows():
        s = S[(S.exposure_type == k.exposure_type) & np.isclose(S.dose, k.dose)
              & (S.band == "high")]
        R = float(s["R"].mean()) if len(s) else np.nan
        no_resp = k.get("total_with_second_round_bn", np.nan)
        # WITH RESPONSE: general revenue is made whole by the surplus tax; replacement
        # income removes the demand channel and the first-round credit losses; the trust
        # funds and the unreachable tax base remain.
        for leak_lab, leak in (("no_leakage", 0.0), ("haven_leakage_20pct", 0.20)):
            remaining = (k.oasdi_bn + k.hi_bn
                         + leak * k.general_revenue_bn)
            rows.append({
                "exposure_type": k.exposure_type, "dose": k.dose,
                "leakage_case": leak_lab,
                "retained_wage_share_R": R,
                "break_even_tau_k": 0.301 * (1 - R) if R == R else np.nan,
                "no_response_total_bn": no_resp,
                "with_response_total_bn": remaining,
                "removed_bn": (no_resp - remaining) if no_resp == no_resp else np.nan,
                "share_removed": (1 - remaining / no_resp) if no_resp == no_resp else np.nan,
            })
    return pd.DataFrame(rows)



# ---------------------------------------------------------------- the two columns
BANK_SHEETS = {"mortgage_bank_held": "first_lien_mortgage", "auto_lenders": "other_consumer",
               "card_consumer_lenders": "credit_card", "student_loan_holders": "other_consumer"}
MATERIALITY = 0.25       # central tightness from A82, on each sheet's own yardstick


def two_column_table(D, F, cap):
    """The dose-response table with a SECOND set of columns: first round, and with
    second-round effects. Item 4 of the final session."""
    C = cap["sheets"]
    fed_losses = FED["losses_bn"]
    rows = []
    for _, d in D.iterrows():
        f = F[(F.exposure_type == d.exposure_type)
              & np.isclose(F.dose, d.dose_share_of_total_wage_bill) & (F.band == "high")]
        if not len(f):
            continue
        s = f.iloc[0]
        row = {"exposure_type": d.exposure_type,
               "dose": d.dose_share_of_total_wage_bill,
               "horizon": d.horizon_years, "incidence": d.incidence,
               "inside_observed_data_range": d.inside_observed_data_range,
               "severity_ratio": float(s["severity_ratio"])}
        crossed1, crossed2 = [], []
        # public budget and trust funds: first round only, they have no Fed-mapped column
        for sheet, thresh_basis in [("public_budget", C["public_budget"]["capacity_bn"]),
                                    ("oasdi", C["oasdi"]["capacity_bn"]),
                                    ("hi", C["hi"]["capacity_bn"])]:
            v1 = d[f"{sheet}_loss_hi_bn"]
            row[f"{sheet}_first_round_bn"] = v1
            row[f"{sheet}_second_round_bn"] = v1 + (
                0.301 * float(s["severity_ratio"]) * FED["gdp_fall"] * cap["gdp_bn"]
                if sheet == "public_budget" else 0.0)
            # threshold: A82's sourced bars, central tightness
            bar = {"public_budget": 0.066, "oasdi": 0.121, "hi": 0.121}[sheet] * thresh_basis
            if v1 >= bar:
                crossed1.append(sheet)
            if row[f"{sheet}_second_round_bn"] >= bar:
                crossed2.append(sheet)
        # agency and FHA, against their own capital
        for sheet, capk in [("mortgage_agency", "mortgage_agency"),
                            ("mortgage_FHA", "mortgage_agency_FHA")]:
            v1 = d.get(f"{sheet}_loss_hi_bn", 0.0)
            row[f"{sheet}_first_round_bn"] = v1
            # the second round adds the Fed-mapped first-lien loss in proportion to holding
            v2 = v1 + float(s["first_lien_mortgage_bn"]) * (
                MORTGAGE_HOLDER[sheet] / MORTGAGE_HOLDER["bank_portfolio"])
            row[f"{sheet}_second_round_bn"] = v2
            bar = MATERIALITY * C[capk]["capacity_bn"]
            if v1 >= bar:
                crossed1.append(sheet)
            if v2 >= bar:
                crossed2.append(sheet)
        # bank books, against the Fed's own loss for that book
        for sheet, book in BANK_SHEETS.items():
            v1 = d[f"{sheet}_loss_hi_bn"]
            v2 = v1 + float(s[f"{book}_bn"])
            row[f"{sheet}_first_round_bn"] = v1
            row[f"{sheet}_second_round_bn"] = v2
            bar = MATERIALITY * fed_losses[book]
            if v1 >= bar:
                crossed1.append(sheet)
            if v2 >= bar:
                crossed2.append(sheet)
        # business credit and CRE exist only in the second round
        for sheet, book in [("business_credit", "business_credit"),
                            ("commercial_real_estate", "cre")]:
            row[f"{sheet}_first_round_bn"] = 0.0
            v2 = float(s[f"{book}_bn"])
            row[f"{sheet}_second_round_bn"] = v2
            if v2 >= MATERIALITY * fed_losses[book]:
                crossed2.append(sheet)
        row["crossed_first_round"] = ";".join(crossed1)
        row["crossed_second_round"] = ";".join(crossed2)
        row["n_crossed_first_round"] = len(crossed1)
        row["n_crossed_second_round"] = len(crossed2)
        rows.append(row)
    return pd.DataFrame(rows)


MORTGAGE_HOLDER = {"mortgage_agency": 6694.0 / 13100.0,
                   "mortgage_FHA": 1647.0 / 13100.0,
                   "bank_portfolio": 1500.0 / 13100.0}


def main():
    cap = json.loads((OUT / "capacities.json").read_text())
    fx = pd.read_csv(OUT / "fiscal_extended_axis.csv")
    fx["type"] = fx["group"].str.replace(r"_top\d+", "", regex=True)
    fx = fx[fx["type"].isin(TYPES) & (fx["tau_l"] == "bottom_up_0.301")
            & (fx["tau_k_reading"] == "barkai_rent_0.351")]
    pd.set_option("display.width", 260)

    # ---------------- 4a, 4b, 4f
    S = severity(cap, fx)
    S.round(4).to_csv(OUT / "second_round_severity.csv", index=False)
    print("=== 4a AND 4f: MACRO SEVERITY AND THE DEMAND SHORTFALL. ALL SCENARIO ===")
    print(f"  MPC out of labour income {MPC_LABOUR}, out of capital income {MPC_CAPITAL}, "
          f"derived as one minus the\n  saving rates in Mian, Straub and Sufi 2025. "
          f"Output is held CONSTANT, so every dollar of\n  wage income lost becomes a dollar "
          f"of capital income: the shortfall is a DISTRIBUTIONAL\n  failure, not a resource "
          f"shortage.")
    v = S[(S.band == "high") & (S.exposure_type == "cognitive_AIOE")]
    print("\n  cognitive AIOE, upper end of the demand band:")
    print(v[["dose", "delivered", "wage_income_fall_pct", "consumption_fall_bn",
             "consumption_fall_pct_gdp", "hp_fall_national_pct",
             "hp_fall_high_cost_metro_pct", "severity_vs_fed_on_demand",
             "second_round_job_losses_pct_of_employment",
             "inside_observed_data_range"]].round(2).to_string(index=False))

    print("\n=== 4b: WHERE EACH DOSE SITS AGAINST THE FED SEVERELY ADVERSE SCENARIO ===")
    print("    ratio of the scenario's demand shortfall to the Fed's 4.6 percent GDP fall")
    print(S[S.band == "high"].pivot_table(index="dose", columns="exposure_type",
                                          values="severity_vs_fed_on_demand"
                                          ).round(2).to_string())
    print("\n    and on house prices, against the Fed's 30 percent fall")
    print(S[S.band == "high"].pivot_table(index="dose", columns="exposure_type",
                                          values="severity_vs_fed_on_house_prices"
                                          ).round(3).to_string())

    # ---------------- 4c, 4e
    F = fed_mapping(S)
    F.round(3).to_csv(OUT / "second_round_fed_mapping.csv", index=False)
    print("\n=== 4c AND 4e: THE FED'S OWN LOSS RATES APPLIED TO THE WHOLE BOOKS ===")
    print("    business credit, CRE and cards enter ONLY through this mapping, per the "
          "prereg.\n    Beyond the Fed's own severity the numbers are an EXTRAPOLATION of "
          "its rates and are\n    labelled as such.")
    w = F[(F.band == "high") & (F.exposure_type == "cognitive_AIOE")]
    print(w[["dose", "severity_ratio", "at_or_beyond_fed_severity", "business_credit_bn",
             "cre_bn", "credit_card_bn", "first_lien_mortgage_bn",
             "total_second_round_bank_losses_bn"]].round(1).to_string(index=False))

    # ---------------- 4g
    G, base = debt_deflation()
    G.round(4).to_csv(OUT / "second_round_debt_deflation.csv", index=False)
    print(f"\n=== 4g: PRICES AND WAGES FALL, NOMINAL DEBT DOES NOT ===")
    print(f"    baseline share of obligated working-core households above DSTI 50: "
          f"{base:.2%}")
    print(G.round(4).to_string(index=False))
    print("    The default uplift column uses the Gerardi, Herkenhoff, Ohanian and Willen "
          "exchange\n    rate: job loss is worth 5.0 points of default probability and is "
          "equivalent to a 35\n    percent equity decline. FLAGGED: that is an equity "
          "mapping used here for a price level\n    fall, which is an extension of their "
          "result, not their result.")

    # ---------------- 4h
    print("\n=== 4h: CREDIT SUPPLY TIGHTENS BEFORE DEFAULTS ARRIVE. LABELLED SENSITIVITY ===")
    print("    No verified elasticity of house prices to a lender pullback was obtained, so "
          "this is\n    a STATED ASSUMPTION and not an estimate. Additional house price fall "
          "in high-exposure\n    metros, on top of the income-driven fall:")
    hp = S[(S.band == "high") & (S.exposure_type == "cognitive_AIOE")]
    for _, r in hp.iterrows():
        extra = [f"{-(abs(r.hp_fall_high_cost_metro_pct) + 100 * e):.1f}%"
                 for e in CREDIT_SUPPLY_EXTRA_HP_FALL]
        print(f"    dose {r.dose:>4.0%}: income-driven {r.hp_fall_high_cost_metro_pct:6.1f}%"
              f"   with a 5, 10 or 20 point pullback: {', '.join(extra)}")

    # ---------------- 4i
    B, b0, debt_date = debt_paths(S, cap)
    B.round(4).to_csv(OUT / "second_round_debt_paths.csv", index=False)
    print(f"\n=== 4i: FEDERAL DEBT DYNAMICS. debt to GDP starts at {b0:.1%} ({debt_date}) ===")
    print("    STATED ASSUMPTIONS: reserve currency r = g = 4.0 percent; an adverse reserve "
          "currency\n    case r 5.0 against g 3.5; an emerging market that cannot borrow "
          "freely in its own\n    currency r 9.0 against g 3.0. No CBO baseline: CBO "
          "publication pages return HTTP 403.")
    bb = B[(B.exposure_type == "cognitive_AIOE") & (B.outlays == "no_outlays")]
    print(bb.pivot_table(index=["dose", "horizon"], columns="regime",
                         values="debt_to_gdp_end").round(2).to_string())

    # ---------------- 4j and amendment (c)
    D = pd.read_csv(OUT / "dose_response_first_round.csv")
    D = D[(D.horizon_years == 10) & (D.incidence == "c_sourced_mix")]
    K = consolidate(D, F, cap)
    K.round(3).to_csv(OUT / "sovereign_consolidation.csv", index=False)
    print("\n=== AMENDMENT (c): WHO ULTIMATELY BEARS THE LOSS ===")
    print(f"    97.3 percent of student debt is federally held (FRED FGCCSAQ027S). GSE "
          f"losses are\n    absorbed first by CRT and private mortgage insurance, then by "
          f"Enterprise capital, and\n    only beyond that by the federal government under "
          f"conservatorship.")
    print(K[["exposure_type", "dose", "federal_first_round_bn", "private_first_round_bn",
             "federal_share_first_round", "second_round_private_bn",
             "federal_share_with_second_round", "inside_observed_data_range"]
            ].round(3).to_string(index=False))

    maj1 = (K["federal_share_first_round"] > 0.5).mean()
    maj2 = (K["federal_share_with_second_round"] > 0.5).mean()
    print(f"\n  REGISTERED EXPECTATION (c): the federal government bears the MAJORITY at "
          f"every dose in both columns.")
    print(f"    first round: majority in {maj1:.0%} of rows")
    print(f"    with second round: majority in {maj2:.0%} of rows")
    print(f"    VERDICT: {'CONFIRMED' if maj1 == 1 and maj2 == 1 else 'REFUTED as stated'}")

    # ---------------- the two columns, and the registered expectations
    T2 = two_column_table(D, F, cap)
    T2.round(3).to_csv(OUT / "dose_response_two_columns.csv", index=False)
    print("\n=== THE DOSE-RESPONSE TABLE WITH BOTH COLUMNS. Which sheets cross 25 percent "
          "of their own yardstick ===")
    for _, r in T2.iterrows():
        print(f"  {r.exposure_type:15s} dose {r.dose:>4.0%}  "
              f"[{'inside' if r.inside_observed_data_range else 'OUTSIDE'} the data]")
        print(f"      first round  ({r.n_crossed_first_round}): "
              f"{r.crossed_first_round or 'nothing crosses'}")
        print(f"      second round ({r.n_crossed_second_round}): "
              f"{r.crossed_second_round or 'nothing crosses'}")

    print("\n=== REGISTERED EXPECTATION (i), from notes/prereg_second_round.md ===")
    print("  'At moderate displacement, under about 25 percent, only the public budget and "
          "the trust\n   funds cross, in both columns. At large displacement the first-round "
          "column still shows\n   little bank stress while the second-round column crosses.'")
    mod = T2[T2.dose <= 0.10]
    fiscal = {"public_budget", "oasdi", "hi"}
    mod_ok = all(set(filter(None, r.crossed_first_round.split(";"))) <= fiscal
                 and set(filter(None, r.crossed_second_round.split(";"))) <= fiscal
                 for _, r in mod.iterrows())
    big = T2[T2.dose >= 0.50]
    big_first_banks = [len(set(filter(None, r.crossed_first_round.split(";"))) - fiscal)
                       for _, r in big.iterrows()]
    big_second = [r.n_crossed_second_round for _, r in big.iterrows()]
    print(f"    moderate doses, only fiscal sheets cross in both columns: "
          f"{'YES' if mod_ok else 'NO'}")
    print(f"    large doses, non-fiscal sheets crossing in the FIRST round: "
          f"{min(big_first_banks)} to {max(big_first_banks)}")
    print(f"    large doses, sheets crossing in the SECOND round: "
          f"{min(big_second)} to {max(big_second)}")

    print("\n=== REGISTERED EXPECTATION (ii) ===")
    for dose in (0.50, 0.75):
        sub = T2[np.isclose(T2.dose, dose)]
        if not len(sub):
            continue
        fr = sum(sub.iloc[0][f"{s}_first_round_bn"] for s in BANK_SHEETS)
        sr = sum(sub.iloc[0][f"{s}_second_round_bn"] for s in BANK_SHEETS) + \
            sub.iloc[0]["business_credit_second_round_bn"] + \
            sub.iloc[0]["commercial_real_estate_second_round_bn"]
        print(f"    dose {dose:.0%}: bank losses first round {fr:,.0f}bn, with second round "
              f"{sr:,.0f}bn\n              against the Fed severely adverse "
              f"{FED['total_loan_losses_bn']:,.1f}bn, a ratio of {sr / FED['total_loan_losses_bn']:.2f}"
              f"\n              share of the two-column total coming from the SECOND round: "
              f"{1 - fr / sr:.0%}")

    # ---------------- 4j
    W = two_worlds(K, S, cap)
    W.round(4).to_csv(OUT / "two_worlds.csv", index=False)
    print("\n=== 4j: TWO WORLDS. NO POLICY RESPONSE against WITH RESPONSE ===")
    print("  The instruments are those named in framework/architecture_spec.md. "
          "framework/architecture.md\n  itself is NOT YET BUILT: it is gated on owner "
          "approval of a thesis statement.")
    print(W[W.leakage_case == "no_leakage"][
        ["exposure_type", "dose", "retained_wage_share_R", "break_even_tau_k",
         "no_response_total_bn", "with_response_total_bn", "share_removed"]
    ].round(3).to_string(index=False))
    print("\n  with a 20 percent leakage of the surplus beyond the reach of the capital tax:")
    print(W[W.leakage_case == "haven_leakage_20pct"][
        ["exposure_type", "dose", "with_response_total_bn", "share_removed"]
    ].round(3).to_string(index=False))
    print("\n  WHAT THE RESPONSE DOES NOT REMOVE: the payroll-funded trust funds, because "
          "replacement\n  income financed from a capital tax is not covered wages. That is a "
          "design choice, not a\n  law of nature, and making the replacement payroll-taxable "
          "would close it.")
    print("  OUTPUT IS PRESERVED IN EVERY SCENARIO HERE. The losses are DISTRIBUTIONAL "
          "FAILURES,\n  not resource shortages.")

    (OUT / "second_round_summary.json").write_text(json.dumps({
        "mpc_labour": list(MPC_LABOUR), "mpc_capital": list(MPC_CAPITAL),
        "hp_elasticity": HP_ELASTICITY, "okun": OKUN,
        "federal_student_share": FEDERAL_STUDENT_SHARE,
        "debt_to_gdp_start": b0, "debt_date": debt_date,
        "baseline_dsti50_share": base,
        "federal_majority_first_round_share_of_rows": float(maj1),
        "federal_majority_with_second_round_share_of_rows": float(maj2),
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
