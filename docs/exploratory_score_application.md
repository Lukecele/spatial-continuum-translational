# Exploratory Score Application

The frozen exploratory signatures were applied to public expression data without
refitting genes, weights, thresholds, or outcome models.

## Inputs

- `GSE99898`: 38 melanoma biopsies from 17 patients, grouped as PRE, EDT, and
  PROG.
- `GSE196434`: 91 melanoma metastasis expression samples, grouped as PRE and
  POST; patient/state metadata are preserved where available.
- Public PRINCE RNA-seq: 65 baseline tumor expression samples with known A1/B2/C2
  arms; two samples lack an arm join and remain `unknown`.

## Outputs

- `data/derived/exploratory_public_score_application.json`
- `figures/exploratory_scores/gse99898_exploratory_score.png`
- `figures/exploratory_scores/gse99898_paired_deltas.png`
- `figures/exploratory_scores/gse196434_exploratory_score.png`
- `figures/exploratory_scores/prince_exploratory_score.png`

The report includes dataset-level gene-wise normalization, sample-level missing
gene counts, leave-one-gene-out sensitivity, patient-state paired deltas where
available, and arm-level summaries for PRINCE.

## Interpretation limits

These are descriptive exploratory scores. The observed means must not be read as
response effects, treatment effects, or clinical predictions. GSE99898 and
GSE196434 use different platforms and treatment-state designs; PRINCE is
summarized by treatment arm without causal comparison. No external cohort was
used to refit a gene list, weight, threshold, or outcome model.

## Reproduction

```bash
python3 scripts/apply_exploratory_scores_public.py \\
  --gse99898-matrix /path/GSE99898_series_matrix.txt.gz \\
  --gse99898-platform /path/GPL10558.txt \\
  --gse99898-soft /path/GSE99898_family.soft.gz \\
  --gse196434-raw /path/GSE196434_MR_GEO_rawdata.txt.gz \\
  --gse196434-soft /path/GSE196434_family.soft.gz \\
  --prince-root /path/prince-trial-data \\
  --output data/derived/exploratory_public_score_application.json

python3 scripts/plot_exploratory_score_application.py \\
  data/derived/exploratory_public_score_application.json \\
  --output-dir figures/exploratory_scores
```
