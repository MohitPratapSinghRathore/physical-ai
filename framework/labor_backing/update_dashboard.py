"""B12. Add the FAILURE-STATE indicators to the trigger dashboard.

The dashboard already carries AI-lending concentration (bank C and I commitments to
AI-adjacent industries). What it did not carry is the indicator that says which KIND of
bust a failure would be: whether AI capex is funded from operating cash flow, which is the
2000 structure, or from debt, which is the 2008 structure. The two historical anchors
measured in build_ai_leg.py differ sharply in what they did to bank balance sheets and to
federal receipts, and this indicator is what distinguishes them in advance.

Idempotent: rows are keyed on the indicator name and replaced rather than duplicated.
Writes to data/release/dashboard/ by explicit instruction (item B12).
"""
import json, pathlib
import pandas as pd

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[1]
DASH = ROOT / "data" / "release" / "dashboard" / "dashboard.csv"
TODAY = "2026-09-20"


def main():
    two = json.loads((HERE / "two_sided_bet.json").read_text())
    fin = two["financing_structure"]
    d = pd.read_csv(DASH)

    rows = [
        dict(indicator="Debt-financed share of AI capex (FAILURE-STATE indicator)",
             value=round(fin["debt_financed_share_of_capex"], 4),
             threshold="Below about 0.20 the structure resembles the 2000 to 2002 "
                       "EQUITY-financed bust, in which bank losses were small and the "
                       "federal receipts fall was 9.5 percent. Above about 0.50 it "
                       "resembles the 2008 DEBT-financed crisis, receipts fall 16.0 "
                       "percent and corporate tax receipts 53.4 percent",
             status="RESEMBLES 2000, NOT 2008. LOWER BOUND: excludes off-balance-sheet "
                    "and SPV financing, which is not sourced",
             source="SEC XBRL company facts, data/processed/legA_tier2.csv: capex in "
                    "excess of operating cash flow, over capex, across "
                    f"{fin['n_companies']} named filers",
             date=TODAY),
        dict(indicator="AI capex self-funding ratio (operating cash flow over capex)",
             value=round(fin["aggregate_self_funding_ratio"], 4),
             threshold="Above 1.0 the named spenders fund capex internally. Below 1.0 the "
                       "marginal dollar is external. WATCH THE COMPOSITION: "
                       + ", ".join(fin["companies_with_capex_above_ocf"])
                       + " are already below 1.0 individually",
             status="ABOVE 1.0 in aggregate; four of nine filers below it individually",
             source="SEC XBRL company facts, data/processed/legA_tier2.csv",
             date=TODAY),
        dict(indicator="Federal share of labour-backed claims (held, guaranteed or owed)",
             value=round(json.loads(
                 (HERE / "direct_ratio_latest.json").read_text())
                 ["sovereign_exposure"]["share_union"], 4),
             threshold="No threshold exists. Reported because it is the concentration the "
                       "whole thesis turns on, and it roughly doubled between 1970 and 2025",
             status="PROVISIONAL, never independently replicated",
             source="Federal Reserve Z.1 CSV package, framework/labor_backing/",
             date=TODAY),
    ]
    new = pd.DataFrame(rows)
    d = d[~d["indicator"].isin(new["indicator"])]
    out = pd.concat([d, new], ignore_index=True)

    # mark the existing AI-lending row as a failure-state indicator
    m = out["indicator"] == "Bank C and I commitments to AI-adjacent industries"
    out.loc[m, "indicator"] = ("Bank C and I commitments to AI-adjacent industries "
                               "(FAILURE-STATE indicator)")
    out.to_csv(DASH, index=False)
    print(f"dashboard: {len(out)} rows, {len(new)} added or replaced")
    print(out.tail(4)[["indicator", "value", "status"]].to_string(index=False))


if __name__ == "__main__":
    main()
