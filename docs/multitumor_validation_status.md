# Multi-Tumor Validation Status

This table prevents the expansion from being confused with completed empirical
validation.

| Tumor | Status | What is actually supported |
| --- | --- | --- |
| EGFR-mutant NSCLC | Analyzed | Original reaction-diffusion/CRI work plus new public TN/MRD/PD metadata analyses |
| GIST | Exploratory internal validation | cBioPortal cohort with 438 complete patients and 205 RFS events; 5-fold C-index 0.881 +/- 0.036; no external calibration yet |
| BRAF-mutant melanoma | Exploratory external validation | Public BRAF-inhibitor resistance cohort with 45 treatment-annotated patients; response/resistance association analysis, not a calibrated clinical model |
| Luminal breast cancer | Proposed translation | Collagen/CAF and CDK4/6 state variables documented; no dataset-specific model or result yet |
| Clear-cell renal carcinoma | Proposed translation | Hypoxia/sinusoidal transport variables documented; no dataset-specific model or result yet |
| Pancreatic ductal adenocarcinoma | Proposed translation | Desmoplasia/KRAS transport variables documented; no dataset-specific model or result yet |

## Interpretation rule

EGFR-mutant NSCLC, GIST, and melanoma now have analyzed computational results,
each with explicit exploratory limits. Breast, renal, and pancreatic tumors
remain a pre-specified computational research program: their data sources,
parameters, and falsification tests must be registered before any tumor-specific
result is reported.
