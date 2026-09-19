"""Item 5: the REINSTATEMENT TERM, one re-run of the specification table, and then the
labour model is FROZEN as an appendix scenario generator.

WHY THIS TERM IS MISSING AND WHY THAT MATTERS. Every version of this project's labour model
has been a displacement-only model. Workers leave employment, some are reemployed into
EXISTING jobs at a hazard that falls with slack, and the destination pool shrinks as
displacement accumulates. There is no channel by which the technology that destroys tasks
also creates them. Acemoglu and Restrepo's own framework says that channel is not small and
is not optional.

THE SOURCE, verified this session and now in data/raw/manual/.
Acemoglu and Restrepo, "Automation and New Tasks: How Technology Displaces and Reinstates
Labor", Journal of Economic Perspectives 33(2), Spring 2019, pages 3 to 30.

  1947 to 1987, page 19: "the displacement effect reduced labor demand at about 0.48 percent
  per year, but simultaneously, there was an equally strong reinstatement effect, equivalent
  to an increase in labor demand of 0.47 percent per year."

  1987 to 2017, page 21: "reinstatement increased labor demand only by 0.35 percent per year
  compared to 0.47 percent in 1947-1987" and "displacement reduced labor demand by 0.7
  percent per year compared to 0.48 percent in 1947-1987". Cumulatively over that period,
  "changes in the task content of production reduced labor demand by 10 percent".

So reinstatement is not a hypothetical offset. It ran at 0.47 percent a year for forty years
and at 0.35 percent a year for the thirty after that, against displacement of 0.48 and then
0.70. THE HISTORICAL RECORD IS OF TWO LARGE AND NEARLY OFFSETTING FLOWS, and a model with
only one of them will overstate the net damage of any displacement path by construction.

HOW IT ENTERS. Each year new tasks raise labour demand by r times employment, which draws
workers out of the unemployment pool into new jobs, capped by the pool itself:

    reinstated = min(r * E, U)

Three settings are crossed with every existing dimension:

    off_0.000        the displacement-only model this project has been running
    recent_0.0035    Acemoglu and Restrepo's 1987 to 2017 estimate
    postwar_0.0047   their 1947 to 1987 estimate

THE HONEST READING OF THE RESULT, stated before it is computed. Adding a reinstatement flow
can only RAISE the speed limit, because it adds an outflow from unemployment. The question
is by how much, and whether the speed limit is more sensitive to this term than to the
modelling choices the project has been arguing about. If it is, then the ranking of what
matters in the specification table changes and the paper must say so.

AFTER THIS RUN THE LABOUR MODEL IS FROZEN. It becomes an appendix scenario generator: it
produces doses for the dose-response table and nothing else. No result in the body of the
paper depends on its parameters, and no further session reopens them.
"""
import itertools, json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"

from src.specification_table import (SLACK, PHIS, EXITS, TS, ALPHAS, TURNOVER, HORIZONS,
                                     fred)

REINSTATEMENT = {"off_0.0000": 0.0,
                 "AR_recent_0.0035": 0.0035,
                 "AR_postwar_0.0047": 0.0047}


