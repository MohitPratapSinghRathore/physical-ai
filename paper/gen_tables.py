"""Generate paper/tables/*.tex from the measured artifacts.

PLAYBOOK SECTION 3. Tables are generated from the same measured files the
\result macros come from, never hand typed. Run: python paper/gen_tables.py
"""
import csv
import json
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "tables"
OUT.mkdir(exist_ok=True)


def load(rel):
    return json.loads((ROOT / rel).read_text())


def rows(rel):
    with (ROOT / rel).open(newline="") as fh:
        return list(csv.DictReader(fh))


# Tables whose natural width exceeds the text block. The replacement column
# specification lets long headers wrap; the tighter column separation does the rest.
# Presentation only: no value in any cell is affected.
WIDE = {
    "tab_tau_k.tex": ("{llrrrr}", "{p{2.9cm}p{2.2cm}rp{2.1cm}rr}"),
    "tab_relief.tex": ("{lrrrrr}", "{p{4.0cm}rrrrr}"),
    "tab_incidence_holder.tex": ("{lrrr}", "{p{4.8cm}p{2.2cm}p{2.5cm}p{2.5cm}}"),
    "tab_under_reporting.tex": ("{lrrrr}", "{lrrrr}"),
    "tab_institutions_by_model.tex": ("{lrrrrrr}", "{lrrrrrr}"),
}


def fit(name, body):
    """Apply the width treatment for one table, if it needs one."""
    if name not in WIDE:
        return body
    old, new = WIDE[name]
    body = body.replace(r"\begin{tabular}" + old, r"\begin{tabular}" + new, 1)
    return r"\setlength{\tabcolsep}{4pt}" + "\n" + body


def write(name, body):
    body = fit(name, body)
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
    """Table 2, on the ADOPTED basis.

    The five household coefficients are the debt-weighted wage share of the income that
    services each class, which is what the definition asks for. They are taken from
    b2_backing_basis; every other class is unchanged by the choice of basis. The
    wage-backed column is the level times the coefficient, and the total row is the
    all-claims direct ratio on the same basis.
    """
    lb = load("data/release/labor_backing/direct_ratio_latest.json")
    b2 = load("data/release/revision_r2/b2_headline_effect.json")
    adopted = {k: v["alternative"] for k, v in b2["coefficients"].items()}
    by = lb["by_class"]
    total_claims = lb["total_claims_bn"]
    ratio = b2["alternative"]["ratios"]["all_claims_direct"]
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Claim class & Level (USD bn) & Labor backing & Wage-backed (USD bn) \\",
             r"\midrule"]
    for key, label in CLASS_LABELS:
        c = by[key]
        backing = adopted.get(key, c["backing"])
        mark = r"\,$\dagger$" if backing == 0 else ""
        lines.append(f"{label}{mark} & {c['level_bn']:,.1f} & {backing:.4f} "
                     f"& {backing * c['level_bn']:,.1f} \\\\")
    lines += [r"\midrule",
              f"All thirteen classes & {total_claims:,.1f} & "
              f"{ratio:.4f} & {ratio * total_claims:,.1f} \\\\",
              r"\bottomrule", r"\end{tabular}"]
    write("tab_claim_classes.tex", "\n".join(lines))



# The sensitivity file carries the project's internal labels; these are the paper's.
SENS_LABEL = {
    "CENTRAL": "Central case",
    "THE ONE-STEP RULE: business classes take the indirect share":
        "The one-step rule: business classes take the indirect share",
    "federal receipts: the 77.7 percent upper bound":
        "Federal receipts at the upper bound of the labor-linked share",
    "commercial mortgage treated like multifamily":
        "Commercial mortgage treated as rent-serviced",
    "mortgage backing: the superseded A38 definition":
        "Mortgage backing on the earlier definition",
    "state and local: all personal current taxes":
        "State and local debt against all personal current taxes",
    "mortgage backing: SIPP balances":
        "Mortgage backing from survey balances rather than payments",
    "rent backing: the A38 definition": "Rent backing on the earlier definition",
    "other consumer: the card share alone":
        "Other consumer credit at the card share alone",
}


