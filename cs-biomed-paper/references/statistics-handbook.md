# Statistics handbook (cross-disciplinary)

Practical statistics for CS×biomedical papers — the rules CS pipelines most often break. Each rule
carries its reason; when in doubt, consult a statistician and cite the method you used. This is a
working reference, not a textbook.

## 1. Data splitting & leakage (the #1 cause of inflated results)

- **Split by the independent unit, never the sample.** The unit is usually the **patient/subject**
  (sometimes the site). Slices, patches, windows, segments, and augmented copies from one patient must
  all stay on the same side of train/val/test. Per-sample random splits leak and inflate metrics.
- **Fit everything on training data only** — normalization, feature selection, imputation, class
  balancing, and hyper-parameter tuning. Fitting any of these on the full dataset before splitting is
  leakage.
- **Temporal validation** for prediction models: train on earlier data, test on later. **Geographic /
  multi-site** validation for generalization. A re-split of the same dataset is *internal*, not
  external.
- **Cross-validation** must be **group-aware** (GroupKFold by patient). Nested CV when tuning, to keep
  the test fold unseen.
- Avoid **look-ahead / immortal-time bias**: predictors must be available at the prediction moment; no
  post-outcome variables.

## 2. Uncertainty & effect size (never report a bare number)

- Report **95% confidence intervals** on every headline metric. For AUC/Dice/sensitivity, **bootstrap
  CIs** (resample the test patients, e.g. 1000×) are standard and account for finite test size.
- Report an **effect size**, not only a p-value: difference in metric, Cohen's d, odds/hazard ratio,
  risk difference. "Statistically significant" ≠ "clinically meaningful".
- Compare models with a paired test on the **same test cases** (e.g. paired bootstrap, DeLong's test
  for two AUCs, McNemar for paired binary outcomes).

## 3. Right test for the design

| Design | Typical approach |
|---|---|
| Two independent groups, continuous | t-test (or Mann–Whitney if non-normal) |
| Paired / same subjects | paired t-test / Wilcoxon signed-rank |
| Repeated measures, multiple lesions per patient, multi-site | **mixed-effects / hierarchical models** (random intercept per patient/site), or GEE |
| Two AUCs on same cases | DeLong's test |
| Paired binary classifier outputs | McNemar's test |
| Survival / time-to-event | Kaplan–Meier + log-rank; Cox model (check proportional hazards) |
| Agreement | Bland–Altman, ICC, Cohen's/Fleiss' κ |

Naïve per-sample tests on non-independent data (clustered within patient) **understate variance** and
manufacture false significance — use mixed models.

## 4. Multiple comparisons

Many metrics / regions / genes / hyper-parameters tested → correct: **Bonferroni** (strict,
family-wise) or **Benjamini–Hochberg FDR** (high-dimensional, e.g. omics — report q-values). State the
number of comparisons and the method.

## 5. Calibration (for risk/probability models)

Discrimination (AUC) ≠ calibration. Report a **calibration plot**, **calibration slope & intercept**
(or observed:expected ratio), and **Brier score**. Consider recalibration if needed. Clinical utility:
**decision-curve / net-benefit analysis**, NRI/IDI.

## 6. Sample size & power

State the basis for n (power analysis for a trial; events-per-variable ≥ ~10–20 for classical
prediction models; learning-curve/saturation argument for deep models). Underpowered subgroup claims
are a common reviewer target.

## 7. Class imbalance & metric choice

For rare positives, accuracy is misleading. Report **AUPRC**, sensitivity/specificity, **PPV/NPV at the
realistic prevalence** (not the resampled one), and false-alarm rate. Don't evaluate on an artificially
balanced test set if deployment is imbalanced.

## 8. Reproducibility of the statistics

Fix and report random seeds; report **mean ± SD over multiple seeds/folds** for ML metrics (a single
run is not evidence); name the software and version used for the analysis. Pre-specify the primary
analysis to avoid p-hacking / metric-shopping.

## Reporting template (drop into Methods)

`[待补充]` Statistical analysis was performed using <software vX>. <Primary metric> is reported with
95% confidence intervals (1000-sample bootstrap over test <patients>). Groups were compared with
<test> ; p-values were corrected for multiple comparisons using <Bonferroni/BH-FDR>. Models were
validated on an independent <external/temporal> cohort. Calibration was assessed by <plot/slope>.
