#!/usr/bin/env python3
"""Audit treatment-state metadata for the primary resistance cohorts."""

import csv
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

FILES = {
    "GSE342824_xenium": Path("/tmp/treatment-cohorts/GSE342824_xenium_cell_metadata.tsv.gz"),
    "GSE292469_snRNA": Path("/tmp/treatment-cohorts/GSE292469_cell_metadata.tsv.gz"),
}
OUTPUT = Path("data/derived/treatment_cohort_metadata_audit.json")


def audit(path: Path) -> dict:
    rows = 0
    unique = defaultdict(set)
    counts = defaultdict(Counter)
    with gzip.open(path, "rt", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = reader.fieldnames or []
        for row in reader:
            rows += 1
            for field in ("patient_id", "sample_id", "timepoint", "time_point", "core_id", "cell_type_coarse", "cell_type", "cell_type_very_coarse", "EGFR.mut", "mut_pos_cell", "is_tumor_cell", "pd_like_tn", "pd_axiscell_type_pdlike_simple", "scDblFinder.class"):
                if field in row and row[field] != "":
                    unique[field].add(row[field])
                    counts[field][row[field]] += 1
    return {
        "file": str(path),
        "rows": rows,
        "fields": fields,
        "unique_values": {field: sorted(values) for field, values in unique.items()},
        "counts": {field: dict(counter) for field, counter in counts.items()},
    }


def main() -> None:
    report = {name: audit(path) for name, path in FILES.items()}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({name: {"rows": value["rows"], "fields": len(value["fields"])} for name, value in report.items()}, indent=2))


if __name__ == "__main__":
    main()
