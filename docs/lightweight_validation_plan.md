# Lightweight Validation Plan

This is the executable validation path for the current Manuscript 2 pilot. It
uses public metadata, precomputed spatial annotations, sample-level clinical
records, and focused mutation data. It does not require the 12 GB snRNA count
matrix or the 82 GB Xenium raw archive.

## Inputs

- GSE342824 Xenium cell metadata and gene-panel metadata.
- GSE292469 snRNA cell metadata.
- GSE189487 spatial matrices and coordinates.
- GSE301973 extracted spatial case.
- cBioPortal TCGA-LUAD and TRACERx clinical/mutation downloads.
- Verified PubMed/GEO provenance in `evidence/` and `docs/dataset_review.md`.

## Validated outputs

- cohort structural checks;
- patient/sample-level TN/PD and TN/MRD/PD comparisons;
- cell-type composition analysis;
- Xenium metadata proxies for tumour, basal, neuroendocrine, and EGFR/MAPK
  context;
- independent spatial detection-fraction replication;
- exploratory TCGA DFS Cox baseline;
- reproducible figures and manuscript tables.

## Claims allowed

The lightweight analysis can support:

- feasibility of an evidence-linked computational framework;
- descriptive association of treatment state with spatial/cellular metadata;
- hypothesis generation for lineage plasticity and compartment changes;
- reproducible data and analysis provenance.

It cannot support:

- a gene-expression signature score when counts are unavailable;
- an individual recurrence prediction;
- a treatment recommendation;
- a causal sanctuary claim;
- osimertinib efficacy estimation.

## Reproduction

Run the repository test suite and the metadata scripts after the public raw
metadata have been downloaded locally. All derived reports must retain the
sample/patient unit of replication and must not treat cells as independent
patients.

The full count matrix remains an optional enhancement for a later gene-level
analysis. It is not required to reproduce the current pilot conclusions.
