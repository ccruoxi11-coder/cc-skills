# Example — "帮我写这篇差异表达/组学分析的结果和方法"

A bioinformatics/omics request. The cross-disciplinary traps here are multiple-comparison correction
and batch effects — the two things omics reviewers check first.

## Detected axes

`stage: 03-method + 06-section-writing / paper_type: bioinformatics-omics / section: method + results /
venue: general-sci (confirm) / language: zh-to-en`

→ load `stage/03-method.md`, `stage/06-section-writing.md`, `section/method.md`, `section/results.md`,
`paper_type/bioinformatics-omics.md`, `language/zh-to-en.md`. Open `references/statistics-handbook.md`
on demand for FDR / effect-size guidance.

## One-sentence argument (Stage 0 gate)

> In [待补充：生物学问题，如某条件下的转录组改变], we show [待补充：差异表达/通路发现] using
> [待补充：平台 + 分析流程], validated on [待补充：独立队列 / qPCR 或功能实验], bounded by
> [待补充：样本量/混杂未控制范围].

External/independent validation status: **[待补充]** — a finding from one cohort without an
independent or experimental validation is a known omics weakness; flag it now.

## Mandatory standards & hard rules (`paper_type/bioinformatics-omics.md`)

No single AI checklist governs omics — align to the relevant community standard + **FAIR**, and:

- **Multiple-comparison correction is non-negotiable** — thousands of genes → FDR (Benjamini–Hochberg);
  report **q-values**, never bare p. `[待补充：校正方法与 q 阈值]`.
- **Batch effects** — report and correct (ComBat/limma), show before/after PCA; batch must not be
  confounded with the biological variable. `[待补充：批次设计与校正]`.
- **Effect size + biological plausibility** — log fold-change + interpretation, not significance alone.
- **Data deposition** — raw data in the mandated repository (GEO/SRA/ENA/PRIDE) with accession
  `[待补充：accession 号]` (often required before review).
- **Pipeline versions** — exact tool versions, reference genome/build, parameters (reproducible).

## Deliverable shape

- **Method**: cohort/sample design → platform & preprocessing → **batch handling** → differential
  analysis + **FDR correction** → independent/experimental validation plan → tool versions & data
  deposition. (Forbidden vague phrases per `section/method.md`.)
- **Results**: number of significant features at the stated q-threshold, effect sizes, batch-corrected
  PCA, validation result — all with `[待补充]` until provided. No interpretation (that's Discussion).

A `heatmap` figure fits expression matrices: `python scripts/figure_template.py --kind heatmap
--csv expr.csv --out fig.pdf` (viridis, not jet).

## Claim–evidence map

`Claim: feature X differs by condition | Evidence: [待补充：q-value, logFC, 验证] | Status: needs evidence`

## Assumptions or missing inputs

- `[待补充：样本量与分组]`、`[待补充：批次结构]`、`[待补充：校正后显著基因数]`、`[待补充：accession]`、
  `[待补充：独立/实验验证]`.

## Reporting-standard hooks

FDR correction, batch-effect control, and public data deposition are the omics items reviewers most
often find missing — closing them here pre-empts the stage-09 audit.

## Next minimal action

Confirm the batch/correction design and whether an independent or experimental validation exists; then
I draft the statistical-analysis paragraph of Methods.
