"""Physical AI Exposure Index (PAEI) from O*NET 31.0.

Design. Existing occupational AI-exposure measures (Frey-Osborne; Felten et al.; Webb;
Eloundou et al.) score exposure to cognitive automation. Physical AI is a different
technology with a different binding constraint, so it needs its own index.

The index is two-factor and multiplicative, following Moravec's paradox: a robot displaces
a task only if the task (a) requires a body at all, and (b) sits in an environment
structured enough for a machine to act in reliably. Either factor near zero means no
physical-AI exposure, which a purely additive index would miss.

    PAEI = P * S

    P = embodiment intensity      (does this job require a physical body?)
    S = environmental structure   (enablers minus frictions), rescaled to [0,1]

P high and S low is the Moravec region: physically demanding, hard to automate
(emergency plumber, home health aide). P high and S high is the exposed region
(assembly, packing, machine tending). P low means the job is exposed to cognitive AI
instead, which this index deliberately does not score.

All elements are normalised to [0,1] using O*NET published scale anchors
(Scales Reference.txt), never by min-max across occupations, so the index is comparable
across O*NET releases.
"""
import csv, io, json, pathlib, zipfile
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
ZIP = ROOT / "data" / "raw" / "onet" / "db_31_0_text.zip"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)
ONET_VERSION = "31.0"

A, WA, WC = "Abilities", "Work Activities", "Work Context"

# ---- construct definitions: (element id, source file, scale id) ----
EMBODIMENT = [
    ("1.A.2.a.1", A, "IM"),    # Arm-Hand Steadiness
    ("1.A.2.a.2", A, "IM"),    # Manual Dexterity
    ("1.A.2.a.3", A, "IM"),    # Finger Dexterity
    ("1.A.2.b.2", A, "IM"),    # Multilimb Coordination
    ("1.A.3.a.1", A, "IM"),    # Static Strength
    ("1.A.3.a.4", A, "IM"),    # Trunk Strength
    ("1.A.3.b.1", A, "IM"),    # Stamina
    ("1.A.3.c.3", A, "IM"),    # Gross Body Coordination
    ("4.A.3.a.1", WA, "IM"),   # Performing General Physical Activities
    ("4.A.3.a.2", WA, "IM"),   # Handling and Moving Objects
    ("4.A.3.a.3", WA, "IM"),   # Controlling Machines and Processes
    ("4.A.3.a.4", WA, "IM"),   # Operating Vehicles, Mechanized Devices, or Equipment
    ("4.C.2.d.1.b", WC, "CX"), # Spend Time Standing
    ("4.C.2.d.1.g", WC, "CX"), # Spend Time Using Hands to Handle, Control, or Feel Objects
    ("4.C.2.d.1.h", WC, "CX"), # Spend Time Bending or Twisting Your Body
]

STRUCTURE_ENABLERS = [
    ("4.C.3.b.2", WC, "CX"),   # Degree of Automation
    ("4.C.3.b.7", WC, "CX"),   # Importance of Repeating Same Tasks
    ("4.C.3.d.3", WC, "CX"),   # Pace Determined by Speed of Equipment
    ("4.C.2.a.1.a", WC, "CX"), # Indoors, Environmentally Controlled
    ("4.C.2.d.1.i", WC, "CX"), # Spend Time Making Repetitive Motions
    ("4.C.3.b.4", WC, "CX"),   # Importance of Being Exact or Accurate
]

STRUCTURE_FRICTIONS = [
    ("4.C.3.a.4", WC, "CX"),   # Freedom to Make Decisions
    ("4.C.3.b.8", WC, "CX"),   # Determine Tasks, Priorities and Goals
    ("4.C.2.a.1.c", WC, "CX"), # Outdoors, Exposed to All Weather Conditions
    ("4.C.2.b.1.e", WC, "CX"), # Exposed to Cramped Work Space, Awkward Positions
    ("4.C.1.a.4", WC, "CX"),   # Contact With Others
    ("4.C.1.b.1.f", WC, "CX"), # Deal With External Customers or the Public
    ("4.C.3.a.1", WC, "CX"),   # Consequence of Error
]

FILES = {A: "db_31_0_text/Abilities.txt", WA: "db_31_0_text/Work Activities.txt",
         WC: "db_31_0_text/Work Context.txt"}


