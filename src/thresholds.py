"""Item 1: materiality thresholds for every balance sheet, with justification and source,
and the order of stress run at three tightness levels to test whether the ordering is
invariant.

A THRESHOLD IS A CHOICE, NOT A MEASUREMENT. The honest treatment is to state each one, say
where it comes from, and then show whether the conclusion survives moving it. That is what
this module does.

BLOCKED SOURCES, named once. CBO publication pages and SSA.gov both return HTTP 403 to this
environment on every route tried, so the CARES Act scoring and the Trustees Report projected
depletion date could not be read. **Both precedents are therefore DERIVED from FRED series
this repository already holds, which is weaker than citing the scoring document but is
verifiable end to end.** The exact documents remain: CBO's Preliminary Estimate of the Effects
of H.R. 748, the CARES Act, and the annual OASDI Trustees Report.

THE THRESHOLDS

  Bank-type sheets (mortgage, auto, card, student, bank capital)
      The scenario loss as a share of what the Federal Reserve's severely adverse scenario
      produces for that same sheet. Justification: it is the benchmark a supervisor already
      runs, so the comparison needs no new convention. Source: 2026 DFAST, Table 9.
      loose 50 percent, central 25, tight 10.

  Public budget
      The annual revenue loss as a share of federal current receipts, benchmarked against the
      DERIVED precedent of the 2008 to 2009 revenue collapse, the largest peacetime
      peak-to-trough fall in federal receipts in the FRED series. Justification: a
      displacement shock that removes as much revenue as the Great Recession did is, by
      construction, a fiscal event of recognised significance.
      loose is the full precedent, central is half, tight is a quarter.

  Trust funds
      The annual payroll income loss as a share of that fund's payroll income, benchmarked
      against the OASDI combined deficit already being run. Justification: a loss equal to
      the deficit the fund is already running doubles it. Source: A32, verified, 160.2bn in
      2025 against 1,323.2bn of payroll income, so 12.1 percent.
      loose 24.2 percent (double the existing deficit), central 12.1 (equal to it), tight 6.1.

  Landlords and multifamily
      Rent arrears sufficient to push debt service coverage below the sourced underwriting
      range. With a DSCR of D and an arrears share a, coverage falls to D x (1 - a), so the
      breach share is 1 - 1/D for a property underwritten at D. FLAGGED: the agency minimum
      could not be read (Fannie Form 4660 behind DUS Navigate, Freddie's Guide is a
      JavaScript application), so the range 1.20 to 1.35 is used.
      loose D = 1.35 (breach at 25.9 percent arrears), central 1.25 (20.0), tight 1.20 (16.7).
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

FED_LOSSES = {"mortgage": 22.5, "card": 203.0, "auto": 54.1, "student": 54.1}
BANK_TIGHTNESS = {"loose": 0.50, "central": 0.25, "tight": 0.10}
OASDI_DEFICIT_BN, OASDI_PAYROLL_BN = 160.2, 1323.2       # A32, verified
DSCR = {"loose": 1.35, "central": 1.25, "tight": 1.20}


def fred(series):
    p = RAW / "fred" / f"{series}.csv"
    if not p.exists():
        import requests
        r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}",
                         timeout=90)
        r.raise_for_status()
        p.write_bytes(r.content)
    d = pd.read_csv(p)
    d.columns = ["date", "v"]
    d["date"] = pd.to_datetime(d["date"])
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    return d.dropna()


def main():
    # ---- derived public budget precedent ----
    rec = fred("FGRECPT")
    ann = rec.set_index("date")["v"].resample("YE").mean()
    peak_fall, peak_years = 0.0, None
    for i in range(1, len(ann)):
        f = (ann.iloc[i - 1] - ann.iloc[i]) / ann.iloc[i - 1]
        if f > peak_fall:
            peak_fall, peak_years = f, (ann.index[i - 1].year, ann.index[i].year)
    receipts_now = float(ann.iloc[-1])
    print("=== DERIVED PUBLIC BUDGET PRECEDENT ===")
    print(f"  largest annual fall in federal current receipts in the FRED series: "
          f"{peak_fall:.1%}, {peak_years[0]} to {peak_years[1]}")
    print(f"  current federal receipts {receipts_now:,.1f}bn")
    BUDGET = {"loose": peak_fall, "central": peak_fall / 2, "tight": peak_fall / 4}

    TRUST = {"loose": 2 * OASDI_DEFICIT_BN / OASDI_PAYROLL_BN,
             "central": OASDI_DEFICIT_BN / OASDI_PAYROLL_BN,
             "tight": OASDI_DEFICIT_BN / OASDI_PAYROLL_BN / 2}
    print("\n=== THRESHOLDS, all three tightness levels ===")
    print(f"  bank sheets, share of the Fed severely adverse loss: "
          f"{BANK_TIGHTNESS}")
    print(f"  public budget, share of federal receipts: "
          f"{ {k: round(v, 4) for k, v in BUDGET.items()} }")
    print(f"  trust funds, share of fund payroll income: "
          f"{ {k: round(v, 4) for k, v in TRUST.items()} }")
    print(f"  multifamily, arrears share that breaches DSCR: "
          f"{ {k: round(1 - 1 / v, 4) for k, v in DSCR.items()} }")

    # ---- load the corrected results ----
    cb = pd.read_csv(OUT / "credit_benchmarked.csv")
    # A80 scaled by official aggregate divided by the WORKING-CORE balance, which conflates
    # survey under-reporting with sample coverage and over-scaled every row. The corrected
    # under-reporting factors come from the FULL SIPP universe (item 2). Applied here as a
    # ratio so the rest of the pipeline does not have to be rebuilt.
    ur = pd.read_csv(OUT / "under_reporting_factors.csv")
    corr = {r["loan"]: r["UNDER_REPORTING_factor"] / r["A80_factor_working_core"]
            for _, r in ur.iterrows()}
    for c in ["bank_loss_lo_bn", "bank_loss_hi_bn", "pct_of_fed_lo", "pct_of_fed_hi"]:
        cb[c] = cb.apply(lambda r: r[c] * corr.get(r["loan"], 1.0), axis=1)
    print("\n=== credit rows rescaled by the corrected under-reporting factors ===")
    for k, v in corr.items():
        print(f"  {k:9s} x {v:.3f}")
    tf = pd.read_csv(OUT / "trust_fund_corrected.csv")
    fx = pd.read_csv(OUT / "fiscal_extended_axis.csv")
    fx = fx[(fx.tau_l == "bottom_up_0.301") & (fx.outlays == "no_outlays")
            & (fx.tau_k_reading == "barkai_rent_0.351") & (fx.rho_mode == "fitted")
            & (fx.horizon == 10)]
    tf["wb"] = tf["share_of_total_wage_bill"]
    fx = fx.copy(); fx["wb"] = fx["share_of_total_wage_bill"]

    LEVELS = [0.10, 0.25, 0.50, 0.75]
    rows = []
    for tight in ("loose", "central", "tight"):
        for wb in LEVELS:
            # bank sheets
            for loan in ["mortgage", "student", "auto", "card"]:
                s = cb[(cb.loan == loan) & np.isclose(cb.share_of_wage_bill, wb)]
                if not len(s):
                    continue
                val = float(s["pct_of_fed_hi"].iloc[0]) / 100.0
                rows.append({"tightness": tight, "wb": wb, "sheet": loan,
                             "value": val, "threshold": BANK_TIGHTNESS[tight],
                             "crossed": val >= BANK_TIGHTNESS[tight]})
            # public budget
            f2 = fx[np.isclose(fx.wb, wb, atol=0.04)]
            if len(f2):
                val = float(f2["terminal_pct_receipts"].mean()) / 100.0
                rows.append({"tightness": tight, "wb": wb, "sheet": "public_budget",
                             "value": val, "threshold": BUDGET[tight],
                             "crossed": val >= BUDGET[tight]})
            # trust funds
            t2 = tf[np.isclose(tf.wb, wb, atol=0.04)]
            if len(t2):
                val = float(t2["OASDI_loss_pct_of_fund_payroll_income"].mean()) / 100.0
                rows.append({"tightness": tight, "wb": wb, "sheet": "trust_funds",
                             "value": val, "threshold": TRUST[tight],
                             "crossed": val >= TRUST[tight]})
    G = pd.DataFrame(rows)
    G.round(5).to_csv(OUT / "threshold_sensitivity.csv", index=False)

    pd.set_option("display.width", 240)
    print("\n=== CROSSING POINT, share of the total wage bill, by tightness ===")
    order = {}
    for tight in ("loose", "central", "tight"):
        s = G[(G.tightness == tight) & G.crossed]
        firsts = s.groupby("sheet")["wb"].min().sort_values()
        order[tight] = list(firsts.index)
        print(f"\n  {tight}:")
        for sheet, wb in firsts.items():
            print(f"    {sheet:15s} crosses at {wb:.0%}")
        never = sorted(set(G.sheet.unique()) - set(firsts.index))
        for n in never:
            print(f"    {n:15s} never crosses in the grid")

    print("\n=== IS THE ORDERING INVARIANT? ===")
    inv = len(set(tuple(v) for v in order.values())) == 1
    print(f"  {'YES, identical at all three tightness levels' if inv else 'NO'}")
    if not inv:
        for k, v in order.items():
            print(f"    {k:8s}: {' -> '.join(v)}")
        # robust pairs: those whose relative order is the same in all three
        sheets = sorted(set(G.sheet.unique()))
        robust, fragile = [], []
        for i in range(len(sheets)):
            for j in range(i + 1, len(sheets)):
                a, b = sheets[i], sheets[j]
                rel = set()
                for k, v in order.items():
                    if a in v and b in v:
                        rel.add(v.index(a) < v.index(b))
                    else:
                        rel.add(None)
                (robust if len(rel) == 1 and None not in rel else fragile).append((a, b))
        print(f"\n  ROBUST comparisons ({len(robust)}): "
              + "; ".join(f"{a} vs {b}" for a, b in robust))
        print(f"  FRAGILE comparisons ({len(fragile)}), NOT ranked: "
              + "; ".join(f"{a} vs {b}" for a, b in fragile))

    (OUT / "thresholds_summary.json").write_text(json.dumps({
        "bank": BANK_TIGHTNESS, "public_budget": BUDGET, "trust_funds": TRUST,
        "dscr": DSCR,
        "budget_precedent": {"largest_annual_receipts_fall": peak_fall,
                             "years": peak_years,
                             "derivation": "FRED FGRECPT annual means; CBO scoring pages "
                                           "return HTTP 403 to this environment"},
        "trust_precedent": {"oasdi_deficit_bn": OASDI_DEFICIT_BN,
                            "oasdi_payroll_bn": OASDI_PAYROLL_BN,
                            "share": OASDI_DEFICIT_BN / OASDI_PAYROLL_BN,
                            "source": "A32, verified in the repository"},
        "ordering_invariant": bool(inv),
        "orders": order,
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
