"""Playbook section 8 gates that need the built PDF, plus the body word count.

The dash rule is enforced on the BODY, from the introduction to the start of the
reference list. The reference list itself is excluded because the bibliography
style renders page ranges with an en dash, which is the publisher's convention
rather than authorial punctuation; any en dash there that is not inside a page
range is still reported as a failure.

Run after a build:  python paper/pdf_gates.py [main.pdf]
"""
import pathlib
import re
import sys

from pypdf import PdfReader

HERE = pathlib.Path(__file__).parent


def main():
    target = HERE / (sys.argv[1] if len(sys.argv) > 1 else "main.pdf")
    text = "\n".join((p.extract_text() or "") for p in PdfReader(str(target)).pages)

    start = text.find("Introduction")
    stop = text.rfind("References")
    body = text[start:stop if stop > start else None]
    refs = text[stop:] if stop > start else ""

    em, en, qq = body.count("—"), body.count("–"), text.count("??")
    rob = text.lower().count("robust")
    stray = len(re.findall(r"(?<!\d)–|–(?!\d)", refs))
    words = len(re.findall(r"\S+", body))

    print(f"{target.name}: body em-dash {em}, body en-dash {en}, 'robust' {rob}, "
          f"undefined refs {qq}")
    print(f"reference list: en dashes outside a page range {stray}")
    print(f"body word count (introduction to references): {words}")

    # ---- identifiers typeset as mathematics in table cells
    # A source identifier that reaches a table keeps its underscore, and inside math the
    # underscore becomes a subscript, so "tau_k" prints as a variable rather than as the
    # words the paper uses. Both forms are caught: the underscore inside math in the
    # generated table source, and the literal underscore surviving into the PDF.
    math_underscore = []
    for tex in sorted((HERE / "tables").glob("*.tex")):
        src = tex.read_text(encoding="utf-8")
        for seg in re.findall(r"(?<!\\)\$([^$]*)\$", src):
            if "_" in seg.replace("\\_", ""):
                math_underscore.append(f"{tex.name}: ${seg[:40]}$")
    pdf_underscore = sorted(set(re.findall(r"\b[a-z]{2,}_[a-z0-9]{2,}\b", text)))
    print(f"identifiers in math in table cells: {math_underscore or 'none'}")
    print(f"underscore identifiers surviving into the PDF: {pdf_underscore or 'none'}")

    fails = []
    if math_underscore:
        fails.append(f"underscore inside math in a table cell: {math_underscore[:4]}")
    if pdf_underscore:
        fails.append(f"raw identifiers printed in the PDF: {pdf_underscore[:6]}")
    if em or en:
        fails.append("dash rule violated in the body")
    if stray:
        fails.append("en dash outside a page range in the reference list")
    if rob:
        fails.append("the word robust appears in the PDF")
    if qq:
        fails.append("undefined references in the PDF")
    if fails:
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("PDF-LEVEL GATES PASS")


if __name__ == "__main__":
    main()
