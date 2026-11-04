#!/usr/bin/env python3
"""Stratify candidate spatial genes by annotated cell type."""

import argparse
import json
from pathlib import Path

import h5py
import numpy as np
from scipy.sparse import csr_matrix


def decode(value) -> str:
    return value.decode() if isinstance(value, bytes) else str(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("h5ad", type=Path)
    parser.add_argument("--signatures", type=Path, default=Path("data/signatures.json"))
    parser.add_argument("--output", type=Path, default=Path("data/derived/gse301973_signature_by_cell_type.json"))
    args = parser.parse_args()

    signatures = json.loads(args.signatures.read_text())
    requested_genes = sorted({gene for values in signatures.values() if isinstance(values, list) for gene in values})
    with h5py.File(args.h5ad, "r") as handle:
        indptr = handle["X"]["indptr"][:]
        n_obs = len(indptr) - 1
        n_vars = handle["var"]["_index"].shape[0]
        matrix = csr_matrix(
            (handle["X"]["data"][:], handle["X"]["indices"][:], indptr),
            shape=(n_obs, n_vars),
        )
        genes = [decode(value) for value in handle["var"]["_index"][:]]
        gene_to_index = {gene.upper(): index for index, gene in enumerate(genes)}
        cell_type_group = handle["obs"]["cell_type"]
        cell_types = [decode(value) for value in cell_type_group["categories"][:]]
        cell_codes = cell_type_group["codes"][:]

        report = {"h5ad": str(args.h5ad), "n_obs": n_obs, "cell_types": {}, "genes": {}}
        for code, cell_type in enumerate(cell_types):
            report["cell_types"][cell_type] = int(np.count_nonzero(cell_codes == code))
        for gene in requested_genes:
            index = gene_to_index.get(gene.upper())
            if index is None:
                report["genes"][gene] = {"present": False}
                continue
            values = np.asarray(matrix[:, index].toarray()).ravel()
            by_type = {}
            for code, cell_type in enumerate(cell_types):
                mask = cell_codes == code
                subset = values[mask]
                by_type[cell_type] = {
                    "cells": int(mask.sum()),
                    "detected_cells": int(np.count_nonzero(subset)),
                    "detection_fraction": float(np.count_nonzero(subset) / len(subset)),
                    "mean_value": float(subset.mean()),
                }
            report["genes"][gene] = {"present": True, "by_cell_type": by_type}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
