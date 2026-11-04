#!/usr/bin/env python3
"""Run structural QC on the extracted GSE301973 spatial objects."""

import argparse
import json
from collections import Counter
from pathlib import Path

import h5py
import pyarrow.parquet as pq


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("h5ad", type=Path)
    parser.add_argument("positions", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/derived/gse301973_qc.json"))
    args = parser.parse_args()

    with h5py.File(args.h5ad, "r") as handle:
        data = handle["X"]["data"]
        n_obs = handle["X"]["indptr"].shape[0] - 1
        n_vars = handle["var"]["_index"].shape[0]
        nnz = int(data.shape[0])
        report = {
            "h5ad": str(args.h5ad),
            "n_obs": n_obs,
            "n_vars": n_vars,
            "nonzero_values": nnz,
            "mean_nonzero_features_per_obs": nnz / n_obs,
            "mean_value_sum_per_obs": float(data[:].sum() / n_obs),
            "obs_fields": sorted(handle["obs"].keys()),
        }
        cell_type_group = handle["obs"]["cell_type"]
        categories = [
            value.decode() if isinstance(value, bytes) else str(value)
            for value in cell_type_group["categories"][:]
        ]
        codes = cell_type_group["codes"][:]
        report["cell_type_counts"] = dict(
            Counter(categories[int(code)] for code in codes).most_common()
        )
        sample_group = handle["obs"]["sample"]
        sample_categories = [
            value.decode() if isinstance(value, bytes) else str(value)
            for value in sample_group["categories"][:]
        ]
        report["sample_labels"] = sample_categories

    positions = pq.read_table(
        args.positions,
        columns=["in_tissue", "array_row", "array_col", "pxl_row_in_fullres", "pxl_col_in_fullres"],
    ).to_pydict()
    tissue = [bool(value) for value in positions["in_tissue"]]
    report["positions_rows"] = len(tissue)
    report["positions_in_tissue"] = sum(tissue)
    report["positions_in_tissue_fraction"] = sum(tissue) / len(tissue)
    report["array_row_range"] = [min(positions["array_row"]), max(positions["array_row"])]
    report["array_col_range"] = [min(positions["array_col"]), max(positions["array_col"])]
    report["fullres_row_range"] = [min(positions["pxl_row_in_fullres"]), max(positions["pxl_row_in_fullres"])]
    report["fullres_col_range"] = [min(positions["pxl_col_in_fullres"]), max(positions["pxl_col_in_fullres"])]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