def tab_sensitivity():
    rs = rows("data/release/labor_backing/debt_only_sensitivity.csv")
    lines = [r"\begin{tabular}{lrr}", r"\toprule",
             r"Judgement call & Debt-only ratio & Move (per cent) \\", r"\midrule"]
    for r in rs:
        call = SENS_LABEL.get(r["judgement_call"], r["judgement_call"])
        lines.append(f"{call} & {float(r['debt_only_ratio']):.4f} "
                     f"& {float(r['move_pct']):+.2f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_debt_only_sensitivity.tex", "\n".join(lines))


def tab_series():
    years = ["1952", "1970", "1990", "2000", "2008", "2020", "2025"]
    dr = {r["year"]: r for r in rows("data/release/labor_backing/direct_ratio_timeseries.csv")}
    do = {r["year"]: r for r in rows("data/release/labor_backing/debt_only_ratio_timeseries.csv")}
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
    lb = load("data/release/labor_backing/direct_ratio_latest.json")
    sh = lb["labour_backed_by_holder_share"]
    bn = lb["labour_backed_by_holder_bn"]
    lines = [r"\begin{tabular}{lrr}", r"\toprule",
             r"Holder & Wage-backed claims held (USD bn) & Share \\", r"\midrule"]
    for key, label in HOLDER_LABELS:
        lines.append(f"{label} & {bn[key]:,.1f} & {sh[key]:.4f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_holders.tex", "\n".join(lines))


def tab_structural():
    rs = rows("data/release/labor_backing/item3_sovereign_robustness.csv")
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
    rs = rows("data/release/labor_backing/quintile_labour_backing.csv")
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Wage quintile & Share of the wage bill & Share of household wage-backed claims "
             r"& Claims per wage dollar \\", r"\midrule"]
    b2 = load("data/release/revision_r2/b2_headline_effect.json")
    adopted = b2["quintile_gradient"]["alternative"]
    for r in rs:
        per = ("withdrawn" if r["wage_quintile"] == "Q1_bottom"
               else f"{float(adopted[r['wage_quintile']]):.4f}")
        lines.append(f"{QLAB[r['wage_quintile']]} & "
                     f"{float(r['quintile_wage_bill_share']):.4f} & "
                     f"{float(r['share_of_household_labour_backed']):.4f} & {per} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_quintile.tex", "\n".join(lines))


def tab_under_reporting():
    b = load("data/release/method/benchmark_cap_summary.json")["under_reporting"]
    label = {"mortgage": "Mortgage", "card": "Credit card", "auto": "Auto",
             "student": "Student"}
    lines = [r"\begin{tabular}{lrrrr}", r"\toprule",
             r"Book & Official aggregate (USD bn) & Survey universe (USD bn) "
             r"& Under-reporting factor & Coverage share \\", r"\midrule"]
    for r in b:
        lines.append(f"{label[r['loan']]} & {r['official_aggregate_bn']:,.1f} & "
                     f"{r['sipp_FULL_universe_bn']:,.1f} & "
                     f"{r['UNDER_REPORTING_factor']:.4f} & "
                     f"{r['working_core_share_of_full']:.4f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_under_reporting.tex", "\n".join(lines))


