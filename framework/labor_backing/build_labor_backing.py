"""Labour backing ratio: definition pass computation (Part B, items B1 to B4).

PROVISIONAL throughout. Nothing this script produces is a standing claim. It writes only
inside framework/labor_backing/ and reads, but never modifies, data/processed/.

WHAT IT COMPUTES

  B1/B3  the DIRECT labour backing ratio for the United States, latest quarter: the share
         of the outstanding claim stock whose FIRST-ROUND servicing cash flow is labour
         income, by claim class and by holder class.
  B2     the INDIRECT extension, reported separately and never blended into the headline.
  B4     the same direct ratio annually from 1952, with a shift-share decomposition of its
         movement into claim-stock composition and the labour-linked share of receipts.

SOURCES

  Claim stocks and holders: Financial Accounts of the United States (Z.1), full CSV data
  file, https://www.federalreserve.gov/releases/z1/data/FRB_Z1_csv.zip. Every series carries
  its own published description, unit and unit multiplier in that file, so units are read
  and never asserted (decision D1).

  Receipts composition: NIPA via FRED, fetched with published metadata (decision D1).

  Household wage-backed shares: A43/A47 for mortgage service and gross rent (standing,
  claim 42), and sipp_wage_backed_shares.py in this directory for the consumer credit
  classes (PROVISIONAL, produced this session).

  Federal labour-linked receipts share: data/processed/labor_tax_share.json (A8, D15).

CACHE
  The 64MB Z.1 bundle is cached outside the repository. Pass --cache to place it elsewhere.
"""
import argparse, csv, io, json, os, pathlib, re, sys, tempfile, urllib.request, zipfile
from collections import defaultdict

OUT = pathlib.Path(__file__).parent
ROOT = OUT.parents[1]
PROC = ROOT / "data" / "processed"
Z1_URL = "https://www.federalreserve.gov/releases/z1/data/FRB_Z1_csv.zip"
UA = "physical-ai research (team@oviguide.in)"
FREDCSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
FREDMETA = "https://fred.stlouisfed.org/data/{}.txt"

# ----------------------------------------------------------------------------- Z.1 access

def z1_path(cache):
    cache.mkdir(parents=True, exist_ok=True)
    p = cache / "FRB_Z1_csv.zip"
    if not p.exists():
        req = urllib.request.Request(Z1_URL, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=900) as r, open(p, "wb") as fh:
            fh.write(r.read())
    return p


def load_z1(cache, wanted):
    """Return {series_code: {date: value}} and {series_code: meta} for wanted codes (.Q)."""
    want = {"Z1/Z1/%s.Q" % c for c in wanted}
    data = defaultdict(dict)
    meta = {}
    z = zipfile.ZipFile(z1_path(cache))
    with z.open("Z1.csv") as fh:
        r = csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8-sig", newline=""))
        for row in r:
            s = row["series_name"]
            if s not in want:
                continue
            v = row["value"]
            if v in ("", "ND", "NA"):
                continue
            code = s[6:-2]
            data[code][row["date"]] = float(v)
            if code not in meta:
                meta[code] = {"description": row["short_description"], "unit": row["unit"],
                              "unit_mult": row["unit_mult"], "frequency": row["frequency"]}
    return data, meta


# --------------------------------------------------------------------------- FRED access

def fred(series, cache):
    cache.mkdir(parents=True, exist_ok=True)
    out, meta = {}, {}
    for sid in series:
        p = cache / ("%s.csv" % sid)
        m = cache / ("%s.meta.json" % sid)
        if not p.exists():
            req = urllib.request.Request(FREDCSV.format(sid), headers={"User-Agent": UA})
            p.write_bytes(urllib.request.urlopen(req, timeout=120).read())
            req = urllib.request.Request(FREDMETA.format(sid), headers={"User-Agent": UA})
            h = urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "replace")
            def f(label):
                mm = re.search(r"%s</th>\s*<td>(.*?)</td>" % label, h, re.S)
                return re.sub(r"\s+", " ", mm.group(1)).strip() if mm else "?"
            t = re.search(r"<title>Table Data - (.*?) \| FRED", h, re.S)
            m.write_text(json.dumps({"title": re.sub(r"\s+", " ", t.group(1)).strip() if t else "?",
                                     "units": f("Units"), "freq": f("Frequency"),
                                     "source": f("Source"), "release": f("Release"),
                                     "last_updated": f("Last Updated"),
                                     "url": FREDCSV.format(sid)}, indent=2))
        rows = list(csv.reader(io.StringIO(p.read_text())))
        vals = {}
        for d, v in rows[1:]:
            if v not in ("", "."):
                vals[d] = float(v)
        out[sid] = vals
        meta[sid] = json.loads(m.read_text())
    return out, meta


