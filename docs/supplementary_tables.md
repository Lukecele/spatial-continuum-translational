# Manuscript 2 Supplementary Tables

## Table S1. Cohort registry

Source: `data/registry.tsv` and `docs/dataset_review.md`.

| Cohort | Role | Unit | Main limitation |
| --- | --- | --- | --- |
| GSE342824 | Primary EGFR-TKI resistance Xenium cohort | patient/section/cell | Preprint-linked; raw Xenium expression is not included in the repository |
| GSE292469 | Primary TN/MRD/PD snRNA cohort | specimen/nucleus | Unmatched observational states |
| GSE301973 | Paired spatial case study | one patient/section | One patient only |
| GSE189487 | Independent spatial biology replication | six patients/spot | No treatment-response endpoint |
| TCGA-LUAD | Molecular/prognostic benchmark | patient | Not osimertinib-specific |
| TRACERx | Molecular/relapse context | patient/sample | Current RFS encoding is unsuitable for the first event model |

## Table S2. Primary cohort metadata audit

Source: `data/derived/treatment_cohort_metadata_audit.json`.

- Xenium: 1,400,257 cells; 465,959 tumour-flagged cells; 917,430 TN and
  482,827 PD cells.
- snRNA: 457,724 nuclei; 166,112 tumour-flagged nuclei; 266,448 TN, 60,013
  MRD, and 131,263 PD nuclei.

## Table S3. Frozen resistance signatures

Source: `data/resistance_signatures_v1.json` and
`data/derived/resistance_signatures_v1_panel_validation.json`.

All six frozen signatures have 100% requested-gene coverage in the GSE342824
Xenium panel. Numeric expression scores remain pending until gene-level matrices
are available; metadata-only proxies are kept separate.

## Table S4. Exploratory paired/state comparisons

Source: `data/derived/resistance_statistical_comparison.json`.

The Xenium analysis uses five TN/PD patient pairs. The snRNA comparison uses
sample-level unmatched TN/MRD/PD groups. All intervals and p-values are
exploratory and are not clinical treatment-effect estimates.

## Reproducibility

All tables can be regenerated from the scripts in `scripts/` and the derived
JSON outputs committed in `data/derived/`. Raw GEO and cBioPortal files are not
committed because of size and licensing constraints.
