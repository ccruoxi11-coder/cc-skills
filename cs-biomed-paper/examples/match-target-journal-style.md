# Example — "按这几篇目标期刊的文章风格，帮我审核修改我的稿子"

The user supplies a few published papers from the journal they're targeting and asks to align their
draft to that journal's style. Routes through the journal-fit workflow.

## Detected axes

`stage: 07-polish-en (+ 09-prereview-risk) / paper_type: [from content] / venue: [the named journal] /
language: zh-to-en or en`

→ load `stage/07-polish-en.md`, the matching `venue/*.md`, `language/*.md`. Open
`references/journal-fit.md` on demand and run `scripts/journal_style_profile.py`.

## Inputs needed

- **3–6 exemplars** from the *target journal, same article type* (original research, not reviews),
  exported to `.txt`/`.md` by the user. `[待补充：目标期刊的 3–6 篇代表作（用户提供，注意版权）]`.
- The user's draft as `.txt`/`.md`. The skill measures only supplied text — it does not fetch papers
  or invent journal norms.

## Workflow (per `references/journal-fit.md`)

1. Profile + audit quantitatively:
   ```
   python scripts/journal_style_profile.py --exemplars refs/ --manuscript mydraft.txt --report fit.md
   ```
   Output: a table of the journal's range vs the draft for sentence/paragraph length, **hedging vs
   promotional language**, first person, passive voice, **uncertainty markers (95% CI/±)**, citation
   density — each marked in-range / above / below.
2. Treat each deviation as a *question*, prioritized:
   - **boosters above / hedging below** → over-claiming for this venue → recalibrate verbs to evidence
     (highest-value fix; `core/stance.md` + stage 07).
   - **uncertainty markers below** → the substance may lack CIs → back to stage 04, not just wording.
   - **citation density below** → check both-field coverage (stage 02).
3. Read 1–2 exemplars directly for what the script can't measure: abstract moves (significance-first vs
   method-first), Results↔Discussion separation, where Methods sit, figure conventions.
4. Revise the draft to the journal's register via stage 07 + `section/*.md` — **without changing any
   scientific claim**.

## Claim–evidence map

`Claim: draft fits the journal | Evidence: profile deviations + exemplar reading | Status: descriptive
guidance, author decides each change`

## Assumptions or missing inputs

- `[待补充：目标期刊及 3–6 篇代表作]`、`[待补充：用户稿件纯文本]`. With <3 exemplars the profile range is
  unreliable — say so and ask for more.

## Reporting-standard hooks

Not a reporting-standard step, but "uncertainty markers below the journal" and "over-claiming" often
co-occur with real CLAIM/TRIPOD+AI gaps (missing CIs, unbounded claims) — route those to stage 09.

## Hard rule

Match *register*, not *substance*. Never alter a result, number, or claim to hit a style target, and
never invent a journal norm — measure the exemplars the user gives.

## Next minimal action

Ask the user for 3–6 target-journal papers (as text) + their draft; run the profiler and return the
prioritized deviation list with concrete, claim-preserving edits.
