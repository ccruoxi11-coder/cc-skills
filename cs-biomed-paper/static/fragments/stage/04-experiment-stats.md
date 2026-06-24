# Stage 04 — Experiment & statistics design

**Goal:** evidence that survives both ML and clinical review. This stage is where most
cross-disciplinary papers are won or lost.

## Steps

1. **Datasets & splits.** Internal cohort + at least one **external** cohort (different site/scanner/
   device/population) for the generalization claim. Splits **grouped by subject/site**. Report the
   cohort table (n, demographics, prevalence, inclusion/exclusion).
2. **Baselines** — strong, current, fairly tuned, including the clinically used method or a clinician
   reference where relevant. A straw-man baseline is a reviewer red flag.
3. **Ablations** — isolate each claimed contribution (one change at a time). Tie each to a module
   from stage 03.
4. **Metrics — CS + clinical.** Beyond AUC/Dice/F1: **calibration** (for risk models), and
   clinical-utility metrics where they apply (sensitivity/specificity at a chosen operating point,
   PPV/NPV at realistic prevalence, decision-curve net benefit, NRI). Pick the operating point by a
   stated rule, not post hoc.
5. **Statistics.** 95% CIs and an effect size on every headline number (bootstrap CIs for AUC/Dice
   are standard). Correct test for the design: paired/mixed-effects for repeated measures or multiple
   lesions per patient; multiple-comparison correction (Bonferroni/FDR) across many metrics/regions/
   genes. State the sample-size / power basis. See `references/statistics-handbook.md`.
6. **Subgroup & failure analysis** — performance by site, scanner, sex, age, stage; named failure
   modes with examples.

## Common pitfalls

- "External validation" that is just another split of the same dataset → not external.
- Reporting only discrimination (AUC) for a risk model, never calibration.
- Bare point estimates / a lone p-value with no CI or effect size.
- Per-sample tests on non-independent data (slices/windows from the same patient).
- Tuning the threshold or selecting the best seed on the test set.

## Output

A cohort + experiment design table, the metric/statistics plan, and `[待补充]` for any missing
external cohort, CI, or correction. Once methods/results prose exists, lint it for the classic traps
with `python scripts/stats_leakage_lint.py --manuscript paper.txt` (per-sample splits, missing CIs,
uncorrected p, no calibration) — triage, then fix the underlying gap.
