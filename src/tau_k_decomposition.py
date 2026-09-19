"""Items 2 and 3: which tau_k, and the (R, tau_k) diagram.

A50 found that within the omega range the verdict on the fiscal condition is decided by
tau_k. That makes tau_k the parameter the paper turns on, and it has been carried as a bare
grid of 0.05, 0.10 and 0.21 with no account of WHY it might take any of those values. This
module decomposes it.

THE DECOMPOSITION

Taxable surplus from automation splits into the NORMAL RETURN to the capital employed and
the RENT (pure profit) earned above it. The two are taxed differently and the difference is
not a detail:

    tau_k(AI surplus) = sigma_rent * tau_rent + (1 - sigma_rent) * tau_normal

WHY EXPENSING MATTERS. Under full immediate expensing a business-level capital tax becomes a
cash-flow tax, which exempts the normal return and falls only on rents. Verified verbatim,
Auerbach (2017), NBER Working Paper 23881, "Demystifying the Destination-Based Cash-Flow
Tax": "Hence, the cash-flow tax acts as a tax on pure profits, exempting only the normal
return from taxation." Acemoglu, Manera and Restrepo (2020) show the same algebra in their
setting: "with immediate expensing (alpha_j = 1), we have tau_k,j passthrough,equity = 0",
and for an equity-financed C corporation the effective rate collapses to the shareholder
level rate.

SOURCED INPUTS

    tau_normal   Acemoglu, Manera and Restrepo (2020), Brookings Papers on Economic
                 Activity, verified verbatim: "Effective capital taxes on software and
                 equipment, on the other hand, are much lower, 10 percent in the 2010s and
                 5 percent after the 2017 tax reforms, though they used to be about 20
                 percent in 2000."
                 These are the ORIGIN of the 0.05, 0.10 and 0.21 grid this project has been
                 using without attribution.

    tau_stat     21 percent, the US statutory federal corporate rate since the 2017 Act.

    haven share  Torslov, Wier and Zucman, "The Missing Profits of Nations", verified
                 verbatim: "close to 40% of multinational profits are shifted to tax havens
                 globally", and for the US specifically, "In 2016, according to the BEA
                 Value Added tables, 48% of the pre-tax profit (1-p)*rK of majority-owned
                 affiliates of US multinationals were made in tax havens."
                 NOTE, and it bounds the use made of it: 48 percent refers to the profits of
                 FOREIGN AFFILIATES, not to all profits of US multinationals.

    sigma_rent   Barkai (2020), Journal of Finance 75(5), verified verbatim: "the pure
                 profit share (equal to the ratio of pure profits to gross value added)
                 increases by 13.5 percentage points", from a level that was "very small in
                 the early 1980s"; and "the capital share declines from 32% of gross value
                 added in 1984 to 25% of gross value added in 2014".
                 Rent share of total capital income implied: 13.5 / (25 + 13.5) = 0.351.
                 This is an ECONOMY-WIDE nonfinancial corporate anchor and it is the ONLY
                 sourced point on this parameter.

WHAT IS SOURCED AND WHAT IS NOT. tau_normal, tau_stat, the haven share and the 0.351 rent
anchor are sourced and verified. Every rent share above 0.351 is a SCENARIO with no source:
AI and software businesses plausibly earn higher rents than the nonfinancial corporate
average, but this repository has not measured that and will not assert it. Scenario rows are
labelled in the output and must be labelled in the paper.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

TAU_NORMAL = {"post_TCJA_0.05": 0.05, "2010s_0.10": 0.10, "year_2000_0.20": 0.20}
TAU_STAT = 0.21
# domestic share of rents actually reaching the US tax base
DOMESTIC = {
    "closed_economy_1.00": 1.00,
    "profit_shifting_0.52": 0.52,     # 1 - 0.48, TWZ US affiliate haven share
    "profit_shifting_global_0.60": 0.60,   # 1 - 0.40, TWZ global shifted share
    "imported_capital_0.00": 0.00,    # surplus accrues entirely abroad
}
SIGMA_RENT = {
    "barkai_sourced_0.351": 0.351,
    "scenario_0.50": 0.50,
    "scenario_0.75": 0.75,
}
SOURCED_SIGMA = "barkai_sourced_0.351"
TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}


def main():
    rws = json.loads((OUT / "retained_wage_share_summary.json").read_text())
    V = pd.read_csv(OUT / "bls_dws_vintages.csv").dropna(subset=["rho"])
    om_cf = rws["omegas"]["counterfactual_blended_central"]
    rho26 = rws["rho_2026"]
    R26 = rho26 * om_cf

    rows = []
    for sn, sg in SIGMA_RENT.items():
        for dn, dm in DOMESTIC.items():
            for tn, tnv in TAU_NORMAL.items():
                tau_rent = dm * TAU_STAT
                tk = sg * tau_rent + (1 - sg) * tnv
                rows.append({
                    "sigma_rent_case": sn, "sigma_rent": sg,
                    "domestic_case": dn, "domestic_share": dm,
                    "tau_normal_case": tn, "tau_normal": tnv,
                    "tau_rent_effective": tau_rent, "tau_k_implied": tk,
                    "sourced": (sn == SOURCED_SIGMA)})
    T = pd.DataFrame(rows)
    T.round(5).to_csv(OUT / "tau_k_decomposition.csv", index=False)

    srcd = T[T["sourced"]]
    print("=== tau_k IMPLIED ON AI SURPLUS ===")
    print("\n-- SOURCED rent share only (Barkai 0.351) --")
    print(srcd.pivot_table(index="domestic_case", columns="tau_normal_case",
                           values="tau_k_implied").round(4).to_string())
    print("\n-- full grid including SCENARIO rent shares --")
    print(T.pivot_table(index=["sigma_rent_case", "domestic_case"],
                        columns="tau_normal_case",
                        values="tau_k_implied").round(4).to_string())
    print(f"\n  sourced-only range: {srcd.tau_k_implied.min():.4f} to "
          f"{srcd.tau_k_implied.max():.4f}")
    print(f"  full range incl. scenarios: {T.tau_k_implied.min():.4f} to "
          f"{T.tau_k_implied.max():.4f}")

    # where does each land against the break-even requirement at observed R?
    print(f"\n=== against observed R = {R26:.4f} ===")
    need = {ln: (1 - R26) * tl for ln, tl in TAU_L.items()}   # tau_k needed to just pass
    for ln, tk_need in need.items():
        print(f"  tau_l {ln:18s}: condition passes iff tau_k >= {tk_need:.4f}")
    T["passes_AMR"] = T.tau_k_implied >= need["AMR_0.255"]
    T["passes_central"] = T.tau_k_implied >= need["bottom_up_0.301"]
    print(f"\n  cells passing at tau_l 0.255: {int(T.passes_AMR.sum())} of {len(T)} "
          f"(sourced-rent-share only: {int(srcd.assign(p=srcd.tau_k_implied>=need['AMR_0.255']).p.sum())} of {len(srcd)})")
    print(f"  cells passing at tau_l 0.301: {int(T.passes_central.sum())} of {len(T)}")

    (OUT / "tau_k_decomposition_summary.json").write_text(json.dumps({
        "tau_normal_sourced_AMR2020": TAU_NORMAL,
        "tau_statutory": TAU_STAT,
        "domestic_share_cases": DOMESTIC,
        "sigma_rent_cases": SIGMA_RENT,
        "sourced_sigma_rent": SOURCED_SIGMA,
        "tau_k_range_sourced_sigma": [float(srcd.tau_k_implied.min()),
                                      float(srcd.tau_k_implied.max())],
        "tau_k_range_all": [float(T.tau_k_implied.min()), float(T.tau_k_implied.max())],
        "R_2026": R26,
        "tau_k_needed_to_pass": need,
    }, indent=2))
    make_figure(T, srcd, R26, V, rws, need)


def make_figure(T, srcd, R26, V, rws, need):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    om_cf = rws["omegas"]["counterfactual_blended_central"]
    om_sw = rws["omegas"]["switcher_scenario_0.58"]
    fig, ax = plt.subplots(figsize=(9.2, 6.0))

    tk = np.linspace(0, 0.32, 400)
    colors = {"AMR_0.255": "#1f4e79", "bottom_up_0.301": "#a6320a",
              "bottom_up_0.318": "#5a5a5a"}
    for ln, tl in TAU_L.items():
        ax.plot(tk, 1 - tk / tl, color=colors[ln], lw=2.0,
                label=f"break-even, tau_l = {tl:.3f}, no outlays")
    # with outlays g = 0.10 at rho = 0.6616
    rho = rws["rho_2026"]
    ax.plot(tk, 1 - tk / 0.301 + 0.10 * (1 - rho) / 0.301, color="#a6320a",
            lw=1.6, ls="--", label="break-even, tau_l = 0.301, outlays g = 0.10")

    # tau_k regime bands from the decomposition, SOURCED rent share only
    lo, hi = float(srcd.tau_k_implied.min()), float(srcd.tau_k_implied.max())
    ax.axvspan(lo, hi, color="#c8dcc8", alpha=0.55, zorder=0)
    ax.axvspan(float(T.tau_k_implied.min()), float(T.tau_k_implied.max()),
               color="#e8f0e8", alpha=0.45, zorder=0)

    # DWS vintages
    R_v = V["rho"].to_numpy(float) * om_cf
    ax.scatter(np.full(len(R_v), 0.10), R_v, s=34, color="#333333", zorder=5,
               marker="o", label="14 DWS vintages at tau_k = 0.10")
    for _, v in V.iterrows():
        if v["release_date"][:4] in ("2000", "2010", "2026"):
            ax.annotate(v["release_date"][:4], (0.10, v["rho"] * om_cf),
                        textcoords="offset points", xytext=(7, -3), fontsize=8)
    ax.scatter([0.10], [R26], s=95, color="#c00000", zorder=6, marker="*",
               label=f"2026 observed, R = {R26:.3f}")
    ax.scatter([0.10], [rws["rho_2026"] * om_sw], s=70, color="#c00000", zorder=6,
               marker="v", label=f"switcher scenario, R = {rws['rho_2026']*om_sw:.3f}")

    ax.set_xlim(0, 0.32); ax.set_ylim(0, 1.0)
    ax.set_xlabel("Effective tax rate on AI surplus, tau_k")
    ax.set_ylabel("Retained wage share, R = rho x omega")
    ax.grid(alpha=0.25, lw=0.6)
    ax.set_title("The fiscal condition has two levers. Points above a line satisfy it.",
                 fontsize=11)
    h, l = ax.get_legend_handles_labels()
    h += [Line2D([], [], color="#c8dcc8", lw=10),
          Line2D([], [], color="#e8f0e8", lw=10)]
    l += ["tau_k, sourced rent share (Barkai 0.351)",
          "tau_k, incl. scenario rent shares"]
    ax.legend(h, l, frameon=False, fontsize=8.2, loc="upper right")
    fig.tight_layout()
    d = ROOT / "paper" / "figures"
    d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / "fig_R_tauk.png", dpi=200, bbox_inches="tight")
    fig.savefig(d / "fig_R_tauk.pdf", bbox_inches="tight")
    print(f"\nfigure written to {d / 'fig_R_tauk.png'}")


if __name__ == "__main__":
    main()
