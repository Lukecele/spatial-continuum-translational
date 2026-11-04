# Controlled-Access Data Request Draft

This draft is prepared for an institutional PI or data-access representative.
No credentials, personal identifiers, or clinical-access tokens are stored in
the repository.

## IMmotion151 / EGA

- Dataset: `EGAS00001004353`
- Study: IMmotion151, metastatic clear-cell renal cell carcinoma
- Requested material: de-identified RNA-seq expression, treatment arm, PFS,
  response, and available MSKCC/IMDC covariates
- Intended use: independent, arm-stratified external validation of a frozen
  renal score; no model refitting on the requested dataset
- Analysis plan: feature mapping and preprocessing frozen before access; patient
  is the replication unit; atezolizumab+bevacizumab and sunitinib remain
  separate estimands; no re-identification; no redistribution
- Public basis: the 15G publication identifies `EGAS00001004353` as the source
  for IMmotion151 expression and outcomes and reports 823 RNA-seq-evaluable
  patients
- Repository contact: `data/derived/renal_external_immotion151_candidate.json`

## NEO-ORB / Breast

- Trial: `NCT01610284`
- Requested material: de-identified patient-level treatment arm, PIK3CA group,
  ORR, pCR, follow-up, and available expression/clinical covariates
- Intended use: independent, treatment-stratified validation of a frozen
  PI3K/letrozole score; no model refitting on NEO-ORB
- Limitation: neoadjuvant ORR/pCR must remain separate from metastatic
  progression endpoints

## Required request attachments

1. Institutional affiliation and responsible PI.
2. Scientific abstract and prespecified analysis plan.
3. Data-security and non-redistribution statement.
4. Confirmation that no re-identification will be attempted.
5. Exact feature list, weights, endpoint, and time origin of the frozen score.

Until approval and receipt of the required files, these cohorts remain
compatibility candidates and cannot be called score-validated.
