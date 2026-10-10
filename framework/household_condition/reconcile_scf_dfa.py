"""
Feasibility: reconcile SCF 2022 aggregates to the Financial Accounts via the
Distributional Financial Accounts, using the measurement paper's separation of
SURVEY UNDER-REPORTING from SAMPLE COVERAGE (claim 127 correction).

COMPUTES NO RESULT OF THE EXERCISE. Produces ratios so the specification can
state a reconciliation tolerance against known gaps.
"""
from pathlib import Path
import io
import json
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "household_condition"
OUT = ROOT / "framework" / "household_condition"
DFA_Q = "2022:Q4"


def scf_agg(df, col):
    """SCF weighted aggregate in $bn. WGT sums to households over ALL five
    implicates, so the full-sample sum is already the household total."""
    return float((df[col] * df["wgt"]).sum() / 1e9)


def main():
    z = zipfile.ZipFile(RAW / "scfp2022s.zip")
    scf = pd.read_stata(io.BytesIO(z.read("rscfp2022.dta")))

    zd = zipfile.ZipFile(RAW / "dfa.zip")
    dfa = pd.read_csv(io.BytesIO(zd.read("dfa-networth-levels.csv")))
    q = dfa[dfa["Date"] == DFA_Q]
    D = {c: float(q[c].sum()) / 1000.0 for c in q.columns if c not in
         ("Date", "Category")}          # DFA is $m -> $bn

    rows = []

    def add(label, scf_val, dfa_val, note=""):
        ratio = scf_val / dfa_val if dfa_val else np.nan
        rows.append({"cell": label, "scf_bn": round(scf_val, 1),
                     "dfa_z1_bn": round(dfa_val, 1),
                     "scf_over_official": round(ratio, 4),
                     "implied_under_reporting_factor": round(1 / ratio, 4)
                     if ratio else np.nan, "note": note})

    # ---- debt --------------------------------------------------------------
    add("Home mortgages (incl. HELOC)", scf_agg(scf, "mrthel"),
        D["Home mortgages"],
        "SCF MRTHEL is mortgage + home-equity lines on the primary residence")
    cons_scf = scf_agg(scf, "ccbal") + scf_agg(scf, "install")
    add("Consumer credit (revolving + installment)", cons_scf,
        D["Consumer credit"], "SCF CCBAL + INSTALL against DFA consumer credit")
    add("  of which revolving (credit card)", scf_agg(scf, "ccbal"), np.nan,
        "no separate DFA line; compared to Z.1 revolving in the note below")
    add("Total liabilities", scf_agg(scf, "debt"), D["Liabilities"],
        "DFA liabilities include items the SCF does not field")

    # ---- equity ------------------------------------------------------------
    add("Corporate equity + mutual funds, DIRECT",
        scf_agg(scf, "stocks") + scf_agg(scf, "nmmf"),
        np.nan, "SCF direct holdings only; DFA line mixes direct and indirect")
    add("Corporate equity + mutual funds, ALL household routes",
        scf_agg(scf, "stocks") + scf_agg(scf, "nmmf")
        + scf_agg(scf, "retqliq") + scf_agg(scf, "annuit"),
        D["Corporate equities and mutual fund shares"],
        "SCF direct + retirement + annuities against the DFA equity line")
    add("Private business equity", scf_agg(scf, "bus"),
        D["Unincorporated businesses"],
        "SCF BUS includes S-corp and partnership stakes the DFA books "
        "differently; NOT expected to reconcile")
    add("Pension entitlements", scf_agg(scf, "retqliq"),
        D["DB pension entitlements"] + D["DC pension entitlements"],
        "SCF fields DC balances well and DB entitlements barely at all")

    rec = pd.DataFrame(rows)
    rec.to_csv(OUT / "scf_dfa_reconciliation.csv", index=False)

    # ---- the paper's own SIPP-based factors, for comparison ---------------
    ur = pd.read_csv(ROOT / "data" / "processed"
                     / "under_reporting_factors.csv")
    comp = {r.loan: {"paper_sipp_under_reporting_factor":
                     float(r.UNDER_REPORTING_factor),
                     "paper_official_bn": float(r.official_aggregate_bn)}
            for r in ur.itertuples()}
    scf_cells = {"mortgage": scf_agg(scf, "mrthel"),
                 "card": scf_agg(scf, "ccbal"),
                 "auto": scf_agg(scf, "veh_inst"),
                 "student": scf_agg(scf, "edn_inst")}
    for k, v in comp.items():
        v["scf_2022_bn"] = round(scf_cells[k], 1)
        v["implied_scf_factor_vs_paper_official"] = round(
            v["paper_official_bn"] / scf_cells[k], 4)

    out = {"dfa_quarter": DFA_Q,
           "reconciliation": rows,
           "paper_sipp_factors_vs_scf": comp,
           "scf_households_m": round(float(scf["wgt"].sum() / 1e6), 2)}
    (OUT / "scf_dfa_reconciliation.json").write_text(
        json.dumps(out, indent=2, default=float), encoding="utf-8")

    print(rec.to_string(index=False))
    print("\nPaper's SIPP factors against the SCF cells "
          "(paper official aggregates are a later vintage; indicative only):")
    for k, v in comp.items():
        print(f"  {k:9s} SIPP factor {v['paper_sipp_under_reporting_factor']:.4f}"
              f"   SCF 2022 {v['scf_2022_bn']:9.1f}bn"
              f"   implied SCF factor {v['implied_scf_factor_vs_paper_official']:.4f}")


if __name__ == "__main__":
    main()
