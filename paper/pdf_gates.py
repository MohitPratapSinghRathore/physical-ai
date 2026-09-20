"""Playbook section 8 gates that need the built PDF, plus the body word count.

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

    em, en, qq = text.count("—"), text.count("–"), text.count("??")
    rob = text.lower().count("robust")
    print(f"{target.name}: em-dash {em}, en-dash {en}, 'robust' {rob}, undefined refs {qq}")

    body = text
    start = body.find("Introduction")
    stop = body.rfind("References")
    words = len(re.findall(r"\S+", body[start:stop if stop > start else None]))
    print(f"body word count (introduction to references): {words}")

    fails = []
    if em or en:
        fails.append("dash rule violated in the PDF")
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
