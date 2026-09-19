"""Item 3: rho across every reachable Displaced Worker Survey vintage, against labour slack.

The engine and the P1r condition both take rho, the share of displaced workers employed at
the survey date. One vintage is a point estimate in one labour market. The frontier needs
rho as a FUNCTION of slack, and the only way to get that without inventing a functional form
is to read it off the historical vintages.

SOURCE. BLS Worker Displacement news releases, biennial, read directly from bls.gov with the
declared User-Agent. The BLS archived-news-release index lists releases back to 2008 only;
pre-2008 vintages are attempted at the historical text-file path and every failure is
recorded by name rather than silently dropped.

EXTRACTION. From each release, the total number of long-tenured displaced workers and the
number employed at the survey date, taken from the summary paragraph, which states both in
a fixed form. rho = employed / total. Where the summary states only a percentage, that
percentage is used and the fact is recorded.

SLACK. Civilian unemployment rate (UNRATE, FRED) in the survey month, which is January of
the release year for every vintage.

The fitted relationship is deliberately the simplest defensible one: an ordinary least
squares line of rho on the survey-month unemployment rate, reported with its slope, its
standard error, its R-squared and the full scatter. No functional form is imposed beyond
linearity and none is extrapolated outside the observed range without saying so.
"""
import io, json, pathlib, re, time, urllib.request
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
UA = "physical-ai-research/1.0 (team@oviguide.in)"
INDEX = "https://www.bls.gov/bls/news-release/home.htm"
ARCH = "https://www.bls.gov/news.release/archives/"
CURRENT = "https://www.bls.gov/news.release/disp.nr0.htm"

# Pre-2008 vintages. The survey is biennial from 1984; these are the release dates BLS used
# for the historical text files. Every one that fails is reported by name.
PRE2008_GUESSES = [
    "disp_08172006.txt", "disp_07302004.txt", "disp_08212002.txt", "disp_08092000.txt",
    "disp_08191998.txt", "disp_08221996.txt", "disp_08251994.txt", "disp_09141992.txt",
    "disp_disp_1990.txt",
]
HIST = "https://www.bls.gov/news.release/history/"


def get(url, timeout=60):
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(r, timeout=timeout).read().decode("utf-8", "replace")


