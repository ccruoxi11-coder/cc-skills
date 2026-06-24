# Example — "审稿人说没有外部验证，会不会被拒？怎么回复？"

Two coupled requests: a rejection-risk read (stage 09) and a reviewer reply (stage 10). This is the
single most common biomedical-AI objection, so it doubles as a worked reviewer-risk audit.

## Detected axes

`stage: 09-prereview-risk + 10-rebuttal / paper_type: clinical-ml → TRIPOD+AI / venue: general-sci
(confirm) / language: zh-to-en`

→ load `stage/09-prereview-risk.md`, `stage/10-rebuttal.md`, `paper_type/clinical-ml.md`. Open
`references/rebuttal-patterns.md` and `references/reporting-standards/tripod-ai.md` on demand; run
`scripts/rebuttal_build.py` on the decision letter.

## Risk read (stage 09 — reviewer-risk audit)

"No external validation" is a **first-tier** objection: for a TRIPOD+AI prediction model, external
(temporal/geographic) validation is effectively expected. Severity high, likelihood high. Two routes:

- **Route A — supply it.** If a later time window or another site/hospital exists, run external
  validation and report discrimination **and calibration** there (`[待补充：外部队列 AUC, 95% CI,
  calibration slope/intercept]`). This usually converts the objection.
- **Route B — cap the claim.** If no independent cohort is feasible now, you cannot claim
  generalization. Re-scope the title/abstract/discussion to *internal* performance, add it to
  limitations, and say external validation is future work. Do **not** argue the objection away.

## Reply strategy (stage 10 — per-point)

Per `stage/10-rebuttal.md`, classify the point as *do & show* (Route A) or *justify + partial* (Route
B), then use the fixed template:

```
### R{n}.{k}
**Comment.** > [reviewer's exact words on external validation]
**Response.** We agree external validation is essential. [Route A: we added it / Route B: we have
re-scoped the claim and added it as a limitation].
**Change made.** [Route A: new external-cohort results + calibration; Route B: re-scoped claim in
title/abstract/discussion].
**Location.** [待补充：new Table SX / Results §X / Discussion limitations].
**New/revised manuscript text:** > [待补充：粘贴修改后的稿件原文]
```

Never claim a change was made without making it — editors check.

## Claim–evidence map

`Claim: model generalizes | Evidence: [待补充：外部队列结果] | Status: needs evidence (drives Route A vs B)`

## Assumptions or missing inputs

- `[待补充：是否存在独立时间窗/外部中心数据]` (decides Route A vs B)、`[待补充：原审稿意见全文]`、
  `[待补充：calibration 结果]`.

## Reporting-standard hooks (TRIPOD+AI)

External validation + calibration are explicit TRIPOD+AI items — resolving this objection also closes
two checklist gaps that stage 09 would otherwise flag.

## Next minimal action

Tell me whether an independent cohort exists (Route A) or not (Route B); paste the reviewer's exact
wording and I'll draft the point-by-point reply.
