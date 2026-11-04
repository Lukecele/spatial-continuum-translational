# External Validation Status

## Current status

No compatible external cohort has yet validated the same full model with the
same tumor, treatment context, endpoint, and variable definitions.

## What exists

- GIST: strong internal validation in `gist_msk_2023`; other public GIST cohorts
  expose different endpoints or incomplete covariates.

GSE225978 adds an external phenotype check: 21 high-risk imatinib-treated GIST
patients are separated into 10 metastatic and 11 non-metastatic cases. The
cohort supports external recurrence-phenotype replication, but lacks the full
clinical covariate set required to validate the complete Cox score.
- Melanoma: public cBioPortal BRAF-inhibitor treatment-response cohort plus
  GSE196434, an independent 50-patient PRE/POST melanoma metastasis cohort with
  long/short response groups and BRAFi/BRAFi+MEKi labels. Full-score validation
  is currently blocked because no melanoma-specific score has been frozen
  independently of GSE196434; mixed treatment contexts must remain stratified.
- Breast: response-annotated MSK cohort plus NEO-ORB, a second PI3K-plus-
  letrozole clinical cohort (257 randomized patients; neoadjuvant ORR/pCR).
  The currently verified NEO-ORB data are aggregate and the full score remains
  unvalidated.
- Renal: IMmotion151 adds a second compatible treatment-response/PFS cohort
  (823 RNA-seq patients; atezolizumab plus bevacizumab versus sunitinib),
  independent of IMmotion150. The external publication uses a different 15G
  score; the repository score remains unvalidated there. The expression/outcome
  source is controlled-access EGA `EGAS00001004353`, not an immediately
  downloadable public file. A separate 97-patient
  ccRCC geospatial cohort provides biological support but uses OS/CSS and
  different treatment metadata.
- Pancreas: Wainberg et al. adds a second compatible cohort (50 patients;
  nivolumab plus gemcitabine/nab-paclitaxel; PFS/OS/response) independent of
  PRINCE. It is a non-randomized phase I study with aggregate data, so the
  repository score remains unvalidated. PRINCE itself now has a public
  de-identified patient-level clinical file with 108 unique patients, 108 PFS
  records, and 108 OS records; a pancreas-specific score still needs to be
  frozen before score validation. The repository now includes a reproducible
  arm-level descriptive summary; observed-time medians are not Kaplan-Meier
  estimates and no causal arm comparison is claimed.
- Renal: IMmotion150 treatment-response/PFS cohort; other renal cohorts are
  molecular or prognostic contexts with different endpoints.
- Pancreas: PRINCE treatment-response/PFS cohort; other pancreatic cohorts are
  genomic or survival contexts with different treatment designs.

## Correct interpretation

These cohorts provide independent biological or treatment-context evidence, not
external validation of one pooled clinical score. Each tumor remains a separate
estimand until a compatible second cohort is found.
