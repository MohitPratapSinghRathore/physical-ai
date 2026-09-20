"""MODULE A3. The institutions the paper omitted: state and local government, pension
funds, insurers and private credit.

Each gets three things and nothing more: the exposure MECHANISM, its SIZE, and what it can
and cannot absorb. Sizes are MEASURED from FRED and Z.1; the loss applications are SCENARIO.

The reason these three were omitted is worth stating: the engine was built around lenders,
and all three are exposed to wages through something other than a loan. State and local
government is exposed through its own tax base; pension funds through payroll-linked
contributions; insurers and private credit through holdings.
"""
import io
import json
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).parent
PROC = Path(__file__).resolve().parents[2] / "data" / "processed"
LB = Path(__file__).resolve().parents[1] / "labor_backing"
RAW = Path(__file__).resolve().parents[2] / "data" / "raw" / "fred"


def fred_annual(series, year=2025):
    p = RAW / f"{series}.csv"
    if p.exists():
        txt = p.read_text()
    else:
        r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}",
                         timeout=90)
        r.raise_for_status()
        txt = r.text
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt)
    d = pd.read_csv(io.StringIO(txt))
    d.columns = ["date", "v"]
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    d["date"] = pd.to_datetime(d["date"])
    d = d.dropna()
    a = d[d.date.dt.year == year]["v"]
    return float(a.mean()) if len(a) else float(d["v"].iloc[-1])


