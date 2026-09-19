"""Amendment A: the destination-pool variant of the stock-flow model.

THE PROBLEM WITH A56. The rho(u) relationship behind the speed limit was estimated on
CYCLICAL variation across fourteen survey vintages. In a cycle, the jobs displaced workers
return to still exist; the recession ends and the destination pool refills. Sustained
technological displacement is not that. If the occupations displaced workers would move into
are themselves being automated, the pool shrinks permanently and the historical hazard
overstates reemployment by more and more as displacement accumulates.

THE AMENDMENT

    h_eff(t) = h(u_t) * max(0, 1 - phi * D(t))

    D(t)  cumulative displacement to date as a share of INITIAL employment
    phi   the share of a displaced worker's feasible destination jobs that are themselves in
          exposed occupations

phi = 0 is A56 exactly. It assumes new work is created at the historical rate indefinitely,
so that however much has already been displaced, the next displaced worker faces the same
reemployment hazard as the first. **The 3.15 percent a year speed limit in A56 is an UPPER
BOUND conditional on that assumption**, and this module is the statement of how much it
depends on it.

phi = 1 is the opposite pole: every destination job is as exposed as the job lost, so the
pool shrinks one for one with cumulative displacement and reemployment stops entirely once
D reaches 1.

ESTIMATING phi. Occupation-to-occupation transition matrices were sought and are recorded in
the output as not obtained from a verifiable public source within this session, so phi is run
over the specified grid {0, 0.5, 1}. A fourth value is added per construct as a transparent
ANCHOR rather than an estimate: if destinations were drawn in proportion to employment, the
probability that a destination is itself in the exposed group equals that group's share of
employment. That anchor is a lower bound on phi for any realistic mobility pattern, because
displaced workers move to NEARBY occupations, and nearby occupations are more similar in
exposure than a random draw would be. It is labelled as an anchor everywhere.

Run for embodied only, cognitive only (both indices) and both together, because the union of
the two exposure sets is larger and its pool therefore shrinks fastest.
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))
ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

PHI_GRID = [0.0, 0.5, 1.0]
D_GRID = [0.005, 0.0075, 0.01, 0.0125, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05]
HORIZONS = [2, 5, 10, 20]   # amendment E: the 2 and 5 year cases were missing
AR_LONG_RUN_EXIT = 0.75


def exposed_shares():
    """Employment share of each construct's top-quintile group, and of the union."""
    from src.stress import scenarios as SC
    B = SC.occupation_scores()
    h3 = SC._h3()
    _, groups = h3.build_groups()
    tot = B["employment"].sum()
    out = {}
    for name in ["cognitive_AIOE", "cognitive_GPT", "embodied"]:
        out[name] = float(B[B["occp"].isin(groups[name])]["employment"].sum() / tot)
    union = set(groups["cognitive_AIOE"]) | set(groups["embodied"])
    out["both_AIOE"] = float(B[B["occp"].isin(union)]["employment"].sum() / tot)
    union_g = set(groups["cognitive_GPT"]) | set(groups["embodied"])
    out["both_GPT"] = float(B[B["occp"].isin(union_g)]["employment"].sum() / tot)
    return out


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
    still = rho + (1 - rho) * (1 - e)
    rc = rho / still if still > 0 else 0.0
    h = 1 - (1 - min(rc, 0.999)) ** (1.0 / T)
    a = 1 - (1 - min((1 - rho) * e, 0.999)) ** (1.0 / T)
    return h, a


def simulate(d, years, phi, R, S, T, exit_mode, s_other, E0, U0):
    E, U, Dcum = E0, U0, 0.0
    path = []
    for t in range(years):
        u = U / (U + E) if (U + E) > 0 else 1.0
        h, a = hazards(u * 100, R, S, T, exit_mode)
        h_eff = h * max(0.0, 1.0 - phi * Dcum)
        Dis = d * E
        Oth = s_other * E
        U2 = U + Dis + Oth - (h_eff + a) * U
        E2 = E - Dis - Oth + h_eff * U
        Dcum += Dis / E0
        E, U = max(E2, 0.0), max(U2, 0.0)
        path.append({"t": t + 1, "u": U / (U + E) if (U + E) > 0 else 1.0,
                     "D_cum": Dcum, "h_eff": h_eff})
    return pd.DataFrame(path)


