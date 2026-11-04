#!/usr/bin/env python3
"""Download focused metastatic breast treatment-response data."""

import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = "https://www.cbioportal.org/api"
STUDY = "brca_mskcc_2019"
SAMPLE_LIST = "brca_mskcc_2019_all"
GENES = {"PIK3CA": 5290, "ESR1": 2099, "CCNE1": 898, "RB1": 5925}
OUTPUT = Path("data/raw/cbioportal/brca_mskcc_2019")


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
    clinical = paged(f"/studies/{STUDY}/clinical-data", {"clinicalDataType": "PATIENT"})
    mutations = []
    for gene, entrez_id in GENES.items():
        for row in paged(f"/molecular-profiles/{STUDY}_mutations/mutations", {"sampleListId": SAMPLE_LIST, "entrezGeneId": entrez_id}):
            mutations.append({"gene": gene, **row})
    (OUTPUT / "clinical_patient.json").write_text(json.dumps(clinical, indent=2) + "\n")
    (OUTPUT / "mutations_pik3ca_esr1_ccne1_rb1.json").write_text(json.dumps(mutations, indent=2) + "\n")
    (OUTPUT / "manifest.json").write_text(json.dumps({"study": STUDY, "clinical_rows": len(clinical), "mutation_rows": len(mutations), "genes": GENES}, indent=2) + "\n")
    print(json.dumps({"clinical_rows": len(clinical), "mutation_rows": len(mutations)}, indent=2))


if __name__ == "__main__":
    main()
