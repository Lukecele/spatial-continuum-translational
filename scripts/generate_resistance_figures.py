#!/usr/bin/env python3
"""Generate metadata-based figures for Manuscript 2."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

INPUT = Path("data/derived/resistance_metadata_analysis.json")
OUTPUT = Path("figures")


def paired_plot(rows: list[dict]) -> None:
    pairs = {}
    for row in rows:
        pairs.setdefault(row["patient_id"], {})[row["timepoint"]] = row
    pairs = {patient: value for patient, value in pairs.items() if {"TN", "PD"} <= set(value)}
    metrics = [
        ("mean_alveolar_score_tumor", "Tumour alveolar score"),
        ("mean_basal_squamous_score_tumor", "Basal/squamous score"),
        ("mean_neuroendocrine_score_tumor", "Neuroendocrine score"),
        ("pd_like_tumor_fraction", "PD-like tumour fraction"),
    ]
    fig, axes = plt.subplots(1, len(metrics), figsize=(14, 3.8), constrained_layout=True)
    for axis, (metric, label) in zip(axes, metrics):
        for patient, values in sorted(pairs.items()):
            axis.plot([0, 1], [values["TN"][metric], values["PD"][metric]], marker="o", linewidth=1.5, alpha=0.8)
        axis.set_title(label, fontsize=9)
        axis.set_xticks([0, 1], ["TN", "PD"])
        axis.grid(axis="y", alpha=0.25)
    fig.suptitle("GSE342824 paired Xenium metadata: exploratory TN to PD changes")
    fig.savefig(OUTPUT / "xenium_paired_resistance_metadata.png", dpi=220)
    plt.close(fig)


def snrna_plot(rows: list[dict]) -> None:
    states = ["TN", "MRD", "PD"]
    grouped = {state: [row for row in rows if row["timepoint"] == state] for state in states}
    fig, axes = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)
    for index, (metric, label) in enumerate((("tumor_fraction", "Tumour nuclei fraction"), ("mean_nfeature_rna", "Mean detected features"))):
        values = [[row[metric] for row in grouped[state]] for state in states]
        axes[index].boxplot(values, tick_labels=states, showmeans=True)
        axes[index].set_title(label)
        axes[index].grid(axis="y", alpha=0.25)
    fig.suptitle("GSE292469 sample-level metadata by treatment state")
    fig.savefig(OUTPUT / "snrna_state_metadata_qc.png", dpi=220)
    plt.close(fig)


def main() -> None:
    data = json.loads(INPUT.read_text())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    paired_plot(data["xenium_by_sample"])
    snrna_plot(data["snrna_by_sample"])
    print(f"Wrote figures to {OUTPUT}")


if __name__ == "__main__":
    main()
