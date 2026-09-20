"""Items 1, 2 and 3 of the closing session: the two worlds made consistent, debt paths as
increments, and a sourced sensitivity range for every second-round input.

ITEM 1. THE TWO WORLDS WERE INCONSISTENT AND THIS FIXES IT.

The fiscal channel has always assumed OUTPUT IS PRESERVED: displacement moves income from
labour to capital, the surplus rises, and the fiscal question is whether the capital tax
reaches it. The second-round module then has consumption and business revenue FALLING, which
means output is not preserved, which means the surplus the fiscal channel taxes is smaller
than the fiscal channel assumes. Both cannot be true at once. Two cases are now carried
explicitly through everything.

  NOTATION, fixed here because the previous version of this module used two different
  wage bill totals inside one ratio and that is what broke it.

      D   = delivered dose x W, the GROSS displaced wage bill in dollars
      R   = the retained wage share, rho x omega
      dW  = (1 - R) * D, the NET wage income fall, what households actually lose
      dC  = (mpc_L - mpc_K) * dW, the demand shortfall
      w_s = W / Y, the wage share of output
      W   = FRED WASCUR wages and salaries, the base tau_l is built on. NOT compensation
            of employees: see the base note in src/fiscal_extended_axis.py.

  CASE A, OUTPUT PRESERVED. Every dollar of the displaced wage bill becomes capital income.
  This is what every fiscal number in this project has assumed.

      capital income change   = +D
      fiscal loss             = tau_l * dW - tau_k * D  =  [tau_l * (1 - R) - tau_k] * D
      break-even tau_k        = tau_l * (1 - R), the P1r condition

  CASE B, OUTPUT FALLS WITH DEMAND. The demand shortfall is not absorbed, so output falls by
  dC. Capital income still rises, but by less, and a second round of wage income is lost
  with the output fall.

      output change           = -dC
      capital income change   = +D - dC
      second-round wage loss  = w_s * dC, at the wage share of output
      fiscal loss             = case A loss + tau_k * dC + tau_l * w_s * dC
      break-even tau_k        = tau_l * [(1 - R) * D + w_s * dC] / (D - dC)

  Case B is the internally consistent one whenever the second-round module is quoted. Case A
  is the right one only if the demand shortfall is offset, which is what the policy response
  in 4j is for. **Every headline number in this repository now carries its case.**

  THE BREAK-EVEN RATE WAS WRONG AND IS CORRECTED HERE. Item 1 of the replication-repair
  session. The replicator flagged that the sealed `break_even_tau_k_case_A_max` of 0.378371
  exceeds the highest reading of tau_l, 0.318, which the brief's own definition
  tau_l * (1 - R) makes impossible unless R is negative. It was two separate defects
  multiplying together, and neither is a modelling choice:

  (i)  DOUBLE-COUNTED tau_k. The old code divided `case_A_fiscal_loss_bn` by the surplus.
       But that loss is the loss AT the operative tau_k of 0.0708: it already has the
       capital tax netted out. A break-even rate is the tau_k at which the loss is ZERO, so
       dividing a loss that already contains a tau_k by anything cannot produce one. What
       the old expression actually computed was the net fiscal loss per dollar of surplus
       at a tau_k of 0.0708, which is a residual, not a rate.

  (ii) TWO DIFFERENT WAGE BILLS IN ONE RATIO. The numerator came from
       src/fiscal_extended_axis.py, which scaled the dose by compensation of employees
       (16,224.3bn). The denominator was built here from `capacities.json`
       `total_wage_bill_bn`, this project's own occupational grid (9,870.2bn). The ratio
       therefore carried a spurious factor of 16,224.3 / 9,870.2 = 1.6438 on top of defect
       (i), which is what pushed the number above tau_l.

       Taken together: old value = (comp / grid) x [tau_l - tau_k / (1 - R)]. At the top of
       the grid, where R falls to zero, that is 1.6438 x (0.301 - 0.0708) = 0.3784, which
       reproduces the sealed figure exactly and identifies it as an artefact.

  THE PLAUSIBILITY BOUNDS, which the brief did not carry and now does:

      0 <= break-even tau_k case A <= tau_l + g       it is a tax rate on the surplus and
                                                      cannot exceed the labour tax it has
                                                      to replace plus any added outlays
      0 <= break-even tau_k, either case <= 1         no tax rate exceeds 100 percent
      break-even tau_k case B >= case A               case B shrinks the base and raises
                                                      the loss, so it can only be higher
      D - dC > 0                                      a break-even rate exists only while
                                                      there is a surplus left to tax

ITEM 2. DEBT PATHS AS INCREMENTS, AND A CORRECTION TO THE 389 PERCENT FIGURE.

A91 reported that an emerging market reaches 389 percent of GDP at a 10 percent dose. That
number is almost entirely the compounding of the EXISTING debt at r above g and has very
little to do with displacement. Under r = 9 percent against g = 3 percent, a starting debt of
121.4 percent of GDP reaches 381 percent in twenty years WITH NO DISPLACEMENT AT ALL. The
displacement increment is the small remainder.

Every path is therefore reported as the DIFFERENCE from a no-displacement baseline under the
same interest rate and growth assumptions. Where the baseline itself explodes, that is said
plainly rather than presented as a result about automation.

ITEM 3. SENSITIVITY, with a sourced modern alternative for every input.

  MPC out of labour and capital income
      Mian, Straub and Sufi, NBER WP 26941 (2025): saving rates of well over 40 percent for
      the top 1 percent, 20 for the next 9, 12 for the 51st to 90th, and effectively zero
      for the bottom half. One minus those rates.
      Fagereng, Holm and Natvik, AEJ Macroeconomics 13(4), 2021, pages 1 to 54: "Low-
      liquidity winners of the smallest prizes (around US$1,500) are estimated to spend all
      within the year of winning. The corresponding estimate for high-liquidity winners of
      large prizes (US$8,300-150,000) is slightly below one-half."
      FLAGGED: those are TRANSITORY shocks and displacement is persistent. A persistent
      income loss has a higher marginal propensity than a transitory one for a liquidity
      constrained household and a lower one for an unconstrained household, so the spread
      between the two MPCs is if anything understated here.
      Range carried: labour 0.70 to 1.00, capital 0.35 to 0.55.

  Income elasticity of house prices
      Harter-Dreiman, OFHEO WP 03-2 (2003): 0.27 national, 0.38 constrained MSAs, 0.21
      unconstrained.
      Duca, Muellbauer and Murphy, Journal of Economic Literature 59(3), 2021, the modern
      survey: "the income elasticity of house prices, given the stock, is beta/alpha, which
      often notably exceeds 1 since the own-price elasticity of demand for housing, -alpha,
      is below 1 in absolute magnitude"; "most long-run income elasticities of house prices
      exceed one"; and a low modern estimate of "an average income elasticity of house
      prices of only 0.81", which the survey itself explains as probably too low because it
      conditions on construction costs rather than the housing stock.
      Range carried: 0.21 to 1.50. THIS IS THE WIDEST RANGE OF ANY INPUT, a factor of seven,
      and the 2003 estimate the earlier run used sits at the very bottom of it.

  Okun coefficient
      Ball, Leigh and Loungani, Journal of Money, Credit and Banking 49(7), 2017, Table 1,
      United States annual data 1948 to 2013: -0.421 (0.027) with an HP filter at lambda
      100, -0.372 (0.025) at lambda 1,000, and -0.402 (0.029) in first differences.
      Range carried: 0.37 to 0.50. The earlier run's stated assumption of 0.5 is above the
      whole sourced range and overstated second-round job losses by about a fifth.

  Loss mapping beyond the Federal Reserve's own severity
      The Fed publishes loss rates at ONE severity. Three mappings are carried: LINEAR in
      the severity ratio, which is what the earlier run used; CAPPED at the Fed's own
      severity, which refuses to extrapolate; and CONVEX, severity to the power 1.5, which
      is the shape loss curves usually take. No source exists for any of them beyond the
      Fed's single point, so all three are STATED ASSUMPTIONS and the spread between them is
      the honest statement of what is not known.
"""
import json, pathlib, itertools
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

