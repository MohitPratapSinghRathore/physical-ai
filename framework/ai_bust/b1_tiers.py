"""MODULE B1. The AI side sized in tiers, and the "resembles 2000 or 2008" verdict
restated as a function of which tier you believe.

Each tier carries a confidence label. The point of the exercise is that the project's
existing verdict rests on Tier 1 alone, and Tier 1 is the only tier that is fully sourced.

  TIER 1  HARD. On-balance-sheet AI debt from the nine named SEC filers' own us-gaap facts:
          long-term debt plus finance leases. data/processed/legA_tier2.csv.
  TIER 2  VERIFIED SECONDARY. Large bank C and I commitments to AI-adjacent industries,
          Chicago Fed Insights February 2026, verified at A45. COMMITTED, not drawn; the
          same source puts outstanding at 9 percent of tier 1 capital against 25 percent
          committed, so roughly a third is drawn.
  TIER 3  SCENARIO. Listed AI-exposed equity. There is no clean selection rule that both
          survives scrutiny and is computable from what we have, so this project's existing
          convention is used and labelled: a stated share of US nonfinancial corporate
          equity at Z.1 market value. The share is swept, not estimated.
  TIER 4  NOT SOURCED. Off-balance-sheet data centre vehicles, GPU-backed loans, private
          credit to data centres, data centre ABS and CMBS, vendor financing. BIS Quarterly
          Review March 2026 identifies off-balance-sheet SPV structures as DOMINANT in data
          centre financing. **We have no verified total for any of it.** It is carried as a
          named hole with a solved-for threshold rather than a guess.
  MEMO    Chip supply chain. Named and deliberately not sized: it is an input market, not a
          claim on AI capital, and mixing it into a debt-financed share would double count.

THE VERDICT INDICATOR. The project reads the structure against two verified historical
episodes: 2000 to 2002, equity financed, federal receipts fell 9.5 percent; 2007 to 2009,
debt financed, receipts fell 16.0 percent and corporate tax receipts 53.4 percent. The
boundary values 0.20 and 0.50 on the debt-financed share of capex were read off those
episodes. The existing verdict is "resembles 2000, not 2008" at a debt-financed share of
0.0654.
"""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
PROC = Path(__file__).resolve().parents[2] / "data" / "processed"
LB = Path(__file__).resolve().parents[1] / "labor_backing"