def tab_tau_k():
    tk = load("data/release/tau_k/tau_k_assembled.json")
    req = tk["required_tau_k"]
    name = {"Barkai": "First rent reading", "Karabarbounis_Neiman_case_R": "Second rent reading"}
    lines = [r"\begin{tabular}{llrrrr}", r"\toprule",
             r"Base for the taxable holder share & Rent reading & Central & Fifth to "
             r"ninety-fifth & Analytic maximum & Share of the space that closes \\",
             r"\midrule"]
    for row, cen in zip(tk["assembled_SOURCED"], tk["assembled_CENTRAL_at_sourced_centrals"]):
        lines.append(
            f"All equity outstanding & {name[row['rent_reading']]} & "
            f"{cen['tau_k_central']:.4f} & {row['tau_k_p05']:.4f} to {row['tau_k_p95']:.4f} & "
            f"{row['tau_k_max_ANALYTIC']:.4f} & {row['pass_share_vs_required_low']:.4f} \\\\")
    for row in tk["MARKED_SENSITIVITY_at_CRS_implied_theta"]:
        lines.append(
            f"Domestically held stock & {name[row['rent_reading']]} & "
            f"{row['tau_k_central']:.4f} & {row['tau_k_p05']:.4f} to {row['tau_k_p95']:.4f} & "
            f"{row['tau_k_max_ANALYTIC']:.4f} & {row['pass_share_vs_required_low']:.4f} \\\\")
    lines += [r"\midrule",
              f"Required, easier labor tax reading & & {req['by_labour_reading']['AMR_0.255']:.4f}"
              r" & & & \\",
              "Required, harder labor tax reading & & "
              f"{req['by_labour_reading']['bottom_up_0.318']:.4f}" + r" & & & \\",
              r"\bottomrule", r"\end{tabular}"]
    write("tab_tau_k.tex", "\n".join(lines))


def tab_levers():
    tk = load("data/release/tau_k/tau_k_assembled.json")
    label = {"deferral_factor": "Deferral and step-up at death",
             "state_cit_effective": "State corporate income tax",
             "shifted_share": "Profit shifting",
             "shareholder_rate": "Shareholder-level statutory rate",
             "debt_share": "Debt share of AI capital",
             "bondholder_rate": "Effective rate on bondholders",
             "theta_taxable": "Share of equity in taxable accounts"}
    movers = sorted(tk["single_parameter_movers"], key=lambda m: -m["swing"])
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Lever & Rate at the low end & Rate at the high end & Swing \\", r"\midrule"]
    for m in movers:
        lines.append(f"{label[m['parameter']]} & {m['tau_k_at_range_low']:.4f} & "
                     f"{m['tau_k_at_range_high']:.4f} & {m['swing']:.4f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_levers.tex", "\n".join(lines))


EXPOSURE = {"embodied": "Physically exposed", "cognitive_AIOE": "Cognitively exposed, first index",
            "cognitive_GPT": "Cognitively exposed, second index"}


