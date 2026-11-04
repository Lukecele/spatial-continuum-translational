# External Compatible Cohort Search

## GIST RFS

The current `gist_msk_2023` cohort is the strongest internal dataset: 438
complete patients and 205 RFS events. Public cBioPortal alternatives found:

- `gist_msk_2022`: 499 samples, but the exposed clinical endpoint is OS rather
  than the same RFS definition.
- `gist_msk_2025`: 42 samples, mutation-focused and without a compatible RFS
  endpoint in the available metadata.

These are useful sensitivity/context cohorts, not external RFS validation for
the current GIST model.

## BRAF-mutant melanoma

`skcm_broad_brafresist_2012` provides the current treatment-response cohort: 45
patients with 14 early-resistance cases and vemurafenib/dabrafenib context.

`GSE196434` is a compatible second clinical expression cohort: 91 melanoma
metastasis samples from 50 patients, with PRE/POST treatment specimens and
long-response versus short-response groups. The metadata include BRAFi and
BRAFi+MEKi treatment contexts. It is registered as an external validation
candidate; the full score has not yet been applied, and the two treatment
contexts must remain stratified.

TCGA and immunotherapy melanoma cohorts are not valid substitutes for a
BRAF-inhibitor response validation.

## Breast treatment response

`brca_mskcc_2019` provides 54 response-annotated patients, mainly in a
PI3K-inhibitor/letrozole treatment context. CDK4/6 resistance cohorts and
metastatic breast genomic cohorts are available, but they do not share the same
therapy and response fields. They must remain separate analyses.

`NEO-ORB` (NCT01610284; PMID 30723140) is a compatible second clinical cohort:
257 HR-positive/HER2-negative patients randomized to alpelisib plus letrozole
(131) or placebo plus letrozole (126), with objective response and pathological
complete response endpoints. The currently verified evidence is aggregate trial
data; patient-level score validation and harmonization with the metastatic
cohort remain pending.

## Renal and pancreatic trials

- IMmotion150 is the current renal treatment-response cohort with PFS and
  response metadata.
- PRINCE is the current pancreatic treatment-response cohort with PFS, OS, and
  response metadata.

Other renal and pancreatic genomic cohorts are useful for biological context,
but cannot be pooled with these trial endpoints or treatment arms.

## Conclusion

The search did not find compatible external cohorts for immediate pooled
validation. The correct next acquisition is a cohort with the same tumor,
treatment, endpoint, and minimum covariates, not simply a larger unrelated
cohort.
