"""Item 2 of the final analysis session. A bounded replacement for the reemployment rate
on the extended displacement axis.

THE DEFECT. rho is obtained as the fixed point of a stock-flow identity against a fitted
line. In closed form

    rho = (INT + SLOPE*NE0 + SLOPE*c) / (1 + SLOPE*c),   c = 100 * d_emp * (1 - EXIT_SHARE)

with INT = 1.227975, SLOPE = -0.027490, NE0 = 19.310920, EXIT_SHARE = 0.462. The denominator
vanishes at

    d_emp = 1 / (0.027490 * 100 * 0.538) = 0.676150

and above that the closed form returns values outside [0, 1]: at an embodied employment dose
of 0.7365 it returns rho = 4.39, which is not a rate. Equivalently the naive iteration has
multiplier |SLOPE| * 100 * d_emp * 0.538, which exceeds 1 above the same threshold.

WHAT THE PROJECT CODE ACTUALLY DID. src/fiscal_extended_axis.py used a DAMPED iteration with
an in-loop np.clip(rho, 0, 0.999). That is why the published numbers never printed 4.39: past
the pole the damped iteration walks into the clip and settles at rho = 0. So the bound was
being enforced accidentally, by a numerical device, and the value it produced at the boundary
was reported as though it were a solution. It is not a solution. It is the floor.

THE REPLACEMENT, which is what item 2 specifies.

  1. Solve the fixed point.
  2. Accept it as a POINT ESTIMATE only where it lies inside the OBSERVED range of rho,
     [0.49, 0.74], which is the y-range of the fourteen-vintage fit.
  3. Clamp rho to [0, 1] everywhere. This is now an enforced bound, not a side effect.
  4. Outside the observed range, and wherever the denominator is non-positive, report no
     point estimate at all. Report the band that was already defined for extrapolation:
     from the WORST OBSERVED VINTAGE, rho = 0.49, down to ZERO, labelled outside the data.

The band is not new. It is the same "floor at the lowest observed rho" mode the extended axis
already carried. What changes is that outside the observed range it becomes the ONLY output,
rather than one of two modes sitting beside a point estimate that the data cannot support.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"

EXIT_SHARE = 0.462
NONEMP_MAX = 24.71


def params():
    S = json.loads((OUT / "slack_reestimate.json").read_text())
    f = S["fits"]["rho_on_PRIME_AGE_nonemployment"]
    sf = json.loads((OUT / "stock_flow_v3_summary.json").read_text())
    return {
        "intercept": f["intercept"], "slope": f["slope"],
        "nonemp0": sf["baseline"]["nonemp0"],
        "rho_obs_lo": f["y_range"][0], "rho_obs_hi": f["y_range"][1],
        "nonemp_obs_lo": f["x_range"][0], "nonemp_obs_hi": f["x_range"][1],
    }


def pole(p):
    """The employment dose at which the closed form's denominator vanishes."""
    return -1.0 / (p["slope"] * 100.0 * (1.0 - EXIT_SHARE))


def solve_bounded(d_emp, p):
    """Bounded reemployment rate at an employment dose.

    Returns a dict. `status` is one of:
      inside          a point estimate, rho lies inside the observed range
      outside_range   the fixed point exists but lies outside the observed rho range
      no_solution     the denominator is non-positive, no admissible fixed point exists
    Every return carries rho_band_lo and rho_band_hi. Inside the observed range the band
    collapses to the point. Outside it is [0, the worst observed vintage].
    """
    c = 100.0 * d_emp * (1.0 - EXIT_SHARE)
    den = 1.0 + p["slope"] * c
    out = {"d_emp": d_emp, "denominator": den, "past_pole": den <= 0.0}
    if den <= 0.0:
        rho_raw = float("nan")
        status = "no_solution"
    else:
        rho_raw = (p["intercept"] + p["slope"] * p["nonemp0"] + p["slope"] * c) / den
        status = ("inside" if p["rho_obs_lo"] <= rho_raw <= p["rho_obs_hi"]
                  else "outside_range")
    # BOUND, enforced not incidental: rho is a rate.
    rho_clamped = float(np.clip(rho_raw, 0.0, 1.0)) if np.isfinite(rho_raw) else np.nan
    if status == "inside":
        lo = hi = rho_clamped
    else:
        lo, hi = 0.0, p["rho_obs_lo"]        # zero to the worst observed vintage
    ne_lo = p["nonemp0"] + c * (1 - hi)      # low rho gives high nonemployment
    ne_hi = p["nonemp0"] + c * (1 - lo)
    out.update({"rho_fixed_point_raw": rho_raw, "rho_clamped": rho_clamped,
                "status": status, "rho_band_lo": lo, "rho_band_hi": hi,
                "nonemp_lo": ne_lo, "nonemp_hi": ne_hi,
                "outside_data": bool(ne_hi > NONEMP_MAX or status != "inside"),
                "point_estimate_available": status == "inside"})
    return out


