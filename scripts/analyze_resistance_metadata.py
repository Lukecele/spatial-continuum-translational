#!/usr/bin/env python3
"""Analyze treatment-state and resistance metadata at sample level."""

import csv
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

XENIUM = Path("/tmp/treatment-cohorts/GSE342824_xenium_cell_metadata.tsv.gz")
SNRNA = Path("/tmp/treatment-cohorts/GSE292469_cell_metadata.tsv.gz")
OUTPUT = Path("data/derived/resistance_metadata_analysis.json")


def number(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def xenium() -> list[dict]:
    groups = defaultdict(list)
    with gzip.open(XENIUM, "rt", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            groups[row["sample_id"]].append(row)
    results = []
    for sample_id, rows in sorted(groups.items()):
        tumor = [row for row in rows if row.get("is_tumor_cell") == "TRUE"]
        pd_like = [row for row in tumor if row.get("pd_like_tn") == "TRUE"]
        c797s = [row for row in rows if "C797S" in row.get("EGFR.mut", "")]
        results.append(
            {
                "sample_id": sample_id,
                "patient_id": rows[0]["patient_id"],
                "timepoint": rows[0]["timepoint"],
                "cells": len(rows),
                "tumor_cells": len(tumor),
                "tumor_fraction": len(tumor) / len(rows),
                "pd_like_tumor_fraction": len(pd_like) / len(tumor) if tumor else None,
                "c797s_cell_fraction": len(c797s) / len(rows),
                "mean_alveolar_score_tumor": mean([number(row.get("alveolar_score")) for row in tumor if number(row.get("alveolar_score")) is not None]),
                "mean_basal_squamous_score_tumor": mean([number(row.get("basal_squamous_score")) for row in tumor if number(row.get("basal_squamous_score")) is not None]),
                "mean_neuroendocrine_score_tumor": mean([number(row.get("neuroendocrine_score")) for row in tumor if number(row.get("neuroendocrine_score")) is not None]),
            }
        )
    return results


def snrna() -> list[dict]:
    groups = defaultdict(list)
    with gzip.open(SNRNA, "rt", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            groups[row["sample_id"]].append(row)
    results = []
    for sample_id, rows in sorted(groups.items()):
        tumor = [row for row in rows if row.get("is_tumor_cell") == "TRUE"]
        cell_type_counts = Counter(row.get("cell_type", "unknown") for row in rows)
        results.append(
            {
                "sample_id": sample_id,
                "timepoint": rows[0]["time_point"],
                "nuclei": len(rows),
                "tumor_nuclei": len(tumor),
                "tumor_fraction": len(tumor) / len(rows),
                "mean_ncount_rna": mean([number(row.get("nCount_RNA")) for row in rows if number(row.get("nCount_RNA")) is not None]),
                "mean_nfeature_rna": mean([number(row.get("nFeature_RNA")) for row in rows if number(row.get("nFeature_RNA")) is not None]),
                "cell_type_counts": dict(cell_type_counts),
            }
        )
    return results


def state_summary(rows: list[dict], state_key: str, metrics: list[str]) -> dict:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[state_key]].append(row)
    return {
        state: {
            "samples": len(values),
            **{metric: mean([value[metric] for value in values if value[metric] is not None]) for metric in metrics},
        }
        for state, values in sorted(grouped.items())
    }


def main() -> None:
    xenium_rows = xenium()
    snrna_rows = snrna()
    report = {
        "xenium_by_sample": xenium_rows,
        "xenium_by_state": state_summary(
            xenium_rows,
            "timepoint",
            ["tumor_fraction", "pd_like_tumor_fraction", "c797s_cell_fraction", "mean_alveolar_score_tumor", "mean_basal_squamous_score_tumor", "mean_neuroendocrine_score_tumor"],
        ),
        "snrna_by_sample": snrna_rows,
        "snrna_by_state": state_summary(snrna_rows, "timepoint", ["tumor_fraction", "mean_ncount_rna", "mean_nfeature_rna"]),
        "interpretation": "State summaries average sample-level metrics; they are descriptive and not inferential patient-level treatment effects.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"xenium_samples": len(xenium_rows), "snrna_samples": len(snrna_rows)}, indent=2))


if __name__ == "__main__":
    main()