def annual(series, how="last"):
    by = defaultdict(list)
    for d, v in sorted(series.items()):
        by[d[:4]].append(v)
    if how == "last":
        return {y: vs[-1] for y, vs in by.items()}
    return {y: sum(vs) / len(vs) for y, vs in by.items()}


# --------------------------------------------------------------------- the claim universe
# Ultimate-obligor universe. Look-through vehicles (agency pools, mutual funds, pension
# entitlements, insurance reserves) are NOT rows here: including them alongside the
# underlying obligations would count the same cash flow twice. They appear on the holder
# side instead, which is where B1's look-through rule bites.

CLASSES = [
    # key, label, z1 code(s) added, z1 code(s) subtracted, servicing cash flow
    ("home_mortgage", "Home mortgages, one to four family (households)",
     ["FL153165105"], [], "household income"),
    ("cc_auto", "Consumer credit, automobile loans", ["FL153166400"], [], "household income"),
    ("cc_student", "Consumer credit, student loans", ["FL153166220"], [], "household income"),
    ("cc_revolving", "Consumer credit, revolving", ["FL153166100"], [], "household income"),
    ("cc_other", "Consumer credit, other non-revolving", ["FL153166205"], [], "household income"),
    ("hh_other", "Other household and nonprofit debt (residual)",
     ["FL154104005"], ["FL153165105", "FL153166000"], "household income and nonprofit revenue"),
    ("multifamily", "Multifamily residential mortgages", ["FL893065405"], [], "rent"),
    ("cre_farm", "Commercial and farm mortgages", ["FL893065505", "FL893065603"], [], "business revenue"),
    ("business_other", "Other nonfinancial business debt (residual)",
     ["FL144104005"], ["FL143165405", "FL143165505"], "business revenue"),
    ("federal", "Federal government debt securities and loans", ["FL314104005"], [], "federal receipts"),
    ("state_local", "State and local government debt securities and loans",
     ["FL214104005"], [], "state and local receipts"),
]
EQUITY = ("equity", "Corporate equities, domestic issuers, market value", ["LM883164105"], [], "residual business cash flow")

