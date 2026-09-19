"""Items 3 and 4: tau_k with alternative sources for each unknown, and the US trajectory
through (R, tau_k) space from 2000 to 2026.

ITEM 3. Each of the two unknowns in A53 rested on a single source. Both now have a verified
alternative that points the OTHER WAY, and tau_k is reported as a range spanned by them.

RENT SHARE, sigma_rent

    Barkai (2020), Journal of Finance 75(5). Pure profit share of gross value added rises
    13.5 percentage points from a near-zero base; capital share 25 percent of gross value
    added in 2014. Implied rent share of total capital income 13.5/(25+13.5) = 0.351.

    Karabarbounis and Neiman (2019), NBER Macroeconomics Annual 33, 167 to 228,
    "Accounting for Factorless Income". They analyse the same residual and are explicit that
    the economic-profits reading is one of three, calling it Case Pi. Verified: "We are
    skeptical of Case Pi as it reveals a tight negative relationship between real interest
    rates and economic profits, leads to large fluctuations in inferred factor-augmenting
    technologies, and results in profits that have risen since the early 1980s but that
    remain lower today than in the 1960s and 1970s", and "We view Case R as most promising",
    Case R attributing the residual to deviations of the rental rate of capital rather than
    to rents. Under Case R the rent share of capital income is approximately ZERO, because
    the residual Barkai reads as profit is read instead as mismeasured cost of capital.

    sigma_rent is therefore reported over 0.00 to 0.351, with 0.75 kept as a labelled
    scenario for AI specifically. The two ends are not a confidence interval; they are two
    incompatible readings of the same accounting residual by credible authors, and the paper
    must say so rather than splitting the difference.

DOMESTICALLY TAXED SHARE

    Torslov, Wier and Zucman. Verified and CONFIRMED to be the US-multinational figure:
    "In 2016, according to the BEA Value Added tables, 48% of the pre-tax profit (1-p)*rK of
    majority-owned affiliates of US multinationals were made in tax havens." This refers to
    FOREIGN AFFILIATE profits, not to worldwide profits of US multinationals. Implied
    domestic share of the shifted-eligible base: 0.52.

    Clausing (2016), "The effect of profit shifting on the corporate tax base in the U.S.
    and beyond". Verified: "profit shifting is likely costing the U.S. government between
    $77 and $111 billion in corporate tax revenue by 2012". Converted to a domestic share by
    comparing the loss with actual federal corporate receipts in 2012: domestic share =
    receipts / (receipts + loss). The arithmetic is shown in the output and the conversion
    is a derivation of this project, not a figure Clausing reports.

    The two are NOT measuring the same object and the range between them is reported as a
    range of interpretations, not as sampling error.

ITEM 4. THE TRAJECTORY

For each of the fourteen DWS vintages, R is observed (rho from that vintage, omega held at
the 2026 counterfactual value because earlier Table 7 distributions are not parsed) and
tau_k is assigned from the tax regime in force that year:

    tau_normal   AMR's own series: about 0.20 in 2000, 0.10 through the 2010s, 0.05 from
                 2018 after the 2017 Act. Interpolated linearly between the anchor years and
                 flagged as interpolation.
    tau_stat     0.35 through 2017, 0.21 from 2018.
    shifting     HELD CONSTANT at the TWZ 0.52 domestic share. No verified time series of
                 the US haven share was obtained, so the path's horizontal movement is
                 driven by statutory and expensing changes only. Stated, not hidden.
"""
import io, json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"

TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}
SIGMA = {"KN_caseR_0.00": 0.00, "barkai_0.351": 0.351, "scenario_AI_0.75": 0.75}
TAU_NORMAL = {"post_TCJA_0.05": 0.05, "2010s_0.10": 0.10, "year_2000_0.20": 0.20}
CLAUSING_LOSS_BN = (77.0, 111.0)   # USD bn, by 2012


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


def tau_normal_year(y):
    """AMR's series, linearly interpolated between the anchors it states."""
    return float(np.interp(y, [2000, 2010, 2017, 2018, 2026],
                              [0.20, 0.10, 0.10, 0.05, 0.05]))


