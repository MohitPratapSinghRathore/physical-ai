"""Item 2, part two. Recompute every extended-axis fiscal result under the bounded rho of
src/rho_bounded.py, and mark exactly what changed.

The arithmetic below is the arithmetic of src/fiscal_extended_axis.py, unchanged, with one
substitution: rho comes from solve_bounded instead of the damped clipped iteration. Where
the bounded treatment returns a band rather than a point, every downstream quantity is
returned as a band and the row is labelled outside the data.

The old file is not overwritten. It is read and diffed, so the change is auditable.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from rho_bounded import params, solve_bounded, pole, audit_rho

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

TAU_L = {"bottom_up_0.301": 0.301, "top_down_0.318": 0.318}
TAU_K_READINGS = {"barkai_rent_0.351": 0.0708, "KN_caseR_rent_0.00": 0.0500}
G_CASES = {"no_outlays": 0.0, "modest_0.10": 0.10, "full_0.25": 0.25}
DISCOUNT = 0.03
OMEGA_SWITCHER = 0.58


def fiscal(rho, d_emp, d_wb, comp, om_cf, tl, tk, g, H):
    """One cell of the extended-axis fiscal arithmetic."""
    R = rho * om_cf * (OMEGA_SWITCHER ** max(d_emp - 1, 0))
    D = comp * d_wb
    k = tl * (1 - R) - tk + g * (1 - rho)
    term = k * D
    cum = k * D * (H + 1) / 2
    pv = sum((k * D * (t / H)) / (1 + DISCOUNT) ** t for t in range(1, H + 1))
    return R, term, cum, pv


def main():
    p = params()
    om_cf = json.loads((OUT / "retained_wage_share_summary.json").read_text()
                       )["omegas"]["counterfactual_blended_central"]
    comp = json.loads((OUT / "capacities.json").read_text())["national_wage_bill_bn"]
    fp = json.loads((OUT / "fiscal_persistence_summary.json").read_text())
    receipts = fp["federal_receipts_bn"]
    axis = pd.read_csv(OUT / "scenario_axis_levels.csv")
    axis = axis[axis.share_of_TOTAL_wage_bill > 0].copy()

    rows = []
    for _, a in axis.iterrows():
        d_emp = float(a["share_of_TOTAL_employment"])
        d_wb = float(a["share_of_TOTAL_wage_bill"])
        b = solve_bounded(d_emp, p)
        # low rho is the bad end for the fiscal loss, high rho the good end
        ends = ([("point", b["rho_clamped"])] if b["point_estimate_available"]
                else [("band_worst", b["rho_band_lo"]), ("band_best", b["rho_band_hi"])])
        for H in (2, 5, 10, 20):
            for tkn, tk in TAU_K_READINGS.items():
                for ln, tl in TAU_L.items():
                    for gn, g in G_CASES.items():
                        for end, rho in ends:
                            R, term, cum, pv = fiscal(rho, d_emp, d_wb, comp, om_cf,
                                                      tl, tk, g, H)
                            rows.append({
                                "group": a["group"],
                                "level_of_exposed": a["level_of_exposed"],
                                "share_of_total_wage_bill": d_wb, "d_emp": d_emp,
                                "horizon": H, "tau_k_reading": tkn, "tau_l": ln,
                                "outlays": gn, "rho_status": b["status"], "end": end,
                                "rho": rho, "R": R,
                                "outside_data": b["outside_data"],
                                "terminal_year_loss_bn": term,
                                "cumulative_loss_bn": cum, "present_value_bn": pv,
                                "terminal_pct_receipts": 100 * term / receipts})
    N = pd.DataFrame(rows)
    N.round(6).to_csv(OUT / "fiscal_extended_axis_bounded.csv", index=False)

    # ---- diff against the superseded file, on the base reading
    O = pd.read_csv(OUT / "fiscal_extended_axis.csv")
    key = ["group", "share_of_total_wage_bill", "horizon", "tau_k_reading",
           "tau_l", "outlays"]
    ob = O[O.rho_mode == "fitted"].copy()
    # the superseded file was written with .round(4); match on the same precision
    ob["share_of_total_wage_bill"] = ob["share_of_total_wage_bill"].round(4)
    N["share_of_total_wage_bill"] = N["share_of_total_wage_bill"].round(4)
    diffs = []
    for k, gnew in N.groupby(key):
        m = ob
        for c, v in zip(key, k):
            m = m[np.isclose(m[c], v, atol=1e-4)] if isinstance(v, float) else m[m[c] == v]
        if m.empty:
            continue
        old = float(m["terminal_year_loss_bn"].iloc[0])
        old_rho = float(m["rho"].iloc[0])
        st = gnew["rho_status"].iloc[0]
        if st == "inside":
            new = float(gnew["terminal_year_loss_bn"].iloc[0])
            lo = hi = new
        else:
            lo = float(gnew["terminal_year_loss_bn"].min())
            hi = float(gnew["terminal_year_loss_bn"].max())
        diffs.append({"group": k[0], "share_of_total_wage_bill": k[1], "horizon": k[2],
                      "tau_k_reading": k[3], "tau_l": k[4], "outlays": k[5],
                      "rho_status": st, "rho_old": old_rho,
                      "rho_new_lo": float(gnew["rho"].min()),
                      "rho_new_hi": float(gnew["rho"].max()),
                      "terminal_old_bn": old, "terminal_new_lo_bn": lo,
                      "terminal_new_hi_bn": hi,
                      "point_withdrawn": st != "inside",
                      "old_inside_new_band": bool(lo - 1e-9 <= old <= hi + 1e-9)})
    D = pd.DataFrame(diffs)
    D.round(6).to_csv(OUT / "fiscal_extended_axis_bounded_diff.csv", index=False)

    base = D[(D.tau_l == "bottom_up_0.301") & (D.outlays == "no_outlays")
             & (D.tau_k_reading == "barkai_rent_0.351") & (D.horizon == 10)]

    emb = base[base.group.str.startswith("embodied")].sort_values(
        ["group", "share_of_total_wage_bill"])

    summ = {
        "pole_at_d_emp": pole(p),
        "observed_rho_range": [p["rho_obs_lo"], p["rho_obs_hi"]],
        "extrapolation_band": [0.0, p["rho_obs_lo"]],
        "rows_total": int(len(D)),
        "rows_point_withdrawn": int(D.point_withdrawn.sum()),
        "share_of_rows_withdrawn": round(float(D.point_withdrawn.mean()), 4),
        "withdrawn_by_group": D[D.point_withdrawn].groupby("group")
                               .size().to_dict(),
        "old_point_inside_new_band_where_withdrawn":
            int(D[D.point_withdrawn].old_inside_new_band.sum()),
        "of_which_rows": int(D.point_withdrawn.sum()),
        "plausibility": [audit_rho(N["rho"], "bounded extended axis"),
                         audit_rho(O["rho"], "superseded extended axis")],
    }
    (OUT / "fiscal_extended_axis_bounded_summary.json").write_text(
        json.dumps(summ, indent=2, default=str))

    pd.set_option("display.width", 220)
    print("EMBODIED, base reading, 10-year horizon")
    print(emb[["group", "share_of_total_wage_bill",
               "rho_status", "rho_old", "rho_new_lo", "rho_new_hi", "terminal_old_bn",
               "terminal_new_lo_bn", "terminal_new_hi_bn", "point_withdrawn",
               "old_inside_new_band"]].round(4).to_string(index=False))
    print()
    print("ALL GROUPS, base reading, share of rows with the point estimate withdrawn")
    g = base.groupby("group").agg(rows=("point_withdrawn", "size"),
                                  withdrawn=("point_withdrawn", "sum"))
    g["pct"] = (100 * g.withdrawn / g.rows).round(1)
    print(g.to_string())
    print()
    print("SUMMARY")
    for k, v in summ.items():
        if k != "plausibility":
            print(" ", k, "=", v)
    print(" plausibility:")
    for c in summ["plausibility"]:
        print("   ", "PASS" if c["passes"] else "FAIL", c["where"],
              "violations", c["violations"], "worst", c["worst"])


if __name__ == "__main__":
    main()
