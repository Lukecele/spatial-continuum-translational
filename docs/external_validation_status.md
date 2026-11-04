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
  in GSE196434 is pending; mixed treatment contexts must remain stratified.
- Breast: response-annotated MSK cohort plus NEO-ORB, a second PI3K-plus-
  letrozole clinical cohort (257 randomized patients; neoadjuvant ORR/pCR).
  The currently verified NEO-ORB data are aggregate and the full score remains
  unvalidated.
- Renal: IMmotion150 remains the only compatible treatment-response/PFS cohort.
  A 97-patient independent ccRCC geospatial cohort provides biological support,
  but uses OS/CSS and different treatment metadata.
- Pancreas: PRINCE remains the only compatible treatment-response/PFS cohort;
  no second matching trial cohort was identified in the public catalog.
- Renal: IMmotion150 treatment-response/PFS cohort; other renal cohorts are
  molecular or prognostic contexts with different endpoints.
- Pancreas: PRINCE treatment-response/PFS cohort; other pancreatic cohorts are
  genomic or survival contexts with different treatment designs.

## Correct interpretation

These cohorts provide independent biological or treatment-context evidence, not
external validation of one pooled clinical score. Each tumor remains a separate
estimand until a compatible second cohort is found.