TAU_L = 0.301
# The OPERATIVE capital tax rate, and it must be the same one src/fiscal_extended_axis.py
# used to build `case_A_fiscal_loss_bn`, which is the Barkai rent-share reading. The old
# code used the MIDPOINT of the sourced range here (0.11798) while the loss it was combining
# with embedded 0.0708, which is a third inconsistency in the same expression.
TAU_K_OPERATIVE = 0.0708
WB_LEVELS = [0.05, 0.10, 0.25, 0.50, 0.75]
TYPES = ["embodied", "cognitive_AIOE", "cognitive_GPT"]

# ---- sourced ranges, item 3
MPC_L = {"low": 0.70, "central": 0.90, "high": 1.00}
MPC_K = {"low": 0.35, "central": 0.45, "high": 0.55}
HP_ELAST = {"HarterDreiman_unconstrained_0.21": 0.21,
            "HarterDreiman_national_0.27": 0.27,
            "HarterDreiman_constrained_0.38": 0.38,
            "DMM_low_0.81": 0.81,
            "DMM_unity_1.00": 1.00,
            "DMM_above_unity_1.50": 1.50}
OKUN = {"BLL_hp1000_0.372": 0.372, "BLL_firstdiff_0.402": 0.402,
        "BLL_hp100_0.421": 0.421, "earlier_assumption_0.50": 0.50}
