# Original Manuscript Claim Audit

## Supported or directly grounded claims

- Mori et al. (PMID 25641031): 211 analyzed lung-cancer patients and mean IFP
  8.5 mmHg are directly supported by the abstract.
- Planchard et al. (PMID 26902828): extensive distribution, low/moderate
  clearance, and mean half-life 48.3 hours are directly supported.
- Offin et al. (PMID 31228622): 43/863 EGFR-mutant cases with TP53/RB1
  co-alterations, 18% transformation among evaluable cases, and shorter time to
  discontinuation are directly supported.
- The existence and titles of all 24 PMID identifiers in the original repo were
  resolved by the automated source audit.

## Derived model quantities

The following are computations or assumptions built from cited parameters, not
values directly measured in every cited paper: `D_eff`, `lambda`, `r_crit`, the
31.28% sanctuary fraction, the parameter sensitivity envelope, and the CRI
weights. They must be labeled as model-derived quantities.

Independent recalculation with standard Bessel functions gives `r_crit =
166.34 um` and a viable-cord sanctuary fraction of `30.90%` for the stated
baseline parameters. The manuscript reports 165.89 um and 31.28%; this is a
small numerical discrepancy, but it should be corrected or explained before
the original manuscript is reused.

The six cohort sizes printed in the original table sum to `3,201`, not the
reported `3,205`. This is an arithmetic discrepancy requiring correction.

## Requires claim-level rechecking

- Exact 67.9% and 57.9% ADAURA event-clustering values require table/figure-level
  verification against the full PMID 40097663 article, not only identifier
  resolution.
- The 75-80% absence of C797S claim requires explicit cohort denominators and
  assay definitions.
- Cross-drug sanctuary percentages require parameter provenance and a common
  calculation protocol for every drug.
- The SG-ADAURA phase III design is a proposed protocol, not clinical evidence.

The ADAURA ctDNA abstract directly supports the rounded event claims: 19/28
events after cessation (67.9%), 11/19 within 12 months (57.9%), and a 4.7-month
median lead time with 95% CI 2.2-5.6 months.

## Conclusion

The old manuscript has a valid source backbone, but source resolution is not
claim validation. The new manuscript must preserve that distinction.
