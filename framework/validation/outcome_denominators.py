"""
Amendment 3 feasibility: are the household-class and business-class denominators
large enough to carry the split outcomes?

PRE-SHOCK ONLY. This reads 2014-06-30 loan BALANCES, which are predictors. No
charge-off, non-performing or failure value is read.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"

HH = ["LNRERES", "LNCRCD", "LNAUTO", "LNCONOTH"]
BUS = ["LNCI", "LNRENRES"]
MIN_DENOM_FRAC = 0.05      # class book must be >=5% of gross loans
MIN_DENOM_ABS = 5_000      # and >= $5m (call report is in $000s)


def main():
    fin = pd.read_csv(RAW / "fdic_financials_20140630.csv")
    num = [c for c in fin.columns
           if c not in ("NAMEFULL", "STNAME", "ID", "REPDTE")]
    fin[num] = fin[num].apply(pd.to_numeric, errors="coerce")
    fin = fin[(fin["LNLSGR"] > 0) & (fin["ASSET"] > 0)].copy()

    fin["hh_loans"] = fin[HH].fillna(0).sum(axis=1)
    fin["bus_loans"] = fin[BUS].fillna(0).sum(axis=1)
    fin["bus_loans_incl_constr"] = (fin["bus_loans"]
                                    + fin["LNRECONS"].fillna(0))
    fin["hh_frac"] = fin["hh_loans"] / fin["LNLSGR"]
    fin["bus_frac"] = fin["bus_loans"] / fin["LNLSGR"]

    expo = pd.read_csv(RAW / "bank_mining_exposure_2014.csv")
    expo.columns = ["CERT", "mining_expo"]
    fin = fin.merge(expo, on="CERT", how="left")
    fin["exposed"] = fin["mining_expo"] > 0.10

    # pre-specified energy-adjacent proxy: C&I intensity x local mining exposure
    fin["energy_adjacent_ci"] = (fin["LNCI"].fillna(0) / fin["LNLSGR"]) \
        * fin["mining_expo"].fillna(0)

    def qual(col_loans, col_frac):
        return ((fin[col_loans] >= MIN_DENOM_ABS)
                & (fin[col_frac] >= MIN_DENOM_FRAC))

    q_hh = qual("hh_loans", "hh_frac")
    q_bus = qual("bus_loans", "bus_frac")

    res = {
        "n_banks": int(len(fin)),
        "household_denominator": {
            "median_share_of_gross_loans": float(fin["hh_frac"].median()),
            "p10_share": float(fin["hh_frac"].quantile(.10)),
            "p90_share": float(fin["hh_frac"].quantile(.90)),
            "banks_qualifying": int(q_hh.sum()),
            "banks_qualifying_pct": float(100 * q_hh.mean()),
            "exposed_banks_qualifying": int((q_hh & fin["exposed"]).sum()),
        },
        "business_denominator": {
            "median_share_of_gross_loans": float(fin["bus_frac"].median()),
            "p10_share": float(fin["bus_frac"].quantile(.10)),
            "p90_share": float(fin["bus_frac"].quantile(.90)),
            "banks_qualifying": int(q_bus.sum()),
            "banks_qualifying_pct": float(100 * q_bus.mean()),
            "exposed_banks_qualifying": int((q_bus & fin["exposed"]).sum()),
        },
        "both_qualifying": int((q_hh & q_bus).sum()),
        "both_qualifying_exposed": int((q_hh & q_bus & fin["exposed"]).sum()),
        "energy_adjacent_ci_proxy": {
            "mean": float(fin["energy_adjacent_ci"].mean()),
            "sd": float(fin["energy_adjacent_ci"].std()),
            "p90": float(fin["energy_adjacent_ci"].quantile(.90)),
            "corr_with_mining_exposure": float(
                fin["energy_adjacent_ci"].corr(fin["mining_expo"])),
            "corr_with_ci_share": float(
                fin["energy_adjacent_ci"].corr(
                    fin["LNCI"].fillna(0) / fin["LNLSGR"])),
        },
        "exposed_banks_ci_share_median": float(
            (fin.loc[fin["exposed"], "LNCI"].fillna(0)
             / fin.loc[fin["exposed"], "LNLSGR"]).median()),
        "unexposed_banks_ci_share_median": float(
            (fin.loc[~fin["exposed"], "LNCI"].fillna(0)
             / fin.loc[~fin["exposed"], "LNLSGR"]).median()),
    }
    (OUT / "outcome_denominators.json").write_text(
        json.dumps(res, indent=2), encoding="utf-8")

    fin[["CERT", "hh_loans", "bus_loans", "bus_loans_incl_constr", "hh_frac",
         "bus_frac", "energy_adjacent_ci", "mining_expo", "exposed"]].to_csv(
        RAW / "outcome_denominators_2014.csv", index=False)

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
