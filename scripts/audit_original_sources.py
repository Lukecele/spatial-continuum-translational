#!/usr/bin/env python3
"""Audit PMID identifiers in the original repository."""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PMID_PATTERN = re.compile(r"(?:PMID\s*[: ]\s*|pubmed\.ncbi\.nlm\.nih\.gov/)(\d{7,8})", re.I)


def collect_pmids(root: Path) -> dict[str, list[str]]:
    locations = {}
    for path in root.rglob("*"):
        if path.suffix.lower() not in {".md", ".txt", ".cff"}:
            continue
        try:
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        for pmid in PMID_PATTERN.findall(text):
            locations.setdefault(pmid, []).append(str(path.relative_to(root)))
    return locations


def fetch_summaries(pmids: list[str]) -> dict:
    query = urlencode({"db": "pubmed", "id": ",".join(pmids), "retmode": "json"})
    request = Request(
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?{query}",
        headers={"User-Agent": "spatial-continuum-translational/0.1"},
    )
    with urlopen(request, timeout=60) as response:
        return json.load(response).get("result", {})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/derived/original_source_audit.json"))
    args = parser.parse_args()

    locations = collect_pmids(args.root)
    result = fetch_summaries(sorted(locations))
    records = []
    unresolved = []
    for pmid in sorted(locations):
        record = result.get(pmid)
        if not record or record.get("error"):
            unresolved.append(pmid)
            continue
        records.append(
            {
                "pmid": pmid,
                "title": record.get("title"),
                "journal": record.get("fulljournalname"),
                "pubdate": record.get("pubdate"),
                "source_files": locations[pmid],
            }
        )
    report = {
        "source_root": str(args.root),
        "unique_pmids": len(locations),
        "resolved_records": len(records),
        "unresolved_pmids": unresolved,
        "records": records,
        "interpretation": "This audits identifier resolution only; it does not verify the scientific claims made around each citation.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("unique_pmids", "resolved_records", "unresolved_pmids")}, indent=2))


if __name__ == "__main__":
    main()
