"""B1. The bridge from income sources to backing coefficients, one row per claim class.

SPECIFICATION, STATED BEFORE COMPUTING. For each of the thirteen classes the table gives the
numerator and the denominator of the coefficient, the source they come from, the proxy
assumption that stands between the two, and an alternative estimate where one exists. The
alternative is the wage-share-of-servicing-income figure from B2 for the household classes,
the published variant where the rules file carries one, and n/a where neither exists.

CONSOLIDATION RULE, stated once and applied throughout. A claim is assigned to the party that
bears the credit risk, not to the party that holds legal title. An agency-guaranteed mortgage
sits in a security held by a pension fund or a foreign investor, but the guarantee means the
credit loss falls on the guarantor, so the claim is assigned to the federal sector. A loan
sold into a private securitization carries no such guarantee, so it is assigned to the holders
of the securities. Treasury debt is assigned by the income that services it rather than by who
owns the security, which is the receipts convention of the accounts. The one place this rule
cannot be applied from the data is the private mortgage remainder, which is an arithmetic
residual and is treated as private in full.

STATUS. MEASURED levels and coefficients; the proxy assumptions are stated assumptions.
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent

# numerator and denominator of each coefficient, and the proxy standing between them
SPEC = {
    "home_mortgage": (
        "mortgage service paid by households with an employed member aged 25 to 64",
        "mortgage service paid by all households",
        "American Community Survey 2023",
        "who pays the service stands in for what income pays it"),
    "credit_card": (
        "card balances owed by working-core households",
        "card balances owed by all households",
        "Survey of Income and Program Participation 2025",
        "who owes stands in for what income services the balance"),
    "auto_loan": (
        "vehicle loan balances owed by working-core households",
        "vehicle loan balances owed by all households",
        "Survey of Income and Program Participation 2025",
        "who owes stands in for what income services the balance"),
    "student_loan": (
        "student loan balances owed by working-core households",
        "student loan balances owed by all households",
        "Survey of Income and Program Participation 2025",
        "who owes stands in for what income services the balance"),
    "other_consumer": (
        "balance-weighted mean of the card, auto and student coefficients",
        "the same three classes",
        "derived from the three above",
        "the residual consumer class is assumed to resemble the three measured ones"),
    "multifamily_mortgage": (
        "gross rent paid by households with an employed member aged 25 to 64",
        "gross rent paid by all renter households",
        "American Community Survey 2023",
        "rent is assumed to service the mortgage on the building one for one"),
    "treasury": (
        "social insurance contributions in full plus the wage share of the individual "
        "income tax",
        "federal current receipts",
        "national accounts and Statistics of Income",
        "receipts composition stands in for the composition of debt service"),
    "state_local_debt": (
        "the wage-linked share of state and local own receipts",
        "state and local own receipts",
        "national accounts and Statistics of Income",
        "as for Treasury debt"),
    "corporate_bonds": ("zero by the one-step rule", "n/a", "convention",
                        "business revenue is not traced further"),
    "corporate_loans": ("zero by the one-step rule", "n/a", "convention",
                        "business revenue is not traced further"),
    "noncorporate_business_debt": ("zero by the one-step rule", "n/a", "convention",
                                   "business revenue is not traced further"),
    "commercial_mortgage": ("zero by the one-step rule", "n/a", "convention",
                            "rent from business tenants is not traced further"),
    "corporate_equity": ("zero by the one-step rule", "n/a", "convention",
                         "excluded from the debt-only denominator in any case"),
}


def main():
    with (ROOT / "framework/labor_backing/claim_class_rules.csv").open(
            newline="", encoding="utf-8") as fh:
        rules = {r["claim_class"]: r for r in csv.DictReader(fh)}
    alt_path = HERE / "b2_backing_basis.json"
    alt = {}
    if alt_path.exists():
        for r in json.loads(alt_path.read_text())["by_class"]:
            alt[r["claim_class"]] = r["wage_share_of_servicing_income"]

    rows = []
    for key, (num, den, src, proxy) in SPEC.items():
        r = rules[key]
        alternative = alt.get(key)
        if alternative is None:
            v = r["variants"].split(";")[0].strip() if r["variants"] else ""
            alternative = v if v else "n/a"
        else:
            alternative = f"{alternative:.4f} (wage share of servicing income)"
        rows.append({
            "claim_class": key,
            "label": r["label"],
            "level_bn": r["level_bn"],
            "coefficient": r["labour_backing_share"],
            "numerator": num,
            "denominator": den,
            "source": src,
            "proxy_assumption": proxy,
            "alternative_estimate": alternative,
        })
    assert len(rows) == 13, f"expected thirteen classes, built {len(rows)}"
    with (HERE / "b1_bridge.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote b1_bridge.csv with {len(rows)} classes; "
          f"{sum(1 for r in rows if 'wage share' in r['alternative_estimate'])} carry the "
          f"wage-share alternative")


if __name__ == "__main__":
    main()
