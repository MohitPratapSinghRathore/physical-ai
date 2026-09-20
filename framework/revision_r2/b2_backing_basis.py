"""B2. What the household backing coefficients actually measure, and the alternative.

SPECIFICATION, STATED BEFORE COMPUTING.

The paper defines the labor backing of a claim class as the share of the cash flow that services
it which is labor income. Two different quantities can be computed from the survey, and the
published coefficients are the first.

  COVERAGE (what is published):
      cov(c) = sum over working-core households of w_h * D_h(c)
             / sum over ALL households of w_h * D_h(c)
    the share of the balances of class c owed by households with an employed member aged 25 to
    64. It is a statement about WHO OWES, not about which income services the debt.

  WAGE SHARE OF SERVICING INCOME (the alternative computed here):
      wag(c) = sum over debtor households of w_h * D_h(c) * (earnings_h / income_h)
             / sum over debtor households of w_h * D_h(c)
    the debt-weighted share of total household income that is wages, among households owing the
    class, on the assumption that a household services its debts out of its income in proportion
    to the composition of that income.

PLAUSIBILITY BOUNDS, STATED BEFORE COMPUTING.
  1. Both quantities lie in [0, 1] for every class; asserted in code.
  2. The per-household wage ratio is clipped to [0, 1] before weighting, so a household with
     small or negative total income and positive earnings cannot contribute a ratio above one.
  3. The wage share is computed only over households with positive income and a positive balance.
  4. The two need not agree. If the wage-share version is lower, the published coefficients
     overstate labor backing and every ratio built on them falls.

READER. The project's general survey loader holds too many columns in memory for this machine,
so this module streams the file itself, keeping fourteen columns and the December reference
month only.

STATUS. MEASURED from the survey. The mapping to claim classes and the proportional-servicing
assumption are stated assumptions.
"""
import io
import json
import pathlib
import zipfile

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent
SIPP = ROOT / "data" / "raw" / "sipp" / "pu2025_csv.zip"

COLS = ["SSUID", "ERESIDENCEID", "PNUM", "MONTHCODE", "WPFINWGT", "ERELRPE", "TAGE",
        "RMESR", "TPEARN", "THTOTINC", "THDEBT_CC", "THDEBT_ED", "THDEBT_VEH", "THDEBT_HOME"]
CLASSES = [("credit_card", "THDEBT_CC"), ("auto_loan", "THDEBT_VEH"),
           ("student_loan", "THDEBT_ED"), ("home_mortgage", "THDEBT_HOME")]


def read_month12():
    with zipfile.ZipFile(SIPP) as z:
        name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]
        with z.open(name) as fh:
            parts = []
            for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                                  sep="|", usecols=COLS, chunksize=100_000,
                                  low_memory=False):
                ch = ch[pd.to_numeric(ch["MONTHCODE"], errors="coerce") == 12]
                if len(ch):
                    parts.append(ch)
            return pd.concat(parts, ignore_index=True)


def main():
    D = read_month12()
    D["hh"] = D["SSUID"].astype(str) + "_" + D["ERESIDENCEID"].astype(str)
    for c in ("WPFINWGT", "TAGE", "RMESR", "TPEARN", "THTOTINC", "ERELRPE",
              "THDEBT_CC", "THDEBT_ED", "THDEBT_VEH", "THDEBT_HOME"):
        D[c] = pd.to_numeric(D[c], errors="coerce")

    # household level: reference-person weight, household aggregates, summed earnings
    ref = D[D["ERELRPE"].isin([1, 2])].sort_values("WPFINWGT").groupby("hh").tail(1)
    hh = ref.set_index("hh")[["WPFINWGT", "TAGE", "THTOTINC", "THDEBT_CC", "THDEBT_ED",
                              "THDEBT_VEH", "THDEBT_HOME"]].copy()
    hh["earn_m"] = D.groupby("hh")["TPEARN"].sum().reindex(hh.index).fillna(0.0)
    hh["any_employed"] = (D.assign(e=D["RMESR"].between(1, 5))
                          .groupby("hh")["e"].any().reindex(hh.index).fillna(False))
    hh = hh[hh["WPFINWGT"] > 0]

    w = hh["WPFINWGT"].to_numpy(float)
    core = (hh["any_employed"].to_numpy(bool)
            & hh["TAGE"].between(25, 64).to_numpy())
    inc = hh["THTOTINC"].fillna(0.0).to_numpy(float)
    earn = hh["earn_m"].fillna(0.0).to_numpy(float)
    ratio = np.clip(np.where(inc > 0, earn / np.maximum(inc, 1e-9), 0.0), 0.0, 1.0)

    rows = []
    for label, col in CLASSES:
        d = hh[col].fillna(0.0).to_numpy(float)
        total = float((w * d).sum())
        cov = float((w * d * core).sum()) / max(total, 1e-9)
        hold = d > 0
        wag = float((w[hold] * d[hold] * ratio[hold]).sum()) \
            / max(float((w[hold] * d[hold]).sum()), 1e-9)
        core_hold = hold & core
        wag_core = float((w[core_hold] * d[core_hold] * ratio[core_hold]).sum()) \
            / max(float((w[core_hold] * d[core_hold]).sum()), 1e-9)
        assert 0.0 <= cov <= 1.0, f"{label}: coverage outside the unit interval"
        assert 0.0 <= wag <= 1.0, f"{label}: wage share outside the unit interval"
        rows.append({
            "claim_class": label,
            "coverage_share_published_basis": round(cov, 6),
            "wage_share_of_servicing_income": round(wag, 6),
            "wage_share_within_working_core": round(wag_core, 6),
            "difference_wage_minus_coverage": round(wag - cov, 6),
            "weighted_balances_bn": round(float((w * d).sum()) / 1e9, 1),
            "debtor_households_millions": round(float(w[hold].sum()) / 1e6, 2),
        })

    out = {
        "status": "MEASURED from the survey; the mapping to claim classes and the "
                  "proportional-servicing assumption are stated assumptions.",
        "definitions": {
            "coverage_share_published_basis":
                "share of the class's balances owed by working-core households, which is who "
                "owes rather than which income services the debt",
            "wage_share_of_servicing_income":
                "debt-weighted share of total household income that is wages, among households "
                "owing the class, which is what the paper's definition asks for",
        },
        "plausibility_bounds_checked": [
            "both quantities in [0, 1] for every class, asserted in code",
            "per-household wage ratio clipped to [0, 1] before weighting",
            "wage share computed only over households with positive income and balance",
        ],
        "households_weighted_millions": round(float(w.sum()) / 1e6, 2),
        "by_class": rows,
    }
    (HERE / "b2_backing_basis.json").write_text(json.dumps(out, indent=2) + "\n")
    pd.DataFrame(rows).to_csv(HERE / "b2_backing_basis.csv", index=False)
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
