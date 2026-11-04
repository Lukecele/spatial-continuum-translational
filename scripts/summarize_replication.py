#!/usr/bin/env python3
"""Summarize GSE189487 signature detection by histology."""

import json
from collections import defaultdict
from pathlib import Path

INPUT = Path("data/derived/gse189487_signature_replication.json")
OUTPUT = Path("data/derived/gse189487_signature_by_histology.json")


def main() -> None:
    data = json.loads(INPUT.read_text())
    grouped = defaultdict(lambda: defaultdict(list))
    for sample in data["samples"]:
        histology = sample["histology"] or "unknown"
        for signature in sample["signatures"].values():
            for gene, values in signature.items():
                if values.get("present"):
                    grouped[histology][gene].append(values["detection_fraction"])

    report = {"source": str(INPUT), "histologies": {}}
    for histology, genes in sorted(grouped.items()):
        report["histologies"][histology] = {}
        for gene, values in sorted(genes.items()):
            report["histologies"][histology][gene] = {
                "samples": len(values),
                "mean_detection_fraction": sum(values) / len(values),
                "min_detection_fraction": min(values),
                "max_detection_fraction": max(values),
            }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"histologies": sorted(report["histologies"])}, indent=2))


if __name__ == "__main__":
    main()
