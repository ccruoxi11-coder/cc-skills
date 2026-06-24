# Stage 06 — Section drafting

**Goal:** draft or rebuild manuscript sections, each to its own rules.

## Steps

1. Identify which **section(s)** are in scope and load the matching `section/*.md` fragment(s).
2. Map each paragraph to **one job**: context, gap, approach, result, comparison, mechanism,
   implication, or limitation. Split any paragraph carrying two jobs.
3. Draft **from evidence outward** — keep each claim next to the data that support it; do not stack
   claims at the top and bury evidence at the bottom.
4. Keep the **Terminology Ledger** stable: lock the canonical name of each method, model, dataset,
   metric, and abbreviation on first use and reuse it everywhere.
5. Calibrate verbs to evidence (`show` vs `suggest` vs `may`); sweep out unsupported novelty/universal
   claims (`first`, `unique`, `always`).
6. Honour the **mandatory reporting standard** as you write — e.g. a CLAIM/TRIPOD+AI item belongs in
   the section it maps to, not only in a checklist at the end.

## Drafting order

Plan title + abstract early, **draft them last** (they summarize the finished argument). Usual draft
order: method → experiments/results → intro → discussion → conclusion → abstract → title.

## Common pitfalls

- Results and interpretation braided together → observations belong in Results, meaning in Discussion.
- Inconsistent terminology across sections.
- A section that ignores the reporting standard, forcing a painful retrofit at stage 09.

## Output

The drafted section(s) per `core/output-format.md`, with the paragraph-job map in *Why this structure*.
