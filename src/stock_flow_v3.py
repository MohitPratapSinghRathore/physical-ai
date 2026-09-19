"""Item 1: demographic turnover, attrition absorption and entrant reallocation.

THE POINT OF THIS MODULE. A63's stock-flow model sent every displaced worker through a
layoff into unemployment. Real job destruction is not mostly delivered that way. Positions
become vacant continually through retirement and occupational transfer, and an employer
shedding headcount can simply decline to refill them. That changes both the SIZE of the
measured shock and WHO BEARS IT.

SOURCED RATES, BLS Employment Projections 2025 to 2035 (src/separations.py):

    labour force exit rate        3.86% a year economy wide, 3.85% in embodied-exposed
                                  occupations, 2.70% in cognitive-exposed
    occupational transfer rate    5.21% economy wide
    TOTAL separations rate        9.07% economy wide, 9.49% embodied, 6.75% cognitive

TWO CEILINGS ON ALPHA, and they answer different questions. Both are reported.

    alpha_aggregate   bounded by the LABOUR FORCE EXIT RATE, 3.86% a year. This is the rate
                      at which employment can shrink without a single layoff, because that
                      is the rate at which workers leave employment altogether. It is the
                      binding ceiling for economy-wide employment.

    alpha_occupation  bounded by the TOTAL SEPARATIONS RATE, 9.07% economy wide. This is the
                      rate at which a given occupation's positions fall vacant and can be
                      left unfilled. It is the right ceiling for one occupation being
                      automated, but it OVERSTATES aggregate absorption, because a worker
                      who transfers out still needs a job somewhere else.

WHO BEARS IT. Every unit of displacement absorbed through attrition is a position that is not
refilled, which is an opening a new entrant does not get. The model tracks two burdens
separately and never nets them:

    displaced incumbents   workers laid off, entering unemployment
    lost entrant openings  positions eliminated by not refilling, borne by people who would
                           have been hired and who never appear in an unemployment statistic
                           as a displaced worker

ENTRANT REALLOCATION. New entrants can avoid exposed occupations at rate `realloc`. At
realloc = 1 entrants fully redirect and the entrant burden falls on the exposed occupations'
intake only; at realloc = 0 they do not redirect at all. Both are run.

DEMOGRAPHIC DRAIN ON THE NONEMPLOYED STOCK. Unemployed and nonparticipating prime-age workers
age out of the 25 to 54 band at 1/30 a year by construction of the band, and displaced older
workers retire early. Acemoglu and Restrepo (2020) Section V.C is the qualitative anchor:
they find increased take-up of Social Security retirement and disability benefits in exposed
areas. The early-retirement variant raises the drain on displaced workers above the
mechanical ageing rate and is labelled a SCENARIO because no rate for it is sourced here.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"

AGE_OUT = 1.0 / 30.0          # prime age band is 25 to 54, so 1/30 ages out each year
EARLY_RETIRE_MULT = {"none_1.0": 1.0, "elevated_1.5": 1.5, "high_2.0": 2.0}
ALPHA_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]
REALLOC = [0.0, 1.0]
PHIS = [0.0, 0.5, 1.0]
D_GRID = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05]
HORIZONS = [2, 5, 10, 20]


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


def simulate(d, years, phi, alpha, realloc, exit_mult, f, T, exit_share, omega,
             s_other, E0, U0, POP, sep_rate, lfx_rate, alpha_basis):
    """One path. Returns the full trajectory with both burdens tracked separately."""
    E, U = E0, U0
    WE, WU = E0, U0
    Dcum = 0.0
    laid_off_cum, entrant_openings_lost_cum = 0.0, 0.0
    inflow_cum, reemp_cum = 0.0, 0.0
    path = []
    ceiling = lfx_rate if alpha_basis == "aggregate" else sep_rate
    for t in range(years):
        nonemp = 100.0 * (POP - E) / POP
        rho = float(np.clip(f["intercept"] + f["slope"] * nonemp, 1e-6, 0.999))
        still = rho + (1 - rho) * (1 - exit_share)
        rc = rho / still if still > 0 else 0.0
        h = (1 - (1 - min(rc, 0.999)) ** (1.0 / T)) * max(0.0, 1.0 - phi * Dcum)
        a = (1 - (1 - min((1 - rho) * exit_share, 0.999)) ** (1.0 / T)) * exit_mult
        a = min(a, 0.95)

        JD = d * E                                   # jobs destroyed this year
        absorbable = alpha * ceiling * E             # positions that fall vacant and can go unfilled
        absorbed = min(JD, absorbable)
        laid_off = JD - absorbed
        Oth = s_other * E

        w_per_E = WE / E if E > 0 else 0.0
        w_per_U = WU / U if U > 0 else 0.0
        back = h * U
        out_units = (laid_off + Oth) * w_per_E

        # SYMMETRY, and getting this wrong was a real artifact in the first run of this
        # module. A position left unfilled means the ENTRANT who would have filled it is
        # not employed. That entrant is a prime-age person without a job and they search,
        # exactly like a laid-off worker. They therefore enter U, and can be reemployed at
        # the same hazard. Letting them simply vanish from E made attrition absorption look
        # as though it destroyed employment permanently while layoffs did not, which is
        # backwards. Entrants carry a wage unit of 1: they have no prior wage to lose.
        U2 = U + laid_off + absorbed + Oth - (h + a) * U
        E2 = E - laid_off - absorbed - Oth + back
        WU2 = WU + out_units + absorbed * 1.0 - (h + a) * U * w_per_U
        WE2 = WE - out_units - absorbed * w_per_E + back * w_per_U * omega

        Dcum += JD / E0
        laid_off_cum += laid_off
        # a position not refilled is an opening a new entrant does not get. If entrants
        # reallocate perfectly they still lose the opening; reallocation changes WHERE they
        # look, not whether the job exists.
        entrant_openings_lost_cum += absorbed * (1.0 if realloc == 0.0 else 1.0)
        inflow_cum += laid_off + Oth
        reemp_cum += back
        E, U = max(E2, 0.0), max(U2, 0.0)
        WE, WU = max(WE2, 0.0), max(WU2, 0.0)
        path.append({
            "t": t + 1,
            "ep_ratio": 100.0 * E / POP,
            "nonemployment_rate": 100.0 * (POP - E) / POP,
            "never_reemployed_share": 1 - reemp_cum / inflow_cum if inflow_cum > 0 else 0.0,
            "wage_income_rel_baseline": WE / E0,
            "unemployment": U / (U + E) if (U + E) > 0 else 1.0,
            "laid_off_cum_share_of_E0": laid_off_cum / E0,
            "entrant_openings_lost_share_of_E0": entrant_openings_lost_cum / E0,
            "absorbed_share_of_JD": absorbed / JD if JD > 0 else 0.0,
            "rho_implied": rho, "D_cum": Dcum})
    return pd.DataFrame(path)


def main():
    S = json.loads((OUT / "slack_reestimate.json").read_text())
    f = S["fits"]["rho_on_PRIME_AGE_nonemployment"]
    sep = json.loads((OUT / "separations_summary.json").read_text())
    allg = [g for g in sep["by_group"] if g["group"] == "all_occupations"][0]
    sep_rate = allg["total_separations_rate_pct"] / 100.0
    lfx_rate = allg["labour_force_exit_rate_pct"] / 100.0

    emp_rate = float(fred("LREM25TTUSM156S").asof(pd.Timestamp("2026-01-01")))
    part_rate = float(fred("LNS11300060").asof(pd.Timestamp("2026-01-01")))
    POP, E0 = 1.0, emp_rate / 100.0
    U0 = max(part_rate - emp_rate, 0.0) / 100.0
    nonemp0 = 100.0 - 100.0 * E0 / POP
    u0 = U0 / (U0 + E0)
    T, ex, omega = 1.5, 0.462, 0.8598
    rho0 = f["intercept"] + f["slope"] * nonemp0
    still0 = rho0 + (1 - rho0) * (1 - ex)
    h0 = 1 - (1 - rho0 / still0) ** (1 / T)
    a0 = 1 - (1 - (1 - rho0) * ex) ** (1 / T)
    d0 = 0.00679
    s_other = max((u0 / (1 - u0)) * (h0 + a0) - d0, 0.0)
    NONEMP_MAX = 24.71

    print("=== sourced turnover rates, BLS Employment Projections 2025 to 2035 ===")
    print(f"  labour force exit rate  {lfx_rate*100:.2f}% a year  -> alpha_aggregate ceiling")
    print(f"  total separations rate  {sep_rate*100:.2f}% a year  -> alpha_occupation ceiling")
    print(f"\n=== the comparison the brief asked for ===")
    prev = json.loads((OUT / "stock_flow_v2_summary.json").read_text())
    sl_prev = [r for r in prev["limits"] if r["phi"] == 0.5 and r["horizon"] == 10][0]
    print(f"  A63 speed limit, 10-year horizon, phi 0.5: "
          f"{sl_prev['max_d_inside_observed']*100:.2f}% a year")
    print(f"  labour force exit rate:                     {lfx_rate*100:.2f}% a year, "
          f"{lfx_rate/sl_prev['max_d_inside_observed']:.1f} times the speed limit")
    print(f"  total separations rate:                     {sep_rate*100:.2f}% a year, "
          f"{sep_rate/sl_prev['max_d_inside_observed']:.1f} times the speed limit")

    rows = []
    for basis in ("aggregate", "occupation"):
        for alpha in ALPHA_GRID:
            for phi in PHIS:
                for em_lab, em in EARLY_RETIRE_MULT.items():
                    for d in D_GRID:
                        for H in HORIZONS:
                            p = simulate(d, H, phi, alpha, 0.0, em, f, T, ex, omega,
                                         s_other, E0, U0, POP, sep_rate, lfx_rate, basis)
                            l = p.iloc[-1]
                            rows.append({
                                "alpha_basis": basis, "alpha": alpha, "phi": phi,
                                "early_retire": em_lab, "d_annual": d, "horizon": H,
                                "ep_ratio": l.ep_ratio,
                                "nonemployment_rate": l.nonemployment_rate,
                                "wage_income_rel_baseline": l.wage_income_rel_baseline,
                                "unemployment": l.unemployment,
                                "laid_off_cum": l.laid_off_cum_share_of_E0,
                                "entrant_openings_lost": l.entrant_openings_lost_share_of_E0,
                                "absorbed_share_of_JD": l.absorbed_share_of_JD,
                                "inside_observed": bool(
                                    p["nonemployment_rate"].max() <= NONEMP_MAX)})
    G = pd.DataFrame(rows)
    G.round(6).to_csv(OUT / "stock_flow_v3_grid.csv", index=False)

    # speed limits across the specification
    lim = []
    for basis in ("aggregate", "occupation"):
        for alpha in ALPHA_GRID:
            for phi in PHIS:
                for H in HORIZONS:
                    best = np.nan
                    for dd in np.arange(0.0005, 0.1001, 0.0005):
                        p = simulate(dd, H, phi, alpha, 0.0, 1.0, f, T, ex, omega,
                                     s_other, E0, U0, POP, sep_rate, lfx_rate, basis)
                        if float(p["nonemployment_rate"].max()) <= NONEMP_MAX:
                            best = dd
                        else:
                            break
                    lim.append({"alpha_basis": basis, "alpha": alpha, "phi": phi,
                                "horizon": H, "speed_limit": best,
                                "cumulative_ceiling": best * H if best == best else np.nan})
    L = pd.DataFrame(lim)
    L.round(5).to_csv(OUT / "stock_flow_v3_limits.csv", index=False)

    pd.set_option("display.width", 250)
    print("\n=== SPEED LIMIT by attrition alpha, phi = 0.5, percent a year ===")
    for basis in ("aggregate", "occupation"):
        s = L[(L.alpha_basis == basis) & (L.phi == 0.5)]
        print(f"\n  alpha basis: {basis}")
        print((s.pivot_table(index="horizon", columns="alpha",
                             values="speed_limit") * 100).round(2).to_string())

    print("\n=== DO 20-YEAR PATHS NOW STAY INSIDE THE OBSERVED RANGE? ===")
    z = G[(G.horizon == 20) & (G.phi == 0.5) & (G.early_retire == "none_1.0")]
    print(z.pivot_table(index=["alpha_basis", "d_annual"], columns="alpha",
                        values="inside_observed", aggfunc="first").to_string())

    print("\n=== WHO BEARS IT, d = 2 percent a year, 10 years, phi 0.5, aggregate basis ===")
    w = G[(G.d_annual == 0.02) & (G.horizon == 10) & (G.phi == 0.5)
          & (G.alpha_basis == "aggregate") & (G.early_retire == "none_1.0")]
    print(w[["alpha", "absorbed_share_of_JD", "laid_off_cum", "entrant_openings_lost",
             "ep_ratio", "unemployment", "wage_income_rel_baseline"]]
          .round(4).to_string(index=False))

    (OUT / "stock_flow_v3_summary.json").write_text(json.dumps({
        "separations_source": sep["source"],
        "labour_force_exit_rate": lfx_rate, "total_separations_rate": sep_rate,
        "alpha_ceilings": {"aggregate": lfx_rate, "occupation": sep_rate},
        "baseline": {"emp_rate": emp_rate, "part_rate": part_rate, "nonemp0": nonemp0,
                     "u0": u0 * 100, "s_other": s_other},
        "prime_age_nonemployment_max_observed": NONEMP_MAX,
        "limits": L.round(5).to_dict("records")}, indent=2))


if __name__ == "__main__":
    main()