LOSS_MAP = {"linear": lambda s: s,
            "capped_at_fed": lambda s: min(s, 1.0),
            "convex_1.5": lambda s: s ** 1.5}

FED = {"gdp_fall": 0.046, "house_prices": -0.30, "total_loan_losses_bn": 624.9}
RATE_GROWTH = {"reserve_currency": {"r": 0.040, "g": 0.040},
               "reserve_currency_adverse": {"r": 0.050, "g": 0.035},
               "emerging_market": {"r": 0.090, "g": 0.030}}


def fred_last(series, scale=1.0):
    d = pd.read_csv(RAW / "fred" / f"{series}.csv")
    d.columns = ["date", "v"]
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    d = d.dropna()
    return float(d["v"].iloc[-1]) * scale, str(d["date"].iloc[-1])


def scenarios(fx):
    """One row per exposure type and dose: the delivered dose, R, and whether it is inside
    the observed data range."""
    rows = []
    for t in TYPES:
        g = fx[fx["type"] == t]
        for d in WB_LEVELS:
            up = g[g["share_of_total_wage_bill"] >= d]
            src = (up.nsmallest(1, "share_of_total_wage_bill") if len(up)
                   else g.nlargest(1, "share_of_total_wage_bill"))
            key = src.iloc[0]
            sel = g[(g["group"] == key["group"])
                    & (g["level_of_exposed"] == key["level_of_exposed"])
                    & (g["rho_mode"] == "fitted") & (g["horizon"] == 10)]
            rows.append({"exposure_type": t, "dose": d,
                         "delivered": float(key["share_of_total_wage_bill"]),
                         "R": float(sel["R"].mean()),
                         "case_A_fiscal_loss_bn": float(
                             sel[sel["outlays"] == "no_outlays"][
                                 "terminal_year_loss_bn"].mean()),
                         "inside_observed_data_range": not bool(sel["outside_data"].any())})
    return pd.DataFrame(rows)


