"""B1, B3 and B4: the DIRECT (first-round) labour backing ratio.

PROVISIONAL throughout. Nothing here is a standing claim and nothing here has been
independently replicated. Produced in one session, so the same-session rule applies.

Writes, next to this file:
  claim_class_rules.csv        B1, one row per class: the rule, the share, the variants
  direct_ratio_latest.json     B3, overall and by class, latest complete year
  holder_matrix_latest.csv     B3, labour-backed claims by ULTIMATE holder
  direct_ratio_timeseries.csv  B4, annual, as far back as the inputs allow
  z1_extract.csv               provenance: every Z.1 series actually used
  plausibility_direct.csv      every bound, checked, violations first
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[1]
PROC = ROOT / "data" / "processed"
FRED = ROOT / "data" / "raw" / "fred"

import config as C
from z1_loader import load_all, annual, catalog

LATEST = None   # resolved from the data


# --------------------------------------------------------------------------- inputs
def fred_annual(sid, col=None):
    """Annual mean of a FRED csv already in data/raw/fred. Returns int year -> value."""
    d = pd.read_csv(FRED / f"{sid}.csv")
    d.columns = [c.strip() for c in d.columns]
    dc = d.columns[0]
    vc = col or d.columns[1]
    d[dc] = pd.to_datetime(d[dc])
    d[vc] = pd.to_numeric(d[vc], errors="coerce")
    return d.dropna(subset=[vc]).groupby(d[dc].dt.year)[vc].mean()


def receipts_shares():
    """Labour-linked share of federal and of state and local receipts, by year.

    FEDERAL  = [social insurance contributions + wage share of AGI x personal current
               taxes] / federal current receipts.
    S AND L  = [wage share of AGI x state and local personal current taxes]
               / state and local current tax receipts.
    The SOI wage share of AGI exists for 2021 to 2023 only. Earlier years hold it at the
    earliest observed value. THAT IS A DATA LIMIT, not a measurement, and it is flagged
    in the time series output as soi_wage_share_is_held_constant.
    """
    lt = json.loads((PROC / "labor_tax_share.json").read_text())
    soi = {int(y): v["wage_share_of_agi"] for y, v in lt["soi_detail"].items()}

    def wage_share(y):
        """NEAREST observed SOI year. The series exists for 2021 to 2023 only, so every
        year outside that window carries the closest one and is flagged as held."""
        if y in soi:
            return soi[y], False
        return soi[min(soi, key=lambda k: abs(k - y))], True

    fed_receipts = fred_annual("FGRECPT")                 # billions
    fed_personal = fred_annual("A074RC1Q027SBEA")         # billions
    fed_socins = fred_annual("W780RC1Q027SBEA")           # billions
    sl_tax = fred_annual("W070RC1Q027SBEA")               # billions
    sl_personal = fred_annual("W071RC1Q027SBEA")          # billions

    rows = {}
    years = sorted(set(fed_receipts.index) & set(fed_personal.index) & set(fed_socins.index))
    for y in years:
        w, held = wage_share(y)
        fed = (fed_socins[y] + w * fed_personal[y]) / fed_receipts[y]
        fed_ub = (fed_socins[y] + fed_personal[y]) / fed_receipts[y]
        sl = (w * sl_personal[y] / sl_tax[y]) if y in sl_tax.index and sl_tax[y] > 0 else np.nan
        sl_ub = (sl_personal[y] / sl_tax[y]) if y in sl_tax.index and sl_tax[y] > 0 else np.nan
        rows[y] = dict(federal_receipts_labour_share=fed,
                       federal_receipts_labour_share_upper=fed_ub,
                       state_local_receipts_labour_share=sl,
                       state_local_receipts_labour_share_upper=sl_ub,
                       soi_wage_share_of_agi=w,
                       soi_wage_share_is_held_constant=held)
    return pd.DataFrame(rows).T


def backing_table():
    """Central labour backing share per class, plus the named variants."""
    ur = pd.read_csv(PROC / "under_reporting_factors.csv").set_index("loan")
    s = {k: float(ur.loc[k, "working_core_share_of_full"])
         for k in ["mortgage", "card", "auto", "student"]}
    bal = {k: float(ur.loc[k, "sipp_FULL_universe_bn"]) for k in ["card", "auto", "student"]}
    blend = sum(s[k] * bal[k] for k in bal) / sum(bal.values())
    return {
        "acs_mortgage_service": (C.ACS_MORTGAGE_SERVICE_WORKING_CORE,
                                 {"sipp_balances": s["mortgage"], "acs_a38_definition": 0.80305}),
        "acs_rent": (C.ACS_RENT_WORKING_CORE, {"acs_a38_definition": 0.69913}),
        "sipp_card": (s["card"], {}),
        "sipp_auto": (s["auto"], {}),
        "sipp_student": (s["student"], {}),
        "sipp_consumer_blend": (blend, {}),
        "zero": (0.0, {"one_step_traced_to_demand": "see B2, never blended"}),
    }, s, blend


# --------------------------------------------------------------------------- holders
_SECTOR_CACHE = {}


def _sector_series(A, cat, instrument):
    """sector code -> annual asset series, for every sector Z.1 carries for this
    instrument FAMILY (the first five digits of the instrument code).

    Z.1 does not carry the same instrument suffix for every sector: bank Treasury
    holdings sit under a different suffix from insurer Treasury holdings, and the
    central bank uses another again. Matching on the exact suffix silently dumps whole
    holder classes into the residual, so the family is matched and the closest suffix
    within it is taken per sector.
    """
    key = instrument
    if key in _SECTOR_CACHE:
        return _SECTOR_CACHE[key]
    fam = instrument[:5]
    best = {}
    for code, desc in cat.items():
        if code[4:9] != fam:
            continue
        if "asset" not in desc.lower():
            continue
        sec = code[2:4]
        p = _pick(A, code)
        if not p:
            continue
        s = annual(A[p])
        if not len(s):
            continue
        # prefer the exact instrument suffix, then a market-value LM series, then any
        score = (code[4:] == instrument, code.startswith("LM"), len(s))
        if sec not in best or score > best[sec][0]:
            best[sec] = (score, s, code, desc)
    out = {k: (v[1], v[2], v[3]) for k, v in best.items()}
    _SECTOR_CACHE[key] = out
    return out


def holder_shares(A, cat, instrument, year):
    """Ultimate-holder shares of one instrument in one year, summing to exactly 1.

    An aggregate sector is used ONLY when Z.1 carries no component of it for this
    instrument, so nothing is double counted. Whatever the named holders do not cover
    against the all-sectors control total is residual_unallocated, which is a RESIDUAL
    and not a measurement.
    """
    sec = _sector_series(A, cat, instrument)
    present = {k for k, (s, _, _) in sec.items() if year in s.index}
    use = {}
    for k in present:
        if k in C.AGGREGATE_SECTORS:
            continue
        if k in C.SECTOR_FALLBACK:
            if any(c in present for c in C.SECTOR_FALLBACK[k]):
                continue                      # components available, skip the aggregate
            h = C.FALLBACK_HOLDER[k]
        elif k in C.HOLDER_OF_SECTOR:
            h = C.HOLDER_OF_SECTOR[k]
        else:
            continue
        use[k] = h
    agg = {h: 0.0 for h in C.HOLDER_CLASSES}
    for k, h in use.items():
        agg[h] += float(sec[k][0][year])
    tot_code = _pick(A, f"LM89{instrument}") or _pick(A, f"FL89{instrument}")
    control = np.nan
    if tot_code:
        ts = annual(A[tot_code])
        if year in ts.index:
            control = float(ts[year])
    allocated = sum(agg.values())
    if np.isnan(control) or control < allocated:
        control = allocated
    agg["residual_unallocated"] = max(control - allocated, 0.0)
    total = sum(agg.values())
    if total <= 0:
        return {h: np.nan for h in C.HOLDER_CLASSES}, control
    return {h: agg[h] / total for h in C.HOLDER_CLASSES}, control


def _pick(A, prefix):
    hits = [k for k in A if k.startswith(prefix)]
    if not hits:
        return None
    q = [h for h in hits if h.endswith(".Q")]
    return (q or hits)[0]


def series_of(A, code):
    p = _pick(A, code)
    return annual(A[p]) if p else pd.Series(dtype=float)


# --------------------------------------------------------------------------- build
def main():
    A = load_all()
    cat = catalog()
    back, sipp_s, blend = backing_table()
    rec = receipts_shares()

    used = []

    def lvl(codes, year=None):
        out = None
        for c in codes:
            s = series_of(A, c)
            used.append(c)
            out = s if out is None else out.add(s, fill_value=0.0)
        return out

    # class levels, millions of dollars, annual
    levels = {}
    for cl in C.CLASSES:
        levels[cl["key"]] = lvl(cl["liab"])
    L = pd.DataFrame(levels).dropna(how="all")
    years = [int(y) for y in L.index if not np.isnan(L.loc[y]).all()]
    complete = [y for y in years if L.loc[y].notna().all() and y in rec.index]
    latest = max(complete)

    # backing share by class and year
    def bshare(cl, y, variant=None):
        kind = cl["backing"]
        if kind == "federal_receipts":
            return float(rec.loc[y, "federal_receipts_labour_share_upper" if variant == "upper"
                                 else "federal_receipts_labour_share"])
        if kind == "state_local_receipts":
            return float(rec.loc[y, "state_local_receipts_labour_share_upper" if variant == "upper"
                                 else "state_local_receipts_labour_share"])
        central, vars_ = back[kind]
        if variant and variant in vars_ and isinstance(vars_[variant], float):
            return vars_[variant]
        return central

    # ---------------- B1 table
    rows = []
    for cl in C.CLASSES:
        central, vars_ = back.get(cl["backing"], (np.nan, {}))
        rows.append(dict(claim_class=cl["key"], label=cl["label"],
                         z1_liability_codes=" + ".join(cl["liab"]),
                         tracing_rule=cl["rule"],
                         labour_backing_share=round(bshare(cl, latest), 6),
                         variants="; ".join(f"{k}={v}" for k, v in vars_.items()) if vars_ else "",
                         level_bn=round(float(L.loc[latest, cl["key"]]) / 1000.0, 1),
                         year=latest))
    B1 = pd.DataFrame(rows)
    B1.to_csv(HERE / "claim_class_rules.csv", index=False)

    # ---------------- B3 holder matrix, latest year
    hrows = []
    student_fed = None
    sf = series_of(A, "FL313066220")
    if latest in sf.index:
        student_fed = float(sf[latest]) / float(L.loc[latest, "student_loan"])

    for cl in C.CLASSES:
        instr = C.CLASS_HOLDER_INSTRUMENT[cl["key"]]
        hs, control = holder_shares(A, cat, instr, latest)
        if cl["key"] == "student_loan" and student_fed is not None:
            # Z.1 carries the FEDERAL student holding directly. Everything else is
            # allocated pro rata across the non-federal consumer credit holders.
            rest = {k: v for k, v in hs.items() if k != "federal_government"}
            rs = sum(v for v in rest.values() if not np.isnan(v))
            hs = {k: (student_fed if k == "federal_government"
                      else (rest.get(k, 0.0) / rs) * (1 - student_fed) if rs > 0 else 0.0)
                  for k in C.HOLDER_CLASSES}
        elif instr == "3066000" and cl["key"] != "student_loan":
            # strip the federal student holding out of the generic consumer credit map
            rest = {k: v for k, v in hs.items() if k != "federal_government"}
            rs = sum(v for v in rest.values() if not np.isnan(v))
            hs = {k: (0.0 if k == "federal_government"
                      else (rest.get(k, 0.0) / rs) if rs > 0 else 0.0)
                  for k in C.HOLDER_CLASSES}
        lb = float(L.loc[latest, cl["key"]]) / 1000.0 * bshare(cl, latest)
        for h in C.HOLDER_CLASSES:
            hrows.append(dict(claim_class=cl["key"], holder=h,
                              obligor=C.OBLIGOR_OF_CLASS[cl["key"]],
                              holder_share=round(float(hs[h]), 6),
                              labour_backed_bn=round(lb * float(hs[h]), 2),
                              class_total_bn=round(float(L.loc[latest, cl["key"]]) / 1000.0, 1),
                              class_labour_backed_bn=round(lb, 2), year=latest))
    H = pd.DataFrame(hrows)
    H.to_csv(HERE / "holder_matrix_latest.csv", index=False)

    # ---------------- B4 time series
    trows = []
    for y in complete:
        tot = lb_tot = 0.0
        fed_lb = 0.0
        per = {}
        for cl in C.CLASSES:
            v = float(L.loc[y, cl["key"]]) / 1000.0
            b = bshare(cl, y)
            tot += v
            lb_tot += v * b
            per[cl["key"]] = v * b
        for cl in C.CLASSES:
            if per[cl["key"]] == 0:
                continue
            instr = C.CLASS_HOLDER_INSTRUMENT[cl["key"]]
            hs, _ = holder_shares(A, cat, instr, y)
            f = hs["federal_government"]
            if cl["key"] == "student_loan":
                s = series_of(A, "FL313066220")
                if y in s.index and L.loc[y, "student_loan"] > 0:
                    f = float(s[y]) / float(L.loc[y, "student_loan"])
            elif instr == "3066000":
                f = 0.0
            if not np.isnan(f):
                fed_lb += per[cl["key"]] * f
        # obligor leg: labour-backed claims the federal government OWES, less the part
        # it also holds, which is already in fed_lb
        fed_obl = sum(v for k, v in per.items()
                      if C.OBLIGOR_OF_CLASS[k] == "federal_government")
        hs_t, _ = holder_shares(A, cat, C.CLASS_HOLDER_INSTRUMENT["treasury"], y)
        overlap = per["treasury"] * (0.0 if np.isnan(hs_t["federal_government"])
                                     else hs_t["federal_government"])
        union = fed_lb + fed_obl - overlap
        trows.append(dict(year=y, total_claims_bn=round(tot, 1),
                          labour_backed_bn=round(lb_tot, 1),
                          direct_labour_backing_ratio=round(lb_tot / tot, 6),
                          federal_labour_backed_bn=round(fed_lb, 1),
                          sovereign_share_of_labour_backed=round(fed_lb / lb_tot, 6),
                          sovereign_obligor_bn=round(fed_obl, 1),
                          sovereign_union_bn=round(union, 1),
                          sovereign_share_union=round(union / lb_tot, 6),
                          household_debt_labour_backed_bn=round(
                              sum(per[k] for k in ["home_mortgage", "credit_card",
                                                   "auto_loan", "student_loan",
                                                   "other_consumer"]), 1),
                          federal_receipts_labour_share=round(
                              float(rec.loc[y, "federal_receipts_labour_share"]), 6),
                          soi_wage_share_is_held_constant=bool(
                              rec.loc[y, "soi_wage_share_is_held_constant"]),
                          household_debt_share_of_claims=round(
                              sum(float(L.loc[y, k]) for k in
                                  ["home_mortgage", "credit_card", "auto_loan",
                                   "student_loan", "other_consumer"]) / 1000.0 / tot, 6)))
    T = pd.DataFrame(trows).sort_values("year")
    T.to_csv(HERE / "direct_ratio_timeseries.csv", index=False)

    # ---------------- provenance
    prov = []
    for c in sorted(set(used)):
        s = series_of(A, c)
        prov.append(dict(z1_code=c, description=cat.get(c, "?"),
                         first_year=int(s.index.min()) if len(s) else None,
                         last_year=int(s.index.max()) if len(s) else None,
                         value_latest_mn=float(s.get(latest, np.nan))))
    pd.DataFrame(prov).to_csv(HERE / "z1_extract.csv", index=False)

    # ---------------- B3 summary
    latest_row = T[T.year == latest].iloc[0]
    by_class = {cl["key"]: dict(
        level_bn=round(float(L.loc[latest, cl["key"]]) / 1000.0, 1),
        backing=round(bshare(cl, latest), 6),
        labour_backed_bn=round(float(L.loc[latest, cl["key"]]) / 1000.0 * bshare(cl, latest), 1))
        for cl in C.CLASSES}
    hsum = H.groupby("holder")["labour_backed_bn"].sum()

    # SOVEREIGN EXPOSURE has two distinct legs and they must not be confused.
    #   holder or guarantor  a credit loss on a claim the federal government owns or
    #                        guarantees (GSE and Ginnie pools, FHA and VA, the federal
    #                        student book)
    #   obligor              a revenue shortfall on a claim the federal government owes
    #                        and services out of labour-linked receipts (Treasury)
    # The paper's 75.9 to 91.6 percent federal share of FIRST-ROUND LOSSES is the union
    # of the two, so the union is the quantity that compares with it.
    cls_lb = {cl["key"]: float(L.loc[latest, cl["key"]]) / 1000.0 * bshare(cl, latest)
              for cl in C.CLASSES}
    fed_holder = float(H[(H.holder == "federal_government")]["labour_backed_bn"].sum())
    fed_obligor = sum(v for k, v in cls_lb.items()
                      if C.OBLIGOR_OF_CLASS[k] == "federal_government")
    # a Treasury security the federal government also holds would be counted twice
    fed_both = float(H[(H.holder == "federal_government")
                       & (H.claim_class.isin([k for k in cls_lb
                                              if C.OBLIGOR_OF_CLASS[k]
                                              == "federal_government"]))]
                     ["labour_backed_bn"].sum())
    lb_total = float(latest_row.labour_backed_bn)
    sovereign = dict(
        labour_backed_held_or_guaranteed_bn=round(fed_holder, 1),
        labour_backed_obligor_bn=round(fed_obligor, 1),
        overlap_removed_bn=round(fed_both, 1),
        labour_backed_sovereign_exposure_bn=round(fed_holder + fed_obligor - fed_both, 1),
        share_held_or_guaranteed=round(fed_holder / lb_total, 6),
        share_obligor=round(fed_obligor / lb_total, 6),
        share_union=round((fed_holder + fed_obligor - fed_both) / lb_total, 6),
    )

    summary = dict(
        status="PROVISIONAL, produced in one session, not independently replicated",
        definition="FIRST-ROUND servicing only. Business-revenue-serviced classes are zero by rule.",
        latest_year=int(latest),
        total_claims_bn=float(latest_row.total_claims_bn),
        labour_backed_bn=float(latest_row.labour_backed_bn),
        direct_labour_backing_ratio=float(latest_row.direct_labour_backing_ratio),
        by_class=by_class,
        labour_backed_by_holder_bn={k: round(float(v), 1) for k, v in hsum.items()},
        labour_backed_by_holder_share={k: round(float(v) / float(hsum.sum()), 6)
                                       for k, v in hsum.items()},
        sovereign_share_of_labour_backed=float(latest_row.sovereign_share_of_labour_backed),
        sovereign_exposure=sovereign,
        social_insurance_memo=dict(
            note="MEMO ITEM, never inside the ratio. Payroll share of each fund's OWN total "
                 "income, 2026 Trustees summary Table 5.",
            payroll_share=C.SOCIAL_INSURANCE_PAYROLL_SHARE,
            oasdi_payroll_income_bn=1322.6, hi_payroll_income_bn=403.2,
            oasdi_reserves_bn=2561.3, hi_reserves_bn=255.7),
        sipp_working_core_shares=sipp_s,
        other_consumer_blend=blend,
    )
    (HERE / "direct_ratio_latest.json").write_text(json.dumps(summary, indent=1))

    # ---------------- plausibility, violations first
    checks = []

    def chk(name, ok, detail):
        checks.append(dict(check=name, verdict="OK" if ok else "VIOLATION", detail=detail))

    for cl in C.CLASSES:
        b = bshare(cl, latest)
        chk(f"backing share in [0,1]: {cl['key']}", 0.0 <= b <= 1.0, f"{b:.4f}")
        chk(f"labour-backed <= total: {cl['key']}", b <= 1.0,
            f"{by_class[cl['key']]['labour_backed_bn']} <= {by_class[cl['key']]['level_bn']}")
    for k, g in H.groupby("claim_class"):
        s = g["holder_share"].sum()
        chk(f"holder shares sum to 1: {k}", abs(s - 1.0) < 1e-5, f"{s:.8f}")
    r = float(latest_row.direct_labour_backing_ratio)
    chk("aggregate ratio in [0,1]", 0.0 <= r <= 1.0, f"{r:.4f}")
    nz = [v["backing"] for v in by_class.values()]
    chk("aggregate ratio between smallest and largest class share",
        min(nz) <= r <= max(nz), f"{min(nz):.4f} <= {r:.4f} <= {max(nz):.4f}")
    chk("sovereign share of labour-backed in [0,1]",
        0.0 <= float(latest_row.sovereign_share_of_labour_backed) <= 1.0,
        f"{latest_row.sovereign_share_of_labour_backed:.4f}")
    chk("time series is monotonic in year", T.year.is_monotonic_increasing,
        f"{T.year.min()} to {T.year.max()}")
    for nm in ["share_held_or_guaranteed", "share_obligor", "share_union"]:
        chk(f"sovereign {nm} in [0,1]", 0.0 <= sovereign[nm] <= 1.0, f"{sovereign[nm]:.4f}")
    chk("sovereign union >= each leg",
        sovereign["share_union"] >= max(sovereign["share_held_or_guaranteed"],
                                        sovereign["share_obligor"]) - 1e-9,
        f"{sovereign['share_union']:.4f}")
    P = pd.DataFrame(checks).sort_values("verdict")
    P.to_csv(HERE / "plausibility_direct.csv", index=False)

    v = (P.verdict == "VIOLATION").sum()
    print(f"latest complete year {latest}")
    print(f"  total claims        {latest_row.total_claims_bn:>12,.0f} bn")
    print(f"  labour backed       {latest_row.labour_backed_bn:>12,.0f} bn")
    print(f"  DIRECT RATIO        {r:>12.4f}")
    print(f"  sovereign share     {latest_row.sovereign_share_of_labour_backed:>12.4f}")
    print(f"  series {T.year.min()} to {T.year.max()}, {len(T)} years")
    print(f"  plausibility: {len(P)} checks, {v} violations")
    if v:
        print(P[P.verdict == "VIOLATION"].to_string(index=False))
    print("\n  by holder (labour-backed, bn):")
    for k, val in hsum.sort_values(ascending=False).items():
        print(f"    {k:26s} {val:>10,.0f}  {val/hsum.sum():>7.2%}")


if __name__ == "__main__":
    main()
