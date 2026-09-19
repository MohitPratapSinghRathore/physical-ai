"""Item 4: the fiscal condition restated in ONE statistic, the retained wage share R.

R = rho x omega

R is the share of the displaced wage bill that survives as taxable labour income: the share
of workers reemployed, times the wage they earn relative to what they would otherwise have
earned. Everything the fiscal condition needs from the labour market is in this one number.

DERIVATION

The P1r condition, closed economy, with s the additional taxable surplus per dollar of
displaced wage bill and g added public outlays per dollar of displaced wage bill:

    tau_k*s + tau_l*rho*omega  >=  tau_l + g*(1 - rho)

WITHOUT OUTLAYS (g = 0), and at s = 1, its maximum by construction:

    tau_l*R >= tau_l - tau_k          =>      R >= 1 - tau_k/tau_l

WITH OUTLAYS, g paid to the non-reemployed share (1 - rho):

    tau_l*R >= tau_l - tau_k*s + g*(1 - rho)
    R >= 1 - (tau_k*s)/tau_l + g*(1 - rho)/tau_l

The outlay term is NOT a constant: it depends on rho, which is the same rho inside R. A
labour market that reemploys fewer workers is penalised twice, once through a smaller R and
once through a larger outlay bill. That interaction is invisible in the rho* formulation and
is the reason for restating the condition this way.

WHICH OMEGA. The counterfactual one, from src/omega_blended.py. The condition compares tax
raised after displacement against tax that WOULD have been raised on the same workers absent
displacement, and the counterfactual wage bill grows with economy-wide wages.

VINTAGES. rho is observed for 14 Displaced Worker Survey vintages, 2000 to 2026
(src/bls_dws_history.py). omega is observed for the 2026 vintage only, because earlier
releases do not publish Table 7 in a form this project has parsed. Historical R therefore
holds omega FIXED at the 2026 counterfactual value and varies only rho. That is an
assumption and it is stated on every historical figure: if omega is procyclical, historical
R in slack years is OVERSTATED here.

SWITCHER SCENARIO. Huckfeldt (2022) measures earnings losses relative to a no-displacement
counterfactual, the same basis as omega_counterfactual, and finds occupation SWITCHERS lose
42 percent initially against 21 percent for stayers. AI displacement of an occupation forces
switching by construction, so the switcher end is the relevant analogue and is carried as a
labelled scenario.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}
TAU_K = {"equipment_0.05": 0.05, "net_capital_0.10": 0.10, "statutory_upper_0.21": 0.21}
G = {"none_0.00": 0.0, "modest_0.10": 0.10, "full_0.25": 0.25}

# Huckfeldt (2022), AER 112(4) 1273-1310, verified: 42 percent initial earnings drop for
# occupation switchers against 21 percent for stayers, both relative to a no-displacement
# counterfactual. Switchers remain about 10 percent below counterfactual a decade later.
HUCKFELDT = {"switcher_initial_loss": 0.42, "stayer_initial_loss": 0.21,
             "switcher_loss_10y": 0.10, "stayer_loss_1y": 0.064}


def required_R(tau_l, tau_k, g, rho, s=1.0):
    return 1.0 - (tau_k * s) / tau_l + g * (1.0 - rho) / tau_l


def main():
    ob = json.loads((OUT / "omega_blended_summary.json").read_text())
    om_cf = ob["omega_blended_counterfactual"]
    om_nom = ob["omega_blended_nominal"]
    V = pd.read_csv(OUT / "bls_dws_vintages.csv")
    V = V.dropna(subset=["rho"]).sort_values("release_date")
    rho_2026 = float(V[V["release_date"].str.startswith("2026")]["rho"].iloc[0])

    omegas = {
        "counterfactual_blended_central": om_cf["central"],
        "counterfactual_blended_low": om_cf["low"],
        "counterfactual_blended_high": om_cf["high"],
        "nominal_blended_central": om_nom["central"],
        "full_time_only_nominal_0.985": 0.9853,
        "stipulated_JLS_0.75": 0.75,
        "switcher_scenario_0.58": 1.0 - HUCKFELDT["switcher_initial_loss"],
        "stayer_scenario_0.79": 1.0 - HUCKFELDT["stayer_initial_loss"],
    }

    # ---------- the grid in R ----------
    rows = []
    for ln, tl in TAU_L.items():
        for kn, tk in TAU_K.items():
            for gn, g in G.items():
                req = required_R(tl, tk, g, rho_2026)
                for on, ov in omegas.items():
                    R = rho_2026 * ov
                    rows.append({"tau_l": ln, "tau_k": kn, "g": gn,
                                 "omega_case": on, "omega": ov,
                                 "rho": rho_2026, "R": R, "R_required": req,
                                 "infeasible": req > 1.0, "met": (R >= req) and req <= 1.0,
                                 "gap": R - req})
    G_ = pd.DataFrame(rows)
    G_.round(5).to_csv(OUT / "retained_wage_share_grid.csv", index=False)

    # ---------- historical vintages, omega held at the 2026 counterfactual ----------
    hv = []
    for _, v in V.iterrows():
        for on in ["counterfactual_blended_central", "switcher_scenario_0.58"]:
            ov = omegas[on]
            R = v["rho"] * ov
            for ln, tl in TAU_L.items():
                for kn, tk in TAU_K.items():
                    req = required_R(tl, tk, 0.0, v["rho"])
                    hv.append({"release_date": v["release_date"], "rho": v["rho"],
                               "survey_unrate": v["survey_unrate"], "omega_case": on,
                               "R": R, "tau_l": ln, "tau_k": kn, "R_required": req,
                               "met": (R >= req) and req <= 1.0})
    H = pd.DataFrame(hv)
    H.round(5).to_csv(OUT / "retained_wage_share_vintages.csv", index=False)

    pd.set_option("display.width", 250)
    print("=== R = rho x omega, 2026 survey, rho = %.4f ===" % rho_2026)
    for on, ov in omegas.items():
        print(f"  {on:34s} omega {ov:.4f}   R = {rho_2026*ov:.4f}")

    print("\n=== REQUIRED R = 1 - tau_k/tau_l (no outlays, s = 1) ===")
    base = G_[(G_.g == "none_0.00") & (G_.omega_case == "counterfactual_blended_central")]
    print(base.pivot_table(index="tau_l", columns="tau_k",
                           values="R_required").round(4).to_string())

    print("\n=== MET? central omega (counterfactual blended 0.8598), by g ===")
    c = G_[G_.omega_case == "counterfactual_blended_central"]
    for gn in G:
        s = c[c.g == gn]
        print(f"  g = {gn:12s} met in {int(s['met'].sum()):2d} of {len(s)} cells; "
              f"infeasible {int(s['infeasible'].sum())}")
    print("\n  cell detail at g = none, s = 1:")
    for _, r in c[c.g == "none_0.00"].iterrows():
        print(f"    tau_l {r.tau_l:16s} tau_k {r.tau_k:20s} "
              f"R {r.R:.4f} vs required {r.R_required:.4f}  "
              f"gap {r.gap:+.4f}  met {r.met}")

    print("\n=== MET count by omega case, g = none, s = 1 ===")
    z = G_[G_.g == "none_0.00"]
    print(z.groupby("omega_case").agg(met=("met", "sum"),
                                      cells=("met", "size")).to_string())

    print("\n=== HISTORICAL VINTAGES, omega fixed at the 2026 counterfactual ===")
    hc = H[H.omega_case == "counterfactual_blended_central"]
    per = hc.groupby(["release_date", "rho", "survey_unrate"]).agg(
        met_cells=("met", "sum"), cells=("met", "size"), R=("R", "first")).reset_index()
    print(per.round(4).to_string(index=False))
    print(f"\n  vintages meeting the condition in AT LEAST ONE cell: "
          f"{int((per.met_cells > 0).sum())} of {len(per)}")
    mostperm = hc[(hc.tau_l == "AMR_0.255") & (hc.tau_k == "net_capital_0.10")]
    print(f"  in the most permissive tau_k = 0.10 cell (tau_l 0.255): "
          f"{int(mostperm['met'].sum())} of {len(mostperm)}")
    central = hc[(hc.tau_l == "bottom_up_0.301") & (hc.tau_k == "net_capital_0.10")]
    print(f"  in the central cell (tau_l 0.301, tau_k 0.10): "
          f"{int(central['met'].sum())} of {len(central)}")
    print(f"\n  R range across vintages: {hc['R'].min():.4f} to {hc['R'].max():.4f}")
    sw = H[H.omega_case == "switcher_scenario_0.58"]
    print(f"  under the SWITCHER scenario, vintages meeting in any cell: "
          f"{int(sw.groupby('release_date')['met'].max().sum())} of "
          f"{sw['release_date'].nunique()}")

    (OUT / "retained_wage_share_summary.json").write_text(json.dumps({
        "rho_2026": rho_2026, "omegas": omegas,
        "huckfeldt_2022": HUCKFELDT,
        "R_2026_central": rho_2026 * omegas["counterfactual_blended_central"],
        "R_vintage_range": [float(hc["R"].min()), float(hc["R"].max())],
        "vintages_meeting_any_cell": int((per.met_cells > 0).sum()),
        "vintages_total": int(len(per)),
    }, indent=2))


if __name__ == "__main__":
    main()
