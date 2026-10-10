"""
Session 1 evidence: is the holder leg reducible to the public GSE share of
mortgages, which is two FRED series divided? Result: no. Changes correlate
at +0.09 and the two diverge structurally after 2008.
"""
from pathlib import Path
import io
import urllib.request
import pandas as pd

OUT = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]


def fred(sid):
    t = urllib.request.urlopen(
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}",
        timeout=60).read().decode()
    f = pd.read_csv(io.StringIO(t))
    f.columns = ["date", "v"]
    f["v"] = pd.to_numeric(f["v"], errors="coerce")
    f["year"] = pd.to_datetime(f["date"]).dt.year
    return f.dropna().groupby("year")["v"].mean().rename(sid)


def main():
    gse = fred("AGSEBMPTCMAHDFS")     # agency and GSE-backed mortgage pools
    tot = fred("ASTMA")               # total mortgages, all sectors
    pub = (gse / tot).rename("public_gse_share_of_mortgages")

    d = pd.read_csv(ROOT / "framework" / "labor_backing"
                    / "direct_ratio_timeseries.csv")
    d["holder"] = d["federal_labour_backed_bn"] / d["labour_backed_bn"]
    m = d.set_index("year")[["holder"]].join(pub, how="inner").dropna()

    lv = m["holder"].corr(m["public_gse_share_of_mortgages"])
    dm = m.diff().dropna()
    df = dm["holder"].corr(dm["public_gse_share_of_mortgages"])
    m.to_csv(OUT / "s1_divergence.csv")
    print(f"overlap {m.index.min()}-{m.index.max()}, n={len(m)}")
    print(f"levels      r = {lv:+.4f}")
    print(f"differences r = {df:+.4f}")
    print(m.loc[[1965, 1989, 2001, 2007, 2013, 2025]].round(4).to_string())


if __name__ == "__main__":
    main()
