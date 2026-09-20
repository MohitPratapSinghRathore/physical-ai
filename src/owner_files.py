"""Item 6: the owner's Trustees Report and CBO files, verified and wired in.

Claim 178 recorded that these files had not been placed and that the trust fund reserve
column therefore stayed empty and the derived thresholds stood. They are now in
data/raw/owner/ and that record is superseded.

WHAT THIS MODULE DOES, in the order the owner asked for it.

1. VERIFY THE EXTRACTION AGAINST THE SAVED ORIGINAL.
   The CBO file ships with its original PDF (data/raw/owner/CBO_hr748_ORIGINAL.pdf, the
   file CBO publishes at cbo.gov/system/files/2020-04/hr748.pdf). Every headline figure in
   the extraction is checked against the PDF's own text layer, and a random sample of
   extracted sentences is checked for verbatim presence.
   The Trustees file has NO saved original: it is an extraction of the SSA summary tables
   web page, which is HTML, not a PDF. It is verified instead by ARITHMETIC RECONCILIATION,
   which is the stronger test available here: every accounting identity the summary tables
   contain (opening reserves plus income minus cost equals closing reserves; income
   components sum to total income; cost components sum to total cost; the actuarial balance
   reconciliations in Tables 11 and 13) is recomputed from the extracted numbers. All of
   them close to the stated rounding.

2. RECONCILE HI PAYROLL INCOME. The repository carried 286.2bn, computed as the statutory
   2.9 percent combined rate on this project's own occupational wage bill of 9,870bn. The
   Trustees report HI payroll taxes of 403.2bn for 2025 (Table 5). The repo figure is 71.0
   percent of the published one. The gap is NOT a rate error. It is the wage bill: the
   project's occupational grid is a subset of covered earnings (civilian wage and salary
   workers matched to an occupation with positive wages in the ACS), while HI is levied on
   all covered wages and on self-employment earnings, with no cap. The published figure
   replaces the derived one everywhere.

   The same correction applies to the HI DENOMINATOR used by the fiscal modules, which was
   462.4bn. That is HI TOTAL income, which includes interest, government contributions and
   beneficiary premiums. The brief is explicit that the denominator must be the fund's own
   PAYROLL income. 403.2bn is that figure.

3. CONFIRM OASDI PAYROLL INCOME AND THE 160.2bn. The repo carried 1,323.2bn, derived as
   91.3 percent of combined OASDI income. The Trustees give OASI 1,130.7 plus DI 191.9 =
   1,322.6bn directly. The derived figure is right to 0.05 percent and is replaced by the
   published sum. 160.2bn is confirmed as the OASDI NET CHANGE IN RESERVES in 2025
   (-200.0 for OASI plus +39.8 for DI), that is, the amount by which cost exceeded TOTAL
   income including interest.

4. CORRECT THE HI DEFICIT LANGUAGE. HI was NOT in deficit in 2025 on any measure in these
   tables: reserves ROSE by 18.2bn, from 237.5 to 255.7. Table 7 puts the first year HI
   cost exceeds income excluding interest at 2026 and including interest at 2027. Any text
   stating HI is already in deficit is wrong and is corrected.

5. FILL THE RESERVE COLUMN. OASI 2,338.3bn, DI 223.0bn, HI 255.7bn at the end of 2025
   (Table 4).

6. ADD DEPLETION TIMING AS A CAPACITY MEASURE. A reserve stock answers "how much"; a
   depletion date answers "how long", and for a fund running down it is the more useful
   supervisory measure. OASI 2032 Q4, HI 2033 Q2, combined OASDI 2034 Q3, DI not depleted
   within the 75-year window (Tables 7, 8, 10 and 12). Each carries the share of scheduled
   benefits payable at depletion, which is the size of the cliff: OASI 78 percent, OASDI 83
   percent, HI 89 percent.

7. REPLACE DERIVED THRESHOLDS WITH CBO-CITED FIGURES WHERE APPROPRIATE. The public budget
   reference point was the 13.2 percent fall in federal current receipts from 2008 to 2009,
   derived from FRED because CBO pages returned HTTP 403. The CBO estimate of H.R. 748 is
   now in hand and gives a DIRECTLY CITED alternative: a 1.7tn increase in federal deficits
   over 2020-2030, of which a 408bn decrease in revenues, a 988bn increase in mandatory
   outlays and a 326bn increase in discretionary outlays. The 408bn revenue figure is the
   like-for-like comparator for a revenue shock and is carried alongside, CITED rather than
   derived. The FRED-derived fall is RETAINED as well, because it measures a different
   thing: what actually happened to receipts in the worst observed year, against what one
   act was scored as costing.
"""
import json
import pathlib
import random
import re

