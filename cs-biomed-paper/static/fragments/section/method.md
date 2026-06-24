# Section: Method (Materials & Methods)

## Default structure

`study design & data (cohorts, inclusion/exclusion, ethics) → task formulation & notation →
preprocessing → model/approach overview → per-module detail → training & data-split protocol →
statistical analysis plan → implementation/reproducibility`.

## Rules

- In biomedical work the **data and study design come first** — describe cohorts, eligibility, the
  reference/ground-truth standard, and ethics approval before the model.
- Per module use **motivation → mechanism → role** (re-implementable detail).
- Make the **leakage-safe data flow explicit**: subject/site-level splits; preprocessing/feature
  selection/tuning fit on training data only.
- Include the **statistical analysis plan** (tests, CI method, correction) — reviewers expect it here.
- Name what will be released (code/weights/data) and the seeds/environment.

## Forbidden vague phrases

`standard preprocessing`, `routine methods`, `the model was validated`, `data were analyzed
statistically`, `samples were randomly assigned` (without saying how) → replace with the actual,
reproducible specifics.

## Pitfalls

Architecture described but data handling/ethics omitted; preprocessing leakage; no analysis plan;
unstated ground-truth/labeling procedure. Mark gaps `[待补充]`.
