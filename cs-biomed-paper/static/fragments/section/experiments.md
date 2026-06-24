# Section: Experiments (setup)

This section describes *what was run* (the protocol); raw findings go in Results.

## Rules

- **Datasets & cohorts** — source, n, demographics, prevalence, split scheme (subject/site-level),
  and which cohort is the **external** validation set.
- **Baselines** — current, strong, fairly tuned, including the clinical reference where relevant.
- **Ablations** — each isolates one claimed contribution (map to a method module).
- **Metrics** — list CS metrics *and* clinical/utility metrics, with the operating-point rule.
- **Statistics & implementation** — test choices, CI method, corrections; seeds, hardware, framework
  versions.

## Pitfalls

- Straw-man baselines; tuning on the test set.
- "External" set that is the same dataset re-split.
- Metrics chosen post hoc to look good.
- Implementation under-specified → not reproducible.

Keep protocol here, numbers in Results. Mark `[待补充]` for any missing cohort or setting.
