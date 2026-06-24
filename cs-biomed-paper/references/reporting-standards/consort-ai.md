# CONSORT-AI — randomized trials of AI interventions (and SPIRIT-AI for protocols)

**Source:** Liu X, Cruz Rivera S, Moher D, et al. *Reporting guidelines for clinical trial reports for
interventions involving artificial intelligence: the CONSORT-AI extension.* Nat Med / BMJ / Lancet
Digit Health 2020. Protocol counterpart: **SPIRIT-AI** (Cruz Rivera et al., 2020). These extend
CONSORT 2010 / SPIRIT 2013 — apply the **base checklist plus the AI-specific items**.

> Use only for prospective/interventional trials evaluating an AI system in clinical use. For a
> retrospective model, use TRIPOD+AI / STARD instead. Verify against the official extensions.

## AI-specific items added on top of CONSORT 2010

- **Intervention (AI) description** — state the AI intervention is used; version; how it was integrated
  into the care pathway.
- **Intended use** — intended setting, users, and the clinical pathway the AI fits into.
- **Input data** — required input data, acquisition/handling, and inclusion/exclusion at the data
  level (e.g. minimum image quality).
- **Output** — what the AI outputs and how outputs inform decisions / actions.
- **Human–AI interaction** — the level of human oversight; how clinicians use/override the output.
- **Error analysis** — how poor-quality or unavailable input is handled; analysis of errors and
  failure cases.
- **Algorithm version & changes** — version used; whether/how it changed during the trial.
- **Access** — how the AI system / code can be accessed and any restrictions.

## Base CONSORT spine (still required)

Trial design & registration; participants & eligibility; randomization & allocation concealment;
blinding; primary/secondary outcomes; sample size; statistical methods; participant flow (CONSORT flow
diagram); results with effect size & CI; harms; limitations; funding.

## Cross-disciplinary red flags

- Treating a retrospective evaluation as a "trial".
- AI version drift during the study unreported; human-AI interaction unspecified.
- No handling of degraded/missing input; error/failure analysis absent.
- Trial not prospectively registered.

Fill `[待补充]` for any unmet base or AI item.