def tab_incidence_holder():
    rs = [r for r in rows("data/release/dose_response/sovereign_consolidation.csv")
          if r["dose"] == "0.1" and r["incidence"] == "c_sourced_mix"]
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Where the first-round loss lands & " +
             " & ".join(EXPOSURE[r["exposure_type"]] for r in rs) + r" \\",
             r"\midrule"]
    fields = [("general_revenue_bn", "Federal general revenue"),
              ("oasdi_bn", "Social security trust funds"),
              ("hi_bn", "Hospital insurance trust fund"),
              ("federal_student_bn", "Federal student loan book"),
              ("fha_bn", "Federal housing administration"),
              ("gse_loss_bn", "Housing agencies, gross"),
              ("federal_first_round_bn", "Federal, total"),
              ("private_first_round_bn", "Private holders, total")]
    for key, label in fields:
        vals = " & ".join(f"{float(r[key]):,.1f}" for r in rs)
        lines.append(f"{label} & {vals} \\\\")
    lines.append("Federal share & " +
                 " & ".join(f"{float(r['federal_share_first_round']):.3f}" for r in rs)
                 + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_incidence_holder.tex", "\n".join(lines))


def tab_federal_share_by_dose():
    rs = rows("data/release/incidence/federal_share_by_dose.csv")
    lines = [r"\begin{tabular}{lrrl}", r"\toprule",
             r"Displacement, share of the wage bill & Narrow reading & "
             r"Conservatorship reading & Inside the data \\", r"\midrule"]
    for r in rs:
        inside = "yes" if r["inside_observed_data_range"].lower().startswith("t") else "no"
        lines.append(
            f"{100 * float(r['dose_share_of_total_wage_bill']):.0f} per cent & "
            f"{float(r['narrow_low']):.3f} to {float(r['narrow_high']):.3f} & "
            f"{float(r['conservatorship_low']):.3f} to "
            f"{float(r['conservatorship_high']):.3f} & {inside} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_federal_share_by_dose.tex", "\n".join(lines))


def tab_buffers():
    seen = {}
    for r in rows("data/release/dose_response/by_wage_quintile_dose_response.csv"):
        seen.setdefault(r["wage_quintile"], r)
    lines = [r"\begin{tabular}{lrrr}", r"\toprule",
             r"Wage quintile & Mean wage (USD) & Median months of runway & "
             r"Under one month (per cent) \\", r"\midrule"]
    for key in ("Q1_bottom", "Q2", "Q3_middle", "Q4", "Q5_top"):
        r = seen[key]
        lines.append(f"{QLAB[key]} & {float(r['mean_wage']):,.0f} & "
                     f"{float(r['median_runway_months']):.3f} & "
                     f"{float(r['pct_under_1_month']):.3f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_buffers.tex", "\n".join(lines))


def tab_attrition():
    ten = {}
    for r in rows("data/release/dose_response/dose_response_first_round.csv"):
        if r["dose_share_of_total_wage_bill"] == "0.1":
            ten.setdefault((r["exposure_type"], r["incidence"]), r)
    lines = [r"\begin{tabular}{llrrrr}", r"\toprule",
             r"Exposure group & Who is displaced & Federal budget & Mortgage & Auto "
             r"& Student \\", r"\midrule"]
    case = {"a_incumbents": "incumbents only", "b_entrants": "non-hiring",
            "c_sourced_mix": "sourced mix"}
    for et in ("embodied", "cognitive_AIOE", "cognitive_GPT"):
        for inc in ("a_incumbents", "b_entrants", "c_sourced_mix"):
            r = ten[(et, inc)]
            lines.append(
                f"{EXPOSURE[et]} & {case[inc]} & "
                f"{float(r['public_budget_loss_hi_bn']):,.2f} & "
                f"{float(r['mortgage_national_loss_hi_bn']):,.2f} & "
                f"{float(r['auto_lenders_loss_hi_bn']):,.2f} & "
                f"{float(r['student_loan_holders_loss_hi_bn']):,.2f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_attrition.tex", "\n".join(lines))


def tab_institutions_by_model():
    rs = [r for r in rows("data/release/institutions/a2_distribution_by_class.csv")
          if r["cut"] == "model"]
    models = ["card-heavy", "credit union", "auto-heavy", "C and I heavy",
              "commercial real estate heavy", "diversified", "mortgage portfolio lender"]
    label = {"card-heavy": "Card-heavy lenders", "credit union": "Credit unions",
             "auto-heavy": "Auto-heavy lenders", "C and I heavy": "Commercial and industrial",
             "commercial real estate heavy": "Commercial real estate heavy",
             "diversified": "Diversified", "mortgage portfolio lender": "Mortgage portfolio"}
    idx = {(r["dose"], r["business_model"]): r for r in rs}
    lines = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
             r"Business model & Institutions & Assets (USD bn) & \multicolumn{3}{c}"
             r"{Per cent of assets in breach} \\",
             r"\cmidrule(lr){4-6}",
             r" & & & at 10 per cent & at 25 per cent & at 50 per cent \\", r"\midrule"]
    for m in models:
        base = idx[("0.1", m)]
        lines.append(
            f"{label[m]} & {float(base['n']):,.0f} & {float(base['assets_bn']):,.0f} & "
            f"{float(idx[('0.1', m)]['pct_assets_breaching']):.2f} & "
            f"{float(idx[('0.25', m)]['pct_assets_breaching']):.2f} & "
            f"{float(idx[('0.5', m)]['pct_assets_breaching']):.2f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_institutions_by_model.tex", "\n".join(lines))


