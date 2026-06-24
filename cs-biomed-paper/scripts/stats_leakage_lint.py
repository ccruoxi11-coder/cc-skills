#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""Lint a manuscript for the statistical & data-leakage patterns that get CS×biomed papers rejected.

Self-contained: standard library only. A TRIAGE aid for stages 04 / 09 — it flags the high-risk
methodological patterns reviewers hit first, so you can fix the underlying gap before submission. It
is heuristic (keyword/regex), so every finding needs human confirmation; it does NOT certify
correctness, and it never invents numbers.

Two kinds of checks:
  * LINE checks      — a risky phrase on a line (e.g. "per-window split", "tuned on the test set").
  * DOCUMENT checks  — a claim/metric appears but its required safeguard is absent anywhere (e.g. AUC
                       with no CI; a prediction model with no calibration; generalization with no
                       external cohort).

Severity: HIGH = likely desk-reject / fatal; MED = a reviewer will ask; LOW = tighten the wording.

Usage:
    python stats_leakage_lint.py --manuscript paper.txt
    python stats_leakage_lint.py --manuscript paper.md --report lint.md
    python stats_leakage_lint.py --list                  # show every check + rationale
    python stats_leakage_lint.py --manuscript paper.txt --fail-on high   # exit 1 if any HIGH

