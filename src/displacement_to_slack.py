"""Item 4: map displacement to unemployment, hence to rho, as a fixed point.

The frontier needs rho at each displacement level, and rho depends on slack (A49), and slack
depends on how many displaced workers fail to find work, which depends on rho. That is a
fixed point and it is solved here rather than assumed.

THE EXIT SHARE, AND WHY IT IS NOT TAKEN FROM ACEMOGLU AND RESTREPO

The brief suggested sourcing the share exiting the labour force from Acemoglu and Restrepo's
finding that roughly three quarters of the nonemployment response was nonparticipation.
**That statement could not be verified.** The NBER working paper version of "Robots and Jobs"
was retrieved and searched in full: it contains no such decomposition, the relevant
unemployment and participation results sit in Table A4 of an online appendix that is not in
the paper, and the strings "nonparticipation", "not in the labor force" and "exit the labor
force" do not appear. It is recorded in lit/unverified.md and is NOT used.

The Displaced Worker Survey measures the same quantity directly, on exactly the population
in question, and is used instead. Each release reports the employed, unemployed and
not-in-the-labour-force shares of long-tenured displaced workers at the survey date, so

    exit share = NILF / (unemployed + NILF)

is read straight off the table for ten vintages.

THE RESULT RUNS AGAINST THE SUGGESTED ASSUMPTION. The exit share is not three quarters and
it is not constant: it falls sharply when the labour market is slack, from about 0.64 in
January 2022 to 0.30 in January 2010. Displaced workers stay in the labour force and search
when jobs are scarce. That means a large displacement shock produces MORE measured
unemployment per nonemployed worker, not less, which feeds back into a lower rho. The
feedback is therefore stronger than a fixed high exit share would imply.

THE FIXED POINT

    D            = d * E0                      workers displaced
    rho(u)       = 0.8090 - 0.0304 * u         A49, u in percent
    e(u)         = fitted exit share, bounded to the observed range
    delta U      = D * (1 - rho) * (1 - e)
    delta LF     = -D * (1 - rho) * e
    u_new        = 100 * (U0 + delta U) / (LF0 + delta LF)

iterated to convergence. Baseline U0, LF0 and E0 are the January 2026 CPS levels from FRED.

OUTSIDE THE DATA. The rho fit covers unemployment from 3.6 to 9.8 percent. Beyond 9.8 the
module reports a BAND rather than a point: the lower edge holds rho flat at the minimum
observed value (0.49), the upper edge extrapolates the fitted line. Every figure beyond 9.8
percent is labelled as outside the data and neither edge is presented as an estimate.

COMOVEMENT OF rho AND omega. The DWS releases do not publish the Table 7 earnings
distribution in a form this project has parsed for vintages before 2026, so the comovement of
omega with slack cannot be estimated here. The assumption made instead is stated: omega is
held CONSTANT across displacement levels in the central case, which is CONSERVATIVE in the
direction that matters, because Huckfeldt (2022) finds the cost and incidence of occupation
displacement are higher in recessions, so the true omega in slack states is lower than the
one used and the results below understate the deterioration.
"""
import io, json, pathlib, re, urllib.request
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"
UA = "physical-ai-research/1.0 (team@oviguide.in)"
ARCH = "https://www.bls.gov/news.release/archives/"
INDEX = "https://www.bls.gov/bls/news-release/home.htm"


def get(u, t=60):
    return urllib.request.urlopen(
        urllib.request.Request(u, headers={"User-Agent": UA}), timeout=t
    ).read().decode("utf-8", "replace")