def read_scales(z):
    t = io.TextIOWrapper(z.open("db_31_0_text/Scales Reference.txt"), encoding="utf-8", errors="replace")
    r = csv.reader(t, delimiter="\t"); next(r)
    return {row[0]: (float(row[2]), float(row[3])) for row in r}


def read_values(z, fname, wanted):
    t = io.TextIOWrapper(z.open(fname), encoding="utf-8", errors="replace")
    r = csv.reader(t, delimiter="\t"); hdr = next(r)
    i_val = hdr.index("Data Value")
    rows = []
    for row in r:
        if (row[1], row[3]) in wanted:
            rows.append((row[0], row[1], row[2], row[3], float(row[i_val])))
    return pd.DataFrame(rows, columns=["soc", "element", "name", "scale", "value"])


def factor(df, spec, scales, label):
    """Normalise each element to [0,1] by published scale anchors, then average."""
    want = {(e, s) for e, _, s in spec}
    d = df[[(e, s) in want for e, s in zip(df["element"], df["scale"])]].copy()
    lo = d["scale"].map(lambda s: scales[s][0])
    hi = d["scale"].map(lambda s: scales[s][1])
    d["norm"] = (d["value"] - lo) / (hi - lo)
    wide = d.pivot_table(index="soc", columns="element", values="norm")
    missing = [e for e, _, _ in spec if e not in wide.columns]
    if missing:
        print(f"  WARN {label}: elements absent from O*NET {ONET_VERSION}: {missing}")
    return wide.mean(axis=1, skipna=True), wide.notna().mean(axis=1), wide


def main():
    z = zipfile.ZipFile(ZIP)
    scales = read_scales(z)
    allspec = EMBODIMENT + STRUCTURE_ENABLERS + STRUCTURE_FRICTIONS
    frames = []
    for src, fname in FILES.items():
        wanted = {(e, s) for e, f, s in allspec if f == src}
        if wanted:
            frames.append(read_values(z, fname, wanted))
    df = pd.concat(frames, ignore_index=True)

    P, covP, _ = factor(df, EMBODIMENT, scales, "EMBODIMENT")
    Eplus, covE, _ = factor(df, STRUCTURE_ENABLERS, scales, "ENABLERS")
    Fminus, covF, _ = factor(df, STRUCTURE_FRICTIONS, scales, "FRICTIONS")

    # S in [0,1]: enablers == frictions maps to 0.5
    S = ((Eplus - Fminus) + 1.0) / 2.0

    t = io.TextIOWrapper(z.open("db_31_0_text/Occupation Data.txt"), encoding="utf-8", errors="replace")
    r = csv.reader(t, delimiter="\t"); next(r)
    titles = {row[0]: row[1] for row in r}

    out = pd.DataFrame({"embodiment_P": P, "structure_S": S, "enablers": Eplus,
                        "frictions": Fminus, "coverage_P": covP,
                        "coverage_S": (covE + covF) / 2}).dropna(subset=["embodiment_P", "structure_S"])
    out["PAEI"] = out["embodiment_P"] * out["structure_S"]
    out.insert(0, "title", out.index.map(lambda s: titles.get(s, "?")))
    out.index.name = "onet_soc"
    out = out.sort_values("PAEI", ascending=False).round(4)
    out.to_csv(OUT / "paei_onet.csv")

    meta = {"onet_version": ONET_VERSION, "n_occupations": int(len(out)),
            "elements": {"embodiment": [e for e, _, _ in EMBODIMENT],
                         "enablers": [e for e, _, _ in STRUCTURE_ENABLERS],
                         "frictions": [e for e, _, _ in STRUCTURE_FRICTIONS]},
            "normalisation": "published O*NET scale anchors (Scales Reference.txt)",
            "formula": "PAEI = P * S ; S = ((mean(enablers) - mean(frictions)) + 1)/2"}
    (OUT / "paei_meta.json").write_text(json.dumps(meta, indent=2))

    pd.set_option("display.width", 200)
    print(f"\nBuilt PAEI for {len(out)} O*NET occupations (O*NET {ONET_VERSION})\n")
    print("=== TOP 15 by PAEI (expect structured physical work) ===")
    print(out.head(15)[["title", "embodiment_P", "structure_S", "PAEI"]].to_string(max_colwidth=50))
    print("\n=== BOTTOM 10 by PAEI (expect cognitive/desk work) ===")
    print(out.tail(10)[["title", "embodiment_P", "structure_S", "PAEI"]].to_string(max_colwidth=50))


if __name__ == "__main__":
    main()
