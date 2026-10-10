"""Does replacing the pro rata allocation with institution-specific loss rates
change WHICH banks a stress test identifies as vulnerable?

The published module allocates each category's system loss in proportion to an
institution's holdings of that category, which assumes every lender in a category has
the same loss rate on it. This replaces that with each bank's own historical loss rate
in each category, relative to the system, holding the SYSTEM TOTAL PER CATEGORY FIXED.
So the comparison is about allocation alone, not about severity.

Shrinkage is not a free parameter. A single bank-year loss rate is mostly noise: the
decomposition in dispersion_decomposition.json puts 26.6 percent of the residual
variance between banks and the rest within. The reliability of a T-year average is
therefore T*rho / (1 + (T-1)*rho) with rho = 0.266, and each bank's relative loss
factor is shrunk toward one by exactly that weight.

Run:  python framework/stress_scoping/reallocate.py
"""
import json
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[2]
INST = ROOT / "framework" / "institutions"
OUT = pathlib.Path(__file__).resolve().parent
PANEL = pathlib.Path(r"C:\Users\bdd3\physical-ai-predict\data\raw\predictive\panel.csv")

RHO = 0.266                      # between-bank share of residual variance, measured
BANK_MIN_LEVERAGE = 0.04         # 12 CFR 217.10(a)(1)(iv)

# category -> (balance fields, charge-off fields) in the call report panel
CATS = {
    "residential":     (["LNRERES"], ["NTRERES"]),
    "credit_card":     (["LNCRCD"], ["NTCRCD"]),
    "other_consumer":  (["LNAUTO", "LNCONOTH"], ["NTAUTO", "NTCONOTH"]),
    "cre":             (["LNRENRES"], ["NTRENRES"]),
    "business_credit": (["LNCI"], ["NTCI"]),
}


def loss_factors():
    """Per bank, per category: historical loss rate relative to the system, shrunk."""
    P = pd.read_csv(PANEL, low_memory=False)
    rows = []
    for cat, (bal, nco) in CATS.items():
        b = P[bal].fillna(0).sum(axis=1)
        n = P[nco].fillna(0).sum(axis=1)
        d = pd.DataFrame({"CERT": P.CERT, "bal": b, "nco": n})
        d = d[d.bal > 0]
        g = d.groupby("CERT").agg(bal=("bal", "sum"), nco=("nco", "sum"),
                                  years=("bal", "size"))
        sys_rate = g.nco.sum() / g.bal.sum()
        g["rate"] = g.nco / g.bal
        g["raw"] = g.rate / sys_rate if sys_rate > 0 else 1.0
        # reliability of a T-year average given the measured persistence
        w = g.years * RHO / (1 + (g.years - 1) * RHO)
        g["factor"] = 1.0 + (g.raw - 1.0) * w
        g["factor"] = g.factor.clip(lower=0.1, upper=5.0)
        g["category"] = cat
        g["system_rate"] = sys_rate
        rows.append(g.reset_index()[["CERT", "category", "factor", "years",
                                     "raw", "system_rate"]])
    return pd.concat(rows, ignore_index=True)


def build_bank_panel():
    B = pd.read_csv(INST / "fdic_institutions_20260630.csv")
    k = 1e6
    return pd.DataFrame({
        "CERT": B.CERT,
        "size_class": B.size_class,
        "business_model": B.business_model,
        "assets": B.ASSET / k,
        "capital": B.RBCT1J / k,
        "residential": B.LNRERES / k,
        "credit_card": B.LNCRCD / k,
        "other_consumer": (B.LNAUTO + B.LNCONOTH) / k,
        "cre": (B.LNRENRES + B.LNRECONS + B.LNREMULT) / k,
        "business_credit": B.LNCI / k,
    }).dropna(subset=["assets", "capital"])


def allocate(P, F, totals, use_factors):
    """Spread each category's system total across banks. Totals held fixed."""
    L = pd.Series(0.0, index=P.index)
    for cat, tot in totals.items():
        held = P[cat].clip(lower=0)
        if use_factors:
            f = P.index.map(F.get(cat, {})).astype(float)
            f = pd.Series(f, index=P.index).fillna(1.0)
            weight = held * f
        else:
            weight = held
        s = weight.sum()
        if s > 0 and tot > 0:
            L = L + tot * weight / s
    return L


