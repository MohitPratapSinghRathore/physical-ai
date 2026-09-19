"""Amendment E: physical feasibility bounds on the EMBODIED displacement flow.

Cognitive displacement needs software deployment and is not capacity-constrained in any way
this project can measure, so no cap is applied to it. That is itself a statement and it is
made explicitly: **the fast scenarios in the frontier are cognitive-led by construction**,
because embodied displacement at the same speed would require building physical capital at
rates the capital stock cannot turn over.

Embodied displacement requires machines to exist. Three sourced bounds, from loosest to
tightest, all from public data.

BOUND 1: EQUIPMENT CAPITAL STOCK TURNOVER, the outer bound.
Annual private nonresidential EQUIPMENT investment divided by the net stock of private
nonresidential equipment. This is the fraction of the equipment stock that can be renewed in
a year if every dollar of equipment investment went to it. It is an absurd upper bound,
since equipment investment also replaces worn-out non-automating equipment, but it bounds
everything else.

BOUND 2: INFORMATION PROCESSING AND INDUSTRIAL EQUIPMENT SHARE.
Automation-relevant equipment is a subset. The share of equipment investment in the
categories that could plausibly embody automation capital bounds the flow more tightly.

BOUND 3: ACES ROBOTIC EQUIPMENT CAPITAL EXPENDITURE, the tightest and most direct.
The Annual Capital Expenditures Survey asks firms directly what they spent on robotic
equipment. That figure against the total wage bill of embodied-exposed workers gives the
closest thing to a measured current automation rate.

IFR World Robotics, the standard source for robot installations, is PAID and is recorded in
data/SOURCES.md as unavailable. Nothing here substitutes for it; these are bounds, not
estimates of robot deployment.

CONVERSION TO A DISPLACEMENT FLOW is the weak link and is stated. A dollar of automation
capital does not displace a fixed number of workers, and this project has no measured
capital-to-labour substitution ratio for AI. The conversion used is transparent and crude:
the annual automation capital spend divided by the capital cost of displacing one worker,
where the latter is taken as a multiple of the annual wage. The multiple is run over a grid
and the result is reported as a range across it, never as a point.
"""
import io, json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"

# capital cost of displacing one worker, as a multiple of that worker's annual wage
CAPEX_PER_WORKER_MULTIPLE = [1.0, 2.0, 3.0, 5.0]


def fred(series):
    p = RAW / "fred" / f"{series}.csv"
    if not p.exists():
        import requests
        r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}",
                         timeout=90)
        r.raise_for_status()
        p.write_bytes(r.content)
    d = pd.read_csv(p)
    d.columns = ["date", "value"]
    d["date"] = pd.to_datetime(d["date"])
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    return d.dropna().set_index("date")["value"]


def aces_robotics():
    """Robotic equipment capital expenditure from ACES 2022 table 1a or 1b, if present."""
    import openpyxl
    for fn in ["aces2022_table1b.xlsx", "aces2022_table1a.xlsx"]:
        p = RAW / "robots" / fn
        if not p.exists():
            continue
        wb = openpyxl.load_workbook(p, data_only=True)
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                cells = [str(c) for c in row if c is not None]
                joined = " ".join(cells).lower()
                if "robot" in joined:
                    nums = [c for c in row if isinstance(c, (int, float))]
                    if nums:
                        return {"file": fn, "sheet": ws.title,
                                "label": cells[0] if cells else "",
                                "values": nums[:6]}
    return None