def main():
    # ---- Clausing conversion ----
    fct = fred("FCTAX")          # federal current tax receipts on corporate income, USD bn
    rec2012 = float(fct.asof(pd.Timestamp("2012-10-01")))
    dom_clausing = (rec2012 / (rec2012 + CLAUSING_LOSS_BN[1]),
                    rec2012 / (rec2012 + CLAUSING_LOSS_BN[0]))
    DOMESTIC = {
        "imported_capital_0.00": 0.00,
        "TWZ_US_affiliates_0.52": 0.52,
        "clausing_low": dom_clausing[0],
        "clausing_high": dom_clausing[1],
        "closed_economy_1.00": 1.00,
    }

    rws = json.loads((OUT / "retained_wage_share_summary.json").read_text())
    R26 = rws["R_2026_central"]
    om = rws["omegas"]["counterfactual_blended_central"]

    rows = []
    for sn, sg in SIGMA.items():
        for dn, dm in DOMESTIC.items():
            for tn, tv in TAU_NORMAL.items():
                tk = sg * (dm * 0.21) + (1 - sg) * tv
                rows.append({"sigma_case": sn, "sigma_rent": sg, "domestic_case": dn,
                             "domestic_share": dm, "tau_normal_case": tn,
                             "tau_normal": tv, "tau_k": tk,
                             "sourced": sn in ("KN_caseR_0.00", "barkai_0.351")})
    T = pd.DataFrame(rows)
    T.round(5).to_csv(OUT / "tau_k_second_pass.csv", index=False)
    srcd = T[T.sourced]

    need = {ln: (1 - R26) * tl for ln, tl in TAU_L.items()}

    pd.set_option("display.width", 250)
    print("=== Clausing conversion (a derivation of this project, not his figure) ===")
    print(f"  federal corporate receipts 2012Q4: {rec2012:,.1f} bn USD")
    print(f"  Clausing loss 77 to 111 bn  ->  domestic share "
          f"{dom_clausing[0]:.4f} to {dom_clausing[1]:.4f}")
    print(f"  against TWZ US-affiliate implied domestic share 0.52")

    print("\n=== tau_k RANGE by case, SOURCED rent shares only (KN 0.00 to Barkai 0.351) ===")
    g = srcd.groupby(["domestic_case", "tau_normal_case"])["tau_k"].agg(["min", "max"])
    print(g.round(4).to_string())

    print("\n=== REQUIRED tau_k at R = %.4f, by labour tax rate ===" % R26)
    for ln, v in need.items():
        print(f"  tau_l {ln:18s} ({TAU_L[ln]:.3f}):  tau_k must be >= {v:.4f}")

    print("\n=== PASS or FAIL, sourced rent shares, by labour tax rate ===")
    for ln, v in need.items():
        sub = srcd.assign(passes=srcd.tau_k >= v)
        print(f"\n  -- tau_l = {TAU_L[ln]:.3f}, need tau_k >= {v:.4f}: "
              f"{int(sub.passes.sum())} of {len(sub)} cells pass --")
        piv = sub.pivot_table(index="domestic_case", columns="tau_normal_case",
                              values="passes", aggfunc="mean")
        print(piv.round(2).to_string())

    # ---------------- item 4: trajectory ----------------
    V = pd.read_csv(OUT / "bls_dws_vintages.csv").dropna(subset=["rho"]).copy()
    V["year"] = V["release_date"].str[:4].astype(int)
    V["R"] = V["rho"] * om
    V["tau_normal"] = V["year"].map(tau_normal_year)
    V["tau_stat"] = np.where(V["year"] <= 2017, 0.35, 0.21)
    traj = []
    for sn, sg in [("KN_caseR_0.00", 0.00), ("barkai_0.351", 0.351)]:
        for dn, dm in [("TWZ_US_affiliates_0.52", 0.52),
                       ("closed_economy_1.00", 1.00)]:
            for _, v in V.iterrows():
                tk = sg * (dm * v["tau_stat"]) + (1 - sg) * v["tau_normal"]
                rec = {"year": int(v["year"]), "rho": v["rho"], "R": v["R"],
                       "sigma_case": sn, "domestic_case": dn, "tau_k": tk,
                       "tau_normal": v["tau_normal"], "tau_stat": v["tau_stat"]}
                for ln, tl in TAU_L.items():
                    rec[f"met_{ln}"] = bool(v["R"] >= 1 - tk / tl)
                traj.append(rec)
    TR = pd.DataFrame(traj)
    TR.round(5).to_csv(OUT / "tau_k_trajectory.csv", index=False)

    print("\n=== TRAJECTORY, Barkai rent share, TWZ shifting ===")
    b = TR[(TR.sigma_case == "barkai_0.351") &
           (TR.domestic_case == "TWZ_US_affiliates_0.52")].sort_values("year")
    print(b[["year", "rho", "R", "tau_normal", "tau_stat", "tau_k",
             "met_AMR_0.255", "met_bottom_up_0.301"]].round(4).to_string(index=False))

    print("\n=== CROSSING YEAR, met to unmet, by case ===")
    for (sn, dn), grp in TR.groupby(["sigma_case", "domestic_case"]):
        for ln in TAU_L:
            s = grp.sort_values("year")
            met = s[f"met_{ln}"].to_numpy()
            yrs = s["year"].to_numpy()
            cross = None
            for i in range(1, len(met)):
                if met[i - 1] and not met[i]:
                    cross = int(yrs[i])
            ever = met.any()
            print(f"  {sn:16s} {dn:26s} tau_l {TAU_L[ln]:.3f}: "
                  f"{'never met' if not ever else ('always met' if met.all() else f'crosses at {cross}')}")

    (OUT / "tau_k_second_pass_summary.json").write_text(json.dumps({
        "clausing_receipts_2012_bn": rec2012,
        "clausing_loss_bn": CLAUSING_LOSS_BN,
        "domestic_share_clausing": list(dom_clausing),
        "domestic_share_TWZ": 0.52,
        "sigma_rent_sourced_range": [0.0, 0.351],
        "tau_k_sourced_range": [float(srcd.tau_k.min()), float(srcd.tau_k.max())],
        "required_tau_k": need, "R_2026": R26,
        "shifting_held_constant_in_trajectory": True,
    }, indent=2))
    make_figure(TR, need, R26)