BOUNDARY_2000 = 0.20          # below this, the 2000 equity-financed pattern
BOUNDARY_2008 = 0.50          # above this, the 2008 debt-financed pattern


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    L = pd.read_csv(PROC / "legA_tier2.csv").dropna(subset=["capex"])
    tsb = json.loads((LB / "two_sided_bet.json").read_text())
    cf = tsb["ai_leg"]["chicago_fed"]
    nfc_equity = tsb["ai_leg"]["nonfinancial_corporate_equity_bn"]

    capex = float(L.capex.sum())
    ocf = float(L.ocf.sum())
    excess = float(L.capex_less_ocf.clip(lower=0).sum())   # debt-financed capex, measured
    onbs_debt = float(L.debt_plus_leases.sum())
    share_now = excess / capex

    tiers = [
        {"tier": "1 HARD", "what": "on-balance-sheet AI debt, nine named SEC filers",
         "size_bn": round(onbs_debt, 1), "confidence": "hard, us-gaap facts",
         "in_verdict": "yes, via capex in excess of operating cash flow"},
        {"tier": "2 VERIFIED SECONDARY",
         "what": "large bank C and I commitments to AI-adjacent industries",
         "size_bn": float(cf["large_bank_ci_commitments_ai_bn"]),
         "confidence": "verified secondary, Chicago Fed Insights Feb 2026 (A45)",
         "in_verdict": "NO. Committed, not drawn, and not attributed to capex"},
        {"tier": "2b VERIFIED SECONDARY, drawn",
         "what": "the drawn share of those commitments, implied by the same source",
         "size_bn": round(cf["large_bank_ci_commitments_ai_bn"]
                          * cf["outstanding_share_of_tier1"]
                          / cf["committed_share_of_tier1"], 1),
         "confidence": "implied from outstanding 9 pct vs committed 25 pct of tier 1",
         "in_verdict": "NO"},
        {"tier": "3 SCENARIO", "what": "listed AI-exposed equity, swept share of US "
                                       "nonfinancial corporate equity",
         "size_bn": {f"{int(s*100)} pct": round(nfc_equity * s, 1)
                     for s in tsb["ai_leg"]["ai_equity_share_grid"]},
         "confidence": "SCENARIO. No defensible selection rule computable from our data",
         "in_verdict": "no, it is the equity side"},
        {"tier": "4 NOT SOURCED",
         "what": "off-balance-sheet data centre vehicles, GPU-backed loans, private credit "
                 "to data centres, data centre ABS and CMBS, vendor financing",
         "size_bn": None,
         "confidence": "NOT SOURCED. BIS QR March 2026 calls SPV structures dominant and "
                       "we have no verified total",
         "in_verdict": "NO, and this is the hole the verdict turns on"},
        {"tier": "MEMO", "what": "chip supply chain", "size_bn": None,
         "confidence": "named, deliberately not sized: an input market, not a claim",
         "in_verdict": "no"},
    ]

    # ---- the threshold: how much additional debt-financed capex flips the verdict
    need_2000 = BOUNDARY_2000 * capex - excess
    need_2008 = BOUNDARY_2008 * capex - excess
    commitments = float(cf["large_bank_ci_commitments_ai_bn"])

    curve = []
    for add in [0, 25, 50, 66.1, 100, 150, 213.4, 300, 450]:
        s = (excess + add) / capex
        curve.append({"additional_debt_financed_capex_bn": add,
                      "debt_financed_share": round(s, 4),
                      "verdict": ("resembles 2000" if s < BOUNDARY_2000
                                  else "between" if s < BOUNDARY_2008
                                  else "resembles 2008")})
    C = pd.DataFrame(curve)
    C.to_csv(HERE / "b1_verdict_curve.csv", index=False)

    out = {
        "status": "Tier 1 MEASURED; Tier 2 verified secondary; Tier 3 SCENARIO; "
                  "Tier 4 NOT SOURCED",
        "nine_filers": {"capex_bn": round(capex, 1), "ocf_bn": round(ocf, 1),
                        "debt_financed_capex_bn": round(excess, 1),
                        "on_balance_sheet_debt_bn": round(onbs_debt, 1),
                        "debt_financed_share_of_capex": round(share_now, 4),
                        "self_funding_ratio": round(ocf / capex, 4)},
        "tiers": tiers,
        "verdict_now": "resembles 2000, not 2008",
        "flip_thresholds": {
            "additional_debt_financed_capex_to_reach_0.20_bn": round(need_2000, 1),
            "as_share_of_identified_bank_commitments": round(need_2000 / commitments, 4),
            "additional_to_reach_0.50_bn": round(need_2008, 1),
            "as_share_of_identified_bank_commitments_0.50":
                round(need_2008 / commitments, 4),
        },
        "the_point": "The verdict flips out of the 2000 pattern on "
                     f"{need_2000:.1f}bn of additional debt-financed capex, which is "
                     f"{100*need_2000/commitments:.1f} percent of the bank commitments the "
                     "Chicago Fed has ALREADY identified, and it reaches the 2008 pattern "
                     f"on {need_2008:.1f}bn, which is "
                     f"{100*need_2008/commitments:.1f} percent of them. Tier 4 is "
                     "unmeasured and BIS calls it dominant. **The verdict is therefore "
                     "fragile to a quantity we have not measured, and it should be "
                     "reported as conditional on Tier 1 rather than as a finding about "
                     "the AI financing structure.**",
    }
    (HERE / "b1_tiers.json").write_text(json.dumps(out, indent=2, default=str))

    pd.set_option("display.width", 200)
    print("NINE FILERS, measured")
    for k, v in out["nine_filers"].items():
        print(f"  {k:34s} {v:>12,.4f}" if isinstance(v, float) else f"  {k:34s} {v}")
    print("\nTIERS")
    for t in tiers:
        print(f"  {t['tier']:24s} {str(t['size_bn'])[:46]:48s} {t['confidence'][:52]}")
    print("\nVERDICT AS A FUNCTION OF UNMEASURED DEBT-FINANCED CAPEX")
    print(C.to_string(index=False))
    print(f"\nflip to 'between' at {need_2000:.1f}bn "
          f"({100*need_2000/commitments:.1f} pct of identified bank commitments)")
    print(f"flip to 'resembles 2008' at {need_2008:.1f}bn "
          f"({100*need_2008/commitments:.1f} pct)")


if __name__ == "__main__":
    main()
