"""Absorbing capacity for every balance sheet in the dose-response table.

WHY THIS MODULE EXISTS. Item 1 of the final session retires the ranking. Ranking balance
sheets by threshold crossing is not meaningful because each sheet is measured against a
different yardstick, so the order is an artifact of the yardsticks rather than a fact about
the shock. A82 already showed this: only 4 of 15 pairwise comparisons survived moving the
thresholds. What replaces it is a dose-response table in which every cell is reported three
ways: in dollars, as a share of GDP, and as a share of that sheet's own absorbing capacity.

The third of those is the one a supervisor can act on, and it only means anything if the
capacity measure is stated and sourced. That is what this module does. Every number below is
either read from a document in data/raw/ or fetched from a provider, and each carries its
source string into capacities.json.

CAPACITY MEASURES, by sheet.

  Bank capital
      Two measures, both reported, because they answer different questions.
      (a) CET1 above the regulatory minimum. Aggregate CET1 was 12.8 percent of
          12,583.7bn of risk-weighted assets at 2025:Q4 (2026 DFAST, Table 4). The
          statutory CET1 minimum is 4.5 percent (12 CFR 217.10). The surplus is the capital
          that can be lost before the minimum binds.
      (b) The 708bn of losses the Federal Reserve found the 32 banks could absorb in the
          2026 severely adverse scenario while continuing to lend. This is the supervisor's
          own revealed capacity statement and is the owner's named benchmark.
      A third, stricter reading is stated but not used as the denominator: the test's
      PROJECTED MINIMUM CET1 of 11.2 percent leaves only 1.6 percentage points of headroom
      from the 12.8 starting point, which is what the 708bn of losses actually consumed.

  Bank-held loan books (mortgage, auto, card, student, business credit, CRE)
      The same aggregate CET1 surplus, because losses on any book are absorbed by the same
      capital. The Fed's severely adverse loss for that specific book is reported alongside
      as a second, book-specific yardstick.

  Agency mortgage (the GSEs)
      Combined net worth of Fannie Mae and Freddie Mac, read from their own 10-Q filings
      through the SEC XBRL API. FLAGGED: the GSEs remain in conservatorship, so net worth
      is not the same kind of loss-absorbing capital as bank CET1, and the Treasury senior
      preferred purchase agreements sit behind it. The comparison is a scale comparison,
      not a solvency test.

  Public budget
      Annual federal current receipts (FRED FGRECPT). TWO reference points are carried.
      CITED: CBO's Preliminary Estimate of the Effects of H.R. 748 (the CARES Act), revised
      April 27 2020, scores a 408bn decrease in revenues inside a 1.7tn increase in
      deficits over 2020-2030. The owner has placed that document and its original PDF in
      data/raw/owner/ and src/owner_files.py verifies the extraction against it, so this
      figure is now cited rather than derived. DERIVED, retained because it measures a
      different thing: the 13.2 percent fall in receipts from 2008 to 2009, the largest
      annual fall in the FRED series, which is what actually happened rather than what one
      act was scored as costing.

  OASDI and HI trust funds
      Annual payroll income, now read from the 2026 Trustees summary tables the owner
      placed in data/raw/owner/ (Table 5), not derived. OASDI 1,322.6bn (OASI 1,130.7 plus
      DI 191.9); HI 403.2bn. The HI figure REPLACES a derived 286.2bn, which applied the
      statutory 2.9 percent rate to this project's occupational wage bill: that grid is a
      subset of covered earnings, so the derived figure was 71.0 percent of the published
      one. The RESERVE column, blocked in A85 and A100, is now filled from Table 4: OASI
      2,338.3bn, DI 223.0bn, HI 255.7bn at the end of 2025. DEPLETION TIMING is added as a
      second capacity measure, because for a fund running down "how long" is the more
      useful supervisory number than "how much": OASI 2032 Q4, combined OASDI 2034 Q3, HI
      2033 Q2, DI not within the 75-year window.

  Landlords and multifamily lenders
      Not a dollar capacity. The binding constraint is debt service coverage: a property
      underwritten at a coverage ratio D breaches at an arrears share of 1 - 1/D. FLAGGED:
      the agency minimum could not be read (Fannie Form 4660 sits behind DUS Navigate and
      the Freddie Guide is a JavaScript application), so the sourced range 1.20 to 1.35 is
      carried and the breach share is reported as a range.
"""
import json, pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

