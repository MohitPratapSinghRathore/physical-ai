"""MODULE A1. Institution-level balance sheets for every US insured bank.

MEASURED, not scenario. Source: FDIC BankFind Suite public API,
https://banks.data.fdic.gov/api/financials, report date 2026-06-30, which is the same
vintage as the NY Fed Household Debt and Credit data this project already uses.

Every field below is an FDIC Research Information System item pulled directly. Nothing is
derived here except the two coverage checks at the end.

FIELD MAP, and the one gap it has:
    ASSET     total assets
    RBCT1J    tier 1 (core) capital, leverage definition
    RBCT1CER  tier 1 risk-based capital ratio, percent
    EQ        total equity capital
    LNRERES   real estate loans secured by 1-4 family residential properties
    LNREMULT  real estate loans secured by multifamily residential properties
    LNRENRES  real estate loans secured by nonfarm nonresidential properties
    LNRECONS  construction and land development
    LNREAG    loans secured by farmland
    LNCI      commercial and industrial loans
    LNCRCD    credit card loans
    LNAUTO    automobile loans
    LNCONOTH  other consumer loans
    LNLSNET   total loans and leases, net
    LNATRES   allowance for credit losses
    NETINC    net income, year to date
    ITAXR     applicable income taxes

    GAP, STATED: the API does not expose the revolving open-end (home equity) split of
    1-4 family residential, so LNRERES is first-lien AND home equity combined. The
    instruction asks for them separately and we cannot separate them from this source.
    Consequence: the residential category is treated as one book and the home equity
    share of it is unknown. Recorded as a limitation, not silently merged.
"""
import json
import time
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).parent
UA = {"User-Agent": "physical-ai research team@oviguide.in"}
BASE = "https://banks.data.fdic.gov/api"
REPDTE = "20260630"

FIELDS = ["CERT", "ASSET", "RBCT1J", "RBCT1CER", "EQ", "LNRERES", "LNREMULT", "LNRENRES",
          "LNRECONS", "LNREAG", "LNCI", "LNCRCD", "LNAUTO", "LNCONOTH", "LNLSNET",
          "LNATRES", "DEP", "NETINC", "ITAXR"]


def page(endpoint, params, total_key="total"):
    out, offset = [], 0
    while True:
        p = dict(params)
        p.update({"limit": 10000, "offset": offset, "format": "json"})
        r = requests.get(f"{BASE}/{endpoint}", params=p, headers=UA, timeout=180)
        r.raise_for_status()
        j = r.json()
        rows = [d["data"] for d in j.get("data", [])]
        out.extend(rows)
        total = j["meta"][total_key]
        offset += len(rows)
        if not rows or offset >= total:
            return out, total
        time.sleep(0.3)


def main():
    HERE.mkdir(parents=True, exist_ok=True)

    fin, n_fin = page("financials", {"filters": f"REPDTE:{REPDTE}",
                                     "fields": ",".join(FIELDS)})
    F = pd.DataFrame(fin)
    inst, n_inst = page("institutions", {"filters": "ACTIVE:1",
                                         "fields": "CERT,NAME,STNAME,BKCLASS,SPECGRP,SPECGRPN"})
    I = pd.DataFrame(inst)

    D = F.merge(I.drop(columns=[c for c in ["ID"] if c in I.columns]),
                on="CERT", how="left")
    num = [c for c in FIELDS if c != "CERT"]
    for c in num:
        D[c] = pd.to_numeric(D[c], errors="coerce").fillna(0.0)

    # ---- size class, on total assets in thousands as FDIC reports them
    def size_class(a):
        if a >= 700_000_000:
            return "largest (over 700bn)"
        if a >= 100_000_000:
            return "large (100 to 700bn)"
        if a >= 10_000_000:
            return "regional (10 to 100bn)"
        if a >= 1_000_000:
            return "midsize (1 to 10bn)"
        return "community (under 1bn)"
    D["size_class"] = D["ASSET"].map(size_class)

    # ---- business model, from concentration of the loan book. Thresholds are stated
    # choices, not estimates: a book is "heavy" in a category when that category is at
    # least the stated share of net loans and leases.
    L = D["LNLSNET"].replace(0, pd.NA)
    D["sh_card"] = (D.LNCRCD / L).fillna(0)
    D["sh_auto"] = (D.LNAUTO / L).fillna(0)
    D["sh_cre"] = ((D.LNRENRES + D.LNRECONS) / L).fillna(0)
    D["sh_res"] = (D.LNRERES / L).fillna(0)
    D["sh_ci"] = (D.LNCI / L).fillna(0)
    D["sh_multi"] = (D.LNREMULT / L).fillna(0)

    def model(r):
        if r.sh_card >= 0.25:
            return "card-heavy"
        if r.sh_auto >= 0.25:
            return "auto-heavy"
        if r.sh_cre >= 0.50:
            return "commercial real estate heavy"
        if r.sh_res >= 0.50:
            return "mortgage portfolio lender"
        if r.sh_ci >= 0.40:
            return "C and I heavy"
        return "diversified"
    D["business_model"] = D.apply(model, axis=1)

    D.to_csv(HERE / "fdic_institutions_20260630.csv", index=False)

    cats = ["LNRERES", "LNREMULT", "LNRENRES", "LNRECONS", "LNREAG", "LNCI", "LNCRCD",
            "LNAUTO", "LNCONOTH"]
    tot = {c: float(D[c].sum()) / 1e6 for c in cats}          # thousands to bn
    summ = {
        "source": "FDIC BankFind Suite public API, banks.data.fdic.gov/api/financials",
        "report_date": REPDTE,
        "retrieved": time.strftime("%Y-%m-%d"),
        "n_institutions_financials": int(n_fin),
        "n_institutions_matched": int(D.NAME.notna().sum()),
        "total_assets_bn": round(float(D.ASSET.sum()) / 1e6, 1),
        "total_tier1_bn": round(float(D.RBCT1J.sum()) / 1e6, 1),
        "total_net_loans_bn": round(float(D.LNLSNET.sum()) / 1e6, 1),
        "loans_by_category_bn": {k: round(v, 1) for k, v in tot.items()},
        "size_class_counts": D.size_class.value_counts().to_dict(),
        "business_model_counts": D.business_model.value_counts().to_dict(),
        "KNOWN_GAP": "LNRERES combines first-lien and home equity; the API exposes no "
                     "revolving open-end split, so the two cannot be separated from this "
                     "source. Treated as one residential book and recorded as a limitation.",
    }
    (HERE / "fdic_summary.json").write_text(json.dumps(summ, indent=2))

    pd.set_option("display.width", 200)
    print(f"FDIC institutions at {REPDTE}: {n_fin}")
    print(f"  total assets      {summ['total_assets_bn']:>12,.1f} bn")
    print(f"  tier 1 capital    {summ['total_tier1_bn']:>12,.1f} bn")
    print(f"  net loans         {summ['total_net_loans_bn']:>12,.1f} bn")
    print("\nloans by category, bn")
    for k, v in summ["loans_by_category_bn"].items():
        print(f"  {k:10s} {v:>12,.1f}")
    print("\nby size class")
    print(D.groupby("size_class").agg(n=("CERT", "size"),
                                      assets_bn=("ASSET", lambda s: s.sum() / 1e6))
          .round(1).to_string())
    print("\nby business model")
    print(D.groupby("business_model").agg(n=("CERT", "size"),
                                          assets_bn=("ASSET", lambda s: s.sum() / 1e6))
          .round(1).to_string())


if __name__ == "__main__":
    main()
