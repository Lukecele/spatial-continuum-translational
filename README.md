# Spatial Continuum Translational

Research extensions for the unchanged [`spatial-continuum-oncology`](https://github.com/Lukecele/spatial-continuum-oncology) package.

## Scope

The first extension is a transparent, exploratory GIST phenotype score. It uses
mitotic rate, anatomical site, tumour rupture, mutation group, and tumour size
as explicit inputs. It is **not** a calibrated probability, a clinical decision
rule, or a treatment recommendation.

The original package remains the source of the NSCLC CRI engine. This repository
only adds new modules and calls the original `cri-calc` through a compatibility
boundary.

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
- Version `v0.1.0`: [10.5281/zenodo.23956462](https://doi.org/10.5281/zenodo.23956462)

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
