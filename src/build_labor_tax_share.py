"""Correct the labor-linked share of US federal receipts using IRS SOI.

Phase 1 reported 77.7 percent by treating ALL federal personal current taxes as
labor-linked. That is an upper bound: individual income tax is levied on wages, but also
on capital gains, dividends, interest, business and retirement income, none of which
Physical AI threatens through the wage channel.

Correction (MASTER_PROMPT_PHASE2.md Step 0): split personal current taxes by the wage and
salary share of adjusted gross income, from IRS Statistics of Income Table 1.4, All
Returns: Sources of Income.

    labor-linked receipts = personal current taxes * (wages / AGI)
                          + federal social insurance contributions

Social insurance contributions are labor-linked by construction (payroll base) and are not
scaled.

Known limitation, stated in the output: the wage share of AGI is not the wage share of TAX.
The individual income tax is progressive and non-wage income concentrates at the top of the
distribution, where marginal rates are highest, so the wage share of tax paid is plausibly
BELOW the wage share of AGI. The corrected figure is therefore itself likely an upper bound
on the true labor-linked share, though a much tighter one than 77.7 percent. Computing the
wage share of tax properly requires bracket-level liability data, which is a later
extension.
"""
import json, pathlib
import pandas as pd
import requests

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw" / "irs", ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}

# IRS SOI Table 1.4 "All Returns: Sources of Income, Adjustments, and Tax Items"
FILES = {2023: "23in14ar.xls", 2022: "22in14ar.xls", 2021: "21in14ar.xls"}
URL = "https://www.irs.gov/pub/irs-soi/{}"

COL_AGI = 2     # adjusted gross income less deficit (thousands of dollars)
COL_TOTINC = 4  # total income
COL_WAGES = 6   # salaries and wages, amount
ROW_ALL = 8     # "All returns, total"


def soi_year(fn):
    p = RAW / fn
    if not p.exists():
        r = requests.get(URL.format(fn), headers=UA, timeout=120)
        r.raise_for_status()
        p.write_bytes(r.content)
    d = pd.read_excel(p, "TBL14", header=None)
    label = str(d.iloc[ROW_ALL, 0]).strip()
    if not label.lower().startswith("all returns"):
        raise ValueError(f"{fn}: row {ROW_ALL} is '{label}', not the all-returns total")
    agi = float(d.iloc[ROW_ALL, COL_AGI]) / 1e6      # thousands -> USD bn
    tot = float(d.iloc[ROW_ALL, COL_TOTINC]) / 1e6
    wag = float(d.iloc[ROW_ALL, COL_WAGES]) / 1e6
    return {"agi_usd_bn": agi, "total_income_usd_bn": tot, "wages_usd_bn": wag,
            "wage_share_of_agi": wag / agi, "wage_share_of_total_income": wag / tot,
            "file": fn}


def main():
    soi = {}
    for yr, fn in FILES.items():
        try:
            soi[yr] = soi_year(fn)
            s = soi[yr]
            print(f"  SOI {yr} ({fn}): AGI {s['agi_usd_bn']:,.1f} bn, "
                  f"wages {s['wages_usd_bn']:,.1f} bn, "
                  f"wage share of AGI {100*s['wage_share_of_agi']:.1f}%")
        except Exception as ex:
            print(f"  SOI {yr} ({fn}): FAILED, {ex}")

    if not soi:
        raise SystemExit("no SOI year could be read")

    # guard against IRS serving the same file under different names
    shares = {y: round(s["wage_share_of_agi"], 6) for y, s in soi.items()}
    if len(set(shares.values())) == 1 and len(shares) > 1:
        print("  WARNING: identical wage shares across years. IRS may be serving the same "
              "file under different names. Using the latest year only and flagging it.")

    latest = max(soi)
    share = soi[latest]["wage_share_of_agi"]

    w = json.loads((OUT / "legW_us_derived.json").read_text())
    pct = w["fed_personal_current_taxes_usd_bn"]
    sic = w["fed_social_insurance_contrib_usd_bn"]
    rec = w["fed_current_receipts_usd_bn"]

    upper = pct + sic
    central = pct * share + sic

    res = {
        "soi_years_read": sorted(soi),
        "soi_year_used": latest,
        "wage_share_of_agi": share,
        "wage_share_of_total_income": soi[latest]["wage_share_of_total_income"],
        "fed_personal_current_taxes_usd_bn": pct,
        "fed_social_insurance_contrib_usd_bn": sic,
        "fed_current_receipts_usd_bn": rec,
        "labor_linked_upper_bound_usd_bn": upper,
        "labor_linked_upper_bound_pct": 100 * upper / rec,
        "labor_linked_central_usd_bn": central,
        "labor_linked_central_pct": 100 * central / rec,
        "soi_detail": soi,
        "caveat": ("The wage share of AGI is not the wage share of tax. The individual "
                   "income tax is progressive and non-wage income concentrates in the top "
                   "brackets, so the wage share of tax paid is plausibly below the wage "
                   "share of AGI. The central figure is therefore still an upper bound, "
                   "though a much tighter one. A bracket-level calculation is a later "
                   "extension."),
    }
    (OUT / "labor_tax_share.json").write_text(json.dumps(res, indent=2))

    print(f"\n  wage share of AGI (SOI {latest}):        {100*share:.1f}%")
    print(f"  federal personal current taxes:          {pct:,.1f} bn")
    print(f"  of which labor-linked:                   {pct*share:,.1f} bn")
    print(f"  federal social insurance contributions:  {sic:,.1f} bn")
    print(f"  federal current receipts:                {rec:,.1f} bn")
    print(f"\n  UPPER BOUND  (Phase 1 figure):           {100*upper/rec:.1f}%")
    print(f"  CENTRAL      (SOI-corrected):            {100*central/rec:.1f}%")


if __name__ == "__main__":
    main()
