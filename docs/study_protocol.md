# Study Protocol: Spatial CRI Translational Pilot

## Research question

In publicly available EGFR-mutated NSCLC data, are spatial features related to
vascular access, hypoxia, stromal restriction, and EGFR/TP53/RB1 state associated
with a measurable drug-response phenotype beyond a clinicopathologic baseline?

This pilot tests the biological plausibility of the extension. It does not claim
to predict an individual patient's recurrence or to recommend treatment.

## Hypotheses

- H1: spatially restricted tumour regions show higher hypoxia/stromal scores and
  lower vascular-access scores than regions with stronger vascular proximity.
- H2: these spatial features are associated with an ex-vivo or molecular drug
  response endpoint when such an endpoint is available.
- H3: the spatial model improves a pre-specified baseline only if the gain is
  reproducible in an independent dataset.

## Data matrix

| Dataset role | Required fields | Acceptance criteria | Status |
| --- | --- | --- | --- |
| Discovery spatial cohort | expression matrix, spatial coordinates, tissue annotation, sample metadata | public accession; raw or processed data and license recorded | To verify |
| Independent spatial cohort | same as discovery, different study or batch | independent accession and compatible feature mapping | To verify |
| Clinical benchmark | treatment, EGFR status, recurrence or survival endpoint, covariates | patient-level endpoint and documented cohort provenance | To verify |
| Drug-response benchmark | drug, dose or response metric, cell/tissue identity | response definition and assay metadata available | To verify |

No dataset is included until its accession, download URL, release date, license,
unit of analysis, and missing-data profile are recorded in the repository.
Every candidate must also pass `docs/cohort_screening_protocol.md` and be
recorded in `data/cohort_screening.tsv` before it is used for model fitting or
described as external validation.
Tumor-specific scores must additionally pass `docs/score_freeze_protocol.md`
and be recorded in `data/derived/score_freeze_readiness.json` before any
external score validation is reported.

## Primary analysis

1. Pre-register cohort and sample exclusions before model fitting.
2. Define vascular, hypoxia, stromal, and EGFR/TP53/RB1 signatures from the
   literature and freeze the gene lists before looking at outcomes.
3. Normalize within each dataset using a documented method, then harmonize only
   features shared across datasets.
4. Calculate spatial summaries without using the outcome labels.
5. Compare a clinical or molecular baseline against the spatial extension using
   a held-out sample-level split.
6. Report effect sizes, confidence intervals, calibration where applicable,
   missingness, and sensitivity to spatial resolution.

## Falsification and safeguards

- A null association is a valid result.
- No treatment recommendation is produced by the pilot.
- No patient-level claim is made from cell-line or ex-vivo data.
- Batch, tissue quality, tumour purity, and cell-line identity are reported.
- Any recurrence model requires an external clinical cohort and a pre-specified
  endpoint; it cannot be inferred from spatial data alone.

## Deliverables

- `evidence/pubmed.json`: verified literature records and their roles.
- `data/registry.tsv`: accession, provenance, license, fields, and QC status.
- `data/signatures.json`: candidate spatial feature genes, explicitly unfrozen.
- Reproducible download and preprocessing scripts.
- Locked analysis code and tests against small synthetic fixtures.
- A pilot report with negative results and limitations included.
