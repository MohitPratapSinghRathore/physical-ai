"""B8. Re-express the repository's existing results as labour backing times displacement.

PROVISIONAL. Writes only inside framework/labor_backing/. Reads, and never modifies,
data/processed/.

THE PROPOSED IDENTITY

    exposure of claim class c  =  stock_c  x  LB_c  x  w  x  (1 - R)

where LB_c is the class's DIRECT labour backing share (B1), w is the share of the TOTAL wage
bill displaced (the A74 axis), and R = rho x omega is the retained wage share, so that
w x (1 - R) is the share of the wage bill permanently lost after reemployment.

WHAT THE QUANTITY IS, stated before any comparison, because the two sides are not the same
object. The identity gives INCOME AT RISK BEHIND A CLAIM: the part of the claim stock whose
first-round servicing income has gone. The household engine gives EXPOSURE AT DEFAULT: the
balances of the households that actually default. The second is the first times a default
hit rate, so a level gap of roughly an order of magnitude is expected and is not a
disagreement. What CAN be compared is the ordering across classes, the response to w, and
the fiscal cell, where both sides are revenue flows and the comparison is like for like.

POST-CORRECTION INPUTS ONLY. Fiscal magnitudes come from A77 (fiscal_extended_axis), credit
from A76 (verify/hand_check_credit), the axis from A74 (scenario_axis). A70 and A75 are
withdrawn and are not read. A78's scope paragraph applies to every credit row here.
"""
import csv, json, pathlib

OUT = pathlib.Path(__file__).parent
PROC = OUT.parents[1] / "data" / "processed"


def rows(p):
    return list(csv.DictReader(open(p)))