def tab_relief():
    """Relief instruments with the second round fixed and with demand feedback."""
    rs = [r for r in rows("data/release/revision_r1/a3_relief_feedback.csv")
          if r["dose"] == "0.1"]
    pairs = {}
    for r in rs:
        pairs.setdefault(r["instrument"], {})[
            "fixed" if r["feedback"].startswith("none") else "feedback"] = r
    label = {"combined package": "All together: forbearance, income-driven repayment "
                                 "and enhanced wage insurance",
             "wage insurance, current US, 0.50 for 26 weeks":
                 "Wage insurance, 0.50 replacement for 26 weeks",
             "wage insurance, enhanced, 0.70 for 52 weeks":
                 "Wage insurance, 0.70 replacement for 52 weeks",
             "forbearance, full": "Forbearance on mortgage and consumer credit"}
    order = ["forbearance, full", "wage insurance, current US, 0.50 for 26 weeks",
             "wage insurance, enhanced, 0.70 for 52 weeks", "combined package"]
    lines = [r"\begin{tabular}{lrrrrr}", r"\toprule",
             r"Instrument & \multicolumn{2}{c}{Second round fixed} "
             r"& \multicolumn{2}{c}{With demand feedback} & Fiscal cost \\",
             r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}",
             r" & USD bn & per cent & USD bn & per cent & USD bn \\", r"\midrule"]
    for key in order:
        a, b = pairs[key]["fixed"], pairs[key]["feedback"]
        cost = a["fiscal_cost_bn"]
        cost = "n/a" if cost in ("", "None") else f"{float(cost):,.0f}"
        lines.append(
            f"{label[key]} & {float(a['loss_removed_bn']):,.1f} & "
            f"{float(a['loss_removed_pct']):.1f} & {float(b['loss_removed_bn']):,.1f} & "
            f"{float(b['loss_removed_pct']):.1f} & {cost} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_relief.tex", "\n".join(lines))




HOLDER_NAME = {"federal_government": "Federal government", "banks": "Banks",
               "rest_of_world": "Rest of the world", "other_financial": "Other financial",
               "households": "Households", "state_local_government": "State and local",
               "insurers": "Insurers", "pensions": "Pension funds",
               "nonfinancial_business": "Nonfinancial business",
               "residual_unallocated": "Unallocated remainder"}


def tab_payoff():
    rs = rows("data/release/ai_bust/b4_payoff_by_holder.csv")
    lines = [r"\begin{tabular}{lrrrrr}", r"\toprule",
             r"Holder & Wage side & AI side & AI fails & Partial & AI succeeds \\",
             r"\midrule"]
    for r in rs:
        lines.append(f"{HOLDER_NAME[r['holder']]} & {float(r['wage_leg_share']):.4f} & "
                     f"{float(r['ai_leg_share']):.4f} & {float(r['net_ai_fails']):+.4f} & "
                     f"{float(r['net_partial']):+.4f} & {float(r['net_success']):+.4f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_payoff.tex", "\n".join(lines))


def tab_tiers():
    tiers = load("data/release/ai_bust/b1_tiers.json")["tiers"]
    lines = [r"\begin{tabular}{p{2.1cm}p{6.3cm}rp{3.1cm}}", r"\toprule",
             r"Tier & What it covers & Size (USD bn) & Confidence \\", r"\midrule"]
    for x in tiers:
        size = x["size_bn"]
        if size is None:
            size = "n/a"
        elif isinstance(size, dict):
            size = f"{min(size.values()):,.0f} to {max(size.values()):,.0f}"
        else:
            size = f"{size:,.1f}"
        conf = x["confidence"].split(",")[0].split(".")[0]
        lines.append(f"{x['tier']} & {x['what']} & {size} & {conf} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_ai_tiers.tex", "\n".join(lines))


def _clean(s, limit=None):
    s = s.replace("**", "").replace("&", "and").replace("_", " ")
    s = re.sub(r"\bdoses?\b", "displacement level", s)
    # the architecture note uses British spelling and capitalised emphasis; the paper does not
    for a, b in (("labour", "labor"), ("Labour", "Labor"), ("pre-fund", "pre-fund"),
                 ("BEFORE", "before"), ("NOT", "not"), ("SOONEST", "soonest"),
                 ("CHEAPEST", "cheapest"), ("HARDEST", "hardest"), ("ALL", "all"),
                 ("BAND", "band"), ("MEASURED", "measured"), ("SCENARIO", "scenario"),
                 ("REPLICATED", "rebuilt"), ("STANDING", "measured")):
        s = re.sub(r"\b%s\b" % a, b, s)
    s = s.replace("inside the data and larger displacement level",
                  "inside the data and at larger displacement")
    s = s.split(";")[0].split(",")[0] if limit == "short" else s
    return s


