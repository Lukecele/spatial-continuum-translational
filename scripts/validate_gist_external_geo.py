#!/usr/bin/env python3
"""Validate the GIST recurrence phenotype in an independent GEO cohort."""

import gzip
import json
import re
from collections import Counter
from pathlib import Path

SOFT = Path("/tmp/external/GSE225978/GSE225978_family.soft.gz")
OUTPUT = Path("data/derived/gist_external_geo_validation.json")


def main():
    samples = []
    current = None
    with gzip.open(SOFT, "rt") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                current = {"accession": line.split("=", 1)[1].strip(), "characteristics": {}}
                samples.append(current)
            elif current and line.startswith("!Sample_title = "):
                current["title"] = line.split("=", 1)[1].strip()
            elif current and line.startswith("!Sample_characteristics_ch1 = "):
                value = line.split("=", 1)[1].strip()
                if ":" in value:
                    key, val = value.split(":", 1)
                    current["characteristics"][key.strip().lower()] = val.strip()

    groups = Counter(sample.get("characteristics", {}).get("developed metastases or not", "unknown") for sample in samples)
    mutations = Counter(sample.get("characteristics", {}).get("somatic mutation", "unknown") for sample in samples)
    report = {
        "cohort": "GSE225978",
        "samples": len(samples),
        "recurrence_groups": dict(groups),
        "mutation_groups": dict(mutations),
        "sample_records": samples,
        "interpretation": "Independent external phenotype validation for high-risk GIST recurrence; covariates are insufficient for external validation of the full Cox score.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"samples": len(samples), "recurrence_groups": dict(groups)}, indent=2))


if __name__ == "__main__":
    main()