def main():
    classes = {r["class"]: r for r in rows(OUT / "claim_classes.csv")}
    fp = json.loads((PROC / "fiscal_persistence_summary.json").read_text())
    receipts, comp = fp["federal_receipts_bn"], fp["compensation_bn"]
    wages = 13365.233          # NIPA wage and salary accruals, 2026 Q2, FRED WASCUR
    axis = json.loads((PROC / "scenario_axis_summary.json").read_text())

    # ---- R as a function of w, taken from the A77 run, headline configuration
    fx = [r for r in rows(PROC / "fiscal_extended_axis.csv")
          if r["rho_mode"] == "fitted" and r["horizon"] == "10"
          and r["tau_l"] == "bottom_up_0.301" and r["outlays"] == "no_outlays"
          and r["tau_k_reading"] == "barkai_rent_0.351"]
    for r in fx:
        r["w"] = float(r["share_of_total_wage_bill"])
    fx.sort(key=lambda r: r["w"])

    def at(w):
        """Nearest scenario row on the A77 grid, PREFERRING rows inside the observed labour
        market range. Outside-data rows carry rho extrapolated to zero, which would silently
        set 1 - R to one. When only an outside row is close, it is used and flagged."""
        inside = [r for r in fx if r["outside_data"] == "False" and abs(r["w"] - w) <= 0.03]
        pool = inside or fx
        r = min(pool, key=lambda x: abs(x["w"] - w))
        r["_outside_used"] = not inside
        return r

    credit = rows(PROC / "verify" / "hand_check_credit.csv")
    ws = sorted({float(r["share_of_wage_bill"]) for r in credit})

    # ---- class map: repository result -> labour backing cell
    MAP = {"mortgage": "home_mortgage", "auto": "cc_auto",
           "student": "cc_student", "card": "cc_revolving"}

    out = []
    print("B8. Re-expression against the household engine (A76), bank-universe balances\n")
    hdr = ("  w      class     LB     R      income-at-risk bn   engine EAD bn   ratio   "
           "engine implied uplift")
    print(hdr)
    for w in ws:
        f = at(w)
        R = float(f["R"])
        for r in credit:
            if abs(float(r["share_of_wage_bill"]) - w) > 1e-9:
                continue
            key = MAP[r["loan"]]
            lb = float(classes[key]["central"])
            bal = float(r["total_balance_bn"])            # balances of targeted holders
            iar = bal * lb * w * (1 - R)
            ead = float(r["exposure_at_default_bn"])
            out.append({"w": w, "result": "credit:" + r["loan"], "class": key,
                        "LB": lb, "R": R, "targeted_balance_bn": bal,
                        "income_at_risk_bn": iar, "engine_bn": ead,
                        "ratio_identity_over_engine": iar / ead if ead else None,
                        "engine_default_uplift_pp": float(r["mean_default_uplift_pp"])})
            print("  %-6.2f %-9s %.3f  %.3f  %14.1f   %13.1f   %5.2f   %6.4f"
                  % (w, r["loan"], lb, R, iar, ead, iar / ead, float(r["mean_default_uplift_pp"]) / 100))

    # ---- the fiscal cell, where both sides are revenue flows
    print("\nB8. Re-expression against the fiscal channel (A77), federal claim\n")
    print("  w     identity  engine net  ratio  engine gross  gross on wage base  identity/gross_wagebase")
    lb_fed = float(classes["federal"]["central"])
    for w in (0.05, 0.10, 0.25, 0.50, 0.75):
        f = at(w)
        R = float(f["R"])
        # identity: the labour-linked part of federal receipts falls with the lost wage bill
        ident = lb_fed * w * (1 - R)
        engine_net = float(f["terminal_pct_receipts"]) / 100.0
        # the engine's own gross labour-side loss, before the tau_k offset
        tau_l, tau_k = 0.301, 0.0708
        gross = tau_l * (1 - R) * w * comp / receipts
        gross_wagebase = tau_l * (1 - R) * w * wages / receipts
        out.append({"w": w, "result": "fiscal:federal", "class": "federal", "LB": lb_fed,
                    "R": R, "identity_pct_receipts": 100 * ident,
                    "engine_net_pct_receipts": 100 * engine_net,
                    "engine_gross_pct_receipts": 100 * gross,
                    "engine_gross_on_wage_base_pct_receipts": 100 * gross_wagebase,
                    "engine_w_used": f["w"]})
        print("  %-5.2f %8.2f %11.2f %6.2f %13.2f %19.2f %23.3f"
              % (w, 100 * ident, 100 * engine_net, ident / engine_net if engine_net else 0,
                 100 * gross, 100 * gross_wagebase,
                 ident / gross_wagebase if gross_wagebase else 0))

    # ---- the base-mismatch diagnostic
    diag = {
        "tau_l_bottom_up": 0.301,
        "base_the_rate_was_built_on": "wages and salary accruals, 13,365.2bn (A32 reproduces "
                                      "federal payroll 15.52 percent as 2,074.4 / 13,365.2 and "
                                      "federal income tax on wages 12.85 percent as "
                                      "2,571.4 x 0.6675 / 13,365.2)",
        "base_the_engine_applies_it_to": "compensation of employees, 16,224.3bn",
        "ratio": comp / wages,
        "effect": "If tau_l 0.301 and 0.318 are rates on wages and salaries, applying them to "
                  "compensation overstates the bottom-up fiscal loss by %.1f percent. The "
                  "AMR 0.255 rows are built differently and are not affected in the same way."
                  % (100 * (comp / wages - 1)),
        "status": "FLAGGED, not asserted as an error in the engine. It is a rate and base "
                  "pairing to check, and it moves the headline fiscal cell.",
    }
    print("\nBASE MISMATCH DIAGNOSTIC")
    print(json.dumps(diag, indent=2))

    # ---- rent, a class the engine has no row for
    lb_mf = float(classes["multifamily"]["central"])
    stock_mf = float(classes["multifamily"]["level_musd"]) / 1000.0
    rent_rows = []
    for w in (0.05, 0.10, 0.25, 0.50, 0.75):
        f = at(w)
        R = float(f["R"])
        rent_rows.append({"w": w, "result": "rent:multifamily", "class": "multifamily",
                          "LB": lb_mf, "R": R,
                          "income_at_risk_bn": stock_mf * lb_mf * w * (1 - R),
                          "engine_bn": None,
                          "note": "the engine has no multifamily or landlord row; A75 flagged "
                                  "the DSCR proxy as the weakest cell it had"})
    out += rent_rows
    print("\nB8. Rent and multifamily, a class with NO engine counterpart")
    for r in rent_rows:
        print("  w %.2f  income at risk behind multifamily debt %8.1f bn" % (r["w"], r["income_at_risk_bn"]))

    keys = sorted({k for r in out for k in r})
    with open(OUT / "connection_table.csv", "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=keys)
        wtr.writeheader()
        wtr.writerows(out)
    (OUT / "connection_diagnostics.json").write_text(json.dumps(
        {"status": "PROVISIONAL", "base_mismatch": diag,
         "axis_total_wage_bill_bn_ACS": axis["total_wage_bill_bn"],
         "nipa_compensation_bn": comp, "nipa_wages_bn": wages,
         "federal_receipts_bn": receipts,
         "inputs": ["A74 scenario_axis", "A76 verify/hand_check_credit",
                    "A77 fiscal_extended_axis", "A78 scope paragraph applies"]}, indent=2))


if __name__ == "__main__":
    main()
