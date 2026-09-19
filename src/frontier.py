"""Item 5 plus amendments B and E: the frontier by LEVEL and SPEED, with two failure modes.

SCENARIO GRID (amendment E)
    horizons   2, 5, 10, 20 years
    levels     5, 10, 25, 50, 75, 90 percent of the EXPOSED wage bill
    types      embodied, cognitive AIOE, cognitive GPT, both
Every scenario is expressed as an ANNUAL FLOW, because A56 showed the flow is what binds,
and each is marked against the speed limit under each phi from the destination-pool model.

TWO FAILURE MODES (amendment B), reported separately at every point because they do not
share a driver:

  (1) SPEED-DRIVEN. Unemployment and household distress. Depends on the annual flow, not on
      the cumulative total. A slow path to 90 percent displacement produces little of it.

  (2) SIZE-DRIVEN. Cumulative loss of labour tax base under P1r. Accrues at ANY speed,
      because every displaced worker whose retained wage share is below break-even subtracts
      from the tax base permanently. A slow path produces all of it, just later.

These are the two halves of the paper and conflating them is the error the frontier exists
to prevent.

WAGE COMPOUNDING for repeatedly displaced workers. A worker displaced twice earns
omega**2 of their counterfactual wage, not omega. The cumulative displacement D(t) exceeds 1
in the faster scenarios, which means the average worker is displaced more than once, and the
retained wage share compounds. Reported under both the stayer omega (0.79) and the switcher
omega (0.58) from Huckfeldt, on the counterfactual basis.

FEASIBILITY (amendment E). Embodied annual flows are marked against the capital-formation
bound from src/feasibility_bounds.py. Cognitive flows carry no cap, and that asymmetry is
the point: scenarios above the speed limit are COGNITIVE-LED by construction.

INSIDE and OUTSIDE the data. Any scenario whose implied unemployment exceeds 9.8 percent is
outside the range the DWS relationships were fitted on and is marked. Those rows are handed
to the sudden-shock module rather than reported as estimates here.
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))
ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

HORIZONS = [2, 5, 10, 20]
LEVELS = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90]
TYPES = ["embodied", "cognitive_AIOE", "cognitive_GPT", "both_AIOE"]
PHIS = [0.0, 0.5, 1.0]
OMEGA_STAYER, OMEGA_SWITCHER = 0.79, 0.58
TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}


def main():
    from src.destination_pool import (load_fits, hazards, simulate, exposed_shares)
    R, S = load_fits()
    base = S["baseline_jan2026"]
    E0, U0 = base["employed"], base["unemployed"]
    u0 = base["unrate"] / 100.0
    U_MAX = S["rho_valid_to_unrate"]
    d0 = (3324.0 / 3.0) / E0
    T, em = 1.5, "short_run"
    h0, a0 = hazards(u0 * 100, R, S, T, em)
    s_other = max((u0 / (1 - u0)) * (h0 + a0) - d0, 0.0)

    sh = exposed_shares()
    share_of_emp = {"embodied": sh["embodied"], "cognitive_AIOE": sh["cognitive_AIOE"],
                    "cognitive_GPT": sh["cognitive_GPT"], "both_AIOE": sh["both_AIOE"]}
    lim = pd.read_csv(OUT / "destination_pool_limits.csv")
    feas = pd.read_csv(OUT / "feasibility_bounds.csv")
    # tightest realistic embodied cap: 10 percent of equipment investment, 2x annual wage
    emb_cap = float(feas[(feas.bound == "2_automation_share_0.10") &
                         (feas.capex_multiple_of_annual_wage == 2.0)
                         ]["as_share_of_total_employment"].iloc[0])
    emb_cap_loose = float(feas[feas.bound == "1_all_equipment_investment"
                               ]["as_share_of_total_employment"].max())

    om_cf = json.loads((OUT / "retained_wage_share_summary.json").read_text()
                       )["omegas"]["counterfactual_blended_central"]

    rows = []
    for typ in TYPES:
        se = share_of_emp[typ]
        for lvl in LEVELS:
            for H in HORIZONS:
                # level is a share of the EXPOSED wage bill; convert to a share of TOTAL
                # employment displaced, then to an annual flow
                total_disp = lvl * se
                d = total_disp / H
                for phi in PHIS:
                    p = simulate(d, H, phi, R, S, T, em, s_other, E0, U0)
                    u_term = float(p["u"].iloc[-1])
                    u_max = float(p["u"].max())
                    Dcum = float(p["D_cum"].iloc[-1])
                    sl = lim[(lim.construct == ("both_AIOE" if typ == "both_AIOE"
                                                else f"{typ}_only" if typ != "embodied"
                                                else "embodied_only")) &
                             (lim.phi_label == f"{phi:g}") & (lim.horizon == H)]
                    speed_limit = float(sl["max_d_inside_observed"].iloc[0]) if len(sl) else np.nan
                    # size-driven: cumulative labour tax base lost
                    times_displaced = Dcum  # per initial worker, on average
                    R_stay = om_cf * (OMEGA_STAYER ** max(times_displaced - 1, 0))
                    R_switch = om_cf * (OMEGA_SWITCHER ** max(times_displaced - 1, 0))
                    rho_term = float(np.clip(R["intercept"] +
                                             R["slope_per_pp_unrate"] * u_term * 100,
                                             0, 1))
                    rows.append({
                        "type": typ, "level_of_exposed": lvl, "horizon": H, "phi": phi,
                        "total_displacement_of_employment": total_disp,
                        "d_annual": d,
                        "speed_limit_at_this_phi_and_horizon": speed_limit,
                        "above_speed_limit": bool(d > speed_limit) if speed_limit == speed_limit else None,
                        "u_terminal": u_term, "u_max": u_max,
                        "outside_data": bool(u_max * 100 > U_MAX),
                        "D_cum": Dcum,
                        "rho_terminal": rho_term,
                        "R_terminal_no_compounding": rho_term * om_cf,
                        "R_terminal_stayer_compounded": rho_term * R_stay,
                        "R_terminal_switcher_compounded": rho_term * R_switch,
                        "embodied_feasible_tight": (d <= emb_cap) if typ == "embodied" else None,
                        "embodied_feasible_loose": (d <= emb_cap_loose) if typ == "embodied" else None,
                    })
    F = pd.DataFrame(rows)
    # size-driven failure: cumulative tax base shortfall against break-even
    for ln, tl in TAU_L.items():
        need = 1 - 0.0708 / tl      # post-2017 tau_k with shifting, from A53
        F[f"size_gap_{ln}"] = F["R_terminal_switcher_compounded"] - need
    F.round(6).to_csv(OUT / "frontier_grid.csv", index=False)

    pd.set_option("display.width", 260)
    print("=== exposed employment shares ===")
    for k, v in share_of_emp.items():
        print(f"  {k:16s} {v*100:5.1f}%")
    print(f"\n=== embodied feasibility caps (annual flow, share of total employment) ===")
    print(f"  tight  (10 pct of equipment investment, 2x annual wage): {emb_cap*100:.3f}%")
    print(f"  loose  (ALL equipment investment, 1x annual wage):       {emb_cap_loose*100:.3f}%")

    print("\n=== ANNUAL FLOW by scenario, percent of total employment a year ===")
    piv = F[F.phi == 0].pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                                    values="d_annual") * 100
    print(piv.round(3).to_string())

    print("\n=== SPEED-DRIVEN failure: terminal unemployment, phi = 0.5 ===")
    p2 = F[F.phi == 0.5].pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                                     values="u_terminal") * 100
    print(p2.round(2).to_string())

    print("\n=== INSIDE the observed data range? phi = 0.5 (True means estimable) ===")
    p3 = F[F.phi == 0.5].pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                                     values="outside_data", aggfunc="first")
    print((~p3.astype(bool)).to_string())

    print("\n=== EMBODIED FEASIBILITY: is the required flow physically attainable? ===")
    e = F[(F.type == "embodied") & (F.phi == 0)]
    pe = e.pivot_table(index="level_of_exposed", columns="horizon",
                       values="embodied_feasible_tight", aggfunc="first")
    print("  tight cap:\n" + pe.to_string())
    pe2 = e.pivot_table(index="level_of_exposed", columns="horizon",
                        values="embodied_feasible_loose", aggfunc="first")
    print("  loose cap:\n" + pe2.to_string())

    print("\n=== SIZE-DRIVEN failure: terminal R with switcher compounding, phi = 0.5 ===")
    p4 = F[F.phi == 0.5].pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                                     values="R_terminal_switcher_compounded")
    print(p4.round(3).to_string())
    print(f"\n  break-even R at tau_k = 0.0708 (post-2017 with shifting): "
          f"{1 - 0.0708/0.255:.3f} (tau_l 0.255) to {1 - 0.0708/0.318:.3f} (tau_l 0.318)")

    # nonlinearity test
    print("\n=== NONLINEARITY: marginal terminal u per extra 1pp of annual flow ===")
    nl = []
    for typ in TYPES:
        for phi in PHIS:
            s = F[(F.type == typ) & (F.phi == phi)]
            s = s[s.d_annual > 0].groupby("d_annual", as_index=False)["u_terminal"].mean()
            s = s.sort_values("d_annual")
            x = s["d_annual"].to_numpy() * 100
            y = s["u_terminal"].to_numpy() * 100
            if len(x) < 5:
                continue
            # A QUADRATIC FIT, not a numerical gradient. The scenario grid produces
            # unevenly and sometimes very closely spaced annual flows, and finite
            # differencing across them divides by near-zero spacings and explodes. The
            # curvature coefficient answers the question directly: is the marginal effect
            # of the flow on distress rising?
            c2, c1, c0 = np.polyfit(x, y, 2)
            xl, xh = float(x.min()), float(x.max())
            slope_lo = c1 + 2 * c2 * xl
            slope_hi = c1 + 2 * c2 * xh
            yhat = c0 + c1 * x + c2 * x ** 2
            r2 = 1 - float(((y - yhat) ** 2).sum()) / float(((y - y.mean()) ** 2).sum())
            nl.append({"type": typ, "phi": phi, "n_points": int(len(x)),
                       "flow_range_pct": f"{xl:.2f} to {xh:.2f}",
                       "curvature": float(c2), "slope_at_lowest_flow": float(slope_lo),
                       "slope_at_highest_flow": float(slope_hi),
                       "acceleration_ratio": float(slope_hi / slope_lo)
                       if slope_lo else np.nan,
                       "quadratic_r2": r2})
    NL = pd.DataFrame(nl)
    NL.round(3).to_csv(OUT / "frontier_nonlinearity.csv", index=False)
    print(NL.round(3).to_string(index=False))
    print("\n  a ratio above 1 means the marginal effect of displacement on distress "
          "ACCELERATES with the flow")


if __name__ == "__main__":
    main()
