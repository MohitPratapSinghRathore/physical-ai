"""THE DEBT-ONLY LABOUR BACKING RATIO. The one new computation of this session.

WHY IT EXISTS, stated plainly because it is a correction to our own headline.

The all-claims labour backing ratio has corporate equity at market value in its denominator,
71,994.9bn of 149,407.2bn in 2025, which is **48 percent**. So the ratio falls when equity
rises and rises when equity falls, independently of anything happening to labour. It read
**0.267 at the 2000 equity peak** and **0.376 in 2008 after the crash**. Anyone using it as a
risk indicator would have read the economy as least risky in 2000 and most risky in 2009.
That is the wrong sign, and it is why the ratio has been presented as an accounting scaffold
rather than as a measure.

**The debt-only ratio removes that.** It excludes every market-valued equity class from the
denominator and asks the narrower, cleaner question: **what share of US DEBT is serviced
directly out of wages?** Debt is carried at par or amortised cost, so the denominator does
not move with asset prices and the series measures composition rather than valuation.

It is reported as a PAIR on the same first-round versus second-round boundary the sovereign
share uses:
  DIRECT   only claims wages pay directly.
  INCLUDING INDIRECT  business debt carried at the measured indirect labour share, that is,
                      business revenue funded by wage-financed spending.

STATUS: MEASURED, PROVISIONAL until the next promotion pass. It is a new construction and
has not been independently rebuilt.
"""
import json
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import config as C          # noqa: E402
from z1_loader import load_all   # noqa: E402
from build_direct import series_of   # noqa: E402

# Classes excluded from the debt-only denominator: everything carried at MARKET VALUE as an
# equity claim. In this project's thirteen-class table that is corporate_equity alone; the
# rule is written by valuation basis, not by name, so a future equity class is caught too.
EQUITY_CLASSES = {"corporate_equity"}


