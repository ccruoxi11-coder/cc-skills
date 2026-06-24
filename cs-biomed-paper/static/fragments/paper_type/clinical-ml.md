# Paper type: Clinical machine learning (prediction / diagnosis / prognosis)

Patient-level risk, diagnostic, or prognostic models from EHR / labs / tabular / multimodal data.

## Mandatory reporting standard

**TRIPOD+AI** — Transparent Reporting of a multivariable prediction model for Individual Prognosis Or
Diagnosis, AI extension (Collins et al., *BMJ* 2024). Open
`references/reporting-standards/tripod-ai.md`. If the study is a **prospective/interventional trial** of
the model, use **CONSORT-AI** (and **SPIRIT-AI** for the protocol). For a pure diagnostic-accuracy
study, **STARD** + **QUADAS-2**.

## Cross-disciplinary hard rules

- **Discrimination AND calibration.** Report calibration (plot, slope, intercept, or O:E) — not only
  AUC. A well-discriminating but miscalibrated model is clinically misleading.
- **Clinical utility** — decision-curve / net-benefit analysis, or NRI/IDI, at a realistic prevalence
  and operating point.
- **Temporal/geographic external validation** — validate on a later time window or another site.
- **Leakage & immortal-time / look-ahead bias** — features must be available at prediction time; no
  post-outcome variables; split by patient and by time where relevant.
- **Missing data** — report rates and handling (multiple imputation, not silent drop); class
  imbalance handled honestly.
- **Predictors & outcome defined** — definitions, timing, and the reference standard.

## Common pitfalls

AUC-only reporting; no calibration; leakage via future features; internal validation only; complete-case
analysis hiding bias; threshold chosen post hoc.

## Typical metrics

AUC/AUPRC (with CIs), calibration slope/intercept, Brier score, sensitivity/specificity/PPV/NPV at the
operating point, decision-curve net benefit.
