"""
The 1947-65 exit, and why it is closed. Built from the session 3 panel.

Reports GROWTH MULTIPLES rather than share changes for the historical episode,
and a genuine ratio (state-held household credit over household credit) for the
guarantee rate, both deliberately, because K4_RESULT.md withdrew an earlier
finding that read a share change as behaviour while its denominator moved.
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
P2 = HERE.parent / "paper2"
HH = ["home_mortgage", "credit_card", "auto_loan", "student_loan",
      "other_consumer"]


def main():
    P = pd.read_csv(P2 / "s3_programme_panel.csv")
    S2 = pd.read_csv(P2 / "s2_series.csv").set_index("year")
    K = pd.read_csv(HERE / "k4_denominator_test.csv").set_index("year")

    rows = []
    for y, g in P.groupby("year"):
        lb = g["level_bn"] * g["beta_central"]
        tot = float(lb.sum())
        rows.append(dict(
            year=int(y), lb=tot,
            treasury=float(lb[g["claim_class"] == "treasury"].sum()),
            household=float(lb[g["claim_class"].isin(HH)].sum())))
    S = pd.DataFrame(rows).set_index("year")

    a, b = 1947, 1965
    print("THE 1947-65 EXIT, in growth multiples")
    for c in ("lb", "treasury", "household"):
        print(f"  {c:10s} x{S[c][b] / S[c][a]:.2f}")
    print(f"  sovereign share {S2.central_union[a]:.4f} -> "
          f"{S2.central_union[b]:.4f}")

    print("\nSTATE SHARE OF HOUSEHOLD CREDIT (a genuine ratio)")
    for y in (1947, 1965, 1980, 2000, 2007, 2025):
        print(f"  {y}: {K.hh_total[y]:.4f}")

    g = P[P["year"] == 2025]
    lb = g["level_bn"] * g["beta_central"]
    tot = float(lb.sum())
    tre = float(lb[g["claim_class"] == "treasury"].sum())
    hh = float(lb[g["claim_class"].isin(HH)].sum())
    other = tot - tre - hh
    hold = S2.central_holder[2025] * tot
    ov = (S2.central_holder[2025] + S2.central_obligor[2025]
          - S2.central_union[2025]) * tot
    rate = K.hh_total[2025]

    print("\nCOUNTERFACTUAL: expand household credit, Treasury fixed")
    print(f"{'x':>6} {'guarantee 0%':>14} {'guarantee 56%':>15}")
    out = []
    for m in (1, 2, 3, 5, 7.61):
        hh2 = hh * m
        tot2 = tre + hh2 + other
        a0 = (hold + tre - ov) / tot2
        a1 = (hold + rate * (hh2 - hh) + tre - ov) / tot2
        out.append(dict(multiple=m, guarantee_zero=a0, guarantee_today=a1))
        print(f"{m:6.2f} {a0:14.4f} {a1:15.4f}")
    pd.DataFrame(out).to_csv(HERE / "exit_counterfactual.csv", index=False)


if __name__ == "__main__":
    main()
