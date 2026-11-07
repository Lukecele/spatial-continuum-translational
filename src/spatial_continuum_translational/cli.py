"""Command-line interface for the exploratory GIST research profile."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import TextIO

from .gist import GistFeatures, GistResearchScore, score_gist_research_profile

SITES = ("gastric", "duodenal", "jejunal_ileal", "rectal", "other")
MUTATIONS = ("kit_exon11", "kit_exon9", "pdgfra", "wild_type", "other")
REQUIRED_FIELDS = {
    "mitoses_per_50_hpf",
    "site",
    "tumor_rupture",
    "mutation",
    "tumor_size_cm",
}
MODEL_VERSION = "gist-research-profile-v1"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate an uncalibrated, research-only GIST phenotype score. "
            "This is not a clinical prediction or treatment recommendation."
        )
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--input",
        type=Path,
        help="TSV, CSV, or JSON input file; use '-' for stdin.",
    )
    input_group.add_argument("--mitoses-per-50-hpf", type=float)
    parser.add_argument("--site", choices=SITES)
    parser.add_argument("--tumor-rupture", action="store_true")
    parser.add_argument("--mutation", choices=MUTATIONS)
    parser.add_argument("--tumor-size-cm", type=float)
    parser.add_argument("--format", choices=("json", "tsv"), default="json")
    parser.add_argument(
        "--output",
        type=argparse.FileType("w", encoding="utf-8"),
        default=sys.stdout,
        help="Output file path; defaults to stdout.",
    )
    return parser


def _features_from_mapping(row: dict[str, str], row_number: int) -> GistFeatures:
    missing = REQUIRED_FIELDS - row.keys()
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"row {row_number}: missing required fields: {names}")

    raw_rupture = row["tumor_rupture"].strip().lower()
    if raw_rupture not in {"true", "false", "1", "0", "yes", "no"}:
        raise ValueError(
            f"row {row_number}: tumor_rupture must be true/false, yes/no, or 1/0"
        )

    site = row["site"].strip()
    mutation = row["mutation"].strip()
    if site not in SITES:
        raise ValueError(f"row {row_number}: unsupported site: {site}")
    if mutation not in MUTATIONS:
        raise ValueError(f"row {row_number}: unsupported mutation: {mutation}")

    try:
        mitoses = float(row["mitoses_per_50_hpf"])
        tumor_size = float(row["tumor_size_cm"])
    except ValueError as error:
        raise ValueError(
            f"row {row_number}: mitoses_per_50_hpf and tumor_size_cm must be numbers"
        ) from error

    return GistFeatures(
        mitoses_per_50_hpf=mitoses,
        site=site,
        tumor_rupture=raw_rupture in {"true", "1", "yes"},
        mutation=mutation,
        tumor_size_cm=tumor_size,
    )


def _read_rows(path: Path) -> list[dict[str, str]]:
    if str(path) == "-":
        source = sys.stdin
        close_source = False
    else:
        source = path.open(encoding="utf-8", newline="")
        close_source = True
    try:
        if path.suffix.lower() == ".json":
            payload = json.load(source)
            rows = payload if isinstance(payload, list) else [payload]
            if not all(isinstance(row, dict) for row in rows):
                raise ValueError("JSON input must be an object or a list of objects")
            return [
                {key: str(value) for key, value in row.items() if value is not None}
                for row in rows
            ]
        delimiter = "," if path.suffix.lower() == ".csv" else "\t"
        return list(csv.DictReader(source, delimiter=delimiter))
    finally:
        if close_source:
            source.close()


def _result(score: GistResearchScore, sample_id: str | None = None) -> dict[str, object]:
    result = asdict(score)
    result["model_version"] = MODEL_VERSION
    result["research_only"] = True
    if sample_id:
        result["sample_id"] = sample_id
    return result


def _write_tsv(output: TextIO, results: list[dict[str, object]]) -> None:
    fieldnames = list(results[0])
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(results)


def main(argv: list[str] | None = None) -> int:
    """Run the GIST research score CLI and return a process exit code."""
    args = _parser().parse_args(argv)
    if args.input is not None:
        rows = _read_rows(args.input)
        results = [
            _result(
                score_gist_research_profile(_features_from_mapping(row, index)),
                row.get("sample_id"),
            )
            for index, row in enumerate(rows, start=2)
        ]
    else:
        required_args = (
            args.mitoses_per_50_hpf,
            args.site,
            args.mutation,
            args.tumor_size_cm,
        )
        if any(value is None for value in required_args):
            _parser().error(
                "single-record mode requires --mitoses-per-50-hpf, --site, "
                "--mutation, and --tumor-size-cm"
            )
        row = {
            "mitoses_per_50_hpf": str(args.mitoses_per_50_hpf),
            "site": args.site,
            "tumor_rupture": str(args.tumor_rupture),
            "mutation": args.mutation,
            "tumor_size_cm": str(args.tumor_size_cm),
        }
        results = [
            _result(score_gist_research_profile(_features_from_mapping(row, 1)))
        ]

    if not results:
        _parser().error("input contains no records")
    if args.format == "json":
        json.dump(results[0] if len(results) == 1 else results, args.output, indent=2)
        args.output.write("\n")
    else:
        _write_tsv(args.output, results)
    if args.output is not sys.stdout:
        args.output.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
