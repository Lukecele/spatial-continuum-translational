# Cohort Screening Protocol

A public dataset is not an external validation cohort by default. Before adding a
cohort to a clinical model, complete this screen and preserve the evidence used
for every decision.

## Required compatibility fields

| Field | Pass condition | Fail condition |
|---|---|---|
| Tumor | Same tumor definition and relevant molecular subtype | Different tumor, mixed subtype, or subtype unavailable |
| Treatment | Same drug/regimen and treatment line or a prespecified compatible class | Different drug, regimen, line, or treatment unknown |
| Endpoint | Same endpoint definition, time origin, and event rule | OS/DFS/RFS/PFS/response substituted without harmonization |
| Unit | Patient is the replication unit | Cells, nuclei, spots, samples, or regions treated as independent patients |
| Outcome | Outcome is available before model fitting and has explicit labels/times | Proxy phenotype, narrative outcome, or post hoc label only |
| Covariates | Required model inputs are measurable with documented definitions | Key predictors absent, incompatible, or irrecoverable |
| Sample size | Prespecified minimum and event count are met | Small exploratory series with unstable estimates |
| Data access | Raw/processed data and provenance can be re-run | Aggregate publication values only for a patient-level score |
| Independence | Cohort is independent of model development and tuning | Same patients, reused trial data, or undisclosed overlap |

## Decision classes

- `FULL_VALIDATION`: all required fields pass; patient-level analysis is
  executable without changing the estimand.
- `CURRENT_MODEL_COHORT`: prespecified development or primary analysis cohort;
  it may be clinically well annotated but is not external validation.
- `PHENOTYPE_REPLICATION`: tumor and biological phenotype are compatible, but
  treatment, endpoint, covariates, or patient-level data are incomplete.
- `BIOLOGICAL_CONTEXT`: useful mechanistic or spatial evidence, but not a
  clinical validation cohort.
- `REJECTED`: incompatible treatment, endpoint, tumor, replication unit, or
  provenance.

## Mandatory record

Every screened candidate must record:

1. accession, DOI/PMID, or trial identifier;
2. tumor and molecular subtype;
3. exact treatment, line, and comparator;
4. endpoint definition and follow-up/time origin;
5. patient count, event count, and replication unit;
6. available covariates and missingness;
7. overlap or independence assessment;
8. decision class and explicit exclusion reason where applicable.

Run the automated gate before committing a new candidate:

```bash
python3 scripts/validate_cohort_screening.py
```

To search for new candidates without adding them automatically, run:

```bash
python3 scripts/search_screened_cohorts.py \\
  --output data/derived/cohort_search_screened.json
```

The search runs the tumor-specific Europe PMC queries in parallel and applies
the NCBI GEO query channel with rate-limit protection. `PASS` is only a
text-level candidate screen; every hit still requires primary-source review,
data-access verification, and a row in this screening register.

No external cohort may be called validated or added to a pooled clinical model
until the decision class is `FULL_VALIDATION`. Treatment arms and incompatible
endpoints remain separate estimands even when they come from the same
publication.
