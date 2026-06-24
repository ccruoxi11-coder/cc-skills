# Stage 09 — Pre-submission rejection-risk self-audit

**Goal:** find and fix what a desk editor or reviewer would reject, before submitting.

## Steps

1. **Reporting-standard pass.** Run `scripts/reporting_check.py` against the mandatory standard for the
   paper type (CLAIM / TRIPOD+AI / CONSORT-AI / STARD / PRISMA). Mark each item present / missing /
   N/A, and fix or `[待补充]` every missing one against the official checklist
   (`references/reporting-standards/*.md`).
2. **Desk-reject sweep** (editor-level): scope fit for the venue; over-claim vs evidence; missing
   ethics/IRB; missing data/code availability; figures/format off-spec; word/section limits.
3. **Reviewer-objection sweep** — triage automatically first with
   `python scripts/stats_leakage_lint.py --manuscript paper.txt --fail-on high`, then work the
   predictable big four for biomedical-AI:
   - *No external validation* → add it or cap the claim.
   - *Data leakage* → prove subject/site-level splits and training-only preprocessing.
   - *Weak/old baselines or unfair comparison* → strengthen.
   - *Stats* → CIs, effect sizes, correct test, multiple-comparison correction, calibration.
   The linter is triage, not authority: fix the underlying gap, don't just satisfy the keyword.
4. **Self-consistency** — abstract numbers == results numbers == table/figure numbers; every claim in
   the abstract is supported in the body; limitations honestly stated.
5. **Venue-fit check (optional).** If the user supplies 3+ papers from the target journal, audit the
   draft's house style with `scripts/journal_style_profile.py` (see `references/journal-fit.md`) —
   over-claiming, missing uncertainty markers, or under-citation relative to the journal show up here.
6. **Decide & route back.** Each finding either gets fixed (return to the owning stage 01/03/04/08) or
   is consciously accepted and pre-empted in the Discussion/limitations.

## Common pitfalls

- Treating the checklist as paperwork at the end instead of fixing the underlying gap.
- Abstract claims the body doesn't support; mismatched numbers across sections.
- Hiding a known limitation that a reviewer will find anyway → name it first.

## Output

The reporting-standard report (the `reporting_check.py` markdown), a prioritized risk list
(severity × likelihood), and the fix/route-back plan.
