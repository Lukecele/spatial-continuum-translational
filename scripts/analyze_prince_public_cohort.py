#!/usr/bin/env python3
"""Build descriptive arm-level summaries from the public PRINCE clinical file."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from statistics import median


ARM_LABELS = {
    "A1": "gemcitabine_nab_paclitaxel_nivolumab",
    "B2": "gemcitabine_nab_paclitaxel_sotigalimab",
    "C2": "gemcitabine_nab_paclitaxel_nivolumab_sotigalimab",
}
RESPONSE_VALUES = {"COMPLETE RESPONSE", "PARTIAL RESPONSE"}


def number(row: dict[str, str], column: str) -> float | None:
    value = row.get(column, "").strip()
    try:
        return float(value)
    except ValueError:
        return None


def summarize(rows: list[dict[str, str]]) -> dict:
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(row["Arm"].strip(), []).append(row)

    arms = {}
    for arm, arm_rows in sorted(groups.items()):
        pfs_times = [number(row, "clinical.observation.pfs") for row in arm_rows]
        os_times = [number(row, "clinical.observation.os") for row in arm_rows]
        pfs_times = [value for value in pfs_times if value is not None]
        os_times = [value for value in os_times if value is not None]
        responses = Counter(row.get("Best Overall Response", "").strip() for row in arm_rows)
        evaluable_responses = sum(value for key, value in responses.items() if key not in {"NA", "NOT EVALUABLE", ""})
        objective_responses = sum(value for key, value in responses.items() if key in RESPONSE_VALUES)
        pfs_events = sum(row.get("clinical.observation.pfs.event", "").strip().upper() == "TRUE" for row in arm_rows)
        os_events = sum(row.get("clinical.observation.os.event", "").strip().upper() == "TRUE" for row in arm_rows)
        arms[arm] = {
            "label": ARM_LABELS.get(arm, "unknown"),
            "patients": len(arm_rows),
            "pfs_records": len(pfs_times),
            "pfs_events": pfs_events,
            "pfs_event_fraction": pfs_events / len(arm_rows) if arm_rows else None,
            "pfs_time_median_days_observed": median(pfs_times) if pfs_times else None,
            "os_records": len(os_times),
            "os_events": os_events,
            "os_event_fraction": os_events / len(arm_rows) if arm_rows else None,
            "os_time_median_days_observed": median(os_times) if os_times else None,
            "response_counts": dict(responses),
            "response_evaluable_patients": evaluable_responses,
            "objective_responses": objective_responses,
            "objective_response_fraction_evaluable": objective_responses / evaluable_responses if evaluable_responses else None,
        }

    return {
        "cohort": "PRINCE",
        "source": "ParkerICI/prince-trial-data",
        "patients": len(rows),
        "arms": arms,
        "analysis_type": "descriptive_arm_level",
        "limitations": [
            "observed-time medians are not Kaplan-Meier medians",
            "no causal comparison between arms is performed",
            "no score is fitted or validated",
            "arm sizes and treatment assignment reflect the trial design",
        ],
        "interpretation": "Public PRINCE data support reproducible arm-specific descriptive analysis; pancreas score validation remains pending a frozen score.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clinical_csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with args.clinical_csv.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    report = summarize(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