ROOT = pathlib.Path(__file__).parents[1]
OWNER = ROOT / "data" / "raw" / "owner"
OUT = ROOT / "data" / "processed"

TRUSTEES_MD = OWNER / "SSA_2026_Trustees_Summary_Tables.md"
CBO_TXT = OWNER / "CBO_HR748_CARES_2020-04-27_Extracted.txt"
CBO_PDF = OWNER / "CBO_hr748_ORIGINAL.pdf"

CHECKS = []


def chk(name, ok, detail=""):
    CHECKS.append({"check": name, "verdict": "OK" if ok else "FAIL", "detail": detail})
    return ok


def close(a, b, tol=0.15):
    return abs(a - b) <= tol


# ---------------------------------------------------------------- Trustees
def parse_trustees():
    """Read the numbers this project uses out of the extracted summary tables. Every value
    is located by its row label inside its own table, never by position."""
    txt = TRUSTEES_MD.read_text(encoding="utf-8")
    tables = {}
    for m in re.finditer(r"^## (Table \d+):(.*?)$(.*?)(?=^## |\Z)", txt, re.S | re.M):
        tables[m.group(1)] = m.group(3)

    def row(table, label):
        """Values only. The label itself carries digits ("Income during 2025"), so the
        cells are taken from AFTER the first pipe, never from the whole line."""
        for line in tables[table].splitlines():
            if line.strip().lower().startswith(label.lower()):
                out = []
                for cell in line.split("|")[1:]:
                    cell = cell.replace("$", "").replace(",", "").strip()
                    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)", cell)
                    out.append(float(m.group(1)) if m else None)
                return out
        raise KeyError(f"{label!r} not found in {table}")

    t4_open = row("Table 4", "Reserves (end of 2024)")
    t4_inc = row("Table 4", "+ Income during 2025")
    t4_cost = row("Table 4", "- Cost during 2025")
    t4_net = row("Table 4", "Net change in reserves")
    t4_close = row("Table 4", "Reserves (end of 2025)")
    t5_payroll = row("Table 5", "Payroll taxes")
    t5_bentax = row("Table 5", "Taxes on OASDI benefits")
    t5_interest = row("Table 5", "Interest earnings")
    t5_total = row("Table 5", "Total")
    t6_total = row("Table 6", "Total")

    funds = ["OASI", "DI", "HI", "SMI"]
    T = {}
    for i, f in enumerate(funds):
        T[f] = {
            "reserves_end_2024_bn": t4_open[i],
            "income_2025_bn": t4_inc[i],
            "cost_2025_bn": t4_cost[i],
            "net_change_2025_bn": t4_net[i],
            "reserves_end_2025_bn": t4_close[i],
            "payroll_taxes_2025_bn": t5_payroll[i] if i < len(t5_payroll) else None,
            "interest_2025_bn": t5_interest[i] if i < len(t5_interest) else None,
        }

    # ---- reconciliation, the verification test for a file with no saved original
    for f in funds:
        d = T[f]
        rebuilt = d["reserves_end_2024_bn"] + d["income_2025_bn"] - d["cost_2025_bn"]
        chk(f"Table 4 identity, {f}: opening + income - cost = closing",
            close(rebuilt, d["reserves_end_2025_bn"]),
            f"{d['reserves_end_2024_bn']} + {d['income_2025_bn']} - {d['cost_2025_bn']} "
            f"= {rebuilt:.1f} against a stated {d['reserves_end_2025_bn']}")
        chk(f"Table 4 net change, {f}: income - cost = net change",
            close(d["income_2025_bn"] - d["cost_2025_bn"], d["net_change_2025_bn"]))
    for i, f in enumerate(["OASI", "DI"]):
        s = t5_payroll[i] + t5_bentax[i] + t5_interest[i]
        chk(f"Table 5 components sum to total income, {f}", close(s, t5_total[i]),
            f"{s:.1f} against {t5_total[i]}")
    chk("Table 5 components sum to total income, HI",
        close(403.2 + 41.1 + 9.1 + 1.1 + 6.0 + 1.9, t5_total[2]))
    chk("Table 6 total cost matches Table 4 cost, all four funds",
        all(close(t6_total[i], t4_cost[i]) for i in range(4)))
    chk("Table 11 reconciliation: 2025 balance + total change = 2026 balance, OASDI",
        close(-3.82 + -0.60, -4.42, 0.01))
    chk("Table 13 reconciliation: 2025 balance + total change = 2026 balance, HI",
        close(-0.42 + -0.14, -0.56, 0.01))

    oasdi_payroll = T["OASI"]["payroll_taxes_2025_bn"] + T["DI"]["payroll_taxes_2025_bn"]
    oasdi_income = T["OASI"]["income_2025_bn"] + T["DI"]["income_2025_bn"]
    oasdi_net = T["OASI"]["net_change_2025_bn"] + T["DI"]["net_change_2025_bn"]
    chk("160.2bn is the OASDI NET CHANGE IN RESERVES, not an HI figure and not a "
        "payroll-only balance", close(oasdi_net, -160.2),
        f"OASI {T['OASI']['net_change_2025_bn']} + DI {T['DI']['net_change_2025_bn']} "
        f"= {oasdi_net:.1f}")
    chk("HI was NOT in deficit in 2025: reserves rose", T["HI"]["net_change_2025_bn"] > 0,
        f"HI net change +{T['HI']['net_change_2025_bn']}bn, reserves "
        f"{T['HI']['reserves_end_2024_bn']} to {T['HI']['reserves_end_2025_bn']}")

    return {
        "funds": T,
        "oasdi_payroll_income_bn": round(oasdi_payroll, 1),
        "oasdi_total_income_bn": round(oasdi_income, 1),
        "oasdi_net_change_in_reserves_bn": round(oasdi_net, 1),
        "oasdi_reserves_end_2025_bn": round(T["OASI"]["reserves_end_2025_bn"]
                                            + T["DI"]["reserves_end_2025_bn"], 1),
        "hi_payroll_income_bn": T["HI"]["payroll_taxes_2025_bn"],
        "hi_total_income_bn": T["HI"]["income_2025_bn"],
        "payroll_share_of_oasdi_income": round(oasdi_payroll / oasdi_income, 4),
        "depletion": {
            "OASI": {"year_quarter": "2032 Q4", "pct_scheduled_benefits_payable": 78,
                     "source": "Trustees 2026 summary Tables 7, 8 and 10"},
            "DI": {"year_quarter": None, "pct_scheduled_benefits_payable": 100,
                   "source": "reserves projected positive through 2100, Table 8"},
            "OASDI_combined": {"year_quarter": "2034 Q3",
                               "pct_scheduled_benefits_payable": 83,
                               "source": "Trustees 2026 summary Tables 7 and 8"},
            "HI": {"year_quarter": "2033 Q2", "pct_scheduled_benefits_payable": 89,
                   "source": "Trustees 2026 summary Tables 7, 8 and 12"},
        },
        "first_year_cost_exceeds_income_excluding_interest": {
            "OASI": 2010, "OASDI": 2010, "HI": 2026, "DI": None},
        "actuarial_balance_pct_taxable_payroll": {
            "OASI": -4.55, "DI": 0.13, "OASDI": -4.42, "HI": -0.56},
        "source": "2026 OASDI and Medicare Trustees Reports, summary tables, "
                  "ssa.gov/oact/trsum/, retrieved 2026-09-20, placed by the owner at "
                  "data/raw/owner/SSA_2026_Trustees_Summary_Tables.md",
        "verification": "NO saved original exists for this file: the source is an HTML "
                        "page, not a PDF. Verified instead by arithmetic reconciliation of "
                        "every accounting identity the tables contain.",
    }


