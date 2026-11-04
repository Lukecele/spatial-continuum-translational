#!/usr/bin/env python3
"""Run exploratory sample-level TN/PD and TN/MRD/PD comparisons."""

import json
from pathlib import Path

import numpy as np
from scipy.stats import kruskal, wilcoxon

INPUT = Path("data/derived/resistance_metadata_analysis.json")
OUTPUT = Path("data/derived/resistance_statistical_comparison.json")
XENIUM_METRICS = (
    "tumor_fraction",
    "pd_like_tumor_fraction",
    "c797s_cell_fraction",
    "mean_alveolar_score_tumor",
    "mean_basal_squamous_score_tumor",
    "mean_neuroendocrine_score_tumor",
)
SNRNA_METRICS = ("tumor_fraction", "mean_ncount_rna", "mean_nfeature_rna")


def bootstrap_mean_difference(values: list[float], iterations: int = 5000) -> list[float]:
    rng = np.random.default_rng(42)
    array = np.asarray(values, dtype=float)
    draws = rng.choice(array, size=(iterations, len(array)), replace=True).mean(axis=1)
    return [float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))]


def paired_xenium(rows: list[dict]) -> dict:
    pairs = {}
    for row in rows:
        pairs.setdefault(row["patient_id"], {})[row["timepoint"]] = row
    complete = [pair for pair in pairs.values() if "TN" in pair and "PD" in pair]
    result = {"pairs": len(complete), "metrics": {}}
    for metric in XENIUM_METRICS:
        differences = [pair["PD"][metric] - pair["TN"][metric] for pair in complete]
        if len(differences) >= 2 and any(differences):
            statistic, p_value = wilcoxon(differences, alternative="two-sided", method="exact")
        else:
            statistic, p_value = None, None
        result["metrics"][metric] = {
            "differences_pd_minus_tn": differences,
            "mean_difference": float(np.mean(differences)),
            "bootstrap_95ci": bootstrap_mean_difference(differences),
            "wilcoxon_statistic": None if statistic is None else float(statistic),
            "wilcoxon_p_value_exploratory": None if p_value is None else float(p_value),
        }
    return result


def snrna_states(rows: list[dict]) -> dict:
    result = {"states": {}, "metrics": {}}
    for state in sorted({row["timepoint"] for row in rows}):
        state_rows = [row for row in rows if row["timepoint"] == state]
        result["states"][state] = len(state_rows)
    for metric in SNRNA_METRICS:
        groups = [
            [row[metric] for row in rows if row["timepoint"] == state and row[metric] is not None]
            for state in sorted(result["states"])
        ]
        statistic, p_value = kruskal(*groups)
        result["metrics"][metric] = {
            "group_order": sorted(result["states"]),
            "group_means": {
                state: float(np.mean([row[metric] for row in rows if row["timepoint"] == state and row[metric] is not None]))
                for state in sorted(result["states"])
            },
            "kruskal_statistic": float(statistic),
            "kruskal_p_value_exploratory": float(p_value),
        }
    return result


def main() -> None:
    data = json.loads(INPUT.read_text())
    report = {
        "xenium_paired": paired_xenium(data["xenium_by_sample"]),
        "snrna_state_comparison": snrna_states(data["snrna_by_sample"]),
        "interpretation": "All p-values are exploratory; Xenium has five patient pairs and snRNA states are observational, unmatched groups.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
