"""Playbook section 8 QA gates. Run from a paper directory:  python ../_qa.py

Checks the built PDF and the LaTeX sources against the non-negotiable rules:
no em-dashes, never the word "robust", title at most twelve words, abstract
within cap, no undefined references or citations, no "---" anywhere, and every
\\result{} macro used is actually defined in results_macros.tex.
"""
import pathlib
import re
import subprocess
import sys

EM_DASH = "\u2014"
ABSTRACT_CAP = 250
TITLE_CAP = 12


def pdf_text(pdf):
    out = subprocess.run(["pdftotext", pdf, "-"], capture_output=True)
    return out.stdout.decode("utf-8", errors="replace")


def main():
    here = pathlib.Path(".").resolve()
    pdf = here / "main.pdf"
    if not pdf.exists():
        print("main.pdf not built")
        return 1
    t = pdf_text(str(pdf))
    src = list((here / "sections").glob("*.tex")) + [here / "main.tex"]
    src_text = "\n".join(f.read_text(encoding="utf-8", errors="replace") for f in src)

    title = re.search(r"\\title\{\\bfseries ([^}]*)\}",
                      (here / "main.tex").read_text(encoding="utf-8")).group(1)
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}",
                  (here / "main.tex").read_text(encoding="utf-8"), re.S)
    abstract = re.sub(r"\\[a-zA-Z]+\{?|\}|\\noindent", " ", m.group(1))

    body = t
    if "References" in t:
        body = t[:t.rfind("References")]

    rows = []
    rows.append(("title words", len(title.split()), f"<= {TITLE_CAP}",
                 len(title.split()) <= TITLE_CAP))
    rows.append(("abstract words", len(abstract.split()), f"<= {ABSTRACT_CAP}",
                 len(abstract.split()) <= ABSTRACT_CAP))
    rows.append(("em-dash in PDF", t.count(EM_DASH), "0", t.count(EM_DASH) == 0))
    rows.append(("'---' in sources", src_text.count("---"), "0",
                 src_text.count("---") == 0))
    # an en-dash used as punctuation reads as a dash; one inside a number range
    # (page numbers in the bibliography) is legitimate, so only flag the former
    en_punct = len(re.findall(r"(?<=[A-Za-z,;\s])–(?=[A-Za-z\s])", t))
    rows.append(("en-dash as punctuation", en_punct, "0", en_punct == 0))
    # a bare double hyphen in prose (not a LaTeX comment or option) renders as a dash
    dbl = len(re.findall(r"(?<![-\w])--(?![-\w])", src_text))
    rows.append(("'--' as punctuation in src", dbl, "0", dbl == 0))
    nrob = len(re.findall("robust", t, re.I))
    rows.append(("'robust' in PDF", nrob, "0", nrob == 0))
    rows.append(("'??' undefined in PDF", body.count("??"), "0", body.count("??") == 0))

    # every \result{} used must be defined
    macros = (here.parent.parent / "paper" / "results_macros.tex").read_text(encoding="utf-8")
    have = set(re.findall(r"result@([A-Za-z0-9]+)\\endcsname", macros))
    used = set(re.findall(r"\\result\{([A-Za-z0-9]+)\}", src_text))
    missing = sorted(used - have)
    rows.append(("undefined \\result macros", len(missing), "0", not missing))

    # playbook 2.3: phrases that read as machine-generated
    tells = ["delve", "it is worth noting", "in today's world", "crucial role",
             "vital role", "navigate the landscape", "tapestry", "testament to",
             "In conclusion,", "Moreover,", "Furthermore,"]
    found = [w for w in tells if w.lower() in t.lower()]
    rows.append(("AI-tell phrases", len(found), "0", not found))

    # Mangled control sequences. Writing LaTeX through a shell heredoc can turn the
    # backslash of \result or \ref into a bare carriage return, leaving a plain CR followed
    # by "esult{...}" or "ef{...}". The macro stays defined and no "??" appears, so every
    # other gate passes while the PDF prints "esultFoo". Four of these reached a reviewer.
    # A CR not followed by LF is never legitimate in these sources.
    CR = bytes([13])
    LF = bytes([10])
    mangled = []
    for f in src:
        b = f.read_bytes()
        for i in range(len(b)):
            if b[i:i + 1] == CR and b[i + 1:i + 2] != LF:
                mangled.append(f"{f.name}: {b[i:i + 24].decode('latin-1')!r}")
    rows.append(("mangled control seqs", len(mangled), "0", not mangled))

    # Repairing the above by restoring only a backslash leaves \esult or \ef, because the
    # letter after the backslash was consumed into the carriage return. LaTeX in nonstopmode
    # then prints the argument and drops the command, so the PDF shows "MultifamilyZeroMovePct"
    # with no stem to find. Check the SOURCE for the truncated forms, not the output.
    trunc = []
    for f in src:
        b = f.read_bytes()
        for bad in (b"\\esult", b"\\ef{", b"\\aragraph", b"\\esultp"):
            if bad in b:
                trunc.append(f"{f.name}: {bad.decode('latin-1')}")
    rows.append(("truncated macro stems", len(trunc), "0", not trunc))

    # Any undefined control sequence in the build log is this class of damage or worse.
    log = here / "main.log"
    undef = []
    if log.exists():
        lt = log.read_text(encoding="utf-8", errors="replace")
        undef = re.findall(r"Undefined control sequence.*", lt)
    rows.append(("undefined control seqs", len(undef), "0", not undef))

    # limitations <-> future research must pair one to one
    nL = len(re.findall(r"\\paragraph\{L\d+\.", src_text))
    nF = len(re.findall(r"\\item\[FR\d+\]", src_text))
    rows.append(("limitations L1..N", nL, f"= FR count ({nF})", nL == nF and nL > 0))

    print(f"{'GATE':30s} {'VALUE':>8s}  {'REQUIRED':<18s} STATUS")
    print("-" * 70)
    ok = True
    for name, val, req, passed in rows:
        ok &= passed
        print(f"{name:30s} {str(val):>8s}  {req:<18s} {'PASS' if passed else 'FAIL'}")
    if mangled:
        print("\nMANGLED CONTROL SEQUENCES (a carriage return replacing a backslash):")
        for x in mangled:
            print("   ", x)
    if trunc:
        print("\nTRUNCATED MACRO STEMS IN THE SOURCE:", ", ".join(trunc))
    if undef:
        print("\nUNDEFINED CONTROL SEQUENCES IN THE LOG:")
        for x in undef[:8]:
            print("   ", x.strip())
    if missing:
        print("\nmissing macros:", ", ".join(missing))
    if found:
        print("\nAI-tell phrases present:", ", ".join(found))
    bw = len(body.split())
    print(f"\nbody words (approx, to references): {bw:,}")
    print("\nALL GATES PASS" if ok else "\nGATES FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
