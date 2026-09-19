"""Item 1: hand arithmetic on the high-displacement credit cells, in a fresh script.

Imports nothing from src/. Reads SIPP directly and retyped Federal Reserve figures, and
works the arithmetic through step by step so each number can be checked by eye.

THE SPECIFIC SUSPICION. A75 concluded that no private balance sheet crosses a 25 percent
materiality threshold at any displacement level, including 75 percent of the total wage bill.
That is surprising. Two candidate explanations are tested here:

  (i)  the credit side SATURATES above the old top-quintile grid, the way the fiscal columns
       were shown to;
  (ii) the loss conversion is wrong. A75 multiplied EXPOSURE AT DEFAULT by the Federal
       Reserve's PORTFOLIO loss rate. A portfolio loss rate already contains a probability of
       default. Exposure at default already contains a probability of default. Multiplying
       them applies default twice and divides the loss by roughly the default rate.

If (ii) holds, the correct conversion is exposure at default times LOSS GIVEN DEFAULT, and
the reported losses are too small by a factor of roughly LGD divided by the portfolio loss
rate.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[2]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

# ---- Federal Reserve 2026 DFAST, Table 9, retyped from the document ----
FED_LOSSES_BN = {"first_lien": 22.5, "junior_heloc": 5.5, "credit_card": 203.0,
                 "other_consumer": 54.1}
FED_RATES = {"first_lien": 0.015, "junior_heloc": 0.032, "credit_card": 0.171,
             "other_consumer": 0.073}
# implied portfolio balances across the 32 banks, from losses / rate
FED_BALANCES_BN = {k: FED_LOSSES_BN[k] / FED_RATES[k] for k in FED_LOSSES_BN}

# ---- Loss given default. Sourced range, stated. ----
# Mortgage severity: the Fed's own first-lien loss rate of 1.5 percent over a nine-quarter
# horizon implies, for any assumed cumulative default rate d, an LGD of 0.015/d. At a 4 to 6
# percent cumulative default rate in a severely adverse scenario that is an LGD of 0.25 to
# 0.375, which brackets the conventional 30 to 40 percent severity. The range below is
# carried and every result is reported across it.
LGD = {"first_lien": (0.25, 0.40), "credit_card": (0.80, 1.00),
       "auto": (0.45, 0.65), "student": (0.75, 1.00)}

GHOW_ONE, GHOW_TWO = 0.050, 0.080
PCOLS = ["SSUID", "ERESIDENCEID", "PNUM", "MONTHCODE", "WPFINWGT", "ERELRPE", "TAGE",
         "RMESR", "TJB1_OCC", "THDEBT_HOME", "THDEBT_CC", "THDEBT_VEH", "THDEBT_ED",
         "THVAL_HOME"]


def load_sipp():
    """Stream the SIPP file line by line, filtering to MONTHCODE 12 before parsing.

    pandas.read_csv on this file exhausted memory even at a 50,000 row chunk size, because
    the C parser buffers the whole pipe-delimited row set before applying usecols. Streaming
    by hand keeps the footprint to one line at a time and is the reason this loader looks
    lower level than the rest of the repository.
    """
    z = zipfile.ZipFile(RAW / "sipp" / "pu2025_csv.zip")
    keep = {}
    rows = []
    with z.open("pu2025.csv") as fh:
        txt = io.TextIOWrapper(fh, encoding="utf-8", errors="replace")
        header = txt.readline().rstrip("\n").split("|")
        idx = {c: header.index(c) for c in PCOLS if c in header}
        missing = [c for c in PCOLS if c not in idx]
        if missing:
            raise KeyError(f"columns absent from the SIPP file: {missing}")
        mc = idx["MONTHCODE"]
        for line in txt:
            f = line.rstrip("\n").split("|")
            if len(f) <= mc or f[mc] != "12":
                continue
            rows.append([f[idx[c]] for c in PCOLS])
    D = pd.DataFrame(rows, columns=PCOLS)
    del rows
    for c in PCOLS:
        if c not in ("SSUID", "ERESIDENCEID"):
            D[c] = pd.to_numeric(D[c], errors="coerce")
    D["hh"] = D["SSUID"].astype(str) + "_" + D["ERESIDENCEID"].astype(str)
    D["employed"] = D["RMESR"].isin([1, 2, 3, 4, 5])
    ref = D[D["ERELRPE"].isin([1, 2])]
    ref = ref.sort_values("WPFINWGT").groupby("hh").tail(1).set_index("hh")
    hh = pd.DataFrame(index=ref.index)
    hh["wgt"] = ref["WPFINWGT"]
    hh["ref_age"] = ref["TAGE"]
    for lab, col in [("mortgage", "THDEBT_HOME"), ("card", "THDEBT_CC"),
                     ("auto", "THDEBT_VEH"), ("student", "THDEBT_ED"),
                     ("home_value", "THVAL_HOME")]:
        hh[lab] = D.groupby("hh")[col].max()
    hh["n_earners"] = D.assign(e=D["employed"].astype(int)).groupby("hh")["e"].sum()
    hh["any_emp"] = hh["n_earners"] > 0
    return hh[hh["wgt"] > 0].copy()


def main():
    hh = load_sipp()
    core = hh["any_emp"] & hh["ref_age"].between(25, 64)
    C = hh[core].copy()
    w = C["wgt"].to_numpy(float)
    print("=== SIPP working-core households ===")
    print(f"  {len(C):,} records, {w.sum()/1e6:.2f}m weighted")

    mortgaged = (C["mortgage"].fillna(0) > 0).to_numpy()
    print(f"  with a mortgage: {w[mortgaged].sum()/1e6:.2f}m "
          f"({100*w[mortgaged].sum()/w.sum():.1f}%)")
    print(f"  total mortgage balance: "
          f"{float((C['mortgage'].fillna(0).to_numpy()*w).sum())/1e9:,.0f}bn")

    print("\n=== Federal Reserve implied portfolio balances across the 32 banks ===")
    for k, v in FED_BALANCES_BN.items():
        print(f"  {k:16s} losses {FED_LOSSES_BN[k]:>6.1f}bn at {FED_RATES[k]:.3f} "
              f"-> balance {v:>8,.0f}bn")

    rows = []
    for wb in (0.05, 0.10, 0.25, 0.50, 0.75):
        # share of working-core EARNERS displaced equals the share of the wage bill
        # displaced, to first order
        share = wb
        two = (C["n_earners"].fillna(0) >= 2).to_numpy()
        # probability at least one earner displaced, and probability both
        p_one = np.where(two, 2 * share * (1 - share), share)
        p_two = np.where(two, share ** 2, 0.0)
        dp = p_one * GHOW_ONE + p_two * GHOW_TWO
        for lab, lgd_key in [("mortgage", "first_lien"), ("card", "credit_card"),
                             ("auto", "auto"), ("student", "student")]:
            bal = C[lab].fillna(0).to_numpy()
            ead = float((dp * w * bal).sum()) / 1e9
            lo, hi = LGD[lgd_key]
            fedkey = {"mortgage": "first_lien", "card": "credit_card",
                      "auto": "other_consumer", "student": "other_consumer"}[lab]
            rows.append({
                "share_of_wage_bill": wb, "loan": lab,
                "hh_with_balance_m": float(w[bal > 0].sum()) / 1e6,
                "total_balance_bn": float((bal * w).sum()) / 1e9,
                "mean_default_uplift_pp": 100 * float(np.average(dp, weights=w)),
                "exposure_at_default_bn": ead,
                "loss_lo_bn": ead * lo, "loss_hi_bn": ead * hi,
                "A75_method_loss_bn": ead * FED_RATES[fedkey],
                "fed_loss_bn": FED_LOSSES_BN[fedkey],
                "pct_of_fed_lo": 100 * ead * lo / FED_LOSSES_BN[fedkey],
                "pct_of_fed_hi": 100 * ead * hi / FED_LOSSES_BN[fedkey],
                "A75_pct_of_fed": 100 * ead * FED_RATES[fedkey] / FED_LOSSES_BN[fedkey],
                # THE SECOND SCALING, and it is essential. The SIPP loss is a
                # HOUSEHOLD-UNIVERSE loss. The Fed figure is the loss on the 32 tested
                # banks' own books. Only the share of each loan type those banks hold is
                # comparable. Implied bank share = Fed implied balance / the national
                # household balance for that loan type.
                "bank_share_implied": FED_BALANCES_BN[fedkey] / max(
                    float((bal * w).sum()) / 1e9, 1e-9),
                "bank_held_loss_lo_bn": ead * lo * min(
                    FED_BALANCES_BN[fedkey] / max(float((bal*w).sum())/1e9, 1e-9), 1.0),
                "bank_held_loss_hi_bn": ead * hi * min(
                    FED_BALANCES_BN[fedkey] / max(float((bal*w).sum())/1e9, 1e-9), 1.0)})
    R = pd.DataFrame(rows)
    OUTD = OUT / "verify"; OUTD.mkdir(parents=True, exist_ok=True)
    R.round(4).to_csv(OUTD / "hand_check_credit.csv", index=False)

    pd.set_option("display.width", 250)
    print("\n=== HAND ARITHMETIC: exposure at default and loss, by share of wage bill ===")
    print(R[["share_of_wage_bill", "loan", "mean_default_uplift_pp",
             "exposure_at_default_bn", "loss_lo_bn", "loss_hi_bn",
             "A75_method_loss_bn"]].round(2).to_string(index=False))

    print("\n=== AS A PERCENT OF THE FED SEVERELY ADVERSE LOSS FOR THAT CATEGORY ===")
    print(R[["share_of_wage_bill", "loan", "fed_loss_bn", "pct_of_fed_lo",
             "pct_of_fed_hi", "A75_pct_of_fed"]].round(1).to_string(index=False))

    R["bank_pct_of_fed_lo"] = 100 * R.bank_held_loss_lo_bn / R.fed_loss_bn
    R["bank_pct_of_fed_hi"] = 100 * R.bank_held_loss_hi_bn / R.fed_loss_bn
    R.round(4).to_csv(OUTD / "hand_check_credit.csv", index=False)
    print("\n=== BANK-HELD ONLY: scaled by the tested banks' share of each loan type ===")
    print("    bank share = the Fed implied portfolio balance divided by the national "
          "household balance")
    print(R[["share_of_wage_bill", "loan", "total_balance_bn", "bank_share_implied",
             "bank_held_loss_lo_bn", "bank_held_loss_hi_bn",
             "bank_pct_of_fed_lo", "bank_pct_of_fed_hi"]].round(3).to_string(index=False))

    print("\n=== CROSSING THE 25 PERCENT MATERIALITY THRESHOLD, bank-held basis ===")
    for loan in ["mortgage", "student", "auto", "card"]:
        sub = R[R.loan == loan].sort_values("share_of_wage_bill")
        crossed = sub[sub.bank_pct_of_fed_hi >= 25]
        if len(crossed):
            first = crossed.iloc[0]
            print(f"  {loan:9s} crosses at {first.share_of_wage_bill:.0%} of the wage bill "
                  f"({first.bank_pct_of_fed_lo:.0f} to {first.bank_pct_of_fed_hi:.0f} "
                  f"percent of the Fed loss)")
        else:
            print(f"  {loan:9s} NEVER crosses in the grid "
                  f"(max {sub.bank_pct_of_fed_hi.max():.1f} percent)")

    print("\n=== THE DIAGNOSIS ===")
    m = R[(R.loan == "mortgage") & (R.share_of_wage_bill == 0.75)].iloc[0]
    ratio = (m.loss_lo_bn + m.loss_hi_bn) / 2 / m.A75_method_loss_bn
    print(f"  At 75 percent of the wage bill, mortgages:")
    print(f"    exposure at default        {m.exposure_at_default_bn:,.1f}bn")
    print(f"    loss at LGD 0.25 to 0.40   {m.loss_lo_bn:,.1f} to {m.loss_hi_bn:,.1f}bn")
    print(f"    A75 method (EAD x 1.5 pct) {m.A75_method_loss_bn:,.1f}bn")
    print(f"    ratio                      {ratio:,.1f}x too small in A75")
    print(f"    Fed first-lien loss        {m.fed_loss_bn:,.1f}bn")
    print(f"    so the correct figure is   {m.pct_of_fed_lo:,.0f} to {m.pct_of_fed_hi:,.0f} "
          f"percent of the Fed loss, against A75's {m.A75_pct_of_fed:,.1f} percent")

    (OUTD / "hand_check_credit.json").write_text(json.dumps({
        "fed_implied_balances_bn": FED_BALANCES_BN, "lgd_ranges": LGD,
        "rows": R.round(4).to_dict("records"),
        "diagnosis": "A75 multiplied exposure at default by a PORTFOLIO loss rate, which "
                     "applies the probability of default twice. The correct conversion is "
                     "exposure at default times loss given default.",
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
