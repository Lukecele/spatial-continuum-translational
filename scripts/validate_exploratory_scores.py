#!/usr/bin/env python3
"""Validate the frozen exploratory tumor-score manifest."""

import json
import sys
from pathlib import Path


MANIFEST = Path(__file__).resolve().parents[1] / "data" / "exploratory_tumor_scores_v1.json"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    if manifest.get("status") != "frozen_exploratory_not_clinically_validated":
        errors.append("manifest must remain explicitly exploratory")
    if "equal weights" not in manifest.get("scoring_rule", ""):
        errors.append("scoring rule must remain deterministic equal-weight")
    if manifest.get("unit_of_replication") not in {"patient", "patient_or_patient_state"}:
        errors.append("replication unit must be patient-aware")
    for name, score in manifest.get("scores", {}).items():
        genes = score.get("genes", [])
        if len(genes) < 3 or len(genes) != len(set(genes)):
            errors.append(f"{name}: invalid or duplicated gene list")
        if not score.get("endpoint"):
            errors.append(f"{name}: missing endpoint")
        if not score.get("status", "").startswith("frozen_exploratory"):
            errors.append(f"{name}: score is not marked exploratory")

    if errors:
        print("FAIL: exploratory score manifest is invalid")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {len(manifest['scores'])} exploratory scores frozen")
    print("Clinical validation remains explicitly prohibited until separate evidence is available")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
