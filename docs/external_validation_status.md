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
- Breast: response-annotated MSK cohort; broader breast genomic cohorts lack the
  same treatment-response endpoint.
- Renal: IMmotion150 treatment-response/PFS cohort; other renal cohorts are
  molecular or prognostic contexts with different endpoints.
- Pancreas: PRINCE treatment-response/PFS cohort; other pancreatic cohorts are
  genomic or survival contexts with different treatment designs.

## Correct interpretation

These cohorts provide independent biological or treatment-context evidence, not
external validation of one pooled clinical score. Each tumor remains a separate
estimand until a compatible second cohort is found.
