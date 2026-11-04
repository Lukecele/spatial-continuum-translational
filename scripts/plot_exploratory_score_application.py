#!/usr/bin/env python3
"""Generate descriptive figures from exploratory score application output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for item in report["reports"]:
        groups = list(item["summary"])
        means = [item["summary"][group]["mean"] for group in groups]
        counts = [item["summary"][group]["n"] for group in groups]
        figure, axis = plt.subplots(figsize=(8, 4.5))
        axis.bar(groups, means, color="#2f6f8f")
        axis.axhline(0, color="#333333", linewidth=0.8)
        axis.set_ylabel("Exploratory score mean")
        axis.set_title(f"{item['dataset']} - {item['score']} (descriptive)")
        axis.tick_params(axis="x", rotation=25)
        for index, (mean, count) in enumerate(zip(means, counts)):
            axis.text(index, mean, f"n={count}", ha="center", va="bottom" if mean >= 0 else "top", fontsize=8)
        figure.tight_layout()
        figure.savefig(args.output_dir / f"{item['dataset'].lower()}_exploratory_score.png", dpi=180)
        plt.close(figure)

        if item["paired_pre_to_prog"]:
            deltas = [row["pre_to_prog_delta"] for row in item["paired_pre_to_prog"]]
            figure, axis = plt.subplots(figsize=(7, 4.5))
            axis.hist(deltas, bins=min(8, max(3, len(deltas))), color="#9b5b3e", edgecolor="white")
            axis.axvline(0, color="#333333", linewidth=0.8)
            axis.set_xlabel("PROG minus PRE exploratory score")
            axis.set_ylabel("Patients")
            axis.set_title(f"{item['dataset']} - paired state deltas (descriptive)")
            figure.tight_layout()
            figure.savefig(args.output_dir / f"{item['dataset'].lower()}_paired_deltas.png", dpi=180)
            plt.close(figure)

    print(f"Generated figures in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
