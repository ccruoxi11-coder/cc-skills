# Journal-fit — audit your draft against target-journal exemplars

A target journal has a measurable house style: sentence rhythm, how strongly authors claim, how much
they hedge, how densely they cite, how they report uncertainty, the abstract "moves". Matching it
reduces desk-reject risk and signals you know the venue. This reference + `scripts/journal_style_profile.py`
turn a handful of **published papers from the target journal** into a profile and audit your draft
against it.

Use during stage 07 (polish to the journal's register) and stage 09 (pre-submission). It complements —
does not replace — `venue/*.md` (framing) and `section/*.md` (structure).

## Workflow

1. **Gather 3–6 exemplars** — recent papers *from the target journal and the same article type* (e.g.
   original research, not a review) that resemble your study. The user must supply them; export each
   to plain text (`.txt`/`.md`). Do **not** fetch papers from the web inside the skill or paste text
   you have no right to use — respect each publisher's terms; this is the user's material.
2. **Profile + audit quantitatively:**
   ```
   python scripts/journal_style_profile.py --exemplars refs/ --manuscript mydraft.txt --report fit.md
   ```
   It reports, per feature, the journal's range vs your draft's value and a verdict (in range / above /
   below): sentence & paragraph length, hedging vs promotional language, first person, passive voice,
   uncertainty markers (95% CI/±), citation density.
3. **Read the deviations as *questions*, not commands.** Off-range ≠ wrong. Decide each consciously:
   - *Boosters above / hedging below* → likely over-claiming for this venue → recalibrate verbs to
     evidence (stage 07, `core/stance.md`). This is usually the highest-value fix.
   - *Uncertainty markers below* → headline numbers may lack CIs → fix the substance (stage 04), not
     just the prose.
   - *Citation density below* → may be under-referencing one of the two fields (stage 02).
   - *Sentence/paragraph length off* → a readability tweak, low stakes.
4. **Audit the qualitative features the script can't measure** by reading 1–2 exemplars directly:
   - **Abstract moves** — does the journal lead with clinical significance or with method? Structured
     vs unstructured? Where does the headline number sit?
   - **Intro funnel** — broad significance first (Nature-family) vs method gap first (ML venues)?
   - **Results↔Discussion separation**, figure/table conventions, where Methods sit (end/supplement?).
   - **Reporting-standard adherence** the journal's own papers show (CLAIM/TRIPOD+AI items present).
5. **Revise the draft** to the journal's register — via stage 07 and the relevant `section/*.md` —
   **without changing any scientific claim**. Style adapts to the venue; evidence does not.

## Hard rules

- **Never alter a result, number, or claim to hit a style target.** Match register, not substance.
- The profile is descriptive guidance from the exemplars supplied, **not** a rule and **not** a
  rewrite engine. With <3 exemplars the range is unreliable — say so.
- Do not invent journal norms from memory; measure the exemplars the user gives, or read them.
- Combine with `venue/*.md` (the editorial expectations) — the script measures style, the fragment
  carries the scope/cover-letter/format expectations.
