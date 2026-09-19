"""Item 2: the full specification table for the speed limit and the cumulative ceiling.

The speed limit has been quoted as 3.15, then 1.25, then 1.15 percent a year across three
sessions as the specification changed. That is not a measurement moving; it is a modelling
choice moving, and the honest presentation is the whole distribution with the drivers ranked.

DIMENSIONS CROSSED

    slack measure       unemployment rate (circular, retained only to show its effect),
                        16-and-over nonemployment, prime-age nonemployment
    phi                 0, 0.5, 1
    exit treatment      DWS short-run 0.462, low 0.296, high 0.643, Acemoglu-Restrepo
                        long-run 0.75
    hazard conversion   T = 1.0, 1.5, 2.0 years
    attrition alpha     0, 0.5, 1 on the aggregate (labour force exit) ceiling
    turnover            on or off (early-retirement multiplier 1.0 or 1.5)
    horizon             2, 5, 10, 20 years

WHAT THE PAPER MAY QUOTE. The range and the ordering of what matters. Never a single number.

A STRUCTURAL POINT THAT MUST TRAVEL WITH ANY ACCELERATION RESULT. In ANY model where the
reemployment hazard falls with slack, the marginal harm of an extra unit of displacement
rises with the flow, because the same inflow meets a lower outflow rate. Acceleration is
therefore a structural property of the class of model, not a discovery about AI. What the
data identify is the STRENGTH of that feedback, and they identify it only inside the observed
range of the slack measure. Outside that range the acceleration is an extrapolation of a
mechanism, not an estimate of one.
"""
import json, pathlib, itertools
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"

SLACK = {
    "unemployment_CIRCULAR": ("rho_on_unrate_ORIGINAL", 9.8, "unemployment"),
    "nonemployment_16plus": ("rho_on_nonemployment", 41.6, "nonemp16"),
    "prime_age_nonemployment": ("rho_on_PRIME_AGE_nonemployment", 24.71, "nonempPA"),
}
PHIS = [0.0, 0.5, 1.0]
EXITS = {"dws_0.462": 0.462, "dws_low_0.296": 0.296, "dws_high_0.643": 0.643,
         "AR_long_run_0.75": 0.75}
TS = [1.0, 1.5, 2.0]
ALPHAS = [0.0, 0.5, 1.0]
TURNOVER = {"off_1.0": 1.0, "on_1.5": 1.5}
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


def run(d, years, fit, slack_kind, cap, phi, exit_share, T, alpha, turn,
        E0, U0, POP, lfx, s_other):
    E, U = E0, U0
    Dcum = 0.0
    worst = 0.0
    for _ in range(years):
        if slack_kind == "unemployment":
            x = 100.0 * U / (U + E) if (U + E) > 0 else 100.0
        else:
            x = 100.0 * (POP - E) / POP
        worst = max(worst, x)
        rho = float(np.clip(fit["intercept"] + fit["slope"] * x, 1e-6, 0.999))
        still = rho + (1 - rho) * (1 - exit_share)
        rc = rho / still if still > 0 else 0.0
        h = (1 - (1 - min(rc, 0.999)) ** (1.0 / T)) * max(0.0, 1.0 - phi * Dcum)
        a = min((1 - (1 - min((1 - rho) * exit_share, 0.999)) ** (1.0 / T)) * turn, 0.95)
        JD = d * E
        absorbed = min(JD, alpha * lfx * E)
        laid = JD - absorbed
        Oth = s_other * E
        back = h * U
        U, E = (max(U + laid + absorbed + Oth - (h + a) * U, 0.0),
                max(E - laid - absorbed - Oth + back, 0.0))
        Dcum += JD / E0
    return worst