def run(d, years, fit, slack_kind, cap, phi, exit_share, T, alpha, turn,
        E0, U0, POP, lfx, s_other, rein):
    """As src/specification_table.run, with one added flow: new tasks reinstate labour at
    rate `rein` times employment each year, drawn from the unemployment pool."""
    E, U = E0, U0
    Dcum, worst = 0.0, 0.0
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
        new_tasks = min(rein * E, max(U + laid + absorbed + Oth - (h + a) * U, 0.0))
        U = max(U + laid + absorbed + Oth - (h + a) * U - new_tasks, 0.0)
        E = max(E - laid - absorbed - Oth + back + new_tasks, 0.0)
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
        for phi, (ename, ex), T, alpha, (tname, turn), H, (rname, rein) in \
                itertools.product(PHIS, EXITS.items(), TS, ALPHAS, TURNOVER.items(),
                                  HORIZONS, REINSTATEMENT.items()):
            x0 = (100.0 * U0 / (U0 + E0) if kind == "unemployment"
                  else 100.0 * (POP - E0) / POP)
            rho0 = float(np.clip(fit["intercept"] + fit["slope"] * x0, 1e-6, 0.999))
            st0 = rho0 + (1 - rho0) * (1 - ex)
            h0 = 1 - (1 - rho0 / st0) ** (1 / T)
            a0 = min((1 - (1 - (1 - rho0) * ex) ** (1 / T)) * turn, 0.95)
            u0 = U0 / (U0 + E0)
            s_other = max((u0 / (1 - u0)) * (h0 + a0) - 0.00679, 0.0)
            best = np.nan
            for dd in np.arange(0.0005, 0.1501, 0.0005):
                if run(dd, H, fit, kind, cap, phi, ex, T, alpha, turn,
                       E0, U0, POP, lfx, s_other, rein) <= cap:
                    best = dd
                else:
                    break
            rows.append({"slack": sname, "phi": phi, "exit": ename, "T": T,
                         "alpha": alpha, "turnover": tname, "horizon": H,
                         "reinstatement": rname, "reinstatement_rate": rein,
                         "speed_limit": best,
                         "cumulative_ceiling": best * H if best == best else np.nan})
    G = pd.DataFrame(rows)
    G.round(5).to_csv(OUT / "specification_table_with_reinstatement.csv", index=False)

    pd.set_option("display.width", 240)
    ok = G.dropna(subset=["speed_limit"])
    print(f"=== SPECIFICATION TABLE WITH THE REINSTATEMENT TERM: {len(G):,} cells, "
          f"{len(ok):,} finite ===")
    print("\n=== SPEED LIMIT, percent a year, by reinstatement setting ===")
    q = ok.groupby("reinstatement")["speed_limit"].describe(
        percentiles=[.05, .5, .95])[["5%", "50%", "95%", "max"]] * 100
    print(q.round(3).to_string())

    base = ok[ok.reinstatement == "off_0.0000"]["speed_limit"].median() * 100
    for r in ["AR_recent_0.0035", "AR_postwar_0.0047"]:
        m = ok[ok.reinstatement == r]["speed_limit"].median() * 100
        print(f"\n  {r}: median speed limit {m:.3f} percent a year against {base:.3f} "
              f"with the term off, a factor of {m / base:.2f}")

    print("\n=== WHAT MATTERS MOST, variance of the speed limit explained by each choice ===")
    tot = ok["speed_limit"].var()
    rank = []
    for c in ["slack", "phi", "exit", "T", "alpha", "turnover", "horizon",
              "reinstatement"]:
        between = ok.groupby(c)["speed_limit"].mean().var(ddof=0)
        rank.append((c, between / tot))
    for c, s in sorted(rank, key=lambda x: -x[1]):
        print(f"    {c:16s} {s:7.3f}")

    print("\n=== CUMULATIVE CEILING, percent of employment ===")
    print((ok.groupby("reinstatement")["cumulative_ceiling"].describe(
        percentiles=[.05, .5, .95])[["5%", "50%", "95%"]] * 100).round(2).to_string())

    (OUT / "reinstatement_summary.json").write_text(json.dumps({
        "source": "Acemoglu and Restrepo, Journal of Economic Perspectives 33(2), 2019",
        "rates": REINSTATEMENT,
        "median_speed_limit_pct_by_setting": {
            k: float(v * 100) for k, v in
            ok.groupby("reinstatement")["speed_limit"].median().items()},
        "variance_share_by_dimension": {c: float(s) for c, s in rank},
        "FROZEN": "The labour model is frozen after this run. It is an appendix scenario "
                  "generator: it produces doses for the dose-response table and nothing "
                  "else. No result in the body of the paper depends on its parameters.",
    }, indent=2, default=str))
    print("\n=== THE LABOUR MODEL IS NOW FROZEN ===")
    print("  It is an appendix scenario generator and nothing else. No result in the body "
          "of the\n  paper depends on its parameters, and no later session reopens them.")


if __name__ == "__main__":
    main()