# ---- 2026 DFAST, Table 4 and the results summary. data/raw/manual/FRB_2026_DFAST_results.pdf
RWA_BN = 12_583.7
CET1_ACTUAL_PCT = 12.8
CET1_STRESSED_MIN_PCT = 11.2
CET1_REGULATORY_MIN_PCT = 4.5          # 12 CFR 217.10, standardised approach
LOSSES_ABSORBED_BN = 708.0
FED_LOSSES_BN = {"mortgage": 22.5, "card": 203.0, "auto": 54.1, "student": 54.1,
                 "business_credit": 158.2, "cre": 76.5, "total": 624.9}

# ---- GSE loss-absorbing layers, amendment (b) of the final session.
# READ FROM THE GSEs' OWN 2025 FORM 10-K FILINGS through the SEC XBRL API and the filing
# text. Pre-provision pre-tax earnings are net income plus income tax expense plus the
# provision for credit losses, which is the standard first-loss earnings layer.
GSE_PPE = {                       # FY2025, USD billions, from us-gaap facts
    "Fannie Mae": {"net_income": 14.36, "tax": 3.62, "provision": 1.61},
    "Freddie Mac": {"net_income": 10.73, "tax": 2.63, "provision": 1.29},
}
# Credit risk transferred to private investors. FHFA Credit Risk Transfer Progress Report,
# Fourth Quarter 2023, the latest edition FHFA has published: from 2013 through 2023 the
# Enterprises transferred a portion of credit risk on about 6.7tn of UPB with a combined
# Risk in Force of 210bn, or 3.2 percent of UPB. FLAGGED AS STALE: 4Q2023 against a 2026
# balance sheet.
CRT_RIF_BN = 210.0
CRT_UPB_TN = 6.7
CRT_RIF_PCT_OF_UPB = 3.2
# Private mortgage insurance, from the 2025 Form 10-Ks.
#   Fannie Mae: total mortgage insurance risk in force 201,355m, 6 percent of the
#   single-family conventional guaranty book; loans with credit enhancement 1,663bn UPB,
#   47 percent of that book; credit enhancement generally required above 80 percent LTV.
#   Freddie Mac: primary mortgage insurance covers 22 percent of the single-family
#   portfolio by UPB and CRT and other 52 percent, with 39 percent not credit enhanced;
#   mortgage insurers' maximum loss limits 181.5bn.
PMI_RIF_BN = {"Fannie Mae": 201.355, "Freddie Mac": 181.5}
CREDIT_ENHANCED_SHARE = {"Fannie Mae": 0.47, "Freddie Mac": 0.61}
# FHA. FLAGGED PROXY, recorded in lit/unverified.md: hud.gov returns HTTP 403 on every
# route, so the FY2025 MMI Fund figures come from secondary reporting and are not cited.
FHA_CAPITAL_RATIO = 0.1147
FHA_INSURANCE_IN_FORCE_BN = 1_647.0
FHA_ECONOMIC_NET_WORTH_BN = FHA_CAPITAL_RATIO * FHA_INSURANCE_IN_FORCE_BN
FHA_STATUTORY_MINIMUM = 0.02

# ---- trust funds. Every figure below is READ from data/processed/owner_sources.json,
#      which src/owner_files.py builds from the owner's 2026 Trustees summary tables and
#      verifies by arithmetic reconciliation. Nothing here is derived any more.
#      The statutory combined HI rate is retained only to document the superseded
#      derivation, never to produce a capacity.
HI_COMBINED_RATE = 0.029               # 26 USC 3101(b) and 3111(b), employee plus employer

# ---- multifamily underwriting, FLAGGED range
DSCR_RANGE = (1.20, 1.35)


def fred_last_annual(series):
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
    d = d.dropna().set_index("date")["v"]
    ann = d.resample("YE").mean()
    return ann, float(ann.iloc[-1]), str(ann.index[-1].date())


def gse_net_worth():
    """Fannie Mae and Freddie Mac net worth from their own filings, through the SEC XBRL
    API. The User-Agent identifies the project and a contact address, per the SEC fair
    access policy; it is never a browser string (decision D8)."""
    import requests
    UA = {"User-Agent": "physical-ai research team@oviguide.in"}
    out = {}
    for name, cik in [("Fannie Mae", "0000310522"), ("Freddie Mac", "0001026214")]:
        val, end, form = None, None, None
        r = requests.get(
            f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=UA,
            timeout=120)
        r.raise_for_status()
        facts = r.json()["facts"]["us-gaap"]
        for tag in ("StockholdersEquity",
                    "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"):
            us = sorted(facts.get(tag, {}).get("units", {}).get("USD", []),
                        key=lambda x: x["end"])
            us = [x for x in us if x.get("form") in ("10-Q", "10-K")]
            if us:
                val, end, form = us[-1]["val"] / 1e9, us[-1]["end"], us[-1]["form"]
                break
        out[name] = {"net_worth_bn": val, "as_of": end, "form": form, "cik": cik,
                     "tag": tag}
    return out


