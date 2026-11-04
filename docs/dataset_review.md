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
- QC of the extracted A archive: 45,661 annotated cells, 18,111 genes, 11,222,500
	2um coordinate rows, and one integrated sample label (`A`).
- Signature QC: stromal genes such as `COL1A1` and `COL3A1` are broadly detected;
	hypoxia and vascular genes are sparse, and `LDHA` is absent. No composite
	signature score is therefore treated as validated from this case.
- Cell-type stratification is biologically coherent at a descriptive level:
	`COL1A1` is highest in stromal cells, `PECAM1` is most detected in endothelial
	cells, and `EGFR` is relatively more detected in tumour cells. `CA9` remains
	rare across all annotations.
- Six-nearest-neighbour analysis shows tumour-to-tumour contact enrichment of
	2.31x and stromal-to-stromal enrichment of 3.78x relative to global cell-type
	frequencies. Tumour-to-stroma contacts are 0.31x expected. These are
	descriptive single-sample findings, not evidence of a clinical sanctuary.

## GSE189487

- Title: Spatiotemporal transcriptional atlas of lung adenocarcinoma from adenocarcinoma in situ to invasive carcinoma.
- Platform/context: spatial transcriptomics with single-cell integration.
- Role: independent biological spatial cohort, not a treatment-outcome validation cohort.
- URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE189487
- Limitation: disease progression is not equivalent to osimertinib response or recurrence.

## GSE189487 replication cohort

- Title: Spatiotemporal transcriptional atlas of lung adenocarcinoma from
	adenocarcinoma in situ to invasive carcinoma.
- Samples: six spatial samples from six treatment-naive patients, spanning AIS,
	MIA, and IAC histological groups.
- Linked publication: PMID 36434043.
- URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE189487
- Role: independent biological replication of cell-type and neighborhood
	signatures, not an osimertinib-response cohort.
- Limitation: the cohort has no direct recurrence endpoint in the GEO metadata.
- Initial replication QC covers all six samples: 1,140-4,992 in-tissue barcodes
	per section. Representative detection ranges are `CA9` 0.06-1.07%, `PECAM1`
	32.7-87.2%, `COL1A1` 54.3-91.5%, and `EGFR` 31.0-60.0%. These ranges are
	descriptive only; platform and tissue-composition normalization is still
	required before comparing histological groups.

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