def tab_instruments():
    rs = rows("data/release/architecture/instruments.csv")
    head = (r"\begin{longtable}{@{}p{0.4cm}p{3.0cm}p{5.0cm}p{1.4cm}p{3.4cm}@{}}")
    cap = (r"\caption{The twelve instruments, the institution that must act, and the regime "
           r"in which each binds. Generated from the released architecture file, which also "
           r"carries the measured mechanism and the verified precedent for every row.}"
           r"\label{tab:instruments}\\")
    colhead = (r"\toprule" "\n"
               r"\# & Institution that must act & Instrument & Type & Binds in \\" "\n"
               r"\midrule" "\n"
               r"\endfirsthead" "\n"
               r"\toprule" "\n"
               r"\# & Institution that must act & Instrument & Type & Binds in \\" "\n"
               r"\midrule" "\n"
               r"\endhead" "\n"
               r"\bottomrule" "\n"
               r"\endfoot")
    lines = [head, cap, colhead]
    for r in rs:
        lines.append(" & ".join([
            r["n"], _clean(r["institution"]), _clean(r["instrument"])[:150],
            _clean(r["type"]), _clean(r["binds_in"])[:80]]) + r" \\")
    lines.append(r"\end{longtable}")
    write("tab_instruments.tex", "\n".join(lines))



# The clearing pass decides WHICH quantities were removed; these are the paper's own
# words for each one. The assert below fails if the two ever drift apart.
REMOVED_TEXT = {
    "incidence_count_spread": (
        "Household counts move by only five to nine per cent across incidence cases",
        "Not reproducible. Under the rebuilder's most natural reading of one case the "
        "spread is fifty-nine per cent, which removes the stability the claim rested on, "
        "and our own brief did not say which reading was intended."),
    "rho_50pct": (
        "The share of displaced wages re-earned at fifty per cent displacement",
        "There is no such number. At that level no exposure group has a solution inside "
        "the observed range, and the physically exposed group has no admissible solution "
        "at all. Only a band can be reported."),
    "hedge_ratio_at_operative": (
        "The share of the federal wage loss offset by capital tax receipts",
        "One of its inputs was never defined in our own brief, so the quantity cannot be "
        "rebuilt from the specification. The claim is not that the offset is zero: it is "
        "that we cannot size it."),
    "quintile_labour_backed_Q1": (
        "Wage-backed claims per wage dollar in the bottom quintile",
        "An independent rebuild landed a factor of two and a half to three and a half "
        "away, and we cannot show its reading was wrong, because we defined neither the "
        "universe nor the normalisation. The gradient survives; this magnitude does not."),
    "exposure_index_scores": (
        "The two occupation-level scores of cognitive exposure",
        "Eleven mismatches in the rebuild, running in opposite directions on the two "
        "indices, so it is not a single weighting error. The wage machinery passes its "
        "controls; the index scores are unsettled."),
}


