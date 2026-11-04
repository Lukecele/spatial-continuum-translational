# Manuscript 2: Current Methods and Results Draft

## Methods status

The primary resistance analysis uses two public GEO series linked to the same
EGFR-mutant lung adenocarcinoma resistance study:

- GSE342824: Xenium in situ data from five patients with ten matched
  treatment-naive/progressive-disease sections.
- GSE292469: single-nucleus RNA-seq from 73 specimens represented by 74
libraries across treatment-naive, minimal residual disease, and progressive
disease states.

Metadata were downloaded from NCBI GEO and analyzed at sample/patient level.
Cell-level observations were not treated as independent patients. The linked
publication is currently a bioRxiv preprint (PMID 40654861).

Secondary support consists of GSE301973, GSE189487, TCGA-LUAD, and TRACERx.
These datasets are used for QC, biological replication, or prognostic context;
they are not substituted for an osimertinib-response validation cohort.

The software release is archived at the Zenodo concept DOI
`10.5281/zenodo.23956445`; the initial archived release is version `v0.1.0`
with DOI `10.5281/zenodo.23956462`.

## Results status

The GSE342824 metadata audit contains 1,400,257 cells, including 465,959
cells flagged as tumour. The sections include 917,430 TN cells and 482,827 PD
cells. EGFR mutation labels include activating variants and C797S; the C797S
signal is concentrated in one PD patient.

The GSE292469 metadata audit contains 457,724 nuclei: 266,448 TN, 60,013 MRD,
and 131,263 PD. Nine cell-type labels are available, including tumour,
fibroblast, endothelial, myeloid, lymphoid, plasma, epithelial, and mast-cell
classes. There are 166,112 tumour-flagged nuclei.

In paired Xenium metadata, PD samples show a lower mean tumour alveolar score
and higher mean neuroendocrine score than TN samples. These comparisons use five
patient pairs and remain exploratory. The snRNA state groups are unmatched and
observational.

The primary metadata audit contains 1,400,257 Xenium cells and 457,724 snRNA
nuclei. The snRNA states contain 28 TN, 14 MRD, and 31 PD samples. The paired
Xenium analysis estimates a mean PD-minus-TN alveolar-score difference of -1.10
and a neuroendocrine-score difference of +0.40; exact tests and bootstrap
intervals are recorded in the repository output. These estimates are not
clinical treatment effects.

## Interpretation boundary

These results support a testable spatial-plasticity hypothesis. They do not
prove that a pharmacological sanctuary causes recurrence, do not estimate
osimertinib efficacy, and do not support treatment recommendations.

## Required before submission

- Download or access the expression/count matrices only if needed for a
  pre-specified gene-level analysis.
- Freeze a resistance/plasticity gene set with verified literature roles.
- Add patient-level treatment and clinical outcome fields where available.
- Validate the primary findings in an independent treatment cohort.
- Report batch, tissue quality, missingness, and sensitivity to cell-type
  annotation.
- Replace all exploratory language only when a powered, externally validated
  analysis supports it.