def strip_tags(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", h)


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


def scrape_status():
    """employed / unemployed / not-in-labour-force percent for each archived vintage."""
    idx = get(INDEX)
    files = sorted(set(re.findall(r"(disp_\d{8}\.htm)", idx)))
    rows = []
    for f in files:
        t = strip_tags(get(ARCH + f))
        yr = f[9:13]
        rec = {"release_file": f, "survey_year": int(yr), "survey_month": f"{yr}-01"}
        # preferred: the Table 1 total row
        m = re.search(r"Total,?\s*(?:20|16)?\s*years and over[.\s]*([\d,]+)\s+100\.0\s+"
                      r"([\d.]+)\s+([\d.]+)\s+([\d.]+)", t)
        if m:
            rec.update({"total_thousands": float(m.group(1).replace(",", "")),
                        "pct_employed": float(m.group(2)),
                        "pct_unemployed": float(m.group(3)),
                        "pct_nilf": float(m.group(4)), "source": "table 1 total row"})
        else:
            # fall back to the summary sentences
            a = re.search(r"proportion unemployed[^.]{0,80}?was\s+([\d.]+)\s*percent", t, re.I)
            b = re.search(r"([\d.]+)\s*percent of long-tenured displaced workers were not in "
                          r"the labor force", t, re.I)
            c = re.search(r"([\d.]+)\s*percent[^.]{0,60}?\breemployed\b", t, re.I)
            if a and b:
                rec.update({"pct_unemployed": float(a.group(1)),
                            "pct_nilf": float(b.group(1)),
                            "pct_employed": float(c.group(1)) if c else np.nan,
                            "source": "summary text"})
            else:
                w = re.search(r"(Twenty-two|Eighteen|Twenty|Nineteen|Seventeen|Sixteen|Fifteen)"
                              r"\s*percent of long-tenured displaced workers were not in the "
                              r"labor force", t, re.I)
                words = {"fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
                         "nineteen": 19, "twenty": 20, "twenty-two": 22}
                if a and w:
                    rec.update({"pct_unemployed": float(a.group(1)),
                                "pct_nilf": float(words[w.group(1).lower()]),
                                "pct_employed": float(c.group(1)) if c else np.nan,
                                "source": "summary text, word form"})
        if "pct_nilf" in rec:
            rec["exit_share"] = rec["pct_nilf"] / (rec["pct_unemployed"] + rec["pct_nilf"])
            rows.append(rec)
    return pd.DataFrame(rows)


def main():
    S = scrape_status()
    u = fred("UNRATE")
    S["survey_unrate"] = [float(u.get(pd.Timestamp(m + "-01"), np.nan))
                          for m in S["survey_month"]]
    S = S.sort_values("survey_year").reset_index(drop=True)
    S.round(4).to_csv(OUT / "dws_labour_force_status.csv", index=False)

    v = S.dropna(subset=["exit_share", "survey_unrate"])
    be1, be0 = np.polyfit(v["survey_unrate"], v["exit_share"], 1)
    resid = v["exit_share"] - (be0 + be1 * v["survey_unrate"])
    r2e = 1 - float((resid ** 2).sum()) / float(((v["exit_share"] - v["exit_share"].mean()) ** 2).sum())

    # rho fit from A49
    RH = json.loads((OUT / "bls_dws_vintages.json").read_text())["fit_rho_on_unrate"]
    b0, b1 = RH["intercept"], RH["slope_per_pp_unrate"]
    U_MAX_OBS, RHO_MIN_OBS = RH["unrate_range"][1], RH["rho_range"][0]

    # January 2026 baseline levels
    lf = float(fred("CLF16OV").asof(pd.Timestamp("2026-01-01")))
    un = float(fred("UNEMPLOY").asof(pd.Timestamp("2026-01-01")))
    emp = lf - un
    u0 = 100 * un / lf

    def solve(d, mode):
        uu = u0
        for _ in range(200):
            if mode == "fit":
                rho = b0 + b1 * uu
            elif mode == "flat_beyond":
                rho = b0 + b1 * min(uu, U_MAX_OBS)
                rho = max(rho, RHO_MIN_OBS)
            else:
                rho = b0 + b1 * uu
            rho = float(np.clip(rho, 0.0, 1.0))
            e = float(np.clip(be0 + be1 * uu, v["exit_share"].min(), v["exit_share"].max()))
            D = d * emp
            dU = D * (1 - rho) * (1 - e)
            dLF = -D * (1 - rho) * e
            nu = 100 * (un + dU) / (lf + dLF)
            if abs(nu - uu) < 1e-9:
                uu = nu
                break
            uu = 0.5 * uu + 0.5 * nu
        return uu, rho, e

    rows = []
    for d in [0.00, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90]:
        uf, rf, ef = solve(d, "fit")
        ub, rb, eb = solve(d, "flat_beyond")
        rows.append({"displacement": d, "unrate_fit": uf, "rho_fit_extrapolated": rf,
                     "rho_flat_floor": rb, "exit_share": ef,
                     "outside_data": uf > U_MAX_OBS})
    F = pd.DataFrame(rows)
    F.round(5).to_csv(OUT / "displacement_to_slack.csv", index=False)
    (OUT / "displacement_to_slack.json").write_text(json.dumps({
        "baseline_jan2026": {"labour_force": lf, "unemployed": un, "employed": emp,
                             "unrate": u0},
        "exit_share_fit": {"intercept": float(be0), "slope_per_pp_unrate": float(be1),
                           "r_squared": float(r2e), "n": int(len(v)),
                           "observed_range": [float(v["exit_share"].min()),
                                              float(v["exit_share"].max())]},
        "rho_fit": RH,
        "rho_valid_to_unrate": U_MAX_OBS,
        "acemoglu_restrepo_three_quarters": "NOT VERIFIED, NOT USED. See lit/unverified.md.",
        "omega_comovement": "NOT estimable from published vintages; omega held constant, "
                            "which understates deterioration per Huckfeldt (2022).",
    }, indent=2))

    pd.set_option("display.width", 220)
    print("=== DWS labour force status of displaced workers, by vintage ===")
    print(S[["survey_year", "pct_employed", "pct_unemployed", "pct_nilf",
             "exit_share", "survey_unrate", "source"]].round(4).to_string(index=False))
    print(f"\n  exit share = NILF / (unemployed + NILF)")
    print(f"  fit: exit = {be0:.4f} + ({be1:.4f}) x unrate,  R2 = {r2e:.3f}, n = {len(v)}")
    print(f"  observed range {v['exit_share'].min():.3f} to {v['exit_share'].max():.3f}")
    print(f"  NOTE: the exit share FALLS with slack, the opposite of a fixed high-exit "
          f"assumption.")
    print(f"\n=== baseline January 2026: labour force {lf/1000:.1f}m, "
          f"unemployed {un/1000:.1f}m, u = {u0:.2f}% ===")
    print("\n=== displacement to slack, fixed point ===")
    print(F.round(4).to_string(index=False))
    print(f"\n  rho fit is valid to unrate {U_MAX_OBS}; rows flagged outside_data are "
          f"extrapolations and the band between rho_fit_extrapolated and rho_flat_floor is "
          f"the honest range there.")


if __name__ == "__main__":
    main()