def audit_rho(values, label=""):
    """The bound added to the plausibility audit: rho in [0, 1]."""
    v = np.asarray([x for x in np.atleast_1d(values) if np.isfinite(x)], dtype=float)
    bad = v[(v < 0.0) | (v > 1.0)]
    return {"check": "rho in [0, 1]", "where": label, "n": int(v.size),
            "violations": int(bad.size),
            "worst": float(bad[np.argmax(np.abs(bad - 0.5))]) if bad.size else None,
            "passes": bool(bad.size == 0)}


def main():
    p = params()
    dpole = pole(p)
    axis = pd.read_csv(OUT / "scenario_axis_levels.csv")
    axis = axis[axis.share_of_TOTAL_wage_bill > 0].copy()

    rows = []
    for _, a in axis.iterrows():
        r = solve_bounded(float(a["share_of_TOTAL_employment"]), p)
        rows.append({"group": a["group"], "level_of_exposed": a["level_of_exposed"],
                     "share_of_total_wage_bill": float(a["share_of_TOTAL_wage_bill"]),
                     **r})
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "rho_bounded_axis.csv", index=False)

    # the same question on the dose-response axis, where the doses are stated in wage-bill
    # terms and converted with each group's ACS relative wage
    relw = {"embodied": 0.6789, "cognitive_GPT": 1.1996, "cognitive_AIOE": 1.5047}
    grid = []
    for g, rw in relw.items():
        for dose in (0.05, 0.10, 0.25, 0.50, 0.75):
            r = solve_bounded(dose / rw, p)
            grid.append({"exposure_type": g, "wage_bill_dose": dose,
                         "relative_wage": rw, **r})
    G = pd.DataFrame(grid)
    G.to_csv(OUT / "rho_bounded_dose_grid.csv", index=False)

    checks = [audit_rho(R["rho_clamped"], "scenario axis, clamped"),
              audit_rho(R["rho_fixed_point_raw"], "scenario axis, raw fixed point"),
              audit_rho(G["rho_clamped"], "dose grid, clamped"),
              audit_rho(G["rho_fixed_point_raw"], "dose grid, raw fixed point"),
              audit_rho(np.r_[R["rho_band_lo"], R["rho_band_hi"],
                              G["rho_band_lo"], G["rho_band_hi"]], "reported bands")]

    summ = {
        "fit": {k: p[k] for k in p},
        "pole_at_d_emp": dpole,
        "pole_in_wage_bill_terms": {g: dpole * rw for g, rw in relw.items()},
        "observed_rho_range": [p["rho_obs_lo"], p["rho_obs_hi"]],
        "extrapolation_band": [0.0, p["rho_obs_lo"]],
        "scenario_axis_status_counts": R["status"].value_counts().to_dict(),
        "dose_grid_status_counts": G["status"].value_counts().to_dict(),
        "plausibility_checks": checks,
    }
    (OUT / "rho_bounded_summary.json").write_text(json.dumps(summ, indent=2, default=str))

    pd.set_option("display.width", 220)
    print(f"pole at d_emp = {dpole:.6f}")
    print("in wage-bill terms:",
          {g: round(dpole * rw, 4) for g, rw in relw.items()})
    print(f"observed rho range [{p['rho_obs_lo']}, {p['rho_obs_hi']}],"
          f" extrapolation band [0.0, {p['rho_obs_lo']}]")
    print()
    print("DOSE GRID")
    print(G[["exposure_type", "wage_bill_dose", "d_emp", "denominator",
             "rho_fixed_point_raw", "rho_clamped", "status", "rho_band_lo",
             "rho_band_hi", "outside_data"]].round(4).to_string(index=False))
    print()
    print("SCENARIO AXIS, status counts:", R["status"].value_counts().to_dict())
    print("rows past the pole:")
    print(R[R.past_pole][["group", "share_of_total_wage_bill", "d_emp",
                          "rho_fixed_point_raw", "status"]].round(4).to_string(index=False))
    print()
    print("PLAUSIBILITY CHECKS")
    for c in checks:
        print(" ", "PASS" if c["passes"] else "FAIL",
              f'{c["check"]:18s} {c["where"]:32s} n={c["n"]:4d}'
              f' violations={c["violations"]} worst={c["worst"]}')


if __name__ == "__main__":
    main()
