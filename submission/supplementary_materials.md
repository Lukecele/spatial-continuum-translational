# Supplementary Materials

## Scope

This supplementary file supports the exploratory reaction-diffusion manuscript.
It documents model inputs, derived quantities, sensitivity scenarios, software
checks, the research-only CRI mapping, and the exploratory GIST benchmark. It
is not an independent clinical validation report and does not provide treatment
recommendations.

## Table S1. Reaction-diffusion parameter ledger

| Quantity | Value | Unit | Status and provenance |
| --- | ---: | --- | --- |
| Capillary radius, $r_0$ | 10.0 | um | Explicit model geometry |
| Plasma trough concentration, $C_{trough}$ | 540 | nM | Source-reported pharmacokinetic input; Planchard et al. 2016 |
| Unbound fraction, $f_u$ | 0.053 | fraction | Source-reported pharmacokinetic input; assay/context dependent |
| Unbound source concentration, $C_0$ | 28.62 | nM | Derived: $C_{trough} f_u$ |
| Cellular threshold, $IC_{50}$ | 10.0 | nM | Provisional source-reported in-vitro input; not a universal tumor threshold |
| Molecular diffusivity, $D_0$ | 607.11 | um^2/s | Derived from Stokes-Einstein assumptions |
| Porosity, $\epsilon$ | 0.25 | fraction | Explicit tissue-model assumption |
| Tortuosity, $\tau$ | 1.60 | dimensionless | Explicit tissue-model assumption |
| Effective diffusivity, $D_{eff}$ | 59.29 | um^2/s | Derived: $D_0\epsilon/\tau^2$ |
| Effective clearance half-life | 1.28 | h | Explicit scenario input, not clinical terminal half-life |
| Elimination rate, $k$ | $1.5052\times10^{-4}$ | 1/s | Derived: $\ln(2)/t_{1/2}$ |
| Penetration length, $\lambda$ | 627.6 | um | Derived: $\sqrt{D_{eff}/k}$ |
| Oxygen-viability boundary, $r_{ox}$ | 200.0 | um | Explicit scenario boundary, not a universal human-tumor constant |
| Threshold ratio, $\theta$ | 0.3494 | dimensionless | Derived: $IC_{50}/C_0$ |

## Table S2. Baseline derived quantities

| Quantity | Value | Interpretation |
| --- | ---: | --- |
| Critical radius, $r_{crit}$ | 165.89 um | Analytical Bessel-profile threshold crossing |
| Conditional shell width, $\Delta r$ | 34.11 um | $r_{ox}-r_{crit}$ under baseline assumptions |
| Conditional viable-cord fraction | 31.28% | Cylindrical volume fraction between $r_{crit}$ and $r_{ox}$ |
| Péclet number | $<0.1$ | Only under the imposed near-flat core IFP-gradient assumption |

The conditional shell is a model-defined concentration region. It is not a
measurement of viable residual disease, dormancy, recurrence, or treatment
failure.

## Table S3. Sensitivity scenarios

All rows use the same $r_0=10$ um, $r_{ox}=200$ um, and source concentration.
The figure uses $IC_{50}=10$ nM; the table additionally varies the threshold.

| $\lambda$ (um) | $IC_{50}$ (nM) | $r_{crit}$ (um) | Interpretation |
| ---: | ---: | ---: | --- |
| 400 | 15.0 | 62 | Conditional sub-threshold region |
| 400 | 8.9 | 148 | Conditional sub-threshold region |
| 627.6 | 10.0 | 165.89 | Baseline; conditional sub-threshold region |
| 800 | 15.0 | 86 | Conditional sub-threshold region |
| 800 | 8.9 | 233 | $r_{crit}>r_{ox}$; no conditional region |
| 3845 | 10.0 | 526 | 48-hour clearance scenario; no conditional region |

These are scenario outputs, not confidence intervals or uncertainty limits.

## Table S4. Péclet boundary calculation

For the model-context gradient of 10 mmHg over 200 um, the implied velocity is
approximately 0.5 um/s. The manuscript's diffusion-dominant condition instead
imposes an approximately flat core pressure profile with an effective gradient
below 5 mmHg/mm, giving $v_{fluid}<0.05$ um/s. With $L=100$ um:

$$Pe=\frac{v_{fluid}L}{D_{eff}}<0.1.$$

At an invasive margin, an illustrative stress-test gradient of approximately
60 mmHg/mm and velocity of 1.0 um/s gives $Pe\approx1.69$. These peripheral
values are illustrative boundary-condition inputs, not patient-level results.

## Table S5. Research-only CRI specification

| Component | Weight | Current mapping |
| --- | ---: | --- |
| Histological pattern, $S$ | 0.47 | lepidic 0.00; acinar/papillary 0.40; mixed/moderate 0.80; solid/micropapillary 1.00 |
| TP53/RB1 genomic state, $G$ | 0.33 | neither 0.00; TP53 only 0.50; RB1 only 0.30; both 1.00 |
| Stromal descriptor, $M$ | 0.20 | low/loose/minimal/normal 0.00; moderate/intermediate 0.50; dense/severe/high/sclerotic/fibrotic 1.00 |

$$CRI=0.47S+0.33G+0.20M.$$

The weights are heuristic author-selected choices. The score has no time,
ctDNA, vessel-distance, tumor-diameter, survival, or treatment-response input.
Its tiers ($CRI<0.30$, $0.30\le CRI\le0.65$, and $CRI>0.65$) are research
strata only, not clinical categories.

## Table S6. Exploratory GIST benchmark

The aligned repository reports a separate patient-level Cox benchmark for
`gist_msk_2023`, distinct from the deterministic research score:

| Quantity | Result |
| --- | ---: |
| Complete patients | 438 |
| RFS events | 205 |
| Tumor-size HR per cm | 1.050 |
| Metastatic-status HR | 5.622 |
| Five-fold mean C-index | 0.881 |
| Five-fold C-index SD | 0.036 |
| Event rates by predicted-risk tertile | 10.3%, 35.6%, 94.5% |
| External validation | Not available |

The benchmark includes metastatic status, which may be leakage-prone for a
recurrence model. These are internal exploratory diagnostics, not validation
of the deterministic GIST score, a calibrated predictor, or a treatment rule.

## Table S7. Software and reproducibility checks

- Research-only CRI calculator: `software_strumenti_calcolo/cri_calc.py`.
- Focused calculator tests: 2 tests plus 3 reference CLI cases.
- Aligned translational repository suite: `PYTHONPATH=src pytest -q`, 7 passed
  in the final audit.
- The expanded reaction-diffusion repository was tested separately; its source
  solver is not required to reproduce the manuscript's analytical Bessel
  calculation.
- Raw patient-level GEO and cBioPortal downloads are not redistributed.

## Limitations

The supplement does not convert source-reported cohort values into new clinical
estimates. No result here establishes a causal sanctuary mechanism, individual
recurrence prediction, osimertinib efficacy, treatment superiority, or clinical
utility of the CRI.
