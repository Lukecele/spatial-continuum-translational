#!/usr/bin/env python3
"""Replicate candidate signature coverage across GSE189487 samples."""

import argparse
import csv
import gzip
import json
from pathlib import Path

import numpy as np
from scipy.io import mmread

SAMPLE_META = {
    "TD1": {"histology": "IAC", "sex": "Female"},
    "TD2": {"histology": "IAC", "sex": "Male"},
    "TD3": {"histology": "MIA", "sex": "Male"},
    "TD5": {"histology": "AIS", "sex": "Female"},
    "TD6": {"histology": "MIA", "sex": "Female"},
    "TD8": {"histology": "AIS", "sex": "Male"},
}


def read_lines(path: Path) -> list[str]:
    with gzip.open(path, "rt") as handle:
        return [line.rstrip("\n").split("\t")[0] for line in handle]


def read_feature_names(path: Path) -> list[str]:
    with gzip.open(path, "rt") as handle:
        return [
            fields[1] if len(fields) > 1 else fields[0]
            for fields in (line.rstrip("\n").split("\t") for line in handle)
        ]


def in_tissue_indices(path: Path, barcodes: list[str]) -> np.ndarray:
    barcode_to_index = {barcode: index for index, barcode in enumerate(barcodes)}
    selected = []
    with gzip.open(path, "rt", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row:
                continue
            barcode = row[0]
            if barcode in barcode_to_index and len(row) >= 2 and row[1] == "1":
                selected.append(barcode_to_index[barcode])
    return np.asarray(selected, dtype=int)


def sample_report(matrix_path: Path, signatures: dict) -> dict:
    prefix = matrix_path.name.removesuffix("_matrix.mtx.gz")
    sample_dir = matrix_path.parent
    barcode_path = sample_dir / f"{prefix}_barcodes.tsv.gz"
    feature_path = sample_dir / f"{prefix}_features.tsv.gz"
    positions_path = sample_dir / f"{prefix}_tissue_positions_list.csv.gz"
    barcodes = read_lines(barcode_path)
    genes = read_feature_names(feature_path)
    matrix = mmread(matrix_path).tocsr()
    selected = in_tissue_indices(positions_path, barcodes)
    sample_id = prefix.split("_")[-1]
    result = {
        "sample": sample_id,
        "histology": SAMPLE_META.get(sample_id, {}).get("histology"),
        "barcodes": len(barcodes),
        "in_tissue": int(len(selected)),
        "genes": len(genes),
        "signatures": {},
    }
    gene_to_index = {gene.upper(): index for index, gene in enumerate(genes)}
    for signature, requested_genes in signatures.items():
        if signature in {"status", "purpose"}:
            continue
        result["signatures"][signature] = {}
        for gene in requested_genes:
            index = gene_to_index.get(gene.upper())
            if index is None:
                result["signatures"][signature][gene] = {"present": False}
                continue
            values = np.asarray(matrix[index, selected].toarray()).ravel()
            result["signatures"][signature][gene] = {
                "present": True,
                "detected_barcodes": int(np.count_nonzero(values)),
                "detection_fraction": float(np.count_nonzero(values) / len(values)) if len(values) else 0.0,
                "mean_value": float(values.mean()) if len(values) else 0.0,
            }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--signatures", type=Path, default=Path("data/signatures.json"))
    parser.add_argument("--output", type=Path, default=Path("data/derived/gse189487_signature_replication.json"))
    args = parser.parse_args()
    signatures = json.loads(args.signatures.read_text())
    reports = [sample_report(path, signatures) for path in sorted(args.root.glob("*_matrix.mtx.gz"))]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"samples": reports}, indent=2) + "\n")
    print(json.dumps({"samples": len(reports)}, indent=2))


if __name__ == "__main__":
    main()
