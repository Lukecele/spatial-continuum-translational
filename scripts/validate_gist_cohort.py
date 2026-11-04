#!/usr/bin/env python3
"""Run an exploratory patient-level GIST recurrence validation."""

import json
import math
from collections import defaultdict
from pathlib import Path

import pandas as pd
from lifelines import CoxPHFitter

ROOT = Path("data/raw/cbioportal/gist_msk_2023")
OUTPUT = Path("data/derived/gist_validation_summary.json")


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main():
    clinical = json.loads((ROOT / "clinical_patient.json").read_text())
    mutations = json.loads((ROOT / "mutations_kit_pdgfra.json").read_text())
    patients = defaultdict(dict)
    for row in clinical:
        patients[row["patientId"]][row["clinicalAttributeId"]] = row["value"]
    for row in mutations:
        patients[row["patientId"]][f"{row['gene']}_mutated"] = 1

    rows = []
    for patient, values in patients.items():
        duration = number(values.get("RFS_MONTHS"))
        status = values.get("RFS_STATUS")
        mitoses = number(values.get("FIRST_TREATMENT_MIOTIC_RATE_50HPF"))
        size = number(values.get("FIRST_TREATMENT_TUMOR_SIZE_CM"))
        if duration is None or status not in {"0:No recurrence", "1:Recurrence"} or mitoses is None or size is None:
            continue
        rows.append({
            "duration_months": duration,
            "event": int(status.startswith("1:")),
            "mitoses_per_50_hpf": mitoses,
            "tumor_size_cm": size,
            "kit_mutated": int(values.get("KIT_mutated", 0)),
            "pdgfra_mutated": int(values.get("PDGFRA_mutated", 0)),
            "metastatic_at_diagnosis": int(values.get("STAGE_AT_DIAGNOSIS") == "Metastatic"),
            "adjuvant_therapy": int(values.get("OS_ADJUVANTTHERAPY") == "Yes"),
        })

    frame = pd.DataFrame(rows)
    covariates = ["mitoses_per_50_hpf", "tumor_size_cm", "kit_mutated", "pdgfra_mutated", "metastatic_at_diagnosis", "adjuvant_therapy"]
    model = CoxPHFitter(penalizer=0.1).fit(frame[["duration_months", "event", *covariates]], duration_col="duration_months", event_col="event")
    coefficients = {}
    for name in covariates:
        coefficients[name] = {
            "hazard_ratio": float(model.hazard_ratios_[name]),
            "ci_lower": math.exp(float(model.confidence_intervals_.loc[name].iloc[0])),
            "ci_upper": math.exp(float(model.confidence_intervals_.loc[name].iloc[1])),
            "p_value_exploratory": float(model.summary.loc[name, "p"]),
        }

    report = {
        "cohort": "gist_msk_2023",
        "complete_patients": len(frame),
        "events": int(frame["event"].sum()),
        "covariates": covariates,
        "coefficients": coefficients,
        "interpretation": "Exploratory patient-level validation of observed GIST features; not a calibrated clinical risk model.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
