#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""Profile the house style of target-journal papers, then audit your draft against it.

Self-contained: standard library only. The "output first" tool behind the journal-fit workflow
(references/journal-fit.md): you supply a few published papers FROM THE TARGET JOURNAL as plain text,
the tool measures their quantitative style (sentence length, hedging vs promotional language, first
person, passive voice, uncertainty markers, citation density), aggregates a profile, then flags where
YOUR manuscript deviates from that journal's norm.

It measures only the text you provide — it does NOT invent norms, rewrite your paper, or fetch papers
from the web (paste/export the exemplars yourself; respect each publisher's terms). It is descriptive
guidance for stage 07 (polish to the journal's register) and stage 09 (pre-submission), not a rule.

Usage:
    # Profile 3+ exemplars and audit your draft against them
    python journal_style_profile.py --exemplars refs/ --manuscript mydraft.txt --report fit.md

    # Exemplars can be a mix of files and directories (*.txt / *.md are read)
    python journal_style_profile.py --exemplars a.txt b.txt c.txt --manuscript draft.md

    # Just profile the exemplars (no draft yet)
    python journal_style_profile.py --exemplars refs/

Input: plain-text / markdown (export .docx/.pdf to .txt first). 3+ exemplars recommended; with <3 the
"range" is unreliable and the report says so.
Output: a markdown profile + deviation report (stdout, and --report path if given).
"""

import argparse
import re
import statistics
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[\"'(A-Z])")

PATTERNS = {
    "hedges": r"\b(may|might|could|would|suggest\w*|indicat\w*|appear\w*|seem\w*|likely|"
              r"potential\w*|possibl\w*|approximat\w*|relativ\w*|tend\w*)\b",
    "boosters": r"\b(novel|first|significantl\w*|dramatic\w*|substantial\w*|remarkabl\w*|"
                r"unprecedent\w*|crucial|robust|powerful|outperform\w*|state-of-the-art|superior|"
                r"breakthrough)\b",
    "first_person": r"\b(we|our|us|ours)\b",
    "passive": r"\b(was|were|is|are|been|being|be)\s+(\w+ed|made|shown|found|done|given|taken|seen|"
               r"known|used|built|drawn|held|reported|observed|performed)\b",
    "uncertainty": r"(95% ?ci|±|confidence interval|\biqr\b|standard deviation)",
    "citations": r"(\[\d+(?:[-,–]\s*\d+)*\]|\([A-Z][A-Za-z]+(?: et al\.?| and [A-Z][A-Za-z]+)?,?\s*"
                 r"(?:19|20)\d{2}[a-z]?\))",
}

# key -> (label, note when ABOVE journal range, note when BELOW journal range)
FEATURE_META = [
    ("mean_sentence_len", "Mean sentence length (words)",
     "Longer sentences than this journal — split long ones for readability.",
     "Shorter sentences than this journal — may read choppy; combine related clauses."),
    ("mean_paragraph_len", "Mean paragraph length (words)",
     "Denser paragraphs than the journal — consider splitting by job (context/result/etc.).",
     "Shorter paragraphs than the journal — fine; ensure each still develops one idea."),
    ("hedges_per_1k", "Hedging density / 1k words",
     "More hedging than the journal — some claims may be under-stated; check verb strength.",
     "Less hedging than the journal — over-claim risk; calibrate show/suggest/may to evidence."),
    ("boosters_per_1k", "Promotional language / 1k words",
     "More promotional words than the journal — trim 'novel / significantly / SOTA / powerful'.",
     "Fewer boosters than the journal — fine; just keep contributions explicit."),
    ("first_person_per_1k", "First person (we/our) / 1k words",
     "More first-person than the journal — some venues prefer impersonal phrasing.",
     "Less first-person than the journal — fine; ensure agency for what *you* did is clear."),
    ("passive_per_1k", "Passive-voice proxy / 1k words",
     "More passive than the journal — prefer active voice for the authors' actions.",
     "Less passive than the journal — fine."),
    ("uncertainty_per_1k", "Uncertainty markers (95% CI/±) / 1k words",
     "More uncertainty markers than the journal — fine, usually good.",
     "Fewer uncertainty markers than the journal — add CIs/SD to headline numbers."),
    ("citations_per_1k", "Citation density / 1k words",
     "Denser citations than the journal — fine; check relevance.",
     "Sparser citations than the journal — may look under-referenced; check coverage of both fields."),
]

MARGIN = 0.15  # tolerance beyond the observed exemplar [min,max] before flagging


def features(text):
    words = WORD_RE.findall(text)
    nw = max(len(words), 1)
    sents = [s for s in SENT_SPLIT.split(text) if s.strip()]
    sent_lens = [len(WORD_RE.findall(s)) for s in sents] or [0]
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    para_lens = [len(WORD_RE.findall(p)) for p in paras] or [nw]
    per_k = lambda c: round(1000.0 * c / nw, 1)
    cnt = lambda key: len(re.findall(PATTERNS[key], text, re.IGNORECASE))
    return {
        "words": nw,
        "mean_sentence_len": round(statistics.mean(sent_lens), 1),
        "mean_paragraph_len": round(statistics.mean(para_lens), 1),
        "hedges_per_1k": per_k(cnt("hedges")),
        "boosters_per_1k": per_k(cnt("boosters")),
        "first_person_per_1k": per_k(cnt("first_person")),
        "passive_per_1k": per_k(cnt("passive")),
        "uncertainty_per_1k": per_k(cnt("uncertainty")),
        "citations_per_1k": per_k(cnt("citations")),
    }


def collect_texts(paths):
    files = []
    for p in paths:
        pp = Path(p)
        if pp.is_dir():
            files += sorted(pp.glob("*.txt")) + sorted(pp.glob("*.md"))
        elif pp.exists():
            files.append(pp)
        else:
            print(f"[warn] not found: {p}", file=sys.stderr)
    out = []
    for f in files:
        try:
            out.append((f.name, f.read_text(encoding="utf-8")))
        except OSError as e:
            print(f"[warn] cannot read {f}: {e}", file=sys.stderr)
    return out


def profile(exemplar_feats):
    prof = {}
    for key, _, _, _ in FEATURE_META:
        vals = [f[key] for f in exemplar_feats]
        prof[key] = {"min": min(vals), "max": max(vals),
                     "mean": round(statistics.mean(vals), 1)}
    return prof


def verdict(value, lo, hi):
    band_lo, band_hi = lo * (1 - MARGIN), hi * (1 + MARGIN)
    if value < band_lo:
        return "below"
    if value > band_hi:
        return "above"
    return "in range"


def render(prof, n_ex, draft_feats):
    out = ["# Journal-fit style profile", "",
           f"Profiled **{n_ex}** exemplar paper(s) from the target journal."]
    if n_ex < 3:
        out.append("\n> ⚠️ Fewer than 3 exemplars — the 'range' is unreliable. Add more papers from "
                   "the same journal/article-type for a meaningful profile.")
    out += ["", "| Feature | Journal range (min–max, mean) | Your draft | Verdict |",
            "|---|---|---|---|"]
    actions = []
    for key, label, note_above, note_below in FEATURE_META:
        p = prof[key]
        rng = f"{p['min']}–{p['max']} (μ {p['mean']})"
        if draft_feats:
            v = draft_feats[key]
            vd = verdict(v, p["min"], p["max"])
            mark = {"in range": "✓ in range", "above": "▲ above", "below": "▼ below"}[vd]
            out.append(f"| {label} | {rng} | {v} | {mark} |")
            if vd == "above":
                actions.append(f"- **{label}** (yours {v} vs journal ≤{p['max']}): {note_above}")
            elif vd == "below":
                actions.append(f"- **{label}** (yours {v} vs journal ≥{p['min']}): {note_below}")
        else:
            out.append(f"| {label} | {rng} | — | (no draft) |")
    if draft_feats:
        out += ["", "## Where your draft deviates from the journal's style", ""]
        out += actions or ["- Draft is within the journal's range on every measured feature. "
                           "Style audit is qualitative from here (structure, abstract moves, figure "
                           "conventions) — see references/journal-fit.md."]
    out += ["", "> Descriptive guidance from the exemplars you supplied — not a rule, and not a "
            "rewrite. Never change a scientific claim to hit a style target. Pair with stage 07 "
            "(polish) and section/*.md for structure.", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Profile journal house-style and audit a draft against it.")
    ap.add_argument("--exemplars", nargs="+", required=True,
                    help="published papers from the target journal (files and/or dirs of .txt/.md)")
    ap.add_argument("--manuscript", help="your draft to audit against the profile")
    ap.add_argument("--report", help="write the markdown report here")
    args = ap.parse_args()

    exemplars = collect_texts(args.exemplars)
    if not exemplars:
        sys.exit("[error] no readable exemplar texts. Export the journal papers to .txt/.md first.")
    ex_feats = [features(t) for _, t in exemplars]
    prof = profile(ex_feats)

    draft_feats = None
    if args.manuscript:
        try:
            draft_feats = features(Path(args.manuscript).read_text(encoding="utf-8"))
        except OSError as e:
            sys.exit(f"[error] cannot read manuscript: {e}")

    report = render(prof, len(exemplars), draft_feats)
    print(report)
    if args.report:
        Path(args.report).write_text(report + "\n", encoding="utf-8")
        print(f"[ok] wrote {args.report}", file=sys.stderr)
    print(f"[note] profiled {len(exemplars)} exemplar(s): "
          f"{', '.join(n for n, _ in exemplars)}", file=sys.stderr)


if __name__ == "__main__":
    main()
