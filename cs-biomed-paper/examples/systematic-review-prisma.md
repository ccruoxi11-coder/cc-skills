# Example — "我要写一篇 AI 用于某临床任务的系统综述，怎么开始？"

A systematic-review request. The defining constraint is PRISMA 2020 + a pre-registered protocol — get
these wrong and the review is unsalvageable at review time.

## Detected axes

`stage: 02-litreview (PRISMA mode) + 06-section-writing / paper_type: systematic-review → PRISMA /
section: method + results / venue: general-sci (confirm) / language: zh-to-en`

→ load `stage/02-litreview.md`, `stage/06-section-writing.md`, `paper_type/systematic-review.md`,
`section/method.md`, `section/results.md`. Open `references/reporting-standards/prisma.md` on demand.

## One-sentence argument (Stage 0 gate)

> In [待补充：临床任务] we synthesize [待补充：纳入研究范围] to answer [待补充：PICO/PIRT 问题],
> bounded by [待补充：纳入/排除与异质性].

This is a *review*, so "external validation" is replaced by **risk-of-bias assessment of included
studies** and **heterogeneity/publication-bias** handling — set expectations accordingly.

## Mandatory standard & hard rules (`paper_type/systematic-review.md`)

**PRISMA 2020.** Register the protocol (**PROSPERO**) *before* screening. Then:

- **Pre-registered protocol** — PICO/PIRT, eligibility, analysis plan fixed before searching.
  `[待补充：PROSPERO 注册号]`.
- **Reproducible search** — full search string per database + dates → the **PRISMA flow diagram**
  (identified → screened → eligible → included, with exclusion counts/reasons). Build it with
  `scripts/ref_search_verify.py` feeding the counts; `[待补充：各数据库命中数]`.
- **Dual independent screening & extraction** — report agreement (κ) + conflict-resolution rule.
- **Risk of bias of every included study** — QUADAS-2/QUADAS-AI (diagnostic) or PROBAST(+AI)
  (prediction). Don't skip it.
- **Heterogeneity & pooling** — if meta-analyzing: I², random vs fixed effects, forest plot, funnel/
  Egger for publication bias. If pooling is inappropriate, structured narrative synthesis + why.
- **AI-specific extraction** — model type, modality, validation type (internal/external), each
  included study's reporting-standard adherence.

## Deliverable shape

- **Method**: protocol/registration → search strategy (verbatim strings + dates) → screening &
  extraction → risk-of-bias tool → synthesis plan.
- **Results**: PRISMA flow diagram, study-characteristics table, risk-of-bias summary, forest plot (if
  pooled) + heterogeneity/publication-bias stats — all `[待补充]` until screening is done.

## Claim–evidence map

`Claim: evidence base supports X | Evidence: [待补充：纳入研究数 + 合并效应/叙述综合] | Status: needs evidence`

## Assumptions or missing inputs

- `[待补充：PROSPERO 注册号]`、`[待补充：检索式与日期]`、`[待补充：纳入研究数与流程图计数]`、
  `[待补充：偏倚评估结果]`、`[待补充：异质性 I²]`.

## Reporting-standard hooks

Missing protocol registration, single-reviewer screening, no flow diagram, and skipped risk-of-bias are
the four PRISMA failures that get reviews rejected — this plan closes all four up front.

## Next minimal action

Confirm the PICO/PIRT question and whether the protocol is registered; then I draft the eligibility
criteria + search strategy section.
