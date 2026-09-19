"""Leg A Tier 2: AI-linked capex and its funding source, from SEC XBRL filings.

Tiered definition (PROJECT_BRIEF.md WS1, extended by decision D4):
  Tier 1  debt issued explicitly against AI assets (GPU-backed, data-centre ABS/CMBS)
  Tier 2  capex of hyperscalers, neoclouds, data-centre REITs and robotics firms from
          filings, split by funding source where disclosed          <- THIS MODULE
  Tier 2b off-balance-sheet and SPV-financed data-centre debt (BIS, private credit)
  Tier 3  valuation exposure (sensitivity only, never in the headline ratio)

This module produces a LOWER BOUND on Leg A, not a measure of it. BIS Quarterly Review
March 2026 documents that data-centre debt is commonly placed in dedicated vehicles with
the operator holding minority equity plus a long-term lease, deliberately outside the
operator's consolidated balance sheet. Filings measure the balance sheet the structure was
designed to keep clean. See notes/findings.md A2 and notes/decisions.md D4.

Self-funding ratio = operating cash flow / capex. Above 1 means capex is covered by
internal funds and the firm is not adding credit exposure at the margin; below 1 means the
gap is being financed. This ratio is the point of the table: it is what determines whether
Leg A is a credit event or an equity event.
"""
import json, pathlib, sys
import pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sources import SEC_COMPANIES, SEC_TAGS

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw" / "sec", ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

FLOW = {"capex", "ocf", "debt_issued"}      # duration facts
STOCK = {"lt_debt", "fin_lease", "ppe_net"} # instant facts


MIN_FY_END = "2024-01-01"   # reject stale facts: a filer that stopped using a tag


def annual(tic, key):
    """Latest full fiscal-year value across all candidate tags for one concept.

    Returns (value, fy_end, tag). Picks the candidate tag with the most recent fiscal
    year end, which is what prevents a filer's abandoned tag (Amazon's
    PaymentsToAcquirePropertyPlantAndEquipment, last used 2016) from being read as current.
    """
    best = None
    for tag in SEC_TAGS[key]:
        f = RAW / f"{tic}_{key}__{tag}.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text())
        units = d.get("units", {})
        rows = units.get("USD") or next(iter(units.values()), [])
        for r in rows:
            if r.get("form") != "10-K" or r.get("fp") != "FY":
                continue
            if key in FLOW:
                if not r.get("start") or not r.get("end"):
                    continue
                days = (pd.Timestamp(r["end"]) - pd.Timestamp(r["start"])).days
                if not 330 <= days <= 400:
                    continue
            if best is None or r["end"] > best[1]:
                best = (r["val"], r["end"], tag)
    if best is None or best[1] < MIN_FY_END:
        return None, None, None
    return best


def main():
    rows = []
    for tic, (cik, name, cls) in SEC_COMPANIES.items():
        rec = {"ticker": tic, "company": name, "class": cls, "cik": cik}
        for key in SEC_TAGS:
            v, end, tag = annual(tic, key)
            rec[key] = None if v is None else v / 1e9   # USD bn
            rec[f"{key}_tag"] = tag
            if key == "capex":
                rec["fy_end"] = end
        rows.append(rec)
    t = pd.DataFrame(rows)

    t["self_funding_ratio"] = t["ocf"] / t["capex"]
    t["capex_less_ocf"] = t["capex"] - t["ocf"]
    t["debt_plus_leases"] = t[["lt_debt", "fin_lease"]].sum(axis=1, min_count=1)

    cols = ["ticker", "company", "class", "fy_end", "capex", "ocf", "self_funding_ratio",
            "capex_less_ocf", "debt_issued", "lt_debt", "fin_lease", "debt_plus_leases",
            "ppe_net"]
    t = t[cols + [c for c in t.columns if c.endswith("_tag")]].sort_values(
        "capex", ascending=False)
    t.round(3).to_csv(OUT / "legA_tier2.csv", index=False)
    stale = t[t["capex"].isna()]["ticker"].tolist()
    if stale:
        print(f"  no current capex fact (dropped, fy_end before {MIN_FY_END}): {stale}")

    tot = {
        "n_companies": int(len(t)),
        "n_with_capex": int(t["capex"].notna().sum()),
        "min_fy_end": MIN_FY_END,
        "total_capex_usd_bn": float(t["capex"].sum()),
        "total_ocf_usd_bn": float(t["ocf"].sum()),
        "aggregate_self_funding_ratio": float(t["ocf"].sum() / t["capex"].sum()),
        "total_capex_less_ocf_usd_bn": float(t["capex"].sum() - t["ocf"].sum()),
        "total_lt_debt_usd_bn": float(t["lt_debt"].sum()),
        "total_finance_leases_usd_bn": float(t["fin_lease"].sum()),
        "note": ("LOWER BOUND. Excludes off-balance-sheet and SPV-financed data-centre "
                 "debt (Tier 2b), which BIS QR March 2026 documents as the dominant "
                 "structure. Capex is total company capex, not AI-attributable capex: "
                 "no filing discloses an AI split, so this OVERSTATES the AI share of "
                 "capex while UNDERSTATING AI-linked debt."),
    }
    (OUT / "legA_tier2_summary.json").write_text(json.dumps(tot, indent=2))

    pd.set_option("display.width", 220)
    print("\n=== Leg A Tier 2: latest FY from 10-K filings (USD bn) ===")
    print(t.round(2).to_string(index=False, max_colwidth=26))
    print()
    for k, v in tot.items():
        if k != "note":
            print(f"  {k:36s} {round(v, 3) if isinstance(v, float) else v}")
    print(f"\n  NOTE: {tot['note']}")


if __name__ == "__main__":
    main()
