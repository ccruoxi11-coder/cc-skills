# Stage 07 — English polishing (zh→en / Nature-style)

**Goal:** clear, correctly hedged scientific English that preserves the author's intent.

## Steps

1. **Translate intent, not syntax.** Chinese lab notes pack background+method+implication into one
   sentence. Decompose into claim / evidence / condition / comparison / implication / limitation, then
   write English in the order the *section* needs (see `language/zh-to-en.md`).
2. **Calibrate hedging.** `显著提高` without a comparator → add the baseline or soften; `首次/创新性`
   without scope → bound it. Match verb to evidence strength.
3. **Sentence hygiene.** One idea per sentence; explicit connectives (however/therefore/whereas);
   prefer active voice for what *you* did; cut filler (`it is worth noting that`, `as we all know`).
4. **Terminology lock.** Keep one canonical English term per concept across the whole paper; do not let
   polishing reintroduce synonyms (a frequent Chinese-author issue).
5. **Nature-style register** when the venue calls for it: lead with significance accessible to a broad
   reader, then specifics (see `venue/nature-family.md`).
6. **Match the target journal's house style** when the user supplies a few of its papers: run
   `scripts/journal_style_profile.py --exemplars refs/ --manuscript draft.txt` to see where the draft
   over-claims, under-hedges, or under-cites relative to the journal, and revise the *register* (never
   the claim) to fit. Workflow + qualitative checks in `references/journal-fit.md`.

## Common pitfalls

- Over-literal translation that keeps Chinese clause order.
- Inflated claims surviving from the draft (`greatly`, `perfectly`, `comprehensively`).
- Terminology drift; pronoun-less repetition of a topic noun.
- "Polishing" that silently changes a scientific claim — never alter substance while editing language.

## Output

Polished English **first**, then a short Chinese note on the major structural/hedging/terminology
changes (so the author can verify intent quickly).
