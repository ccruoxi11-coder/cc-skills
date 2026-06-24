# TRIPOD+AI — prediction model studies (development & validation)

**Source:** Collins GS, Moons KGM, et al. *TRIPOD+AI statement: updated guidance for reporting clinical
prediction models that use regression or machine learning methods.* BMJ 2024;385:e078378. Extends
TRIPOD 2015 (Collins et al., BMJ 2015, ~27 items). Verify exact items against the published TRIPOD+AI
checklist and the TRIPOD+AI for Abstracts.

> Use for any patient-level diagnostic/prognostic model. Self-audit at stage 09 against the official
> checklist; this is a domain-level guide.

## Domains and high-miss items

**Title & Abstract**
- Identifies the study as developing/validating a prediction model and the modality (regression/ML).
- Structured abstract: objective, data, outcome, predictors, sample size, performance (with CIs).

**Introduction**
- Background, rationale (including the clinical role of the model), and objectives.

**Methods**
- **Source of data & study design** (development, validation, or both); setting & dates.
- **Participants** — eligibility, recruitment; **outcome** definition & timing (blinded to predictors?).
- **Predictors** — definition & timing; **available at the moment of prediction** (no look-ahead).
- **Sample size** justification; **missing data** handling (e.g. multiple imputation).
- **Statistical analysis** — model type, predictor selection, hyper-parameter tuning, internal
  validation (CV/bootstrap), how performance was assessed.
- **Fairness / subgroups** (AI extension) — analyses across relevant subgroups.

**Results**
- Participant flow & characteristics; **model development** details; **full model specification** (so
  others can apply it) or access to it.
- **Performance: discrimination AND calibration** (⚠ calibration routinely omitted), with uncertainty;
  results of any **external validation**.

**Discussion**
- Limitations (overfitting, missing data, generalizability); interpretation vs prior models;
  clinical implications & intended use.

**Other (Open science — AI extension)** ⚠
- **Code, data, and model availability**; protocol/registration; funding; conflicts.

## Cross-disciplinary red flags

- AUC reported, calibration omitted; internal validation only (no temporal/geographic external set).
- Leakage: predictors not available at prediction time; preprocessing/selection on the full dataset.
- Complete-case analysis hiding missingness bias; no subgroup/fairness analysis; model not fully
  specified or shared.

Fill `[待补充]` for any unmet item (especially calibration and external validation) rather than omitting.
