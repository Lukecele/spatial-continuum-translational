# Evidence-linked Spatial and Treatment-State Features in EGFR-Mutant Lung Adenocarcinoma

## Abstract

### Background

Resistance to EGFR tyrosine-kinase inhibitors can involve molecular evolution,
cell-state plasticity, and spatial reorganization. A reproducible comparison of
these features requires treatment-state metadata, patient-level units of
replication, and an explicit separation between exploratory biology and clinical
prediction.

### Methods

We assembled public GEO and cBioPortal resources around an EGFR-mutant lung
adenocarcinoma resistance cohort. The primary datasets were GSE342824, a
Xenium in situ cohort with matched treatment-naive and progressive-disease
sections from five patients, and GSE292469, a single-nucleus cohort with
TN/MRD/PD metadata. We audited sample structure, cell annotations, mutation
labels, and quality fields. We froze six panel-aware resistance signatures and
used metadata proxies only where gene-level counts were unavailable. Paired
Xenium differences and sample-level TN/MRD/PD comparisons were treated as
exploratory.

### Results

GSE342824 contained 1,400,257 annotated cells, including 465,959
 tumour-flagged cells, across five complete TN/PD pairs. GSE292469 contained
457,724 nuclei across 28 TN, 14 MRD, and 31 PD samples. The paired Xenium
metadata showed a mean PD-minus-TN decrease of 1.10 in the tumour alveolar
score and an increase of 0.40 in the neuroendocrine score. The linked EGFR
mutation metadata included C797S, concentrated in one PD patient. These results
are hypothesis-generating and are not treatment-effect estimates.

### Conclusions

The primary cohorts and analysis contracts support a reproducible pilot of
spatial treatment-state biology. Gene-level signature scores, external clinical
validation, and prospective treatment inference remain necessary before clinical
claims are possible.

## Introduction

EGFR-mutant lung adenocarcinoma is a model system for studying targeted-therapy
resistance because treatment states can be related to both molecular alterations
and cellular phenotypes. The relevant unit of evidence is not a single cell in
isolation: samples and patients define the experimental replication structure.

The present study extends the spatial-continuum framework toward a treatment-
state analysis. It asks whether public spatial and single-nucleus metadata can
reveal reproducible changes in epithelial lineage state, EGFR/MAPK context,
and tumour composition between treatment-naive, minimal-residual-disease, and
progressive-disease samples.

The study is deliberately not framed as a clinical decision rule. A spatial
pattern may motivate a mechanistic hypothesis without proving a pharmacological
sanctuary, predicting recurrence, or demonstrating treatment efficacy.

## Materials and Methods

### Cohorts

The primary resistance cohorts were:

- GSE342824: ten Xenium sections from five EGFR-mutant LUAD patients, matched
  between treatment-naive and progressive disease.
- GSE292469: 74 libraries representing 73 specimens across TN, MRD, and PD,
  with clinical annotations and MSK-IMPACT metadata available for most
  specimens.

GSE301973 and GSE189487 were used as spatial QC and biological replication
resources. TCGA-LUAD and TRACERx were used as molecular/prognostic context, not
as osimertinib efficacy cohorts.

### Data processing and quality control

Metadata were downloaded from NCBI GEO and parsed with versioned scripts. Cell-
level fields were summarized at sample and patient level. The structural gate
required five complete Xenium TN/PD pairs, all three snRNA treatment states, and
consistent C797S localization in the available metadata.

The repository stores derived JSON reports and scripts. Large raw GEO archives
are not committed. All analyses report the raw source accession and the unit of
replication.

### Frozen resistance signatures

The `resistance-signatures-v1` definition contains six panel-aware signatures:

1. tumour epithelial identity;
2. basal plasticity;
3. neuroendocrine plasticity;
4. EGFR/MAPK resistance;
5. hypoxia/stress;
6. vascular access.

All requested genes are present in the GSE342824 Xenium panel. Metadata proxies
are explicitly labeled as proxies. No gene-expression score is calculated when
only metadata are available.

### Statistical analysis

For Xenium, TN and PD sections were paired by patient. Differences were
calculated as PD minus TN, with exact Wilcoxon tests and fixed-seed bootstrap
intervals used only as exploratory summaries. For snRNA, sample-level TN/MRD/PD
groups were summarized with Kruskal-Wallis diagnostics. Cells and nuclei were
never treated as independent patients.

## Results

### Primary cohort structure

The GSE342824 audit identified 1,400,257 cells, of which 465,959 were flagged as
tumour. The sections contained 917,430 TN cells and 482,827 PD cells. Five
patients had complete TN/PD pairs.

GSE292469 contained 457,724 nuclei: 266,448 TN, 60,013 MRD, and 131,263 PD.
Nine cell-type annotations were available, including tumour, fibroblast,
endothelial, myeloid, lymphoid, plasma, epithelial, and mast-cell classes.
There were 166,112 tumour-flagged nuclei.

