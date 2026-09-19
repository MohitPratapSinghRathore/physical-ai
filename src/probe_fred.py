"""Probe candidate FRED series IDs and print authoritative title/units. Selection aid, not a build step."""
import re, sys, requests
def field(h, label):
    m = re.search(rf'{label}</th>\s*<td>(.*?)</td>', h, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else "?"
for sid in sys.argv[1:]:
    r = requests.get(f"https://fred.stlouisfed.org/data/{sid}.txt", timeout=60)
    if r.status_code != 200:
        print(f"{sid:20s} HTTP {r.status_code}"); continue
    t = re.search(r"<title>Table Data - (.*?) \| FRED", r.text, re.S)
    t = re.sub(r"\s+"," ",t.group(1)).strip() if t else "?"
    print(f"{sid:20s} | {field(r.text,'Units')[:22]:22s} | {field(r.text,'Frequency')[:22]:22s} | {t[:85]}")