def main():
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
    constructs = {
        "embodied_only": sh["embodied"],
        "cognitive_AIOE_only": sh["cognitive_AIOE"],
        "cognitive_GPT_only": sh["cognitive_GPT"],
        "both_AIOE": sh["both_AIOE"],
        "both_GPT": sh["both_GPT"],
    }

    rows = []
    for cname, anchor in constructs.items():
        for phi in PHI_GRID + [round(anchor, 4)]:
            plab = "anchor" if abs(phi - round(anchor, 4)) < 1e-9 else f"{phi:g}"
            for d in D_GRID:
                for H in HORIZONS:
                    p = simulate(d, H, phi, R, S, T, em, s_other, E0, U0)
                    rows.append({"construct": cname, "phi_label": plab, "phi": phi,
                                 "d_annual": d, "horizon": H,
                                 "u_terminal": float(p["u"].iloc[-1]),
                                 "D_cum": float(p["D_cum"].iloc[-1]),
                                 "h_eff_terminal": float(p["h_eff"].iloc[-1]),
                                 "inside_observed": float(p["u"].max()) * 100 <= U_MAX})
    G = pd.DataFrame(rows)
    G.round(5).to_csv(OUT / "destination_pool_grid.csv", index=False)

    # speed limits per construct and phi, at 20 years
    lim = []
    for cname, anchor in constructs.items():
        for phi in PHI_GRID + [round(anchor, 4)]:
            plab = "anchor" if abs(phi - round(anchor, 4)) < 1e-9 else f"{phi:g}"
            for H in HORIZONS:
                best = np.nan
                for d in np.arange(0.0005, 0.0601, 0.0005):
                    p = simulate(d, H, phi, R, S, T, em, s_other, E0, U0)
                    if float(p["u"].max()) * 100 <= U_MAX:
                        best = d
                    else:
                        break
                lim.append({"construct": cname, "phi_label": plab, "phi": phi,
                            "horizon": H, "max_d_inside_observed": best,
                            "max_cumulative_inside": best * H if best == best else np.nan})
    L = pd.DataFrame(lim)
    L.round(5).to_csv(OUT / "destination_pool_limits.csv", index=False)

    pd.set_option("display.width", 250)
    print("=== exposed employment shares (the phi anchors) ===")
    for k, v in sh.items():
        print(f"  {k:20s} {v*100:5.1f}% of employment")
    print(f"\n  phi = 0 reproduces A56 exactly and assumes new work is created at the "
          f"historical rate\n  indefinitely. The A56 speed limit of about 3.15 percent a "
          f"year is an UPPER BOUND\n  conditional on that.")

    print("\n=== SPEED LIMIT, percent of employment a year, by construct and phi ===")
    piv = L.pivot_table(index=["construct", "horizon"], columns="phi_label",
                        values="max_d_inside_observed") * 100
    print(piv.round(3).to_string())

    print("\n=== MAXIMUM CUMULATIVE DISPLACEMENT that stays inside the observed range ===")
    piv2 = L.pivot_table(index=["construct", "horizon"], columns="phi_label",
                         values="max_cumulative_inside") * 100
    print(piv2.round(1).to_string())

    print("\n=== is there a CUMULATIVE SIZE THRESHOLD? terminal u at d = 2.5% a year ===")
    s = G[(G.d_annual == 0.025)]
    print(s.pivot_table(index=["construct", "horizon"], columns="phi_label",
                        values="u_terminal").mul(100).round(2).to_string())
    print("\n  and the cumulative displacement reached:")
    print(s.pivot_table(index=["construct", "horizon"], columns="phi_label",
                        values="D_cum").mul(100).round(1).to_string())

    (OUT / "destination_pool_summary.json").write_text(json.dumps({
        "exposed_shares": sh, "phi_grid": PHI_GRID,
        "phi_anchor_note": "employment share of the exposed group; a LOWER BOUND on phi "
                           "because displaced workers move to nearby occupations, which are "
                           "more similar in exposure than a random draw",
        "transition_matrix_status": "NOT OBTAINED from a verifiable public source in this "
                                    "session; phi run over the specified grid instead",
        "phi0_assumption": "new work created at the historical rate indefinitely; the A56 "
                           "speed limit is an upper bound conditional on it",
        "limits": L.round(5).to_dict("records")}, indent=2))


if __name__ == "__main__":
    main()
