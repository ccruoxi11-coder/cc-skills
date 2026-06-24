# Reporting standards — which one applies

Biomedical-AI manuscripts are judged against a community reporting checklist. Pick by study type,
align both the *writing* and the stage-09 *self-audit* to it, and verify item-by-item against the
**official** checklist (these summaries are derived guides, not the source of truth — principle:
**primary source first**). Master index: the EQUATOR Network, https://www.equator-network.org.

## Decision table

| If the work is… | Use | File | Primary source |
|---|---|---|---|
| AI on medical images (segmentation/detection/classification/reconstruction) | **CLAIM** | `claim.md` | Mongan et al., *Radiol Artif Intell* 2020; CLAIM 2024 update |
| A patient-level prediction/diagnosis/prognosis model | **TRIPOD+AI** | `tripod-ai.md` | Collins et al., *BMJ* 2024 |
| A *prospective/interventional* clinical trial of an AI system | **CONSORT-AI** (protocol: **SPIRIT-AI**) | `consort-ai.md` | *Nat Med / BMJ / Lancet Digit Health* 2020 |
| A diagnostic-accuracy study vs a reference standard | **STARD 2015** (bias: **QUADAS-2**) | `stard.md` | Bossuyt et al., *BMJ/Radiology* 2015 |
| A systematic review / meta-analysis | **PRISMA 2020** | `prisma.md` | Page et al., *BMJ* 2020 |

## How they relate

- They overlap on a common spine: clear question, transparent data, validation, calibration/accuracy,
  honest limitations, availability.
- A study can need **more than one**: a prospective imaging-AI trial may touch CLAIM (the model),
  STARD (accuracy), and CONSORT-AI (the trial). Apply each where it bites.
- Risk-of-bias tools complement reporting checklists: **QUADAS-2/QUADAS-AI** (diagnostic accuracy),
  **PROBAST/PROBAST-AI** (prediction models) — used mainly inside systematic reviews.
- Emerging/adjacent: **DECIDE-AI** (early-stage clinical evaluation), **STARD-AI** (in development),
  **MI-CLAIM**, **CLEAR** (radiomics). If one of these fits better, say so and cite it.

## Using these files

Each standard file lists the checklist's **domains** and the cross-disciplinary items reviewers most
often find missing. `scripts/reporting_check.py` scans a manuscript for keyword coverage of these
domains and emits a present/missing/N-A report — a triage aid, **not** a substitute for the official
checklist. Always reconcile against the official PDF and fill any `[待补充]`.
