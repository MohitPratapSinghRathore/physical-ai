"""MODULE A4. The household-facing instruments, switched on one at a time and together.

This is what replaces "gap closure: not computable" in the architecture wherever it can be
replaced. SCENARIO throughout: the balance sheets are measured, the instruments are not.

THE FIVE INSTRUMENTS, and how each is modelled.

  1. MORTGAGE FORBEARANCE on a displacement trigger. Converts default into deferral for
     displaced borrowers while the trigger is active. Modelled as removing a stated share
     of the FIRST-ROUND residential loss. It cannot touch the second round, because those
     losses come from falling house prices and spending by people who were never displaced.
  2. AUTO the same, on the auto and other-consumer book.
  3. INCOME-DRIVEN STUDENT REPAYMENT with automatic enrolment. The claim already flexes
     with income and the book is 97.28 percent federal, so this converts a default into a
     deferred federal claim. It moves timing and balance sheet, not incidence.
  4. WAGE INSURANCE at a stated replacement rate and duration. This is the only instrument
     that acts on the INCOME rather than on the claim, so it is the only one that reduces
     first-round losses across every book at once AND reduces the fiscal loss.
  5. A CAPITAL TAX at the break-even rate funding that replacement income. Modelled as the
     funding side of instrument 4, not as a separate effect.

THE PASS-THROUGH ASSUMPTION, stated because everything in 4 and 5 rests on it. Household
credit losses are taken to scale linearly with the income shortfall (1 - R). Raising the
retained wage share from R to R' therefore scales first-round losses by (1 - R')/(1 - R).
Linear pass-through is a simplification: real default is convex in the shortfall, because a
household with a small gap draws on buffers and one with a large gap cannot. **So this
UNDERSTATES what wage insurance removes at small doses and OVERSTATES it at large ones.**
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from apply_losses import (build_panel, apply, loss_vector, BANK_MIN_LEVERAGE,
                          CU_MIN_NETWORTH)

HERE = Path(__file__).parent
PROC = Path(__file__).resolve().parents[2] / "data" / "processed"
LB = Path(__file__).resolve().parents[1] / "labor_backing"

# Forbearance take-up and effectiveness. CARES Act forbearance reached about 7 percent of
# mortgages at peak; here the trigger is displacement, so the covered population is the
# displaced, and the question is what share of THEIR default it prevents. Two readings.
FORB_EFFECT = {"partial": 0.50, "full": 0.85}

# Wage insurance. Two designs, both stated rather than optimised.
#   current US: 0.50 replacement for 26 weeks, which is the modal state programme and is on
#   the low side of the OECD (IMF SDN/2024/002).
#   enhanced:   0.70 replacement for 52 weeks.
WAGE_INS = {"current US, 0.50 for 26 weeks": (0.50, 26 / 52),
            "enhanced, 0.70 for 52 weeks": (0.70, 52 / 52)}

FEDERAL_STUDENT_SHARE = 1605.134 / 1650.0


def context(dose, exposure="cognitive_AIOE"):
    """rho, omega, R and the displaced wage bill at this dose."""
    g = pd.read_csv(PROC / "rho_bounded_dose_grid.csv")
    r = g[(g.exposure_type == exposure) & (np.isclose(g.wage_bill_dose, dose))]
    rho = float(r.rho_clamped.iloc[0]) if len(r) and np.isfinite(r.rho_clamped.iloc[0]) \
        else float(r.rho_band_hi.iloc[0])
    inside = bool(r.point_estimate_available.iloc[0]) if len(r) else False
    om = json.loads((PROC / "retained_wage_share_summary.json").read_text()
                    )["omegas"]["counterfactual_blended_central"]
    comp = json.loads((PROC / "capacities.json").read_text())["national_wage_bill_bn"]
    return rho, om, rho * om, comp * dose, inside


def run(dose, band="high"):
    fr, sr, tot, inside_dr = loss_vector(dose, band)
    rho, om, R, D, inside = context(dose)
    P = build_panel()
    base = apply(P, tot, False)
    base_breach_assets = 100 * P.assets[base.breach_min].sum() / P.assets.sum()
    base_breach_n = int(base.breach_min.sum())

    def scenario(name, fr2, fiscal_cost, note):
        t = {k: fr2.get(k, 0.0) + sr.get(k, 0.0) for k in tot}
        R2 = apply(P, t, False)
        removed = sum(tot.values()) - sum(t.values())
        stopped = int(base.breach_min.sum() - R2.breach_min.sum())
        by_model = (P.assign(b0=base.breach_min, b1=R2.breach_min)
                    .groupby("business_model")
                    .apply(lambda d: int(d.b0.sum() - d.b1.sum()), include_groups=False)
                    .to_dict())
        return {"instrument": name, "dose": dose, "band": band,
                "inside_observed_data_range": inside_dr,
                "system_loss_before_bn": round(sum(tot.values()), 2),
                "system_loss_after_bn": round(sum(t.values()), 2),
                "loss_removed_bn": round(removed, 2),
                "loss_removed_pct": round(100 * removed / max(sum(tot.values()), 1e-9), 2),
                "fiscal_cost_bn": fiscal_cost,
                "institutions_breaching_before": base_breach_n,
                "institutions_breaching_after": int(R2.breach_min.sum()),
                "institutions_stopped_breaching": stopped,
                "pct_assets_breaching_before": round(base_breach_assets, 2),
                "pct_assets_breaching_after":
                    round(100 * P.assets[R2.breach_min].sum() / P.assets.sum(), 2),
                "stopped_by_business_model": by_model,
                "note": note}

    rows = []

    # 1 and 2. forbearance
    for tag, eff in FORB_EFFECT.items():
        f2 = dict(fr); f2["residential"] = fr["residential"] * (1 - eff)
        rows.append(scenario(f"mortgage forbearance, {tag} ({eff:.0%} of first-round "
                             "residential default prevented)", f2, None,
                             "fiscal cost NOT SIZED: servicer advances and the carrying "
                             "cost of deferral are real but we have no source for them"))
        f3 = dict(fr); f3["other_consumer"] = fr["other_consumer"] * (1 - eff)
        rows.append(scenario(f"auto and consumer forbearance, {tag}", f3, None,
                             "fiscal cost NOT SIZED; auto has no statutory analogue to "
                             "CARES, so this is contractual"))

    # 3. income-driven student repayment
    stud = float(pd.read_csv(PROC / "dose_response_first_round.csv")
                 .query("exposure_type=='cognitive_AIOE'")
                 .loc[lambda d: np.isclose(d.dose_share_of_total_wage_bill, dose),
                      "student_loan_holders_loss_hi_bn"].max())
    f4 = dict(fr); f4["other_consumer"] = max(fr["other_consumer"] - stud, 0.0)
    rows.append(scenario("income-driven student repayment, automatic enrolment", f4,
                         round(stud * FEDERAL_STUDENT_SHARE, 2),
                         "fiscal cost is the deferred FEDERAL claim, 97.28 pct of the "
                         "book. It moves timing and balance sheet, not incidence"))

    # 4 and 5. wage insurance, and the capital tax that would fund it
    for tag, (rate, frac) in WAGE_INS.items():
        add = (1 - rho) * rate * frac
        R2 = min(R + add, 0.999)
        scale = (1 - R2) / max(1 - R, 1e-9)
        f5 = {k: v * scale for k, v in fr.items()}
        cost = add * D
        rows.append(scenario(f"wage insurance, {tag}", f5, round(cost, 2),
                             f"raises the retained wage share from {R:.4f} to {R2:.4f}; "
                             f"fiscal cost is the benefit paid. Funding it from a capital "
                             f"tax is the section 5.1 question and is NOT separately sized, "
                             f"because the surplus base is undefined"))

    # ALL TOGETHER: best forbearance, IDR, and enhanced wage insurance
    rate, frac = WAGE_INS["enhanced, 0.70 for 52 weeks"]
    add = (1 - rho) * rate * frac
    R2 = min(R + add, 0.999)
    scale = (1 - R2) / max(1 - R, 1e-9)
    fa = {k: v * scale for k, v in fr.items()}
    fa["residential"] *= (1 - FORB_EFFECT["full"])
    fa["other_consumer"] = max(fa["other_consumer"] * (1 - FORB_EFFECT["full"])
                               - stud * scale, 0.0)
    rows.append(scenario("ALL TOGETHER: forbearance (full) + IDR + enhanced wage insurance",
                         fa, round(add * D + stud * FEDERAL_STUDENT_SHARE * scale, 2),
                         "the combined package"))
    return rows


def main():
    allrows = []
    for dose in [0.10, 0.25, 0.50]:
        allrows += run(dose)
    R = pd.DataFrame(allrows)
    R.drop(columns=["stopped_by_business_model"]).to_csv(
        HERE / "a4_instrument_results.csv", index=False)
    (HERE / "a4_instrument_results.json").write_text(json.dumps(allrows, indent=2))

    pd.set_option("display.width", 240)
    pd.set_option("display.max_colwidth", 56)
    for dose in [0.10, 0.25, 0.50]:
        d = R[R.dose == dose]
        print(f"\n{'='*110}\nDOSE {dose:.0%}   inside observed data: "
              f"{bool(d.inside_observed_data_range.iloc[0])}   "
              f"system loss before {d.system_loss_before_bn.iloc[0]:,.1f}bn   "
              f"breaching {d.institutions_breaching_before.iloc[0]} "
              f"({d.pct_assets_breaching_before.iloc[0]:.2f} pct of assets)")
        print(d[["instrument", "loss_removed_bn", "loss_removed_pct", "fiscal_cost_bn",
                 "institutions_stopped_breaching", "pct_assets_breaching_after"]]
              .to_string(index=False))


if __name__ == "__main__":
    main()