Input: a plain-text / markdown manuscript (export .docx/.tex to .txt first).
Output: a markdown report (stdout, and --report path if given). Exit code is 1 if a finding at or
above --fail-on (default: none) is present, so it can gate a pre-submission check.
"""

import argparse
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# Line-level checks: any line matching `bad` is flagged.
LINE_CHECKS = [
    dict(id="leak-unit-split", sev="HIGH", cat="Data leakage",
         bad=r"\b(per-?(window|slice|patch|sample|segment|frame|image)|"
             r"(window|slice|patch|sample|segment)-?(level|wise))\b[^.]*\b(split|cross-?validat|train|test|fold)\b",
         why="Splitting windows/slices/patches/samples instead of the patient leaks correlated data "
             "across train/test and inflates metrics.",
         fix="Split by the independent unit (patient/subject/site); keep all units of one subject on "
             "one side (GroupKFold)."),
    dict(id="leak-preprocess-all-data", sev="HIGH", cat="Data leakage",
         bad=r"\b(normaliz|standardiz|feature selection|imputation|over-?sampl|smote|class[- ]balanc|"
             r"pca|scaling)\b[^.]*\b(whole|entire|full|all)\b[^.]*\b(data|dataset|cohort)\b",
         why="Fitting preprocessing/feature selection on the whole dataset before splitting is "
             "silent leakage.",
         fix="Fit every transform (normalization, selection, imputation, balancing) on the training "
             "fold only, then apply to val/test."),
    dict(id="threshold-on-test", sev="HIGH", cat="Test-set tuning",
         bad=r"\b(threshold|operating point|cut-?off|hyper-?parameter|best (epoch|model|seed))\b[^.]*"
             r"\b(test (set|data|cohort|fold))\b",
         why="Selecting a threshold / hyper-parameter / best seed on the test set is optimistic bias.",
         fix="Choose the operating point and all hyper-parameters on a validation split by a stated "
             "rule, then report once on the untouched test set."),
    dict(id="overclaim-no-comparator", sev="MED", cat="Over-claiming",
         bad=r"\b(significantly|dramatically|greatly|substantially)\s+"
             r"(better|improv\w+|higher|superior|outperform\w*)\b(?![^.]*\b(than|compared|versus|vs\.?|relative to)\b)",
         why="A comparative/significance claim with no stated comparator or test.",
         fix="Name the comparator and the test (e.g. 'higher than [baseline], paired bootstrap "
             "p=[待补充]'), or soften the verb."),
    dict(id="overclaim-absolutes", sev="LOW", cat="Over-claiming",
         bad=r"\b(first (to|ever)|state-of-the-art|\bSOTA\b|revolutionary|unprecedented|"
             r"clinically ready|ready for clinical (use|deployment))\b",
         why="Unbounded novelty / readiness claims draw reviewer fire in biomedical venues.",
         fix="Bound the claim to the evidence (population, validation scope); drop 'clinically ready' "
             "without prospective evidence."),
    dict(id="accuracy-on-imbalance", sev="MED", cat="Metric choice",
         bad=r"\b(accuracy)\b[^.]*\b(imbalanc|rare|prevalence|skewed)\b|"
             r"\b(imbalanc|rare event)\b[^.]*\baccuracy\b",
         why="Accuracy on imbalanced data is misleading (a trivial majority classifier scores high).",
         fix="Report sensitivity/specificity, PPV/NPV at realistic prevalence, AUPRC, or "
             "false-alarm rate."),
]

# Document-level checks: if `trigger` appears but `good` appears nowhere → one finding.
DOC_CHECKS = [
    dict(id="no-ci", sev="HIGH", cat="Uncertainty",
         trigger=r"\b(auc|au-?roc|dice|iou|sensitivity|specificity|accuracy|f1|c-?statistic|"
                 r"c-?index|hd95|assd)\b",
         good=r"\b(95% ?ci|confidence interval|bootstrap|credible interval|±|\bsd\b|"
              r"standard deviation|\biqr\b|interquartile)\b",
         why="Headline metrics are reported with no uncertainty (CI / bootstrap / SD) anywhere.",
         fix="Add 95% CIs — bootstrap over test patients — to every headline metric."),
    dict(id="bare-p", sev="MED", cat="Effect size",
         trigger=r"\bp\s*[<=>]\s*0?\.\d+|\bp-?values?\b",
         good=r"\b(effect size|cohen'?s? d|odds ratio|hazard ratio|risk difference|"
              r"mean difference|95% ?ci)\b",
         why="p-values appear without an effect size or CI; statistical ≠ clinical significance.",
         fix="Report an effect size + 95% CI beside each p-value."),
    dict(id="no-multiple-correction", sev="MED", cat="Multiple comparisons",
         trigger=r"\b(genes?|transcripts?|features?|regions?|voxels?|biomarkers?|variants?|metrics?)\b"
                 r"[^.]*\bp\s*[<=]\s*0?\.\d+",
         good=r"\b(fdr|benjamini|bonferroni|holm|family-?wise|q-?values?|"
              r"corrected for multiple|multiple[- ]comparison)\b",
         why="Many simultaneous tests with no multiple-comparison correction.",
         fix="Apply FDR (Benjamini–Hochberg) or family-wise control; report q-values."),
    dict(id="no-calibration", sev="MED", cat="Clinical validity",
         trigger=r"\b(prediction model|risk (model|score|prediction)|prognostic model|"
                 r"diagnostic model|tripod)\b",
         good=r"\b(calibrat\w+|brier|observed[- :]*(to[- ])?expected|\bo:e\b|reliability (diagram|plot))\b",
         why="A risk/prediction model is reported on discrimination only, with no calibration.",
         fix="Add a calibration plot + slope/intercept (or Brier / O:E ratio)."),
    dict(id="no-external-val", sev="HIGH", cat="External validation",
         trigger=r"\b(generaliz\w+|real-?world|deploy\w*|clinical(ly)? (utilit|useful|applicable|ready)|"
                 r"broadly applicable)\b",
         good=r"\b(external (validation|cohort|test|set|dataset)|independent (cohort|dataset|test|"
              r"validation)|multi-?(center|centre|site)|temporal validation|another (site|hospital|"
              r"center|scanner|device|institution))\b",
         why="Generalization / clinical-utility claims without an external or independent cohort.",
         fix="Validate on data from a different site/scanner/device/time window — or cap the claim to "
             "internal performance and say so."),
    dict(id="no-ethics", sev="HIGH", cat="Ethics / privacy",
         trigger=r"\b(patient|participant|subject|clinical|human (data|subjects?)|cohort|EHR|"
                 r"medical record)\b",
         good=r"\b(irb|institutional review board|ethics (committee|approval|board)|"
              r"declaration of helsinki|informed consent|consent waiver|de-?identif\w+|"
              r"anonymi[sz]ed|hipaa|gdpr)\b",
         why="Human/patient data with no ethics approval, consent, or de-identification statement.",
         fix="State IRB/ethics approval ID, consent (or waiver), and de-identification — use "
             "[待补充：伦理审批号] for unverified values; never invent one."),
]

SEV_ORDER = {"HIGH": 0, "MED": 1, "LOW": 2}
SEV_RANK = {"high": 0, "med": 1, "low": 2, "none": 99}


def lint(text):
    findings = []
    low = text.lower()
    lines = text.splitlines()
    for chk in LINE_CHECKS:
        rx = re.compile(chk["bad"], re.IGNORECASE)
        for i, ln in enumerate(lines, 1):
            if rx.search(ln):
                findings.append((chk["sev"], chk["cat"], chk["id"],
                                 f"line {i}: …{ln.strip()[:120]}…", chk["why"], chk["fix"]))
    for chk in DOC_CHECKS:
        if re.search(chk["trigger"], low, re.IGNORECASE) and not re.search(chk["good"], low, re.IGNORECASE):
            findings.append((chk["sev"], chk["cat"], chk["id"],
                             "document-level: trigger present, safeguard absent",
                             chk["why"], chk["fix"]))
    findings.sort(key=lambda f: SEV_ORDER[f[0]])
    return findings


def render(findings):
    n_high = sum(1 for f in findings if f[0] == "HIGH")
    n_med = sum(1 for f in findings if f[0] == "MED")
    n_low = sum(1 for f in findings if f[0] == "LOW")
    out = [
        "# Stats & leakage lint",
        "",
        f"Findings: **{n_high} HIGH**, {n_med} MED, {n_low} LOW.",
        "",
        "> Triage only — heuristic keyword/regex matching. Each finding needs human confirmation; "
        "a clean report does NOT certify correct statistics. Fix the underlying gap, then re-run.",
        "",
    ]
    if not findings:
        out.append("No high-risk patterns detected. Still verify CIs, group-aware splits, "
                   "calibration, correction, and ethics against the manuscript by hand.\n")
        return "\n".join(out)
    out += ["| Sev | Category | Where | Issue → Fix |", "|---|---|---|---|"]
    for sev, cat, cid, where, why, fix in findings:
        out.append(f"| {sev} | {cat} | {where} | {why} **Fix:** {fix} |")
    out += ["", "## Action list (highest severity first)", ""]
    for sev, cat, cid, where, why, fix in findings:
        out.append(f"- [ ] **[{sev}] {cat}** ({cid}) — {fix}")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Lint a manuscript for stats & data-leakage risks.")
    ap.add_argument("--manuscript", help="plain-text / markdown manuscript")
    ap.add_argument("--report", help="write the markdown report here")
    ap.add_argument("--list", action="store_true", help="list all checks and rationale")
    ap.add_argument("--fail-on", choices=["high", "med", "low", "none"], default="none",
                    help="exit 1 if a finding at/above this severity exists (default: none)")
    args = ap.parse_args()

    if args.list:
        print("# Stats & leakage lint — checks\n")
        for chk in LINE_CHECKS + DOC_CHECKS:
            print(f"[{chk['sev']}] {chk['cat']} ({chk['id']})\n   why: {chk['why']}\n   fix: {chk['fix']}\n")
        return

    if not args.manuscript:
        ap.error("provide --manuscript (or --list)")
    try:
        with open(args.manuscript, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.exit(f"[error] cannot read manuscript: {e}")

    findings = lint(text)
    report = render(findings)
    print(report)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[ok] wrote {args.report}", file=sys.stderr)

    if args.fail_on != "none":
        worst = min((SEV_RANK[f[0].lower()] for f in findings), default=99)
        if worst <= SEV_RANK[args.fail_on]:
            sys.exit(1)


if __name__ == "__main__":
    main()
