"""
Option 2: the euro-area sovereign share of labour-backed claims, against the
US 0.794.

WHAT THIS IS. A STRUCTURE-ONLY comparison. Euro-area claim levels are measured
(ECB QSA). The labour backing coefficients are the US ones, applied unchanged,
because no euro-area equivalent of the ACS/SIPP/SOI build exists here. So this
isolates the effect of INSTITUTIONAL STRUCTURE - the claim mix and who owes what
- from household behaviour. It is NOT the full replication the criterion asked
for, and the sensitivity in section 3 is what decides whether the conclusion
survives that limitation.

QSA OBS_VALUE is in EUR millions.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

US_SOVEREIGN_SHARE = 0.793593        # measurement paper, central
THRESHOLD_PP = 0.15                  # CRITERIA.md option 2

# US coefficients, from claim_class_rules.csv
B_GOVT = 0.657788                    # treasury
B_MORTGAGE = 0.840223
B_CONSUMER = 0.780                   # balance-weighted card/auto/other
B_BUSINESS = 0.0


def main():
    q = json.loads((OUT / "qsa_levels.json").read_text())
    v = {k: (d["value_mn_eur"] / 1e6 if d else np.nan)   # -> EUR trillions
         for k, d in q.items()}
    period = q["govt_debt_securities"]["period"]

    govt = v["govt_debt_securities"] + v["govt_loans"]
    hh_long = v["household_loans_long"]
    hh_short = v["household_loans_short"]
    nfc = v["nfc_debt_securities"] + v["nfc_loans"]

    rows = [
        ("Government debt (securities + loans)", govt, B_GOVT),
        ("Household loans, long term (mortgage proxy)", hh_long, B_MORTGAGE),
        ("Household loans, short term (consumer proxy)", hh_short, B_CONSUMER),
        ("Non-financial corporate debt", nfc, B_BUSINESS),
    ]
    df = pd.DataFrame(rows, columns=["class", "level_tn_eur", "beta"])
    df["labour_backed_tn"] = df["level_tn_eur"] * df["beta"]
    lb_tot = float(df["labour_backed_tn"].sum())

    # sovereign legs
    obligor = float(df.loc[df["class"].str.startswith("Government"),
                           "labour_backed_tn"].iloc[0])
    # holder leg: government and central bank holdings of LOANS (the only
    # labour-backed claims they could hold beyond their own debt). Central bank
    # holdings of government debt securities are the obligor leg already and
    # would be double counted, so they are excluded, matching the US netting.
    holder = (v["govt_holdings_loans"] + v["cb_holdings_loans"]) * B_MORTGAGE
    holder = min(holder, lb_tot - obligor)      # cannot exceed the non-govt leg
    sov = (obligor + holder) / lb_tot

    print(f"EURO AREA, {period}. Levels in EUR trillions.\n")
    print(df.to_string(index=False, float_format=lambda x: f"{x:10,.2f}"))
    print(f"\n  labour-backed stock            {lb_tot:8.2f} tn EUR")
    print(f"  total claim stock (ex equity)  "
          f"{float(df['level_tn_eur'].sum()):8.2f} tn EUR")
    print(f"  labour backing ratio           "
          f"{lb_tot/float(df['level_tn_eur'].sum()):8.4f}")
    print(f"\n  sovereign OBLIGOR leg          {obligor:8.2f} tn "
          f"({obligor/lb_tot:.4f})")
    print(f"  sovereign HOLDER leg           {holder:8.2f} tn "
          f"({holder/lb_tot:.4f})")
    print(f"  EURO AREA SOVEREIGN SHARE      {sov:8.4f}")
    print(f"  US SOVEREIGN SHARE             {US_SOVEREIGN_SHARE:8.4f}")
    gap = US_SOVEREIGN_SHARE - sov
    print(f"  GAP                            {gap:8.4f} "
          f"({gap*100:.1f} percentage points)")
    print(f"  criterion: gap >= {THRESHOLD_PP*100:.0f}pp -> "
          f"{'MET' if gap >= THRESHOLD_PP else 'NOT MET'}")

    # ---- section 3: sensitivity to the borrowed coefficients -------------
    print("\n\nSENSITIVITY. The government coefficient is the one borrowed "
          "assumption that\nmatters: euro-area states run larger social "
          "insurance systems, so their revenue\nmay be MORE labour-linked "
          "than the US 0.658, which would RAISE the euro share\nand shrink "
          "the gap. Varying it, holding the household coefficients fixed:\n")
    sens = []
    for bg in (0.50, 0.55, 0.60, 0.658, 0.70, 0.75, 0.80, 0.85, 0.90):
        lb = govt * bg + hh_long * B_MORTGAGE + hh_short * B_CONSUMER
        ob = govt * bg
        hd = min((v["govt_holdings_loans"] + v["cb_holdings_loans"])
                 * B_MORTGAGE, lb - ob)
        s = (ob + hd) / lb
        g = US_SOVEREIGN_SHARE - s
        sens.append({"beta_govt": bg, "euro_sovereign_share": s,
                     "gap_pp": g * 100, "criterion_met": bool(g >= THRESHOLD_PP)})
        print(f"  beta_govt {bg:.3f} -> euro share {s:.4f}, "
              f"gap {g*100:5.1f}pp, criterion "
              f"{'MET' if g >= THRESHOLD_PP else 'NOT MET'}")
    break_even = None
    for r in sens:
        if not r["criterion_met"]:
            break_even = r["beta_govt"]
            break
    print(f"\n  The gap falls below {THRESHOLD_PP*100:.0f}pp once the "
          f"euro-area government coefficient reaches about "
          f"{break_even if break_even else '>0.90'}.")

    res = {"period": period, "euro_sovereign_share": sov,
           "us_sovereign_share": US_SOVEREIGN_SHARE, "gap": gap,
           "criterion_threshold_pp": THRESHOLD_PP,
           "criterion_met_at_us_coefficients": bool(gap >= THRESHOLD_PP),
           "labour_backed_tn_eur": lb_tot,
           "obligor_leg": obligor / lb_tot, "holder_leg": holder / lb_tot,
           "sensitivity": sens,
           "gap_closes_at_beta_govt": break_even}
    (OUT / "euro_comparison.json").write_text(
        json.dumps(res, indent=2, default=float), encoding="utf-8")
    df.to_csv(OUT / "euro_claim_stock.csv", index=False)


if __name__ == "__main__":
    main()
