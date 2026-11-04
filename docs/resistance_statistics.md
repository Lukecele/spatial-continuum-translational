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
