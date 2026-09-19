"""A4 step 1: draw a stratified sample of O*NET task statements for independent LLM rating.

The sample is stratified across the S_rank distribution of the parent occupation, so the
raters see the full structure range rather than a mass of mid-structure tasks. Occupations
are sampled with probability proportional to employment within stratum, then one Core task
is drawn per sampled occupation-slot.

The rating file deliberately EXCLUDES S, S_rank, P and PAEI. Raters see only the occupation
title and the task text, so their scores cannot be anchored on the value being validated.
The key is written to a separate file that the raters never receive.
"""
import csv, io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
A4 = OUT / "a4"
A4.mkdir(parents=True, exist_ok=True)
N_OCC = 200
SEED = 20260919


def main():
    grid = pd.read_csv(OUT / "paei_c.csv")
    base = grid[grid["c"] == 0.0][
        ["occp", "soc", "title", "embodiment_P", "structure_S", "structure_S_rank",
         "employment"]].copy()
    base = base[base["employment"].notna() & (base["employment"] > 0)]

    # tasks, keyed by O*NET-SOC -> 6-digit SOC
    z = zipfile.ZipFile(RAW / "onet" / "db_31_0_text.zip")
    t = io.TextIOWrapper(z.open("db_31_0_text/Task Statements.txt"),
                         encoding="utf-8", errors="replace")
    r = csv.reader(t, delimiter="\t"); next(r)
    rows = [{"onet_soc": x[0], "task_id": x[1], "task": x[2], "task_type": x[3]}
            for x in r]
    T = pd.DataFrame(rows)
    T = T[T["task_type"] == "Core"].copy()
    T["soc"] = T["onet_soc"].astype(str).str[:7]

    # map tasks to OCCP through the same soc / broad-group logic used for PAEI
    T["broad"] = T["soc"].str[:6]
    b = base.copy()
    b["broad"] = b["soc"].astype(str).str[:6]
    exact = T.merge(b[["occp", "soc"]], on="soc", how="inner")
    rest = T[~T["soc"].isin(set(b["soc"]))]
    approx = rest.merge(b[["occp", "broad"]].drop_duplicates("broad"),
                        on="broad", how="inner")
    TT = pd.concat([exact, approx], ignore_index=True)

    rng = np.random.default_rng(SEED)
    base["stratum"] = pd.qcut(base["structure_S_rank"], 5, labels=[1, 2, 3, 4, 5])
    picks = []
    per = N_OCC // 5
    for s in [1, 2, 3, 4, 5]:
        pool = base[(base["stratum"] == s) & base["occp"].isin(set(TT["occp"]))]
        if len(pool) == 0:
            continue
        p = pool["employment"] / pool["employment"].sum()
        k = min(per, len(pool))
        idx = rng.choice(pool.index, size=k, replace=False, p=p)
        picks.append(pool.loc[idx])
    P = pd.concat(picks, ignore_index=True)

    out = []
    for _, r_ in P.iterrows():
        cand = TT[TT["occp"] == r_["occp"]]
        if len(cand) == 0:
            continue
        pick = cand.sample(1, random_state=int(rng.integers(1e9))).iloc[0]
        out.append({"item_id": f"T{len(out)+1:03d}",
                    "occupation_title": r_["title"], "task": pick["task"],
                    "occp": int(r_["occp"]), "task_id": pick["task_id"],
                    "structure_S": r_["structure_S"],
                    "structure_S_rank": r_["structure_S_rank"],
                    "embodiment_P": r_["embodiment_P"],
                    "employment": r_["employment"], "stratum": int(r_["stratum"])})
    D = pd.DataFrame(out)

    # rater file: NO S, S_rank, P, PAEI
    D[["item_id", "occupation_title", "task"]].to_csv(A4 / "a4_items_for_raters.csv",
                                                      index=False)
    D.to_csv(A4 / "a4_key.csv", index=False)

    rubric = """# A4 rating rubric: environmental structure of a work task

You are scoring WORK ENVIRONMENTS, not difficulty, skill, pay, or how impressive the job is.

For each item you are given an occupation title and one task that occupation performs.
Score the environment in which THAT TASK is carried out on four dimensions, each 1 to 5.

1. ENVIRONMENT PREDICTABILITY
   5 = the physical setting is fixed and known in advance and barely changes between
       repetitions (a fixed workstation, a production line, a controlled indoor room)
   1 = the setting changes every time and cannot be known in advance (a different customer
       home each visit, open terrain, a disaster site, a moving crowd)

2. OBJECT VARIABILITY
   5 = the task acts on identical, standardised objects presented the same way each time
   1 = the objects vary in shape, size, weight, position or condition every time, or are
       living, deformable, or unique

3. WORKSPACE ACCESS
   5 = the work area is open, uncluttered and easy for a machine on a fixed base or simple
       wheeled platform to reach
   1 = the work area is confined, cluttered, elevated, underground, requires climbing,
       crawling, or moving through human-scale spaces built only for people

4. NEED FOR IMPROVISATION
   5 = the task follows a fixed procedure with no judgement about how to proceed physically
   1 = the worker constantly improvises the physical approach in response to what is found

Score honestly and independently per dimension. Do NOT try to produce an overall
automation score, and do NOT let the prestige or wage of the occupation influence you. A
highly paid surgeon and a low paid home health aide can both sit in unpredictable settings;
a machine operator and a data entry clerk can both sit in predictable ones.

Output STRICT JSON, a single array, one object per item, nothing else:

[{"item_id":"T001","predictability":3,"object_variability":2,"workspace_access":4,"improvisation":2}]

Every item in the input must appear exactly once in your output.
"""
    (A4 / "a4_rubric.md").write_text(rubric, encoding="utf-8")

    meta = {"n_items": int(len(D)), "seed": SEED,
            "stratified_on": "structure_S_rank quintile, PPS by employment",
            "rater_file": "a4_items_for_raters.csv (no S, S_rank, P or PAEI)",
            "key_file": "a4_key.csv"}
    (A4 / "a4_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"wrote {len(D)} items to {A4/'a4_items_for_raters.csv'}")
    print(D.groupby("stratum").size().to_string())


if __name__ == "__main__":
    main()
