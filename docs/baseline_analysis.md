# Baseline Clinical Summary

The baseline is descriptive and patient-level. It is not a fitted survival
model and it does not estimate treatment efficacy.

## Endpoint mapping

- TCGA-LUAD (`luad_tcga_pan_can_atlas_2018`): `DFS_STATUS`;
  `1:Recurred/Progressed` is an event and `0:DiseaseFree` is non-event.

TRACERx is not included in this first quantitative summary because its extracted
RFS field contains only `Recurrence` and `Deceased`, with no usable non-event or
censoring category for this comparison. It remains a contextual benchmark.
No cross-study hazard ratio is reported.

## Reproduction

After downloading the ignored raw data:

```bash
python scripts/baseline_summary.py
```

The output is `data/derived/baseline_event_summary.tsv`. Mutation groups mean
that a mutation was observed in the focused cBioPortal mutation profile; they do
not mean that a patient was clinically EGFR-mutant unless the source metadata
supports that interpretation.
