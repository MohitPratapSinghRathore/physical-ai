"""
Mining-earnings disclosure suppression: how much is hidden, and what does each
handling choice do to the exposed-bank sample?

BEA suppresses county mining earnings with (D) when publication would disclose an
individual employer, which happens where there are FEW establishments. Suppressed
counties are therefore small-but-nonzero, not zero. They remain inside the state
total, so the state residual bounds them in aggregate.

Treatment side only. No outcome variable is read.
"""
from pathlib import Path
import io
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"

MINING, TOTAL_EARN = "200", "35"


def load(line):
    with zipfile.ZipFile(RAW / "CAINC5N.zip") as z:
        df = pd.read_csv(io.BytesIO(
            z.read("CAINC5N__ALL_AREAS_2001_2024.csv")),
            encoding="latin-1", dtype=str)
    df["GeoFIPS"] = df["GeoFIPS"].str.strip().str.replace('"', "", regex=False)
    return df[df["LineCode"] == line].set_index("GeoFIPS")


def main():
    mine = load(MINING)
    earn = load(TOTAL_EARN)

    cty = ~mine.index.str.endswith("000")
    st = mine.index.str.endswith("000") & (mine.index != "00000")

    m_cty = pd.to_numeric(mine.loc[cty, "2013"], errors="coerce")
    m_st = pd.to_numeric(mine.loc[st, "2013"], errors="coerce")
    e_cty = pd.to_numeric(earn.loc[cty, "2013"], errors="coerce")

    flags = mine.loc[cty, "2013"]
    n_d = int((flags == "(D)").sum())
    n_na = int((flags == "(NA)").sum())

    # state residual: state total less the disclosed counties in that state
    state_of = pd.Series(m_cty.index.str[:2], index=m_cty.index)
    disclosed_sum = m_cty.groupby(state_of).sum(min_count=1)
    st_key = pd.Series(m_st.values, index=m_st.index.str[:2])
    st_key = st_key[~st_key.index.duplicated()]

    rows = []
    for s in sorted(set(state_of) & set(st_key.index)):
        tot = st_key.get(s, np.nan)
        disc = disclosed_sum.get(s, 0.0)
        n_sup = int(((state_of == s) & (m_cty.isna())).sum())
        if pd.isna(tot) or n_sup == 0:
            continue
        resid = tot - disc
        rows.append({
            "state_fips": s, "state_mining_earnings": tot,
            "disclosed_sum": disc, "residual": resid,
            "n_suppressed_counties": n_sup,
            "residual_share_of_state": resid / tot if tot else np.nan,
            "mean_residual_per_suppressed_county": resid / n_sup,
        })
    res = pd.DataFrame(rows).sort_values("residual", ascending=False)
    res.to_csv(OUT / "suppression_state_residual.csv", index=False)

    tot_resid = res["residual"].sum()
    tot_state = st_key.reindex(res["state_fips"]).sum()
    print("PART D. Mining-earnings suppression, 2013")
    print(f"  counties: {len(m_cty)}   disclosed: {m_cty.notna().sum()}   "
          f"(D): {n_d}   (NA): {n_na}")
    print(f"  suppressed earnings as share of state mining totals, pooled: "
          f"{tot_resid / tot_state:.4f}")
    print(f"  states where the residual exceeds 10% of the state total: "
          f"{(res['residual_share_of_state'] > 0.10).sum()} of {len(res)}")
    print(f"  negative residuals (state total below disclosed sum, i.e. "
          f"rounding/definition noise): {(res['residual'] < 0).sum()}")

    # upper bound on a suppressed county's exposure: give it the whole state residual
    sup_idx = m_cty[m_cty.isna()].index
    ub = pd.Series(index=sup_idx, dtype=float)
    for s, grp in pd.Series(sup_idx).groupby(sup_idx.str[:2]):
        r = res.loc[res["state_fips"] == s, "residual"]
        ub.loc[grp.values] = float(r.iloc[0]) if len(r) else np.nan
    ub_expo = (ub / e_cty.reindex(sup_idx)).replace([np.inf, -np.inf], np.nan)
    print(f"  suppressed counties whose UPPER BOUND exposure could still "
          f"exceed 10%: {(ub_expo > 0.10).sum()} of {len(sup_idx)}")
    print(f"  ... whose upper bound is below 2% (safely unexposed): "
          f"{(ub_expo < 0.02).sum()}")

    # ---- effect of each handling choice on the bank sample ----------------
    expo_disclosed = (m_cty / e_cty).replace([np.inf, -np.inf], np.nan)
    sod = pd.read_csv(RAW / "fdic_sod_2014.csv")
    sod = sod.dropna(subset=["STCNTYBR"])
    sod["fips"] = (sod["STCNTYBR"].astype(float).astype(int)
                   .astype(str).str.zfill(5))
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"], errors="coerce").fillna(0)

    def bank_expo(county_expo, treat_missing_as):
        s = sod.copy()
        s["e"] = s["fips"].map(county_expo)
        if treat_missing_as == "zero":
            s["e"] = s["e"].fillna(0.0)
        elif treat_missing_as == "drop":
            s = s.dropna(subset=["e"])
        return s.groupby("CERT").apply(
            lambda g: np.average(g["e"], weights=g["DEPSUMBR"])
            if g["DEPSUMBR"].sum() > 0 and len(g) else np.nan,
            include_groups=False)

    # deposit share of a bank sitting in suppressed counties
    sod["is_sup"] = sod["fips"].isin(set(sup_idx))
    sup_share = sod.groupby("CERT").apply(
        lambda g: np.average(g["is_sup"].astype(float), weights=g["DEPSUMBR"])
        if g["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)

    a = bank_expo(expo_disclosed, "zero")
    b = bank_expo(expo_disclosed, "drop")
    comp = pd.DataFrame({"expo_missing_as_zero": a, "expo_disclosed_only": b,
                         "deposit_share_in_suppressed_counties": sup_share})
    comp.to_csv(RAW / "bank_exposure_suppression_variants.csv")

    print("\n  Effect on the exposed-bank sample (deposit-weighted, 2014):")
    print(f"    banks with any branch data: {len(comp)}")
    for t in (0.02, 0.05, 0.10):
        na = int((a > t).sum())
        nb = int((b > t).sum())
        print(f"    exposure >{t:.0%}:  missing-as-zero {na:5d}   "
              f"disclosed-only {nb:5d}   difference {nb - na:+d}")
    print(f"    banks with >50% of deposits in suppressed counties: "
          f"{(sup_share > 0.50).sum()}")
    print(f"    banks with >25% of deposits in suppressed counties: "
          f"{(sup_share > 0.25).sum()}")
    print(f"    banks with zero deposits in suppressed counties: "
          f"{(sup_share == 0).sum()}")


if __name__ == "__main__":
    main()
