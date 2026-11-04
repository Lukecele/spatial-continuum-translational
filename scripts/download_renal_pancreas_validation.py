#!/usr/bin/env python3
"""Download patient clinical data for renal and pancreatic trial cohorts."""

import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://www.cbioportal.org/api"
STUDIES = {
    "rcc_iatlas_immotion150_2018": "Immotion150",
    "paad_iatlas_prince_2022": "PRINCE",
}
OUTPUT = Path("data/raw/cbioportal/renal_pancreas")


def get(path, params):
    request = Request(f"{BASE}{path}?{urlencode(params)}", headers={"User-Agent": "spatial-continuum-translational/0.1"})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def paged(path, params):
    rows = []
    page = 0
    while True:
        batch = get(path, {**params, "pageSize": 1000, "pageNumber": page})
        rows.extend(batch)
        if len(batch) < 1000:
            return rows
        page += 1


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for study, label in STUDIES.items():
        rows = paged(f"/studies/{study}/clinical-data", {"clinicalDataType": "PATIENT"})
        path = OUTPUT / f"{study}_clinical_patient.json"
        path.write_text(json.dumps(rows, indent=2) + "\n")
        manifest[study] = {"label": label, "clinical_rows": len(rows)}
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
