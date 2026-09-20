"""Word count of the manuscript, by section file and in total.

Counts prose only: result macros collapse to one token, LaTeX commands and
environment lines are dropped, table files are not counted.

Run:  python paper/wordcount.py
"""
import pathlib
import re

HERE = pathlib.Path(__file__).parent


def words(tex):
    t = re.sub(r"%.*", "", tex)
    t = re.sub(r"\\result\{[A-Za-z]+\}", "00", t)
    t = re.sub(r"\\(begin|end|input|label|ref|eqref|cite[tp])\{[^}]*\}", " ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = re.sub(r"[{}&\\$~^_]", " ", t)
    return len(re.findall(r"[^\s]+", t))


def main():
    total = 0
    rows = []
    main_tex = (HERE / "main.tex").read_text(encoding="utf-8")
    front = main_tex.split("\\input{sections")[0]
    abstract = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", front, re.S)
    n = words(abstract.group(1))
    rows.append(("abstract", n))
    for f in sorted((HERE / "sections").glob("*.tex")):
        n = words(f.read_text(encoding="utf-8"))
        rows.append((f.stem, n))
        total += n
    appendix = main_tex.split("\\appendix")
    if len(appendix) > 1:
        body = appendix[1].split("\\bibliographystyle")[0]
        rows.append(("appendix (in main.tex)", words(body)))
    width = max(len(r[0]) for r in rows)
    for name, n in rows:
        print(f"{name.ljust(width)}  {n:>6,}")
    print(f"{'MAIN TEXT, sections only'.ljust(width)}  {total:>6,}")


if __name__ == "__main__":
    main()
