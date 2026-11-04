#!/usr/bin/env python3
"""Run exploratory TCGA-LUAD DFS Kaplan-Meier and Cox analyses."""

import json
import math
import re
from pathlib import Path

from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import proportional_hazard_test

ROOT = Path("data/raw/cbioportal/luad_tcga_pan_can_atlas_2018")
OUTPUT = Path("data/derived/tcga_luad_survival_summary.json")
GENES = ("EGFR", "TP53", "RB1")


def clinical_table() -> dict[str, dict[str, str]]:
    rows = json.loads((ROOT / "clinical_patient.json").read_text())
    patients: dict[str, dict[str, str]] = {}
    for row in rows:
        patients.setdefault(row["patientId"], {})[row["clinicalAttributeId"]] = row["value"]
    return patients


def mutation_flags() -> dict[str, set[str]]:
    rows = json.loads((ROOT / "mutations_egfr_tp53_rb1.json").read_text())
    return {gene: {row["patientId"] for row in rows if row["gene"] == gene} for gene in GENES}


def parse_number(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def build_rows() -> list[dict[str, float | int]]:
    patients = clinical_table()
    mutated = mutation_flags()
    rows = []
    for patient_id, values in patients.items():
        duration = parse_number(values.get("DFS_MONTHS"))
        status = values.get("DFS_STATUS")
        if duration is None or status not in {"0:DiseaseFree", "1:Recurred/Progressed"}:
            continue
        row: dict[str, float | int] = {
            "duration_months": duration,
            "event": int(status.startswith("1:")),
        }
        for gene in GENES:
            row[f"{gene.lower()}_mutated"] = int(patient_id in mutated[gene])
        age = parse_number(values.get("AGE"))
        if age is not None:
            row["age"] = age
        stage = values.get("AJCC_PATHOLOGIC_TUMOR_STAGE", "")
        match = re.search(r"STAGE\s+(I{1,3}|IV)", stage)
        if match:
            row["stage_advanced"] = int(match.group(1) in {"II", "III", "IV"})
        rows.append(row)
    return rows


def main() -> None:
    import pandas as pd

    frame = pd.DataFrame(build_rows())
    summary: dict[str, object] = {
        "cohort": "luad_tcga_pan_can_atlas_2018",
        "endpoint": "DFS_MONTHS / DFS_STATUS",
        "n_complete": int(len(frame)),
        "events": int(frame["event"].sum()),
        "genes": {},
    }

    for gene in GENES:
        column = f"{gene.lower()}_mutated"
        groups = {}
        for label, group in frame.groupby(column):
            fitter = KaplanMeierFitter().fit(group["duration_months"], group["event"])
            groups["mutated" if label else "not_observed"] = {
                "n": int(len(group)),
                "events": int(group["event"].sum()),
                "median_dfs_months": None if fitter.median_survival_time_ == float("inf") else float(fitter.median_survival_time_),
            }
        summary["genes"][gene] = groups

    covariates = [f"{gene.lower()}_mutated" for gene in GENES]
    if "age" in frame.columns:
        covariates.append("age")
    if "stage_advanced" in frame.columns:
        covariates.append("stage_advanced")
    cox_frame = frame[["duration_months", "event", *covariates]].dropna()
    model = CoxPHFitter(penalizer=0.1).fit(
        cox_frame, duration_col="duration_months", event_col="event"
    )
    ph_test = proportional_hazard_test(model, cox_frame, time_transform="rank")
    summary["cox"] = {
        "n_complete": int(len(cox_frame)),
        "events": int(cox_frame["event"].sum()),
        "penalizer": 0.1,
        "coefficients": {
            name: {
                "hazard_ratio": float(model.hazard_ratios_[name]),
                "ci_lower": math.exp(float(model.confidence_intervals_.loc[name].iloc[0])),
                "ci_upper": math.exp(float(model.confidence_intervals_.loc[name].iloc[1])),
                "p_value": float(model.summary.loc[name, "p"]),
            }
            for name in covariates
        },
        "proportional_hazards_p_values": {
            name: float(ph_test.summary.loc[name, "p"])
            for name in covariates
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
