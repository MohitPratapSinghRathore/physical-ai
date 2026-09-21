"""Playbook section 8 gates, run against the LaTeX source and the resolved bibliography.

The PDF-level gates (dashes, undefined refs, the anonymous leak check) are in
pdf_gates.py and run after a build. These are the source-level gates.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent

# Strings that belong to the project's internal record, never to the manuscript.
INTERNAL = [
    "superseded A38", "dose", "tau_k", "tau_b", "tau_l", "rho(", "sealed",
    "plausibility audit", "instance that", "the brief", "replication brief",
    "data/raw", "src/", "framework/", "notes/",
]
# A-numbers: the project's own session identifiers, e.g. A115, A118.
A_NUMBER = re.compile(r"\bA1[0-9]{2}\b")

# Strings that must never reach a printed bibliography entry.
BIB_BANNED = ["data/raw", "repository", "verified", "placed by", "src/", "``", "''"]

BANNED_PHRASES = [
    "delve", "it is worth noting", "in today's world", "crucial role",
    "vital role", "navigate the landscape", "tapestry", "testament to",
    "In conclusion,",
]


def main():
    main_tex = (HERE / "main.tex").read_text(encoding="utf-8")
    t = main_tex
    main_body = main_tex.split("\\appendix")[0]
    for sec in sorted((HERE / "sections").glob("*.tex")):
        text = sec.read_text(encoding="utf-8")
        t += "\n" + text
        if not sec.stem.startswith("appendix"):
            main_body += "\n" + text
    tables = ""
    for tab in sorted((HERE / "tables").glob("*.tex")):
        tables += "\n" + tab.read_text(encoding="utf-8")
    m = (HERE / "results_macros.tex").read_text(encoding="utf-8")
    bib = (HERE / "references.bib").read_text(encoding="utf-8")

    fails = []

    defined = set(re.findall(r"result@([A-Za-z]+)\\endcsname", m))
    used = set(re.findall(r"\\result\{([A-Za-z]+)\}", t))
    undef = sorted(used - defined)
    print(f"macros defined {len(defined)}, used in prose {len(used)}")
    if undef:
        fails.append(f"undefined result macros used: {undef}")

    em, en, tri = t.count("\u2014"), t.count("\u2013"), t.count("---")
    print(f"em-dash {em}, en-dash {en}, '---' {tri}")
    if em or en or tri:
        fails.append("dash rule violated")

    rob = t.lower().count("robust")
    print(f"'robust' occurrences {rob}")
    if rob:
        fails.append("the word robust appears")

    # internal vocabulary, in the prose and in the generated tables. Macro names and
    # mathematics are stripped first: a symbol inside an equation is defined there.
    body = t + tables
    body = re.sub(r"\\result\{[A-Za-z]+\}", " ", body)
    body = re.sub(r"\\begin\{equation\}.*?\\end\{equation\}", " ", body, flags=re.S)
    body = re.sub(r"\$[^$]*\$", " ", body)
    low = body.lower()
    hits = sorted({s for s in INTERNAL if s.lower() in low})
    anums = sorted(set(A_NUMBER.findall(body)))
    print(f"internal vocabulary: {hits or 'none'}; A-numbers: {anums or 'none'}")
    if hits:
        fails.append(f"internal vocabulary in the manuscript: {hits}")
    if anums:
        fails.append(f"internal session identifiers in the manuscript: {anums}")

    # ---- the main text states results, not the history of its own drafts. The appendices
    # may describe what the rebuild rounds caught; the body may not narrate earlier versions.
    SELF_NARRATION = ["earlier version", "was wrong", "withdrawn", "this project",
                      "we have tested it", "for most of this project", "has been replaced",
                      "a looser version"]
    narr = sorted({s for s in SELF_NARRATION if s.lower() in main_body.lower()})
    print(f"self-narration in the main text: {narr or 'none'}")
    if narr:
        fails.append(f"the main text narrates its own earlier drafts: {narr}")

    ti = re.search(r"\\title\{(.+?)\}\s*\n", t, re.S).group(1)
    ti = re.sub(r"\\\\|\\bfseries|[{}]", " ", ti)
    nti = len(ti.split())
    print(f"title ({nti} words): {' '.join(ti.split())}")
    if nti > 13:  # the owner chose a thirteen-word title
        fails.append(f"title is {nti} words, cap is 13")

    ab = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", t, re.S).group(1)
    ab = re.sub(r"\\result\{[A-Za-z]+\}", "00", ab)
    ab = re.sub(r"\\[a-zA-Z]+", " ", ab)
    nab = len(ab.split())
    print(f"abstract words {nab}")
    if nab > 200:
        fails.append(f"abstract is {nab} words, cap is 200")

    keys = set(re.findall(r"@[a-z]+\{([A-Za-z0-9]+),", bib))
    cited = {k.strip() for group in re.findall(r"\\cite[tp]\{([^}]*)\}", t)
             for k in group.split(",")}
    unres = sorted(cited - keys)
    uncited = sorted(keys - cited)
    print(f"bibliography entries {len(keys)}, cited in text {len(cited)}")
    if unres:
        fails.append(f"unresolved citations: {unres}")
    if uncited:
        fails.append(f"entries in the bibliography that the text never cites: {uncited}")

    # ---- every statement about closing the fiscal condition must match the artifact.
    # Absolute claims about the parameter space are banned outright, because the artifact
    # reports a pass SHARE by base and by labor tax reading, and an earlier version of this
    # manuscript asserted an absolute that the same artifact contradicts.
    ABSOLUTES = ["no corner of the parameter space", "nowhere in the space",
                 "cannot pass anywhere", "no combination closes", "never closes"]
    found = sorted({a for a in ABSOLUTES if a.lower() in t.lower()})
    tk_path = HERE.parent / "data" / "release" / "tau_k" / "tau_k_assembled.json"
    if tk_path.exists():
        tk = json.loads(tk_path.read_text())
        ours = [r for r in tk["assembled_SOURCED"] if r["rent_reading"] == "Barkai"][0]
        crs = [r for r in tk["MARKED_SENSITIVITY_at_CRS_implied_theta"]
               if r["rent_reading"] == "Barkai"][0]
        req = tk["required_tau_k"]["by_labour_reading"]
        shares = {"ours, easier": ours["pass_share_vs_required_low"],
                  "ours, harder": ours["pass_share_vs_required_high"],
                  "domestic base, easier": crs["pass_share_vs_required_low"],
                  "domestic base, harder": crs["pass_share_vs_required_high"]}
        maxima = {"ours": ours["tau_k_max_ANALYTIC"], "domestic base": crs["tau_k_max_ANALYTIC"]}
        exceeds = {k: v > req["AMR_0.255"] for k, v in maxima.items()}
        print(f"fiscal condition: pass shares {shares}; analytic maxima {maxima}; "
              f"exceeds the easier required rate {exceeds}")
        if found and any(exceeds.values()):
            fails.append(f"absolute claim about the parameter space {found} while the "
                         f"artifact's analytic maximum exceeds the easier required rate")
        elif found:
            fails.append(f"absolute claim about the parameter space: {found}. Report the "
                         f"pass share by base and by reading instead")
        # Any sentence CLAIMING that the condition closes must carry a pass-share macro.
        # Sentences reporting a withdrawn claim are exempt: they are corrections, not claims.
        WITHDRAWAL = ("earlier version", "asserted", "was wrong", "contradicts",
                      "has been replaced", "we do not make it")
        for sent in re.split(r"(?<=[.])\s+", t):
            if "closes the condition" in sent and "\\result{PassShare" not in sent \
                    and "closes nowhere" not in sent \
                    and not any(w in sent.lower() for w in WITHDRAWAL):
                fails.append("a sentence claims the condition closes without citing a pass "
                             f"share macro: {sent.strip()[:90]}")
                break
    else:
        print("fiscal condition gate: artifact not released, gate skipped")

    # the printed bibliography must carry no internal note
    bbl = HERE / "main.bbl"
    if bbl.exists():
        printed = bbl.read_text(encoding="utf-8")
        bad = sorted({s for s in BIB_BANNED if s.lower() in printed.lower()})
        print(f"printed bibliography, banned strings: {bad or 'none'}")
        if bad:
            fails.append(f"printed reference entries contain internal notes: {bad}")
    else:
        print("printed bibliography: main.bbl not built yet, gate skipped")

    # ---- the coefficient basis: Table 2 must print the basis the text says is adopted
    basis_file = ROOT / "data" / "release" / "revision_r2" / "b2_headline_effect.json"
    table2 = HERE / "tables" / "tab_claim_classes.tex"
    if basis_file.exists() and table2.exists():
        coeffs = json.loads(basis_file.read_text(encoding="utf-8"))["coefficients"]
        printed = table2.read_text(encoding="utf-8")
        LABEL = {"home_mortgage": "Home mortgage", "credit_card": "Credit card",
                 "auto_loan": "Auto loan", "student_loan": "Student loan"}
        wrong = []
        for key, label in LABEL.items():
            row = [ln for ln in printed.splitlines() if ln.startswith(label + " &")]
            if not row:
                wrong.append(f"{label}: row not found in Table 2")
                continue
            cell = row[0].split("&")[2].strip()
            adopted = f"{coeffs[key]['alternative']:.4f}"
            coverage = f"{coeffs[key]['published']:.4f}"
            if cell != adopted:
                wrong.append(f"{label}: table prints {cell}, adopted basis is {adopted}"
                             + (" (that is the coverage construction)"
                                if cell == coverage else ""))
        print(f"Table 2 coefficient basis: {wrong or 'adopted wage basis, as stated'}")
        if wrong:
            fails.append("Table 2 does not print the adopted coefficient basis: "
                         + "; ".join(wrong))
    else:
        print("Table 2 coefficient basis: artifact or table missing, gate skipped")

    # ---- withholding must not be described as unquantified anywhere
    unquantified = []
    for sent in re.split(r"(?<=[.])\s+", t):
        low = sent.lower()
        if "withhold" in low and ("not quantified" in low
                                  or "have not quantified" in low):
            unquantified.append(sent.strip()[:90])
    print(f"withholding described as unquantified: {unquantified or 'none'}")
    if unquantified:
        fails.append("withholding is quantified in Section 5 but described as "
                     f"unquantified: {unquantified}")

    hits = [b for b in BANNED_PHRASES if b.lower() in t.lower()]
    print(f"AI-tell phrases: {hits or 'none'}")
    if hits:
        fails.append(f"AI-tell phrases present: {hits}")

    stubs = len(re.findall(r"^% TO DRAFT", t, re.M))
    print(f"sections still to draft: {stubs}")

    print()
    if fails:
        print("GATES FAILED:")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("ALL SOURCE-LEVEL GATES PASS")


if __name__ == "__main__":
    main()
