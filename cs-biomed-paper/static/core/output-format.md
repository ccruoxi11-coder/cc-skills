# Output format

Every response delivers a usable artefact plus the honesty scaffolding around it.

## Default shape

1. **Detected axes** — one line: `stage / paper_type → standard / section / venue / language`.
   Lets the user correct routing cheaply (principle: **explicit over implicit**).
2. **One-sentence argument** — the claim–evidence–boundary in a single line (from `stance.md`):
   `In [problem] we show [advance] via [approach], validated on [internal + external], bounded by
   [where it fails].` Write it first so the artefact serves the argument, not the other way round.
   If the argument can't be stated yet, that *is* the deliverable — run the Stage 0 gate.
3. **The artefact** — the actual deliverable for the stage:
   - drafting → the prose (and a 3–7 bullet section outline for a full section);
   - experiment/stats → a design table or test plan;
   - figures → the generated file path + the script used;
   - literature → the verified reference list / `.bib` path;
   - self-audit → the reporting-standard report (present / missing / N/A per item);
   - rebuttal → the point-by-point skeleton.
4. **Claim–evidence map** (when results or claims are involved):
   `Claim: … | Evidence: … | Status: supported / needs evidence / inferred`.
5. **Assumptions or missing inputs** — every `[待补充：…]` placeholder, the validation gaps, and any
   ethics/stat item that must be filled with a *verified* value. Do not pad with style nits.
6. **Reporting-standard hooks** — which checklist items this artefact satisfies and which remain open.
7. **Next minimal action** — the single highest-leverage next step (e.g. "add the external cohort's
   AUC + 95% CI to Table 2"), plus a one-line invitation to redirect: "Name the paragraph, claim, or
   checklist item that is off and I'll revise only that."

## Language convention

For Chinese-author input (`language: zh-to-en`), give the **polished English first**, then a short
Chinese note explaining the major structural / hedging / terminology choices, so the author can verify
intent without re-reading the English from scratch.

## Hard rules on fabrication

- Never invent: numbers, baselines, p-values, CIs, effect sizes, sample sizes, cohort details,
  citations/DOIs, ethics approval IDs, or consent language.
- Missing value → `[待补充：<what is needed and where it goes>]`, surfaced in *Assumptions*.
- Every non-obvious rule you apply should carry its reason or source inline (principle: **primary
  source first**), so the user can audit the advice, not just trust it.

## Files over descriptions

When a script can produce the artefact (`.bib`, figure, checklist report, rebuttal skeleton), run it
and hand back the file path. A real, openable file beats a paragraph describing one.
