#!/usr/bin/env python3
"""Deterministic exploratory Composite Resistance Index calculator.

This module is a research calculator only. It does not estimate survival,
recommend treatment, or support clinical decision-making.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from typing import Dict, Iterable, Optional, Sequence, TextIO

WEIGHTS = {"S": 0.47, "G": 0.33, "M": 0.20}


def _score_pattern(pattern: object) -> tuple[float, str]:
    value = str(pattern or "").strip().lower()
    if "lepidic" in value:
        return 0.00, "Lepidic pattern"
    if "solid" in value or "micropapillary" in value:
        return 1.00, "Solid or micropapillary pattern"
    if "mixed" in value or "moderate" in value:
        return 0.80, "Mixed pattern"
    if "acinar" in value or "papillary" in value:
        return 0.40, "Acinar or papillary pattern"
    raise ValueError(f"Unknown histologic pattern: {pattern!r}")


def _is_mutated(value: object, gene: str) -> bool:
    text = str(value or "").strip().lower()
    if text in {"", "wt", "wildtype", "wild-type", "wild type", "normal", "negative", "neg"}:
        return False
    if text in {"mut", "mutated", "mutation", "altered", "positive", "pos", "loss", "deleted", "deletion", "true", "yes", "1"}:
        return True
    raise ValueError(f"Unknown {gene} status: {value!r}")


def _score_genomics(tp53: object, rb1: object) -> tuple[float, str]:
    tp53_mut = _is_mutated(tp53, "TP53")
    rb1_mut = _is_mutated(rb1, "RB1")
    if tp53_mut and rb1_mut:
        return 1.00, "TP53 and RB1 altered"
    if tp53_mut:
        return 0.50, "TP53 altered only"
    if rb1_mut:
        return 0.30, "RB1 altered only"
    return 0.00, "TP53 and RB1 wild type"


def _score_stroma(stroma: object) -> tuple[float, str]:
    value = str(stroma or "").strip().lower()
    if value in {"low", "loose", "minimal", "normal"}:
        return 0.00, "Low or loose stromal descriptor"
    if value in {"dense", "severe", "high", "sclerotic", "fibrotic"}:
        return 1.00, "Dense or fibrotic stromal descriptor"
    if value in {"moderate", "intermediate", "moderate stroma"}:
        return 0.50, "Moderate stromal descriptor"
    raise ValueError(f"Unknown stromal descriptor: {stroma!r}")


def calculate_cri(pattern: object, tp53: object = "wt", rb1: object = "wt", stroma: object = "moderate") -> Dict[str, object]:
    """Return deterministic exploratory component scores and a research tier."""
    s_score, s_description = _score_pattern(pattern)
    g_score, g_description = _score_genomics(tp53, rb1)
    m_score, m_description = _score_stroma(stroma)
    cri = WEIGHTS["S"] * s_score + WEIGHTS["G"] * g_score + WEIGHTS["M"] * m_score
    if cri < 0.30:
        tier = "TIER 1 (EXPLORATORY LOW SCORE)"
    elif cri <= 0.65:
        tier = "TIER 2 (EXPLORATORY INTERMEDIATE SCORE)"
    else:
        tier = "TIER 3 (EXPLORATORY HIGH SCORE)"
    return {
        "S": round(s_score, 2),
        "G": round(g_score, 2),
        "M": round(m_score, 2),
        "CRI": round(cri, 3),
        "tier": tier,
        "desc_S": s_description,
        "desc_G": g_description,
        "desc_M": m_description,
    }


def _find_column(fieldnames: Sequence[str], candidates: Iterable[str]) -> Optional[str]:
    normalized = {field.strip().lower(): field for field in fieldnames}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    return None


def process_batch(input_path: str, output_path: Optional[str] = None, delimiter: Optional[str] = None) -> None:
    """Append research CRI components to a TSV or CSV file."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)
    if delimiter is None:
        delimiter = "," if input_path.lower().endswith(".csv") else "\t"
    with open(input_path, encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, delimiter=delimiter)
        if not reader.fieldnames:
            raise ValueError("Input file has no header row")
        fields = list(reader.fieldnames)
        pattern_column = _find_column(fields, ["pattern", "histology", "subtype", "growth_pattern", "histologic_subtype"])
        if pattern_column is None:
            raise ValueError("Input requires a pattern or histology column")
        tp53_column = _find_column(fields, ["tp53", "tp53_status", "tp53_mut", "p53"])
        rb1_column = _find_column(fields, ["rb1", "rb1_status", "rb1_mut"])
        stroma_column = _find_column(fields, ["stroma", "stromal_density", "desmoplasia", "ifp"])
        output_fields = fields + ["S_score", "G_score", "M_score", "CRI_Score", "Research_Tier"]
        destination: TextIO = open(output_path, "w", encoding="utf-8", newline="") if output_path else sys.stdout
        try:
            writer = csv.DictWriter(destination, fieldnames=output_fields, delimiter=delimiter)
            writer.writeheader()
            for row in reader:
                result = calculate_cri(
                    row.get(pattern_column, ""),
                    row.get(tp53_column, "wt") if tp53_column else "wt",
                    row.get(rb1_column, "wt") if rb1_column else "wt",
                    row.get(stroma_column, "moderate") if stroma_column else "moderate",
                )
                row.update({
                    "S_score": f"{result['S']:.2f}",
                    "G_score": f"{result['G']:.2f}",
                    "M_score": f"{result['M']:.2f}",
                    "CRI_Score": f"{result['CRI']:.3f}",
                    "Research_Tier": result["tier"],
                })
                writer.writerow(row)
        finally:
            if output_path:
                destination.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate an exploratory CRI research score.")
    parser.add_argument("--batch", "-b")
    parser.add_argument("--out", "-o")
    parser.add_argument("--delimiter", "-d", choices=["\t", ","])
    parser.add_argument("--pattern")
    parser.add_argument("--tp53", default="wt")
    parser.add_argument("--rb1", default="wt")
    parser.add_argument("--stroma", default="moderate")
    args = parser.parse_args()
    try:
        if args.batch:
            process_batch(args.batch, args.out, args.delimiter)
        elif args.pattern:
            print(calculate_cri(args.pattern, args.tp53, args.rb1, args.stroma))
        else:
            parser.error("provide --pattern or --batch")
    except (FileNotFoundError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
