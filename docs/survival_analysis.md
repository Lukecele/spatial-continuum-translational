# Exploratory TCGA-LUAD Survival Analysis

The first baseline uses the TCGA-LUAD PanCancer Atlas cohort from cBioPortal.
It is an exploratory molecular benchmark, not an osimertinib efficacy analysis.

## Endpoint and model

- Endpoint: `DFS_MONTHS` and `DFS_STATUS`.
- Complete duration/status rows: 301 patients.
- Observed events: 89.
- Model: multivariable Cox proportional-hazards model with `EGFR`, `TP53`, and
  `RB1` mutation flags, age, and a binary early-versus-advanced pathological
  stage grouping. The Cox fit uses a prespecified 0.1 penalizer because the
  detailed stage categories showed separation.
- Missing rows are excluded from the complete-case Cox fit.

## Current result

The generated result is stored in
`data/derived/tcga_luad_survival_summary.json`.

The stabilized exploratory EGFR coefficient is HR 1.06 (95% CI 0.61-1.84,
p=0.84). This is not evidence of a clinical effect. The cohort does not provide sufficient
osimertinib-specific treatment information, the mutation flags are based on the
public molecular profile, and the model does not yet include smoking, cohort/
batch, or other clinical confounders. The proportional-hazards diagnostics are
screening checks, not proof that the assumption holds.

## Reproduction

```bash
python -m pip install -e '.[analysis]'
python scripts/download_cbioportal.py
python scripts/survival_analysis.py
```

The analysis must be extended with pre-specified covariates, proportional-hazard
checks, sensitivity analyses, and an external cohort before it can support a
manuscript claim.