def make_figure(TR, need, R26):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.6), sharey=True)
    for ax, sn, ttl in zip(axes, ["barkai_0.351", "KN_caseR_0.00"],
                           ["Rent share 0.351 (Barkai)",
                            "Rent share 0.00 (Karabarbounis and Neiman, Case R)"]):
        tk = np.linspace(0, 0.30, 300)
        for ln, tl in TAU_L.items():
            ax.plot(tk, 1 - tk / tl, lw=1.6,
                    label=f"break-even, tau_l = {tl:.3f}" if sn == "barkai_0.351" else None)
        for dn, col, mk in [("TWZ_US_affiliates_0.52", "#c00000", "o"),
                            ("closed_economy_1.00", "#1f4e79", "s")]:
            s = TR[(TR.sigma_case == sn) & (TR.domestic_case == dn)].sort_values("year")
            ax.plot(s["tau_k"], s["R"], color=col, lw=1.4, marker=mk, ms=4.5, alpha=0.9,
                    label=("US path, " + ("with shifting" if "TWZ" in dn else "closed economy")))
            for _, v in s.iterrows():
                if int(v["year"]) in (2000, 2010, 2018, 2026):
                    ax.annotate(str(int(v["year"])), (v["tau_k"], v["R"]),
                                textcoords="offset points", xytext=(6, 3), fontsize=8)
        ax.set_xlim(0, 0.30); ax.set_ylim(0, 0.9)
        ax.set_xlabel("Effective tax rate on AI surplus, tau_k")
        ax.set_title(ttl, fontsize=10)
        ax.grid(alpha=0.25, lw=0.6)
    axes[0].set_ylabel("Retained wage share, R = rho x omega")
    axes[0].legend(frameon=False, fontsize=8)
    axes[1].legend(frameon=False, fontsize=8)
    fig.suptitle("The US path through (R, tau_k) space, 2000 to 2026. "
                 "Points above a break-even line satisfy the fiscal condition.",
                 fontsize=11, y=1.02)
    fig.tight_layout()
    d = ROOT / "paper" / "figures"
    d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / "fig_trajectory_R_tauk.png", dpi=200, bbox_inches="tight")
    fig.savefig(d / "fig_trajectory_R_tauk.pdf", bbox_inches="tight")
    print(f"\nfigure written to {d / 'fig_trajectory_R_tauk.png'}")


if __name__ == "__main__":
    main()
