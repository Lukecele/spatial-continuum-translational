# Spatial Continuum Translational

Canonical translational repository and submission home for the Spatial Continuum
project. It provides research extensions for the unchanged
[`spatial-continuum-oncology`](https://github.com/Lukecele/spatial-continuum-oncology)
package, which remains a legacy software dependency rather than the submission
destination.

Repository: https://github.com/Lukecele/spatial-continuum-translational

Research hub: [Luca's Cave](https://lucacelebrano.me/) · [ORCID](https://orcid.org/0009-0007-0931-3555) · [LinkedIn](https://www.linkedin.com/in/luca-celebrano/)

## ⚡ 60-Second Quickstart

Install the package and run the exploratory GIST phenotype model in Python:

```bash
git clone https://github.com/Lukecele/spatial-continuum-translational.git
cd spatial-continuum-translational
pip install -e .
```

```python
from spatial_continuum_translational.gist import GistFeatures, score_gist_research_profile

# Compute transparent exploratory GIST phenotype score
features = GistFeatures(
    mitoses_per_50_hpf=5,
    site="gastric",              # gastric, duodenal, jejunal_ileal, rectal, other
    tumor_rupture=False,
    mutation="kit_exon11",       # kit_exon11, kit_exon9, pdgfra, wild_type, other
    tumor_size_cm=8.0,
)
result = score_gist_research_profile(features)
print(f"Exploratory Score: {result.score:.3f}")
print(f"Components: mitotic={result.mitotic_component}, site={result.site_component}, size={result.size_component}")
```

The same research-only calculation is available as a CLI, which emits JSON by
default and TSV when requested:

```bash
spatial-continuum-gist \
  --mitoses-per-50-hpf 5 \
  --site gastric \
  --mutation kit_exon11 \
  --tumor-size-cm 8
```

```bash
spatial-continuum-gist \
  --mitoses-per-50-hpf 5 \
  --site gastric \
  --mutation kit_exon11 \
  --tumor-size-cm 8 \
  --format tsv \
  --output gist-score.tsv
```

For reproducible user-provided cohorts, use a UTF-8 TSV, CSV, or JSON file with
these required fields:

`mitoses_per_50_hpf`, `site`, `tumor_rupture`, `mutation`, `tumor_size_cm`

An optional `sample_id` is preserved in the annotated output. The CLI runs
locally, does not upload input data, validates every row, and emits the fixed
model version in the result:

```bash
spatial-continuum-gist \
  --input examples/gist_cohort.tsv \
  --format tsv \
  --output results/gist_cohort_scored.tsv
```

The machine-readable bio.tools draft metadata is maintained at
[`metadata/biotools.json`](./metadata/biotools.json) and describes the CLI as
an emerging research tool, not a clinical predictor.

Run test suite:
```bash
pytest tests/
```

## Scope

The first extension is a transparent, exploratory GIST phenotype score. It uses
mitotic rate, anatomical site, tumour rupture, mutation group, and tumour size
as explicit inputs. It is **not** a calibrated probability, a clinical decision
rule, or a treatment recommendation.

The original package remains the source of the legacy NSCLC CRI engine. This
repository only adds new modules and calls the original `cri-calc` through a
compatibility boundary. The included submission package contains its own
research-only CRI calculator for auditability.

## Evidence

The initial evidence set is stored in `evidence/pubmed.json` and was checked
against PubMed on 2026-11-04:

- PMID 24737415: recurrence factors after adjuvant imatinib.
- PMID 30383140: PERSIST-5 adjuvant imatinib context.
- PMID 38598874: prognostic context of R1 margins.

These papers motivate the input features; they do not validate the score.
Calibration and external validation are future work.

## Study protocol

The pilot question, hypotheses, data requirements, and falsification safeguards
are defined in `docs/study_protocol.md`. Candidate datasets are tracked in
`data/registry.tsv` and are not treated as evidence until their metadata is
verified.

## Development

```bash
python -m pip install -e ../spatial-continuum-oncology
python -m pip install -e '.[test]'
python -m pytest
```

The old repository is deliberately not modified by this project.

The current pilot follows the lightweight metadata-first validation path in
`docs/lightweight_validation_plan.md`; the large gene-count archives are an
optional future enhancement, not a prerequisite.

## DOI

- Project concept DOI: [10.5281/zenodo.23956445](https://doi.org/10.5281/zenodo.23956445)
- Version `v0.1.12`: [10.5281/zenodo.23963563](https://doi.org/10.5281/zenodo.23963563)

## Preprint

Celebrano, L. *A Biophysical Reaction-Diffusion Framework for Conditional
Sub-Threshold Compartments in Solid Tumors: An Exploratory Translational Model.*
Research Square, 2026. [10.21203/rs.3.rs-11633521/v1](https://doi.org/10.21203/rs.3.rs-11633521/v1)

## Spatial data inspection

The GSE301973 archive is intentionally kept outside Git because it is large.
After downloading it locally, inspect its contents without extracting everything:

```bash
python scripts/inspect_spatial_archive.py /path/to/GSM9093278_A.tar.gz
```

## Exploratory baseline

After downloading the ignored cBioPortal data, install the analysis extras and
run `python scripts/survival_analysis.py` to reproduce the TCGA-LUAD baseline.
The result is descriptive and is not an osimertinib efficacy claim.

## Submission package

The exploratory preprint and its publication artifacts are collected in
`submission/`. This package includes the authoritative Markdown manuscript,
DOCX/PDF renders, figures, cover letter, research-only CRI calculator, focused
tests, and the associated audit files. It is intentionally kept separate from
the repository's translational analysis code and datasets.

The CRI calculator is deterministic and research-only: it does not estimate
survival, recommend treatment, or provide a clinically validated classifier.
