#!/usr/bin/env python3
"""Compute frozen gene signatures from the GSE292469 10x HDF5 matrix."""

import argparse
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path

import h5py
import numpy as np

SIGNATURE_FILE = Path("data/resistance_signatures_v1.json")
METADATA_FILE = Path("/tmp/treatment-cohorts/GSE292469_cell_metadata.tsv.gz")
OUTPUT = Path("data/derived/gse292469_gene_signature_scores.json")


def load_metadata(path: Path) -> list[dict[str, str]]:
    with gzip.open(path, "rt", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def decode(value) -> str:
    return value.decode() if isinstance(value, bytes) else str(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path)
    parser.add_argument("--metadata", type=Path, default=METADATA_FILE)
    parser.add_argument("--signatures", type=Path, default=SIGNATURE_FILE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    metadata = load_metadata(args.metadata)
    signatures = json.loads(args.signatures.read_text())["signatures"]
    requested = sorted({gene for signature in signatures.values() for gene in signature["genes"]})

    with h5py.File(args.matrix, "r") as handle:
        group = handle["matrix"] if "matrix" in handle else handle
        feature_group = group["features"]
        feature_names = [decode(value) for value in feature_group["name"][:]]
        feature_index = {name.upper(): index for index, name in enumerate(feature_names)}
        missing = [gene for gene in requested if gene.upper() not in feature_index]
        if missing:
            raise ValueError(f"Missing genes from matrix: {missing}")
        indices = [feature_index[gene.upper()] for gene in requested]
        data = group["data"]
        matrix_indices = group["indices"]
        indptr = group["indptr"]
        shape = tuple(int(value) for value in group["shape"][:])
        if shape[1] != len(metadata):
            raise ValueError(f"Metadata cells {len(metadata)} do not match matrix columns {shape[1]}")

        per_cell = np.zeros((len(indices), shape[1]), dtype=np.float64)
        for column in range(shape[1]):
            start = int(indptr[column])
            end = int(indptr[column + 1])
            rows = matrix_indices[start:end]
            values = data[start:end]
            lookup = {int(row): float(value) for row, value in zip(rows, values)}
            for gene_position, matrix_row in enumerate(indices):
                per_cell[gene_position, column] = lookup.get(matrix_row, 0.0)

    by_sample = defaultdict(list)
    for index, row in enumerate(metadata):
        by_sample[row["sample_id"]].append(index)

    report = {
        "matrix": str(args.matrix),
        "cells": len(metadata),
        "genes_requested": requested,
        "by_sample": {},
        "interpretation": "Scores are mean z-scored expression across cells within each sample; sample is the unit of replication.",
    }
    gene_position = {gene: index for index, gene in enumerate(requested)}
    for sample, cell_indices in sorted(by_sample.items()):
        state = metadata[cell_indices[0]]["time_point"]
        sample_values = per_cell[:, cell_indices]
        scores = {}
        for signature_name, signature in signatures.items():
            positions = [gene_position[gene] for gene in signature["genes"]]
            values = sample_values[positions]
            gene_means = values.mean(axis=1)
            gene_std = values.std(axis=1)
            normalized = (gene_means - gene_means.mean()) / (gene_means.std() or 1.0)
            scores[signature_name] = {
                "genes": signature["genes"],
                "mean_expression": float(gene_means.mean()),
                "mean_gene_z": float(normalized.mean()),
                "cell_count": len(cell_indices),
            }
        report["by_sample"][sample] = {"state": state, "cell_count": len(cell_indices), "scores": scores}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"samples": len(report["by_sample"]), "cells": report["cells"]}, indent=2))


if __name__ == "__main__":
    main()
