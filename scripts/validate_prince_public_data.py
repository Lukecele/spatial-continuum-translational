#!/usr/bin/env python3
"""Validate the public de-identified PRINCE clinical dataset."""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


REQUIRED_COLUMNS = {
    "Deidentified.ID",
    "Arm",
    "Arm Description",
    "Received Nivolumab",
    "Efficacy Population Flag",
    "clinical.observation.pfs",
    "clinical.observation.pfs.event",
    "clinical.observation.os",
    "clinical.observation.os.event",
    "Best Overall Response",
}
EXPECTED_ARMS = {"A1", "B2", "C2"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clinical_csv", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    with args.clinical_csv.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise SystemExit(f"Missing required columns: {sorted(missing)}")
        rows = list(reader)

    ids = [row["Deidentified.ID"].strip() for row in rows]
    arms = Counter(row["Arm"].strip() for row in rows)
    response = Counter(row["Best Overall Response"].strip() for row in rows)
    pfs_events = Counter(row["clinical.observation.pfs.event"].strip() for row in rows)
    os_events = Counter(row["clinical.observation.os.event"].strip() for row in rows)

    errors = []
    if not rows:
        errors.append("clinical file is empty")
    if len(ids) != len(set(ids)):
        errors.append("duplicate de-identified patient IDs")
    if set(arms) != EXPECTED_ARMS:
        errors.append(f"unexpected treatment arms: {sorted(arms)}")
    for row in rows:
        if not row["clinical.observation.pfs"].strip():
            errors.append("missing PFS time")
            break
        if not row["clinical.observation.os"].strip():
            errors.append("missing OS time")
            break

    report = {
        "source": "ParkerICI/prince-trial-data",
        "clinical_file": str(args.clinical_csv),
        "patients": len(rows),
        "unique_patient_ids": len(set(ids)),
        "arms": dict(arms),
        "pfs_records": sum(bool(row["clinical.observation.pfs"].strip()) for row in rows),
        "pfs_events": dict(pfs_events),
        "os_records": sum(bool(row["clinical.observation.os"].strip()) for row in rows),
        "os_events": dict(os_events),
        "response_counts": dict(response),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
        "interpretation": "Public patient-level PRINCE clinical metadata are available for arm-specific descriptive analysis; score validation remains blocked until a pancreas-specific score is frozen.",
    }

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
