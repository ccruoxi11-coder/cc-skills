# Default stance — CS × biomedical writing

This is the floor for **every** invocation. It is not optional, and it is what makes this
skill different from a pure-CS or pure-clinical writing aid.

## 1. Claim – evidence – boundary (the unit of every paper)

Before drafting anything, force the work into one sentence:

> In [clinical/biological problem], we show [advance] using [approach], validated on
> [internal + external evidence], with [boundary / where it fails].

- Do not invent results, baselines, metrics, sample sizes, p-values, effect sizes, cohorts,
  mechanisms, references, or limitations. Missing input → write `[待补充：…]` and list it under
  *Assumptions or missing inputs* (principle: **don't fabricate**).
- Calibrate verbs to evidence strength: `show / demonstrate` (strong direct), `suggest / indicate`
  (trend / indirect), `may / could` (plausible, unverified). Reviewers in medicine punish
  over-claiming harder than in CS.
- Strike unbounded novelty (`first ever`, `revolutionary`, `clinically ready`) unless the evidence
  — including external validation — genuinely supports it.

## 2. Reporting-standard premise (mandatory, by paper type)

A biomedical-AI paper is judged against a community **reporting standard**, not just by its metrics.
Decide the type early and align both *writing* and *self-check* to its checklist. Source of truth:
the EQUATOR Network (https://www.equator-network.org). Open the matching `references/reporting-standards/*.md` when checking.

| Paper type | Mandatory standard | Primary source |
|---|---|---|
| medical-imaging | **CLAIM** | Mongan et al., *Radiol Artif Intell* 2020 (CLAIM 2024 update) |
| clinical-ml (prediction model) | **TRIPOD+AI** | Collins et al., *BMJ* 2024 |
| prospective AI clinical trial | **CONSORT-AI** (+ **SPIRIT-AI** for protocols) | *Nat Med / BMJ / Lancet Digit Health* 2020 |
| diagnostic-accuracy study | **STARD** (+ **QUADAS-2** for risk of bias) | Bossuyt et al., STARD 2015 |
| systematic review / meta-analysis | **PRISMA 2020** | Page et al., *BMJ* 2020 |

If the type is genuinely ambiguous, ask one targeted question before drafting.

## 3. Clinical / biological validity ≠ CS metrics

A high AUC / Dice / F1 is necessary, not sufficient. Every results-bearing draft must also address,
or flag as `[待补充]`:

- **External validation** — performance on data from a *different* site / scanner / device / cohort,
  not just a held-out split of one dataset.
- **Clinical or biological meaning** — what the number means for a decision (e.g. NRI/decision-curve
  net benefit, effect on a downstream biological readout), not only discrimination.
- **Calibration** — for risk models, calibration plot / slope, not only discrimination (AUC).
- **Subgroup & failure analysis** — performance by site, scanner, sex, age, disease stage; named
  failure modes. "Where does it break and on whom?" is a reviewer's first question.

## 4. Statistical rigor (the cross-disciplinary trap)

CS pipelines routinely violate clinical statistics. Default to, or flag:

- **Correct unit & non-independence** — repeated measures / multiple lesions per patient / multi-site
  data need mixed-effects or clustered methods, not naïve per-sample tests.
- **Split by subject / site, never by sample** — splitting slices, windows, or augmented copies of
  one patient across train/test is **data leakage**. Group-aware splits only.
- **Uncertainty + effect size** — report 95% CIs and an effect size, not bare point estimates or a
  lone p-value.
- **Multiple-comparison correction** — many metrics/regions/genes → correct (Bonferroni / FDR).

Details live in `references/statistics-handbook.md`.

## 5. Reproducibility, ethics, and privacy (the floor for human/biological data)

State, or mark `[待补充]`, never silently omit:

- **Data & code availability** (FAIR): repository + accession/DOI, or a concrete access route;
  random seeds, environment, and exact splits (see stage 08).
- **Ethics / governance**: IRB / ethics-committee approval ID, informed consent or waiver,
  declaration of Helsinki / institutional equivalent. For animal work, the relevant approval.
- **Privacy / compliance**: how patient data were de-identified; relevant regime (e.g. HIPAA / GDPR /
  local regulation) — name only what the user confirms, otherwise `[待补充：伦理审批号 / 数据合规依据]`.

Do not draft fake approval numbers or consent language. Ethics text is the author's legal
responsibility — produce a template with placeholders and tell the user to fill verified values.

## 6. Intake — confirm before drafting

If `core claim`, `evidence`, or `boundary` is missing, or the paper type is ambiguous, run the
confirmation gate in `workflow.md` (step 0): echo back the one-sentence argument, state the detected
axes and the mandatory standard, ask at most 2–3 targeted questions, and wait. A wrong premise wastes
the whole draft.
