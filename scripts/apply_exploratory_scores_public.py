#!/usr/bin/env python3
"""Apply frozen exploratory signatures to public expression matrices.

This produces descriptive scores only. It never fits genes, weights, thresholds,
or clinical models on the analyzed cohort.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import re
from collections import defaultdict
from pathlib import Path


SCORES = {
    "melanoma_braf_mapk_escape": {"AXL": 1, "NGFR": 1, "WNT5A": 1, "EGFR": 1, "PDGFRB": 1, "JUN": 1, "FOS": 1},
    "breast_pi3k_pathway_activity": {"PIK3CA": 1, "AKT1": 1, "PDPK1": 1, "MTOR": 1, "RPS6KB1": 1, "EIF4EBP1": 1, "PTEN": -1},
    "pancreas_stromal_immune_exclusion": {"COL1A1": 1, "COL3A1": 1, "COL5A1": 1, "FAP": 1, "CXCL12": 1, "TGFB1": 1, "SPP1": 1, "CSF1": 1},
}
ENSEMBL = {
    "AXL": "ENSG00000167601", "NGFR": "ENSG00000064393", "WNT5A": "ENSG00000114251", "EGFR": "ENSG00000146648", "PDGFRB": "ENSG00000113721", "JUN": "ENSG00000177606", "FOS": "ENSG00000170345",
    "PIK3CA": "ENSG00000121879", "AKT1": "ENSG00000142208", "PDPK1": "ENSG00000140992", "MTOR": "ENSG00000198793", "RPS6KB1": "ENSG00000108443", "EIF4EBP1": "ENSG00000187840", "PTEN": "ENSG00000171862",
    "COL1A1": "ENSG00000108821", "COL3A1": "ENSG00000168542", "COL5A1": "ENSG00000130635", "FAP": "ENSG00000078098", "CXCL12": "ENSG00000107562", "TGFB1": "ENSG00000105329", "SPP1": "ENSG00000118785", "CSF1": "ENSG00000184371",
}


def zscores(values: list[float]) -> list[float]:
    mean = sum(values) / len(values) if values else 0.0
    variance = sum((value - mean) ** 2 for value in values) / len(values) if values else 0.0
    sd = math.sqrt(variance)
    return [(value - mean) / sd if sd else 0.0 for value in values]


def score_matrix(matrix: dict[str, dict[str, float]], score_name: str) -> list[dict]:
    weights = SCORES[score_name]
    samples = sorted(matrix)
    gene_z: dict[str, dict[str, float]] = {}
    for gene in weights:
        raw = [matrix[sample].get(gene) for sample in samples]
        if sum(value is not None for value in raw) < max(2, math.ceil(len(samples) * 0.8)):
            continue
        present = [value if value is not None else 0.0 for value in raw]
        gene_z[gene] = dict(zip(samples, zscores(present)))
    rows = []
    for sample in samples:
        available = [gene for gene in weights if gene in gene_z]
        score = sum(gene_z[gene][sample] * weights[gene] for gene in available) / len(available) if available else None
        rows.append({"sample": sample, "score": score, "genes_available": available, "gene_count": len(available)})
    return rows


def pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) < 2:
        return None
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum((a - left_mean) * (b - right_mean) for a, b in zip(left, right))
    left_sd = math.sqrt(sum((a - left_mean) ** 2 for a in left))
    right_sd = math.sqrt(sum((b - right_mean) ** 2 for b in right))
    return numerator / (left_sd * right_sd) if left_sd and right_sd else None


def sensitivity(matrix: dict[str, dict[str, float]], score_name: str) -> dict:
    baseline = {row["sample"]: row["score"] for row in score_matrix(matrix, score_name)}
    genes = list(SCORES[score_name])
    leave_one_out = {}
    for gene in genes:
        reduced = {sample: {key: value for key, value in values.items() if key != gene} for sample, values in matrix.items()}
        changed = {row["sample"]: row["score"] for row in score_matrix(reduced, score_name)}
        pairs = [(baseline[sample], changed[sample]) for sample in baseline if baseline[sample] is not None and changed.get(sample) is not None]
        leave_one_out[gene] = {
            "samples_compared": len(pairs),
            "pearson_with_baseline": pearson([pair[0] for pair in pairs], [pair[1] for pair in pairs]),
            "mean_absolute_change": sum(abs(pair[0] - pair[1]) for pair in pairs) / len(pairs) if pairs else None,
        }
    return {"normalization": "gene-wise z-score within dataset", "leave_one_gene_out": leave_one_out}


def parse_soft_titles(path: Path) -> dict[str, dict]:
    records = {}
    current = None
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                current = {"accession": line.split("=", 1)[1].strip()}
            elif current and line.startswith("!Sample_title = "):
                current["title"] = line.split("=", 1)[1].strip()
                records[current["accession"]] = current
                title = current["title"]
                state_match = re.search(r"Patient\s+(\d+)\s+(PRE|EDT|PROG)\s+(.+)", title, re.IGNORECASE)
                if state_match:
                    current["patient"] = state_match.group(1)
                    current["state"] = state_match.group(2).upper()
                    current["treatment"] = state_match.group(3).strip()
                alias = title.split()[0] if title else ""
                if alias and alias != current["accession"]:
                    records[alias] = current
            elif current and line.startswith("!Sample_characteristics_ch1 = "):
                value = line.split("=", 1)[1].strip()
                if ":" in value:
                    key, item = value.split(":", 1)
                    current[key.strip().lower()] = item.strip()
    return records


def parse_gpl(path: Path) -> dict[str, str]:
    mapping = {}
    in_table = False
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\r\n")
            if line == "!platform_table_begin":
                in_table = True
                header = next(handle).rstrip("\r\n").split("\t")
                continue
            if in_table and line == "!platform_table_end":
                break
            if in_table:
                values = line.split("\t")
                if values and len(values) >= len(header):
                    row = dict(zip(header, values))
                    if row.get("ID") and row.get("Symbol"):
                        mapping[row["ID"]] = row["Symbol"].strip()
    return mapping


def parse_gse99898(matrix_path: Path, platform_path: Path, soft_path: Path) -> tuple[dict, dict]:
    probe_to_gene = parse_gpl(platform_path)
    metadata = parse_soft_titles(soft_path)
    matrix: dict[str, dict[str, float]] = defaultdict(dict)
    sample_ids: list[str] = []
    in_table = False
    with gzip.open(matrix_path, "rt", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if line == "!series_matrix_table_begin":
                header = next(csv.reader([next(handle)], delimiter="\t"))
                sample_ids = [item.strip('"') for item in header[1:]]
                in_table = True
                continue
            if in_table and line == "!series_matrix_table_end":
                break
            if in_table:
                values = next(csv.reader([line], delimiter="\t"))
                probe = values[0].strip('"')
                gene = probe_to_gene.get(probe, "").upper()
                if gene in {g for genes in SCORES.values() for g in genes}:
                    for sample, value in zip(sample_ids, values[1:]):
                        try:
                            matrix[sample][gene] = max(matrix[sample].get(gene, float("-inf")), float(value.strip('"')))
                        except ValueError:
                            pass
    meta = {sample: metadata.get(sample, {}) for sample in sample_ids}
    return matrix, meta


def parse_gse196434(raw_path: Path, soft_path: Path) -> tuple[dict, dict]:
    metadata = parse_soft_titles(soft_path)
    for record in metadata.values():
        if record.get("sample_class") and not record.get("state"):
            record["state"] = record["sample_class"].split()[0].upper()
        patient_match = re.search(r"\[pt([^\]]+)\]", record.get("title", ""), re.IGNORECASE)
        if patient_match:
            record["patient"] = patient_match.group(1)
    wanted_ids = {ENSEMBL[gene] for genes in SCORES.values() for gene in genes}
    matrix: dict[str, dict[str, float]] = defaultdict(dict)
    with gzip.open(raw_path, "rt", encoding="utf-8", errors="replace") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        samples = header[1:]
        for row in reader:
            gene_id = row[0].split(".", 1)[0]
            if gene_id not in wanted_ids:
                continue
            gene = next(g for g, identifier in ENSEMBL.items() if identifier == gene_id)
            for sample, value in zip(samples, row[1:]):
                try:
                    matrix[sample][gene] = math.log2(float(value) + 1.0)
                except ValueError:
                    pass
    return matrix, {sample: metadata.get(sample, {}) for sample in samples}


def parse_prince(root: Path) -> tuple[dict, dict]:
    metadata_path = root / "RNAseq" / "NatureMed_GX_ph2_metadata.csv"
    clinical_path = root / "Clinical" / "PICI0002_ph2_clinical.csv"
    clinical = {}
    with clinical_path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            clinical[row["Deidentified.ID"]] = row
    matrix: dict[str, dict[str, float]] = {}
    meta = {}
    with metadata_path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            patient = row["Deidentified.ID"]
            filename = row["Filename"]
            path = root / "RNAseq" / "Data" / filename
            if not path.exists():
                continue
            values = {}
            with path.open(newline="", encoding="utf-8-sig") as expression:
                for gene_row in csv.DictReader(expression, delimiter="\t"):
                    gene = gene_row.get("Gene Symbol", "").upper()
                    if gene in SCORES["pancreas_stromal_immune_exclusion"]:
                        try:
                            values[gene] = math.log2(float(gene_row["TPM"]) + 1.0)
                        except (KeyError, ValueError):
                            pass
            sample = row["sample.id"]
            matrix[sample] = values
            meta[sample] = {"patient": patient, "arm": clinical.get(patient, {}).get("Arm"), "state": row.get("timepoint.id")}
    return matrix, meta


def build_report(name: str, matrix: dict, meta: dict, score_name: str) -> dict:
    rows = score_matrix(matrix, score_name)
    for row in rows:
        row.update(meta.get(row["sample"], {}))
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        group = row.get("arm") if name == "PRINCE" else row.get("state")
        group = group or "unknown"
        if row["score"] is not None:
            grouped[group].append(row["score"])
    summary = {group: {"n": len(values), "mean": sum(values) / len(values), "min": min(values), "max": max(values)} for group, values in grouped.items()}
    paired_deltas = []
    by_patient = defaultdict(dict)
    for row in rows:
        if row.get("patient") and row.get("state"):
            by_patient[row["patient"]][row["state"]] = row["score"]
    for patient, states in by_patient.items():
        if states.get("PRE") is not None and states.get("PROG") is not None:
            paired_deltas.append({"patient": patient, "pre_to_prog_delta": states["PROG"] - states["PRE"]})
    return {
        "dataset": name,
        "score": score_name,
        "samples": len(rows),
        "summary": summary,
        "paired_pre_to_prog": paired_deltas,
        "sensitivity": sensitivity(matrix, score_name),
        "rows": rows,
        "interpretation": "Exploratory descriptive score; no outcome fitting or external refitting.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gse99898-matrix", type=Path)
    parser.add_argument("--gse99898-platform", type=Path)
    parser.add_argument("--gse99898-soft", type=Path)
    parser.add_argument("--gse196434-raw", type=Path)
    parser.add_argument("--gse196434-soft", type=Path)
    parser.add_argument("--prince-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    reports = []
    if args.gse99898_matrix and args.gse99898_platform and args.gse99898_soft:
        matrix, meta = parse_gse99898(args.gse99898_matrix, args.gse99898_platform, args.gse99898_soft)
        reports.append(build_report("GSE99898", matrix, meta, "melanoma_braf_mapk_escape"))
    if args.gse196434_raw and args.gse196434_soft:
        matrix, meta = parse_gse196434(args.gse196434_raw, args.gse196434_soft)
        reports.append(build_report("GSE196434", matrix, meta, "melanoma_braf_mapk_escape"))
    if args.prince_root:
        matrix, meta = parse_prince(args.prince_root)
        reports.append(build_report("PRINCE", matrix, meta, "pancreas_stromal_immune_exclusion"))
    if not reports:
        raise SystemExit("No complete dataset input set provided")
    result = {"version": "exploratory-tumor-scores-v1", "reports": reports}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({report["dataset"]: report["summary"] for report in reports}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
