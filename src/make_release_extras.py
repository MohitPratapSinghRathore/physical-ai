"""Copy the processed artifacts the manuscript cites into data/release/.

The manuscript's macros are generated from data/release/ only, so any measured
artifact a section reports has to be part of the released replication package.
This script derives those files from the pipeline outputs in data/processed/ and
framework/ and writes them under data/release/. It never computes anything new.

Run:  python src/make_release_extras.py
"""
import csv
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
REL = ROOT / "data" / "release"


def load(rel):
    return json.loads((ROOT / rel).read_text())


def rows(rel):
    with (ROOT / rel).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_rows(rel, fieldnames, records):
    out = REL / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(records)
    print("wrote", out.relative_to(ROOT))


def federal_share_by_dose():
    d = load("data/processed/item4_federal_share_summary.json")
    inside = {str(x) for x in d["inside_data_doses"]}
    recs = []
    for dose in sorted(d["by_dose_narrow"], key=float):
        n, c = d["by_dose_narrow"][dose], d["by_dose_conservatorship"][dose]
        recs.append({"dose_share_of_total_wage_bill": dose,
                     "narrow_low": n[0], "narrow_high": n[1],
                     "conservatorship_low": c[0], "conservatorship_high": c[1],
                     "inside_observed_data_range": str(dose in inside
                                                       or float(dose) in d["inside_data_doses"])})
    write_rows("incidence/federal_share_by_dose.csv",
               ["dose_share_of_total_wage_bill", "narrow_low", "narrow_high",
                "conservatorship_low", "conservatorship_high",
                "inside_observed_data_range"], recs)


def housing_agencies():
    book = rows("data/processed/gse_book_structure.csv")
    unenhanced = {r["enterprise"]: float(r["share_of_book"])
                  for r in book if r["loan_class"] == "none"}
    wf = rows("data/processed/gse_waterfall_rebuilt.csv")
    recs = []
    for r in wf:
        recs.append({
            "dose_share_of_total_wage_bill": r["dose"],
            "end": r["end"],
            "weighting": r["weighting"],
            "inside_observed_data_range": r["inside_observed_data_range"],
            "agency_loss_bn": r["agency_loss_bn"],
            "transferred_to_private_cover_bn": r["transferred_bn"],
            "private_cover_share_of_loss": round(float(r["transferred_bn"])
                                                 / float(r["agency_loss_bn"]), 6),
            "retained_bn": r["retained_bn"],
            "capital_bn": r["capital_bn"],
            "treasury_draw_bn": r["federal_beyond_bn"],
        })
    write_rows("incidence/housing_agency_waterfall.csv", list(recs[0]), recs)
    write_rows("incidence/housing_agency_unenhanced_share.csv",
               ["enterprise", "unenhanced_share_of_single_family_book"],
               [{"enterprise": k, "unenhanced_share_of_single_family_book": v}
                for k, v in unenhanced.items()])


def pay_control():
    src = rows("data/processed/pay_control.csv")
    write_rows("incidence/pay_control.csv", list(src[0]), src)


def buffers():
    src = rows("data/processed/incidence_balance_sheets.csv")
    write_rows("incidence/household_balance_sheets.csv", list(src[0]), src)


def institutions():
    for name in ("a2_summary.json", "a2_system_results.csv",
                 "a2_distribution_by_class.csv", "a4_instrument_results.csv",
                 "a4_instrument_results.json", "a3_omitted_institutions.json",
                 "fdic_summary.json", "ncua_summary.json"):
        src = ROOT / "framework" / "institutions" / name
        if src.exists():
            dst = REL / "institutions" / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print("wrote", dst.relative_to(ROOT))


def ai_bust():
    for name in ("b1_tiers.json", "b1_verdict_curve.csv", "b2_transmission.json",
                 "b2_transmission.csv", "b3_b4_summary.json",
                 "b3_bust_through_engine.csv", "b4_payoff_by_holder.csv"):
        src = ROOT / "framework" / "ai_bust" / name
        if src.exists():
            dst = REL / "ai_bust" / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print("wrote", dst.relative_to(ROOT))


def tau_k():
    for name in ("tau_k_assembled.json", "components.json", "published_shares.json",
                 "tau_k_crs_theta_sensitivity.csv", "z1_bond_holders.json"):
        src = ROOT / "framework" / "tau_k" / name
        if src.exists():
            dst = REL / "tau_k" / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print("wrote", dst.relative_to(ROOT))


def labor_backing():
    for name in ("direct_ratio_latest.json", "direct_ratio_timeseries.csv",
                 "debt_only_ratio.json", "debt_only_ratio_timeseries.csv",
                 "debt_only_sensitivity.csv", "sensitivity.json",
                 "item3_sovereign_robustness.json", "item3_sovereign_robustness.csv",
                 "quintile_labour_backing.csv", "two_sided_bet.json",
                 "capital_gains_bound.json"):
        src = ROOT / "framework" / "labor_backing" / name
        if src.exists():
            dst = REL / "labor_backing" / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print("wrote", dst.relative_to(ROOT))


def method():
    for name in ("replication_r_sensitivity.json", "fiscal_channel_summary.json",
                 "benchmark_cap_summary.json", "incidence_summary.json",
                 "pay_control_summary.json", "item4_federal_share_summary.json",
                 "gse_waterfall_summary.json", "verify/plausibility_audit.json"):
        src = ROOT / "data" / "processed" / name
        if src.exists():
            dst = REL / "method" / pathlib.Path(name).name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print("wrote", dst.relative_to(ROOT))


def revision_r1():
    for name in ("a1_pass_through.json", "a1_required_by_g.csv", "a1_g_cases.csv",
                 "a2_cashflow_bridge.json", "a2_transition_path.csv",
                 "a3_relief_feedback.json", "a3_relief_feedback.csv", "a3_by_class.csv",
                 "a4_two_directions.json", "a4_rate_grid.csv"):
        src = ROOT / "framework" / "revision_r1" / name
        if src.exists():
            dst = REL / "revision_r1" / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print("wrote", dst.relative_to(ROOT))


if __name__ == "__main__":
    federal_share_by_dose()
    housing_agencies()
    pay_control()
    buffers()
    institutions()
    ai_bust()
    tau_k()
    labor_backing()
    method()
    revision_r1()
