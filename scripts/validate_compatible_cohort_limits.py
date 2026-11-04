#!/usr/bin/env python3
"""Validate the maximum-compatible-cohort ledger."""

import json
from pathlib import Path

INPUT = Path("data/derived/compatible_cohort_limits.json")
OUTPUT = Path("data/derived/compatible_cohort_limits_audit.json")


def main():
    report = json.loads(INPUT.read_text())
    sets = report["sets"]
    checks = {
        "six_separate_estimands": len(sets) == 6,
        "gist_rfs_has_events": sets["gist_rfs"]["events"] == 205,
        "melanoma_response_is_not_cell_level": sets["melanoma_braf_response"]["response_annotated_patients"] == 45,
        "renal_and_pancreas_are_separate": sets["renal_trial_response"]["endpoint"] != sets["pancreatic_trial_response"]["endpoint"],
        "excluded_pool_rules_present": len(report["excluded_pools"]) >= 5,
    }
    output = {"checks": checks, "all_checks_pass": all(checks.values()), "interpretation": report["principle"]}
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))
    if not output["all_checks_pass"]:
        raise SystemExit("Compatible cohort limits audit failed")


if __name__ == "__main__":
    main()
