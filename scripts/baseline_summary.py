#!/usr/bin/env python3
"""Build a descriptive patient-level mutation/event summary."""

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path("data/raw/cbioportal")
OUTPUT = Path("data/derived/baseline_event_summary.tsv")
GENES = ("EGFR", "TP53", "RB1")
ENDPOINTS = {
    "luad_tcga_pan_can_atlas_2018": "DFS_STATUS",
}


def load_rows(path: Path) -> list[dict[str, str]]:
    return json.loads(path.read_text())


def event_value(study_id: str, value: str) -> int | None:
    if study_id == "luad_tcga_pan_can_atlas_2018":
        if value == "1:Recurred/Progressed":
            return 1
        if value == "0:DiseaseFree":
            return 0
    return None


def summarize(study_dir: Path) -> list[dict[str, str]]:
    study_id = study_dir.name
    clinical = load_rows(study_dir / "clinical_patient.json")
    mutations = load_rows(study_dir / "mutations_egfr_tp53_rb1.json")
    patients: dict[str, dict[str, str | int]] = defaultdict(dict)

    endpoint_name = ENDPOINTS[study_id]
    for row in clinical:
        patient = patients[row["patientId"]]
        if row["clinicalAttributeId"] == endpoint_name:
            event = event_value(study_id, row["value"])
            if event is not None:
                patient["event"] = event
    for row in mutations:
        patients[row["patientId"]][row["gene"]] = 1

    rows = []
    for gene in GENES:
        for mutated in (0, 1):
            eligible = [
                values
                for values in patients.values()
                if "event" in values and int(values.get(gene, 0)) == mutated
            ]
            events = sum(int(values["event"]) for values in eligible)
            rows.append(
                {
                    "study_id": study_id,
                    "endpoint": endpoint_name,
                    "gene": gene,
                    "mutation_group": "mutated" if mutated else "not_observed",
                    "patients": str(len(eligible)),
                    "events": str(events),
                    "event_rate": f"{events / len(eligible):.6f}" if eligible else "",
                }
            )
    return rows


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for study_dir in sorted(ROOT.iterdir()):
        if study_dir.is_dir() and study_dir.name in ENDPOINTS:
            rows.extend(summarize(study_dir))
    with OUTPUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
