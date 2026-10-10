"""
Amendment 1 construct: DEBTOR-SPECIFIC local wage dependence.

Motivation. The feasibility check showed the accounts' class coefficients are
near-binary, so the bank-level measure is 94 percent reproducible from loan
shares and the POPULATION-WIDE county wage share. If the accounts have any
distinctive content it must be debtor-specific: the wage dependence of the
households that actually owe the debt, which is not the wage dependence of the
county as a whole.

Vintage. ACS 2009-2013 5-year PUMS, restricted to records carrying PUMA10, i.e.
survey years 2012-2013 on 2010 PUMA geography. Chosen because:
  - it is PRE-SHOCK for the 2014-2016 oil collapse (the repo's own PUMS is the
    2023 1-year file, which is POST-shock and cannot be used here);
  - restricting to PUMA10 avoids mixing 2000- and 2010-definition PUMAs, which
    the 5-year file otherwise does, and matches the 2010 tract-to-PUMA crosswalk.
Cell sizes are reported; the cost of this restriction is roughly 3/5 of the
5-year sample.

No outcome variable is read anywhere in this file.
"""
from pathlib import Path
import io
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"
PUMS = RAW / "pums2013"

MIN_CELL = 100          # minimum unweighted households per PUMA x group cell

HUS_COLS = ["serialno", "PUMA10", "ST", "TEN", "WGTP", "HINCP", "MRGP",
            "GRNTP", "ADJINC", "TYPE", "NP"]
PUS_COLS = ["serialno", "WAGP", "ADJINC"]


def read_zip_csv(zpath, cols, chunk=500_000):
    """Stream the needed columns out of a multi-part PUMS zip."""
    out = []
    with zipfile.ZipFile(zpath) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".csv")]
        for n in sorted(names):
            with z.open(n) as f:
                head = f.readline().decode().strip().split(",")
            use = [c for c in cols if c in head]
            with z.open(n) as f:
                for part in pd.read_csv(f, usecols=use, dtype=str,
                                        chunksize=chunk, low_memory=False):
                    out.append(part)
            print(f"    {n}: done")
    return pd.concat(out, ignore_index=True)


def build_household_frame():
    print("  reading housing records")
    h = read_zip_csv(PUMS / "csv_hus.zip", HUS_COLS)
    h = h[h["PUMA10"].notna() & (h["PUMA10"].str.strip() != "")]
    for c in ["TEN", "WGTP", "HINCP", "MRGP", "GRNTP", "ADJINC", "TYPE", "NP"]:
        h[c] = pd.to_numeric(h[c], errors="coerce")
    h = h[(h["TYPE"] == 1) & (h["NP"] > 0) & (h["WGTP"] > 0)]
    h["puma_id"] = (h["ST"].str.zfill(2) + h["PUMA10"].str.zfill(5))

    print("  reading person records")
    p = read_zip_csv(PUMS / "csv_pus.zip", PUS_COLS)
    p["WAGP"] = pd.to_numeric(p["WAGP"], errors="coerce").fillna(0)
    wage = p.groupby("serialno")["WAGP"].sum().rename("hh_wage")

    h = h.merge(wage, left_on="serialno", right_index=True, how="left")
    h["hh_wage"] = h["hh_wage"].fillna(0)

    # ADJINC puts income in constant 2013 dollars; it is a 7-decimal integer.
    adj = h["ADJINC"] / 1e6
    h["hh_wage_adj"] = h["hh_wage"] * adj
    h["hincp_adj"] = h["HINCP"] * adj
    # Mortgage payment and gross rent are monthly; annualise.
    h["mort_service"] = h["MRGP"].fillna(0) * 12
    h["rent_service"] = h["GRNTP"].fillna(0) * 12
    return h


def wage_share(df, wcol):
    """Aggregate wage share of income: sum(w*wage)/sum(w*income)."""
    d = df[df["hincp_adj"] > 0]
    w = d[wcol]
    den = (w * d["hincp_adj"]).sum()
    return (w * d["hh_wage_adj"]).sum() / den if den > 0 else np.nan


