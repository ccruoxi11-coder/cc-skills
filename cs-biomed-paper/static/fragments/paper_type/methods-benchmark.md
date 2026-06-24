# Paper type: Methods / benchmark

A new method, architecture, loss, or a benchmark/dataset contribution, evaluated on biomedical data.

## Reporting & community standards

Pick the standard by the *application* the method is evaluated on: imaging → **CLAIM**; prediction →
**TRIPOD+AI**; diagnostic accuracy → **STARD**. Even a "pure method" paper using clinical data must
respect that standard's validation and leakage rules. For a benchmark/dataset paper, follow dataset
documentation norms (datasheets/data statements) and FAIR.

## Cross-disciplinary hard rules

- **Fair, current, well-tuned baselines** — same data, splits, and budget; report tuning. A
  straw-man comparison is the top reviewer objection for method papers.
- **Ablations isolate the contribution** — one change at a time, each mapped to a claimed component.
- **Significance of improvements** — report CIs and a significance test across seeds/folds; a 0.3%
  gain within the noise band is not a contribution. Report mean ± SD over multiple seeds.
- **Group-aware evaluation** — even for a "method" paper, splits on biomedical data must be by
  subject/site; no leakage.
- **Cost characteristics** — parameters, FLOPs, latency, memory, training cost; deployment realism
  matters for biomedical use.
- **Generalization** — at least one external/independent dataset; don't claim general superiority from
  one benchmark.

## Common pitfalls

Weak baselines; SOTA claim from a single dataset; improvement within noise; no seed variance; ablations
that change two things at once; ignoring compute cost; method validated only where it wins.

## Typical metrics

Task metric(s) with CIs and across-seed variance, ablation deltas with significance, efficiency
(params/FLOPs/latency), and an external-dataset result.
