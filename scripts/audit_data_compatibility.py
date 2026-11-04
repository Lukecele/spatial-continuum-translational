#!/usr/bin/env python3
"""Retrospectively audit endpoint/cohort compatibility in derived results."""

import json
from pathlib import Path

ROOT = Path("data/derived")
OUTPUT = ROOT / "data_compatibility_audit.json"


def load(name):
    return json.loads((ROOT / name).read_text())


def main():
    heterogeneity = load("cohort_heterogeneity_audit.json")
    gist = load("gist_validation_summary.json")
    melanoma = load("melanoma_validation_summary.json")
    resistance = load("resistance_metadata_analysis.json")
    stats = load("resistance_statistical_comparison.json")

    checks = {
        "pooled_clinical_model_disallowed": heterogeneity["pooled_clinical_model_allowed"] is False,
        "gist_is_patient_level": gist["complete_patients"] == 438,
        "gist_has_rfs_events": gist["events"] == 205,
        "melanoma_uses_response_context": "response_counts" in melanoma and "early_resistance" in melanoma,
        "egfr_xenium_is_paired": stats["xenium_paired"]["pairs"] == 5,
        "egfr_snrna_states_separate": stats["snrna_state_comparison"]["states"] == {"MRD": 14, "PD": 31, "TN": 28},
        "metadata_analysis_has_no_survival_endpoint": "survival" not in resistance,
    }
    report = {
        "checks": checks,
        "all_compatibility_checks_pass": all(checks.values()),
        "interpretation": "Cohorts and endpoints remain separated; this audit does not establish external clinical validity.",
    }
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not report["all_compatibility_checks_pass"]:
        raise SystemExit("Data compatibility audit failed")


if __name__ == "__main__":
    main()
