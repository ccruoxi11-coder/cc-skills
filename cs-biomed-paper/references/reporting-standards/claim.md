# CLAIM — Checklist for Artificial Intelligence in Medical Imaging

**Source:** Mongan J, Moy L, Kahn CE Jr. *Checklist for Artificial Intelligence in Medical Imaging
(CLAIM)*. Radiology: Artificial Intelligence 2020;2(2):e200029. Updated **CLAIM 2024** (Tejani et al.,
*Radiol Artif Intell* 2024). The original is a **42-item** checklist modeled on STARD. Verify the exact
current item text against the published checklist — the list below is a domain-level guide.

> Use this to draft an imaging-AI paper and to self-audit at stage 09. Cross-check every item against
> the official CLAIM PDF; do not treat this summary as the authority.

## Domains and the items reviewers most often miss

**Title & Abstract**
- States that AI/ML is used; structured summary of design, methods, results, conclusions.

**Introduction**
- Scientific/clinical background and the specific study objectives / hypothesis.

**Methods — Study design**
- Prospective vs retrospective; study goal (e.g. model creation, diagnostic accuracy).

**Methods — Data**
- Data sources; eligibility criteria; **how data were de-identified**; how missing data were handled.

**Methods — Ground truth (reference standard)** ⚠ often weak
- How the reference standard was established; rationale; **annotator qualifications & number**;
  inter-rater variability handling.

**Methods — Data partitions** ⚠ leakage hotspot
- How data were assigned to **train/validation/test at the patient level**; intended sample size;
  no overlap of a patient across partitions.

**Methods — Model**
- Model description detailed enough to reproduce; software/frameworks & versions; initialization,
  pre-training, transfer learning.

**Methods — Training**
- Training approach; hyper-parameters; selection of final model.

**Methods — Evaluation**
- Metrics; **how the operating point was chosen**; statistical measures of significance & uncertainty
  (CIs); methods for explainability; **external/independent validation**.

**Results**
- Flow of cases (a flow diagram); demographic/clinical characteristics; model performance with
  uncertainty; failure analysis.

**Discussion**
- Study limitations including potential bias and generalizability; implications for practice.

**Other**
- Registration number; protocol availability; **source of funding**; **data & code availability**.

## Cross-disciplinary red flags CLAIM is designed to catch

- Patient-level leakage across partitions (slices/patches of one patient split across sets).
- Reference standard / annotation process undefined.
- No external validation; operating point tuned on test data.
- Metrics without uncertainty; no failure analysis; PHI left in images.

Map each item to the manuscript section it belongs in (Methods/Results/Discussion) and fill `[待补充]`
for any unmet item rather than glossing over it.
