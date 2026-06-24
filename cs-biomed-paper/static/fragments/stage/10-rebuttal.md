# Stage 10 — Point-by-point reviewer rebuttal

**Goal:** a respectful, complete, evidence-backed reply that makes acceptance easy for the editor.

## Steps

1. **Parse every comment.** Run `scripts/rebuttal_build.py` to split each reviewer's letter into
   atomic, numbered points (R1.1, R1.2, …). Miss none — silence reads as evasion.
2. **Classify** each point: *do & show* (make the change), *clarify* (it exists / was misread),
   *justify* (push back with evidence), or *cannot do* (explain the constraint and offer the best
   alternative). Most should be *do & show*.
3. **Reply template per point:**
   - restate the comment faithfully (no straw-manning);
   - state the **change made**;
   - give the **location** (section/figure/line or "new Table S3");
   - **quote the new manuscript text** (in a coloured/quoted block);
   - reference any new evidence (new experiment, external cohort, added stat).
4. **Tone.** Thank reviewers, agree where possible, disagree only with data and courtesy, never
   defensive or dismissive. Address the editor's summary points explicitly.
5. **Consistency.** Every promised change must actually appear in the revised manuscript; cross-check
   that resolving one comment didn't break another or a number elsewhere.

## Common pitfalls

- Answering only the easy comments; burying a "no" without explanation.
- Claiming a change was made but not making it (editors check).
- Defensive tone; arguing without new evidence.
- Re-introducing inconsistencies (a changed number that the abstract still quotes the old value of).

## Output

The point-by-point response document (one block per numbered comment) + a change-log mapping each reply
to the edited location, via `scripts/rebuttal_build.py`. Deeper patterns: `references/rebuttal-patterns.md`.
