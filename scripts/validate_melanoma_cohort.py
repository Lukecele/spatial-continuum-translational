#!/usr/bin/env python3
"""Run exploratory patient-level melanoma BRAF-resistance validation."""

import json
from collections import defaultdict
from pathlib import Path

from scipy.stats import fisher_exact

ROOT = Path("data/raw/cbioportal/skcm_broad_brafresist_2012")
OUTPUT = Path("data/derived/melanoma_validation_summary.json")


def main():
    clinical = json.loads((ROOT / "clinical_patient.json").read_text())
    mutations = json.loads((ROOT / "mutations_braf_nras_map2k.json").read_text())
    patients = defaultdict(dict)
    for row in clinical:
        patients[row["patientId"]][row["clinicalAttributeId"]] = row["value"]
    for row in mutations:
        patients[row["patientId"]][f"{row['gene']}_mutated"] = 1

    rows = []
    for patient, values in patients.items():
        resistance = values.get("EARLY_RESISTANCE")
        response = values.get("TREATMENT_BEST_RESPONSE")
        if resistance not in {"Yes", "No"} and response is None:
            continue
        rows.append({
            "patient_id": patient,
            "resistance": resistance == "Yes",
            "response": response,
            "medication": values.get("MEDICATION"),
            "duration_weeks": float(values["DURATION_OF_THERAPY_WEEKS"]) if values.get("DURATION_OF_THERAPY_WEEKS") else None,
            "nras_mutated": bool(values.get("NRAS_mutated")),
            "map2k1_mutated": bool(values.get("MAP2K1_mutated")),
            "map2k2_mutated": bool(values.get("MAP2K2_mutated")),
        })

    associations = {}
    for gene in ("nras_mutated", "map2k1_mutated", "map2k2_mutated"):
        table = [[0, 0], [0, 0]]
        for row in rows:
            table[int(row[gene])][int(row["resistance"])] += 1
        odds_ratio, p_value = fisher_exact(table)
        associations[gene] = {"table_mutation_by_resistance": table, "odds_ratio": float(odds_ratio), "p_value_exploratory": float(p_value)}
    ordered = sorted(associations, key=lambda gene: associations[gene]["p_value_exploratory"])
    for rank, gene in enumerate(ordered, start=1):
        associations[gene]["bh_fdr_exploratory"] = min(1.0, associations[gene]["p_value_exploratory"] * len(ordered) / rank)

    report = {
        "cohort": "skcm_broad_brafresist_2012",
        "patients_with_treatment_fields": len(rows),
        "early_resistance": sum(row["resistance"] for row in rows),
        "response_counts": {response: sum(row["response"] == response for row in rows) for response in sorted({row["response"] for row in rows if row["response"]})},
        "medication_counts": {med: sum(row["medication"] == med for row in rows) for med in sorted({row["medication"] for row in rows if row["medication"]})},
        "mutation_associations": associations,
        "interpretation": "Exploratory melanoma resistance validation; small cohort and incomplete clinical fields prevent clinical prediction.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
