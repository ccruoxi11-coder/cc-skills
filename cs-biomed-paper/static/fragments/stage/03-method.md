# Stage 03 — Method design & description

**Goal:** a method a peer could re-implement, with a data flow that cannot leak.

## Steps

1. **Task formulation** — inputs, outputs, scope, and the clinical/biological decision it serves.
   Define notation once.
2. **Overview then modules.** One pipeline figure anchors the section. For each module write the
   three elements: **motivation** (what problem, why the obvious alternative fails), **mechanism**
   (what it does, to re-implementable detail), **role** (its contribution → an ablation hook).
3. **Design the leakage-safe data flow now**, before experiments: where the train/val/test boundary
   sits, that splits are **by subject/site** (not slice/window/augmented copy), and that any
   normalization, feature selection, or hyper-parameter tuning is fit on training data only. State it
   in the method so reviewers can see it. (Details: `references/statistics-handbook.md`.)
4. **Reproducibility scope** — what code, weights, and data will be released (→ stage 08), and the
   fixed seeds / environment.

## Common pitfalls

- Black-box module (missing one of motivation/mechanism/role) → reads as unjustified.
- Preprocessing fit on the whole dataset (normalization, feature selection, class balancing before
  the split) → silent leakage; the classic cross-disciplinary error.
- Vague boilerplate: `using standard preprocessing`, `the model was validated`, `routine methods` →
  replace with the actual reproducible detail.
- Architecture described, data handling omitted — in biomedical work the data flow *is* the method.

## Output

Task formulation, pipeline overview, per-module 3-element descriptions, the data-flow/leakage
statement, and the reproducibility scope (or `[待补充]`).