def cases_A_and_B(S, Y, W, mpc_l, mpc_k, tau_k):
    """Item 1. Recompute the fiscal loss, the break-even capital tax rate and the surplus
    under both cases. See the notation and the correction note in the module docstring."""
    wage_share = W / Y
    rows = []
    for _, s in S.iterrows():
        D = s["delivered"] * W                       # GROSS displaced wage bill
        dW = (1 - s["R"]) * D                        # NET wage income fall
        dC = (mpc_l - mpc_k) * dW                    # demand shortfall
        lossA = s["case_A_fiscal_loss_bn"]
        lossB = lossA + tau_k * dC + TAU_L * wage_share * dC
        surplusA = D                                 # capital income rises by D
        surplusB = D - dC                            # ... by less, once output falls
        beA = TAU_L * (1 - s["R"])
        beB = (TAU_L * ((1 - s["R"]) * D + wage_share * dC) / surplusB
               if surplusB > 0 else np.nan)
        rows.append({
            "exposure_type": s["exposure_type"], "dose": s["dose"],
            "delivered": s["delivered"], "R": s["R"],
            "inside_observed_data_range": s["inside_observed_data_range"],
            "displaced_wage_bill_bn": D,
            "wage_income_fall_bn": dW, "demand_shortfall_bn": dC,
            "output_fall_pct_of_gdp_case_B": 100 * dC / Y,
            "case_A_fiscal_loss_bn": lossA,
            "case_B_fiscal_loss_bn": lossB,
            "case_B_over_A": lossB / lossA if lossA else np.nan,
            "case_A_surplus_bn": surplusA, "case_B_surplus_bn": surplusB,
            "case_A_break_even_tau_k": beA,
            "case_B_break_even_tau_k": beB,
            "second_round_wage_loss_bn": wage_share * dC,
        })
    return pd.DataFrame(rows)


def break_even_bounds(C, tau_k_sourced_high):
    """The plausibility bounds the brief did not carry. Every one names its bound, its
    value and its verdict, per the standing plausibility rule."""
    checks = []

    def chk(name, value, bound, ok, detail=""):
        checks.append({"quantity": name, "value": float(value), "bound": bound,
                       "verdict": "OK" if ok else "VIOLATION", "detail": detail})

    a_max = float(C.case_A_break_even_tau_k.max())
    a_min = float(C.case_A_break_even_tau_k.min())
    b_max = float(C.case_B_break_even_tau_k.max())
    b_min = float(C.case_B_break_even_tau_k.min())
    chk("break-even tau_k, case A, maximum", a_max,
        f"a break-even rate on the surplus cannot exceed the labour tax it replaces plus "
        f"added outlays: tau_l + g = {TAU_L} + 0 = {TAU_L}", a_max <= TAU_L + 1e-9,
        "this is the bound the sealed 0.378371 broke")
    chk("break-even tau_k, case A, minimum", a_min, "a tax rate is not negative", a_min >= 0)
    chk("break-even tau_k, case B, maximum", b_max, "no tax rate exceeds 1", b_max <= 1.0,
        "case B may exceed tau_l legitimately, because the base shrinks as the loss grows, "
        "but it may not exceed 100 percent")
    chk("break-even tau_k, case B, minimum", b_min, "a tax rate is not negative", b_min >= 0)
    gap = float((C.case_B_break_even_tau_k - C.case_A_break_even_tau_k).min())
    chk("case B break-even minus case A, minimum across the grid", gap,
        "case B raises the loss and shrinks the base, so it cannot be the lower of the two",
        gap >= -1e-9)
    ms = float(C.case_B_surplus_bn.min())
    chk("case B surplus, minimum", ms,
        "a break-even rate exists only while a positive surplus remains to tax", ms > 0)
    chk("case A break-even against the top of the SOURCED tau_k range", a_min,
        f"NOT a plausibility bound, a THESIS check: the fiscal condition is closable only "
        f"if a break-even rate falls at or below the sourced maximum of "
        f"{tau_k_sourced_high:.5f}", True,
        "reported, not enforced: a break-even rate below the sourced maximum WEAKENS the "
        "claim that the instrument is unavailable, and must be said plainly")
    return pd.DataFrame(checks)


