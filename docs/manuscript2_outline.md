# Manuscript 2 Working Outline

## Working title

Evidence-linked molecular and spatial characterization of recurrence-associated
microenvironmental features in lung adenocarcinoma: a reproducible pilot study

## Central claim to test

Public molecular and spatial data can support a reproducible hypothesis about
microenvironmental restriction and recurrence-associated phenotypes, but the
current study does not establish osimertinib efficacy or a clinical decision rule.

## Planned sections

1. **Introduction**: motivate the spatial-continuum hypothesis and state the
   distinction between mechanistic plausibility and clinical validation.
2. **Data and evidence**: GEO, cBioPortal cohorts, accession records, PubMed
   roles, licensing, and exclusion criteria.
3. **Methods**: preprocessing, frozen signatures, baseline survival model,
   spatial QC, feature extraction, train/test boundaries, and missingness.
4. **Results**: cohort flow, QC, descriptive baseline, spatial case study, and
   independent benchmark results.
5. **Sensitivity analyses**: alternative gene sets, spatial resolution, endpoint
   definitions, and removal of high-leverage samples.
6. **Limitations**: small paired spatial case, non-osimertinib-specific clinical
   benchmarks, observational confounding, and lack of prospective validation.
7. **Conclusion**: define the next experiment without treatment advice.

## Current evidence state

- TCGA-LUAD baseline Cox: exploratory only; EGFR HR 1.06, 95% CI 0.61-1.84,
  p=0.84 after age, stage grouping, TP53, and RB1 adjustment.
- TRACERx: contextual benchmark; current RFS status encoding is unsuitable for
  the first quantitative event model.
- GSE301973: one paired pre/post spatial case; suitable for pipeline QC and
  hypothesis generation, not population inference.

The manuscript remains a protocol-plus-pilot until an external clinical cohort
and a properly powered spatial cohort are identified.
