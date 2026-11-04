# Clinical Validation Roadmap with Heterogeneous Cohorts

## Principle

Cohorts are not interchangeable. The study will never pool hazard ratios or
response rates merely because the tumor label is the same.

## Cohort strata

| Cohort | Disease | Treatment context | Endpoint | Valid use |
| --- | --- | --- | --- | --- |
| GSE342824/GSE292469 | EGFR-mutant LUAD | EGFR-TKI resistance states | TN/MRD/PD metadata | spatial/state hypothesis |
| TCGA-LUAD | LUAD | heterogeneous historical treatment | DFS/PFS/OS | molecular prognostic benchmark |
| TRACERx | NSCLC | heterogeneous adjuvant context | RFS/ctDNA context | evolutionary benchmark |
| gist_msk_2023 | GIST | heterogeneous clinical treatment | RFS/OS | GIST feature validation |
| skcm_broad_brafresist_2012 | melanoma | vemurafenib/dabrafenib | response/early resistance | BRAF-resistance benchmark |

## Required validation sequence

1. Define the estimand separately for every cohort.
2. Harmonize only variables with identical meanings and units.
3. Fit each cohort-specific model independently.
4. Report cohort-specific effect sizes, uncertainty, missingness, and event
   counts.
5. Test transportability using covariate-overlap and sensitivity checks.
6. Use leave-one-cohort-out validation only when endpoints and treatment context
   are compatible.
7. Do not meta-analyze across different tumors or endpoints without a prespecified
   hierarchical model and a defensible biological rationale.

## Clinical rule boundary

The current data support exploratory association and transportability analysis.
They do not support a pooled clinical rule. A clinical rule requires a target
population, a single endpoint, treatment-consistent cohorts, calibration,
external validation, and prospective evaluation.

## Maximum-compatible cohort limits

The maximum usable `N` is endpoint-specific, not the sum of every dataset in
the repository. The limits are recorded in
`data/derived/compatible_cohort_limits.json`:

- GIST RFS: 438 complete patients and 205 events;
- BRAF-inhibitor melanoma response: 45 annotated patients and 14 early-
   resistance cases;
- breast treatment response: 54 annotated patients and 14 progressive cases;
- renal IMmotion150: 263 patients, 262 PFS records, 79 progressions;
- pancreatic PRINCE: 74 patients, 73 PFS records, 12 progressions.

These are not additive totals. Each set has a different tumor, treatment,
endpoint, and estimand.

## Immediate computational work

- Add cohort-specific calibration summaries for GIST and melanoma.
- Quantify missingness and covariate overlap before any pooled analysis.
- Compare model performance by cohort without pooling raw patients.
- Keep the EGFR spatial cohort as a biological state analysis, not a recurrence
  endpoint cohort.