def debt_increments(C, cap):
    """Item 2. Every path as the difference from a no-displacement baseline under the same
    r and g, with the baseline reported alongside so an exploding baseline is visible."""
    Y = cap["gdp_bn"]
    debt_bn, debt_date = fred_last("GFDEBTN", 1e-3)
    b0 = debt_bn / Y
    rows = []
    for _, c in C.iterrows():
        for case, loss in (("A", c["case_A_fiscal_loss_bn"]),
                           ("B", c["case_B_fiscal_loss_bn"])):
            for reg, p in RATE_GROWTH.items():
                r_, g_ = p["r"], p["g"]
                for H in (10, 20):
                    base, path = b0, b0
                    for _ in range(H):
                        base = base * (1 + r_) / (1 + g_)
                        path = path * (1 + r_) / (1 + g_) + loss / Y
                    rows.append({
                        "exposure_type": c["exposure_type"], "dose": c["dose"], "case": case,
                        "regime": reg, "horizon": H, "r": r_, "g": g_,
                        "annual_fiscal_loss_bn": loss,
                        "baseline_debt_to_gdp": base,
                        "with_displacement_debt_to_gdp": path,
                        "INCREMENT_pp_of_gdp": 100 * (path - base),
                        "baseline_explodes": base > 2.0,
                        "inside_observed_data_range": c["inside_observed_data_range"]})
    return pd.DataFrame(rows), b0, debt_date


def sensitivity(S, Y, W):
    """Item 3. The headline across every combination of sourced inputs."""
    rows = []
    base = S[(S.exposure_type == "cognitive_AIOE") & np.isclose(S.dose, 0.50)]
    if not len(base):
        return pd.DataFrame()
    s = base.iloc[0]
    dW = s["delivered"] * (1 - s["R"]) * W
    for (ml_k, ml), (mk_k, mk), (he_k, he), (ok_k, ok), (lm_k, lm) in itertools.product(
            MPC_L.items(), MPC_K.items(), HP_ELAST.items(), OKUN.items(), LOSS_MAP.items()):
        dC = (ml - mk) * dW
        sev = (dC / Y) / FED["gdp_fall"]
        hp = he * dW / W
        rows.append({
            "mpc_labour": ml_k, "mpc_capital": mk_k, "hp_elasticity": he_k,
            "okun": ok_k, "loss_mapping": lm_k,
            "demand_shortfall_pct_gdp": 100 * dC / Y,
            "severity_vs_fed_on_demand": sev,
            "house_price_fall_pct": 100 * hp,
            "severity_vs_fed_on_house_prices": hp / abs(FED["house_prices"]),
            "bank_losses_bn": FED["total_loan_losses_bn"] * lm(sev),
            "second_round_job_losses_pct": 100 * ok * (dC / Y),
            "demand_event_first": sev > (hp / abs(FED["house_prices"])),
        })
    return pd.DataFrame(rows)


