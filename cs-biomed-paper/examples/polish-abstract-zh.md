# Example — "帮我润色这段摘要"（中文笔记输入）

A polishing request from Chinese lab notes. Shows the zh-to-en repair flow without changing scientific
meaning.

## Detected axes

`stage: 07-polish-en / section: abstract / paper_type: [infer from content] / venue: general-sci
(confirm) / language: zh-to-en`

→ load `stage/07-polish-en.md`, `section/abstract.md`, `language/zh-to-en.md`.

## Method (per `language/zh-to-en.md` — translate intent, not syntax)

1. Decompose each Chinese sentence into **claim / evidence / condition / comparison / implication /
   limitation**, then write English in the order the *abstract* needs (`section/abstract.md`):
   `background/clinical need → gap → what we did → key quantified result (+ uncertainty) → external
   validation → conclusion + boundary`.
2. **Hedge calibration** — `显著提高/明显改善` without a comparator → add the baseline or soften;
   `首次/创新性` without scope → bound it. Match verb to evidence (`show` vs `suggest` vs `may`).
3. **Terminology lock** — one canonical English term per method/dataset/metric; no synonym drift.
4. **Never change the claim** — if a number or comparator is missing, do not invent it; mark
   `[待补充：主指标及 95% CI / 外部队列 n]` and surface it.

## Output convention

Polished English **first**, then a short Chinese note on the major structural / hedging / terminology
changes — so the author verifies intent without re-reading the English.

## Claim–evidence map

`Claim: [from the notes] | Evidence: [待补充：摘要中的数值是否与正文一致] | Status: verify consistency`
(abstract numbers must match the body exactly — the top self-audit failure.)

## Assumptions or missing inputs

- `[待补充：主指标 + 95% CI]`、`[待补充：外部队列 n]`、`[待补充：目标期刊（结构式摘要要求？）]`.

## Reporting-standard hooks

The abstract must not over-claim generalization beyond the validation scope; the headline metric +
uncertainty + cohort sizes are the items a desk editor scans first.

## Next minimal action

Paste the Chinese abstract notes; I return polished English first + a Chinese change note, flagging any
number that must be verified against the body.
