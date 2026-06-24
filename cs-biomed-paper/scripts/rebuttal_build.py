#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""Turn a raw reviewer decision letter into a structured point-by-point rebuttal skeleton.

Self-contained: standard library only. The "output first" tool for stage 10. It parses a plain-text
decision letter, splits it into per-reviewer numbered comments, and emits a markdown response
document with one ready-to-fill block per comment (Comment / Response / Change made / Location /
Quoted new text) plus a change-log table.

It does NOT write your responses — that needs your real changes and evidence. It guarantees no comment
is missed (the #1 rebuttal failure) and enforces the structure from references/rebuttal-patterns.md.

Input format (flexible). It recognizes reviewer headers like:
    Reviewer 1 / Reviewer #1 / Reviewer 1: / REVIEWER ONE / Editor
and splits each reviewer's text into comments by: numbered items (1. / 1) / (1)), or blank-line
paragraphs as a fallback. Comments under "Editor"/"AE" are kept as an Editor section.

Usage:
    python rebuttal_build.py --letter decision.txt --out response.md
    python rebuttal_build.py --letter decision.txt           # print to stdout
    python rebuttal_build.py --letter decision.txt --classify  # add a suggested-type hint per comment

Output: a markdown response template (to --out or stdout) and a count of comments per reviewer.
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

REVIEWER_RE = re.compile(
    r"^\s*(reviewer\s*#?\s*\w+|editor(?:'s)?(?:\s+comments)?|associate\s+editor|\bAE\b)\s*[:\-.]?\s*$",
    re.IGNORECASE)
NUM_ITEM_RE = re.compile(r"^\s*(?:\(?\d+[\.\)]|\bcomment\s*\d+\b[:.\-]?)\s+", re.IGNORECASE)

# Keyword hints for the suggested response type (triage only).
TYPE_HINTS = [
    ("Do & show (likely add experiment/analysis)",
     r"\b(external validation|baseline|ablation|calibration|statistic|significan|confidence interval|"
     r"add|provide|include|missing|should (also )?(report|compare|test)|leakage|overfit)\b"),
    ("Clarify (likely already present / misread)",
     r"\b(unclear|not clear|confus|please (clarify|specify|explain)|ambiguous|how (was|did)|define)\b"),
    ("Justify / push back (needs evidence)",
     r"\b(why (not|did)|disagree|questionable|not convinced|justify|rationale|seems)\b"),
    ("Cannot do / scope (explain + alternative)",
     r"\b(impossible|cannot|out of scope|beyond|prospective trial|larger cohort not)\b"),
]


def split_reviewers(text):
    """Return ordered list of (section_name, body_text)."""
    lines = text.splitlines()
    sections, current, buf = [], "General comments", []
    for ln in lines:
        if REVIEWER_RE.match(ln):
            if buf:
                sections.append((current, "\n".join(buf).strip()))
                buf = []
            current = re.sub(r"\s*[:\-.]\s*$", "", ln.strip())
        else:
            buf.append(ln)
    if buf:
        sections.append((current, "\n".join(buf).strip()))
    return [(n, b) for n, b in sections if b]


def split_comments(body):
    """Split a reviewer body into atomic comments: numbered items, else paragraphs."""
    lines = body.splitlines()
    if any(NUM_ITEM_RE.match(ln) for ln in lines):
        comments, cur = [], []
        for ln in lines:
            if NUM_ITEM_RE.match(ln) and cur:
                comments.append(" ".join(cur).strip()); cur = [NUM_ITEM_RE.sub("", ln)]
            elif NUM_ITEM_RE.match(ln):
                cur = [NUM_ITEM_RE.sub("", ln)]
            else:
                cur.append(ln)
        if cur:
            comments.append(" ".join(cur).strip())
        return [c for c in comments if c.strip()]
    # fallback: blank-line-separated paragraphs
    paras = re.split(r"\n\s*\n", body)
    return [re.sub(r"\s+", " ", p).strip() for p in paras if p.strip()]


def classify(comment):
    low = comment.lower()
    for label, pattern in TYPE_HINTS:
        if re.search(pattern, low):
            return label
    return "Do & show (default)"


def tag(section, idx):
    m = re.search(r"(\d+)", section)
    if m:
        return f"R{m.group(1)}.{idx}"
    if re.search(r"editor|AE", section, re.IGNORECASE):
        return f"E.{idx}"
    return f"G.{idx}"


def build(sections, do_classify):
    out = ["# Response to Reviewers", "",
           "We thank the editor and reviewers for their constructive feedback. Below we respond to "
           "each comment point by point. Reviewer comments are in *italics*; our responses follow; "
           "new or changed manuscript text is shown in quoted blocks.", "",
           "_Summary of main changes:_ [待补充：1–3 句概述主要修改，如新增外部验证 / 校准分析 / 更强基线]",
           ""]
    changelog = ["", "## Change log", "", "| Tag | Change | Location in revised manuscript |",
                 "|---|---|---|"]
    counts = {}
    for section, body in sections:
        comments = split_comments(body)
        counts[section] = len(comments)
        out.append(f"## {section}")
        out.append("")
        for i, c in enumerate(comments, 1):
            t = tag(section, i)
            out.append(f"### {t}")
            hint = f"  _(suggested type: {classify(c)})_" if do_classify else ""
            out.append(f"**Comment.**{hint}")
            out.append("")
            out.append("> " + c.replace("\n", "\n> "))
            out.append("")
            out.append("**Response.** [待补充：回应——同意/澄清/反驳，并说明理由]")
            out.append("")
            out.append("**Change made.** [待补充：具体修改了什么；若无修改，说明原因]")
            out.append("")
            out.append("**Location.** [待补充：章节/图/表/行号，或 \"new Supplementary Table SX\"]")
            out.append("")
            out.append("**New/!revised manuscript text:**")
            out.append("")
            out.append("> [待补充：粘贴修改后的稿件原文，便于编辑直接核对]")
            out.append("")
            changelog.append(f"| {t} | [待补充] | [待补充] |")
    return "\n".join(out + changelog) + "\n", counts


def main():
    ap = argparse.ArgumentParser(description="Build a point-by-point rebuttal skeleton.")
    ap.add_argument("--letter", required=True, help="plain-text reviewer decision letter")
    ap.add_argument("--out", help="write the markdown skeleton here (else stdout)")
    ap.add_argument("--classify", action="store_true",
                    help="add a suggested response-type hint per comment")
    args = ap.parse_args()

    try:
        with open(args.letter, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.exit(f"[error] cannot read letter: {e}")

    sections = split_reviewers(text)
    if not sections:
        sys.exit("[error] no content parsed from the letter.")
    skeleton, counts = build(sections, args.classify)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(skeleton)
        print(f"[ok] wrote {args.out}")
    else:
        print(skeleton)

    total = sum(counts.values())
    print(f"[summary] {total} comment(s) across {len(counts)} section(s):", file=sys.stderr)
    for sec, n in counts.items():
        print(f"   - {sec}: {n}", file=sys.stderr)
    print("[reminder] address EVERY comment; verify each promised change is actually in the "
          "manuscript before resubmitting.", file=sys.stderr)


if __name__ == "__main__":
    main()
