# Tumor-Specific Score Freeze Protocol

A score is eligible for external validation only after its definition is frozen
using development data that are independent of the external cohort.

## Required frozen fields

Each tumor-specific score must define:

- development cohort and accession;
- patient-level replication unit;
- treatment and line;
- primary endpoint and time origin;
- feature/gene list and biological provenance;
- preprocessing and normalization;
- weights or deterministic scoring rule;
- threshold, if a binary score is used;
- missing-feature and missing-patient rules;
- arm stratification rules;
- external cohort identifier, kept hidden from feature selection.

## Leakage rules

The external cohort must not be used to:

- select genes or clinical covariates;
- tune weights or thresholds;
- choose the endpoint or time origin;
- decide sample exclusions after inspecting outcomes;
- merge treatment arms that were prespecified as separate estimands.

## Current readiness

| Tumor | Development score | External cohort | Status |
|---|---|---|---|
| GIST | Exploratory Cox model in `gist_msk_2023` | GSE225978 | Blocked: required covariates absent externally |
| Melanoma | No frozen melanoma score | GSE196434; GSE99898 | Blocked: score definition and development feature set absent |
| Breast | No frozen PI3K/letrozole score | NEO-ORB; `brca_mskcc_2019` | Blocked: score definition and patient-level NEO-ORB data absent |
| Renal | No repository renal score; published 15G is a separate model | IMmotion151 | Blocked: controlled data access and feature mapping |
| Pancreas | No frozen PRINCE-like score | Public PRINCE; Wainberg 2020 | Blocked: score definition absent; public clinical data support descriptive analysis |

A blocked score must remain labeled exploratory or unavailable. It must not be
reported as externally validated.
