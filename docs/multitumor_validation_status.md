# Multi-Tumor Validation Status

This table prevents the expansion from being confused with completed empirical
validation.

| Tumor | Status | What is actually supported |
| --- | --- | --- |
| EGFR-mutant NSCLC | Analyzed | Original reaction-diffusion/CRI work plus new public TN/MRD/PD metadata analyses |
| GIST | Exploratory internal validation | cBioPortal cohort with 438 complete patients and 205 RFS events; 5-fold C-index 0.881 +/- 0.036; no external calibration yet |
| BRAF-mutant melanoma | Exploratory external validation | Public BRAF-inhibitor resistance cohort with 45 treatment-annotated patients; NRAS p=0.044 before correction and BH FDR=0.131, not confirmed |
| Luminal breast cancer | Exploratory treatment-response validation | Public MSK cohort with 54 response-annotated patients and 14 progressive cases; incomplete therapy/mutation fields limit interpretation |
| Clear-cell renal carcinoma | Exploratory treatment-response validation | IMmotion150 cohort with 263 patients, 262 PFS records, and 79 progressions |
| Pancreatic ductal adenocarcinoma | Exploratory treatment-response validation | PRINCE cohort with 74 patients, 73 PFS records, and 12 progressions |

## Interpretation rule

EGFR-mutant NSCLC, GIST, melanoma, renal cell carcinoma, and pancreatic cancer now have analyzed computational results,
each with explicit exploratory limits. Breast, renal, and pancreatic tumors
remain a pre-specified computational research program: their data sources,
parameters, and falsification tests must be registered before any tumor-specific
result is reported.
