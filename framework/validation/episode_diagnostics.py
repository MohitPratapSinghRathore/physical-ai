"""
Episode diagnostics: how concentrated and how large is the wage-income shock in
each candidate episode, and is the exposed set big enough to identify anything?

Treatment-side only. No loss, delinquency, charge-off or failure series is read.

Source: BEA CAINC5N, county earnings by NAICS industry, 2001-2024.
"""
from pathlib import Path
import io
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"

MINING = "200"      # Mining, quarrying, and oil and gas extraction
TOTAL_EARN = "35"   # Earnings by place of work
PI = "10"           # Personal income


def load():
    with zipfile.ZipFile(RAW / "CAINC5N.zip") as z:
        name = "CAINC5N__ALL_AREAS_2001_2024.csv"
        df = pd.read_csv(io.BytesIO(z.read(name)), encoding="latin-1", dtype=str)
    df["GeoFIPS"] = df["GeoFIPS"].str.strip().str.replace('"', "", regex=False)
    return df


def series(df, line, years):
    s = df[df["LineCode"] == line].set_index("GeoFIPS")
    out = s[years].apply(pd.to_numeric, errors="coerce")
    return out[~out.index.str.endswith("000")]


def main():
    df = load()
    yrs = [str(y) for y in range(2001, 2024)]
    mining = series(df, MINING, yrs)
    earn = series(df, TOTAL_EARN, yrs)
    pi = series(df, PI, yrs)

    idx = mining.index.intersection(earn.index).intersection(pi.index)
    mining, earn, pi = mining.loc[idx], earn.loc[idx], pi.loc[idx]

    # ---- oil and gas exposure, measured BEFORE the collapse ---------------
    expo = (mining["2013"] / earn["2013"]).replace([np.inf, -np.inf], np.nan)
    expo = expo.dropna()
    high = expo[expo > 0.10].index        # >10% of earnings from mining
    print("PART C. Oil and gas exposure, pre-shock 2013")
    print(f"  counties with usable mining data: {len(expo)}")
    print(f"  counties >10% of earnings from mining: {len(high)}")
    print(f"  counties  >5% of earnings from mining: {(expo > 0.05).sum()}")
    print(f"  exposure p50 {expo.median():.4f}  p90 {expo.quantile(.9):.4f} "
          f" p99 {expo.quantile(.99):.4f}  max {expo.max():.4f}")

    # ---- wage-bill change in exposed vs rest, each episode ----------------
    episodes = {
        "2001 recession": ("2001", "2003"),
        "2007-2010 financial crisis": ("2007", "2010"),
        "2014-2016 oil collapse": ("2014", "2016"),
        "2020 pandemic": ("2019", "2020"),
    }
    rows = []
    for name, (t0, t1) in episodes.items():
        d = ((earn[t1] - earn[t0]) / pi[t0]).replace(
            [np.inf, -np.inf], np.nan).dropna()
        ex = expo.reindex(d.index).dropna()
        d = d.loc[ex.index]
        hi = ex[ex > 0.10].index
        lo = ex[ex <= 0.10].index
        rows.append({
            "episode": name,
            "window": f"{t0}-{t1}",
            "n_exposed": len(hi),
            "earn_change_exposed_pct": round(100 * d.loc[hi].median(), 2),
            "earn_change_rest_pct": round(100 * d.loc[lo].median(), 2),
            "gap_pp": round(100 * (d.loc[hi].median() - d.loc[lo].median()), 2),
            "corr_exposure_with_change": round(float(ex.corr(d)), 3),
        })
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "episode_exposure_contrast.csv", index=False)
    print("\n  Earnings change over base personal income, by 2013 mining "
          "exposure\n")
    print(out.to_string(index=False))

    # ---- how many banks sit in exposed counties? -------------------------
    sod = pd.read_csv(RAW / "fdic_sod_2014.csv")
    sod = sod.dropna(subset=["STCNTYBR"])
    sod["fips"] = (sod["STCNTYBR"].astype(float).astype(int)
                   .astype(str).str.zfill(5))
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"], errors="coerce").fillna(0)
    sod = sod.merge(expo.rename("expo"), left_on="fips",
                    right_index=True, how="left")
    bank_expo = sod.groupby("CERT").apply(
        lambda g: np.average(g["expo"].fillna(0), weights=g["DEPSUMBR"])
        if g["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)
    print("\n  Deposit-weighted mining exposure of banks, 2014")
    print(f"    banks with any branch data: {bank_expo.notna().sum()}")
    for t in (0.02, 0.05, 0.10):
        print(f"    banks with exposure >{t:.0%}: {(bank_expo > t).sum()}")
    bank_expo.rename("bank_mining_exposure_2014").to_csv(
        RAW / "bank_mining_exposure_2014.csv")


if __name__ == "__main__":
    main()
