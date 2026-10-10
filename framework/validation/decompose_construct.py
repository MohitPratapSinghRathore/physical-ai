"""
The decisive construct test, and episode characterisation.

Part A. Does the labour backing coefficient vector add anything over a plain
        interaction of the household share of the book with the county wage
        share? If R2 is ~1, the accounts are doing no work in this construct.

Part B. Size and geographic spread of the wage-income shock in each candidate
        episode, from BEA county personal income by source. These are TREATMENT
        variables, not outcomes: no bank loss, delinquency or failure series is
        touched anywhere in this session.
"""
from pathlib import Path
import numpy as np
import numpy.linalg as la
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"


def r2(y, X):
    X = np.column_stack([np.ones(len(X))] + [np.asarray(c, float) for c in X.T])
    bh, *_ = la.lstsq(X, y, rcond=None)
    return 1 - ((y - X @ bh) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def part_a():
    p = pd.read_csv(RAW / "preshock_panel_2014.csv").dropna(
        subset=["lb_bank", "geo_wage_share"])
    y = p["lb_bank"].to_numpy()
    comp = ["sh_resre", "sh_consumer", "sh_cre", "sh_constr", "sh_ci",
            "sh_ag", "sh_sec"]
    C = p[comp].fillna(0).to_numpy()
    w = p["geo_wage_share"].to_numpy()[:, None]

    models = {
        "loan composition only": C,
        "county wage share only": w,
        "composition + wage share, additive": np.hstack([C, w]),
        "composition + wage share + interactions": np.hstack([C, w, C * w]),
        "household share x wage share, two terms only": np.hstack([
            p[["sh_household"]].to_numpy(), w]),
        "household share x wage share, with interaction": np.hstack([
            p[["sh_household"]].to_numpy(), w,
            p[["sh_household"]].to_numpy() * w]),
    }
    rows = [{"model": k, "R2_explaining_lb_bank": r2(y, X)}
            for k, X in models.items()]
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "construct_decomposition.csv", index=False)
    print("PART A. What explains bank labour backing, pre-shock 2014\n")
    print(df.to_string(index=False))
    return df


def part_b():
    bea = pd.read_csv(RAW / "bea_cainc4_all_areas.csv", dtype=str)
    bea["GeoFIPS"] = bea["GeoFIPS"].str.strip().str.replace('"', "", regex=False)
    yrs = [str(y) for y in range(1998, 2024)]
    keep = bea[bea["LineCode"].isin(["10", "50"])].copy()
    for y in yrs:
        keep[y] = pd.to_numeric(keep[y], errors="coerce")
    wide = keep.pivot_table(index="GeoFIPS", columns="LineCode",
                            values=yrs, aggfunc="first")
    wage = wide.xs("50", axis=1, level=1)
    pi = wide.xs("10", axis=1, level=1)
    cty = ~wage.index.str.endswith("000")
    wage, pi = wage[cty], pi[cty]

    episodes = {
        "2001 recession": ("2000", "2002"),
        "2007-2010 financial crisis": ("2007", "2010"),
        "2014-2016 oil collapse": ("2014", "2016"),
        "2020 pandemic": ("2019", "2020"),
    }
    rows = []
    for name, (t0, t1) in episodes.items():
        base = pi[t0]
        d = (wage[t1] - wage[t0]) / base          # wage bill change over income
        d = d.replace([np.inf, -np.inf], np.nan).dropna()
        # real terms, deflated by the national wage bill growth, to isolate
        # the cross-sectional (relocatable) component
        nat = (wage[t1].sum() - wage[t0].sum()) / pi[t0].sum()
        rel = d - nat
        rows.append({
            "episode": name,
            "window": f"{t0}-{t1}",
            "n_counties": int(d.shape[0]),
            "national_wage_bill_change_pct_of_income": round(100 * nat, 2),
            "county_sd_pct": round(100 * d.std(), 2),
            "p10_pct": round(100 * d.quantile(.10), 2),
            "p50_pct": round(100 * d.quantile(.50), 2),
            "p90_pct": round(100 * d.quantile(.90), 2),
            "share_counties_negative": round(float((d < 0).mean()), 3),
            "share_counties_below_minus_2pct_relative": round(
                float((rel < -0.02).mean()), 3),
            "cross_sectional_sd_rel_pct": round(100 * rel.std(), 2),
        })
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "episode_shock_spread.csv", index=False)
    print("\n\nPART B. Wage-bill shock, size and spread, by candidate episode")
    print("(change in county wage bill over base-year personal income)\n")
    print(df.to_string(index=False))
    return df


if __name__ == "__main__":
    part_a()
    part_b()
