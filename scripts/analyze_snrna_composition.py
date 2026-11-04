#!/usr/bin/env python3
"""Analyze sample-level snRNA cell-type composition across TN/MRD/PD."""

import csv
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import kruskal

INPUT = Path("/tmp/treatment-cohorts/GSE292469_cell_metadata.tsv.gz")
OUTPUT = Path("data/derived/snrna_cell_composition_analysis.json")
STATES = ("TN", "MRD", "PD")


def main() -> None:
    samples = defaultdict(Counter)
    state_by_sample = {}
    with gzip.open(INPUT, "rt", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            sample = row["sample_id"]
            samples[sample][row["cell_type"]] += 1
            state_by_sample[sample] = row["time_point"]

    sample_rows = []
    all_types = sorted({cell_type for counts in samples.values() for cell_type in counts})
    for sample, counts in sorted(samples.items()):
        total = sum(counts.values())
        sample_rows.append({
            "sample_id": sample,
            "state": state_by_sample[sample],
            "nuclei": total,
            "fractions": {cell_type: counts[cell_type] / total for cell_type in all_types},
        })

    raw_results = {}
    for cell_type in all_types:
        groups = [[row["fractions"].get(cell_type, 0.0) for row in sample_rows if row["state"] == state] for state in STATES]
        statistic, p_value = kruskal(*groups)
        raw_results[cell_type] = {
            "group_means": {state: float(np.mean(group)) for state, group in zip(STATES, groups)},
            "kruskal_statistic": float(statistic),
            "p_value": float(p_value),
        }

    ordered = sorted(raw_results.items(), key=lambda item: item[1]["p_value"])
    m = len(ordered)
    for rank, (_, result) in enumerate(ordered, start=1):
        result["bh_fdr"] = min(1.0, result["p_value"] * m / rank)

    report = {
        "input": str(INPUT),
        "states": {state: sum(row["state"] == state for row in sample_rows) for state in STATES},
        "samples": sample_rows,
        "cell_types": raw_results,
        "interpretation": "Sample-level descriptive composition analysis; p-values and FDR are exploratory and do not establish treatment effects.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"samples": len(sample_rows), "cell_types": len(all_types)}, indent=2))


if __name__ == "__main__":
    main()
