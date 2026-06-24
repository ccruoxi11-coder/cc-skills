---
name: cs-biomed-paper
description: >-
  End-to-end SCI paper writing for computer-science × biomedical work (medical imaging, clinical ML /
  prediction models, biosignal & wearable, bioinformatics/omics, methods & benchmarks, systematic
  reviews). Routes the full pipeline — topic & novelty, literature, method, experiment & statistics,
  submission-grade figures, section drafting, Chinese-to-English polishing, citation & data/code (FAIR)
  statements, pre-submission rejection-risk audit, and point-by-point reviewer rebuttal — while
  enforcing the cross-disciplinary hard constraints (CLAIM / TRIPOD+AI / CONSORT-AI / STARD / PRISMA
  reporting standards, external validation, clinical validity beyond CS metrics, statistical rigor,
  reproducibility, ethics/privacy). Use whenever the user writes or revises a biomedical-AI paper,
  drafts a section, makes a submission figure, replies to reviewers, or runs a reporting-standard or
  rejection-risk check. Chinese triggers: 医工交叉、医学AI、SCI写作、写论文/写paper、写引言/写方法/写讨论/
  写摘要、医学影像、临床预测模型、生物信号/可穿戴、生物信息/组学、方法基准、系统综述、投稿级图/配图、
  审稿回复/rebuttal、数据可用性、报告规范、外部验证、统计检验、消融实验、拒稿自查.
version: 1.1.0
---

# CS × Biomedical Paper — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (the default stance + the full submission workflow + output format, plus per-stage / per-section / per-paper-type / per-venue / per-language playbooks).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the request's axes and loads only the fragments needed for the current job, then reaches for heavy `references/` material on demand.

Do not apply the writing or reporting logic from memory or from this router. Always load the fragments from disk as described below. The router is deliberately short — update fragments, not this file, when adding scope.

## Routing protocol

Follow these five steps every time the skill is invoked.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the axes (`stage`, `section`, `paper_type`, `venue`, `language`), the allowed values, and the file each value maps to.

Then Read every file under `always_load`:

- `static/core/stance.md` — claim–evidence–boundary discipline, the reporting-standard premise, and the ethics / reproducibility / privacy floor that applies to **every** biomedical-AI manuscript.
- `static/core/workflow.md` — the 10-stage selection-to-submission workflow.
- `static/core/output-format.md` — the default shape of what you return.

### 2. Detect the axis values for this request

For each axis, decide the value using the manifest `detect:` hint and the user's input:

- `stage` — one or several of the 10 pipeline stages. **Multi.** This is the primary axis.
- `section` — abstract / intro / related-work / method / experiments / results / discussion / conclusion / title. May be multiple. Only relevant when drafting prose.
- `paper_type` — medical-imaging / clinical-ml / bioinformatics-omics / biosignal-wearable / methods-benchmark / systematic-review. This decides which **reporting standard** is mandatory.
- `venue` — nature-family / ieee-tmi-media / miccai-cvpr-neurips / general-sci. Default: general-sci.
- `language` — zh-to-en (default for Chinese or mixed notes) / en.

State the detected axis values in one short line before working, so the user can correct you cheaply (principle: **explicit over implicit**).

### 3. Load the matching fragments

Read only the fragment files the detected values map to. Do **not** read all of `static/fragments/`. For a multi-value axis (`stage`, `section`), load each selected value's fragment.

The `paper_type` fragment names the mandatory reporting standard — note its `references/reporting-standards/*.md` pointer but open that only when actually checking the manuscript (step 5).

### 4. Do the work, applying fragments in priority order

1. Core stance (`core/stance.md`) — surface missing claim / evidence / boundary and the reporting/ethics premise first.
2. Stage playbook(s) — the operational steps for this part of the pipeline.
3. Paper-type playbook — the cross-disciplinary constraints (reporting standard, clinical validity, leakage/validation rules) for this kind of work.
4. Section playbook(s) — structure and per-section rules, when drafting prose.
5. Venue framing — journal/conference expectations.
6. Language rules (apply last) — zh-to-en repair or en.

Run the workflow in `core/workflow.md`. Prefer producing a **usable file** over describing it (principle: **output first**): run `scripts/` for searches, reporting checks, figures, and rebuttal scaffolds when the environment allows.

When essential evidence, statistics, or boundary is missing, write an explicit placeholder such as `[待补充：外部验证队列的 AUC 与 95% CI]` and list it under `Assumptions or missing inputs:` — never invent numbers, baselines, p-values, sample sizes, or citations.

### 5. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest. Typical triggers:

- Checking a manuscript against the mandatory standard → `references/reporting-standards/<standard>.md`.
- Statistical design questions (mixed effects, CIs/effect size, multiple comparisons, subject/site-level splits) → `references/statistics-handbook.md`.
- Making a submission-grade figure → `references/figure-standards.md` (+ `scripts/figure_template.py`).
- Structuring a reviewer reply → `references/rebuttal-patterns.md` (+ `scripts/rebuttal_build.py`).
- Venue-specific submission mechanics → `references/venue-submission.md`.

## Worked examples & self-test (optional)

- `examples/*.md` are on-demand worked examples (write an intro, reply to a "no external validation"
  reviewer, polish a Chinese abstract) showing the expected routing + output shape. Read one only when
  a user request closely matches it; they are **not** loaded by default.
- `tests/routing_smoke_test.py` is a stdlib-only guardrail: it checks every manifest path exists, the
  frontmatter is valid, and the Chinese routing cues + paper_type→standard mappings haven't drifted.
  Run it after editing the manifest or fragments: `python tests/routing_smoke_test.py`.

## Why this split

- The static layer is versioned and reviewable; adding a paper type, venue, or section is **one new file plus one manifest line** (principle: **self-contained & extensible**).
- The dynamic layer keeps each invocation cheap: only the fragments for this job enter context, not the full reference set.
- Reporting standards, statistics, and figure rules live in `references/` so a short drafting run stays light but the hard constraints are one hop away.
