"""Fetch the FDIC failed-bank list. data/raw is gitignored, so this script is the
reproducible record of where the outcome variable comes from. 586 resolutions 2000-2023."""
import json, pathlib, urllib.request

OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "raw" / "fdic_failures"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, off = [], 0
    while True:
        u = ("https://banks.data.fdic.gov/api/failures"
             "?filters=FAILYR%3A%5B2000%20TO%202023%5D"
             "&fields=NAME,CERT,FAILDATE,FAILYR,QBFASSET,COST,RESTYPE,RESTYPE1,CITYST"
             f"&limit=1000&offset={off}&format=json")
        d = json.loads(urllib.request.urlopen(u, timeout=60).read())
        b = [r["data"] for r in d.get("data", [])]
        if not b:
            break
        rows += b
        off += 1000
        if len(b) < 1000:
            break
    (OUT / "failures.json").write_text(json.dumps(rows, indent=1))
    print(f"wrote {len(rows)} failures to {OUT/'failures.json'}")


if __name__ == "__main__":
    main()