### Metadata-based state differences

In the paired Xenium analysis, the mean tumour alveolar score decreased by 1.10
from TN to PD, while the mean neuroendocrine score increased by 0.40. These
values describe the five paired sections and do not estimate a population-level
treatment effect.

The C797S label was concentrated in one progressive-disease patient. This is
consistent with a resistance-associated observation but cannot establish that
C797S caused the observed state transition.

The snRNA state groups were unmatched. Tumour fraction and sequencing QC
metrics differed descriptively among TN, MRD, and PD. Because QC metrics can
reflect tissue composition and library quality, they are not interpreted as
resistance phenotypes.

At the sample level, endothelial-cell fraction averaged 2.6% in TN and 6.6% in
PD. The exploratory Benjamini-Hochberg FDR was 0.024. Epithelial fraction was
highest in MRD but did not remain significant after multiple-testing correction.
These composition results may reflect tissue sampling or state-associated
cellularity and are not treatment-effect estimates.

### Spatial replication and contextual benchmarks

GSE189487 provided six independent spatial samples across AIS, MIA, and IAC.
Stromal and epithelial/EGFR-related features were detectable across datasets,
while hypoxia and vascular features were more platform-sensitive. GSE301973 was
limited to a single paired case and was therefore used for pipeline QC rather
than inference.

The TCGA-LUAD exploratory survival baseline included 301 complete cases and 89
DFS events. The penalized Cox model estimated an EGFR mutation HR of 1.06 (95%
CI 0.61-1.84; p=0.84) after age, stage grouping, TP53, and RB1 adjustment.
This was a molecular benchmark, not an osimertinib efficacy analysis.

## Discussion

The main contribution of this pilot is an evidence-linked workflow that keeps
cohort structure, data provenance, and biological interpretation separate. The
primary resistance datasets provide a stronger basis for spatial treatment-state
analysis than generic lung cancer cohorts because they contain matched TN/PD
sections or explicit TN/MRD/PD metadata.

The paired Xenium observations support further investigation of lineage-state
changes during progression. They do not prove a spatial pharmacological
sanctuary. The concentration of C797S in a single PD patient similarly supports
case-level investigation but not a general resistance mechanism.

The frozen signature set is useful as a reproducibility contract. Its panel
coverage prevents silent substitution of unavailable genes, while the proxy
report prevents metadata fields from being mislabeled as expression scores.

This is a computational and bioinformatic contribution. Public clinical data
can sharpen the route from mechanism to a testable clinical question, but cannot
replace real clinical assessment or prospective intervention. The practical
output is a clearer, reproducible path for future clinical validation.

## Limitations

- The linked primary publication is currently a bioRxiv preprint.
- The Xenium cohort contains only five patient pairs.
- The snRNA states are unmatched and observational.
- Gene-level count matrices are not included because the source files are very
  large; several frozen signatures are therefore not numerically scored.
- No complete osimertinib-specific recurrence endpoint is currently linked to
  the spatial measurements.
- Batch, tissue quality, treatment details, and clinical confounding require
  additional analysis.
- The current results cannot support treatment recommendations or individual
  patient risk predictions.

## Figures

![Paired Xenium treatment-state metadata.](xenium_paired_resistance_metadata.png)

![snRNA sample-level treatment-state metadata and QC.](snrna_state_metadata_qc.png)

## Data and Code Availability

Code, derived reports, tests, citation metadata, and manuscript materials are
archived at:

- GitHub: https://github.com/Lukecele/spatial-continuum-translational
- Zenodo concept DOI: https://doi.org/10.5281/zenodo.23956445

The original spatial-continuum-oncology repository is preserved separately and
is not modified by this study.

## References used in the current evidence ledger

1. PMID 40654861. *Complementary modes of resistance to EGFR TKI in lung
  adenocarcinoma through MAPK activation and cellular plasticity.* bioRxiv,
  2025. Primary GSE342824/GSE292469 cohort preprint.
2. PMID 36434043. *Delineating the dynamic evolution from preneoplasia to
  invasive lung adenocarcinoma by integrating single-cell RNA sequencing and
  spatial transcriptomics.* Experimental & Molecular Medicine, 2022.
3. PMID 41152910. *IFITM3-MET interaction drives osimertinib resistance through
  AKT pathway activation in EGFR-mutant non-small cell lung cancer.* Molecular
  Cancer, 2025.
4. PMID 28445112. *Tracking the Evolution of Non-Small-Cell Lung Cancer.* The
  New England Journal of Medicine, 2017.
5. PMID 28445469. *Phylogenetic ctDNA analysis depicts early-stage lung cancer
  evolution.* Nature, 2017.
