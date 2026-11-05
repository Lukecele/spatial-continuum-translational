# A reproducible framework for exploratory multi-tumor transcriptional signatures across public cohorts

**Luca Celebrano**$^{1,*}$  
$^{1}$ Department of Clinical Medicine and Surgery, School of Medicine and Surgery, University of Naples Federico II, Via Sergio Pansini 5, 80131 Naples, Italy  
$^{*}$ Corresponding author: l.celebrano@studenti.unina.it  
ORCID: 0009-0007-0931-3555  
GitHub: https://github.com/Lukecele

## Article type

Research article / methodological exploratory study

## Abstract

### Background
Transcriptional signatures are frequently transferred between studies despite differences in tumor type, treatment state, platform, and clinical endpoint. A transparent workflow is needed to distinguish a frozen exploratory score from a clinically validated biomarker.

### Methods
We assembled a reproducible framework for tumor-specific transcriptional scores. Three equal-weight signatures were frozen before public-cohort scoring: a seven-gene melanoma MAPK-bypass/stress-escape score (AXL, NGFR, WNT5A, EGFR, PDGFRB, JUN, FOS), a seven-gene breast PI3K-pathway score, and an eight-gene pancreatic stromal/immune-exclusion score. Scores were calculated as the mean of gene-wise standardized expression values, with a pre-specified minimum of 80% measured genes. We applied the melanoma score to GSE99898 and GSE196434 and the pancreatic score to the public PRINCE RNA-seq cohort. A fixed score threshold of 0 was used for descriptive sensitivity and specificity. Two-sided paired Student t-tests were used for patient-matched treatment-state comparisons, and Welch two-sample Student t-tests were used for independent response groups.

### Results
In GSE99898, the fixed threshold gave 53.8% sensitivity and 82.4% specificity for PROG versus PRE, with 13 patient pairs and a paired t-test p-value of 0.420. In GSE196434, the threshold gave 59.1% sensitivity and 47.8% specificity for POST versus PRE, with 9 patient pairs and a paired t-test p-value of 0.735. For short versus long response in the same cohort, sensitivity was 48.8% and specificity was 41.7%. In PRINCE, objective response versus non-response gave 52.2% sensitivity and 43.3% specificity among 53 labeled samples; the Welch t-test p-value was 0.423. Wilson confidence intervals were wide for all estimates.

### Conclusions
The framework is reproducible and exposes the uncertainty of transferring frozen exploratory scores across public cohorts. The present results do not support clinical validation or treatment-response prediction. They provide a transparent baseline for future pre-registered development and independent validation.

**Keywords:** transcriptional signature; biomarker reproducibility; public cohorts; melanoma; pancreatic cancer; exploratory analysis; reproducible research

## Introduction

Gene-expression signatures are attractive because they can connect biological hypotheses to measurable tumor states. Their apparent portability is often difficult to assess, however, because expression platforms, normalization procedures, patient populations, treatment states, and endpoints differ between studies. A score that is useful for describing a phenotype is not automatically a diagnostic test, a prognostic model, or a treatment-selection tool.

We developed a small, auditable framework to preserve this distinction. The framework freezes gene lists, directions, equal weights, missing-gene rules, and score threshold before applying the signatures to public expression data. It reports both positive and negative findings, including confidence intervals and non-significant tests. The objective of this study is not to claim clinical utility. It is to quantify how a transparent exploratory score behaves when transported across public cohorts and study designs.

## Methods

### Study design and analysis principles

This was a retrospective, computational, exploratory study using public expression matrices and associated metadata. The analysis followed a metadata-first compatibility gate. Cohorts were retained only when sample identifiers, expression measurements, and relevant treatment-state or response metadata could be joined reproducibly.

The analysis protocol prohibited outcome-based refitting of genes, weights, directions, or thresholds on the evaluated cohort. PRE, EDT, PROG, POST, response, PFS, and OS were not pooled into one endpoint. All findings are descriptive and should not be interpreted as causal treatment effects.

