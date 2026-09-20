"""Item 4: the slack measure preference, tested on windows rather than asserted.

The replication brief version 1 said that fitting rho on the unemployment rate is circular
and "gives a higher R squared and a speed limit about 2.5 times larger, and it is wrong".
The replicator replied that the higher-R-squared remark is "true only on a post-2008
window". This module was written to record that window restriction.

IT DOES NOT HOLD, AND THE RECORD IS THE OPPOSITE OF WHAT WAS EXPECTED. The unemployment
rate has the higher R squared on BOTH windows, and its advantage is LARGER post-2008, not
smaller: 0.940 against 0.732 on 2010 to 2026, against 0.812 against 0.773 on the full
sample. There is no window on which prime-age nonemployment wins on fit.

So the preference for prime-age nonemployment is a preference on MECHANISM alone, and it
has to be defended that way every time it is stated. The mechanism argument is unaffected
and still stands on its own: displacement raises unemployment, workers who exit the labour
force leave the unemployment rate unchanged, and those are exactly the workers who did not
get reemployed, so the unemployment rate cannot measure the slack a reemployment hazard
responds to. Selecting the specification on fit would select the circular one, and the
post-2008 result says it would do so MORE strongly as exits became more important, which is
what a circularity should look like.

The "2.5 times larger speed limit" claim is separately NOT SUPPORTED: the slope ratio is
1.107 on the full sample and 1.096 post-2008.

x for the prime-age specification is 100 minus the OECD prime-age 25 to 54 employment to
population ratio (FRED LREM25TTUSM156S) taken AS OF each DWS survey month.
x for the unemployment specification is the survey-month unemployment rate carried in
data/processed/bls_dws_vintages.csv.
y is the percent of long-tenured displaced workers employed at the survey date, DWS Table 1
total row, all ages.

The full-sample fits this module produces reproduce the project's own stored fits to five
decimal places, which is what makes the window comparison trustworthy.
"""
import json
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

WINDOWS = {"full sample, 2000 to 2026": 2000, "post-2008, 2010 to 2026": 2010}


def fit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    b, a = np.polyfit(x, y, 1)
    pred = a + b * x
    ss_res = float(((y - pred) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return {"intercept": a, "slope": b, "r_squared": 1 - ss_res / ss_tot, "n": len(x)}


def prime_age_nonemployment():
    """100 minus the prime-age employment to population ratio, taken AS OF each survey
    month. `asof` and not a strict January lookup, because the OECD series lags: at the
    January 2026 survey month the latest observation is 2025-09, which is where the
    published prime-age nonemployment rate of 19.31 comes from. A strict January rule drops
    the 2026 vintage and gives n = 13."""
    d = pd.read_csv(RAW / "fred" / "LREM25TTUSM156S.csv")
    d.columns = ["date", "v"]
    d["date"] = pd.to_datetime(d["date"])
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    return d.dropna().set_index("date")["v"].sort_index()


def main():
    V = pd.read_csv(OUT / "bls_dws_vintages.csv")
    V["year"] = V["survey_month"].str.slice(0, 4).astype(int)
    pa = prime_age_nonemployment()
    V["x_prime_age"] = [100.0 - float(pa.asof(pd.Timestamp(m)))
                        for m in V["survey_month"]]
    V = V.dropna(subset=["x_prime_age", "survey_unrate", "rho"])

    print("=== ITEM 4: THE SLACK MEASURE, TESTED ON WINDOWS ===")
    print("  y = share of long-tenured displaced workers employed at the survey date\n")
    rows = []
    for label, start in WINDOWS.items():
        W = V[V["year"] >= start]
        fp = fit(W["x_prime_age"], W["rho"])
        fu = fit(W["survey_unrate"], W["rho"])
        winner = ("prime-age nonemployment" if fp["r_squared"] > fu["r_squared"]
                  else "the unemployment rate")
        print(f"  {label}  (n = {fp['n']})")
        print(f"    rho on prime-age nonemployment  intercept {fp['intercept']:8.5f}  "
              f"slope {fp['slope']:9.5f}  R2 {fp['r_squared']:.5f}")
        print(f"    rho on the unemployment rate    intercept {fu['intercept']:8.5f}  "
              f"slope {fu['slope']:9.5f}  R2 {fu['r_squared']:.5f}")
        print(f"    better fit: {winner}")
        print(f"    slope ratio, unemployment over prime-age: "
              f"{abs(fu['slope'] / fp['slope']):.3f}\n")
        rows.append({"window": label, "n": fp["n"],
                     "prime_age_r_squared": fp["r_squared"],
                     "unrate_r_squared": fu["r_squared"],
                     "better_fit": winner,
                     "slope_ratio_unrate_over_prime_age":
                         abs(fu["slope"] / fp["slope"]),
                     "prime_age_intercept": fp["intercept"],
                     "prime_age_slope": fp["slope"],
                     "unrate_intercept": fu["intercept"], "unrate_slope": fu["slope"]})
    R = pd.DataFrame(rows)
    R.round(6).to_csv(OUT / "slack_window_check.csv", index=False)

    full = R.iloc[0]
    post = R.iloc[1]
    verdict = (
        "The preference for prime-age nonemployment over the unemployment rate is a "
        "preference on MECHANISM. On FIT it holds only on the post-2008 window: on the full "
        f"sample the unemployment rate fits better ({full.unrate_r_squared:.5f} against "
        f"{full.prime_age_r_squared:.5f}), and on the post-2008 window prime-age "
        f"nonemployment fits better ({post.prime_age_r_squared:.5f} against "
        f"{post.unrate_r_squared:.5f})."
        if full.better_fit != post.better_fit else
        f"Both windows select {post.better_fit} on fit. The expected post-2008 restriction "
        f"does NOT hold: the unemployment rate's advantage is LARGER post-2008 "
        f"({post.unrate_r_squared:.5f} against {post.prime_age_r_squared:.5f}) than on the "
        f"full sample ({full.unrate_r_squared:.5f} against "
        f"{full.prime_age_r_squared:.5f}). The preference for prime-age nonemployment rests "
        f"on MECHANISM alone and must be defended that way wherever it is stated.")
    print("=== VERDICT ===")
    print("  " + verdict.replace(". ", ".\n  "))
    print(f"\n  The version-1 claim that the circular fit gives a speed limit 'about 2.5 "
          f"times larger'\n  is not supported: the slope ratio is "
          f"{full.slope_ratio_unrate_over_prime_age:.3f} on the full sample and "
          f"{post.slope_ratio_unrate_over_prime_age:.3f} post-2008.")
    (OUT / "slack_window_check.json").write_text(json.dumps(
        {"windows": rows, "verdict": verdict,
         "speed_limit_2.5x_claim": "NOT SUPPORTED, withdrawn"}, indent=2))


if __name__ == "__main__":
    main()
