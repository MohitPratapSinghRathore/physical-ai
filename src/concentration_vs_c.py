"""Item 4: concentration of the at-risk RATE as a function of c, and the tradable split.

REGISTERED HYPOTHESIS, recorded by the owner before this was run:
    geographic concentration of the at-risk RATE declines as c rises, because exposure
    shifts from tradable manufacturing to nontradable local services.

Two parts.

(a) Concentration of the at-risk RATE (not dollars) across PUMAs and counties, at each c:
    Gini and the p90/p10 ratio. Rates, so area size does not drive the statistic.

(b) Tradable versus nontradable split of the embodiment-weighted wage bill at risk at each c.
    Classification is a documented sector rule, NOT Mian and Sufi's import/export-per-worker
    measure. Mian, A. and Sufi, A. (2014), "What Explains the 2007-2009 Drop in Employment?",
    Econometrica 82(6), is the methodological precedent for splitting local labour demand
    into tradable and nontradable; the rule applied here is a coarser NAICS sector
    assignment and is labelled as such rather than attributed to them.

        tradable     NAICS 11 agriculture, 21 mining, 31-33 manufacturing
        nontradable  44-45 retail, 61 education, 62 health care, 71 arts and recreation,
                     72 accommodation and food, 81 other services
        mixed        everything else (construction, utilities, wholesale, transport,
                     information, finance, real estate, professional, management,
                     administrative, public administration)

Benchmark for magnitude, from Acemoglu and Restrepo (2020), Journal of Political Economy
128(6): their commuting-zone exposure to robots has an interquartile range of about 1 robot
per thousand workers (Pittsburgh at p75 against Omaha at p25) and a p1 to p99 range of about
9 (West Palm Beach against Detroit). That is roughly a ninefold spread between the extreme
percentiles of their exposure measure.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

TRADABLE = {"11", "21", "31", "32", "33"}
NONTRADABLE = {"44", "45", "61", "62", "71", "72", "81"}


def gini(x, w=None):
    x = np.asarray(x, float)
    m = np.isfinite(x) & (x >= 0)
    x = x[m]
    if len(x) < 2 or x.sum() == 0:
        return np.nan
    xs = np.sort(x)
    n = len(xs)
    return float((n + 1 - 2 * np.sum(np.cumsum(xs)) / np.cumsum(xs)[-1]) / n)


def p_ratio(x, lo=10, hi=90):
    x = np.asarray(x, float)
    x = x[np.isfinite(x) & (x > 0)]
    if len(x) < 20:
        return np.nan
    a, b = np.percentile(x, lo), np.percentile(x, hi)
    return float(b / a) if a > 0 else np.nan


def main():
    res = {}

    # ---------------- (a) concentration of the at-risk RATE ----------------
    D = pd.read_csv(OUT / "dar_geo_puma.csv")
    C = pd.read_csv(OUT / "dar_geo_county.csv", dtype={"county_fips": str})
    C["wage_at_risk_share"] = C["wage_at_risk"] / C["wage_bill"].replace(0, np.nan)
    C["mortgage_at_risk_share"] = C["mortgage_at_risk"] / C["mortgage_total"].replace(0, np.nan)
    C["rent_at_risk_share"] = C["rent_at_risk"] / C["rent_total"].replace(0, np.nan)

    rows = []
    for lvl, df in [("PUMA", D), ("county", C)]:
        for c in sorted(df["c"].unique()):
            d = df[df["c"] == c]
            for metric in ["wage_at_risk_share", "mortgage_at_risk_share",
                           "rent_at_risk_share"]:
                v = d[metric].replace([np.inf, -np.inf], np.nan).dropna()
                rows.append({"level": lvl, "c": c, "metric": metric,
                             "n_areas": int(len(v)),
                             "gini_of_rate": gini(v),
                             "p90_p10_ratio": p_ratio(v),
                             "p10": float(np.percentile(v, 10)) if len(v) > 20 else np.nan,
                             "p50": float(np.percentile(v, 50)) if len(v) > 20 else np.nan,
                             "p90": float(np.percentile(v, 90)) if len(v) > 20 else np.nan})
    A = pd.DataFrame(rows)
    A.round(5).to_csv(OUT / "concentration_of_rate_vs_c.csv", index=False)

    # hypothesis test: does the Gini of the rate fall as c rises?
    hyp = {}
    for lvl in ["PUMA", "county"]:
        for metric in ["wage_at_risk_share", "mortgage_at_risk_share"]:
            s = A[(A["level"] == lvl) & (A["metric"] == metric) & (A["c"] > 0)]
            s = s.sort_values("c")
            if len(s) >= 3:
                slope = float(np.polyfit(s["c"], s["gini_of_rate"], 1)[0])
                hyp[f"{lvl}_{metric}"] = {
                    "gini_at_lowest_c": float(s["gini_of_rate"].iloc[0]),
                    "gini_at_c1": float(s["gini_of_rate"].iloc[-1]),
                    "slope_gini_on_c": slope,
                    "direction": "DECLINES (hypothesis supported)" if slope < 0
                                 else "RISES (hypothesis contradicted)"}
    res["a_concentration"] = hyp

    # ---------------- (b) tradable split of wage bill at risk ----------------
    pan = pd.read_csv(OUT / "within_industry_s_panel.csv")
    naics_cols = [c for c in pan.columns if c.isdigit() and len(c) == 2]
    pan["trad_share"] = pan[[c for c in naics_cols if c in TRADABLE]].sum(axis=1)
    pan["nontrad_share"] = pan[[c for c in naics_cols if c in NONTRADABLE]].sum(axis=1)
    pan["mixed_share"] = 1.0 - pan["trad_share"] - pan["nontrad_share"]

    grid = pd.read_csv(OUT / "paei_c.csv")
    g = grid.merge(pan[["occp", "trad_share", "nontrad_share", "mixed_share"]],
                   on="occp", how="inner")
    g = g[g["wage_bill"].notna() & (g["wage_bill"] > 0)]

    rows = []
    for c in sorted(g["c"].unique()):
        d = g[g["c"] == c]
        risk = d["wage_bill"] * d["embodiment_P"] * d["exposed_threshold_rank"]
        tot = float(risk.sum())
        if tot <= 0:
            continue
        rows.append({"c": c, "wagebill_at_risk_usd_bn": tot / 1e9,
                     "tradable_pct": 100 * float((risk * d["trad_share"]).sum()) / tot,
                     "nontradable_pct": 100 * float((risk * d["nontrad_share"]).sum()) / tot,
                     "mixed_pct": 100 * float((risk * d["mixed_share"]).sum()) / tot})
    B = pd.DataFrame(rows)
    B.round(3).to_csv(OUT / "tradable_split_vs_c.csv", index=False)
    if len(B) >= 3:
        res["b_tradable"] = {
            "tradable_pct_at_c0.2": float(B.loc[np.isclose(B["c"], 0.2), "tradable_pct"].iloc[0]),
            "tradable_pct_at_c1.0": float(B.loc[np.isclose(B["c"], 1.0), "tradable_pct"].iloc[0]),
            "slope_tradable_on_c": float(np.polyfit(B["c"], B["tradable_pct"], 1)[0]),
        }

    res["ar_benchmark"] = {
        "source": "Acemoglu and Restrepo (2020) JPE 128(6)",
        "iqr_robots_per_thousand": 1.0,
        "p1_to_p99_robots_per_thousand": 9.0,
        "note": "roughly a ninefold spread between extreme percentiles of their exposure",
    }
    (OUT / "concentration_vs_c_summary.json").write_text(json.dumps(res, indent=2))

    pd.set_option("display.width", 220)
    print("=== (a) concentration of the AT-RISK RATE, county level ===")
    print(A[(A["level"] == "county") & (A["c"] > 0)]
          [["c", "metric", "n_areas", "gini_of_rate", "p90_p10_ratio", "p10", "p90"]]
          .round(4).to_string(index=False))
    print("\n=== (a) same, PUMA level ===")
    print(A[(A["level"] == "PUMA") & (A["c"] > 0)]
          [["c", "metric", "gini_of_rate", "p90_p10_ratio"]].round(4).to_string(index=False))
    print("\n=== HYPOTHESIS TEST: does the Gini of the rate fall as c rises? ===")
    for k, v in hyp.items():
        print(f"  {k:36s} gini {v['gini_at_lowest_c']:.4f} -> {v['gini_at_c1']:.4f}  "
              f"slope {v['slope_gini_on_c']:+.4f}  {v['direction']}")
    print("\n=== (b) tradable vs nontradable split of wage bill at risk ===")
    print(B.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
