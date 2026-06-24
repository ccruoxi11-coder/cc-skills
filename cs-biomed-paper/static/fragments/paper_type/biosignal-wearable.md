# Paper type: Biosignal / wearable

ECG, EEG, EMG, PPG, accelerometer/IMU, and other physiological time-series from devices or wearables.

## Reporting & community standards

For a diagnostic/screening claim use **STARD**; for a prediction model **TRIPOD+AI**; for a prospective
device trial **CONSORT-AI**. Always state the **device(s), sampling rate, and acquisition protocol**.
Open the matching `references/reporting-standards/*.md`.

## Cross-disciplinary hard rules

- **Subject-wise splits (the cardinal rule).** Windows/segments from one subject must not cross
  train/test. Per-window random splits are the most common leakage error in this field and inflate
  results dramatically.
- **Cross-device / cross-population validation** — different device, sensor placement, sampling rate,
  or population. Report sensor and demographic shift.
- **Signal processing stated** — filtering, resampling, windowing, artifact rejection, segmentation;
  fit any learned normalization on training subjects only.
- **Label provenance & timing** — how labels were obtained and synchronized to the signal; the
  reference standard.
- **Realistic operating conditions** — motion artifact, missing data, day-to-day variability; report
  performance under noise, not only clean segments.
- **Class imbalance & event-level metrics** — for rare events report sensitivity/specificity, PPV at
  realistic prevalence, false-alarm rate per hour.

## Common pitfalls

Per-window (not per-subject) splitting; single-device claims; testing only on clean data; ignoring
label-signal synchronization; reporting accuracy on an imbalanced dataset.

## Typical metrics

Sensitivity/specificity, AUC/AUPRC, F1, Cohen's κ, false-alarm rate/hour, MAE for regression — all
subject-wise with CIs.