def main():
    h = build_household_frame()
    print(f"  households on PUMA10 geography: {len(h):,}")

    groups = {
        "mortgage": h["TEN"] == 1,          # owned with a mortgage
        "renter":   h["TEN"] == 3,          # rented
        "all":      h["TEN"].notna(),       # all occupied households
    }

    rows = []
    for name, mask in groups.items():
        g = h[mask].copy()
        # household-weighted
        hh = g.groupby("puma_id").apply(
            lambda d: wage_share(d, "WGTP"), include_groups=False)
        n = g.groupby("puma_id").size().rename("n_hh")
        r = pd.DataFrame({"wage_share": hh, "n_hh": n})
        r["group"] = name
        # payment- or rent-weighted, where the data allow
        if name == "mortgage":
            g["sw"] = g["WGTP"] * g["mort_service"]
            r["wage_share_payment_wtd"] = g.groupby("puma_id").apply(
                lambda d: wage_share(d, "sw"), include_groups=False)
        elif name == "renter":
            g["sw"] = g["WGTP"] * g["rent_service"]
            r["wage_share_payment_wtd"] = g.groupby("puma_id").apply(
                lambda d: wage_share(d, "sw"), include_groups=False)
        else:
            r["wage_share_payment_wtd"] = np.nan
        rows.append(r.reset_index())
    puma = pd.concat(rows, ignore_index=True)
    puma["below_min_cell"] = puma["n_hh"] < MIN_CELL
    puma.to_csv(OUT / "puma_debtor_wage_shares_2013.csv", index=False)

    print("\n  PUMA x group cells")
    for name in groups:
        s = puma[puma["group"] == name]
        print(f"    {name:9s} pumas {len(s):5d}  median cell {s.n_hh.median():7.0f}"
              f"  below {MIN_CELL}: {int(s.below_min_cell.sum()):4d}"
              f"  wage share p50 {s.wage_share.median():.4f}")

    # ---- PUMA -> county, housing-unit weighted ---------------------------
    x = pd.read_csv(RAW / "crosswalk" / "2010_tract_to_2010_puma.txt", dtype=str)
    x.columns = [c.strip().upper() for c in x.columns]
    x["puma_id"] = x["STATEFP"].str.zfill(2) + x["PUMA5CE"].str.zfill(5)
    x["county_fips"] = x["STATEFP"].str.zfill(2) + x["COUNTYFP"].str.zfill(3)
    x["tract_geoid"] = (x["STATEFP"].str.zfill(2) + x["COUNTYFP"].str.zfill(3)
                        + x["TRACTCE"].str.zfill(6))

    with zipfile.ZipFile(RAW / "crosswalk" / "Gaz_tracts_national.zip") as z:
        gz = pd.read_csv(io.BytesIO(z.read("Gaz_tracts_national.txt")),
                         sep="\t", dtype=str, encoding="latin-1")
    gz.columns = [c.strip() for c in gz.columns]
    gz["HU10"] = pd.to_numeric(gz["HU10"], errors="coerce").fillna(0)
    x = x.merge(gz[["GEOID", "HU10"]], left_on="tract_geoid",
                right_on="GEOID", how="left")
    x["HU10"] = x["HU10"].fillna(0)

    # allocation factor: housing units, not tract counts (the repo's existing
    # crosswalk uses tract COUNTS and flags that as an approximation)
    cnt = x.groupby(["puma_id", "county_fips"])["HU10"].sum().rename("hu")
    cnt = cnt.reset_index()
    tot = cnt.groupby("puma_id")["hu"].sum().rename("hu_total")
    cnt = cnt.merge(tot, on="puma_id")
    cnt["afact"] = np.where(cnt["hu_total"] > 0,
                            cnt["hu"] / cnt["hu_total"], np.nan)
    cnt = cnt.dropna(subset=["afact"])
    cnt.to_csv(RAW / "puma2010_to_county_afact_hu.csv", index=False)
    print(f"\n  crosswalk: {cnt.puma_id.nunique()} pumas -> "
          f"{cnt.county_fips.nunique()} counties, housing-unit weighted")

    # county wage share by group: afact-weighted mean over overlapping PUMAs
    out = []
    for name in groups:
        s = puma[(puma["group"] == name) & (~puma["below_min_cell"])]
        m = cnt.merge(s, on="puma_id", how="inner")
        for col in ["wage_share", "wage_share_payment_wtd"]:
            m[col + "_w"] = m[col] * m["afact"] * m["hu"]
        agg = m.groupby("county_fips").apply(lambda d: pd.Series({
            "wage_share": (d["wage_share"] * d["hu"]).sum() / d["hu"].sum()
            if d["hu"].sum() > 0 else np.nan,
            "wage_share_payment_wtd":
                (d["wage_share_payment_wtd"] * d["hu"]).sum() / d["hu"].sum()
                if d["hu"].sum() > 0 else np.nan,
            "n_pumas": len(d),
            "n_hh_total": d["n_hh"].sum(),
        }), include_groups=False)
        agg["group"] = name
        out.append(agg.reset_index())
    county = pd.concat(out, ignore_index=True)
    county.to_csv(OUT / "county_debtor_wage_shares_2013.csv", index=False)

    print("\n  County-level debtor-specific wage shares")
    for name in groups:
        s = county[county["group"] == name]
        print(f"    {name:9s} counties {len(s):5d}  wage share p50 "
              f"{s.wage_share.median():.4f}  payment-wtd p50 "
              f"{s.wage_share_payment_wtd.median():.4f}")


if __name__ == "__main__":
    main()
