"""Item 2: fiscal persistence on the EXTENDED total-wage-bill axis.

A75 flagged a defect: the fiscal columns saturated above 25 percent of the total wage bill,
because the persistence run was built on top-quintile scenarios that cap at 23.1 percent. The
2.05 and 9.29 figures at 50 and 75 percent were floors, not estimates. This module removes
the saturation.

HOW R IS OBTAINED ON THE EXTENDED AXIS. R = rho x omega, and rho is the fitted function of
prime-age nonemployment (A63). Terminal nonemployment is taken from the stock-flow identity:
at a cumulative displacement share d of employment, with reemployment share rho and exit
share e, the terminal nonemployment rate is

    nonemp = nonemp_0 + d * (1 - rho)

solved as a fixed point in rho, exactly as src/displacement_to_slack.py does for the
unextended grid. Beyond the observed prime-age nonemployment maximum of 24.71 percent every
row is FLAGGED outside_data and the rho extrapolation is reported as a band between the
fitted line and a floor at the lowest rho ever observed.

The switcher-omega compounding from A62 is retained: workers displaced more than once earn
omega to the power of the number of displacements.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}
TAU_K_READINGS = {"barkai_rent_0.351": 0.0708, "KN_caseR_rent_0.00": 0.0500}
G_CASES = {"no_outlays": 0.0, "modest_0.10": 0.10, "full_0.25": 0.25}
DISCOUNT = 0.03
OASDI_BN, HI_BN = 1323.2, 462.4
OMEGA_SWITCHER = 0.58
NONEMP_MAX = 24.71
EXIT_SHARE = 0.462


def main():
    S = json.loads((OUT / "slack_reestimate.json").read_text())
    f = S["fits"]["rho_on_PRIME_AGE_nonemployment"]
    rho_min_obs = 0.49
    sf = json.loads((OUT / "stock_flow_v3_summary.json").read_text())
    nonemp0 = sf["baseline"]["nonemp0"]
    om_cf = json.loads((OUT / "retained_wage_share_summary.json").read_text()
                       )["omegas"]["counterfactual_blended_central"]
    fp = json.loads((OUT / "fiscal_persistence_summary.json").read_text())
    receipts, comp = fp["federal_receipts_bn"], fp["compensation_bn"]

    axis = pd.read_csv(OUT / "scenario_axis_levels.csv")
    axis = axis[axis.share_of_TOTAL_wage_bill > 0].copy()

    def solve(d_emp, mode):
        ne = nonemp0
        for _ in range(300):
            rho = f["intercept"] + f["slope"] * ne
            if mode == "floor":
                rho = max(rho, rho_min_obs)
            rho = float(np.clip(rho, 0.0, 0.999))
            ne2 = nonemp0 + 100.0 * d_emp * (1 - rho) * (1 - EXIT_SHARE)
            if abs(ne2 - ne) < 1e-9:
                ne = ne2
                break
            ne = 0.5 * ne + 0.5 * ne2
        return ne, rho

    rows = []
    for _, a in axis.iterrows():
        d_emp = a["share_of_TOTAL_employment"]
        d_wb = a["share_of_TOTAL_wage_bill"]
        for mode in ("fitted", "floor"):
            ne, rho = solve(d_emp, mode)
            outside = ne > NONEMP_MAX
            times = max(d_emp, 0.0)
            R = rho * om_cf * (OMEGA_SWITCHER ** max(times - 1, 0))
            D = comp * d_wb
            for H in (2, 5, 10, 20):
                for tkn, tk in TAU_K_READINGS.items():
                    for ln, tl in TAU_L.items():
                        for gn, g in G_CASES.items():
                            k = tl * (1 - R) - tk + g * (1 - rho)
                            term = k * D
                            cum = k * D * (H + 1) / 2
                            pv = sum((k * D * (t / H)) / (1 + DISCOUNT) ** t
                                     for t in range(1, H + 1))
                            rows.append({
                                "group": a["group"], "level_of_exposed": a["level_of_exposed"],
                                "share_of_total_wage_bill": d_wb,
                                "rho_mode": mode, "horizon": H,
                                "tau_k_reading": tkn, "tau_l": ln, "outlays": gn,
                                "nonemployment_terminal": ne, "rho": rho, "R": R,
                                "outside_data": bool(outside),
                                "terminal_year_loss_bn": term,
                                "cumulative_loss_bn": cum, "present_value_bn": pv,
                                "terminal_pct_receipts": 100 * term / receipts,
                                "terminal_pct_OASDI": 100 * term / OASDI_BN,
                                "terminal_pct_HI": 100 * term / HI_BN})
    M = pd.DataFrame(rows)
    M.round(4).to_csv(OUT / "fiscal_extended_axis.csv", index=False)

    base = M[(M.tau_l == "bottom_up_0.301") & (M.outlays == "no_outlays")
             & (M.tau_k_reading == "barkai_rent_0.351") & (M.rho_mode == "fitted")
             & (M.horizon == 10)]
    base = base.copy()
    base["wb_pct"] = (base.share_of_total_wage_bill * 100).round(0)

    pd.set_option("display.width", 240)
    print("=== FISCAL LOSS ON THE EXTENDED AXIS, no saturation ===")
    print("    terminal-year loss, tau_l 0.301, no outlays, Barkai, 10-year horizon")
    for target in (10, 25, 50, 75):
        sub = base[np.isclose(base.wb_pct, target, atol=4)]
        if not len(sub):
            continue
        m = sub.mean(numeric_only=True)
        n_out = int(sub.outside_data.sum())
        print(f"  {target:>3}% of the wage bill: "
              f"{m.terminal_pct_receipts:6.2f}% of receipts, "
              f"{m.terminal_pct_OASDI:6.2f}% of OASDI payroll, "
              f"{m.terminal_pct_HI:6.1f}% of HI revenue   "
              f"[nonemp {m.nonemployment_terminal:.1f}%, rho {m.rho:.3f}, "
              f"{n_out}/{len(sub)} outside data]")

    print("\n=== against the SATURATED figures A75 reported ===")
    print("    A75 said 2.05 percent of receipts and 9.29 percent of OASDI at 25, 50 and 75")
    (OUT / "fiscal_extended_axis_summary.json").write_text(json.dumps({
        "saturation_removed": True,
        "rho_modes": ["fitted", "floor at the lowest observed rho of 0.49"],
        "nonemployment_max_observed": NONEMP_MAX,
        "range_terminal_pct_receipts": [float(M.terminal_pct_receipts.min()),
                                        float(M.terminal_pct_receipts.max())],
    }, indent=2))


if __name__ == "__main__":
    main()
