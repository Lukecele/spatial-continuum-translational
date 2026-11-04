#!/usr/bin/env python3
"""Audit endpoint and treatment heterogeneity before clinical pooling."""

import json
from pathlib import Path

OUTPUT = Path("data/derived/cohort_heterogeneity_audit.json")

COHORTS = [
    {
        "cohort": "GSE342824_GSE292469",
        "tumor": "EGFR-mutant LUAD",
        "treatment_context": "EGFR-TKI resistance states",
        "endpoint": "TN/MRD/PD metadata",
        "unit": "patient/specimen",
        "pooling_allowed": False,
        "reason": "No common recurrence endpoint",
    },
    {
        "cohort": "luad_tcga_pan_can_atlas_2018",
        "tumor": "LUAD",
        "treatment_context": "heterogeneous historical treatment",
        "endpoint": "DFS/PFS/OS",
        "unit": "patient",
        "pooling_allowed": False,
        "reason": "Not osimertinib-specific",
    },
    {
        "cohort": "nsclc_tracerx_2017",
        "tumor": "NSCLC",
        "treatment_context": "heterogeneous adjuvant context",
        "endpoint": "RFS/ctDNA context",
        "unit": "patient/sample",
        "pooling_allowed": False,
        "reason": "Endpoint encoding and treatment context differ",
    },
    {
        "cohort": "gist_msk_2023",
        "tumor": "GIST",
        "treatment_context": "heterogeneous clinical treatment",
        "endpoint": "RFS/OS",
        "unit": "patient",
        "pooling_allowed": False,
        "reason": "Different tumor and endpoint from lung cohorts",
    },
    {
        "cohort": "skcm_broad_brafresist_2012",
        "tumor": "BRAF-mutant melanoma",
        "treatment_context": "vemurafenib/dabrafenib",
        "endpoint": "response/early resistance",
        "unit": "patient",
        "pooling_allowed": False,
        "reason": "Response endpoint and tumor context differ",
    },
]


def main():
    report = {
        "cohorts": COHORTS,
        "pooled_clinical_model_allowed": False,
        "reason": "Cohort-specific estimands and endpoints must be preserved.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"cohorts": len(COHORTS), "pooled_clinical_model_allowed": False}, indent=2))


if __name__ == "__main__":
    main()
