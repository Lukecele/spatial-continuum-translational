# External Validation Status

## Current status

No compatible external cohort has yet validated the same full model with the
same tumor, treatment context, endpoint, and variable definitions.

## What exists

- GIST: strong internal validation in `gist_msk_2023`; other public GIST cohorts
  expose different endpoints or incomplete covariates.
- Melanoma: public BRAF-inhibitor treatment-response cohort; no independent
  matched cohort with the same response definition was identified.
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
