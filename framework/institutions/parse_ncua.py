"""MODULE A1, part two. Institution-level balance sheets for federally insured credit unions.

MEASURED, not scenario. Source: NCUA quarterly Call Report data, 2026-06 cycle,
https://ncua.gov/files/publications/analysis/call-report-data-2026-06.zip, retained at
framework/institutions/ncua_2026-06.zip.

ACCOUNT MAP, read from the archive's own AcctDesc.txt:
    Acct_010    TOTAL ASSETS
    Acct_997    Total Net Worth                    (the credit union analogue of tier 1)
    Acct_703A   1st lien 1-4 family residential
    Acct_386A   junior lien 1-4 family residential (home equity, SEPARATELY REPORTED, unlike
                the FDIC series, which is a point worth noting: for credit unions we CAN see
                the split and for banks we cannot)
    Acct_385    new vehicle
    Acct_370    used vehicle
    Acct_396    unsecured credit card
    Acct_397    all other unsecured

Credit unions are included because the instruction asks for them and because they are the
one institution class whose book is almost entirely household credit, which is exactly the
exposure this paper measures. They hold no C and I book to speak of and almost no commercial
real estate, so a wage shock reaches them more directly than it reaches a diversified bank.
"""
import io
import json
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
ZIP = HERE / "ncua_2026-06.zip"

ACCTS = {
    "Acct_010": "assets",
    "Acct_997": "net_worth",
    "Acct_703A": "res_first_lien",
    "Acct_386A": "res_junior_lien",
    "Acct_385": "auto_new",
    "Acct_370": "auto_used",
    "Acct_396": "credit_card",
    "Acct_397": "other_unsecured",
}


def load_wide(z):
    """Credit union call report tables are one row per credit union, columns are accounts.
    Walk every FS220 table and take whichever of our accounts it carries."""
    frames = []
    for name in z.namelist():
        if not name.startswith("FS220") or not name.endswith(".txt"):
            continue
        try:
            d = pd.read_csv(io.BytesIO(z.read(name)), encoding="latin-1",
                            low_memory=False)
        except Exception:
            continue
        if "CU_NUMBER" not in d.columns:
            continue
        # the archive's data files use uppercase ACCT_ while AcctDesc.txt uses Acct_
        up = {k.upper(): k for k in ACCTS}
        cols = [c for c in d.columns if c.upper() in up]
        d = d.rename(columns={c: up[c.upper()] for c in cols})
        cols = [up[c.upper()] for c in cols]
        if cols:
            frames.append(d[["CU_NUMBER"] + cols])
    out = None
    for f in frames:
        out = f if out is None else out.merge(f, on="CU_NUMBER", how="outer",
                                              suffixes=("", "_dup"))
    out = out[[c for c in out.columns if not c.endswith("_dup")]]
    return out


def main():
    z = zipfile.ZipFile(ZIP)
    D = load_wide(z)
    info = pd.read_csv(io.BytesIO(z.read("FOICU.txt")), encoding="latin-1",
                       low_memory=False)
    keep = [c for c in ["CU_NUMBER", "CU_NAME", "STATE"] if c in info.columns]
    D = D.merge(info[keep], on="CU_NUMBER", how="left")

    D = D.rename(columns=ACCTS)
    for v in ACCTS.values():
        if v not in D.columns:
            D[v] = 0.0
        D[v] = pd.to_numeric(D[v], errors="coerce").fillna(0.0)

    D["residential"] = D.res_first_lien + D.res_junior_lien
    D["auto"] = D.auto_new + D.auto_used
    D["consumer_other"] = D.other_unsecured
    D["total_measured_loans"] = (D.residential + D.auto + D.credit_card
                                 + D.consumer_other)
    D = D[D.assets > 0].copy()

    def size_class(a):                      # NCUA reports dollars, not thousands
        if a >= 10e9:
            return "credit union, over 10bn"
        if a >= 1e9:
            return "credit union, 1 to 10bn"
        if a >= 100e6:
            return "credit union, 100m to 1bn"
        return "credit union, under 100m"
    D["size_class"] = D.assets.map(size_class)
    D["business_model"] = "credit union"

    D.to_csv(HERE / "ncua_institutions_202606.csv", index=False)

    bn = 1e9
    summ = {
        "source": "NCUA quarterly Call Report data, 2026-06 cycle",
        "file": "ncua_2026-06.zip",
        "n_credit_unions": int(len(D)),
        "total_assets_bn": round(float(D.assets.sum()) / bn, 1),
        "total_net_worth_bn": round(float(D.net_worth.sum()) / bn, 1),
        "loans_bn": {
            "residential_first_lien": round(float(D.res_first_lien.sum()) / bn, 1),
            "residential_junior_lien": round(float(D.res_junior_lien.sum()) / bn, 1),
            "auto": round(float(D.auto.sum()) / bn, 1),
            "credit_card": round(float(D.credit_card.sum()) / bn, 1),
            "other_unsecured": round(float(D.other_unsecured.sum()) / bn, 1),
        },
        "net_worth_ratio_system": round(float(D.net_worth.sum() / D.assets.sum()), 4),
        "note": "Credit unions report the junior-lien (home equity) split separately, "
                "which the FDIC API does not expose for banks.",
    }
    (HERE / "ncua_summary.json").write_text(json.dumps(summ, indent=2))

    print(f"credit unions: {summ['n_credit_unions']}")
    print(f"  assets      {summ['total_assets_bn']:>10,.1f} bn")
    print(f"  net worth   {summ['total_net_worth_bn']:>10,.1f} bn "
          f"({100*summ['net_worth_ratio_system']:.2f} pct of assets)")
    for k, v in summ["loans_bn"].items():
        print(f"  {k:26s} {v:>10,.1f} bn")
    print()
    print(D.groupby("size_class").agg(n=("CU_NUMBER", "size"),
                                      assets_bn=("assets", lambda s: s.sum() / bn))
          .round(1).to_string())


if __name__ == "__main__":
    main()