def main():
    fac = loss_factors()
    F = {c: dict(zip(g.CERT, g.factor)) for c, g in fac.groupby("category")}
    P = build_bank_panel().set_index("CERT")

    # system loss per category: a fixed severity on the system book, so that the two
    # allocations differ only in how the SAME total is spread
    sev = {"residential": 0.030, "credit_card": 0.150, "other_consumer": 0.060,
           "cre": 0.055, "business_credit": 0.040}
    totals = {c: float(P[c].clip(lower=0).sum() * s) for c, s in sev.items()}

    P["loss_prorata"] = allocate(P, F, totals, False)
    P["loss_specific"] = allocate(P, F, totals, True)
    for m in ("prorata", "specific"):
        P[f"ratio_{m}"] = (P.capital - P[f"loss_{m}"]) / P.assets
        P[f"breach_{m}"] = P[f"ratio_{m}"] < BANK_MIN_LEVERAGE

    cov = P.index.isin(fac.CERT.unique())
    a, b = set(P.index[P.breach_prorata]), set(P.index[P.breach_specific])
    both, only_p, only_s = a & b, a - b, b - a
    jac = len(both) / len(a | b) if (a | b) else float("nan")

    # how far does the loss ORDERING move, among banks with any household book
    m = P[(P.residential + P.credit_card + P.other_consumer) > 0]
    rk = m.loss_prorata.rank().corr(m.loss_specific.rank(), method="spearman")

    res = {
        "description": "Pro rata versus institution-specific allocation of the same system "
                       "loss per category, across the June 2026 FDIC panel.",
        "banks": int(len(P)),
        "banks_with_history": int(cov.sum()),
        "coverage_of_assets": round(float(P.assets[cov].sum() / P.assets.sum()), 4),
        "system_loss_bn": round(float(sum(totals.values())), 1),
        "severities_applied": sev,
        "shrinkage_rho": RHO,
        "breaching_prorata": len(a),
        "breaching_specific": len(b),
        "breaching_both": len(both),
        "only_prorata": len(only_p),
        "only_specific": len(only_s),
        "jaccard_overlap_of_breach_sets": round(float(jac), 4),
        "spearman_of_loss_ordering": round(float(rk), 4),
        "assets_breaching_prorata_pct": round(float(
            100 * P.assets[P.breach_prorata].sum() / P.assets.sum()), 4),
        "assets_breaching_specific_pct": round(float(
            100 * P.assets[P.breach_specific].sum() / P.assets.sum()), 4),
        "factor_spread": {
            c: {"p10": round(float(g.factor.quantile(.10)), 3),
                "median": round(float(g.factor.median()), 3),
                "p90": round(float(g.factor.quantile(.90)), 3)}
            for c, g in fac.groupby("category")},
    }
    (OUT / "reallocation_result.json").write_text(json.dumps(res, indent=2))
    P.reset_index()[["CERT", "size_class", "business_model", "assets", "capital",
                     "loss_prorata", "loss_specific", "breach_prorata",
                     "breach_specific"]].to_csv(OUT / "reallocation_panel.csv", index=False)

    print(f"banks {res['banks']:,}, with history {res['banks_with_history']:,} "
          f"({res['coverage_of_assets']:.1%} of assets)")
    print(f"system loss held fixed at {res['system_loss_bn']:,.1f} bn\n")
    print("institution-specific loss factor, spread within each category")
    for c, v in res["factor_spread"].items():
        print(f"  {c:17s} p10 {v['p10']:5.2f}   median {v['median']:5.2f}   p90 {v['p90']:5.2f}")
    print(f"\nbreaching under pro rata            {res['breaching_prorata']:4d}")
    print(f"breaching under institution-specific{res['breaching_specific']:5d}")
    print(f"  in both                           {res['breaching_both']:4d}")
    print(f"  pro rata only                     {res['only_prorata']:4d}")
    print(f"  institution-specific only         {res['only_specific']:4d}")
    print(f"  overlap of the two sets (Jaccard)  {res['jaccard_overlap_of_breach_sets']:.3f}")
    print(f"\nSpearman of the loss ordering        {res['spearman_of_loss_ordering']:.4f}")


if __name__ == "__main__":
    main()