def main():
    res = {}
    # ---- Bound 1 and 2: equipment investment against equipment stock ----
    try:
        inv = fred("Y033RC1Q027SBEA")      # private nonresidential equipment investment
        res["equipment_investment_bn"] = float(inv.iloc[-1])
        res["equipment_investment_date"] = str(inv.index[-1].date())
    except Exception as e:
        res["equipment_investment_error"] = f"{type(e).__name__}"
    try:
        # UNITS AND COVERAGE CHECKED AT THE PROVIDER, per decision D1. This series is
        # "Current-Cost Net Stock of Fixed Assets: Private: Nonresidential", in MILLIONS of
        # dollars, and covers structures and intellectual property as well as equipment. It
        # is therefore NOT an equipment stock and is recorded for context only. No bound in
        # this file divides by it.
        stock = fred("K1NTOTL1ES000")
        res["all_nonresidential_fixed_assets_bn"] = float(stock.iloc[-1]) / 1000.0
        res["equipment_net_stock_date"] = str(stock.index[-1].date())
    except Exception as e:
        res["equipment_net_stock_error"] = f"{type(e).__name__}"

    if "equipment_investment_bn" in res and "all_nonresidential_fixed_assets_bn" in res:
        res["equipment_investment_over_all_fixed_assets"] = (
            res["equipment_investment_bn"] / res["all_nonresidential_fixed_assets_bn"])

    # ---- Bound 3: ACES robotics ----
    res["aces_robotics"] = aces_robotics()

    # ---- embodied wage bill, from the repo ----
    import sys
    sys.path.insert(0, str(ROOT))
    from src.stress import scenarios as SC
    B = SC.occupation_scores()
    _, groups = SC._h3().build_groups()
    emb = B[B["occp"].isin(groups["embodied"])]
    emp_emb = float(emb["employment"].sum())
    res["embodied_employment"] = emp_emb
    res["embodied_share_of_employment"] = emp_emb / float(B["employment"].sum())

    # mean wage of embodied workers, from the DAR tables if present
    try:
        dar = pd.read_csv(OUT / "dar_us.csv")
        res["dar_columns"] = list(dar.columns)[:8]
    except Exception:
        pass
    # fall back to the national average wage from FRED
    try:
        comp = fred("COE")            # compensation of employees, USD bn
        payems = fred("PAYEMS")       # total nonfarm payrolls, thousands
        avg_wage = (comp.iloc[-1] * 1e9) / (payems.iloc[-1] * 1e3)
        res["average_compensation_per_worker"] = float(avg_wage)
    except Exception as e:
        res["avg_wage_error"] = f"{type(e).__name__}"

    rows = []
    if "average_compensation_per_worker" in res:
        aw = res["average_compensation_per_worker"]
        inv_usd = res["equipment_investment_bn"] * 1e9
        for m in CAPEX_PER_WORKER_MULTIPLE:
            cost = m * aw
            # if the ENTIRE equipment investment went to displacing embodied workers
            workers = inv_usd / cost
            rows.append({"bound": "1_all_equipment_investment",
                         "capex_multiple_of_annual_wage": m,
                         "workers_displaceable_per_year": workers,
                         "as_share_of_embodied_employment": workers / emp_emb,
                         "as_share_of_total_employment":
                             workers / float(B["employment"].sum())})
        # BOUND 2: only a SHARE of equipment investment is automation capital. No measured
        # share exists in this repository, so it is run over a grid and labelled a scenario.
        for m in CAPEX_PER_WORKER_MULTIPLE:
            for share in (0.05, 0.10, 0.20):
                workers = (inv_usd * share) / (m * aw)
                rows.append({"bound": f"2_automation_share_{share:.2f}",
                             "capex_multiple_of_annual_wage": m,
                             "workers_displaceable_per_year": workers,
                             "as_share_of_embodied_employment": workers / emp_emb,
                             "as_share_of_total_employment":
                                 workers / float(B["employment"].sum())})
    F = pd.DataFrame(rows)
    if len(F):
        F.round(6).to_csv(OUT / "feasibility_bounds.csv", index=False)
    (OUT / "feasibility_bounds.json").write_text(json.dumps(res, indent=2, default=str))

    pd.set_option("display.width", 240)
    print("=== inputs ===")
    for k, v in res.items():
        if k != "aces_robotics":
            print(f"  {k}: {v}")
    print(f"  aces_robotics: {res.get('aces_robotics')}")

    if len(F):
        print("\n=== BOUND 1: if EVERY dollar of equipment investment displaced embodied "
              "workers ===")
        print(F.assign(
            workers_m=lambda x: x.workers_displaceable_per_year / 1e6,
            pct_embodied=lambda x: x.as_share_of_embodied_employment * 100,
            pct_total=lambda x: x.as_share_of_total_employment * 100
        )[["capex_multiple_of_annual_wage", "workers_m", "pct_embodied",
           "pct_total"]].round(3).to_string(index=False))
        print("\n  The last column is the implied MAXIMUM annual embodied displacement flow "
              "as a\n  share of total employment. It is an absurd upper bound because all "
              "equipment\n  investment also replaces ordinary worn-out capital.")


if __name__ == "__main__":
    main()
