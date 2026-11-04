#!/usr/bin/env python3
"""Validate structural assumptions of the primary treatment cohorts."""

import json
from pathlib import Path

INPUT = Path("data/derived/treatment_resistance_state_summary.json")
OUTPUT = Path("data/derived/primary_cohort_validation.json")


def main() -> None:
    data = json.loads(INPUT.read_text())
    xenium = data["xenium"]
    snrna = data["snrna"]
    patients = {}
    for row in xenium.values():
        patients.setdefault(row["patient_id"], set()).add(row["timepoint"])
    complete_pairs = sorted(patient for patient, states in patients.items() if states == {"TN", "PD"})
    snrna_states = {row["time_point"] for row in snrna.values()}
    c797s_samples = sorted(
        sample
        for sample, row in xenium.items()
        if any("C797S" in genotype for genotype in row["egfr_mut"])
    )
    checks = {
        "five_complete_xenium_pairs": len(complete_pairs) == 5,
        "xenium_pair_patients": complete_pairs,
        "snrna_has_tn_mrd_pd": snrna_states == {"TN", "MRD", "PD"},
        "snrna_state_sample_counts": {
            state: sum(row["time_point"] == state for row in snrna.values())
            for state in sorted(snrna_states)
        },
        "c797s_localized_to_pd_sample": c797s_samples == ["XE5_PD"],
    }
    report = {"checks": checks, "all_structural_checks_pass": all(value is True for key, value in checks.items() if isinstance(value, bool))}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not report["all_structural_checks_pass"]:
        raise SystemExit("Primary cohort structural validation failed")


if __name__ == "__main__":
    main()
