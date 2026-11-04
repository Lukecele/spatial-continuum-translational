#!/usr/bin/env python3
"""Summarize treatment-state metadata at sample and patient level."""

import csv
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

XENIUM = Path("/tmp/treatment-cohorts/GSE342824_xenium_cell_metadata.tsv.gz")
SNRNA = Path("/tmp/treatment-cohorts/GSE292469_cell_metadata.tsv.gz")
OUTPUT = Path("data/derived/treatment_resistance_state_summary.json")


def xenium_summary() -> dict:
    samples = defaultdict(lambda: {"patient_id": None, "timepoint": None, "cells": 0, "tumor_cells": 0, "mut_pos_cells": 0, "egfr_mut": Counter(), "pd_like_tn": Counter()})
    with gzip.open(XENIUM, "rt", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            summary = samples[row["sample_id"]]
            summary["patient_id"] = row["patient_id"]
            summary["timepoint"] = row["timepoint"]
            summary["cells"] += 1
            summary["tumor_cells"] += row.get("is_tumor_cell") == "TRUE"
            summary["mut_pos_cells"] += row.get("mut_pos_cell") in {"Pos", "TRUE", "True", "1"}
            if row.get("EGFR.mut"):
                summary["egfr_mut"][row["EGFR.mut"]] += 1
            if row.get("pd_like_tn"):
                summary["pd_like_tn"][row["pd_like_tn"]] += 1
    return {sample: {**values, "egfr_mut": dict(values["egfr_mut"]), "pd_like_tn": dict(values["pd_like_tn"])} for sample, values in sorted(samples.items())}


def snrna_summary() -> dict:
    samples = defaultdict(lambda: {"time_point": None, "nuclei": 0, "tumor_nuclei": 0, "cell_types": Counter()})
    with gzip.open(SNRNA, "rt", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            summary = samples[row["sample_id"]]
            summary["time_point"] = row["time_point"]
            summary["nuclei"] += 1
            summary["tumor_nuclei"] += row.get("is_tumor_cell") == "TRUE"
            summary["cell_types"][row["cell_type"]] += 1
    return {sample: {**values, "cell_types": dict(values["cell_types"])} for sample, values in sorted(samples.items())}


def main() -> None:
    report = {
        "xenium": xenium_summary(),
        "snrna": snrna_summary(),
        "interpretation": "Cell-level counts are descriptive; inferential analyses must use sample or patient as the unit of replication.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"xenium_samples": len(report["xenium"]), "snrna_samples": len(report["snrna"])}, indent=2))


if __name__ == "__main__":
    main()
