"""Playbook section 8: anonymous build must contain zero identity leaks.

Run from a paper directory:  python ../_anoncheck.py
Greps the blind PDF for every author surname, affiliation, email and repo URL.
"""
import pathlib
import subprocess
import sys

NEEDLES = [
    "Rathore", "Mohit", "Kalsi", "Gunveer", "Meduri", "Sriharsha",
    "Mandal", "Pratap", "Oviqo", "Shillong", "Indian Institute of Management",
    "Andhra", "github.com", "MohitPratapSinghRathore", "physical-ai",
    "gunveerkalsi", "@gmail", "Disclosure statement", "Funding.",
]


def text_of(path):
    """Plain text of a built PDF or DOCX."""
    if path.suffix == ".pdf":
        out = subprocess.run(["pdftotext", str(path), "-"], capture_output=True)
    else:
        out = subprocess.run(["pandoc", str(path), "-t", "plain"], capture_output=True)
    return out.stdout.decode("utf-8", errors="replace")


def main():
    # Both blind deliverables must be checked. The DOCX is built from its own
    # .bbl; reading the author build's would put real names into the anonymous
    # reference list, which is exactly the leak this catches.
    targets = [pathlib.Path("main_anon.pdf")]
    targets += sorted(pathlib.Path(".").glob("*_anon.docx"))
    rc = 0
    for p in targets:
        if not p.exists():
            print(f"{p.name}: NOT BUILT")
            rc = 1
            continue
        t = text_of(p)
        hits = [n for n in NEEDLES if n.lower() in t.lower()]
        if hits:
            print(f"{p.name}: IDENTITY LEAKS: {', '.join(hits)}")
            rc = 1
        else:
            print(f"{p.name}: checked {len(NEEDLES)} identifying strings, 0 leaks")
    return rc


if __name__ == "__main__":
    sys.exit(main())