def strip_tags(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = h.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", h)


def parse_release(text):
    """Pull total long-tenured displaced, number reemployed, and the reemployment percent."""
    out = {}
    m = re.search(r"([\d.,]+)\s*million\s+workers\s+were\s+displaced\s+from\s+jobs\s+"
                  r"they\s+had\s+held\s+for\s+at\s+least\s+3\s+years", text, re.I)
    if m:
        out["total_millions"] = float(m.group(1).replace(",", ""))
    m = re.search(r"(\d{1,2}(?:\.\d)?)\s*percent\s+of\s+the\s+[\d.]+\s*million\s+"
                  r"(?:long-tenured\s+)?(?:workers\s+)?displaced", text, re.I)
    if not m:
        m = re.search(r"In\s+January\s+\d{4},?\s+(\d{1,2}(?:\.\d)?)\s*percent\s+of\s+the\s+"
                      r"[\d.]+\s*million\s+long-tenured\s+displaced\s+workers\s+were\s+"
                      r"reemployed", text, re.I)
    if not m:
        m = re.search(r"(\d{1,2}(?:\.\d)?)\s*percent\b[^.]{0,80}\breemployed", text, re.I)
    if m:
        out["rho_percent_stated"] = float(m.group(1))
    m = re.search(r"displaced\s+from\s+January\s+(\d{4})\s+through\s+December\s+(\d{4})",
                  text, re.I)
    if m:
        out["window_start"], out["window_end"] = int(m.group(1)), int(m.group(2))
    return out


def unrate():
    """Civilian unemployment rate, monthly. Uses the repository copy if present."""
    p = RAW / "fred" / "UNRATE.csv"
    if p.exists():
        d = pd.read_csv(p)
    else:
        u = ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=UNRATE")
        d = pd.read_csv(io.StringIO(get(u)))
        p.parent.mkdir(parents=True, exist_ok=True)
        d.to_csv(p, index=False)
    d.columns = ["date", "unrate"]
    d["date"] = pd.to_datetime(d["date"])
    return d.set_index("date")["unrate"]


def main():
    idx = get(INDEX)
    files = sorted(set(re.findall(r"(disp_\d{8}\.htm)", idx)))
    print(f"archive index lists {len(files)} releases: {', '.join(files)}")

    rows, missing = [], []
    for f in files:
        url = ARCH + f
        try:
            txt = strip_tags(get(url))
        except Exception as e:
            missing.append((f, f"{type(e).__name__}"))
            continue
        d = parse_release(txt)
        d["release_file"] = f
        d["url"] = url
        d["release_date"] = f"{f[5:9]}-{f[9:11]}-{f[11:15]}"[0:2]  # placeholder, fixed below
        mm, dd, yyyy = f[5:7], f[7:9], f[9:13]
        d["release_date"] = f"{yyyy}-{mm}-{dd}"
        d["survey_month"] = f"{yyyy}-01"
        rows.append(d)
        time.sleep(0.4)

    # pre-2008 attempts
    for g in PRE2008_GUESSES:
        try:
            txt = get(HIST + g, timeout=25)
            d = parse_release(re.sub(r"\s+", " ", txt))
            d["release_file"] = g
            d["url"] = HIST + g
            mm, dd, yyyy = g[5:7], g[7:9], g[9:13]
            d["release_date"] = f"{yyyy}-{mm}-{dd}"
            d["survey_month"] = f"{yyyy}-01"
            rows.append(d)
        except Exception as e:
            missing.append((g, type(e).__name__))
        time.sleep(0.3)

    D = pd.DataFrame(rows)
    D["rho"] = D["rho_percent_stated"] / 100.0
    u = unrate()
    D["survey_unrate"] = [float(u.get(pd.Timestamp(s + "-01"), np.nan))
                          for s in D["survey_month"]]
    D = D.sort_values("release_date").reset_index(drop=True)

    fit = {}
    v = D.dropna(subset=["rho", "survey_unrate"])
    if len(v) >= 3:
        x = v["survey_unrate"].to_numpy(float)
        y = v["rho"].to_numpy(float)
        n = len(x)
        b1, b0 = np.polyfit(x, y, 1)
        yhat = b0 + b1 * x
        ss = float(((y - yhat) ** 2).sum())
        se_b1 = float(np.sqrt(ss / (n - 2) / ((x - x.mean()) ** 2).sum()))
        r2 = 1 - ss / float(((y - y.mean()) ** 2).sum())
        fit = {"n_vintages": int(n), "intercept": float(b0), "slope_per_pp_unrate": float(b1),
               "slope_se": se_b1, "t": float(b1 / se_b1) if se_b1 else np.nan,
               "r_squared": float(r2),
               "unrate_range": [float(x.min()), float(x.max())],
               "rho_range": [float(y.min()), float(y.max())]}

    D.to_csv(OUT / "bls_dws_vintages.csv", index=False)
    (OUT / "bls_dws_vintages.json").write_text(json.dumps(
        {"vintages": D.round(5).to_dict("records"), "fit_rho_on_unrate": fit,
         "unreachable": [{"file": a, "error": b} for a, b in missing]}, indent=2))

    pd.set_option("display.width", 200)
    print("\n=== DWS VINTAGES ===")
    print(D[["release_date", "window_start", "window_end", "total_millions",
             "rho", "survey_unrate"]].to_string(index=False))
    if missing:
        print("\n=== NOT REACHABLE, listed rather than dropped ===")
        for a, b in missing:
            print(f"  {a:26s} {b}")
    if fit:
        print("\n=== rho on survey-month unemployment rate, OLS ===")
        print(f"  rho = {fit['intercept']:.4f} + ({fit['slope_per_pp_unrate']:.4f}) "
              f"x unrate      n = {fit['n_vintages']}")
        print(f"  slope se {fit['slope_se']:.4f}, t = {fit['t']:.2f}, "
              f"R2 = {fit['r_squared']:.3f}")
        print(f"  unrate observed range {fit['unrate_range']}, "
              f"rho observed range {fit['rho_range']}")


if __name__ == "__main__":
    main()
