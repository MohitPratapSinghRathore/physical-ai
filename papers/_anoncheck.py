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


def main():
    pdf = pathlib.Path("main_anon.pdf")
    if not pdf.exists():
        print("main_anon.pdf not built")
        return 1
    out = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True)
    t = out.stdout.decode("utf-8", errors="replace")
    hits = [n for n in NEEDLES if n.lower() in t.lower()]
    print(f"anon PDF: {pdf.resolve().parent.name}/main_anon.pdf")
    if hits:
        print("IDENTITY LEAKS:", ", ".join(hits))
        return 1
    print(f"checked {len(NEEDLES)} identifying strings: 0 leaks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
