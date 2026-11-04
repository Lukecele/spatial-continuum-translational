#!/usr/bin/env python3
"""Create an aggregate summary from the local cBioPortal downloads."""

import json
from pathlib import Path

ROOT = Path("data/raw/cbioportal")
OUTPUT = Path("data/derived/benchmark_summary.tsv")
GENES = ("EGFR", "TP53", "RB1")
ENDPOINTS = {"DFS_MONTHS", "DFS_STATUS", "PFS_MONTHS", "PFS_STATUS", "OS_MONTHS", "OS_STATUS", "RFS_MONTHS", "RFS_STATUS"}


def summarize(study_dir: Path) -> list[str]:
    clinical = json.loads((study_dir / "clinical_patient.json").read_text())
    mutations = json.loads((study_dir / "mutations_egfr_tp53_rb1.json").read_text())
    patients = {row["patientId"] for row in clinical}
    endpoint_patients = {
        row["patientId"] for row in clinical if row["clinicalAttributeId"] in ENDPOINTS
    }
    rows = []
    for gene in GENES:
        gene_patients = {row["patientId"] for row in mutations if row["gene"] == gene}
        rows.append(
            "\t".join(
                [
                    study_dir.name,
                    gene,
                    str(len(patients)),
                    str(len(gene_patients)),
                    str(len(endpoint_patients)),
                ]
            )
        )
    return rows


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rows = ["study_id\tgene\tclinical_patients\tmutated_patients\tendpoint_patients"]
    for study_dir in sorted(ROOT.iterdir()):
        if study_dir.is_dir():
            rows.extend(summarize(study_dir))
    OUTPUT.write_text("\n".join(rows) + "\n")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
