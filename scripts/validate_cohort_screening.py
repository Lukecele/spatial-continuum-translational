#!/usr/bin/env python3
"""Validate the mandatory cohort-screening register."""

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREENING = ROOT / "data" / "cohort_screening.tsv"

REQUIRED_COLUMNS = {
    "candidate_id",
    "accession_or_trial",
    "tumor",
    "treatment",
    "endpoint",
    "unit",
    "patients",
    "events",
    "covariates",
    "independence",
    "decision_class",
    "reason_or_next_step",
    "source_checked",
}
ALLOWED_CLASSES = {
    "CURRENT_MODEL_COHORT",
    "FULL_VALIDATION",
    "PHENOTYPE_REPLICATION",
    "BIOLOGICAL_CONTEXT",
    "REJECTED",
}


def main() -> int:
    with SCREENING.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        columns = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - columns
        if missing_columns:
            print(f"FAIL: missing screening columns: {sorted(missing_columns)}")
            return 1

        rows = list(reader)

    errors: list[str] = []
    seen: set[str] = set()
    for number, row in enumerate(rows, start=2):
        candidate_id = row["candidate_id"].strip()
        if not candidate_id:
            errors.append(f"line {number}: empty candidate_id")
            continue
        if candidate_id in seen:
            errors.append(f"line {number}: duplicate candidate_id {candidate_id}")
        seen.add(candidate_id)

        for column in REQUIRED_COLUMNS - {"events"}:
            if not row[column].strip():
                errors.append(f"line {number}: empty {column}")

        if row["decision_class"] not in ALLOWED_CLASSES:
            errors.append(f"line {number}: invalid decision_class {row['decision_class']}")
        if row["unit"].strip().lower() not in {"patient", "patient/sample"}:
            errors.append(f"line {number}: non-patient replication unit {row['unit']}")
        if row["patients"].strip().upper() == "NA":
            errors.append(f"line {number}: patients must be numeric")
        else:
            try:
                if int(row["patients"]) <= 0:
                    errors.append(f"line {number}: patients must be positive")
            except ValueError:
                errors.append(f"line {number}: invalid patients value {row['patients']}")
        if row["decision_class"] == "FULL_VALIDATION":
            if row["independence"].strip().lower() != "independent":
                errors.append(f"line {number}: FULL_VALIDATION requires independence=independent")
            if row["covariates"].strip().lower() in {"na", "unknown", ""}:
                errors.append(f"line {number}: FULL_VALIDATION requires documented covariates")

    if errors:
        print("FAIL: cohort screening register is invalid")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {len(rows)} cohort screening records validated")
    print("No incomplete or unclassified cohort record detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
