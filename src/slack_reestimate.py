"""Item 1: repair the outcome measure and the circularity in the stock-flow model.

THE PROBLEM, and it is a real defect in A56 and A61.

The stock-flow model lets unemployed workers leave the labour force at hazard a(u). Exit
removes them from BOTH the numerator and the denominator of the unemployment rate, so the
model can hold unemployment down by pushing people out of the labour force entirely. The
reemployment hazard is then driven by that same suppressed unemployment rate through
rho(u) = 0.8090 - 0.0304 u, which rewards the model for the exits.

That is circular, and the direction of the bias is knowable in advance: exits suppress u,
suppressed u raises rho, higher rho drains the unemployment stock faster, which suppresses u
further. **The speed limit and the cumulative ceiling in A56 and A61 are therefore too
generous, and the unemployment paths in A62 are too flat.**

Exit to nonparticipation is also not a benign outcome. A displaced worker who stops looking
has lost their wage income just as completely as one who is counted unemployed. Reporting
unemployment as the headline measures the wrong thing.

THE REPAIR, in two parts.

1. OUTCOME MEASURES. Every scenario now reports, in this order:
     employment to population ratio
     cumulative share of displaced workers never reemployed
     aggregate wage income relative to baseline
     unemployment, LAST
   Unemployment is kept because supervisors use it, not because it is the right measure here.

2. SLACK MEASURE. rho is re-estimated on a slack measure that COUNTS exits, so the feedback
   loop cannot be gamed by pushing people out of the labour force. Two candidates, both
   re-fitted on the same fourteen DWS vintages:
     nonemployment rate  = 1 - employment/population, 16 and over
     E/P gap             = employment/population at the vintage minus its sample maximum
   Whichever fits better on the vintages is used, and both are reported.

CONSISTENCY CHECK. For every scenario the model's REALISED reemployment share among the
displaced is compared with the rho implied by the model's own slack at that point. If the
realised share materially exceeds the implied rho, the circularity is still operating.
"""
import io, json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"


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


def fit(x, y):
    n = len(x)
    b1, b0 = np.polyfit(x, y, 1)
    yh = b0 + b1 * x
    ss = float(((y - yh) ** 2).sum())
    se = float(np.sqrt(ss / (n - 2) / ((x - x.mean()) ** 2).sum()))
    r2 = 1 - ss / float(((y - y.mean()) ** 2).sum())
    return {"intercept": float(b0), "slope": float(b1), "slope_se": se,
            "t": float(b1 / se) if se else np.nan, "r_squared": float(r2), "n": n,
            "x_range": [float(x.min()), float(x.max())],
            "y_range": [float(y.min()), float(y.max())]}


def main():
    V = pd.read_csv(OUT / "bls_dws_vintages.csv").dropna(subset=["rho"]).copy()
    V["survey_month"] = V["release_date"].str[:4] + "-01-01"
    ep = fred("EMRATIO")          # employment-population ratio, 16 and over, percent
    # PRIME AGE, 25 to 54. The 16-and-over ratio falls secularly as the population ages, so
    # it conflates demographics with slack and its observed range is only about one point
    # wide at the vintage dates. The prime-age rate strips the demographic trend and is the
    # standard fix. Both are fitted and reported.
    pa = fred("LREM25TTUSM156S")
    unr = fred("UNRATE")
    V["ep_ratio"] = [float(ep.asof(pd.Timestamp(m))) for m in V["survey_month"]]
    V["nonemployment_rate"] = 100.0 - V["ep_ratio"]
    V["prime_ep"] = [float(pa.asof(pd.Timestamp(m))) for m in V["survey_month"]]
    V["prime_nonemployment"] = 100.0 - V["prime_ep"]
    V["unrate"] = [float(unr.asof(pd.Timestamp(m))) for m in V["survey_month"]]
    ep_max = float(V["ep_ratio"].max())
    V["ep_gap"] = ep_max - V["ep_ratio"]

    fits = {
        "rho_on_unrate_ORIGINAL": fit(V["unrate"].to_numpy(float), V["rho"].to_numpy(float)),
        "rho_on_nonemployment": fit(V["nonemployment_rate"].to_numpy(float),
                                    V["rho"].to_numpy(float)),
        "rho_on_ep_gap": fit(V["ep_gap"].to_numpy(float), V["rho"].to_numpy(float)),
        "rho_on_PRIME_AGE_nonemployment": fit(V["prime_nonemployment"].to_numpy(float),
                                              V["rho"].to_numpy(float)),
    }
    # exit share on the same measures
    S = pd.read_csv(OUT / "dws_labour_force_status.csv")
    S["survey_month"] = S["survey_month"].astype(str) + "-01"
    S["ep_ratio"] = [float(ep.asof(pd.Timestamp(m))) for m in S["survey_month"]]
    S["nonemployment_rate"] = 100.0 - S["ep_ratio"]
    S["ep_gap"] = ep_max - S["ep_ratio"]
    e = S.dropna(subset=["exit_share"])
    fits["exit_on_nonemployment"] = fit(e["nonemployment_rate"].to_numpy(float),
                                        e["exit_share"].to_numpy(float))
    fits["exit_on_ep_gap"] = fit(e["ep_gap"].to_numpy(float),
                                 e["exit_share"].to_numpy(float))

    best = max(["rho_on_nonemployment", "rho_on_ep_gap",
                "rho_on_PRIME_AGE_nonemployment"],
               key=lambda k: fits[k]["r_squared"])
    out = {"vintages": V[["release_date", "rho", "unrate", "ep_ratio",
                          "nonemployment_rate", "ep_gap"]].round(4).to_dict("records"),
           "fits": fits, "ep_max_in_sample": ep_max,
           "chosen_slack_measure": best,
           "why": "rho is re-estimated on a slack measure that counts exits, so the model "
                  "cannot suppress measured slack by pushing workers out of the labour "
                  "force and be rewarded with a higher reemployment hazard."}
    V.round(4).to_csv(OUT / "slack_vintages.csv", index=False)
    (OUT / "slack_reestimate.json").write_text(json.dumps(out, indent=2))

    pd.set_option("display.width", 220)
    print("=== DWS vintages with slack measures that count exits ===")
    print(V[["release_date", "rho", "unrate", "ep_ratio", "nonemployment_rate",
             "prime_ep", "prime_nonemployment"]].round(3).to_string(index=False))
    print(f"\n  sample maximum employment to population ratio: {ep_max:.2f} percent")

    print("\n=== FITS ===")
    for k, f in fits.items():
        print(f"\n  {k}")
        print(f"    y = {f['intercept']:.4f} + ({f['slope']:.4f}) x    "
              f"se {f['slope_se']:.4f}, t = {f['t']:.2f}, R2 = {f['r_squared']:.3f}, "
              f"n = {f['n']}")
        print(f"    x observed {f['x_range'][0]:.2f} to {f['x_range'][1]:.2f}, "
              f"y observed {f['y_range'][0]:.3f} to {f['y_range'][1]:.3f}")

    print(f"\n=== CHOSEN: {best} ===")
    fb = fits[best]
    fo = fits["rho_on_unrate_ORIGINAL"]
    print(f"  R2 {fb['r_squared']:.3f} against {fo['r_squared']:.3f} for the original "
          f"unemployment-rate fit")
    print(f"  the original fit is RETAINED for reporting unemployment, and the new fit "
          f"DRIVES the hazard")


if __name__ == "__main__":
    main()
