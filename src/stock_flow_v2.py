"""Item 1 rebuild: stock-flow model driven by a slack measure that COUNTS exits, with the
outcome measures in the right order.

WHAT CHANGED FROM A56 AND A61

1. THE HAZARD IS NO LONGER DRIVEN BY THE UNEMPLOYMENT RATE. It is driven by PRIME-AGE
   NONEMPLOYMENT, 100 minus the 25-to-54 employment rate, re-estimated on the same fourteen
   DWS vintages in src/slack_reestimate.py:

       rho = 1.2280 - 0.0275 * prime_age_nonemployment    R-squared 0.773, t = -6.40

   against the original rho = 0.8090 - 0.0304 * unemployment_rate, R-squared 0.812.

   Two candidates that count exits were tried. The 16-and-over nonemployment rate fits at
   R-squared 0.540 and is REJECTED for a second reason as well: it falls secularly as the
   population ages, so it conflates demographics with slack, and its observed range at the
   vintage dates is only about one point wide, which makes any speed limit computed against
   it degenerate. Prime-age nonemployment strips the demographic trend, has a 6.4 point
   observed range (18.27 to 24.71), and fits nearly as well as the original.

   The model is therefore run on PRIME-AGE aggregates throughout, which is also the better
   match to the population being modelled: DWS displaced workers are long-tenured, three or
   more years on the lost job, and are overwhelmingly prime-age.

2. THE EXIT SHARE IS NOW A CONSTANT WITH A RANGE, NOT A FUNCTION OF SLACK.
   A54 fitted exit share on the unemployment rate at R-squared 0.777. Re-fitted on
   nonemployment it is R-squared 0.137, t = -1.13, NOT SIGNIFICANT. The original fit was
   partly mechanical: exit share is NILF/(U+NILF) and the unemployment rate is U/(U+E), so
   both move with U by construction. The slack dependence of the exit share does not survive
   a measure that does not share a component with it. Exit share is therefore held at the
   2026 value of 0.462 with the observed range 0.296 to 0.643 as sensitivity, and claim 57
   is downgraded.

3. OUTCOMES ARE REPORTED IN THIS ORDER, with unemployment LAST:
       employment to population ratio
       cumulative share of displaced workers never reemployed
       aggregate wage income relative to baseline
       unemployment

4. WAGE INCOME TRACKS COMPOSITION. Workers carry "wage units": one for a never-displaced
   worker, omega for a worker reemployed once, omega squared for twice, and so on. The model
   tracks the stock of wage units among the employed and the unemployed separately, so
   aggregate wage income falls both because fewer people work and because those who return
   return at a discount.

5. CONSISTENCY CHECK. At every step the model's REALISED reemployment share among the
   cumulative displaced is compared with the rho implied by the model's own slack. If the
   realised share materially exceeds the implied rho, the circularity is still operating and
   the run is flagged.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"

T_CASES = {"T_1.0y": 1.0, "T_1.5y_central": 1.5, "T_2.0y": 2.0}
EXIT_CASES = {"low_0.296": 0.296, "central_2026_0.462": 0.462, "high_0.643": 0.643}
OMEGA_CASES = {"stayer_0.79": 0.79, "dws_blend_0.86": 0.8598, "switcher_0.58": 0.58}
D_GRID = [0.005, 0.0075, 0.01, 0.0125, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05]
HORIZONS = [2, 5, 10, 20]
PHIS = [0.0, 0.5, 1.0]


def fred(series):
    p = RAW / "fred" / f"{series}.csv"
    if not p.exists():
        import requests
        r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}",
                         timeout=90)
        r.raise_for_status()
        p.write_bytes(r.content)
    d = pd.read_csv(p)
    d.columns = ["date", "value"]
    d["date"] = pd.to_datetime(d["date"])
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    return d.dropna().set_index("date")["value"]


def load():
    S = json.loads((OUT / "slack_reestimate.json").read_text())
    f = S["fits"]["rho_on_PRIME_AGE_nonemployment"]
    return f, S


def hazards(nonemp_pct, f, T, exit_share):
    rho = float(np.clip(f["intercept"] + f["slope"] * nonemp_pct, 1e-6, 0.999))
    still = rho + (1 - rho) * (1 - exit_share)
    rc = rho / still if still > 0 else 0.0
    h = 1 - (1 - min(rc, 0.999)) ** (1.0 / T)
    a = 1 - (1 - min((1 - rho) * exit_share, 0.999)) ** (1.0 / T)
    return h, a, rho


def simulate(d, years, phi, f, T, exit_share, omega, s_other, E0, U0, POP0):
    E, U = E0, U0
    WE, WU = E0 * 1.0, U0 * 1.0      # wage units
    Dcum = 0.0
    disp_total, reemp_total = 0.0, 0.0
    path = []
    for t in range(years):
        nonemp = 100.0 * (POP0 - E) / POP0
        h, a, rho_imp = hazards(nonemp, f, T, exit_share)
        h_eff = h * max(0.0, 1.0 - phi * Dcum)
        Dis = d * E
        Oth = s_other * E
        w_per_E = WE / E if E > 0 else 0.0
        w_per_U = WU / U if U > 0 else 0.0
        out_units = (Dis + Oth) * w_per_E
        back = h_eff * U
        back_units = back * w_per_U * omega
        U2 = U + Dis + Oth - (h_eff + a) * U
        E2 = E - Dis - Oth + back
        WU2 = WU + out_units - (h_eff + a) * U * w_per_U
        WE2 = WE - out_units + back_units
        Dcum += Dis / E0
        disp_total += Dis + Oth   # ALL inflows to unemployment, not only AI displacement,
        # because reemployment below drains the whole stock and comparing it with AI
        # displacement alone produced shares above 1
        reemp_total += back
        E, U = max(E2, 0.0), max(U2, 0.0)
        WE, WU = max(WE2, 0.0), max(WU2, 0.0)
        N = max(POP0 - E - U, 0.0)
        path.append({
            "t": t + 1,
            "ep_ratio": 100.0 * E / POP0,
            "never_reemployed_share": 1.0 - (reemp_total / disp_total) if disp_total > 0 else 0.0,
            "wage_income_rel_baseline": WE / E0,
            "unemployment": U / (U + E) if (U + E) > 0 else 1.0,
            "nonemployment_rate": 100.0 * (POP0 - E) / POP0,
            "rho_implied": rho_imp,
            "realised_reemp_share": reemp_total / disp_total if disp_total > 0 else np.nan,
            "D_cum": Dcum, "h_eff": h_eff, "N": N})
    return pd.DataFrame(path)


def main():
    f, S = load()
    # PRIME-AGE (25 to 54) aggregates, normalised so that population = 1.
    emp_rate = float(fred("LREM25TTUSM156S").asof(pd.Timestamp("2026-01-01")))  # percent
    part_rate = float(fred("LNS11300060").asof(pd.Timestamp("2026-01-01")))     # percent
    pop = 1.0
    E0 = emp_rate / 100.0
    U0 = max(part_rate - emp_rate, 0.0) / 100.0
    ep0 = 100.0 * E0 / pop
    nonemp0 = 100.0 - ep0
    # observed baseline displacement flow, DWS long-tenured, as a share of employment
    d0 = 0.00679

    T, ex = 1.5, EXIT_CASES["central_2026_0.462"]
    h0, a0, rho0 = hazards(nonemp0, f, T, ex)
    u0 = U0 / (U0 + E0)
    s_other = max((u0 / (1 - u0)) * (h0 + a0) - d0, 0.0)

    print("=== baseline January 2026, PRIME AGE 25 to 54, population normalised to 1 ===")
    print(f"  employment rate {emp_rate:.2f}%, participation {part_rate:.2f}%")
    print(f"  prime-age nonemployment {nonemp0:.2f}%, prime-age unemployment "
          f"{u0*100:.2f}%")
    print(f"  rho implied by the PRIME-AGE fit at baseline: {rho0:.4f} "
          f"(observed 2026 rho = 0.6616)")
    print(f"  hazards h = {h0:.4f}, a = {a0:.4f}; residual inflow "
          f"s_other = {s_other*100:.3f}% a year")

    rows = []
    for phi in PHIS:
        for d in D_GRID:
            for H in HORIZONS:
                p = simulate(d, H, phi, f, T, ex, OMEGA_CASES["dws_blend_0.86"],
                             s_other, E0, U0, pop)
                last = p.iloc[-1]
                rows.append({"phi": phi, "d_annual": d, "horizon": H,
                             "ep_ratio": last.ep_ratio,
                             "ep_drop_pp": ep0 - last.ep_ratio,
                             "never_reemployed_share": last.never_reemployed_share,
                             "wage_income_rel_baseline": last.wage_income_rel_baseline,
                             "unemployment": last.unemployment,
                             "nonemployment_rate": last.nonemployment_rate,
                             "rho_implied": last.rho_implied,
                             "realised_reemp_share": last.realised_reemp_share,
                             "circularity_gap": last.realised_reemp_share - last.rho_implied,
                             "D_cum": last.D_cum,
                             "outside_data": last.nonemployment_rate > 24.71})
    G = pd.DataFrame(rows)
    G.round(6).to_csv(OUT / "stock_flow_v2_grid.csv", index=False)

    pd.set_option("display.width", 250)
    print("\n=== OUTCOMES at phi = 0.5, 10-year horizon (unemployment LAST) ===")
    s = G[(G.phi == 0.5) & (G.horizon == 10)]
    print(s[["d_annual", "ep_ratio", "ep_drop_pp", "never_reemployed_share",
             "wage_income_rel_baseline", "unemployment"]].round(4).to_string(index=False))

    print("\n=== CONSISTENCY CHECK: realised reemployment share minus implied rho ===")
    c = G.pivot_table(index="d_annual", columns=["phi", "horizon"],
                      values="circularity_gap")
    print(c.round(4).to_string())
    worst = G.reindex(G.circularity_gap.abs().sort_values(ascending=False).index).head(3)
    print("\n  largest absolute gaps:")
    for _, r in worst.iterrows():
        print(f"    phi {r.phi} d {r.d_annual*100:.2f}% H {int(r.horizon)}y: "
              f"realised {r.realised_reemp_share:.4f} against implied rho "
              f"{r.rho_implied:.4f}, gap {r.circularity_gap:+.4f}")

    # speed limit on the NONEMPLOYMENT range
    NONEMP_MAX = 24.71    # worst prime-age vintage in the sample, January 2012
    lim = []
    for phi in PHIS:
        for H in HORIZONS:
            best = np.nan
            for dd in np.arange(0.0005, 0.0601, 0.0005):
                p = simulate(dd, H, phi, f, T, ex, OMEGA_CASES["dws_blend_0.86"],
                             s_other, E0, U0, pop)
                if float(p["nonemployment_rate"].max()) <= NONEMP_MAX:
                    best = dd
                else:
                    break
            lim.append({"phi": phi, "horizon": H, "max_d_inside_observed": best,
                        "max_cumulative_inside": best * H if best == best else np.nan})
    L = pd.DataFrame(lim)
    L.round(5).to_csv(OUT / "stock_flow_v2_limits.csv", index=False)
    print(f"\n=== SPEED LIMIT on PRIME-AGE NONEMPLOYMENT (max observed {NONEMP_MAX}%) ===")
    print((L.pivot_table(index="horizon", columns="phi",
                         values="max_d_inside_observed") * 100).round(2).to_string())
    print("\n=== MAX CUMULATIVE inside the observed range, percent ===")
    print((L.pivot_table(index="horizon", columns="phi",
                         values="max_cumulative_inside") * 100).round(1).to_string())

    # nonlinearity on E/P and wage income
    nl = []
    for phi in PHIS:
        for metric in ["ep_drop_pp", "wage_income_rel_baseline", "unemployment"]:
            s = G[(G.phi == phi) & (G.horizon == 10)].sort_values("d_annual")
            x = s["d_annual"].to_numpy() * 100
            y = s[metric].to_numpy() * (100 if metric == "unemployment" else 1)
            c2, c1, c0 = np.polyfit(x, y, 2)
            slo, shi = c1 + 2 * c2 * x.min(), c1 + 2 * c2 * x.max()
            yh = c0 + c1 * x + c2 * x ** 2
            r2 = 1 - float(((y - yh) ** 2).sum()) / float(((y - y.mean()) ** 2).sum())
            nl.append({"phi": phi, "metric": metric, "curvature": c2,
                       "slope_low": slo, "slope_high": shi,
                       "acceleration_ratio": shi / slo if slo else np.nan,
                       "r2": r2})
    NL = pd.DataFrame(nl)
    NL.round(4).to_csv(OUT / "stock_flow_v2_nonlinearity.csv", index=False)
    print("\n=== NONLINEARITY on E/P, wage income and unemployment, 10-year horizon ===")
    print(NL.round(4).to_string(index=False))
    print("\n  acceleration ratio above 1 means the marginal harm RISES with the flow")

    (OUT / "stock_flow_v2_summary.json").write_text(json.dumps({
        "baseline": {"pop": pop, "E0": E0, "U0": U0, "ep0": ep0, "nonemp0": nonemp0,
                     "u0": u0 * 100, "rho_implied_new_fit": rho0,
                     "rho_observed_2026": 0.6616},
        "slack_fit_used": f, "exit_share": ex,
        "exit_share_slack_dependence": "NOT SIGNIFICANT on the corrected measure "
                                       "(R2 0.137, t = -1.13); held constant with a range",
        "prime_age_nonemployment_max_observed": NONEMP_MAX,
        "s_other": s_other,
        "limits": L.round(5).to_dict("records")}, indent=2))


if __name__ == "__main__":
    main()
