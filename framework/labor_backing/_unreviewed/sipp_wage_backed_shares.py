"""Working-core share of each household claim class, SIPP 2025.

PROVISIONAL. Produced in the Part B definition pass. Writes only inside
framework/labor_backing/ and modifies nothing in src/ or data/.

Definition follows checklist item C3 exactly as the household stress engine states it:
a WORKING-CORE household contains at least one EMPLOYED MEMBER AGED 25 TO 64. Every other
household is NON-WORKING for the purpose of first-round servicing, which is the same split
A43 and A47 used for mortgage service and gross rent on ACS.

Output is the share of each debt BALANCE held by working-core households. That is not the
same object as A43's share of mortgage SERVICE, and the difference is a named judgement
call in definition.md.
"""
import importlib.util, json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[2]
OUT = pathlib.Path(__file__).parent


def _mod(name, rel):
    s = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def main():
    sb2 = _mod("sb2", "src/sipp_buffers_v2.py")
    D, _ = sb2.load()
    hh = sb2.build_hh(D)

    age = pd.to_numeric(D["TAGE"], errors="coerce")
    core_person = D["employed"] & age.between(25, 64)
    core = D.assign(c=core_person.astype(int)).groupby("hh")["c"].sum().reindex(hh.index).fillna(0) > 0
    hh["working_core"] = core.values

    classes = [("mortgage", "mortgage"), ("vehicle", "vehicle"), ("student", "student"),
               ("credit_card", "credit_card"), ("other_unsecured", "other"),
               ("medical", "medical"), ("all_debt", "all_debt"),
               ("unsecured_total", "unsecured_total"), ("secured_total", "secured_total")]

    w = hh["wgt"].to_numpy(float)
    rows = []
    for label, col in classes:
        v = pd.to_numeric(hh[col], errors="coerce").fillna(0.0).to_numpy(float)
        tot = float((v * w).sum())
        cor = float((v * w * hh["working_core"].to_numpy(bool)).sum())
        holders_tot = float(w[(v > 0)].sum())
        holders_core = float(w[(v > 0) & hh["working_core"].to_numpy(bool)].sum())
        rows.append({"class": label, "sipp_var": col,
                     "balance_total_bn": tot / 1e9, "balance_working_core_bn": cor / 1e9,
                     "working_core_share_of_balance": cor / tot if tot else np.nan,
                     "working_core_share_of_holders": holders_core / holders_tot if holders_tot else np.nan,
                     "n_unweighted_holders": int((v > 0).sum())})
    df = pd.DataFrame(rows)

    meta = {
        "source": "SIPP 2025 panel, person file pu2025_csv.zip, MONTHCODE 12",
        "weights": "WPFINWGT from the household reference person (ERELRPE in (1,2)), per src/sipp_buffers_v2.py",
        "working_core_definition": "at least one member employed (RMESR in 1..5) and aged 25 to 64",
        "households_weighted_m": float(hh["wgt"].sum()) / 1e6,
        "working_core_households_weighted_m": float(hh.loc[hh["working_core"], "wgt"].sum()) / 1e6,
        "working_core_share_of_households": float(hh.loc[hh["working_core"], "wgt"].sum() / hh["wgt"].sum()),
        "status": "PROVISIONAL, produced this session, no second-dataset check (C2 outstanding)",
    }
    df.to_csv(OUT / "sipp_wage_backed_shares.csv", index=False)
    (OUT / "sipp_wage_backed_shares.json").write_text(json.dumps(meta, indent=2))
    print(df.to_string(index=False))
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
