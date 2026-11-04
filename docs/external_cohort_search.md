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
- IMmotion151 is now a compatible second renal clinical cohort: 823 patients
  with RNA-seq in the external 15G analysis, randomized to atezolizumab plus
  bevacizumab or sunitinib, with PFS and response endpoints. It is an
  independent trial from IMmotion150. The published analysis uses the 15G
  score, so validation of the repository score remains pending feature mapping
  and patient-level data access. The source identified by the publication is
  EGA `EGAS00001004353`; access requires a data-use agreement with Genentech.
- PRINCE is the current pancreatic treatment-response cohort with PFS, OS, and
  response metadata.
- Wainberg et al. (PMID 32554514) is a compatible second pancreatic cohort: 50
  chemotherapy-naive patients with locally advanced/metastatic disease treated
  with the exact nivolumab plus gemcitabine/nab-paclitaxel backbone, reporting
  PFS, OS, and objective response. It is an independent phase I cohort with
  aggregate published data; score-level validation remains pending.

The PRINCE investigators also release de-identified patient-level clinical data
and processed RNA-seq in `ParkerICI/prince-trial-data`. The clinical file has
108 unique patients across A1, B2, and C2, with 108 PFS records, 96 PFS events,
108 OS records, 80 OS events, and response labels. This resolves the data-access
blocker for arm-specific descriptive analysis, but not the absence of a frozen
pancreas-specific score.

A renal geospatial study (PMID 37185232) includes 97 independent ccRCC
patients and reports OS/CSS associations, with a related expression score
tested in IMmotion150, IMmotion151, and JAVELIN Renal 101. It is useful
biological support, but it is not a second IMmotion150 treatment-response
cohort because its primary endpoints and treatment metadata are different.

The public cBioPortal catalog was also checked for renal and pancreatic trial
records. It exposes IMmotion150 and PRINCE as the relevant treatment datasets,
but no independent second cohort with the same treatment and endpoint was
identified for either tumor.

Other renal and pancreatic genomic cohorts are useful for biological context,
but cannot be pooled with these trial endpoints or treatment arms.

## Conclusion

The search did not find compatible external cohorts for immediate pooled
validation. The correct next acquisition is a cohort with the same tumor,
treatment, endpoint, and minimum covariates, not simply a larger unrelated
cohort.