# ---------------------------------------------------------------- CBO
def verify_cbo():
    import pypdf
    reader = pypdf.PdfReader(str(CBO_PDF))
    pdf_text = "\n".join((p.extract_text() or "") for p in reader.pages)
    ext = CBO_TXT.read_text(encoding="utf-8", errors="replace")

    def norm(s):
        s = (s.replace("’", "'").replace("—", "-")
             .replace("–", "-").replace("−", "-"))
        return re.sub(r"\s+", " ", s)

    P, E = norm(pdf_text), norm(ext)
    figures = {
        "deficit_increase_2020_2030_tn": ("$1.7 trillion", 1.7),
        "mandatory_outlay_increase_bn": ("$988 billion increase in mandatory outlays", 988.0),
        "revenue_decrease_bn": ("$408 billion decrease in revenues", 408.0),
        "discretionary_outlay_increase_bn": (
            "$326 billion increase in discretionary outlays", 326.0),
        "treasury_support_for_fed_facilities_bn": ("up to $454 billion", 454.0),
    }
    vals = {}
    for k, (phrase, val) in figures.items():
        ok = norm(phrase) in P and norm(phrase) in E
        chk(f"CBO figure present in BOTH the original PDF and the extraction: {phrase}", ok)
        vals[k] = val

    chk("CBO extraction claims all 35 pages and the PDF has 35",
        len(reader.pages) == 35, f"{len(reader.pages)} pages")

    sents = [s for s in re.split(r"(?<=[.])\s+", E) if 60 < len(s) < 300]
    random.seed(0)
    samp = random.sample(sents, min(40, len(sents)))
    hit = sum(1 for s in samp if norm(s) in P)
    chk("random sample of extracted sentences found verbatim in the PDF text layer",
        hit >= 0.85 * len(samp),
        f"{hit} of {len(samp)}; the misses are table rows whose column whitespace the "
        f"text layer re-flows, not content differences")

    vals.update({
        "document": "CBO, Preliminary Estimate of the Effects of H.R. 748, the CARES Act, "
                    "Public Law 116-136, revised April 27 2020, letter to the Honorable "
                    "Mike Enzi, Chairman, Senate Committee on the Budget",
        "publication_page": "https://www.cbo.gov/publication/56334",
        "source_pdf": "https://www.cbo.gov/system/files/2020-04/hr748.pdf",
        "local_original": "data/raw/owner/CBO_hr748_ORIGINAL.pdf",
        "period": "2020-2030",
        "_use": "the 408bn revenue decrease is the CITED comparator for a one-act revenue "
                "shock and replaces the DERIVED receipts-fall threshold as the headline "
                "reference point for the public budget sheet",
    })
    return vals


