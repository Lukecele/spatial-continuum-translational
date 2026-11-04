#!/usr/bin/env python3
"""Measure candidate signature-gene detection in an extracted H5AD."""

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
    parser.add_argument("--output", type=Path, default=Path("data/derived/gse301973_signature_qc.json"))
    args = parser.parse_args()

    signatures = json.loads(args.signatures.read_text())
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

        report = {"h5ad": str(args.h5ad), "n_obs": n_obs, "signatures": {}}
        for signature, requested_genes in signatures.items():
            if signature == "status" or signature == "purpose":
                continue
            entries = []
            for gene in requested_genes:
                index = gene_to_index.get(gene.upper())
                if index is None:
                    entries.append({"gene": gene, "present": False})
                    continue
                values = np.asarray(matrix[:, index].toarray()).ravel()
                entries.append(
                    {
                        "gene": gene,
                        "present": True,
                        "detected_cells": int(np.count_nonzero(values)),
                        "detection_fraction": float(np.count_nonzero(values) / n_obs),
                        "mean_value": float(values.mean()),
                    }
                )
            report["signatures"][signature] = entries

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
