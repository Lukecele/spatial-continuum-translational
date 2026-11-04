#!/usr/bin/env python3
"""Download focused public benchmark data from cBioPortal."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://www.cbioportal.org/api"
GENES = {"EGFR": 1956, "TP53": 7157, "RB1": 5925}
STUDIES = {
    "nsclc_tracerx_2017": "nsclc_tracerx_2017_sequenced",
    "luad_tcga_pan_can_atlas_2018": "luad_tcga_pan_can_atlas_2018_cnaseq",
}


def get_json(path: str, params: dict[str, str]) -> list | dict:
    query = urlencode(params)
    request = Request(f"{BASE_URL}{path}?{query}", headers={"User-Agent": "spatial-continuum-translational/0.1"})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def get_paged(path: str, params: dict[str, str]) -> list:
    page_size = 1000
    rows = []
    page = 0
    while True:
        page_rows = get_json(path, {**params, "pageSize": str(page_size), "pageNumber": str(page)})
        if not isinstance(page_rows, list):
            raise RuntimeError(f"Expected a list from {path}")
        rows.extend(page_rows)
        if len(page_rows) < page_size:
            return rows
        page += 1


def download_study(study_id: str, sample_list_id: str, output_root: Path) -> None:
    study_dir = output_root / study_id
    study_dir.mkdir(parents=True, exist_ok=True)

    clinical = get_paged(
        f"/studies/{study_id}/clinical-data",
        {"clinicalDataType": "PATIENT"},
    )
    (study_dir / "clinical_patient.json").write_text(json.dumps(clinical, indent=2) + "\n")

    mutation_rows = []
    profile_id = f"{study_id}_mutations"
    for gene_name, entrez_gene_id in GENES.items():
        rows = get_paged(
            f"/molecular-profiles/{profile_id}/mutations",
            {"sampleListId": sample_list_id, "entrezGeneId": str(entrez_gene_id)},
        )
        for row in rows:
            mutation_rows.append({"gene": gene_name, **row})

    (study_dir / "mutations_egfr_tp53_rb1.json").write_text(json.dumps(mutation_rows, indent=2) + "\n")
    manifest = {
        "study_id": study_id,
        "sample_list_id": sample_list_id,
        "genes": GENES,
        "clinical_rows": len(clinical),
        "mutation_rows": len(mutation_rows),
        "source": "https://www.cbioportal.org/api",
    }
    (study_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/raw/cbioportal"))
    args = parser.parse_args()

    for study_id, sample_list_id in STUDIES.items():
        download_study(study_id, sample_list_id, args.output)
        print(f"Downloaded {study_id} -> {args.output / study_id}")


if __name__ == "__main__":
    main()
