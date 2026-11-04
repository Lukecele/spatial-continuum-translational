# Data Ledger

This ledger defines the data actually used by the current Manuscript 2 pilot.

| Source | Local input | Unit of replication | Used for | Status |
| --- | --- | --- | --- | --- |
| GSE342824 | Xenium cell metadata and gene-panel metadata | patient/section | matched TN/PD metadata, mutation labels, cell composition, proxy signatures | complete |
| GSE292469 | snRNA cell metadata | specimen/sample | TN/MRD/PD composition, QC, sample-level statistics | complete |
| GSE189487 | six 10x spatial matrices and coordinates | patient/section | independent signature detection replication | complete |
| GSE301973 | one extracted paired spatial case | one patient/section | structural QC and single-case hypothesis generation | complete |
| cBioPortal TRACERx | clinical and focused mutation API data | patient/sample | relapse and molecular context | complete, not used as primary event model |
| cBioPortal TCGA-LUAD | clinical, mutation, and RNA metadata/API data | patient | exploratory DFS Cox baseline | complete |
| cBioPortal GIST | clinical, RFS, and KIT/PDGFRA mutation API data | patient | exploratory GIST feature validation | complete |

## Explicit non-inputs

- The 82 GB GSE342824 Xenium raw archive is not required for the current
  metadata/proxy pilot.
- The 12.5 GB GSE292469 counts matrix was not retained after the NCBI server
  repeatedly returned `503`; no gene-level score is claimed from it.
- No cell is treated as an independent patient.
- No treatment recommendation is derived from any current output.

## Reproducibility entry points

- `scripts/audit_treatment_metadata.py`
- `scripts/analyze_resistance_metadata.py`
- `scripts/statistical_resistance_comparison.py`
- `scripts/analyze_snrna_composition.py`
- `scripts/validate_primary_cohort.py`
- `scripts/apply_signature_proxies.py`
- `scripts/generate_resistance_figures.py`

Derived reports are stored in `data/derived/`; raw source files remain outside
Git because of size and source-distribution constraints.