def main():
    S = json.loads((OUT / "slack_reestimate.json").read_text())
    sep = json.loads((OUT / "separations_summary.json").read_text())
    lfx = [g for g in sep["by_group"]
           if g["group"] == "all_occupations"][0]["labour_force_exit_rate_pct"] / 100.0

    emp_rate = float(fred("LREM25TTUSM156S").asof(pd.Timestamp("2026-01-01")))
    part_rate = float(fred("LNS11300060").asof(pd.Timestamp("2026-01-01")))
    POP, E0 = 1.0, emp_rate / 100.0
    U0 = max(part_rate - emp_rate, 0.0) / 100.0

    rows = []
    for sname, (fkey, cap, kind) in SLACK.items():
        fit = S["fits"][fkey]
        for phi, (ename, ex), T, alpha, (tname, turn), H in itertools.product(
                PHIS, EXITS.items(), TS, ALPHAS, TURNOVER.items(), HORIZONS):
            # calibrate the residual inflow for THIS specification
            x0 = (100.0 * U0 / (U0 + E0) if kind == "unemployment"
                  else 100.0 * (POP - E0) / POP)
            rho0 = float(np.clip(fit["intercept"] + fit["slope"] * x0, 1e-6, 0.999))
            st0 = rho0 + (1 - rho0) * (1 - ex)
            h0 = 1 - (1 - rho0 / st0) ** (1 / T)
            a0 = min((1 - (1 - (1 - rho0) * ex) ** (1 / T)) * turn, 0.95)
            u0 = U0 / (U0 + E0)
            s_other = max((u0 / (1 - u0)) * (h0 + a0) - 0.00679, 0.0)
            best = np.nan
            for dd in np.arange(0.0005, 0.1001, 0.0005):
                if run(dd, H, fit, kind, cap, phi, ex, T, alpha, turn,
                       E0, U0, POP, lfx, s_other) <= cap:
                    best = dd
                else:
                    break
            rows.append({"slack": sname, "phi": phi, "exit": ename, "T": T,
                         "alpha": alpha, "turnover": tname, "horizon": H,
                         "speed_limit": best,
                         "cumulative_ceiling": best * H if best == best else np.nan})
    G = pd.DataFrame(rows)
    G.round(5).to_csv(OUT / "specification_table.csv", index=False)

    pd.set_option("display.width", 240)
    ok = G.dropna(subset=["speed_limit"])
    print(f"=== SPECIFICATION TABLE: {len(G):,} cells, {len(ok):,} with a finite limit ===")
    print(f"\n  speed limit, percent a year, over ALL specifications:")
    q = (ok["speed_limit"] * 100).describe(percentiles=[.05, .25, .5, .75, .95])
    print(q.round(3).to_string())
    print(f"\n  cumulative ceiling, percent of employment:")
    q2 = (ok["cumulative_ceiling"] * 100).describe(percentiles=[.05, .25, .5, .75, .95])
    print(q2.round(2).to_string())

    print("\n=== WHICH ASSUMPTION MOVES IT MOST ===")
    imp = []
    for dim in ["slack", "phi", "exit", "T", "alpha", "turnover", "horizon"]:
        g = ok.groupby(dim)["speed_limit"].median() * 100
        imp.append({"dimension": dim, "n_levels": len(g),
                    "min_median": g.min(), "max_median": g.max(),
                    "spread_pp": g.max() - g.min(),
                    "ratio": g.max() / g.min() if g.min() > 0 else np.nan})
    I = pd.DataFrame(imp).sort_values("ratio", ascending=False)
    print(I.round(3).to_string(index=False))

    print("\n=== median speed limit by slack measure and horizon ===")
    print((ok.pivot_table(index="horizon", columns="slack",
                          values="speed_limit", aggfunc="median") * 100).round(2).to_string())

    print("\n=== the headline range the paper may quote ===")
    pa = ok[ok.slack == "prime_age_nonemployment"]
    print(f"  prime-age nonemployment specification, all other dimensions varied:")
    print(f"    speed limit        {pa.speed_limit.min()*100:.2f} to "
          f"{pa.speed_limit.max()*100:.2f} percent a year, median "
          f"{pa.speed_limit.median()*100:.2f}")
    print(f"    cumulative ceiling {pa.cumulative_ceiling.min()*100:.1f} to "
          f"{pa.cumulative_ceiling.max()*100:.1f} percent, median "
          f"{pa.cumulative_ceiling.median()*100:.1f}")

    (OUT / "specification_summary.json").write_text(json.dumps({
        "n_cells": int(len(G)), "n_finite": int(len(ok)),
        "speed_limit_pct": {"min": float(ok.speed_limit.min() * 100),
                            "p25": float(ok.speed_limit.quantile(.25) * 100),
                            "median": float(ok.speed_limit.median() * 100),
                            "p75": float(ok.speed_limit.quantile(.75) * 100),
                            "max": float(ok.speed_limit.max() * 100)},
        "cumulative_ceiling_pct": {"min": float(ok.cumulative_ceiling.min() * 100),
                                   "median": float(ok.cumulative_ceiling.median() * 100),
                                   "max": float(ok.cumulative_ceiling.max() * 100)},
        "drivers_ranked": I.round(4).to_dict("records"),
        "structural_note": "Acceleration is a property of any model in which the "
                           "reemployment hazard falls with slack. The data identify its "
                           "strength only inside the observed range of the slack measure.",
    }, indent=2))


if __name__ == "__main__":
    main()
