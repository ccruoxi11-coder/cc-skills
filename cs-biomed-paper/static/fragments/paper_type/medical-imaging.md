# Paper type: Medical-imaging analysis

Segmentation, detection, classification, registration, reconstruction, or radiomics on medical images.

## Mandatory reporting standard

**CLAIM** — Checklist for Artificial Intelligence in Medical Imaging (Mongan et al., *Radiol Artif
Intell* 2020; CLAIM 2024 update). Source: EQUATOR / the CLAIM paper. Open
`references/reporting-standards/claim.md` for the item list and check at stage 09. If it's a
diagnostic-accuracy claim, also align to **STARD**; for risk of bias use **QUADAS-2**.

## Cross-disciplinary hard rules

- **Patient-level, multi-center external validation.** A held-out split of one dataset is not
  external. Report scanner/vendor/protocol differences across cohorts.
- **No slice/patch leakage.** All slices/patches/augmented copies of one patient stay on one side of
  the split. Split by patient.
- **Ground truth defined** — who annotated, how many readers, inter-rater agreement, the reference
  standard (pathology / follow-up / consensus).
- **Image handling stated** — resolution, spacing, windowing, normalization, registration; de-identify
  panels (no burned-in PHI).
- **Clinically meaningful metrics** — beyond Dice/IoU/AUC: sensitivity/specificity at a chosen
  operating point, FROC for detection, surface distance (HD95/ASSD) for segmentation; clinical impact
  where possible.

## Common pitfalls

Single-center claim of generalization; Dice without boundary metrics; threshold tuned on test; no
reader study where one is expected; class imbalance ignored; preprocessing fit on all data.

## Typical metrics

Dice / IoU, HD95 / ASSD (segmentation); AUC, sensitivity/specificity, FROC (detection/classification);
all with 95% CIs.
