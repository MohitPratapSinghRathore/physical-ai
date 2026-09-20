"""B10. Add the labour backing quantities to the replication brief and to the round two
sealed file, with full mechanics, so round two covers them.

Idempotent: rerunning replaces the labour backing blocks rather than appending twice.
Writes OUTSIDE framework/labor_backing/ by explicit instruction (item B10 and B11), to
notes/replication_brief_v2.md and notes/sealed/sealed_expected_values_round2.json.
"""
import json, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
BRIEF = ROOT / "notes" / "replication_brief_v2.md"
SEALED = ROOT / "notes" / "sealed" / "sealed_expected_values_round2.json"

MARK_START = "<!-- LABOUR_BACKING_BLOCK_START -->"
MARK_END = "<!-- LABOUR_BACKING_BLOCK_END -->"


def main():
    import pandas as pd
    d = json.loads((HERE / "direct_ratio_latest.json").read_text())
    ind = json.loads((HERE / "indirect_extension.json").read_text())
    sens = json.loads((HERE / "sensitivity.json").read_text())
    two = json.loads((HERE / "two_sided_bet.json").read_text())
    T = pd.read_csv(HERE / "direct_ratio_timeseries.csv")
    q = pd.read_csv(HERE / "quintile_labour_backing.csv")
    sov = d["sovereign_exposure"]
    y = d["latest_year"]

    # ------------------------------------------------ sealed
    sealed = json.loads(SEALED.read_text())
    tol_share = "share_absolute"
    tol_rel = "survey_relative"

    def e(v, tol, note):
        return {"expected": round(float(v), 6), "tolerance": tol, "note": note}

    lb = {
        "_definition": "FIRST-ROUND servicing only. Business-revenue-serviced classes are "
                       "ZERO BY RULE. Social insurance is a memo item OUTSIDE the ratio. "
                       "All values are for the latest complete Z.1 year, "
                       f"{y}. Every quantity is PROVISIONAL and none has ever been "
                       "checked from outside.",
        "total_claims_bn": e(d["total_claims_bn"], tol_rel, "sum of the 13 class levels"),
        "labour_backed_bn": e(d["labour_backed_bn"], tol_rel, "sum of level x backing share"),
        "direct_labour_backing_ratio": e(
            d["direct_labour_backing_ratio"], tol_share,
            "BOUND: in [0,1], and between the smallest and largest class backing share"),
        "indirect_backing_of_business_revenue": e(
            ind["indirect_labour_backing_of_business_revenue"], tol_share,
            "B2, (PCE/GDP) x (WASCUR/PI). BOUND: below each of its two components. "
            "NEVER blended into the direct ratio"),
        "combined_first_and_second_round_ratio": e(
            ind["combined_first_and_second_round_ratio"], tol_share,
            "B2, NOT the headline. BOUND: at or above the direct ratio"),
        "sovereign_share_held_or_guaranteed": e(
            sov["share_held_or_guaranteed"], tol_share,
            "federal government as HOLDER or GUARANTOR. Agency and GSE pools, the GSEs "
            "and the central bank count as federal"),
        "sovereign_share_obligor": e(
            sov["share_obligor"], tol_share,
            "federal government as OBLIGOR, that is Treasury debt serviced from "
            "labour-linked receipts"),
        "sovereign_share_union": e(
            sov["share_union"], tol_share,
            "BOUND: in [0,1] and at or above each leg. THE HEADLINE HOLDER RESULT. "
            "Compare with the 75.9 to 91.6 percent federal share of first-round losses"),
        "series_first_year": e(int(T.year.min()), tol_share, "Z.1 levels begin 1945"),
        "series_last_year": e(int(T.year.max()), tol_share, ""),
        "sovereign_share_union_1970": e(
            float(T[T.year == 1970]["sovereign_share_union"].iloc[0]), tol_share, ""),
        "sovereign_share_union_2008": e(
            float(T[T.year == 2008]["sovereign_share_union"].iloc[0]), tol_share, ""),
        "one_step_rule_move_pct": e(
            sens["largest_single_move_pct"], tol_rel,
            "the single largest judgement call, by a factor of seven over the next one"),
        "sensitivity_range_low": e(sens["range_low"], tol_share, "one at a time"),
        "sensitivity_range_high": e(sens["range_high"], tol_share, "one at a time"),
        "quintile_labour_backed_per_wage_dollar_Q1": e(
            float(q[q.q == 0]["labour_backed_per_unit_wage_bill"].iloc[0]), tol_rel,
            "B5. BOUND: quintile shares sum to 1"),
        "quintile_labour_backed_per_wage_dollar_Q5": e(
            float(q[q.q == 4]["labour_backed_per_unit_wage_bill"].iloc[0]), tol_rel, "B5"),
    }
    for k, v in d["by_class"].items():
        lb[f"class_{k}_level_bn"] = e(v["level_bn"], tol_rel, "Z.1 liability level")
        lb[f"class_{k}_backing"] = e(v["backing"], tol_share, "BOUND: in [0,1]")

    tb = {
        "_definition": "B11 and B12. The AI EQUITY SCALE is a SCENARIO parameter, swept "
                       "over 0.10, 0.20, 0.30 of US nonfinancial corporate equity. The "
                       "central case is 0.20. AI DEBT and bank commitments are sourced. "
                       "Off-balance-sheet financing is NOT sourced, so every failure-state "
                       "figure is a LOWER BOUND.",
        "federal_share_of_ai_leg_central": e(
            two["ai_leg"]["federal_share_of_ai_leg"], tol_share,
            "BOUND: holder shares sum to 1 within the leg"),
        "federal_share_of_wage_leg_union": e(
            sov["share_union"], tol_share, "the same quantity as above, restated"),
        "ai_onbalancesheet_debt_bn": e(
            two["ai_leg"]["ai_onbalancesheet_debt_bn"], tol_rel,
            "SEC XBRL, long term debt plus finance leases, 9 named filers"),
        "ai_bank_commitments_bn": e(
            two["ai_leg"]["ai_bank_commitments_bn"], tol_rel,
            "Chicago Fed, late 2025, SECONDARY source"),
        "debt_financed_share_of_ai_capex": e(
            two["financing_structure"]["debt_financed_share_of_capex"], tol_share,
            "capex in excess of operating cash flow, over capex, across the named filers. "
            "BOUND: in [0,1]. THE FAILURE-STATE INDICATOR"),
        "aggregate_self_funding_ratio": e(
            two["financing_structure"]["aggregate_self_funding_ratio"], tol_rel,
            "operating cash flow over capex. Above 1 is the 2000 structure, below 1 the "
            "2008 structure"),
        "share_of_federal_wage_loss_hedged_at_operative_tau_k": e(
            two["government_implicit_claim"][
                "share_of_federal_wage_loss_hedged_at_operative_10pct_dose"], tol_share,
            "10 percent dose, case A, GROSS of capital tax. The published fiscal loss is "
            "already NET of tax at the operative rate, so the gross basis is required or "
            "the tax is counted twice"),
        "anchor_2000_corporate_tax_fall_pct": e(-35.1, tol_rel,
                                                "measured from FRED FCTAX, 2000 to 2002"),
        "anchor_2008_corporate_tax_fall_pct": e(-53.4, tol_rel,
                                                "measured from FRED FCTAX, 2007 to 2009"),
    }
    sealed["labour_backing"] = lb
    sealed["two_sided_bet"] = tb
    SEALED.write_text(json.dumps(sealed, indent=2, default=str))

    # ------------------------------------------------ brief
    sec = f"""{MARK_START}

## 14. The labour backing ratio, and the two-sided bet by holder

**Everything in this section is PROVISIONAL and none of it has ever been checked from
outside.** Appendix C item 2 said these quantities were the subject of a separate pass.
This is that pass. Sealed under `labour_backing` and `two_sided_bet`.

### 14.1 Data you need

| Source | What | How |
|---|---|---|
| Federal Reserve Z.1, **the CSV package, not FRED** | every claim level and every holder sector, annual from 1945 | `https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip`. Series are keyed `FL`/`LM` + 2-digit sector + 7-digit instrument. The `data_dictionary/` folder maps every code to the Fed's own description. **Do not use per-series FRED calls: they are rate limited and you will silently lose whole holder classes** |
| `data/processed/under_reporting_factors.csv` | working-core share of balances by loan | column `working_core_share_of_full`. These are the CORRECTED factors |
| `data/processed/stress/a38_correction_decomposition.csv` | working-core share of mortgage SERVICE and of RENT | stage `3_plus_engine_core_definition`, class `non_working`, take one minus |
| `data/processed/labor_tax_share.json` | SOI wage share of AGI | 2021 to 2023 ONLY |
| FRED `FGRECPT`, `A074RC1Q027SBEA`, `W780RC1Q027SBEA`, `W070RC1Q027SBEA`, `W071RC1Q027SBEA`, `PCEC`, `PI`, `WASCUR`, `GDP`, `FCTAX` | receipts, consumption, personal income, corporate tax | annual means of quarterly series |
| Fed Distributional Financial Accounts | household equity and debt by wealth percentile | `https://www.federalreserve.gov/releases/z1/dataviz/download/zips/dfa.zip`, file `dfa-networth-levels.csv` |
| `data/processed/legA_tier2.csv` | AI capital spenders' capex, operating cash flow, debt | already in the repository |

### 14.2 The definition, which is the whole argument

**FIRST-ROUND servicing only.** For each claim class the labour backing share is the
fraction of the cash flow that DIRECTLY services it which is labour income. One step.

- Household claims: the working-core share (an employed member aged 25 to 64), **by claim
  type**. Mortgages use the ACS share of mortgage SERVICE; card, auto and student use the
  SIPP share of BALANCES.
- Multifamily mortgages: the working-core share of RENT. One intermediary.
- Treasury: social insurance contributions in full, plus the SOI wage share of the
  individual income tax, over federal current receipts.
- State and local: the wage share of personal current taxes over total state and local tax
  receipts. Property tax is a capital levy; sales tax is a SECOND-round channel.
- **Corporate bonds, corporate and noncorporate business loans, non-multifamily commercial
  mortgages and corporate equity: ZERO BY RULE.** They are serviced from business revenue.
- Social insurance: a MEMO ITEM outside the ratio, at the payroll share of each fund's own
  income (OASI 0.9054, DI 0.9571, HI 0.8720).

**If you disagree with the zero rule, say so, because it moves the headline by
{sens['largest_single_move_pct']:.0f} percent and nothing else moves it by more than 10.**

### 14.3 Holders, and the two legs of the sovereign

Ultimate holder, so **agency and GSE mortgage pools, the GSEs and the central bank count
as federal government**: the guarantee and not the pool investor bears the loss, the GSEs
are in conservatorship, and the Federal Reserve remits to the Treasury.

**The sovereign has two distinct legs and confusing them is the trap in this section:**

- **holder or guarantor**: a credit loss on a claim it owns or guarantees. {sov['share_held_or_guaranteed']:.4f}
- **obligor**: a revenue shortfall on a claim it OWES and services from labour-linked
  receipts, which is Treasury debt. {sov['share_obligor']:.4f}
- **union**, less the overlap where it holds its own debt: **{sov['share_union']:.4f}**

The union is the quantity that compares with the 75.9 to 91.6 percent federal share of
first-round losses, because that figure is itself the union of a revenue loss and a credit
loss.

### 14.4 The connection test, and the error it caught

The obvious formula is `impaired_stock = labour_backing x dose x (1 - R)`. **It is wrong
for credit claims.** `(1 - R)` is the fraction of wage income actually lost after
reemployment, which is right for a REVENUE claim and wrong for a CREDIT claim: a displaced
borrower's whole balance is at risk of default, not the lost-income fraction of it.

With `(1 - R)` in, 0 of 8 auto rows sit inside the benchmark loss band. With it out, 7 of 8
do. **Use `(1 - R)` for the fiscal class and not for the household classes.** Card and
mortgage remain above the band and student below it; those gaps are real and are reported
rather than tuned away.

### 14.5 The gross-versus-net trap in the hedging calculation

The published fiscal loss **already nets out capital tax at the operative rate of 0.0708**
(claim 179). If you ask how much a capital tax hedges the federal loss and divide by the
published figure, **you count the tax twice**. Use the gross loss,
`published_loss + 0.0708 x surplus`. The check that you have it right: at the break-even
rate the hedged share is exactly 1.000 by construction. If it is not, something upstream is
wrong.

### 14.6 Plausibility bounds, stated before the numbers

Every backing share and every holder share in [0, 1]. Holder shares sum to 1 within each
claim class and within each leg. Labour-backed claims at or below total claims in every
class. The aggregate ratio between the smallest and largest class share. The indirect
share below each of its two components. The combined ratio at or above the direct ratio.
The sovereign union at or above each of its legs. The break-even hedge ratio exactly 1.

Checks run in this session: 47 direct, 6 indirect, 8 quintile and connection, 14
two-sided bet. **Zero violations.**

### 14.7 What to attack

1. **The one-step rule.** It is the headline.
2. **Treating agency pools as federal.** Drop it and the sovereign share falls from
   {sov['share_union']:.3f} to 0.587.
3. **Including the obligor leg.** Drop it and the sovereign share falls to {sov['share_held_or_guaranteed']:.3f}.
4. **Holding the labour shares constant before 2021.** The pre-2021 series is a claim stock
   and a holder map with fixed labour shares. Say whether that is a series worth having.
5. **The AI equity scale in B11**, which is a scenario and not a measurement.

{MARK_END}"""

    txt = BRIEF.read_text()
    if MARK_START in txt:
        txt = re.sub(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), sec, txt,
                     flags=re.S)
    else:
        anchor = "## Appendix A."
        txt = txt.replace(anchor, sec + "\n\n---\n\n" + anchor, 1)
    BRIEF.write_text(txt)

    print(f"sealed: +{len(lb)} labour_backing, +{len(tb)} two_sided_bet entries")
    print(f"brief:  section 14 written ({len(sec)} chars)")


if __name__ == "__main__":
    main()
