# Paper type: Systematic review / meta-analysis

A structured synthesis of prior studies (e.g. of AI methods for a clinical task), with or without
quantitative pooling.

## Mandatory reporting standard

**PRISMA 2020** (Page et al., *BMJ* 2020) — open `references/reporting-standards/prisma.md`. Register
the protocol (PROSPERO) before screening. For risk of bias in included diagnostic-AI studies use
**QUADAS-2** / **QUADAS-AI**; for prediction models, **PROBAST(+AI)**.

## Cross-disciplinary hard rules

- **Pre-registered protocol** — research question (PICO/PIRT), eligibility, and analysis plan fixed
  before searching.
- **Reproducible search** — full search strings per database, dates, and the **PRISMA flow diagram**
  (identified → screened → eligible → included, with exclusion counts/reasons).
- **Dual independent screening & extraction** — with agreement (κ) and a conflict-resolution rule.
- **Risk-of-bias assessment** of every included study (QUADAS-2 / PROBAST) — report it, don't skip it.
- **Heterogeneity & pooling** — if meta-analyzing, report I², the model (random vs fixed effects),
  forest plot, and assess publication bias (funnel/Egger). If pooling is inappropriate, do a
  structured narrative synthesis and say why.
- **AI-specific extraction** — model type, data modality, validation type (internal/external),
  reporting-standard adherence of included studies.

## Common pitfalls

No registered protocol; single-reviewer screening; missing PRISMA flow diagram; no risk-of-bias
assessment; pooling heterogeneous studies; ignoring publication bias.

## Typical outputs

PRISMA flow diagram, study-characteristics table, risk-of-bias summary, forest plot (if pooled),
heterogeneity and publication-bias statistics.
