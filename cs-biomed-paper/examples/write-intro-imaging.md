# Example — "帮我写这篇医学影像分割论文的引言"

A high-frequency drafting request. Shows the expected routing and the output shape; all data are
`[待补充]` placeholders (the skill never invents clinical facts or numbers).

## Detected axes

`stage: 06-section-writing / paper_type: medical-imaging → CLAIM / section: intro / venue: general-sci
(default, confirm) / language: zh-to-en`

→ load `stage/06-section-writing.md`, `section/intro.md`, `paper_type/medical-imaging.md`,
`language/zh-to-en.md`. Note the CLAIM pointer (`references/reporting-standards/claim.md`) but don't
open it until the stage-09 self-audit.

## One-sentence argument (Stage 0 gate — confirm before drafting)

> In [待补充：临床分割任务，如肝脏肿瘤], we show [待补充：分割精度/效率优势] using [待补充：方法],
> validated on [待补充：内部队列 + 至少一个外部中心/扫描仪], bounded by [待补充：未覆盖的人群/模态].

External validation status: **[待补充]** — if there is no independent site/scanner cohort, the
generalization claim must be capped here, and the intro must not promise multi-center performance.

## Deliverable — intro skeleton (paragraph-job map)

Per `section/intro.md`: `clinical stakes → current practice & limits → methodological gap → this work
→ contributions`.

1. **Clinical stakes** — burden/decision the segmentation supports, with a **sourced** epidemiology
   fact. `[待补充：流行病学数据来源]` — do not assert a number without a citation.
2. **Current practice & its limits** — manual/semi-automatic segmentation cost, inter-rater
   variability `[待补充：reader 变异数据]`; why it limits the downstream decision.
3. **Dual gap** — (a) clinical: what decision is still limited; (b) methodological: why existing
   methods (cite the CS + clinical literature, stage 02) don't close it. End the gap exactly where the
   contribution begins.
4. **This work** — approach in one sentence + the bounded claim.
5. **Contributions** — 2–4 verifiable bullets, clinical impact first for a medical venue.

## Claim–evidence map

`Claim: method improves [task] | Evidence: [待补充：内部+外部 Dice/HD95 与 95% CI] | Status: needs evidence`

## Assumptions or missing inputs

- `[待补充：目标临床任务与终点]`、`[待补充：外部验证队列]`、`[待补充：流行病学数据来源]`、
  `[待补充：目标期刊以确认 venue]`.

## Reporting-standard hooks (CLAIM)

Intro should already set up: study objective/hypothesis, intended clinical use, and the prospective
vs retrospective framing — CLAIM items that reviewers expect signalled early.

## Next minimal action

Confirm the one-sentence argument + external-validation status; then I draft paragraph 1 (clinical
stakes) once the epidemiology source is provided.
