"""Playbook section 8 QA gates, run against the LaTeX source.

The PDF-level gates (compile clean, undefined refs, anon leak check) run after a build;
these are the source-level gates that can run without a TeX installation.
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent


def main():
    t = (HERE / "main.tex").read_text(encoding="utf-8")
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

    ti = re.search(r"\\title\{(.+?)\}\s*\n", t, re.S).group(1)
    ti = re.sub(r"\\\\|\\bfseries|[{}]", " ", ti)
    nti = len(ti.split())
    print(f"title ({nti} words): {' '.join(ti.split())}")
    if nti > 12:
        fails.append(f"title is {nti} words, cap is 12")

    ab = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", t, re.S).group(1)
    ab = re.sub(r"\\result\{[A-Za-z]+\}", "00", ab)
    ab = re.sub(r"\\[a-zA-Z]+", " ", ab)
    nab = len(ab.split())
    print(f"abstract words {nab}")
    if nab > 250:
        fails.append(f"abstract is {nab} words, cap is 250")

    keys = set(re.findall(r"@[a-z]+\{([A-Za-z0-9]+),", bib))
    cited = set(re.findall(r"\\cite[tp]\{([A-Za-z0-9]+)\}", t))
    unres = sorted(cited - keys)
    print(f"citations used {len(cited)}, all resolve: {not unres}")
    if unres:
        fails.append(f"unresolved citations: {unres}")

    banned = ["delve", "it is worth noting", "in today's world", "crucial role",
              "vital role", "navigate the landscape", "tapestry", "testament to",
              "In conclusion,"]
    hits = [b for b in banned if b.lower() in t.lower()]
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
