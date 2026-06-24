#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""Check a manuscript against a reporting standard (CLAIM / TRIPOD+AI / CONSORT-AI / STARD / PRISMA).

Self-contained: standard library only. This is a TRIAGE aid for stage 09, not an authority. It scans
the manuscript text for keyword/regex signals of each checklist domain and reports, per item:

    [PRESENT]  signal found
    [MISSING]  no signal — fill it or justify N/A
    [CHECK]    weak/ambiguous signal — verify manually

It deliberately reports the DOMAINS of each checklist (the things reviewers most often find missing),
NOT the exact official item numbers. Always reconcile the output against the official checklist PDF
(see references/reporting-standards/<standard>.md). A "PRESENT" only means the words appear — it does
not certify the item is reported correctly.

Usage:
    python reporting_check.py --standard claim     --manuscript paper.txt
    python reporting_check.py --standard tripod-ai --manuscript paper.md  --report check.md
    python reporting_check.py --list                       # list standards & domains

Input: a plain-text or markdown manuscript (export your .docx/.tex to .txt first).
Output: a markdown report to stdout (and to --report path if given) with a coverage summary.
"""

import argparse
import re
import sys

# This tool prints Chinese [待补充] placeholders; force UTF-8 so Windows consoles
# (cp936/cp1252) don't mojibake or raise UnicodeEncodeError. File output is already UTF-8.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# Each standard maps an item label -> list of regex signals (any match = PRESENT).
# Signals are intentionally broad; the goal is to flag likely-missing items for human review.
STANDARDS = {
    "claim": {
        "_name": "CLAIM (Checklist for AI in Medical Imaging) — Mongan et al., Radiol AI 2020/2024",
        "AI/ML use stated (title/abstract)": [r"\b(deep learning|machine learning|neural network|\bAI\b|convolutional)\b"],
        "Study objective / hypothesis": [r"\b(aim|objective|goal|hypothes|we propose|we develop)\b"],
        "Prospective vs retrospective": [r"\b(retrospective|prospective)\b"],
        "Data source & eligibility": [r"\b(data(set)? (were|was) (collected|obtained)|inclusion crit|exclusion crit|eligib|cohort|recruit)\b"],
        "De-identification / privacy": [r"\b(de-?identif|anonymiz|HIPAA|GDPR|IRB|ethic|consent)\b"],
        "Ground truth / reference standard": [r"\b(ground truth|reference standard|annotat|label(ed|ing)|radiologist|expert reader|patholog)\b"],
        "Annotator number & agreement": [r"\b(inter-?(rater|observer)|two (radiologists|experts|readers|annotators)|consensus|kappa|κ)\b"],
        "Data partition (patient-level split)": [r"\b(train(ing)?\s*/?\s*(validation|test)|split (by|at) (patient|subject)|patient-level|group(ed)? (k-?fold|split))\b"],
        "Model description (reproducible)": [r"\b(architecture|backbone|U-?Net|ResNet|transformer|layers|parameters)\b"],
        "Training details / hyper-parameters": [r"\b(learning rate|epochs|batch size|optimizer|Adam|hyper-?parameter|augmentation)\b"],
        "Software/framework & version": [r"\b(PyTorch|TensorFlow|Keras|scikit-?learn|version \d|v\d+\.\d)\b"],
        "Operating point selection": [r"\b(threshold|operating point|cut-?off|Youden)\b"],
        "Metrics with uncertainty (CI)": [r"\b(confidence interval|95% ci|\bCI\b|bootstrap)\b"],
        "External / independent validation": [r"\b(external (validation|cohort|test|set)|independent (cohort|dataset)|multi-?(center|centre|site)|temporal validation)\b"],
        "Case flow / flow diagram": [r"\b(flow (diagram|chart)|consort|cases (were )?excluded|patient flow)\b"],
        "Failure / subgroup analysis": [r"\b(failure (case|mode|analysis)|subgroup|error analysis|misclassif)\b"],
        "Limitations": [r"\b(limitation|our study has|caveat)"],
        "Data & code availability": [r"\b(code (is )?available|github|zenodo|data (are|is) available|availability statement|accession)\b"],
        "Funding / registration": [r"\b(funding|grant|supported by|registered|registration number|NCT\d)\b"],
    },
    "tripod-ai": {
        "_name": "TRIPOD+AI (prediction models) — Collins et al., BMJ 2024",
        "Identified as prediction model (title/abstract)": [r"\b(predict(ion|ive)? model|prognostic|diagnostic model|risk (score|model))\b"],
        "Objective & clinical role": [r"\b(aim|objective|intended use|clinical (role|decision))\b"],
        "Source of data & design": [r"\b(retrospective|prospective|cohort|registry|EHR|electronic health record)\b"],
        "Participants & setting": [r"\b(participant|patient|inclusion|exclusion|setting|recruit)\b"],
        "Outcome definition & timing": [r"\b(outcome (was )?defined|primary outcome|endpoint|follow-?up)\b"],
        "Predictors available at prediction time": [r"\b(predictor|feature|variable|available at (the )?(time|moment) of prediction|baseline)\b"],
        "Sample size justification": [r"\b(sample size|power (analysis|calculation)|events per variable|EPV)\b"],
        "Missing data handling": [r"\b(missing data|imputation|complete[- ]case|multiple imputation)\b"],
        "Model & predictor selection": [r"\b(logistic regression|random forest|gradient boost|XGBoost|feature selection|regulariz|LASSO|neural)\b"],
        "Internal validation (CV/bootstrap)": [r"\b(cross-?validation|bootstrap|internal validation|nested cv)\b"],
        "Discrimination (AUC)": [r"\b(auc|c-?statistic|c-?index|area under)\b"],
        "Calibration": [r"\b(calibration (plot|slope|intercept)|observed[- ]?(to[- ])?expected|brier)\b"],
        "External validation (temporal/geographic)": [r"\b(external validation|temporal validation|geographic|another (site|hospital|center))\b"],
        "Subgroup / fairness analysis": [r"\b(subgroup|fairness|bias across|sex|age group|race|ethnic)\b"],
        "Full model specification / access": [r"\b(coefficients|equation|nomogram|model (is )?available|full specification|web calculator)\b"],
        "Clinical utility": [r"\b(decision curve|net benefit|NRI|reclassification|clinical utility)\b"],
        "Limitations & interpretation": [r"\b(limitation|generaliz|overfit|interpretation)"],
        "Code/data/model availability (open science)": [r"\b(code (is )?available|github|zenodo|data availability|model (is )?available)\b"],
    },
    "consort-ai": {
        "_name": "CONSORT-AI (prospective AI trials) — Nat Med/BMJ/Lancet Digit Health 2020",
        "Prospective trial & registration": [r"\b(randomi[sz]ed|trial|prospective|registered|NCT\d|registration)\b"],
        "AI intervention & version": [r"\b(\bAI\b|algorithm|model) (version|v\d)|version (of the )?(model|algorithm)|software version\b"],
        "Intended use & setting": [r"\b(intended use|intended setting|care pathway|integrated into)\b"],
        "Input data requirements": [r"\b(input data|image quality|minimum (quality|requirement)|data acquisition)\b"],
        "Output & how it informs decisions": [r"\b(output|recommendation|the (model|system) (provides|outputs)|informs (the )?decision)\b"],
        "Human-AI interaction / oversight": [r"\b(human (oversight|in the loop)|clinician (review|override)|human-?ai)\b"],
        "Error / poor-input handling": [r"\b(error analysis|poor[- ]quality|unavailable input|failure|fallback)\b"],
        "Outcomes & sample size": [r"\b(primary outcome|secondary outcome|sample size|power)\b"],
        "Randomization & blinding": [r"\b(randomi[sz]ation|allocation concealment|blind)\b"],
        "Participant flow (CONSORT diagram)": [r"\b(consort (flow )?diagram|participant flow|enrolled|allocated)\b"],
        "Results with effect size & CI": [r"\b(confidence interval|95% ci|effect size|risk (ratio|difference)|odds ratio)\b"],
        "Harms": [r"\b(harm|adverse event|safety)\b"],
        "Access to AI system/code": [r"\b(code (is )?available|access to (the )?(system|model|algorithm)|github)\b"],
    },
    "stard": {
        "_name": "STARD 2015 (diagnostic accuracy) — Bossuyt et al., BMJ 2015",
        "Identified as diagnostic accuracy study": [r"\b(diagnostic accuracy|sensitivity and specificity|screening test|index test)\b"],
        "Objectives / hypotheses": [r"\b(aim|objective|hypothes)\b"],
        "Study design (timing of data collection)": [r"\b(prospective|retrospective|consecutive|cross-?sectional)\b"],
        "Participants & eligibility & setting": [r"\b(eligib|inclusion|exclusion|setting|recruit|sampling)\b"],
        "Index test description": [r"\b(index test|the (model|algorithm|test) (was )?(performed|applied)|test method)\b"],
        "Reference standard & rationale": [r"\b(reference standard|gold standard|ground truth|patholog|follow-?up confirm)\b"],
        "Blinding of readers": [r"\b(blind(ed)? to (the )?(reference|index|results)|masked|without knowledge of)\b"],
        "Methods for estimating accuracy": [r"\b(sensitivity|specificity|ppv|npv|likelihood ratio|roc|auc)\b"],
        "Handling of indeterminate/missing": [r"\b(indeterminate|missing|uninterpretable|excluded from analysis)\b"],
        "Participant flow diagram": [r"\b(flow (diagram|chart)|eligible|excluded|analy[sz]ed)\b"],
        "2x2 / cross-tabulation": [r"\b(2 ?x ?2|cross-?tab|true positive|false positive|contingency)\b"],
        "Estimates with 95% CI": [r"\b(confidence interval|95% ci)\b"],
        "Limitations (bias, applicability)": [r"\b(limitation|spectrum bias|generaliz|applicab)"],
        "Registration / funding / data": [r"\b(registration|registered|funding|data availability)\b"],
    },
    "prisma": {
        "_name": "PRISMA 2020 (systematic reviews) — Page et al., BMJ 2021",
        "Identified as systematic review (title)": [r"\b(systematic review|meta-?analysis|scoping review)\b"],
        "Rationale & objectives (PICO)": [r"\b(rationale|objective|research question|pico|population.*intervention)\b"],
        "Eligibility criteria": [r"\b(eligibility|inclusion crit|exclusion crit)\b"],
        "Information sources (databases & dates)": [r"\b(pubmed|medline|embase|scopus|web of science|ieee|searched.*(from|until|up to)|database)\b"],
        "Full search strategy": [r"\b(search (strategy|string|terms)|mesh|boolean|search query)\b"],
        "Selection process (independent reviewers)": [r"\b(two (reviewers|authors)|independently (screen|review)|dual screen|title and abstract screen)\b"],
        "Data collection / items": [r"\b(data (were )?extract|extraction (form|process)|data items|charting)\b"],
        "Risk-of-bias assessment": [r"\b(risk of bias|quadas|probast|robins|quality assessment)\b"],
        "Synthesis & heterogeneity": [r"\b(meta-?analysis|pooled|random[- ]effects|fixed[- ]effects|heterogeneity|i2|i²|forest plot|narrative synthesis)\b"],
        "Reporting/publication bias": [r"\b(publication bias|funnel plot|egger)\b"],
        "Certainty (GRADE)": [r"\b(grade|certainty of evidence|quality of evidence)\b"],
        "PRISMA flow diagram": [r"\b(prisma (flow )?diagram|records identified|records screened|studies included)\b"],
        "Registration & protocol (PROSPERO)": [r"\b(prospero|registered|protocol|registration number)\b"],
        "Data/code availability": [r"\b(data availability|code (is )?available|supplementary (data|material))\b"],
    },
}


def check(text, standard):
    items = STANDARDS[standard]
    low = text.lower()
    results = []
    for label, signals in items.items():
        if label == "_name":
            continue
        hits = sum(1 for s in signals if re.search(s, low, re.IGNORECASE))
        if hits == 0:
            status = "MISSING"
        elif hits == 1 and len(signals) > 1:
            status = "CHECK"
        else:
            status = "PRESENT"
        results.append((status, label))
    return results, items["_name"]


def render(results, name, standard):
    n = len(results)
    present = sum(1 for s, _ in results if s == "PRESENT")
    check_ = sum(1 for s, _ in results if s == "CHECK")
    missing = sum(1 for s, _ in results if s == "MISSING")
    icon = {"PRESENT": "[PRESENT]", "CHECK": "[CHECK]  ", "MISSING": "[MISSING]"}
    lines = [
        f"# Reporting-standard check — {standard.upper()}",
        f"_{name}_",
        "",
        f"Coverage: **{present}/{n} present**, {check_} to verify, {missing} missing.",
        "",
        "> Triage only. 'PRESENT' = keywords found, NOT that the item is correctly reported.",
        "> Reconcile against the official checklist (references/reporting-standards/"
        f"{standard}.md) and fill every MISSING/CHECK item or mark it N/A with a reason.",
        "",
        "| Status | Checklist domain |",
        "|---|---|",
    ]
    order = {"MISSING": 0, "CHECK": 1, "PRESENT": 2}
    for status, label in sorted(results, key=lambda r: order[r[0]]):
        lines.append(f"| {icon[status]} | {label} |")
    lines += ["", "## Action list", ""]
    for status, label in results:
        if status != "PRESENT":
            lines.append(f"- [ ] **{label}** — {'add to manuscript' if status=='MISSING' else 'verify it is actually reported'} "
                         f"(`[待补充]` if data not yet available).")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Check a manuscript against a reporting standard.")
    ap.add_argument("--standard", choices=list(STANDARDS), help="which checklist")
    ap.add_argument("--manuscript", help="path to a plain-text/markdown manuscript")
    ap.add_argument("--report", help="write the markdown report to this path")
    ap.add_argument("--list", action="store_true", help="list standards and their domains")
    args = ap.parse_args()

    if args.list:
        for key, items in STANDARDS.items():
            print(f"\n## {key}  —  {items['_name']}")
            for label in items:
                if label != "_name":
                    print(f"   - {label}")
        return

    if not args.standard or not args.manuscript:
        ap.error("provide --standard and --manuscript (or --list)")

    try:
        with open(args.manuscript, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.exit(f"[error] cannot read manuscript: {e}")

    results, name = check(text, args.standard)
    report = render(results, name, args.standard)
    print(report)
    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[ok] wrote {args.report}", file=sys.stderr)


if __name__ == "__main__":
    main()
