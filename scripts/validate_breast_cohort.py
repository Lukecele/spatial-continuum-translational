#!/usr/bin/env python3
"""Run exploratory patient-level breast treatment-response validation."""

import json
from collections import defaultdict
from pathlib import Path

from scipy.stats import fisher_exact

ROOT = Path("data/raw/cbioportal/brca_mskcc_2019")
OUTPUT = Path("data/derived/breast_validation_summary.json")


def main():
    clinical = json.loads((ROOT / "clinical_patient.json").read_text())
    mutations = json.loads((ROOT / "mutations_pik3ca_esr1_ccne1_rb1.json").read_text())
    patients = defaultdict(dict)
    for row in clinical:
        patients[row["patientId"]][row["clinicalAttributeId"]] = row["value"]
    for row in mutations:
        patients[row["patientId"]][f"{row['gene']}_mutated"] = 1
    rows = []
    for patient, values in patients.items():
        response = values.get("TREATMENT_BEST_RESPONSE") or values.get("BEST_RESPONSE_TO_THERAPY")
        if response is None:
            continue
        rows.append({
            "patient_id": patient,
            "therapy": values.get("THERAPY"),
            "response": response,
            "progressive": response in {"PD", "Progressive Disease"},
            "pik3ca_mutated": bool(values.get("PIK3CA_mutated")),
            "esr1_mutated": bool(values.get("ESR1_mutated")),
            "ccne1_mutated": bool(values.get("CCNE1_mutated")),
            "rb1_mutated": bool(values.get("RB1_mutated")),
        })
    associations = {}
    for gene in ("pik3ca_mutated", "esr1_mutated", "ccne1_mutated", "rb1_mutated"):
        table = [[0, 0], [0, 0]]
        for row in rows:
            table[int(row[gene])][int(row["progressive"])] += 1
        odds, p = fisher_exact(table)
        associations[gene] = {"table_mutation_by_progression": table, "odds_ratio": float(odds), "p_value_exploratory": float(p)}
    report = {
        "cohort": "brca_mskcc_2019",
        "patients_with_response": len(rows),
        "progressive_cases": sum(row["progressive"] for row in rows),
        "therapy_counts": {therapy: sum(row["therapy"] == therapy for row in rows) for therapy in sorted({row["therapy"] for row in rows if row["therapy"]})},
        "response_counts": {response: sum(row["response"] == response for row in rows) for response in sorted({row["response"] for row in rows})},
        "mutation_associations": associations,
        "interpretation": "Exploratory breast treatment-response validation; small cohort and incomplete clinical fields prevent clinical prediction.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