### Frozen signatures

The frozen signature specification is stored in `data/exploratory_tumor_scores_v1.json`.

The melanoma score represents a hypothesis about MAPK-bypass/stress-escape biology and contains AXL, NGFR, WNT5A, EGFR, PDGFRB, JUN, and FOS with positive equal weights. The breast score represents pathway activity using PIK3CA, AKT1, PDPK1, MTOR, RPS6KB1, EIF4EBP1, and inverse PTEN direction. The pancreatic score represents stromal/immune exclusion using COL1A1, COL3A1, COL5A1, FAP, CXCL12, TGFB1, SPP1, and CSF1.

The breast signature remained pending expression validation because a suitable compatible public breast expression matrix was not available in this analysis release. It is therefore not included in the quantitative public-cohort results below.

### Score calculation

For each dataset, expression was standardized gene-wise and the score was calculated as the arithmetic mean of available standardized genes with their frozen directions. A score was retained only when at least 80% of requested genes were measured. When development-dataset normalization parameters were unavailable, the resulting values were treated as within-cohort descriptive z-scores and were not called external validation.

EGFR is one component of the melanoma score and was not interpreted as an independently validated biomarker in this study. Gene-specific analyses would require a separately specified analysis plan.

### Public cohorts

GSE99898 contains serial melanoma biopsies from 17 patients and includes PRE, EDT, and PROG states. GSE196434 contains 91 melanoma expression samples with PRE/POST and response metadata where available. The PRINCE public RNA-seq data contain 65 baseline pancreatic tumor samples; two samples lack an arm join and were retained as unknown for arm summaries. Response labels were available for 53 samples after metadata joining.

### Statistical analysis

A fixed threshold of score >= 0 was used for all classification summaries. Sensitivity and specificity were calculated against the stated cohort label, not against a clinical diagnostic gold standard. Two-sided 95% Wilson intervals were calculated for binomial proportions.

For patient-matched state comparisons, scores were paired by patient and compared using a two-sided paired Student t-test. GSE99898 was analyzed as PRE versus PROG and GSE196434 as PRE versus POST. For PRINCE, response and non-response groups were compared with a two-sided Welch two-sample Student t-test. No threshold optimization, multiple-testing claim, causal inference, or clinical validation claim was made.

### Reproducibility

The analysis is implemented in Python. The public-score application is implemented in `scripts/apply_exploratory_scores_public.py`, the fixed-threshold audit in `scripts/audit_exploratory_scores.py`, and plotting in `scripts/plot_exploratory_score_application.py`. Continuous integration runs the repository test suite through GitHub Actions. Derived JSON reports and PNG figures are retained in the repository; raw GEO and trial files are not redistributed.

## Results

### Frozen score application

The application pipeline generated sample-level score rows, gene-availability fields, metadata joins, leave-one-gene-out diagnostics, state summaries, and patient-matched deltas. The GSE196434 report contains 9 PRE-to-POST patient pairs. GSE99898 contains 13 PRE-to-PROG pairs in the quantitative audit. PRINCE was summarized by treatment arm and response label without causal arm comparisons.

### Fixed-threshold classification audit

| Dataset and target | n | Sensitivity | Specificity | Statistical comparison |
|---|---:|---:|---:|---|
| GSE99898 PROG versus PRE | 30 | 53.8% (29.1-76.8%) | 82.4% (59.0-93.8%) | paired t-test, n=13, p=0.420 |
| GSE196434 POST versus PRE | 91 | 59.1% (38.7-76.7%) | 47.8% (36.5-59.4%) | paired t-test, n=9, p=0.735 |
| GSE196434 short versus long response | 91 | 48.8% (34.6-63.2%) | 41.7% (28.8-55.7%) | descriptive classification |
| PRINCE objective response versus non-response | 53 | 52.2% (33.0-70.8%) | 43.3% (27.4-60.8%) | Welch t-test, p=0.423 |

