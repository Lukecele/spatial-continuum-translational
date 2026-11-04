# Dataset Review: 2026-11-04

Metadata was checked through NCBI GEO records using the GEO accessions below.
This is a metadata review, not a quality-control or outcome validation.

## GSE301973

- Title: The spatial transcriptomics of EGFR-mutant non-small cell lung cancer before osimertinib treatment.
- Platform/context: Visium HD spatial transcriptomics, pre-treatment EGFR-mutant NSCLC.
- Samples reported by GEO: `GSM9093278` and `GSM9093279`.
- Role: paired spatial case study, not a discovery cohort.
- URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE301973
- Linked publication: PMID 41152910.
- Limitation: GEO describes one patient with paired pre/post-treatment sections;
	the sample titles and protocol must be reconciled before analysis. The dataset
	cannot support model training, population-level inference, or external validation.

## GSE189487

- Title: Spatiotemporal transcriptional atlas of lung adenocarcinoma from adenocarcinoma in situ to invasive carcinoma.
- Platform/context: spatial transcriptomics with single-cell integration.
- Role: independent biological spatial cohort, not a treatment-outcome validation cohort.
- URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE189487
- Limitation: disease progression is not equivalent to osimertinib response or recurrence.

## GSE176078

- Title: A single-cell and spatially resolved atlas of human breast cancers.
- Role: later cross-tumour translation phase.
- URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE176078
- Limitation: outside the first NSCLC pilot.

## cBioPortal clinical benchmarks

### `nsclc_tracerx_2017`

- Study: Non-Small Cell Lung Cancer (TRACERx, NEJM & Nature 2017).
- Available data: 447 samples, mutation profile, adjuvant-treatment attribute,
  and patient-level relapse-free status/months.
- URL: https://www.cbioportal.org/study/summary?id=nsclc_tracerx_2017
- Role: clinical benchmark for molecular association and relapse analysis.
- Limitation: not an osimertinib-specific treatment cohort.

### `luad_tcga_pan_can_atlas_2018`

- Study: Lung Adenocarcinoma (TCGA, PanCancer Atlas).
- Available data: 566 samples, mutation and RNA profiles, DFS/PFS/OS attributes.
- URL: https://www.cbioportal.org/study/summary?id=luad_tcga_pan_can_atlas_2018
- Role: independent molecular and prognostic benchmark.
- Limitation: treatment history is insufficient for an osimertinib efficacy claim.
