# Reviewer rebuttal patterns

How to turn a decision letter into a response that makes acceptance easy. Pair with
`scripts/rebuttal_build.py`, which parses comments into a numbered skeleton.

## Structure of the response document

1. **Opening** — thank the editor and reviewers; one short paragraph summarizing the main changes
   (new external validation, added calibration, new ablation, clarified leakage handling).
2. **Per reviewer, per comment** — numbered (R1.1, R1.2 …), each as a self-contained block:
   - **Comment** (verbatim or faithfully restated — never straw-manned).
   - **Response** — agreement/clarification/justification.
   - **Change made** + **location** (section/figure/table/line, or "new Supplementary Table S3").
   - **Quoted new text** (in a coloured/quoted block) so the editor sees it without opening the file.
3. **Editor summary points** — addressed explicitly and first.
4. Keep a **change-log** mapping every reply to an edit in the manuscript.

## Classifying each comment

| Type | When | Move |
|---|---|---|
| **Do & show** | Reasonable, doable | Make the change; quote it. Most comments. |
| **Clarify** | Reviewer misread / it's already there | Point to where; consider making it more prominent (often the text *was* unclear). |
| **Justify (push back)** | You disagree | Disagree only with **evidence + courtesy**; add an analysis if you can. |
| **Cannot do** | Out of scope / infeasible | Explain the constraint, offer the best alternative, acknowledge as a limitation. |

## Tone rules

- Thank, agree where possible, never defensive or dismissive.
- Disagree with data, not assertion; concede genuine limitations openly — it builds trust.
- Address **every** point; silence reads as evasion.
- Match the register of the venue; keep it concise.

## Common biomedical-AI objections and strong responses

| Objection | Strong response |
|---|---|
| "No external validation" | Add an external/temporal cohort; if impossible, add a held-out site analysis and explicitly bound the generalization claim. |
| "Possible data leakage" | Prove subject/site-level splits and training-only preprocessing; add a paragraph + diagram; re-run if any leakage existed. |
| "Weak/old baselines" | Add current SOTA under identical splits/budget; report tuning. |
| "Stats insufficient" | Add CIs (bootstrap), effect sizes, the correct paired test, multiple-comparison correction; add calibration. |
| "Not clinically meaningful" | Add decision-curve/net-benefit or a clinical-impact analysis; temper claims. |
| "Small sample" | Add power/sensitivity analysis; widen CIs honestly; bound claims; add data if feasible. |
| "Reproducibility" | Release code + seeds + environment + exact splits; add a reproducibility statement. |

## Pitfalls

Answering only easy comments; claiming a change not actually made (editors verify); arguing without new
evidence; introducing a new inconsistency (a number changed in the body but not the abstract). After
revising, re-run a self-consistency check (stage 09) across abstract/text/tables.