The confidence intervals are broad, and the t-tests do not provide evidence against the null hypothesis at conventional significance levels. The GSE99898 specificity estimate is higher than the other observed estimates, but this isolated result is insufficient to establish transportability.

### Figure set

The main figure set shows cohort-level score distributions, available patient-matched deltas, and the PRINCE arm-level descriptive summary. Figure files and captions are listed in `docs/figure_legends.md`.

## Discussion

This study demonstrates a practical way to transport frozen exploratory signatures while preserving an auditable boundary between biological scoring and clinical validation. The main contribution is procedural: the code records the score definition, input compatibility, metadata joins, missing-gene behavior, fixed threshold, confidence intervals, and statistical tests in machine-readable outputs.

The quantitative results are deliberately modest. The observed performance is inconsistent across cohorts, and none of the t-tests is statistically significant. The results should therefore be interpreted as evidence that the present signatures require further development, not as evidence of clinical prediction. In particular, EGFR is only one positively weighted component of the melanoma score; the current audit cannot attribute the aggregate behavior to EGFR alone.

The framework also makes negative evidence visible. A score can have a plausible biological direction and still fail to discriminate public treatment states or response groups when sample size is small, labels are imperfect, platforms differ, or the phenotype is not captured by the selected genes. This is a useful outcome for planning a prospective validation study.

### Limitations

First, the analysis is underpowered, especially for patient-matched comparisons. Second, the public cohorts differ in platform, treatment design, sampling time, and endpoint definition. Third, within-cohort standardization limits direct comparison of score magnitude between datasets. Fourth, the threshold of 0 is fixed but exploratory rather than clinically calibrated. Fifth, two PRINCE samples have unknown treatment arm, and only 53 samples have usable response labels. Sixth, the breast signature was not applied to a compatible public expression matrix in this release. Finally, no independent prospective validation or experimental perturbation was performed.

## Conclusions

A frozen, metadata-aware workflow can expose both the portability and the limitations of exploratory transcriptional signatures. In the present public-cohort audit, sensitivity, specificity, and t-tests do not support clinical validation of the melanoma or pancreatic scores. The repository provides a reproducible baseline for future signature refinement, pre-registration, and independent validation.

## Data and code availability

Source code, frozen signature specifications, derived reports, figures, and documentation are available in the associated GitHub repository. Raw GEO and trial files are accessed from their original public sources and are not redistributed. GSE99898 and GSE196434 were accessed through the NCBI Gene Expression Omnibus (GEO; RRID:SCR_005012) using their public accession identifiers. The PRINCE data are cited by their public study/data record; no separate RRID was assigned to that cohort in the source materials. A Zenodo release should archive the exact Git commit, derived reports, figures, and environment metadata.

## Resource identification

The computational environment used Python (RRID:SCR_008394), SciPy (RRID:SCR_008058), and Matplotlib (RRID:SCR_008624). The frozen score definitions and all analysis scripts are supplied with the repository. Dataset accessions are used instead of inventing RRIDs for public cohorts that do not have a separate resource identifier.

## Declarations

**Ethics approval and consent to participate:** Not applicable; only previously published, de-identified public data were analyzed.

**Consent for publication:** Not applicable.

**Competing interests:** The authors declare no competing interests.

**Funding:** This work received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

**Authors' contributions:** To be completed by the authors.

**Acknowledgements:** To be completed by the authors.

## References to finalize before submission

1. The original report and data record for GSE99898 (GEO accession GSE99898; NCBI GEO, RRID:SCR_005012).
2. The original report and data record for GSE196434 (GEO accession GSE196434; NCBI GEO, RRID:SCR_005012).
3. The PRINCE public dataset publication and data record.
4. Python (RRID:SCR_008394), SciPy (RRID:SCR_008058), and Matplotlib (RRID:SCR_008624), with versions recorded in the final release.
5. The repository release DOI and version used for submission.