def total_wage_bill_bn():
    """Total US wage bill on the project's own occupational grid, the denominator every
    scenario share is expressed against."""
    grid = pd.read_csv(OUT / "paei_c.csv")
    wb = grid[grid["c"] == 0.0][["occp", "wage_bill"]].drop_duplicates("occp")
    return float(wb["wage_bill"].sum()) / 1e9


def build():
    receipts_ann, receipts_bn, receipts_date = fred_last_annual("FGRECPT")
    gdp_ann, gdp_bn, gdp_date = fred_last_annual("GDP")

    peak_fall, peak_years = 0.0, None
    for i in range(1, len(receipts_ann)):
        f = (receipts_ann.iloc[i - 1] - receipts_ann.iloc[i]) / receipts_ann.iloc[i - 1]
        if f > peak_fall:
            peak_fall, peak_years = f, (receipts_ann.index[i - 1].year,
                                        receipts_ann.index[i].year)

    cet1_bn = RWA_BN * CET1_ACTUAL_PCT / 100.0
    cet1_surplus_bn = RWA_BN * (CET1_ACTUAL_PCT - CET1_REGULATORY_MIN_PCT) / 100.0
    cet1_test_headroom_bn = RWA_BN * (CET1_ACTUAL_PCT - CET1_STRESSED_MIN_PCT) / 100.0

    gse = gse_net_worth()
    gse_total = sum(v["net_worth_bn"] for v in gse.values())
    gse_ppe = sum(v["net_income"] + v["tax"] + v["provision"] for v in GSE_PPE.values())

    wage_bill_bn = total_wage_bill_bn()
    national_wage_bill_bn = json.loads(
        (OUT / "legW_us_derived.json").read_text())["wage_bill_usd_bn"]
    own = json.loads((OUT / "owner_sources.json").read_text())
    tr, cbo = own["trustees_2026"], own["cbo_hr748"]
    oasdi_payroll_income_bn = tr["oasdi_payroll_income_bn"]
    hi_payroll_income_bn = tr["hi_payroll_income_bn"]
    hi_derived_superseded_bn = HI_COMBINED_RATE * wage_bill_bn

    cap = {
        "gdp_bn": gdp_bn,
        "gdp_as_of": gdp_date,
        "gdp_source": "FRED GDP, annual mean of quarterly nominal GDP",
        "total_wage_bill_bn": wage_bill_bn,
        "total_wage_bill_source": "this project's occupational grid, data/processed/paei_c.csv",
        "national_wage_bill_bn": national_wage_bill_bn,
        "national_wage_bill_source":
            "FRED WASCUR, NIPA wages and salaries. THE BASE every dose is converted to "
            "dollars on. The occupational grid above is a SUBSET of national wages "
            f"({100 * wage_bill_bn / national_wage_bill_bn:.1f} percent of it, and "
            "src/coverage_reconciliation.py reconciles the two), so a dose expressed as a "
            "share of the grid is scaled to dollars on the national total under an explicit "
            "proportionality assumption. WASCUR and not FRED COE: tau_l is built as federal "
            "taxes over WASCUR, and compensation of employees additionally includes employer "
            "pension and health contributions, which bear neither the income tax nor the "
            "payroll tax.",
        "grid_share_of_national_wage_bill": wage_bill_bn / national_wage_bill_bn,
        "sheets": {
            "bank_capital": {
                "capacity_bn": cet1_surplus_bn,
                "measure": "aggregate CET1 above the 4.5 percent regulatory minimum",
                "source": "2026 DFAST Table 4: CET1 12.8 percent of 12,583.7bn RWA at "
                          "2025:Q4; minimum 4.5 percent per 12 CFR 217.10",
                "alt_capacity_bn": LOSSES_ABSORBED_BN,
                "alt_measure": "losses the Federal Reserve found the 32 banks could absorb "
                               "in the 2026 severely adverse scenario",
                "strict_capacity_bn": cet1_test_headroom_bn,
                "strict_measure": "headroom to the test's PROJECTED MINIMUM CET1 of 11.2 "
                                  "percent, which is what the 708bn actually consumed",
                "cet1_bn": cet1_bn,
            },
            "mortgage_bank_held": {
                "capacity_bn": cet1_surplus_bn,
                "measure": "aggregate bank CET1 above the regulatory minimum",
                "source": "2026 DFAST Table 4",
                "alt_capacity_bn": FED_LOSSES_BN["mortgage"],
                "alt_measure": "Fed severely adverse first-lien domestic mortgage loss, "
                               "2026 DFAST Table 9",
            },
            "mortgage_agency": {
                "capacity_bn": gse_total,
                "measure": "combined net worth of Fannie Mae and Freddie Mac",
                "source": "SEC XBRL company facts from the GSEs' own 10-Q filings: "
                          + "; ".join(f"{k} {v['net_worth_bn']:.1f}bn at {v['as_of']} "
                                      f"({v['form']})" for k, v in gse.items()),
                "flag": "The GSEs are in conservatorship. Net worth is not loss-absorbing "
                        "capital of the same kind as bank CET1 and the Treasury senior "
                        "preferred agreements sit behind it. This is a scale comparison, "
                        "not a solvency test.",
                "detail": gse,
                "layers": {
                    "annual_pre_provision_pre_tax_earnings_bn": gse_ppe,
                    "earnings_source": "FY2025 Forms 10-K through the SEC XBRL API: net "
                                       "income plus income tax expense plus the provision "
                                       "for credit losses",
                    "capital_plus_1y_earnings_bn": gse_total + gse_ppe,
                    "capital_plus_3y_earnings_bn": gse_total + 3 * gse_ppe,
                    "crt_risk_in_force_bn": CRT_RIF_BN,
                    "crt_share_of_upb_pct": CRT_RIF_PCT_OF_UPB,
                    "crt_source": "FHFA Credit Risk Transfer Progress Report, Fourth "
                                  "Quarter 2023: risk transferred on about 6.7tn of UPB "
                                  "with a combined Risk in Force of 210bn, 3.2 percent of "
                                  "UPB. FLAGGED AS STALE, 4Q2023 against a 2026 book.",
                    "pmi_risk_in_force_bn": PMI_RIF_BN,
                    "pmi_total_bn": sum(PMI_RIF_BN.values()),
                    "credit_enhanced_share_of_book": CREDIT_ENHANCED_SHARE,
                    "pmi_source": "2025 Forms 10-K. Fannie Mae: total mortgage insurance "
                                  "risk in force 201,355m, 6 percent of the single-family "
                                  "conventional guaranty book; loans with credit "
                                  "enhancement 1,663bn UPB, 47 percent of the book; credit "
                                  "enhancement generally required above 80 percent LTV. "
                                  "Freddie Mac: primary mortgage insurance on 22 percent "
                                  "of the portfolio, CRT and other on 52 percent, 39 "
                                  "percent not credit enhanced; insurers' maximum loss "
                                  "limits 181.5bn.",
                    "note": "CRT and PMI are LOSS TRANSFERS, not capital. They reduce the "
                            "loss reaching the Enterprises rather than increasing what the "
                            "Enterprises can absorb, and they are applied on the loss side "
                            "of the dose-response table, not added to capacity here.",
                },
            },
            "mortgage_agency_FHA": {
                "capacity_bn": FHA_ECONOMIC_NET_WORTH_BN,
                "measure": "FHA Mutual Mortgage Insurance Fund economic net worth",
                "source": "FLAGGED PROXY, see lit/unverified.md. hud.gov returns HTTP 403 "
                          f"to this environment. Capital ratio {FHA_CAPITAL_RATIO:.2%} on "
                          f"{FHA_INSURANCE_IN_FORCE_BN:,.0f}bn of insurance in force, "
                          f"FY2025, statutory minimum {FHA_STATUTORY_MINIMUM:.0%}",
                "insurance_in_force_bn": FHA_INSURANCE_IN_FORCE_BN,
                "flag": "The MMI Fund is a federal fund. A loss here lands on the federal "
                        "government, not on a private balance sheet, and it is consolidated "
                        "as such in the sovereign block.",
            },
            "mortgage_agency_VA": {
                "capacity_bn": None,
                "measure": "NOT a capacity. The VA home loan guaranty is backed by the full "
                           "faith and credit of the United States and has no separate "
                           "loss-absorbing fund to exhaust",
                "source": "38 USC chapter 37",
                "flag": "Every dollar of VA guaranty loss is a federal loss on the first "
                        "dollar. It is carried in the sovereign block and nowhere else.",
            },
            "auto_lenders": {
                "capacity_bn": cet1_surplus_bn,
                "measure": "aggregate bank CET1 above the regulatory minimum",
                "source": "2026 DFAST Table 4",
                "alt_capacity_bn": FED_LOSSES_BN["auto"],
                "alt_measure": "Fed severely adverse Other consumer loss, which FOLDS auto "
                               "and student together, 2026 DFAST Table 9",
                "flag": "Auto is not broken out from student loans by the Fed. The "
                        "book-specific yardstick is therefore shared between the two rows.",
            },
            "card_consumer_lenders": {
                "capacity_bn": cet1_surplus_bn,
                "measure": "aggregate bank CET1 above the regulatory minimum",
                "source": "2026 DFAST Table 4",
                "alt_capacity_bn": FED_LOSSES_BN["card"],
                "alt_measure": "Fed severely adverse credit card loss, 2026 DFAST Table 9",
            },
            "student_loan_holders": {
                "capacity_bn": cet1_surplus_bn,
                "measure": "aggregate bank CET1 above the regulatory minimum",
                "source": "2026 DFAST Table 4",
                "alt_capacity_bn": FED_LOSSES_BN["student"],
                "alt_measure": "Fed severely adverse Other consumer loss, shared with auto",
                "flag": "Most outstanding student debt is federally held, not bank held, so "
                        "the bank capacity denominator understates who actually bears it. "
                        "The federal holder's capacity is the public budget row.",
            },
            "business_credit": {
                "capacity_bn": cet1_surplus_bn,
                "measure": "aggregate bank CET1 above the regulatory minimum",
                "source": "2026 DFAST Table 4",
                "alt_capacity_bn": FED_LOSSES_BN["business_credit"],
                "alt_measure": "Fed severely adverse commercial and industrial loss",
            },
            "commercial_real_estate": {
                "capacity_bn": cet1_surplus_bn,
                "measure": "aggregate bank CET1 above the regulatory minimum",
                "source": "2026 DFAST Table 4",
                "alt_capacity_bn": FED_LOSSES_BN["cre"],
                "alt_measure": "Fed severely adverse domestic CRE loss",
            },
            "public_budget": {
                "capacity_bn": receipts_bn,
                "measure": "annual federal current receipts",
                "source": f"FRED FGRECPT, annual mean, {receipts_date}",
                "reference_point": {
                    "cited_revenue_decrease_bn": cbo["revenue_decrease_bn"],
                    "cited_revenue_decrease_pct_of_receipts":
                        cbo["revenue_decrease_bn"] / receipts_bn,
                    "cited_deficit_increase_tn": cbo["deficit_increase_2020_2030_tn"],
                    "cited_source": cbo["document"],
                    "cited_local_original": cbo["local_original"],
                    "note": "CITED, replacing the derived threshold. The owner placed the "
                            "CBO document and its original PDF; src/owner_files.py checks "
                            "the extraction against the PDF text layer.",
                    "largest_annual_fall": peak_fall,
                    "years": list(peak_years),
                    "derived_note": "RETAINED alongside because it measures a different "
                                    "thing: the largest annual fall in receipts actually "
                                    "observed in FRED, against what one act was scored as "
                                    "costing.",
                },
            },
            "oasdi": {
                "capacity_bn": oasdi_payroll_income_bn,
                "measure": "annual OASDI payroll income",
                "source": "2026 Trustees summary Table 5: OASI payroll taxes 1,130.7bn "
                          "plus DI 191.9bn. SUPERSEDES the 1,323.2bn derived in A32 as "
                          "91.3 percent of total income; the published payroll share is "
                          f"{100 * tr['payroll_share_of_oasdi_income']:.2f} percent and "
                          "the two figures differ by 0.05 percent.",
                "reserves_bn": tr["oasdi_reserves_end_2025_bn"],
                "reserves_detail_bn": {"OASI": tr["funds"]["OASI"]["reserves_end_2025_bn"],
                                       "DI": tr["funds"]["DI"]["reserves_end_2025_bn"]},
                "reserves_status": "FILLED from 2026 Trustees summary Table 4, end of 2025. "
                                   "The A85 and A100 BLOCKED record is superseded.",
                "depletion": {"OASI": tr["depletion"]["OASI"],
                              "DI": tr["depletion"]["DI"],
                              "combined": tr["depletion"]["OASDI_combined"]},
                "depletion_note": "A SECOND capacity measure. A reserve stock says how "
                                  "much; a depletion date says how long, and for a fund "
                                  "running down that is the number a supervisor uses. The "
                                  "share of scheduled benefits payable at depletion is the "
                                  "size of the cliff.",
                "reference_point": {
                    "net_change_in_reserves_bn": tr["oasdi_net_change_in_reserves_bn"],
                    "net_change_share_of_payroll_income":
                        abs(tr["oasdi_net_change_in_reserves_bn"])
                        / oasdi_payroll_income_bn,
                    "note": "160.2bn is the OASDI NET CHANGE IN RESERVES in 2025 (OASI "
                            "-200.0 plus DI +39.8), that is, the amount by which cost "
                            "exceeded TOTAL income including interest. It is not an HI "
                            "figure and not a payroll-only balance.",
                },
            },
            "hi": {
                "capacity_bn": hi_payroll_income_bn,
                "measure": "annual HI payroll income",
                "source": "2026 Trustees summary Table 5: HI payroll taxes 403.2bn, 2025.",
                "superseded_derived_bn": hi_derived_superseded_bn,
                "superseded_note": f"SUPERSEDES {hi_derived_superseded_bn:,.1f}bn, which "
                                   f"applied the statutory 2.9 percent combined rate to "
                                   f"this project's occupational wage bill of "
                                   f"{wage_bill_bn:,.0f}bn. That grid is a SUBSET of "
                                   f"covered earnings, so the derived figure was "
                                   f"{100 * hi_derived_superseded_bn / hi_payroll_income_bn:.1f}"
                                   f" percent of the published one. The gap is the wage "
                                   f"bill, not the rate.",
                "total_income_bn": tr["hi_total_income_bn"],
                "total_income_note": "462.4bn is HI TOTAL income including interest, "
                                     "government contributions and beneficiary premiums. "
                                     "It is NOT a payroll denominator and must not be used "
                                     "as one.",
                "reserves_bn": tr["funds"]["HI"]["reserves_end_2025_bn"],
                "reserves_status": "FILLED from 2026 Trustees summary Table 4, end of 2025. "
                                   "The A85 and A100 BLOCKED record is superseded.",
                "depletion": tr["depletion"]["HI"],
                "in_deficit_now": False,
                "in_deficit_note": "HI was NOT in deficit in 2025: reserves ROSE by 18.2bn, "
                                   "from 237.5 to 255.7. The Trustees put the first year HI "
                                   "cost exceeds income excluding interest at 2026 and "
                                   "including interest at 2027. Any text stating HI is "
                                   "already in deficit is wrong.",
            },
            "landlords_multifamily": {
                "capacity_bn": None,
                "measure": "NOT a dollar capacity. Arrears share that breaches debt service "
                           "coverage, 1 - 1/D",
                "breach_share_range": [1 - 1 / DSCR_RANGE[1], 1 - 1 / DSCR_RANGE[0]],
                "dscr_range": list(DSCR_RANGE),
                "source": "FLAGGED. The agency minimum could not be read: Fannie Form 4660 "
                          "sits behind DUS Navigate and the Freddie Multifamily Guide is a "
                          "JavaScript application. The range 1.20 to 1.35 is carried as a "
                          "flagged proxy.",
            },
        },
    }
    return cap


def main():
    cap = build()
    (OUT / "capacities.json").write_text(json.dumps(cap, indent=2, default=str))
    print("=== ABSORBING CAPACITY, every measure sourced ===")
    print(f"  GDP {cap['gdp_bn']:,.1f}bn ({cap['gdp_as_of']})")
    print(f"  total wage bill {cap['total_wage_bill_bn']:,.1f}bn")
    for k, v in cap["sheets"].items():
        c = v["capacity_bn"]
        print(f"\n  {k}")
        print(f"    capacity: {'n/a' if c is None else f'{c:,.1f}bn'}  [{v['measure']}]")
        print(f"    source:   {v['source'][:150]}")
        if v.get("alt_capacity_bn"):
            print(f"    also:     {v['alt_capacity_bn']:,.1f}bn  [{v['alt_measure'][:90]}]")
        if v.get("flag"):
            print(f"    FLAG:     {v['flag'][:170]}")
        if v.get("reserves_status"):
            print(f"    reserves: {v['reserves_status'][:170]}")


if __name__ == "__main__":
    main()
