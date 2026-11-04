#!/usr/bin/env python3
"""Run internal cross-validation and simple calibration checks for the GIST model."""

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from sklearn.model_selection import KFold

CLINICAL = Path("data/raw/cbioportal/gist_msk_2023/clinical_patient.json")
MUTATIONS = Path("data/raw/cbioportal/gist_msk_2023/mutations_kit_pdgfra.json")
OUTPUT = Path("data/derived/gist_internal_validation.json")
COVARIATES = ["mitoses_per_50_hpf", "tumor_size_cm", "kit_mutated", "pdgfra_mutated", "metastatic_at_diagnosis", "adjuvant_therapy"]


def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_frame():
    clinical = json.loads(CLINICAL.read_text())
    mutations = json.loads(MUTATIONS.read_text())
    patients = defaultdict(dict)
    for row in clinical:
        patients[row["patientId"]][row["clinicalAttributeId"]] = row["value"]
    for row in mutations:
        patients[row["patientId"]][f"{row['gene']}_mutated"] = 1
    rows = []
    for values in patients.values():
        duration = number(values.get("RFS_MONTHS"))
        mitoses = number(values.get("FIRST_TREATMENT_MIOTIC_RATE_50HPF"))
        size = number(values.get("FIRST_TREATMENT_TUMOR_SIZE_CM"))
        if duration is None or mitoses is None or size is None or values.get("RFS_STATUS") not in {"0:No recurrence", "1:Recurrence"}:
            continue
        rows.append({
            "duration_months": duration,
            "event": int(values["RFS_STATUS"].startswith("1:")),
            "mitoses_per_50_hpf": mitoses,
            "tumor_size_cm": size,
            "kit_mutated": int(values.get("KIT_mutated", 0)),
            "pdgfra_mutated": int(values.get("PDGFRA_mutated", 0)),
            "metastatic_at_diagnosis": int(values.get("STAGE_AT_DIAGNOSIS") == "Metastatic"),
            "adjuvant_therapy": int(values.get("OS_ADJUVANTTHERAPY") == "Yes"),
        })
    return pd.DataFrame(rows)


def main():
    frame = load_frame()
    features = frame[COVARIATES]
    splits = KFold(n_splits=5, shuffle=True, random_state=42)
    predictions = np.full(len(frame), np.nan)
    fold_c_indices = []
    for train_index, test_index in splits.split(features):
        train = frame.iloc[train_index][["duration_months", "event", *COVARIATES]]
        test = frame.iloc[test_index][["duration_months", "event", *COVARIATES]]
        model = CoxPHFitter(penalizer=0.1).fit(train, duration_col="duration_months", event_col="event")
        risk = model.predict_partial_hazard(test[COVARIATES]).to_numpy().ravel()
        predictions[test_index] = risk
        fold_c_indices.append(float(concordance_index(test["duration_months"], -risk, test["event"])))

    observed = frame.copy()
    observed["risk"] = predictions
    observed["risk_tertile"] = pd.qcut(observed["risk"], 3, labels=["low", "middle", "high"])
    calibration = observed.groupby("risk_tertile", observed=False).agg(
        patients=("event", "size"),
        events=("event", "sum"),
        event_rate=("event", "mean"),
        mean_risk=("risk", "mean"),
    ).reset_index()
    report = {
        "cohort": "gist_msk_2023",
        "patients": int(len(frame)),
        "events": int(frame["event"].sum()),
        "covariates": COVARIATES,
        "five_fold_c_index": fold_c_indices,
        "mean_c_index": float(np.mean(fold_c_indices)),
        "sd_c_index": float(np.std(fold_c_indices, ddof=1)),
        "calibration_by_risk_tertile": calibration.to_dict(orient="records"),
        "external_validation": "not_available",
        "interpretation": "Internal validation only; no calibrated clinical risk model or treatment rule is established.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, default=float) + "\n")
    print(json.dumps(report, indent=2, default=float))


if __name__ == "__main__":
    main()
