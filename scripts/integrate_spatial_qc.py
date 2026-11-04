#!/usr/bin/env python3
"""Compare detection fractions across the two spatial datasets."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, default=Path("data/derived/gse301973_signature_qc.json"))
    parser.add_argument("--replication", type=Path, default=Path("data/derived/gse189487_signature_replication.json"))
    parser.add_argument("--threshold", type=float, default=0.01)
    parser.add_argument("--output", type=Path, default=Path("data/derived/spatial_replication_summary.json"))
    args = parser.parse_args()

    case = json.loads(args.case.read_text())
    replication = json.loads(args.replication.read_text())
    genes = sorted(
        {
            gene
            for signature in case["signatures"].values()
            for gene in (entry["gene"] for entry in signature)
        }
        | {
            gene
            for sample in replication["samples"]
            for signature in sample["signatures"].values()
            for gene in signature
        }
    )

    report = {
        "case_dataset": str(args.case),
        "replication_dataset": str(args.replication),
        "comparison_metric": "detection_fraction",
        "threshold": args.threshold,
        "genes": {},
    }
    for gene in genes:
        case_entry = next(
            (entry for signature in case["signatures"].values() for entry in signature if entry["gene"] == gene),
            {"present": False},
        )
        case_fraction = case_entry.get("detection_fraction")
        replication_values = []
        for sample in replication["samples"]:
            entry = next(
                (sample_gene for signature in sample["signatures"].values() for sample_gene_name, sample_gene in signature.items() if sample_gene_name == gene),
                {"present": False},
            )
            if entry.get("present"):
                replication_values.append(entry.get("detection_fraction", 0.0))
        detectable_samples = sum(value >= args.threshold for value in replication_values)
        if case_fraction is not None and case_fraction >= args.threshold and detectable_samples >= 3:
            classification = "replicated_detectable"
        elif case_fraction is not None and replication_values:
            classification = "sparse_or_platform_sensitive"
        else:
            classification = "not_replicated"
        report["genes"][gene] = {
            "case_detection_fraction": case_fraction,
            "replication_sample_count": len(replication_values),
            "replication_mean_detection_fraction": sum(replication_values) / len(replication_values) if replication_values else None,
            "replication_min_detection_fraction": min(replication_values) if replication_values else None,
            "replication_max_detection_fraction": max(replication_values) if replication_values else None,
            "replication_samples_above_threshold": detectable_samples,
            "classification": classification,
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
