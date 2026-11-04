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
- The exploratory histology summary has two samples per AIS, MIA, and IAC group;
	`CA9` is higher in the IAC pair while `COL1A1` is high across groups. These
	observations are QC signals only and are not statistical stage comparisons.

## Treatment-resistance primary cohorts

### `GSE342824` Xenium in situ

- Five EGFR-mutant LUAD patients with ten matched treatment-naive/progressive
	disease sections.
- GEO reports 1,516,917 segmented cells and 1,400,257 cells passing the
	annotation threshold.
- URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE342824

### `GSE292469` single-nucleus RNA-seq

- 73 EGFR-mutant LUAD specimens represented by 74 libraries across TN, MRD on
	EGFR-TKI therapy, and PD states.
- GEO reports 457,724 QC-passing nuclei; clinical annotations cover all samples
	and MSK-IMPACT profiling is available for 68 specimens.
- URL: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE292469

The linked evidence is PMID 40654861, currently a bioRxiv preprint. These are
the primary treatment-resistance cohorts for Manuscript 2; peer-reviewed status
and exact patient-level treatment metadata still require separate verification.

Metadata audit confirms 1,400,257 Xenium cells in GSE342824, including 465,959
tumour-flagged cells and TN/PD counts of 917,430/482,827. GSE292469 contains
457,724 nuclei across TN/MRD/PD counts of 266,448/60,013/131,263, with nine
cell-type annotations and 166,112 tumour-flagged nuclei. The Xenium metadata
also exposes EGFR mutation labels, including C797S, making this the first cohort
in the project with a direct resistance-state spatial design.

The first sample-level metadata analysis is descriptive: Xenium PD samples show
lower mean tumour alveolar scores and higher mean neuroendocrine scores than TN
samples, while the `C797S` signal is concentrated in one PD patient. The snRNA
metadata contains 14 MRD, 31 PD, and 28 TN samples. These are hypothesis signals;
the units of replication are samples/patients, not cells, and the raw expression
matrices have not yet been modeled.
- Cross-dataset detection-fraction integration identifies broadly replicated
	genes (`COL1A1`, `COL1A2`, `COL3A1`, `DCN`, `LUM`, `EGFR`, `PECAM1`, `VWF`) and
	platform-sensitive genes (`CA9`, `HIF1A`, `KDR`, `RAMP2`). `LDHA` is absent in
	the GSE301973 case despite being detected in all six GSE189487 samples, so it
	is not treated as a replicated feature.

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
