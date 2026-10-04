"""Playbook section 7 helper: body word count.

Counts the main text from the Introduction heading to the start of the
Declarations, which excludes the abstract, references, appendices and the
tables and figures that sit after them. Run from a paper directory:

    python ../_count.py
"""
import pathlib
import re
import subprocess
import sys


def main():
    pdf = pathlib.Path("main.pdf")
    if not pdf.exists():
        print("main.pdf not built")
        return 1
    raw = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True).stdout
    t = raw.decode("utf-8", errors="replace")

    start = t.find("1 Introduction")
    end = t.find("Declarations", start)
    if end == -1:
        end = t.find("References", start)
    body = t[start:end]

    # strip page numbers sitting on their own line
    body = re.sub(r"\n\d{1,3}\n", "\n", body)
    words = len(body.split())
    print(f"body words (Introduction to Declarations): {words:,}")
    print(f"rounded for the title page: approximately {round(words, -2):,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
