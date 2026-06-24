# Selection-to-submission workflow (10 stages)

The `stage` axis maps 1:1 onto these. A request usually touches one or a few stages; load only those
fragments, but keep the whole arc in mind so earlier choices (claim, validation plan, reporting
standard) constrain later ones. Each stage fragment has the operable detail; this file is the spine.

## Stage 0 — Alignment gate (always, before drafting prose)

Echo back **all six fields below** in a short block, then stop for confirmation whenever any field is
assumed, blank, or marked `[待补充]`. These fields are mandatory — do not silently fill or skip one.

```
Claim–evidence–boundary : <one sentence: in [problem] we show [advance] via [approach],
                           validated on [internal + external], bounded by [where it fails]>
Paper type              : <medical-imaging | clinical-ml | bioinformatics-omics |
                           biosignal-wearable | methods-benchmark | systematic-review>
Mandatory standard      : <CLAIM | TRIPOD+AI | CONSORT-AI | STARD | PRISMA> (from paper type)
External validation     : <yes: which independent site/scanner/device/cohort/time window
                           | no → claim is capped to internal performance; say so explicitly>
Detected axes           : stage(s) / section(s) / venue / language
Missing inputs          : <every [待补充] needed before a credible draft — data, CI, ethics ID, …>
```

Then ask at most **2–3 targeted questions** on the highest-leverage ambiguity only.

Skip the gate only when claim, evidence, boundary, type, **and external-validation status** are all
unambiguous; even then, state the one-sentence argument and the external-validation status in a single
line before proceeding. A wrong premise — especially an unnoticed lack of external validation — wastes
the whole draft.

## The 10 stages

1. **Topic & novelty positioning** — turn an idea into a defensible claim: the gap, the contribution
   list, the boundary, and *why a biomedical reader should care* (clinical/biological stakes), not
   just CS novelty. → `stage/01-topic-claim.md`
2. **Literature search & synthesis** — multi-source search (PubMed + CS venues + preprints),
   DOI/citation verification, synthesis by theme not by paper. → `stage/02-litreview.md`
   (run `scripts/ref_search_verify.py`).
3. **Method design & description** — task formulation, pipeline, per-module motivation/mechanism/role,
   reproducible detail, and the leakage-safe data flow. → `stage/03-method.md`
4. **Experiment & statistics design** — datasets, baselines, ablations, metrics, **external
   validation**, group-aware splits, statistical tests, CIs/effect sizes, multiple-comparison
   correction, power. → `stage/04-experiment-stats.md` (+ `references/statistics-handbook.md`).
5. **Submission-grade figures** — the right chart for the message, panel layout, fonts/colour/size to
   spec, accessibility, vector output. → `stage/05-figures.md` (run `scripts/figure_template.py`).
6. **Section drafting** — abstract / intro / related-work / method / experiments / results /
   discussion / conclusion / title, each to its `section/*.md` rules. → `stage/06-section-writing.md`.
7. **English polishing (zh→en / Nature-style)** — translate intent not syntax, calibrate hedging,
   fix Chinese-author patterns, keep terminology consistent. → `stage/07-polish-en.md`.
8. **Citation & data/code availability (FAIR)** — reference manager export, Data/Code Availability
   statements, ethics & privacy text, seeds/environment. → `stage/08-citation-data-fair.md`.
9. **Pre-submission rejection-risk self-audit** — run the manuscript against the mandatory reporting
   standard + a desk-reject / reviewer-objection checklist. → `stage/09-prereview-risk.md`
   (run `scripts/reporting_check.py`).
10. **Point-by-point reviewer rebuttal** — structure every comment into a reply with the change made,
    location, and evidence; calibrate tone. → `stage/10-rebuttal.md` (run `scripts/rebuttal_build.py`).

## End-to-end loop

`idea + data → 01 claim → 02 literature → 03 method → 04 experiments+stats → 05 figures →
06 draft sections → 07 polish → 08 FAIR + ethics → 09 self-audit (fix gaps, back to relevant stage) →
submit → reviews → 10 rebuttal → revise (back to 03–08) → resubmit.`

Stage 09 frequently sends you back: a missing external validation (04), an unstated seed (08), or an
over-claim (01) found in self-audit must be fixed *before* submission, not defended later.

## Output discipline at every stage

Follow `output-format.md`: deliver the artefact (prose, table, figure file, .bib, checklist report,
rebuttal skeleton) **plus** an explicit *Assumptions / missing inputs* list. Prefer running a script
to produce a real file over describing one (principle: **output first**).