# Holder-side instruments, for B3.
HOLDER_INSTR = [
    ("home_mortgage", "3065105"),
    ("multifamily", "3065405"),
    ("cre_farm", "3065505"),
    ("consumer_credit", "3066000"),
    ("federal", "3061105"),
    ("state_local", "3062005"),
    ("corp_bonds", "3063005"),
    ("agency_pools", "3061705"),
    ("equity", "3064105"),
    ("mutual_fund_shares", "3064205"),
]
HOLDER_SECTORS = {
    "households": ["15"],
    "banks": ["70"],
    "gses_and_pools": ["42"],
    "insurers": ["52"],
    "pensions": ["59", "34", "22"],
    "government": ["31", "21", "71"],
    "rest_of_world": ["26"],
    "nonfinancial_business": ["14"],
    "money_market_funds": ["63"],
    "other_investment_funds": ["69"],
    "other_financial": ["66", "67", "61", "64", "73", "50", "77"],
}
TOTAL_SECTORS = {"all": "89", "domestic_nonfinancial": "38", "domestic_financial": "79", "row": "26"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.environ.get(
        "LB_CACHE", str(pathlib.Path(tempfile.gettempdir()) / "physical_ai_lb_cache")))
    a = ap.parse_args()
    cache = pathlib.Path(a.cache)

    # ---------------------------------------------------------------- collect Z.1 series
    codes = set()
    for _, _, add, sub, _ in CLASSES + [EQUITY]:
        codes |= set(add) | set(sub)
    codes |= {"FL143165405", "FL143165505"}
    for _, instr in HOLDER_INSTR:
        for secs in list(HOLDER_SECTORS.values()) + [list(TOTAL_SECTORS.values())]:
            for s in secs:
                codes.add("FL%s%s" % (s, instr))
        codes.add("LM88" + instr)
    z, zmeta = load_z1(cache, codes)

    units = {c: m["unit_mult"] for c, m in zmeta.items()}
    bad = sorted({u for u in units.values()} - {"Millions"})
    if bad:
        raise SystemExit("unexpected Z.1 unit multipliers, units are read not asserted: %s" % bad)

    dates = sorted(set(z["FL153165105"]) & set(z["FL314104005"]))
    latest = dates[-1]

    def lvl(code, d):
        return z.get(code, {}).get(d)

    def class_level(add, sub, d):
        vals = [lvl(c, d) for c in add] + [lvl(c, d) for c in sub]
        if any(v is None for v in vals):
            return None
        return sum(lvl(c, d) for c in add) - sum(lvl(c, d) for c in sub)

    # -------------------------------------------------------------------- NIPA receipts
    fs = ["A074RC1Q027SBEA", "W780RC1Q027SBEA", "FGRECPT", "W070RC1Q027SBEA",
          "W071RC1Q027SBEA", "W072RC1Q027SBEA", "W074RC1Q027SBEA", "W076RC1Q027SBEA",
          "W077RC1Q027SBEA", "W782RC1Q027SBEA", "WASCUR", "PI", "PCEC", "GDP", "COE",
          "ASLSTAX"]
    f, fmeta = fred(fs, cache / "fred")
    A = {k: annual(v, "avg" if k != "ASLSTAX" else "last") for k, v in f.items()}

    soi = json.loads((PROC / "labor_tax_share.json").read_text())
    wage_share_agi = soi["wage_share_of_agi"]                      # 2023, A8/D15

    # Time-varying proxy for the wage share of AGI. SOI detail is 2021 to 2023 only, so the
    # frozen 2023 value understates early years, when wages were a larger share of taxable
    # income. The proxy rescales the NIPA wage share of personal income to hit the SOI value
    # in 2023 and is reported as a VARIANT, never as the headline.
    base_y = str(soi["soi_year_used"])
    wpi = {y: A["WASCUR"][y] / A["PI"][y] for y in A["WASCUR"] if A["PI"].get(y)}
    scale = wage_share_agi / wpi[base_y]
    wshare_tv = {y: min(1.0, v * scale) for y, v in wpi.items()}

    # federal labour-linked share of receipts, annually
    fed_share, sl_share = {}, {}
    for y in sorted(set(A["FGRECPT"]) & set(A["A074RC1Q027SBEA"]) & set(A["W780RC1Q027SBEA"])):
        rec, ptax, si = A["FGRECPT"][y], A["A074RC1Q027SBEA"][y], A["W780RC1Q027SBEA"][y]
        if not rec:
            continue
        # wage share of AGI is SOI 2021-23 only; before that it is held at the 2023 value and
        # that freeze is reported, not hidden. central_tv is the time-varying variant.
        fed_share[y] = {"lower": si / rec,
                        "central": (ptax * wage_share_agi + si) / rec,
                        "central_tv": (ptax * wshare_tv.get(y, wage_share_agi) + si) / rec,
                        "upper": (ptax + si) / rec}
    for y in sorted(set(A["W077RC1Q027SBEA"]) & set(A["W070RC1Q027SBEA"])):
        tax = A["W070RC1Q027SBEA"][y]
        ptax = A["W071RC1Q027SBEA"].get(y, 0.0)
        tpi = A["W072RC1Q027SBEA"].get(y, 0.0)
        assets = A["W074RC1Q027SBEA"].get(y, 0.0)
        frombus = A["W076RC1Q027SBEA"].get(y, 0.0)
        si_all = A["W782RC1Q027SBEA"].get(y)
        si_fed = A["W780RC1Q027SBEA"].get(y)
        si_sl = (si_all - si_fed) if (si_all is not None and si_fed is not None) else 0.0
        own = tax + si_sl + assets + frombus            # own-source: excludes federal grants
        if own <= 0:
            continue
        labour_income_tax = ptax * wage_share_agi
        sales = A["ASLSTAX"].get(y)
        if sales is None and A["ASLSTAX"]:            # carried forward as a SHARE of W072
            last = max(A["ASLSTAX"])
            if A["W072RC1Q027SBEA"].get(last):
                sales = tpi * (A["ASLSTAX"][last] / A["W072RC1Q027SBEA"][last])
        labshare_pi = (A["WASCUR"][y] / A["PI"][y]) if y in A["WASCUR"] and A["PI"].get(y) else None
        upper = (labour_income_tax + si_sl + (sales * labshare_pi if sales and labshare_pi else 0.0)) / own
        sl_share[y] = {"lower": labour_income_tax / own,
                       "central": (labour_income_tax + si_sl) / own,
                       "central_tv": (ptax * wshare_tv.get(y, wage_share_agi) + si_sl) / own,
                       "upper": upper,
                       "own_source_bn": own,
                       "sales_tax_bn": sales}

    # ---------------------------------------------- household wage-backed shares (B1 cells)
    sipp_csv = OUT / "sipp_wage_backed_shares.csv"
    sipp = {}
    if sipp_csv.exists():
        for row in csv.DictReader(open(sipp_csv)):
            sipp[row["class"]] = float(row["working_core_share_of_balance"])

    MORTGAGE_SERVICE_WORKING_CORE = 0.8402       # A43/A47, claim 42, standing
    RENT_WORKING_CORE = 0.7275                   # A43/A47, claim 42, standing

    y_latest = latest[:4]
    lab_pi = A["WASCUR"][y_latest] / A["PI"][y_latest]          # lower-variant scaler
    comp_gdi = A["COE"][y_latest] / A["GDP"][y_latest]
    pce_gdp = A["PCEC"][y_latest] / A["GDP"][y_latest]

    def band(central, kind):
        """lower/central/upper for a household cell. The rule value is the upper end: the
        one-sided band is a stated property of the direct definition, not an oversight."""
        return {"lower": central * lab_pi, "central": central, "upper": central}

    cells = {
        "home_mortgage": band(MORTGAGE_SERVICE_WORKING_CORE, "hh"),
        "cc_auto": band(sipp.get("vehicle", float("nan")), "hh"),
        "cc_student": band(sipp.get("student", float("nan")), "hh"),
        "cc_revolving": band(sipp.get("credit_card", float("nan")), "hh"),
        "cc_other": band(sipp.get("other_unsecured", float("nan")), "hh"),
        "hh_other": band(sipp.get("all_debt", float("nan")), "hh"),
        "multifamily": band(RENT_WORKING_CORE, "hh"),
        "cre_farm": {"lower": 0.0, "central": 0.0, "upper": 0.0},
        "business_other": {"lower": 0.0, "central": 0.0, "upper": 0.0},
        "equity": {"lower": 0.0, "central": 0.0, "upper": 0.0},
        "federal": fed_share[y_latest],
        "state_local": {k: sl_share[y_latest][k] for k in ("lower", "central", "upper")},
    }

    # --------------------------------------------------------------- B3: latest-quarter US
    rows = []
    for key, label, add, sub, flow in CLASSES + [EQUITY]:
        v = class_level(add, sub, latest)
        rows.append({"class": key, "label": label, "servicing_flow": flow,
                     "level_musd": v, "lower": cells[key]["lower"],
                     "central": cells[key]["central"], "upper": cells[key]["upper"]})

    debt_rows = [r for r in rows if r["class"] != "equity"]

    def ratio(rs, k):
        tot = sum(r["level_musd"] for r in rs)
        return sum(r["level_musd"] * r[k] for r in rs) / tot, tot

    headline = {}
    for name, rs in (("debt_only", debt_rows), ("debt_plus_equity", rows)):
        headline[name] = {}
        for k in ("lower", "central", "upper"):
            r, tot = ratio(rs, k)
            headline[name][k] = r
        headline[name]["total_musd"] = sum(x["level_musd"] for x in rs)
        headline[name]["labour_backed_musd"] = sum(
            x["level_musd"] * x["central"] for x in rs)

    # ------------------------------------------------------------------ B3: holder classes
    holder_rows = []
    instr_backing = {"home_mortgage": cells["home_mortgage"]["central"],
                     "multifamily": cells["multifamily"]["central"],
                     "cre_farm": 0.0,
                     "consumer_credit": sipp.get("all_debt", float("nan")),
                     "federal": cells["federal"]["central"],
                     "state_local": cells["state_local"]["central"],
                     "corp_bonds": 0.0,
                     "equity": 0.0,
                     # look-through cells, B1's rule for vehicles
                     "agency_pools": cells["home_mortgage"]["central"],
                     "mutual_fund_shares": None}
    instr_totals = {}
    for key, instr in HOLDER_INSTR:
        t = lvl("FL89" + instr, latest)
        if t is None:
            t = lvl("LM88" + instr, latest) or lvl("FL88" + instr, latest)
        instr_totals[key] = t
    # one-step look-through for mutual fund shares: the labour backing of the funds' own
    # portfolio, approximated by the fund sector's holdings of the instruments above.
    mf_assets = {k: lvl("FL65" + i, latest) or 0.0 for k, i in HOLDER_INSTR if k != "mutual_fund_shares"}
    mf_tot = sum(mf_assets.values())
    instr_backing["mutual_fund_shares"] = (
        sum(v * (instr_backing[k] or 0.0) for k, v in mf_assets.items()) / mf_tot if mf_tot else 0.0)

    for hname, secs in HOLDER_SECTORS.items():
        port, backed = 0.0, 0.0
        detail = {}
        for key, instr in HOLDER_INSTR:
            v = sum((lvl("FL%s%s" % (s, instr), latest) or 0.0) for s in secs)
            if hname == "households" and key in ("home_mortgage", "consumer_credit"):
                v = v            # households do hold small amounts; kept as reported
            detail[key] = v
            port += v
            backed += v * (instr_backing[key] or 0.0)
        holder_rows.append({"holder": hname, "portfolio_musd": port,
                            "labour_backed_musd": backed,
                            "labour_backing_share": backed / port if port else float("nan"),
                            **{"held_" + k: detail[k] for k, _ in HOLDER_INSTR}})

    # ------------------------------------------------------------------------ B4: 1952 on
    series_rows = []
    for d in dates:
        if not d.endswith("12-31"):
            continue
        y = d[:4]
        if int(y) < 1952:
            continue
        fs_y = fed_share.get(y)
        sl_y = sl_share.get(y)
        if fs_y is None or sl_y is None:
            continue
        lvls, ok = {}, True
        for key, label, add, sub, flow in CLASSES:
            v = class_level(add, sub, d)
            if v is None:
                ok = False
                break
            lvls[key] = v
        if not ok:
            continue
        eq = class_level(EQUITY[2], EQUITY[3], d)
        cell_y = dict(cells)
        cell_y["federal"] = fs_y
        cell_y["state_local"] = {k: sl_y[k] for k in ("lower", "central", "upper")}
        cell_tv = dict(cell_y)
        cell_tv["federal"] = {"central": fs_y["central_tv"]}
        cell_tv["state_local"] = {"central": sl_y["central_tv"]}
        tot = sum(lvls.values())
        row = {"date": d, "year": int(y), "total_debt_musd": tot, "equity_musd": eq}
        for k in ("lower", "central", "upper"):
            row["ratio_" + k] = sum(lvls[c] * cell_y[c][k] for c in lvls) / tot
        row["ratio_central_tv"] = sum(lvls[c] * cell_tv[c]["central"] for c in lvls) / tot
        row["ratio_central_with_equity"] = (
            sum(lvls[c] * cell_y[c]["central"] for c in lvls) / (tot + eq)) if eq else None
        # frozen-share counterfactual: receipts shares held at latest values, weights move
        row["ratio_frozen_shares"] = sum(lvls[c] * cells[c]["central"] for c in lvls) / tot
        # frozen-weights counterfactual: weights held at latest, receipts shares move
        latest_lvls = {c: [r for r in debt_rows if r["class"] == c][0]["level_musd"] for c in lvls}
        row["ratio_frozen_weights"] = sum(
            latest_lvls[c] * cell_y[c]["central"] for c in lvls) / sum(latest_lvls.values())
        for c in lvls:
            row["share_" + c] = lvls[c] / tot
        row["fed_labour_linked_share"] = fs_y["central"]
        row["sl_labour_linked_share"] = sl_y["central"]
        series_rows.append(row)

    # ------------------------------------------------------------------- B2: indirect ratio
    indirect = {
        "labour_share_of_personal_income_wages": lab_pi,
        "compensation_over_gdp": comp_gdi,
        "consumption_share_of_gdp": pce_gdp,
        "indirect_labour_funding_of_business_revenue_wages": lab_pi * pce_gdp,
        "indirect_labour_funding_of_business_revenue_compensation": comp_gdi * pce_gdp,
        "note": "B2. Reported as a SECOND ratio. Never blended into the headline.",
    }
    ind_central = indirect["indirect_labour_funding_of_business_revenue_compensation"]
    ext_rows = []
    for r in rows:
        add = ind_central if r["servicing_flow"] in ("business revenue", "residual business cash flow") else 0.0
        ext_rows.append({**r, "extended": min(1.0, r["central"] + add)})
    ext_debt = sum(r["level_musd"] * r["extended"] for r in ext_rows if r["class"] != "equity") / \
        sum(r["level_musd"] for r in ext_rows if r["class"] != "equity")
    ext_all = sum(r["level_musd"] * r["extended"] for r in ext_rows) / \
        sum(r["level_musd"] for r in ext_rows)
    indirect["extended_ratio_debt_only"] = ext_debt
    indirect["extended_ratio_debt_plus_equity"] = ext_all

    # ------------------------------------------------------------------- social insurance
    memo = {
        "note": "B1 memo item, deliberately NOT in the headline. A43 forbids folding the "
                "payroll-funded share of transfers into any total that also counts the "
                "fiscal channel, because the same payroll dollar would be counted twice.",
        "oasdi_payroll_share_of_trust_fund_income": 0.913,
        "oasdi_payroll_share_source": "A32, repository",
        "non_working_share_of_mortgage_service": 1 - MORTGAGE_SERVICE_WORKING_CORE,
        "non_working_share_of_rent": 1 - RENT_WORKING_CORE,
    }

    # ------------------------------------------------------------------------------ write
    with open(OUT / "claim_classes.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "holders.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(holder_rows[0]))
        w.writeheader()
        w.writerows(holder_rows)
    with open(OUT / "ratio_time_series.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(series_rows[0]))
        w.writeheader()
        w.writerows(series_rows)
    summary = {
        "status": "PROVISIONAL. Produced in the Part B definition pass. Not a standing claim.",
        "latest_quarter": latest,
        "headline_direct": headline,
        "indirect_B2": indirect,
        "social_insurance_memo": memo,
        "cells": cells,
        "instrument_backing_used_for_holders": instr_backing,
        "federal_labour_linked_share_latest": fed_share[y_latest],
        "state_local_labour_linked_share_latest": sl_share[y_latest],
        "sipp_shares_used": sipp,
        "series_first_year": series_rows[0]["year"] if series_rows else None,
        "z1_series_meta": zmeta,
        "fred_meta": fmeta,
    }
    (OUT / "labor_backing_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    print("latest quarter:", latest)
    print("\nB3 claim classes (levels in millions of dollars, units read from Z.1):")
    for r in rows:
        print("  %-16s %14.0f  lower %.3f central %.3f upper %.3f | %s"
              % (r["class"], r["level_musd"], r["lower"], r["central"], r["upper"], r["label"][:52]))
    print("\nHEADLINE direct ratio")
    for k, v in headline.items():
        print("  %-18s lower %.4f central %.4f upper %.4f  total %.0f musd"
              % (k, v["lower"], v["central"], v["upper"], v["total_musd"]))
    print("\nB2 indirect:", json.dumps(indirect, indent=2))
    print("\nB3 holders:")
    for r in sorted(holder_rows, key=lambda x: -x["portfolio_musd"]):
        print("  %-24s portfolio %12.0f  labour-backed share %.3f"
              % (r["holder"], r["portfolio_musd"], r["labour_backing_share"]))
    print("\nB4 series: %d years, %s to %s"
          % (len(series_rows), series_rows[0]["year"], series_rows[-1]["year"]))
    for r in series_rows[::10] + series_rows[-1:]:
        print("  %s central %.4f  tv %.4f  frozen-shares %.4f  frozen-weights %.4f  fed %.3f  s&l %.3f"
              % (r["year"], r["ratio_central"], r["ratio_central_tv"], r["ratio_frozen_shares"],
                 r["ratio_frozen_weights"], r["fed_labour_linked_share"], r["sl_labour_linked_share"]))


if __name__ == "__main__":
    main()