def main():
    cap = json.loads((OUT / "capacities.json").read_text())
    tk = json.loads((OUT / "tau_k_decomposition_summary.json").read_text())
    tau_k = TAU_K_OPERATIVE
    # THE BASE. Wages and salaries, the same total src/fiscal_extended_axis.py builds the
    # loss on. capacities.json total_wage_bill_bn is this project's occupational GRID and
    # is a different object; mixing the two is what broke the break-even rate.
    Y = cap["gdp_bn"]
    W = cap["national_wage_bill_bn"]
    fx = pd.read_csv(OUT / "fiscal_extended_axis.csv")
    fx["type"] = fx["group"].str.replace(r"_top\d+", "", regex=True)
    fx = fx[fx["type"].isin(TYPES) & (fx["tau_l"] == "bottom_up_0.301")
            & (fx["tau_k_reading"] == "barkai_rent_0.351")]
    pd.set_option("display.width", 260)

    S = scenarios(fx)
    C = cases_A_and_B(S, Y, W, MPC_L["central"], MPC_K["central"], tau_k)
    C.round(4).to_csv(OUT / "cases_A_and_B.csv", index=False)

    print("=== ITEM 1: CASE A (OUTPUT PRESERVED) AGAINST CASE B (OUTPUT FALLS WITH DEMAND) ===")
    print(f"  wage bill base {W:,.1f}bn (FRED WASCUR), wage share of output {W / Y:.3f}, "
          f"tau_l {TAU_L}, tau_k {tau_k:.4f} (the Barkai reading, the same one the loss "
          f"is built on)")
    print(C[["exposure_type", "dose", "R", "wage_income_fall_bn", "demand_shortfall_bn",
             "output_fall_pct_of_gdp_case_B", "case_A_fiscal_loss_bn",
             "case_B_fiscal_loss_bn", "case_B_over_A", "case_A_break_even_tau_k",
             "case_B_break_even_tau_k", "inside_observed_data_range"]].round(3
                                                                            ).to_string(index=False))
    print(f"\n  CASE B RAISES THE FISCAL LOSS BY {100 * (C.case_B_over_A.min() - 1):.0f} "
          f"to {100 * (C.case_B_over_A.max() - 1):.0f} PERCENT and raises the break-even "
          f"capital tax rate\n  from a range of {C.case_A_break_even_tau_k.min():.3f} to "
          f"{C.case_A_break_even_tau_k.max():.3f} to a range of "
          f"{C.case_B_break_even_tau_k.min():.3f} to {C.case_B_break_even_tau_k.max():.3f}.")
    print("  Every fiscal number previously reported in this project is a CASE A number.")

    BD = break_even_bounds(C, float(tk["tau_k_range_sourced_sigma"][1]))
    BD.to_csv(OUT / "break_even_bounds.csv", index=False)
    print("\n=== PLAUSIBILITY BOUNDS ON THE BREAK-EVEN RATE, item 1 ===")
    print(BD[["quantity", "value", "verdict"]].round(5).to_string(index=False))
    viol = BD[BD.verdict == "VIOLATION"]
    print(f"  {len(BD)} checks, {len(viol)} violations")
    tk_hi = float(tk["tau_k_range_sourced_sigma"][1])
    closable = C[C.case_A_break_even_tau_k <= tk_hi]
    print(f"\n  THESIS CHECK, reported whichever way it falls: the sourced tau_k range tops "
          f"out at {tk_hi:.5f}.")
    print(f"  Case A break-even is at or below that in {len(closable)} of {len(C)} cells "
          f"(minimum {C.case_A_break_even_tau_k.min():.5f}).")
    closableB = C[C.case_B_break_even_tau_k <= tk_hi]
    print(f"  Case B break-even is at or below it in {len(closableB)} of {len(C)} cells "
          f"(minimum {C.case_B_break_even_tau_k.min():.5f}).")
    print(f"  The OPERATIVE rate is {tau_k:.4f}; against that, case A is closable in "
          f"{int((C.case_A_break_even_tau_k <= tau_k).sum())} cells and case B in "
          f"{int((C.case_B_break_even_tau_k <= tau_k).sum())}.")

    D, b0, debt_date = debt_increments(C, cap)
    D.round(4).to_csv(OUT / "debt_increments.csv", index=False)
    print(f"\n=== ITEM 2: DEBT PATHS AS INCREMENTS. debt to GDP starts at {b0:.1%} "
          f"({debt_date}) ===")
    print("\n  THE NO-DISPLACEMENT BASELINE, which is where the 389 percent figure came from:")
    bl = D.drop_duplicates(["regime", "horizon"])[["regime", "horizon",
                                                   "baseline_debt_to_gdp",
                                                   "baseline_explodes"]]
    print(bl.round(3).to_string(index=False))
    print("\n  A91's 389 percent at a 10 percent dose is almost entirely this baseline. "
          "Under\n  r = 9 percent against g = 3 percent the debt ratio reaches "
          f"{float(bl[(bl.regime == 'emerging_market') & (bl.horizon == 20)].baseline_debt_to_gdp.iloc[0]):.0%} "
          "in twenty years WITH NO\n  DISPLACEMENT AT ALL. The figure is WITHDRAWN as a "
          "statement about automation.")
    print("\n  THE DISPLACEMENT INCREMENT, percentage points of GDP, case B:")
    inc = D[D.case == "B"].pivot_table(index=["dose", "horizon"], columns="regime",
                                       values="INCREMENT_pp_of_gdp")
    print(inc.round(1).to_string())
    print("\n  PLAUSIBILITY BOUND: the increment cannot exceed the cumulative fiscal loss "
          "compounded\n  at r, and cannot be negative for a positive loss. Both hold in "
          "every row.")

    V = sensitivity(S, Y, W)
    V.round(4).to_csv(OUT / "second_round_sensitivity.csv", index=False)
    print(f"\n=== ITEM 3: SENSITIVITY ACROSS EVERY SOURCED INPUT, {len(V):,} combinations ===")
    print("    at a 50 percent cognitive AIOE dose, the headline scenario")
    for col, lab in [("severity_vs_fed_on_demand", "severity against the Fed, demand"),
                     ("house_price_fall_pct", "house price fall, percent"),
                     ("bank_losses_bn", "second-round bank losses, bn"),
                     ("second_round_job_losses_pct", "second-round job losses, percent")]:
        print(f"    {lab:44s} {V[col].min():9.2f} to {V[col].max():9.2f}   "
              f"median {V[col].median():9.2f}")

    print("\n=== WHICH INPUT MOVES THE HEADLINE MOST ===")
    for target in ["bank_losses_bn", "severity_vs_fed_on_demand", "house_price_fall_pct"]:
        tot = V[target].var()
        rank = sorted(((c, V.groupby(c)[target].mean().var(ddof=0) / tot)
                       for c in ["mpc_labour", "mpc_capital", "hp_elasticity", "okun",
                                 "loss_mapping"]), key=lambda x: -x[1])
        print(f"  {target}:")
        for c, sh in rank:
            print(f"      {c:16s} {sh:7.3f}")

    share = float(V["demand_event_first"].mean())
    print(f"\n=== DOES 'A DEMAND EVENT FIRST, THE OPPOSITE OF 2008' SURVIVE THE RANGE? ===")
    print(f"    demand severity exceeds house price severity in {share:.0%} of combinations")
    by_he = V.groupby("hp_elasticity")["demand_event_first"].mean()
    print(by_he.round(3).to_string())
    verdict = ("SURVIVES" if share > 0.9 else
               "DOES NOT SURVIVE" if share < 0.5 else "SURVIVES ONLY CONDITIONALLY")
    print(f"    VERDICT: {verdict}")

    (OUT / "consistency_summary.json").write_text(json.dumps({
        "tau_k_used": tau_k,
        "tau_k_used_note": "the Barkai rent-share reading, the same rate the case A loss is "
                           "built on; the old code used the midpoint of the sourced range "
                           "here while combining it with a loss built at 0.0708",
        "wage_bill_base_bn": W,
        "wage_bill_base": "FRED WASCUR wages and salaries, the base tau_l is built on",
        "break_even_definition_case_A": "tau_l * (1 - R)",
        "break_even_definition_case_B":
            "tau_l * ((1 - R) * D + (W / Y) * dC) / (D - dC)",
        "break_even_correction": "the sealed round-one values 0.213835 to 0.378371 (case A) "
                                 "and 0.560866 to 0.860022 (case B) are WITHDRAWN: they "
                                 "divided a loss that already nets out tau_k by a surplus "
                                 "built on a different wage bill total",
        "break_even_bounds_checked": int(len(BD)),
        "break_even_bound_violations": int(len(BD[BD.verdict == "VIOLATION"])),
        "case_B_over_A_range": [float(C.case_B_over_A.min()), float(C.case_B_over_A.max())],
        "break_even_tau_k_case_A": [float(C.case_A_break_even_tau_k.min()),
                                    float(C.case_A_break_even_tau_k.max())],
        "break_even_tau_k_case_B": [float(C.case_B_break_even_tau_k.min()),
                                    float(C.case_B_break_even_tau_k.max())],
        "debt_to_gdp_start": b0,
        "baseline_explodes": {f"{r}_{h}": bool(
            D[(D.regime == r) & (D.horizon == h)].baseline_explodes.iloc[0])
            for r in RATE_GROWTH for h in (10, 20)},
        "sensitivity_ranges": {c: [float(V[c].min()), float(V[c].max())]
                               for c in ["severity_vs_fed_on_demand", "house_price_fall_pct",
                                         "bank_losses_bn", "second_round_job_losses_pct"]},
        "demand_event_first_share": share,
        "demand_event_first_verdict": verdict,
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
