# Exploratory Score Audit

The audit in `data/derived/exploratory_score_audit.json` evaluates frozen tumor-specific scores on public expression data.

## Design

- Fixed threshold: score `>= 0`.
- No threshold optimization or refitting on the public cohorts.
- Sensitivity and specificity use the dataset labels defined in the report.
- 95% confidence intervals use the Wilson binomial interval.
- GSE99898 and GSE196434 use paired two-sided Student t-tests by patient.
- PRINCE uses a two-sided Welch two-sample Student t-test between objective response groups.

## Results

- GSE99898 PROG versus PRE: sensitivity 53.8% (Wilson 95% CI 29.1-76.8%), specificity 82.4% (59.0-93.8%), paired t-test p=0.420, n=13 pairs.
- GSE196434 POST versus PRE: sensitivity 59.1% (Wilson 95% CI 38.7-76.7%), specificity 47.8% (36.5-59.4%), paired t-test p=0.735, n=9 pairs.
- GSE196434 short versus long response: sensitivity 48.8% (Wilson 95% CI 34.6-63.2%), specificity 41.7% (28.8-55.7%), n=91 labeled samples.
- PRINCE objective response versus non-response: sensitivity 52.2% (Wilson 95% CI 33.0-70.8%), specificity 43.3% (27.4-60.8%), Welch t-test p=0.423, n=53 labeled samples.

## Interpretation

These are exploratory, descriptive metrics. Sensitivity and specificity refer to the stated cohort labels, not clinical diagnostic performance. The results do not establish clinical utility, causality, calibrated risk, or generalization to an independent clinical population.