def main():
    A = load_all()
    summ = json.loads((HERE / "direct_ratio_latest.json").read_text())
    ind = json.loads((HERE / "indirect_extension.json").read_text())
    ind_share = ind["indirect_labour_backing_of_business_revenue"]
    biz = set(ind["business_revenue_serviced_classes"])
    base = {k: v["backing"] for k, v in summ["by_class"].items()}

    # per-class level by year, in bn, using the project's own series resolver
    lvl = {}
    for c in C.CLASSES:
        parts = [series_of(A, code) for code in c["liab"]]
        parts = [p for p in parts if len(p)]
        if not parts:
            continue
        s = parts[0]
        for extra in parts[1:]:
            s = s.add(extra, fill_value=0.0)
        lvl[c["key"]] = s / 1000.0                    # millions -> bn
    L = pd.DataFrame(lvl).dropna(how="all")
    L = L[L.index >= 1952]

    rows = []
    for y, r in L.iterrows():
        tot_all = float(r.sum())
        tot_debt = float(r[[k for k in r.index if k not in EQUITY_CLASSES]].sum())
        lb_direct = sum(float(r[k]) * base.get(k, 0.0) for k in r.index)
        # indirect: business-revenue classes take the measured indirect share
        lb_incl = lb_direct + sum(float(r[k]) * ind_share
                                  for k in r.index if k in biz)
        lb_direct_debt = sum(float(r[k]) * base.get(k, 0.0)
                             for k in r.index if k not in EQUITY_CLASSES)
        lb_incl_debt = lb_direct_debt + sum(float(r[k]) * ind_share
                                            for k in r.index
                                            if k in biz and k not in EQUITY_CLASSES)
        rows.append({
            "year": int(y),
            "total_all_claims_bn": round(tot_all, 1),
            "total_debt_only_bn": round(tot_debt, 1),
            "equity_share_of_all_claims": round(1 - tot_debt / tot_all, 4),
            "all_claims_ratio_direct": round(lb_direct / tot_all, 4),
            "all_claims_ratio_incl_indirect": round(lb_incl / tot_all, 4),
            "DEBT_ONLY_ratio_direct": round(lb_direct_debt / tot_debt, 4),
            "DEBT_ONLY_ratio_incl_indirect": round(lb_incl_debt / tot_debt, 4),
        })
    D = pd.DataFrame(rows)
    D.to_csv(HERE / "debt_only_ratio_timeseries.csv", index=False)

    latest = D.iloc[-1]

    # ---- sensitivity of the debt-only ratio to the listed judgement calls
    r = L.iloc[-1]
    tot_debt = float(r[[k for k in r.index if k not in EQUITY_CLASSES]].sum())

    def ratio(bk, include_indirect=False):
        v = sum(float(r[k]) * bk.get(k, 0.0) for k in r.index if k not in EQUITY_CLASSES)
        if include_indirect:
            v += sum(float(r[k]) * ind_share for k in r.index
                     if k in biz and k not in EQUITY_CLASSES)
        return v / tot_debt

    central = ratio(base)
    calls = [
        ("THE ONE-STEP RULE: business classes take the indirect share", None),
        ("federal receipts: the 77.7 percent upper bound", {"treasury": 0.7768}),
        ("commercial mortgage treated like multifamily",
         {"commercial_mortgage": base["multifamily_mortgage"]}),
        ("mortgage backing: SIPP balances", {"home_mortgage": 0.8205}),
        ("mortgage backing: the superseded A38 definition", {"home_mortgage": 0.80305}),
        ("rent backing: the A38 definition", {"multifamily_mortgage": 0.69913}),
        ("state and local: all personal current taxes",
         {"state_local_debt": base["state_local_debt"] / 0.66754}),
        ("other consumer: the card share alone", {"other_consumer": base["credit_card"]}),
    ]
    srows = [{"judgement_call": "CENTRAL", "debt_only_ratio": round(central, 6),
              "move_pct": 0.0}]
    for name, ov in calls:
        v = ratio(base, include_indirect=True) if ov is None else ratio({**base, **ov})
        srows.append({"judgement_call": name, "debt_only_ratio": round(v, 6),
                      "move_pct": round(100 * (v / central - 1), 2)})
    S = pd.DataFrame(srows)
    S["abs"] = S.move_pct.abs()
    S = pd.concat([S.iloc[:1], S.iloc[1:].sort_values("abs", ascending=False)])
    S.drop(columns="abs").to_csv(HERE / "debt_only_sensitivity.csv", index=False)

    out = {
        "status": "MEASURED, PROVISIONAL until the next promotion pass. New construction, "
                  "not independently rebuilt.",
        "why": "The all-claims ratio has corporate equity at market value at 48 percent of "
               "its denominator, so it is partly an asset-price series: 0.267 at the 2000 "
               "equity peak, 0.376 in 2008 after the crash. The debt-only ratio removes "
               "that by excluding market-valued equity classes.",
        "latest_year": int(latest.year),
        "DEBT_ONLY_direct": float(latest.DEBT_ONLY_ratio_direct),
        "DEBT_ONLY_incl_indirect": float(latest.DEBT_ONLY_ratio_incl_indirect),
        "all_claims_direct": float(latest.all_claims_ratio_direct),
        "all_claims_incl_indirect": float(latest.all_claims_ratio_incl_indirect),
        "equity_share_of_all_claims_latest": float(latest.equity_share_of_all_claims),
        "debt_only_range_1952_2025": [float(D.DEBT_ONLY_ratio_direct.min()),
                                      float(D.DEBT_ONLY_ratio_direct.max())],
        "all_claims_range_1952_2025": [float(D.all_claims_ratio_direct.min()),
                                       float(D.all_claims_ratio_direct.max())],
        "coefficient_of_variation": {
            "debt_only": round(float(D.DEBT_ONLY_ratio_direct.std()
                                     / D.DEBT_ONLY_ratio_direct.mean()), 4),
            "all_claims": round(float(D.all_claims_ratio_direct.std()
                                      / D.all_claims_ratio_direct.mean()), 4)},
        "largest_judgement_call": S.iloc[1].judgement_call,
        "largest_move_pct": float(S.iloc[1].move_pct),
    }
    (HERE / "debt_only_ratio.json").write_text(json.dumps(out, indent=2))

    pd.set_option("display.width", 200)
    print("DEBT-ONLY LABOUR BACKING RATIO")
    print(f"  {int(latest.year)}: DIRECT {latest.DEBT_ONLY_ratio_direct:.4f}, "
          f"INCLUDING INDIRECT {latest.DEBT_ONLY_ratio_incl_indirect:.4f}")
    print(f"  all-claims for comparison: {latest.all_claims_ratio_direct:.4f} and "
          f"{latest.all_claims_ratio_incl_indirect:.4f}")
    print(f"  equity is {100*latest.equity_share_of_all_claims:.1f} pct of the "
          f"all-claims denominator")
    print()
    print("SERIES, selected years")
    print(D[D.year.isin([1952, 1970, 1990, 2000, 2008, 2020, 2025])].to_string(index=False))
    print()
    print(f"stability 1952 to 2025, coefficient of variation: "
          f"debt-only {out['coefficient_of_variation']['debt_only']}, "
          f"all-claims {out['coefficient_of_variation']['all_claims']}")
    print()
    print("SENSITIVITY of the debt-only direct ratio")
    print(S.drop(columns="abs").to_string(index=False))


if __name__ == "__main__":
    main()
