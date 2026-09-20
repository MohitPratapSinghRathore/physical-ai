"""MODULE A2. Losses applied institution by institution, and the DISTRIBUTION reported.

STATUS. The balance sheets are MEASURED (FDIC and NCUA, 2026-06-30). Everything this
module does with them is SCENARIO: it takes loss totals that are themselves conditional on
a displacement level and allocates them across real institutions.

WHAT IS ALLOCATED, and why there is no double counting.
  FIRST ROUND, from data/processed/dose_response_first_round.csv. Household defaults only.
    The business-credit and commercial-real-estate columns are ZERO in the first round, which
    was checked before writing this: the first-round engine measures displaced households
    defaulting on their own obligations and nothing else.
  SECOND ROUND, from data/processed/second_round_fed_mapping.csv, already decomposed into
    the Federal Reserve's own 2026 severely adverse loan categories. This is where commercial
    real estate, C and I and "other" enter.

ALLOCATION RULE, stated because it is the main assumption. Each category's system loss is
spread across institutions in proportion to that institution's holdings of that category.
That is a pro-rata rule: it assumes every lender in a category has the same loss rate on it.
Real loss rates differ by underwriting, geography and vintage, and the Federal Reserve's own
stress test reports a wide range across banks within a category (credit cards 9.5 to 22.7
percent, C and I 3.4 to 48.5). **So the DISPERSION reported here is driven entirely by
differences in business mix, not by differences in underwriting quality, and it is therefore
a LOWER bound on true dispersion.** Stated, not hidden.

CAPITAL TEST.
  Banks: tier 1 leverage ratio, tier 1 capital over total assets, against the 4 percent
    regulatory minimum in 12 CFR 217.10(a)(1)(iv). The 5 percent well-capitalised threshold
    is reported alongside.
  Credit unions: net worth ratio against the 6 percent "adequately capitalised" threshold of
    12 USC 1790d, with 7 percent "well capitalised" alongside.

EARNINGS OFFSET. Reported both ways. Without an offset, losses hit capital directly, which
overstates breaches because a bank earning money absorbs some of the loss from income. With
the offset, one year of annualised net income is available first. Neither is "the" answer;
the pair brackets it.

NO INSTITUTION IS NAMED. The instruction is explicit and the pro-rata rule would not support
it anyway: this identifies exposed BUSINESS MODELS, not likely failures.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
PROC = Path(__file__).resolve().parents[2] / "data" / "processed"

BANK_MIN_LEVERAGE = 0.04        # 12 CFR 217.10(a)(1)(iv)
BANK_WELLCAP = 0.05
CU_MIN_NETWORTH = 0.06          # 12 USC 1790d, adequately capitalised
CU_WELLCAP = 0.07


def build_panel():
    """One row per institution, loan book in bn, capital in bn, on a common schema."""
    B = pd.read_csv(HERE / "fdic_institutions_20260630.csv")
    k = 1e6                                     # FDIC reports thousands -> bn
    b = pd.DataFrame({
        "id": "FDIC-" + B.CERT.astype(str),
        "kind": "bank",
        "size_class": B.size_class,
        "business_model": B.business_model,
        "assets": B.ASSET / k,
        "capital": B.RBCT1J / k,
        "earnings_1y": (B.NETINC / k) * 2.0,    # year to date at 2026-06-30, annualised
        "residential": B.LNRERES / k,
        "credit_card": B.LNCRCD / k,
        "other_consumer": (B.LNAUTO + B.LNCONOTH) / k,
        "cre": (B.LNRENRES + B.LNRECONS + B.LNREMULT) / k,
        "business_credit": B.LNCI / k,
        "total_loans": B.LNLSNET / k,
    })
    C = pd.read_csv(HERE / "ncua_institutions_202606.csv")
    g = 1e9                                     # NCUA reports dollars -> bn
    c = pd.DataFrame({
        "id": "NCUA-" + C.CU_NUMBER.astype(str),
        "kind": "credit union",
        "size_class": C.size_class,
        "business_model": "credit union",
        "assets": C.assets / g,
        "capital": C.net_worth / g,
        "earnings_1y": 0.0,                     # not extracted; see limitation
        "residential": C.residential / g,
        "credit_card": C.credit_card / g,
        "other_consumer": (C.auto + C.consumer_other) / g,
        "cre": 0.0,
        "business_credit": 0.0,
        "total_loans": C.total_measured_loans / g,
    })
    P = pd.concat([b, c], ignore_index=True)
    P = P[P.assets > 0]

    # ---- COVERAGE EXCLUSION, found by the baseline plausibility check.
    # 17 banks report no capital at all (tier 1 and total equity both zero or absent) and
    # 263.2bn of assets between them. They are almost entirely BKCLASS "OI", insured US
    # branches of foreign chartered institutions, whose capital is held at the parent and
    # is therefore outside FDIC reporting. Seven credit unions likewise report no net worth.
    # Leaving them in produced 53 institutions "breaching" the minimum with ZERO losses
    # applied, which is not a fact about the banking system but a missing field read as a
    # zero. They are EXCLUDED from the capital test and the exclusion is reported.
    no_cap = P.capital <= 0
    P.attrs["excluded_n"] = int(no_cap.sum())
    P.attrs["excluded_assets_bn"] = float(P.assets[no_cap].sum())
    P = P[~no_cap]
    return P.reset_index(drop=True)


def loss_vector(dose, band, exposure="cognitive_AIOE"):
    """System loss by category, bn. First round household-only, plus second round."""
    D = pd.read_csv(PROC / "dose_response_first_round.csv")
    d = D[(np.isclose(D.dose_share_of_total_wage_bill, dose))
          & (D.exposure_type == exposure)]
    sfx = "_hi_bn" if band == "high" else "_lo_bn"
    fr = {
        "residential": float(d["mortgage_bank_held_loss" + sfx].max()),
        "credit_card": float(d["card_consumer_lenders_loss" + sfx].max()),
        # student is 97.28 pct federal; only the private slice reaches these balance sheets
        "other_consumer": float(d["auto_lenders_loss" + sfx].max())
                          + float(d["student_loan_holders_loss" + sfx].max()),
        "cre": 0.0, "business_credit": 0.0, "other": 0.0,
    }
    S = pd.read_csv(PROC / "second_round_fed_mapping.csv")
    s = S[(np.isclose(S.dose, dose)) & (S.exposure_type == exposure)
          & (S.band == band)]
    sr = {"residential": 0.0, "credit_card": 0.0, "other_consumer": 0.0,
          "cre": 0.0, "business_credit": 0.0, "other": 0.0}
    if len(s):
        r = s.iloc[0]
        sr = {
            "residential": float(r.first_lien_mortgage_bn) + float(r.junior_heloc_bn),
            "credit_card": float(r.credit_card_bn),
            "other_consumer": float(r.other_consumer_bn),
            "cre": float(r.cre_bn),
            "business_credit": float(r.business_credit_bn),
            "other": float(r.other_bn),
        }
    tot = {k: fr[k] + sr[k] for k in fr}
    inside = bool(d.inside_observed_data_range.any()) if len(d) else False
    return fr, sr, tot, inside


def apply(P, tot, earnings_offset):
    """Allocate each category pro rata by holdings and test capital."""
    L = pd.Series(0.0, index=P.index)
    for cat in ["residential", "credit_card", "other_consumer", "cre", "business_credit"]:
        held = P[cat]
        s = held.sum()
        if s > 0 and tot.get(cat, 0) > 0:
            L = L + tot[cat] * held / s
    # "other" has no matching book; spread on total loans
    s = P.total_loans.sum()
    if s > 0 and tot.get("other", 0) > 0:
        L = L + tot["other"] * P.total_loans / s

    buffer = P.capital + (P.earnings_1y.clip(lower=0) if earnings_offset else 0.0)
    after = buffer - L
    ratio = after / P.assets
    is_bank = P.kind == "bank"
    minimum = np.where(is_bank, BANK_MIN_LEVERAGE, CU_MIN_NETWORTH)
    wellcap = np.where(is_bank, BANK_WELLCAP, CU_WELLCAP)
    return pd.DataFrame({
        "loss": L, "capital_after": after, "ratio_after": ratio,
        "breach_min": ratio < minimum, "below_wellcap": ratio < wellcap,
    })


def summarise(P, R, by):
    g = P.assign(**R).groupby(by)
    out = g.apply(lambda d: pd.Series({
        "n": len(d),
        "assets_bn": d.assets.sum(),
        "loss_bn": d.loss.sum(),
        "n_breach": int(d.breach_min.sum()),
        "pct_institutions_breaching": 100 * d.breach_min.mean(),
        "pct_assets_breaching": 100 * d.loc[d.breach_min, "assets"].sum()
                                / max(d.assets.sum(), 1e-9),
        "pct_assets_below_wellcap": 100 * d.loc[d.below_wellcap, "assets"].sum()
                                    / max(d.assets.sum(), 1e-9),
    }), include_groups=False)
    return out.round(2)


def main():
    P = build_panel()

    # ---- BASELINE CHECK, run first and reported. A capital test is only meaningful if
    # essentially nobody fails it before any loss is applied.
    zero = {k: 0.0 for k in ["residential", "credit_card", "other_consumer", "cre",
                             "business_credit", "other"]}
    B0 = apply(P, zero, False)
    base = {"n_breaching": int(B0.breach_min.sum()),
            "pct_institutions": round(100 * float(B0.breach_min.mean()), 3),
            "pct_assets": round(100 * float(P.assets[B0.breach_min].sum()
                                            / P.assets.sum()), 3)}
    print("BASELINE, zero losses applied:", base)
    print()

    doses = [0.05, 0.10, 0.25, 0.50, 0.75]
    rows, detail = [], []
    for dose in doses:
        for band in ["low", "high"]:
            fr, sr, tot, inside = loss_vector(dose, band)
            for off in [False, True]:
                R = apply(P, tot, off)
                rows.append({
                    "dose": dose, "band": band, "earnings_offset": off,
                    "inside_observed_data_range": inside,
                    "system_loss_bn": round(sum(tot.values()), 2),
                    "first_round_bn": round(sum(fr.values()), 2),
                    "second_round_bn": round(sum(sr.values()), 2),
                    "n_breaching": int(R.breach_min.sum()),
                    "pct_institutions_breaching": round(100 * R.breach_min.mean(), 2),
                    "pct_system_assets_breaching":
                        round(100 * P.assets[R.breach_min].sum() / P.assets.sum(), 2),
                    "pct_system_assets_below_wellcap":
                        round(100 * P.assets[R.below_wellcap].sum() / P.assets.sum(), 2),
                })
                if band == "high" and not off:
                    for by, tag in [("size_class", "size"), ("business_model", "model")]:
                        s = summarise(P, R, by).reset_index()
                        s.insert(0, "cut", tag)
                        s.insert(0, "dose", dose)
                        detail.append(s)
    Res = pd.DataFrame(rows)
    Res.to_csv(HERE / "a2_system_results.csv", index=False)
    Det = pd.concat(detail, ignore_index=True)
    Det.to_csv(HERE / "a2_distribution_by_class.csv", index=False)

    (HERE / "a2_summary.json").write_text(json.dumps({
        "status": "SCENARIO. Balance sheets measured; loss application conditional.",
        "n_institutions": int(len(P)),
        "n_banks": int((P.kind == "bank").sum()),
        "n_credit_unions": int((P.kind == "credit union").sum()),
        "system_assets_bn": round(float(P.assets.sum()), 1),
        "system_capital_bn": round(float(P.capital.sum()), 1),
        "excluded_no_capital_reported": {
            "n": P.attrs.get("excluded_n"),
            "assets_bn": round(P.attrs.get("excluded_assets_bn", 0.0), 1),
            "why": "tier 1 and total equity both absent; overwhelmingly insured US "
                   "branches of foreign chartered institutions (FDIC BKCLASS OI) whose "
                   "capital is held at the parent. Found by the baseline check, which "
                   "showed them breaching with zero losses applied."},
        "baseline_breaches_after_exclusion": base,
        "capital_test": {
            "banks": "tier 1 leverage vs 4 pct, 12 CFR 217.10(a)(1)(iv)",
            "credit_unions": "net worth ratio vs 6 pct, 12 USC 1790d"},
        "allocation": "pro rata by category holdings; dispersion here is business mix "
                      "only, so it is a LOWER bound on true dispersion",
    }, indent=2))

    pd.set_option("display.width", 220)
    print("SYSTEM RESULTS, no earnings offset unless marked")
    print(Res[["dose", "band", "earnings_offset", "inside_observed_data_range",
               "system_loss_bn", "n_breaching", "pct_institutions_breaching",
               "pct_system_assets_breaching"]].to_string(index=False))
    print()
    for tag, label in [("size", "BY SIZE CLASS"), ("model", "BY BUSINESS MODEL")]:
        print(f"\n{label}, high band, no earnings offset")
        d = Det[(Det.cut == tag) & (Det.dose.isin([0.10, 0.25, 0.50]))]
        col = "size_class" if tag == "size" else "business_model"
        print(d[["dose", col, "n", "assets_bn", "loss_bn",
                 "pct_institutions_breaching", "pct_assets_breaching"]]
              .to_string(index=False))


if __name__ == "__main__":
    main()
