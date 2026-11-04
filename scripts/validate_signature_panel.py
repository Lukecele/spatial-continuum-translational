#!/usr/bin/env python3
"""Validate frozen signature genes against a supplied panel gene list."""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("panel", type=Path)
    parser.add_argument("--signatures", type=Path, default=Path("data/resistance_signatures_v1.json"))
    parser.add_argument("--output", type=Path, default=Path("data/derived/resistance_signatures_v1_panel_validation.json"))
    args = parser.parse_args()

    panel = {line.strip().upper() for line in args.panel.read_text().splitlines() if line.strip()}
    definition = json.loads(args.signatures.read_text())
    report = {"signature_version": definition["version"], "panel": str(args.panel), "signatures": {}}
    for name, signature in definition["signatures"].items():
        present = [gene for gene in signature["genes"] if gene.upper() in panel]
        missing = [gene for gene in signature["genes"] if gene.upper() not in panel]
        report["signatures"][name] = {
            "requested": len(signature["genes"]),
            "present": present,
            "missing": missing,
            "coverage_fraction": len(present) / len(signature["genes"]),
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
