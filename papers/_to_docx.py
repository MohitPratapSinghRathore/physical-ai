"""Playbook section 7 helper: pre-resolve LaTeX that pandoc cannot, then convert.

pandoc cannot run natbib, cannot evaluate the \\ifanon toggle and does not know
the \\result{} macros, so this script resolves all three into plain text first
and writes main_docx.tex for pandoc to consume.

    python ../_to_docx.py full      -> main_docx.tex (author version)
    python ../_to_docx.py anon      -> main_docx.tex (blind version)

Run from a paper directory, after main.pdf and main.bbl have been built.
"""
import pathlib
import re
import sys

HERE = pathlib.Path(".").resolve()
SHARED = HERE.parent.parent / "paper"


def load_macros():
    txt = (SHARED / "results_macros.tex").read_text(encoding="utf-8")
    return dict(re.findall(r"result@([A-Za-z0-9]+)\\endcsname\{([^}]*)\}", txt))


def load_refs():
    """Section and equation numbers from the .aux file."""
    aux = HERE / "main.aux"
    out = {}
    if aux.exists():
        for key, val in re.findall(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}",
                                   aux.read_text(encoding="utf-8", errors="replace")):
            out[key] = val
    return out


def load_cites():
    """key -> (author, year) from the apalike .bbl."""
    bbl = HERE / "main.bbl"
    out = {}
    if bbl.exists():
        for label, key in re.findall(r"\\bibitem\[([^\]]*)\]\{([^}]*)\}",
                                     bbl.read_text(encoding="utf-8", errors="replace")):
            label = label.replace("{", "").replace("}", "").replace("~", " ")
            if "," in label:
                author, year = label.rsplit(",", 1)
                out[key] = (author.strip(), year.strip())
            else:
                out[key] = (label.strip(), "")
    return out


def inline_inputs(text, seen=None):
    seen = seen or set()
    def repl(m):
        name = m.group(1)
        if not name.endswith(".tex"):
            name = name + ".tex"
        for base in (HERE, SHARED):
            p = base / name
            if p.exists() and str(p) not in seen:
                seen.add(str(p))
                return inline_inputs(p.read_text(encoding="utf-8", errors="replace"), seen)
        return ""
    return re.sub(r"\\input\{([^}]*)\}", repl, text)


def resolve_toggle(text, anon):
    """Evaluate \\ifanon ... \\else ... \\fi without nesting support (none is used)."""
    # the toggle's own declaration must go first, or the regex below matches the
    # \ifanon inside \newif\ifanon and eats the preamble
    text = text.replace("\\newif\\ifanon", "")
    text = text.replace("\\ifdefined\\ANON\\anontrue\\else\\anonfalse\\fi", "")
    pat = re.compile(r"\\ifanon(.*?)(?:\\else(.*?))?\\fi", re.S)
    def repl(m):
        a, b = m.group(1), m.group(2) or ""
        return a if anon else b
    while pat.search(text):
        new = pat.sub(repl, text)
        if new == text:
            break
        text = new
    return text


def main():
    mode = (sys.argv[1] if len(sys.argv) > 1 else "full").lower()
    anon = mode == "anon"

    text = (HERE / "main.tex").read_text(encoding="utf-8", errors="replace")
    text = resolve_toggle(text, anon)
    text = inline_inputs(text)

    macros = load_macros()
    missing = set()

    def rmac(m):
        k = m.group(1)
        if k not in macros:
            missing.add(k)
            return k
        return macros[k]
    text = re.sub(r"\\result\{([A-Za-z0-9]+)\}", rmac, text)

    # pandoc drops \maketitle, so promote the title (and authors, when not blind)
    tm = re.search(r"\\title\{\\bfseries\s*(.*?)\}", text, re.S)
    if tm:
        title = re.sub(r"\s+", " ", tm.group(1)).strip()
        head = "\\section*{" + title + "}\n"
        if anon:
            head += "\n\\noindent\\textit{Author names and affiliations removed for " \
                    "double-anonymous peer review.}\n"
        else:
            head += (
                "\n\\noindent Mohit Pratap Singh Rathore$^{1}$, "
                "Gunveer Singh Kalsi$^{1}$, Sriharsha Meduri$^{1}$, "
                "Pratap Chandra Mandal$^{2}$\n\n"
                "\\noindent $^{1}$Oviqo. $^{2}$Indian Institute of Management Shillong.\n\n"
                "\\noindent Corresponding author: Mohit Pratap Singh Rathore, "
                "mohitpratapsinghr@gmail.com\n")
        text = text.replace("\\maketitle", head, 1)

    # pandoc hoists the abstract environment above the title block, which puts the
    # author names in the wrong place for a submission. Demote it to a heading so
    # document order is preserved: title, authors, abstract, keywords.
    text = text.replace("\\begin{abstract}", "\\subsection*{Abstract}")
    text = text.replace("\\end{abstract}", "")

    refs = load_refs()
    text = re.sub(r"\\(?:eq)?ref\{([^}]*)\}", lambda m: refs.get(m.group(1), "?"), text)

    cites = load_cites()

    def citet(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        parts = [f"{cites[k][0]} ({cites[k][1]})" for k in keys if k in cites]
        return "; ".join(parts) if parts else ""

    def citep(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        parts = [f"{cites[k][0]}, {cites[k][1]}" for k in keys if k in cites]
        return "(" + "; ".join(parts) + ")" if parts else ""

    text = re.sub(r"\\citet\{([^}]*)\}", citet, text)
    text = re.sub(r"\\citep\{([^}]*)\}", citep, text)

    # the bibliography itself, as alphabetical paragraphs
    bbl = HERE / "main.bbl"
    biblio = ""
    if bbl.exists():
        raw = bbl.read_text(encoding="utf-8", errors="replace")
        entries = re.split(r"\\bibitem\[[^\]]*\]\{[^}]*\}", raw)[1:]
        clean = []
        for e in entries:
            e = e.split("\\end{thebibliography}")[0]
            e = e.replace("\\newblock", " ").replace("\\em ", "")
            e = re.sub(r"[{}]", "", e)
            e = re.sub(r"\s+", " ", e).strip()
            if e:
                clean.append(e)
        biblio = "\\section*{References}\n\n" + "\n\n".join(clean) + "\n"
    text = re.sub(r"\\bibliographystyle\{[^}]*\}\s*\\bibliography\{[^}]*\}",
                  lambda _: biblio, text)

    out = HERE / "main_docx.tex"
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out.name}  mode={mode}")
    if missing:
        print("WARNING unresolved \\result keys:", ", ".join(sorted(missing)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
