# Exploratory Resistance-State Statistics

## Xenium paired design

The five patients with TN/PD sections were paired by patient. Differences are
computed as `PD - TN` and summarized with exact Wilcoxon tests and a fixed-seed
bootstrap interval for the mean difference.

The mean alveolar score difference is -1.10 and the mean neuroendocrine score
difference is +0.40. These signals are hypothesis-generating only: there are
five pairs, the panel is targeted, and the linked evidence is currently a
preprint.

## snRNA state design

The groups are unmatched observational samples: TN (28), MRD (14), and PD
(31). Kruskal-Wallis p-values are reported only as exploratory diagnostics. The
observed differences in `nCount_RNA` and `nFeature_RNA` indicate that sequencing
quality and cell composition may differ by state; they are not biological
resistance endpoints.

No patient-level treatment effect, hazard ratio, or clinical recommendation is
inferred from these analyses.

## Structural validation gate

The automated primary-cohort validation passes all checks:

- five complete Xenium TN/PD patient pairs;
- TN, MRD, and PD states present in snRNA metadata;
- 14 MRD, 31 PD, and 28 TN snRNA samples;
- `C797S` localized to the expected PD sample in the available Xenium metadata.

This gate validates cohort structure and metadata integrity only. It is not an
independent biological or clinical validation.

## Signature freeze

Resistance-signatures v1 is frozen in `data/resistance_signatures_v1.json`.
Panel validation reports 100% gene-list coverage for all six signatures in the
GSE342824 Xenium panel. Current metadata analyses use existing panel scores and
treatment-state annotations; they do not treat metadata as gene-expression counts.

The proxy application report is stored in
`data/derived/resistance_signature_proxy_application.json`. Xenium proxies are
available for tumour identity, basal plasticity, neuroendocrine plasticity, and
EGFR/MAPK resistance via `C797S` metadata. Hypoxia and vascular signatures are
not scored without gene-level counts. snRNA currently supports tumour-fraction
proxying only.

## snRNA cell composition

The sample-level composition analysis is stored in
`data/derived/snrna_cell_composition_analysis.json`. Endothelial-cell fraction
averaged 2.6% in TN and 6.6% in PD (exploratory Benjamini-Hochberg FDR 0.024).
Epithelial fraction was highest in MRD, but did not remain significant after
multiple-testing correction. These results may reflect tissue composition or
sampling and are not treatment effects.

Small-cohort mutation associations are also corrected with Benjamini-Hochberg
FDR. The melanoma NRAS signal has uncorrected p=0.044 but FDR=0.131 and is not
considered statistically confirmed. Breast mutation associations likewise do
not survive multiple-testing correction.
