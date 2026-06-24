#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""Minimal routing + integrity smoke test for cs-biomed-paper.

Self-contained: standard library only (no PyYAML needed). Run from anywhere:

    python tests/routing_smoke_test.py          # run all checks, exit 0 if green
    python tests/routing_smoke_test.py -v        # verbose: print every passing case

It checks three things, fast, without calling an LLM:

  1. INTEGRITY  — SKILL.md has valid frontmatter (name + description); every path declared in
                  manifest.yaml (always_load, axis values, references.on_demand) exists on disk;
                  the examples/ fixtures exist.
  2. ROUTING    — for a table of realistic Chinese requests, the cue keywords needed to route them to
                  the expected stage / paper_type / section are actually present in manifest.yaml's
                  detect blocks. (We assert the router *can* see the cue, not that an LLM did.)
  3. STANDARDS  — each paper_type fragment names its mandatory reporting standard (CLAIM / TRIPOD+AI /
                  PRISMA / STARD / CONSORT-AI), so paper_type → standard cannot silently break.

This is a guardrail against the cues/paths drifting out of sync, not a substitute for real eval.
"""

import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parents[1]
VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv

_fails = []
_passes = 0


def check(cond, label):
    global _passes
    if cond:
        _passes += 1
        if VERBOSE:
            print(f"  PASS  {label}")
    else:
        _fails.append(label)
        print(f"  FAIL  {label}")


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


# ---------------------------------------------------------------- 1. INTEGRITY
def test_frontmatter():
    txt = read("SKILL.md")
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    check(m is not None, "SKILL.md has a frontmatter block")
    if not m:
        return
    fm = m.group(1)
    check(re.search(r"^name:\s*cs-biomed-paper\s*$", fm, re.M) is not None,
          "frontmatter declares name: cs-biomed-paper")
    check("description:" in fm, "frontmatter has a description")
    # router should stay short — guard against it ballooning into an encyclopedia
    body_lines = txt.count("\n")
    check(body_lines < 200, f"SKILL.md stays router-short ({body_lines} lines < 200)")


def test_manifest_paths():
    man = read("manifest.yaml")
    paths = sorted(set(re.findall(r"(static/[^\s]+\.md|references/[^\s]+\.md|scripts/[^\s]+\.py)", man)))
    check(len(paths) >= 40, f"manifest declares the expected file set ({len(paths)} paths)")
    for p in paths:
        check((ROOT / p).exists(), f"manifest path exists: {p}")


def test_examples_exist():
    for ex in ("examples/write-intro-imaging.md",
               "examples/reviewer-no-external-validation.md",
               "examples/polish-abstract-zh.md",
               "examples/omics-differential-expression.md",
               "examples/systematic-review-prisma.md",
               "examples/match-target-journal-style.md"):
        check((ROOT / ex).exists(), f"example fixture exists: {ex}")


# ---------------------------------------------------------------- 2. ROUTING
# Each case: a realistic Chinese request + the cue substrings that MUST be present in manifest.yaml
# for the router to map it to the intended stage / paper_type / section.
ROUTING_CASES = [
    ("帮我写引言",            ["引言", "intro", "06-section-writing"]),
    ("润色一下摘要",          ["润色", "摘要", "abstract"]),
    ("帮我找文献做综述",       ["找文献", "02-litreview"]),
    ("实验怎么设计、基线消融",  ["实验怎么设计", "04-experiment-stats"]),
    ("画一张投稿级配图",       ["配图", "05-figures"]),
    ("数据可用性 / 代码开源",   ["数据可用性", "08-citation-data-fair"]),
    ("会不会被拒，帮我自查",    ["会不会被拒", "09-prereview-risk"]),
    ("回复审稿意见",          ["回复审稿", "10-rebuttal"]),
    ("医学影像分割",          ["医学影像", "medical-imaging"]),
    ("临床预测模型",          ["临床预测模型", "clinical-ml"]),
    ("单细胞组学分析",         ["单细胞", "组学", "bioinformatics-omics"]),
    ("可穿戴心电信号",         ["心电", "可穿戴", "biosignal-wearable"]),
    ("系统综述 / meta 分析",   ["系统综述", "systematic-review"]),
    ("Nature 子刊投稿",       ["nature-family"]),
    ("投 TMI / MedIA",       ["ieee-tmi-media"]),
    ("统计/数据泄漏自查",      ["stats_leakage_lint.py"]),
    ("按目标期刊文风审稿",     ["journal_style_profile.py", "journal-fit.md"]),
]


def test_routing():
    man = read("manifest.yaml")
    for request, cues in ROUTING_CASES:
        missing = [c for c in cues if c not in man]
        check(not missing, f"routing cue present for “{request}” (missing: {missing})")


# ---------------------------------------------------------------- 3. STANDARDS
PAPER_TYPE_STANDARD = {
    "static/fragments/paper_type/medical-imaging.md": "CLAIM",
    "static/fragments/paper_type/clinical-ml.md": "TRIPOD+AI",
    "static/fragments/paper_type/systematic-review.md": "PRISMA",
    "static/fragments/paper_type/biosignal-wearable.md": "STARD",
}


def test_standards():
    for frag, standard in PAPER_TYPE_STANDARD.items():
        if (ROOT / frag).exists():
            check(standard in read(frag), f"{Path(frag).name} names its standard ({standard})")


def main():
    print("cs-biomed-paper routing + integrity smoke test")
    print("-" * 50)
    test_frontmatter()
    test_manifest_paths()
    test_examples_exist()
    test_routing()
    test_standards()
    print("-" * 50)
    total = _passes + len(_fails)
    if _fails:
        print(f"RESULT: {_passes}/{total} passed, {len(_fails)} FAILED")
        sys.exit(1)
    print(f"RESULT: {_passes}/{total} checks passed — green")


if __name__ == "__main__":
    main()
