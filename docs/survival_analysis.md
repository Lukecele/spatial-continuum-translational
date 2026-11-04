# Exploratory TCGA-LUAD Survival Analysis

The first baseline uses the TCGA-LUAD PanCancer Atlas cohort from cBioPortal.
It is an exploratory molecular benchmark, not an osimertinib efficacy analysis.

## Endpoint and model

- Endpoint: `DFS_MONTHS` and `DFS_STATUS`.
- Complete duration/status rows: 301 patients.
- Observed events: 89.
- Model: multivariable Cox proportional-hazards model with `EGFR`, `TP53`, and
  `RB1` mutation flags plus age when available.
- Missing rows are excluded from the complete-case Cox fit.

## Current result

The generated result is stored in
`data/derived/tcga_luad_survival_summary.json`.

The exploratory EGFR coefficient is HR 1.12 (95% CI 0.59-2.13, p=0.72). This
is not evidence of a clinical effect. The cohort does not provide sufficient
osimertinib-specific treatment information, the mutation flags are based on the
public molecular profile, and the model does not yet include stage, smoking,
cohort/batch, or other clinical confounders.

## Reproduction

```bash
python -m pip install -e '.[analysis]'
python scripts/download_cbioportal.py
python scripts/survival_analysis.py
```

The analysis must be extended with pre-specified covariates, proportional-hazard
checks, sensitivity analyses, and an external cohort before it can support a
manuscript claim.
