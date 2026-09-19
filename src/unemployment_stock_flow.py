"""Item 2: a minimal stock-flow model of unemployment under SUSTAINED displacement.

A54 solved a static fixed point: displace d percent of employment once, see where
unemployment lands. That is the wrong object for an adoption path. Displacement arrives as a
FLOW over years, and what matters is whether the reemployment machinery clears that flow.
This module replaces the static calculation with the smallest dynamic model that can answer
the question, and it is deliberately minimal so that every moving part is visible.

STOCKS AND FLOWS, annual steps

    D_t      = d * E_t                       displaced this year, d is the annual flow rate
    U_{t+1}  = U_t + D_t + s_other * E_t - (h_t + a_t) * U_t
    E_{t+1}  = E_t - D_t - s_other * E_t + h_t * U_t
    N_{t+1}  = N_t + a_t * U_t
    u_t      = U_t / (U_t + E_t)

    h_t  annual reemployment hazard out of unemployment
    a_t  annual hazard of leaving the labour force
    s_other  every other route into unemployment (quits, short-tenure layoffs, entrants),
             calibrated once so the model reproduces the observed 4.32 percent unemployment
             at the observed baseline displacement rate. It is a reduced-form residual and
             is labelled as such; it is NOT a measured separation rate.

CONVERTING THE DWS THREE-YEAR WINDOW TO AN ANNUAL HAZARD, stated exactly

The DWS reports, for workers displaced over a THREE-YEAR window, their status at a single
survey date. Taking displacement as uniform over that window, mean elapsed time to the
survey is T = 1.5 years. Splitting the survey shares into the two competing risks:

    employed share            rho(u)
    exited the labour force   (1 - rho(u)) * e(u)
    still unemployed          (1 - rho(u)) * (1 - e(u))

with rho(u) and e(u) the fitted relationships from A49 and A54. Treating each as a constant
annual hazard operating over T years:

    h(u) = 1 - (1 - rho_cond(u)) ** (1/T),  rho_cond = rho / (rho + (1-rho)(1-e))
    a(u) = 1 - (1 - (1-rho(u)) * e(u)) ** (1/T)

rho_cond is reemployment CONDITIONAL on still participating, which is the right base for a
hazard out of unemployment. T is varied over 1.0, 1.5 and 2.0 years as the sensitivity the
brief asks for, and the conversion is the single largest modelling choice in this file.

TWO EXIT VARIANTS, DIFFERENT HORIZONS, BOTH REPORTED

    short_run  e(u) from the DWS, 0.296 to 0.643, falling with slack. This is the response
               WITHIN THREE YEARS of displacement.
    long_run   e = 0.75 fixed, from Acemoglu and Restrepo (2020), Section V.C, PDF page 34,
               table A15: of the additional nonemployed, about three quarters leave the
               labour force. Estimated on fourteen-year differences, so it describes where
               displaced workers SETTLE over a decade or more.

These are not interchangeable and neither is "the" exit rate. A higher exit share LOWERS
measured unemployment, so the long-run variant is the optimistic one for the unemployment
path and the pessimistic one for the participation rate and the tax base.

WHAT IS LEFT OUT, and the direction of each omission

  - No re-entry from outside the labour force. This UNDERSTATES unemployment.
  - No population or labour force growth. Small over 10 to 20 years relative to the shocks.
  - No wage or vacancy response, no matching function. The hazards are reduced form and
    depend on u only through the fitted DWS relationships.
  - rho(u) is fitted on unemployment from 3.6 to 9.8 percent. Any path leaving that range is
    flagged outside_data on every row and is not an estimate.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

T_CASES = {"T_1.0y": 1.0, "T_1.5y_central": 1.5, "T_2.0y": 2.0}
AR_LONG_RUN_EXIT = 0.75          # Acemoglu and Restrepo (2020), Section V.C, table A15
D_GRID = [0.005, 0.0075, 0.01, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05]
HORIZONS = [10, 20]
NAMED = {"10pct_over_10y": (0.10, 10), "10pct_over_20y": (0.10, 20),
         "25pct_over_10y": (0.25, 10), "25pct_over_20y": (0.25, 20),
         "50pct_over_10y": (0.50, 10), "50pct_over_20y": (0.50, 20),
         "75pct_over_10y": (0.75, 10), "75pct_over_20y": (0.75, 20),
         "90pct_over_10y": (0.90, 10), "90pct_over_20y": (0.90, 20)}


def load_fits():
    R = json.loads((OUT / "bls_dws_vintages.json").read_text())["fit_rho_on_unrate"]
    S = json.loads((OUT / "displacement_to_slack.json").read_text())
    return R, S


def hazards(u_pct, R, S, T, exit_mode):
    rho = float(np.clip(R["intercept"] + R["slope_per_pp_unrate"] * u_pct, 1e-6, 0.999))
    if exit_mode == "long_run":
        e = AR_LONG_RUN_EXIT
    else:
        f = S["exit_share_fit"]
        lo, hi = f["observed_range"]
        e = float(np.clip(f["intercept"] + f["slope_per_pp_unrate"] * u_pct, lo, hi))
    still_lf = rho + (1 - rho) * (1 - e)
    rho_cond = rho / still_lf if still_lf > 0 else 0.0
    h = 1 - (1 - min(rho_cond, 0.999)) ** (1.0 / T)
    a = 1 - (1 - min((1 - rho) * e, 0.999)) ** (1.0 / T)
    return h, a, rho, e


def calibrate_s_other(R, S, T, exit_mode, d0, u0):
    """Residual inflow rate that reproduces u0 at the observed baseline displacement d0."""
    h, a, _, _ = hazards(u0 * 100, R, S, T, exit_mode)
    total_in = (u0 / (1 - u0)) * (h + a)
    return max(total_in - d0, 0.0)


def simulate(d, years, R, S, T, exit_mode, s_other, E0, U0, N0):
    E, U, N = E0, U0, N0
    path = []
    for t in range(years):
        u = U / (U + E) if (U + E) > 0 else 1.0
        h, a, rho, e = hazards(u * 100, R, S, T, exit_mode)
        D = d * E
        Oth = s_other * E
        newU = U + D + Oth - (h + a) * U
        newE = E - D - Oth + h * U
        newN = N + a * U
        E, U, N = max(newE, 0.0), max(newU, 0.0), newN
        path.append({"t": t + 1, "u": U / (U + E) if (U + E) > 0 else 1.0,
                     "rho": rho, "h": h, "a": a, "E": E, "U": U, "N": N})
    return pd.DataFrame(path)


def steady_state(d, R, S, T, exit_mode, s_other, u_guess=0.05):
    u = u_guess
    for _ in range(500):
        h, a, _, _ = hazards(u * 100, R, S, T, exit_mode)
        if h + a <= 1e-9:
            return np.nan, False
        nu = (d + s_other) / (d + s_other + h + a)
        if abs(nu - u) < 1e-12:
            return nu, True
        u = 0.5 * u + 0.5 * nu
    return u, True


def main():
    R, S = load_fits()
    base = S["baseline_jan2026"]
    E0, U0, LF0 = base["employed"], base["unemployed"], base["labour_force"]
    u0 = base["unrate"] / 100.0
    N0 = 0.0
    U_MAX_OBS = S["rho_valid_to_unrate"]
    # observed baseline displacement flow: DWS long-tenured, 3.324m over 3 years
    d0 = (3324.0 / 3.0) / E0

    rows = []
    for tn, T in T_CASES.items():
        for em in ("short_run", "long_run"):
            s_other = calibrate_s_other(R, S, T, em, d0, u0)
            for d in D_GRID:
                ss, ok = steady_state(d, R, S, T, em, s_other)
                rec = {"T_case": tn, "T": T, "exit_mode": em, "s_other": s_other,
                       "d_annual": d, "steady_state_u": ss}
                for H in HORIZONS:
                    p = simulate(d, H, R, S, T, em, s_other, E0, U0, N0)
                    rec[f"u_at_{H}y"] = float(p["u"].iloc[-1])
                    rec[f"rho_at_{H}y"] = float(p["rho"].iloc[-1])
                rec["outside_data_ss"] = bool(np.isnan(ss) or ss * 100 > U_MAX_OBS)
                rows.append(rec)
    G = pd.DataFrame(rows)
    G.round(6).to_csv(OUT / "unemployment_stock_flow.csv", index=False)

    # limits
    lim = []
    for tn, T in T_CASES.items():
        for em in ("short_run", "long_run"):
            s_other = calibrate_s_other(R, S, T, em, d0, u0)
            dd = np.arange(0.0005, 0.1201, 0.0005)
            d_within = np.nan
            d_bounded = np.nan
            for d in dd:
                ss, ok = steady_state(d, R, S, T, em, s_other)
                if ok and not np.isnan(ss) and ss * 100 <= U_MAX_OBS:
                    d_within = d
                h, a, _, _ = hazards(min(ss * 100 if ok and not np.isnan(ss) else 99, 99),
                                     R, S, T, em)
                if ok and not np.isnan(ss) and (h + a) > 1e-6 and ss < 0.999:
                    d_bounded = d
            lim.append({"T_case": tn, "exit_mode": em, "s_other": s_other,
                        "max_d_within_observed_u": d_within,
                        "max_d_bounded": d_bounded})
    L = pd.DataFrame(lim)
    L.round(6).to_csv(OUT / "unemployment_speed_limits.csv", index=False)

    # named scenarios as annual flows
    T, em = 1.5, "short_run"
    s_other = calibrate_s_other(R, S, T, em, d0, u0)
    lw = L[(L.T_case == "T_1.5y_central") & (L.exit_mode == em)].iloc[0]
    nm = []
    for name, (tot, yrs) in NAMED.items():
        d = tot / yrs
        ss, ok = steady_state(d, R, S, T, em, s_other)
        p = simulate(d, yrs, R, S, T, em, s_other, E0, U0, N0)
        nm.append({"scenario": name, "total_displacement": tot, "years": yrs,
                   "d_annual": d, "u_terminal": float(p["u"].iloc[-1]),
                   "rho_terminal": float(p["rho"].iloc[-1]),
                   "steady_state_u": ss,
                   "within_observed_range": bool(d <= lw["max_d_within_observed_u"]),
                   "bounded": bool(d <= lw["max_d_bounded"])})
    NMD = pd.DataFrame(nm)
    NMD.round(5).to_csv(OUT / "unemployment_named_scenarios.csv", index=False)

    (OUT / "unemployment_stock_flow_summary.json").write_text(json.dumps({
        "baseline": base, "d0_observed_annual": d0,
        "hazard_conversion": "h = 1 - (1 - rho_cond)**(1/T), rho_cond = rho/(rho+(1-rho)(1-e))",
        "T_cases": T_CASES, "long_run_exit_source": AR_LONG_RUN_EXIT,
        "limits": L.round(6).to_dict("records"),
        "rho_valid_to_unrate": U_MAX_OBS}, indent=2))

    pd.set_option("display.width", 240)
    print(f"=== baseline: employed {E0/1000:.1f}m, unemployed {U0/1000:.1f}m, "
          f"u = {u0*100:.2f}% ===")
    print(f"  observed DWS long-tenured displacement flow d0 = {d0*100:.3f}% a year")
    print(f"  hazards at u0, T = 1.5, short-run exit: "
          f"h = {hazards(u0*100,R,S,1.5,'short_run')[0]:.4f}, "
          f"a = {hazards(u0*100,R,S,1.5,'short_run')[1]:.4f}")
    print(f"  residual inflow s_other calibrated to {calibrate_s_other(R,S,1.5,'short_run',d0,u0)*100:.3f}% a year")

    print("\n=== STEADY-STATE UNEMPLOYMENT by annual displacement flow ===")
    piv = G[G.T_case == "T_1.5y_central"].pivot_table(
        index="d_annual", columns="exit_mode", values="steady_state_u") * 100
    piv.columns = [f"ss_u_{c}" for c in piv.columns]
    p10 = G[G.T_case == "T_1.5y_central"].pivot_table(
        index="d_annual", columns="exit_mode", values="u_at_10y") * 100
    p20 = G[G.T_case == "T_1.5y_central"].pivot_table(
        index="d_annual", columns="exit_mode", values="u_at_20y") * 100
    out = piv.join(p10.add_prefix("u10y_")).join(p20.add_prefix("u20y_"))
    print(out.round(2).to_string())

    print("\n=== SPEED LIMITS ===")
    print(L.assign(max_d_within_observed_u=lambda x: x.max_d_within_observed_u * 100,
                   max_d_bounded=lambda x: x.max_d_bounded * 100,
                   s_other=lambda x: x.s_other * 100).round(3).to_string(index=False))
    print("  columns in percent of employment per year")

    print("\n=== NAMED ADOPTION SCENARIOS (T = 1.5y, short-run exit) ===")
    print(NMD.assign(d_annual=lambda x: x.d_annual * 100,
                     u_terminal=lambda x: x.u_terminal * 100,
                     steady_state_u=lambda x: x.steady_state_u * 100
                     ).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
