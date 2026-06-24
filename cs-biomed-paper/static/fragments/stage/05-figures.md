# Stage 05 — Submission-grade figures

**Goal:** figures that pass production and carry the argument at a glance.

## Steps

1. **One message per figure.** State the single takeaway before choosing the chart. The chart serves
   the message (forest/CI plot for effects, ROC + calibration for a classifier, Bland–Altman for
   agreement, Kaplan–Meier for survival, box/violin + points for distributions, heatmap for omics).
2. **Generate with the template** `scripts/figure_template.py` → vector `.pdf`/`.svg`. Match the
   target's spec for column width, font, and minimum font size; see `references/figure-standards.md`.
3. **Show uncertainty** — error bars / CI bands / individual points; never a bare bar of means.
4. **Accessibility** — colourblind-safe palette, redundant encoding (shape/line-style, not colour
   alone), readable at print size.
5. **Self-contained caption** — what, n, statistic shown, test, and scale/units. A reader should
   understand the figure without the body text.
6. **Medical-image panels** — include scale bars, windowing, and de-identify (no patient identifiers,
   no burned-in PHI). Overlays (segmentation/heatmap) need a legend and the underlying image.

## Common pitfalls

- Rasterized line art / text below the minimum font size → production rejection.
- Dual y-axes or truncated axes that exaggerate effects.
- Rainbow/jet colormaps for continuous data → use perceptually uniform (viridis/cividis).
- Patient identifiers or burned-in metadata left in an image panel.

## Output

The figure file path(s), the script invocation used, and the caption text.
