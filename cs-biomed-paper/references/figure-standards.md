# Submission-grade figure standards

Make figures that survive production and carry the argument. Always confirm the **target's own author
guidelines** for exact specs — values below are common defaults, not a substitute for the journal's
rules (principle: primary source first). `scripts/figure_template.py` produces compliant vector output.

## Size & resolution

- **Vector formats** (`.pdf`, `.svg`, `.eps`) for line art / plots — infinitely scalable, no
  pixelation. Raster (`.tif`/`.png`) only for photographic content / image panels, at **≥300 dpi**
  (≥600 dpi for line/combination art if raster is unavoidable).
- Size to the **column grid**: single column ≈ 85–90 mm, double column ≈ 170–180 mm (check the venue).
  Design at final print size — don't draw big and shrink (it shrinks the fonts below legibility).

## Typography

- Sans-serif (Arial/Helvetica). **Minimum ~6–8 pt at final size** (verify the venue's minimum).
- Consistent font and size across all panels; no font smaller than the minimum anywhere.
- Embed fonts in the PDF/EPS so they don't substitute at the publisher.

## Colour & accessibility

- **Colourblind-safe palettes** (Okabe–Ito, viridis/cividis). ~8% of men have colour-vision deficiency.
- **Redundant encoding** — distinguish series by shape/line-style/label, not colour alone.
- **Perceptually uniform** colormaps for continuous data (viridis/cividis/magma). **Never jet/rainbow**
  — it creates false gradients and is not colourblind-safe.
- Ensure adequate contrast; avoid red/green as the only contrast.

## Plot integrity

- Show **uncertainty**: error bars (define: SD/SEM/CI), CI bands, or individual data points over the
  summary. Never a bare bar of means ("dynamite plot").
- Don't truncate the y-axis to exaggerate effects; avoid dual y-axes unless unavoidable (and label
  clearly).
- Prefer dot/box/violin + jittered points over bar charts for small-n distributions.

## Panels & captions

- Label panels **a, b, c** (lower-case, consistent placement). Keep alignment and consistent scales
  across comparable panels.
- **Self-contained caption**: title sentence, what each panel shows, n, the statistic and test, error
  definition, scale/units. The figure should be understandable without the body text.

## Medical-image panels (extra rules)

- **De-identify**: no patient names/IDs, remove burned-in PHI/DICOM overlays, strip identifying
  metadata. Crop out identifiers.
- Include a **scale bar**; state windowing/levels and the modality/sequence.
- Overlays (segmentation/attention/heatmap) need a legend and, where possible, the bare image beside
  the overlaid one.

## Chart-to-message map (pick by the message)

| Message | Chart |
|---|---|
| Classifier discrimination | ROC (with AUC + CI) |
| Probability reliability | Calibration plot |
| Effects across groups/studies | Forest plot with CIs |
| Agreement between methods | Bland–Altman |
| Time-to-event | Kaplan–Meier + risk table |
| Distributions (small n) | Box/violin + points |
| High-dim similarity (omics) | Clustered heatmap |
| Ablation / metric comparison | Grouped bars with error bars, or dot plot |

## Quick pre-submission figure check

Vector? fonts embedded & ≥ min size? colourblind-safe + redundant encoding? uncertainty shown? axes
honest? caption self-contained? images de-identified + scale bar? sized to the column grid?
