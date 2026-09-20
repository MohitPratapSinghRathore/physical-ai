"""Generate paper/tables/*.tex from the measured artifacts.

PLAYBOOK SECTION 3. Tables are generated from the same measured files the
\result macros come from, never hand typed. Run: python paper/gen_tables.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "tables"
OUT.mkdir(exist_ok=True)


def load(rel):
    return json.loads((ROOT / rel).read_text())


def rows(rel):
    with (ROOT / rel).open(newline="") as fh:
        return list(csv.DictReader(fh))


def write(name, body):
    (OUT / name).write_text(body.rstrip() + "\n", encoding="utf-8")
    print("wrote", name)


CLASS_LABELS = [
    ("home_mortgage", "Home mortgage"),
    ("credit_card", "Credit card"),
    ("auto_loan", "Auto loan"),
    ("student_loan", "Student loan"),
    ("other_consumer", "Other consumer credit"),
    ("multifamily_mortgage", "Multifamily mortgage"),
    ("treasury", "Treasury debt"),
    ("state_local_debt", "State and local debt"),
    ("corporate_bonds", "Corporate bonds"),
    ("corporate_loans", "Corporate loans"),
    ("noncorporate_business_debt", "Noncorporate business debt"),
    ("commercial_mortgage", "Commercial mortgage"),
    ("corporate_equity", "Corporate equity"),
]

HOLDER_LABELS = [
    ("federal_government", "Federal government"),
    ("banks", "Banks"),
    ("rest_of_world", "Rest of the world"),
    ("other_financial", "Other financial"),
    ("households", "Households, direct"),
    ("state_local_government", "State and local government"),
    ("insurers", "Insurers"),
    ("pensions", "Pension funds"),
    ("nonfinancial_business", "Nonfinancial business"),
    ("residual_unallocated", "Unallocated remainder"),
]


def tab_classes():
    lb = load("framework/labor_backing/direct_ratio_latest.json")
    by = lb["by_class"]
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Claim class & Level (USD bn) & Labor backing & Wage-backed (USD bn) \\",
             r"\midrule"]
    for key, label in CLASS_LABELS:
        c = by[key]
        mark = r"\,$\dagger$" if c["backing"] == 0 else ""
        lines.append(f"{label}{mark} & {c['level_bn']:,.1f} & {c['backing']:.4f} "
                     f"& {c['labour_backed_bn']:,.1f} \\\\")
    lines += [r"\midrule",
              f"All thirteen classes & {lb['total_claims_bn']:,.1f} & "
              f"{lb['direct_labour_backing_ratio']:.4f} & {lb['labour_backed_bn']:,.1f} \\\\",
              r"\bottomrule", r"\end{tabular}"]
    write("tab_claim_classes.tex", "\n".join(lines))


def tab_sensitivity():
    rs = rows("framework/labor_backing/debt_only_sensitivity.csv")
    lines = [r"\begin{tabular}{lrr}", r"\toprule",
             r"Judgement call & Debt-only ratio & Move (per cent) \\", r"\midrule"]
    for r in rs:
        call = r["judgement_call"].replace("THE ONE-STEP RULE: ", "The one-step rule: ")
        call = "Central case" if call == "CENTRAL" else call
        lines.append(f"{call} & {float(r['debt_only_ratio']):.4f} "
                     f"& {float(r['move_pct']):+.2f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_debt_only_sensitivity.tex", "\n".join(lines))


def tab_series():
    years = ["1952", "1970", "1990", "2000", "2008", "2020", "2025"]
    dr = {r["year"]: r for r in rows("framework/labor_backing/direct_ratio_timeseries.csv")}
    do = {r["year"]: r for r in rows("framework/labor_backing/debt_only_ratio_timeseries.csv")}
    lines = [r"\begin{tabular}{lrrrrr}", r"\toprule",
             r"Year & Debt-only ratio & All-claims ratio & Federal, union "
             r"& \quad as creditor & \quad as debtor \\", r"\midrule"]
    for y in years:
        a, b = dr[y], do[y]
        held = float(a["sovereign_share_of_labour_backed"])
        obl = float(a["sovereign_obligor_bn"]) / float(a["labour_backed_bn"])
        lines.append(f"{y} & {float(b['DEBT_ONLY_ratio_direct']):.4f} & "
                     f"{float(a['direct_labour_backing_ratio']):.4f} & "
                     f"{float(a['sovereign_share_union']):.4f} & {held:.4f} & {obl:.4f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_series.tex", "\n".join(lines))


def tab_holders():
    lb = load("framework/labor_backing/direct_ratio_latest.json")
    sh = lb["labour_backed_by_holder_share"]
    bn = lb["labour_backed_by_holder_bn"]
    lines = [r"\begin{tabular}{lrr}", r"\toprule",
             r"Holder & Wage-backed claims held (USD bn) & Share \\", r"\midrule"]
    for key, label in HOLDER_LABELS:
        lines.append(f"{label} & {bn[key]:,.1f} & {sh[key]:.4f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_holders.tex", "\n".join(lines))


def tab_structural():
    rs = rows("framework/labor_backing/item3_sovereign_robustness.csv")
    keep = {
        "THE ONE-STEP RULE: business classes zero (central) vs the B2 indirect share":
            "Indirectly wage-backed claims included",
        "commercial mortgage treated like multifamily rather than zero":
            "Commercial mortgage treated as rent-serviced",
        "agency pools NOT federal (guarantee ignored)":
            "Agency pools not treated as federal",
        "obligor leg EXCLUDED (holder and guarantor only)":
            "Federal debtor position excluded",
    }
    central = float(rs[0]["central_sovereign_union"])
    lines = [r"\begin{tabular}{lrr}", r"\toprule",
             r"Structural choice & Federal exposure & Move (per cent) \\", r"\midrule",
             f"Central case & {central:.4f} & 0.00 \\\\"]
    for r in rs:
        lab = keep.get(r["judgement_call"])
        if lab:
            lines.append(f"{lab} & {float(r['sovereign_union']):.4f} "
                         f"& {float(r['move_pct']):+.2f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_structural.tex", "\n".join(lines))


QLAB = {"Q1_bottom": "Bottom quintile", "Q2": "Second quintile", "Q3_middle": "Middle quintile",
        "Q4": "Fourth quintile", "Q5_top": "Top quintile"}


def tab_quintile():
    rs = rows("framework/labor_backing/quintile_labour_backing.csv")
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Wage quintile & Share of the wage bill & Share of household wage-backed claims "
             r"& Claims per wage dollar \\", r"\midrule"]
    for r in rs:
        per = ("withdrawn" if r["wage_quintile"] == "Q1_bottom"
               else f"{float(r['labour_backed_per_unit_wage_bill']):.4f}")
        lines.append(f"{QLAB[r['wage_quintile']]} & "
                     f"{float(r['quintile_wage_bill_share']):.4f} & "
                     f"{float(r['share_of_household_labour_backed']):.4f} & {per} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_quintile.tex", "\n".join(lines))


if __name__ == "__main__":
    tab_classes()
    tab_sensitivity()
    tab_series()
    tab_holders()
    tab_structural()
    tab_quintile()
