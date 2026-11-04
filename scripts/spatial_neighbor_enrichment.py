#!/usr/bin/env python3
"""Describe cell-type contacts in the extracted spatial H5AD."""

import argparse
import json
from collections import Counter
from pathlib import Path

import h5py
import numpy as np
from scipy.spatial import cKDTree


def decode(value) -> str:
    return value.decode() if isinstance(value, bytes) else str(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("h5ad", type=Path)
    parser.add_argument("--neighbors", type=int, default=6)
    parser.add_argument("--output", type=Path, default=Path("data/derived/gse301973_neighbor_enrichment.json"))
    args = parser.parse_args()

    with h5py.File(args.h5ad, "r") as handle:
        obs = handle["obs"]
        coords = np.column_stack([obs["array_row"][:], obs["array_col"][:]])
        group = obs["cell_type"]
        categories = [decode(value) for value in group["categories"][:]]
        codes = group["codes"][:]

    tree = cKDTree(coords)
    _, neighbor_indices = tree.query(coords, k=args.neighbors + 1)
    neighbor_indices = neighbor_indices[:, 1:]
    type_names = categories
    global_counts = Counter(type_names[int(code)] for code in codes)
    total = len(codes)
    contact_counts = {source: Counter() for source in type_names}
    for source_code, neighbors in zip(codes, neighbor_indices):
        source = type_names[int(source_code)]
        contact_counts[source].update(type_names[int(codes[index])] for index in neighbors)

    report = {
        "h5ad": str(args.h5ad),
        "neighbors_per_cell": args.neighbors,
        "cells": total,
        "global_cell_type_counts": dict(global_counts),
        "contact_enrichment": {},
    }
    for source in type_names:
        source_total = sum(contact_counts[source].values())
        report["contact_enrichment"][source] = {}
        for target in type_names:
            observed = contact_counts[source][target] / source_total if source_total else 0.0
            expected = global_counts[target] / total
            report["contact_enrichment"][source][target] = {
                "observed_neighbor_fraction": observed,
                "global_expected_fraction": expected,
                "enrichment_ratio": observed / expected if expected else None,
            }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"cells": total, "neighbors_per_cell": args.neighbors}, indent=2))


if __name__ == "__main__":
    main()