def main():
    out = {}

    # ---------------------------------------------------------------- (i) state and local
    # Series are the ones this project already uses for the state and local backing share.
    sl_tax = fred_annual("W070RC1Q027SBEA")       # total state and local tax receipts
    sl_personal = fred_annual("W071RC1Q027SBEA")  # state and local personal current taxes
    sl_sales = fred_annual("ASLSTAX")             # sales taxes
    sl_spend = fred_annual("SLEXPND")             # expenditures
    soi = json.loads((PROC / "labor_tax_share.json").read_text())
    w = soi["wage_share_of_agi"]                  # 0.6675, SOI 2023

    wage_linked_income_tax = w * sl_personal
    H = pd.read_csv(LB / "holder_matrix_latest.csv")
    muni_lb = float(H[H.claim_class == "state_local_debt"].labour_backed_bn.sum())
    muni_by_holder = (H[H.claim_class == "state_local_debt"]
                      .groupby("holder").labour_backed_bn.sum()
                      .sort_values(ascending=False).round(1).to_dict())

    out["state_and_local_government"] = {
        "mechanism": "Exposed through its OWN TAX BASE, not through a loan book. Income "
                     "tax falls directly with the wage bill; sales tax falls with the "
                     "spending that wages fund, which is the second-round channel. Unlike "
                     "the federal government it cannot run the deficit through: every "
                     "state but Vermont has a balanced-budget requirement of some form, so "
                     "a revenue fall becomes a spending cut or a tax rise in-year.",
        "size_bn": {
            "total tax receipts": round(sl_tax, 1),
            "personal current taxes": round(sl_personal, 1),
            "of which wage-linked at the SOI wage share": round(wage_linked_income_tax, 1),
            "sales taxes": round(sl_sales, 1),
            "total expenditure": round(sl_spend, 1),
        },
        "wage_linked_share_of_own_tax_receipts": round(wage_linked_income_tax / sl_tax, 4),
        "can_absorb": "Rainy day funds and the property tax base, which does not move with "
                      "wages in the first round. Property tax is the single largest "
                      "stabiliser in the state and local revenue mix and it is a capital "
                      "levy, so it is why this sector is less wage-exposed than the "
                      "federal government.",
        "cannot_absorb": "A multi-year revenue fall. The balanced-budget constraint turns a "
                         "revenue shock into a PROCYCLICAL spending cut, which feeds back "
                         "into the same demand channel that drives nine tenths of the bank "
                         "losses in this paper. THIS IS THE FEEDBACK LOOP THE ENGINE DOES "
                         "NOT MODEL, and it is stated as an omission rather than estimated.",
        "as_holder": {"labour_backed_municipal_debt_bn": round(muni_lb, 1),
                      "by_holder_bn": muni_by_holder},
        "status": "MEASURED sizes; the feedback loop is NOT modelled",
    }

    # ---------------------------------------------------------------- (ii) pension funds
    pens_lb = float(H[H.holder == "pensions"].labour_backed_bn.sum())
    out["pension_funds"] = {
        "mechanism": "Exposed on BOTH sides and in opposite directions. On the liability "
                     "side, defined benefit promises are fixed in nominal terms and do not "
                     "fall when wages fall. On the funding side, contributions are a "
                     "percentage of covered payroll, so they fall one for one with the "
                     "wage bill. Displacement therefore widens the funding gap "
                     "mechanically, without any change in asset returns.",
        "size_bn": {"labour_backed_claims_held": round(pens_lb, 1)},
        "can_absorb": "Asset buffers and the long horizon. A funding gap is not a solvency "
                      "event in the year it opens.",
        "cannot_absorb": "A permanent fall in covered payroll. Amortisation schedules are "
                         "set as a share of payroll, so a smaller payroll raises the "
                         "required CONTRIBUTION RATE on the remaining workers and "
                         "employers. For state and local plans that employer is the same "
                         "balanced-budget government in (i), which is how the two exposures "
                         "compound.",
        "why_the_engine_misses_it": "The engine measures claims serviced from wages. A "
                                    "pension promise is serviced from wages too, but it is "
                                    "not a financial claim in the Z.1 sense used here, so "
                                    "it sits outside the labour backing ratio entirely. "
                                    "The 444.6bn above is only what pensions HOLD, not what "
                                    "they OWE against payroll.",
        "status": "SCENARIO on the mechanism; the holding is MEASURED",
    }

    # ------------------------------------------------- (iii) insurers and private credit
    ins_lb = float(H[H.holder == "insurers"].labour_backed_bn.sum())
    oth_lb = float(H[H.holder == "other_financial"].labour_backed_bn.sum())
    tsb = json.loads((LB / "two_sided_bet.json").read_text())
    cf = tsb["ai_leg"]["chicago_fed"]
    out["insurers_and_private_credit"] = {
        "mechanism": "Exposed as HOLDERS on both legs, which makes them the population to "
                     "which the hedge failure proposition applies most directly. Insurers "
                     "hold long-dated wage-backed credit against long-dated liabilities; "
                     "private credit funds hold AI-linked and business credit funded partly "
                     "by bank lines.",
        "size_bn": {
            "insurers, labour-backed claims held": round(ins_lb, 1),
            "other financial (includes private credit), labour-backed claims held":
                round(oth_lb, 1),
            "large bank C and I commitments to AI-adjacent industries":
                cf["large_bank_ci_commitments_ai_bn"],
        },
        "ai_side_verified": {
            "share of total large bank C and I commitments":
                cf["large_bank_ci_commitments_ai_share_of_total"],
            "committed share of tier 1 capital": cf["committed_share_of_tier1"],
            "rated B and below, software": cf["software_rated_b_and_below_bn"],
            "rated B and below, energy and semis": cf["energy_semis_rated_b_and_below_bn"],
            "source": cf["source"],
        },
        "can_absorb": "Insurers hold to maturity against matched liabilities, so mark-to-"
                      "market moves do not force sales the way they do for a leveraged "
                      "holder.",
        "cannot_absorb": "Correlated impairment across BOTH legs at once, which is the "
                         "partial-success regime. This is the one institution class where "
                         "the paper's central proposition has a direct empirical referent, "
                         "and it is why instrument row 9 exists.",
        "gap": "Private credit is INSIDE the Z.1 other-financial aggregate and cannot be "
               "separated from it with the data used here. The 6,186.9bn is therefore an "
               "upper bound on the private credit holding by a wide and unknown margin.",
        "status": "MEASURED holdings; the AI-side figures are verified secondary (A45)",
    }

    (HERE / "a3_omitted_institutions.json").write_text(json.dumps(out, indent=2))

    for k, v in out.items():
        print("=" * 78)
        print(k.upper().replace("_", " "))
        print("  status:", v["status"])
        print("  size, bn:")
        for kk, vv in v["size_bn"].items():
            print(f"    {kk:62s} {vv:>10,.1f}" if isinstance(vv, (int, float))
                  else f"    {kk}: {vv}")
        if "wage_linked_share_of_own_tax_receipts" in v:
            print(f"  wage-linked share of own tax receipts: "
                  f"{v['wage_linked_share_of_own_tax_receipts']:.4f}")


if __name__ == "__main__":
    main()
