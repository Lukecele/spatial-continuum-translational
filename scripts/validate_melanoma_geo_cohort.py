#!/usr/bin/env python3
"""Validate GSE99898 melanoma treatment-state metadata from a GEO SOFT file."""

from __future__ import annotations

import argparse
import gzip
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


SAMPLE_TITLE = re.compile(r"Patient\s+(?P<patient>\d+)\s+(?P<state>PRE|EDT|PROG)\s+(?P<treatment>.+)", re.IGNORECASE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("soft_gz", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    records = []
    current = None
    with gzip.open(args.soft_gz, "rt", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                current = {"accession": line.split("=", 1)[1].strip()}
                records.append(current)
            elif current and line.startswith("!Sample_title = "):
                title = line.split("=", 1)[1].strip()
                current["title"] = title
                match = SAMPLE_TITLE.match(title)
                if match:
                    current.update(match.groupdict())
            elif current and line.startswith("!Sample_characteristics_ch1 = "):
                value = line.split("=", 1)[1].strip()
                if ":" in value:
                    key, item = value.split(":", 1)
                    current.setdefault("characteristics", {})[key.strip().lower()] = item.strip()

    usable = [record for record in records if record.get("patient") and record.get("state") and record.get("treatment")]
    patient_states = defaultdict(set)
    treatments = Counter()
    states = Counter()
    for record in usable:
        patient_states[record["patient"]].add(record["state"].upper())
        treatments[record["treatment"].lower()] += 1
        states[record["state"].upper()] += 1

    errors = []
    if len(records) != 38:
        errors.append(f"expected 38 samples from series summary, found {len(records)}")
    if len(patient_states) != 17:
        errors.append(f"expected 17 patients from series summary, found {len(patient_states)}")
    if not any("trametinib" in treatment and ("dabrafenib" in treatment or "dabtrafenib" in treatment) for treatment in treatments):
        errors.append("no dabrafenib plus trametinib treatment label found")
    if not any("dabrafenib" in treatment or "vemurafenib" in treatment for treatment in treatments):
        errors.append("no BRAF inhibitor treatment label found")

    report = {
        "cohort": "GSE99898",
        "samples": len(records),
        "usable_sample_records": len(usable),
        "patients": len(patient_states),
        "state_counts": dict(states),
        "treatment_counts": dict(treatments),
        "patients_with_multiple_states": sum(len(states_seen) > 1 for states_seen in patient_states.values()),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "interpretation": "Public melanoma treatment-state phenotype replication; no melanoma score is fitted or validated.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
