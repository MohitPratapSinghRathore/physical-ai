"""
Owner-fetched BLS LAUS county unemployment -> pre-shock county control.

PRE-SHOCK YEARS ONLY. The bulk file carries every year through 2026; this script
reads 2011-2013 and writes nothing else, so no shock-window value enters the
repository in this session.

The bulk file carries multiple measures. Measure code 03 is the unemployment
rate; area type F is a county. Series IDs are parsed as
    LAU + CN + <2-digit state FIPS> + <3-digit county FIPS> + <7 chars> + <2-digit measure>
and cross-checked against la.series rather than trusted on position alone.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
LAUS = RAW / "laus"
OUT = ROOT / "framework" / "validation"

PRE_SHOCK_YEARS = [2011, 2012, 2013]
UNEMP_RATE = "03"


def main():
    ser = pd.read_csv(LAUS / "la.series", sep="\t", dtype=str)
    ser.columns = [c.strip() for c in ser.columns]
    for c in ser.columns:
        ser[c] = ser[c].astype(str).str.strip()
    cty = ser[(ser["area_type_code"] == "F")
              & (ser["measure_code"] == UNEMP_RATE)].copy()
    # county FIPS sits in the area code: CN + SSCCC + zeros
    cty["fips"] = cty["area_code"].str[2:7]
    keep = dict(zip(cty["series_id"], cty["fips"]))
    print(f"  county unemployment-rate series: {len(keep)}")

    rows = []
    with open(LAUS / "la.data.64.County", "r", encoding="latin-1") as f:
        header = f.readline()
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            sid = parts[0].strip()
            if sid not in keep:
                continue
            try:
                yr = int(parts[1])
            except ValueError:
                continue
            if yr not in PRE_SHOCK_YEARS:
                continue
            per = parts[2].strip()
            val = pd.to_numeric(parts[3].strip(), errors="coerce")
            rows.append((keep[sid], yr, per, val))

    d = pd.DataFrame(rows, columns=["fips", "year", "period", "value"])
    print(f"  pre-shock observations read: {len(d):,}")

    # M13 is the annual average where present; otherwise average the months
    ann = d[d["period"] == "M13"].groupby(["fips", "year"])["value"].mean()
    monthly = (d[d["period"].str.startswith("M") & (d["period"] != "M13")]
               .groupby(["fips", "year"])["value"].mean())
    unrate = ann.combine_first(monthly).rename("unemp_rate").reset_index()

    wide = unrate.pivot(index="fips", columns="year", values="unemp_rate")
    wide.columns = [f"unemp_{c}" for c in wide.columns]
    wide["unemp_2011_2013_mean"] = wide.mean(axis=1)
    wide["unemp_change_2011_2013"] = wide.get("unemp_2013") - wide.get("unemp_2011")
    wide = wide.dropna(subset=["unemp_2013"])
    wide.to_csv(OUT / "county_unemployment_preshock.csv")

    print(f"  counties with 2013 rate: {len(wide)}")
    print(f"  2013 unemployment rate: p10 {wide['unemp_2013'].quantile(.1):.2f}"
          f"  p50 {wide['unemp_2013'].median():.2f}"
          f"  p90 {wide['unemp_2013'].quantile(.9):.2f}")

    # deposit-weighted to the bank, as the control enters the regression
    sod = pd.read_csv(RAW / "fdic_sod_2014.csv").dropna(subset=["STCNTYBR"])
    sod["fips"] = (sod["STCNTYBR"].astype(float).astype(int)
                   .astype(str).str.zfill(5))
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"], errors="coerce").fillna(0)
    sod["u"] = sod["fips"].map(wide["unemp_2013"])
    s = sod.dropna(subset=["u"])
    bank = s.groupby("CERT").apply(
        lambda g: np.average(g["u"], weights=g["DEPSUMBR"])
        if g["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)
    bank.rename("bank_unemp_2013").to_csv(RAW / "bank_unemployment_2013.csv")
    print(f"  banks with a deposit-weighted 2013 rate: {bank.notna().sum()}")

    covered = sod["fips"].isin(wide.index)
    print(f"  SOD branch rows matched to a LAUS county: "
          f"{100 * covered.mean():.2f}%")


if __name__ == "__main__":
    main()