def tab_removed():
    rs = [r for r in rows("data/release/headline_clearing_pass.csv")
          if r["tag"] == "REMOVED"]
    ids = {r["id"] for r in rs}
    assert ids == set(REMOVED_TEXT), (
        f"removed claims in the release {sorted(ids)} do not match the text keys "
        f"{sorted(REMOVED_TEXT)}")
    lines = [r"\begin{tabular}{p{5.6cm}p{9.0cm}}", r"\toprule",
             r"Quantity & Why it is not in this paper \\", r"\midrule"]
    for r in rs:
        claim, why = REMOVED_TEXT[r["id"]]
        lines.append(f"{claim} & {why} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    write("tab_removed.tex", "\n".join(lines))



def tab_bridge():
    """Table 3: from income sources to backing coefficients, one row per claim class.

    Set as a longtable so that it breaks across pages rather than overrunning one. The
    coefficient column is the ADOPTED wage basis; the cross-check column carries the
    coverage construction, which is the one that was independently rebuilt. Identifiers
    from the source files are written out in words here.
    """
    rs = rows("data/release/revision_r2/b1_bridge.csv")
    b2 = load("data/release/revision_r2/b2_headline_effect.json")
    adopted = {k: v["alternative"] for k, v in b2["coefficients"].items()}
    coverage = {k: v["published"] for k, v in b2["coefficients"].items()}
    short = {"Home mortgages, one to four family": "Home mortgage",
             "Revolving consumer credit": "Credit card",
             "Consumer credit, automobile loans": "Auto loan",
             "Consumer credit, student loans": "Student loan",
             "Other consumer credit": "Other consumer",
             "Multifamily residential mortgages": "Multifamily mortgage",
             "Treasury securities": "Treasury debt",
             "State and local government debt": "State and local debt"}
    # the source files carry short identifiers; the paper prints words
    PLAIN = {
        "acs_a38_definition=0.69913":
            "the earlier rent definition gives 0.699",
        "one_step_traced_to_demand=see B2":
            "business revenue traced one further step, reported in Appendix~\\ref{app:detail} "
            "and never blended with the headline",
        "business revenue is not traced further":
            "business revenue is not traced further",
        "excluded from the debt-only denominator in any case":
            "excluded from the debt-only denominator in any case",
        "n/a": "",
    }

    def plain(text):
        text = text.strip()
        out = PLAIN.get(text)
        if out is not None:
            return out
        if "(wage share of servicing income)" in text:
            return "the wage share of servicing income, adopted here"
        return text.replace("_", " ").replace("=", " gives ")

    header = (r"Class & Numerator & Denominator & Source & Coefficient & "
              r"Coverage & Proxy assumption \\")
    caption = (r"\caption{From income sources to backing coefficients: the numerator, the "
               r"denominator, the source and the proxy assumption for each class. The "
               r"coefficient column is the adopted wage basis; the cross-check column is the "
               r"coverage construction, which is the one that was independently rebuilt, and "
               r"reads ``same'' where the basis does not apply. Measured; the proxy "
               r"assumptions are stated assumptions.}\label{tab:bridge}\\")
    lines = [r"\begin{longtable}{p{1.5cm}p{2.6cm}p{1.9cm}p{1.7cm}p{1.1cm}p{1.1cm}p{2.8cm}}",
             caption,
             r"\toprule", header, r"\midrule", r"\endfirsthead",
             r"\multicolumn{7}{l}{\itshape Table \ref{tab:bridge}, continued} \\",
             r"\toprule", header, r"\midrule", r"\endhead",
             r"\midrule \multicolumn{7}{r}{\itshape continued on the next page} \\",
             r"\endfoot", r"\bottomrule", r"\endlastfoot"]
    for r in rs:
        key = r["claim_class"]
        label = short.get(r["label"], r["label"])
        coef = adopted.get(key)
        cover = coverage.get(key)
        coef_cell = f"{coef:.4f}" if coef is not None else f"{float(r['coefficient']):.4f}"
        cover_cell = f"{cover:.4f}" if cover is not None else "same"
        cell = plain(r["proxy_assumption"])
        alt = plain(r["alternative_estimate"])
        if alt and "adopted here" not in alt:
            cell = cell + ". " + alt[0].upper() + alt[1:] if cell else alt
        lines.append(" & ".join([label, r["numerator"], r["denominator"], r["source"],
                                 coef_cell, cover_cell, cell]) + r" \\")
    lines.append(r"\end{longtable}")
    write("tab_bridge.tex", "\n".join(lines))


if __name__ == "__main__":
    tab_classes()
    tab_sensitivity()
    tab_series()
    tab_holders()
    tab_structural()
    tab_quintile()
    tab_under_reporting()
    tab_tau_k()
    tab_levers()
    tab_incidence_holder()
    tab_federal_share_by_dose()
    tab_buffers()
    tab_attrition()
    tab_institutions_by_model()
    tab_relief()
    tab_payoff()
    tab_tiers()
    tab_instruments()
    tab_removed()
    tab_bridge()
