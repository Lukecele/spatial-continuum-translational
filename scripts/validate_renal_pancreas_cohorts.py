#!/usr/bin/env python3
"""Summarize renal and pancreatic trial response/PFS metadata separately."""

import json
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path("data/raw/cbioportal/renal_pancreas")
OUTPUT = Path("data/derived/renal_pancreas_validation_summary.json")

STUDIES = {
    "rcc_iatlas_immotion150_2018": {"label": "Immotion150", "response": "RESPONDER", "progression": "PROGRESSION", "time": "PFS_MONTHS", "status": "PFS_STATUS", "treatment": "ICI_RX"},
    "paad_iatlas_prince_2022": {"label": "PRINCE", "response": "RESPONDER", "progression": "PROGRESSION", "time": "PFS_MONTHS", "status": "PFS_STATUS", "treatment": "ICI_RX"},
}


def main():
    report = {}
    for study, config in STUDIES.items():
        rows = json.loads((ROOT / f"{study}_clinical_patient.json").read_text())
        patients = defaultdict(dict)
        for row in rows:
            patients[row["patientId"]][row["clinicalAttributeId"]] = row["value"]
        response = Counter(values.get(config["response"]) for values in patients.values() if values.get(config["response"]))
        progression = Counter(values.get(config["progression"]) for values in patients.values() if values.get(config["progression"]))
        treatments = Counter(values.get(config["treatment"]) for values in patients.values() if values.get(config["treatment"]))
        pfs_patients = [values for values in patients.values() if values.get(config["time"]) and values.get(config["status"])]
        report[study] = {
            "label": config["label"],
            "patients": len(patients),
            "patients_with_pfs": len(pfs_patients),
            "response_counts": dict(response),
            "progression_counts": dict(progression),
            "treatment_counts": dict(treatments),
            "interpretation": "Cohort-specific exploratory treatment-response validation; no cross-tumor pooling.",
        }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