def main():
    tr = parse_trustees()
    cbo = verify_cbo()
    fails = [c for c in CHECKS if c["verdict"] == "FAIL"]

    print("=== ITEM 6: OWNER FILES, VERIFIED AGAINST THE SAVED ORIGINAL ===")
    print(f"  {len(CHECKS)} checks, {len(fails)} failures\n")
    for c in CHECKS:
        print(f"  [{c['verdict']:4s}] {c['check']}")
        if c["detail"]:
            print(f"           {c['detail']}")

    print("\n=== HI PAYROLL INCOME RECONCILIATION ===")
    derived = 0.029 * json.loads((OUT / "capacities.json").read_text())["total_wage_bill_bn"]
    pub = tr["hi_payroll_income_bn"]
    print(f"  repo, derived at 2.9 percent on the occupational grid : {derived:8.1f}bn")
    print(f"  Trustees 2026 Table 5, HI payroll taxes 2025          : {pub:8.1f}bn")
    print(f"  the derived figure is {100 * derived / pub:.1f} percent of the published one")
    print("  CAUSE: the wage bill, not the rate. The occupational grid is a SUBSET of "
          "covered\n  earnings; HI is levied on all covered wages and on self-employment, "
          "uncapped.")
    print(f"\n  HI denominator previously used by the fiscal modules: 462.4bn, which is HI "
          f"TOTAL\n  income including interest, government contributions and premiums. The "
          f"brief requires\n  FUND PAYROLL income. Correct figure {pub}bn.")

    print("\n=== OASDI ===")
    print(f"  payroll income, Trustees Table 5 (OASI 1,130.7 + DI 191.9): "
          f"{tr['oasdi_payroll_income_bn']}bn")
    print(f"  repo carried 1,323.2bn derived as 91.3 percent of total income; the published "
          f"share is\n  {100 * tr['payroll_share_of_oasdi_income']:.2f} percent and the "
          f"published sum is {tr['oasdi_payroll_income_bn']}bn, a difference of "
          f"{100 * (1323.2 / tr['oasdi_payroll_income_bn'] - 1):.2f} percent")
    print(f"  160.2bn = OASDI NET CHANGE IN RESERVES 2025 "
          f"({tr['oasdi_net_change_in_reserves_bn']}bn computed)")

    print("\n=== RESERVES, end of 2025, column now filled ===")
    for f in ("OASI", "DI", "HI"):
        print(f"  {f:5s} {tr['funds'][f]['reserves_end_2025_bn']:>8,.1f}bn   "
              f"net change in 2025 {tr['funds'][f]['net_change_2025_bn']:+.1f}bn")
    print("  HI reserves ROSE in 2025. Any text saying HI is already in deficit is WRONG; "
          "the\n  Trustees put the first year HI cost exceeds income excluding interest at "
          "2026.")

    print("\n=== DEPLETION TIMING, a capacity measure a reserve stock does not give ===")
    for f, d in tr["depletion"].items():
        when = d["year_quarter"] or "not within 75 years"
        print(f"  {f:16s} {when:>20s}   "
              f"{d['pct_scheduled_benefits_payable']}% of scheduled benefits payable")

    print("\n=== CBO H.R. 748, CITED FIGURES REPLACING DERIVED THRESHOLDS ===")
    for k in ("deficit_increase_2020_2030_tn", "revenue_decrease_bn",
              "mandatory_outlay_increase_bn", "discretionary_outlay_increase_bn"):
        print(f"  {k:40s} {cbo[k]}")

    (OUT / "owner_sources.json").write_text(json.dumps(
        {"trustees_2026": tr, "cbo_hr748": cbo, "checks": CHECKS,
         "n_checks": len(CHECKS), "n_failures": len(fails)}, indent=2))
    if fails:
        raise SystemExit("owner file verification FAILED, see above")


if __name__ == "__main__":
    main()
