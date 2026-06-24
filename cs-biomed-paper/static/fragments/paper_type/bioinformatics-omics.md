# Paper type: Bioinformatics / omics

Sequencing, expression, variant, proteomics, microbiome, single-cell, or multi-omics analysis and
methods.

## Reporting & community standards

No single AI checklist governs all omics; align to the relevant community standard and follow
**FAIR** strictly. Examples: **MIAME/MINSEQE**-style minimum information, journal data-deposition
mandates (GEO/SRA/ENA/PRIDE/MetaboLights), and, for any clinical-prediction use of omics, **TRIPOD+AI**.
If it's a systematic synthesis, **PRISMA**. State which standard you followed and why.

## Cross-disciplinary hard rules

- **Multiple-comparison correction is non-negotiable** — thousands of genes/features → FDR
  (Benjamini–Hochberg) or family-wise control; report q-values. Uncorrected p-values are an instant
  reviewer flag.
- **Batch effects** — report and correct (e.g. ComBat/limma); show before/after (PCA). Confounding of
  batch with the biological variable of interest is a fatal design flaw.
- **Independent validation cohort** and/or experimental validation (qPCR / functional assay) for key
  findings.
- **Normalization & pipeline versions** — exact tool versions, reference genome/build, parameters;
  reproducible.
- **Effect size + biological plausibility** — statistical significance alone is not a finding; report
  fold-change/effect size and biological interpretation.
- **Data availability** — raw data in the mandated public repository with accession (often required
  before review).

## Common pitfalls

No FDR correction; batch confounded with condition; significance without effect size or validation;
overfitting a classifier on high-dimensional data with tiny n (leakage via feature selection on all
data); missing accession numbers.

## Typical metrics

Adjusted p/q-values, log fold-change, AUC for classifiers (group-aware CV), enrichment statistics,
variance explained.
