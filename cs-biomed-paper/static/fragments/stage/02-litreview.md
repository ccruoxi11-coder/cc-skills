# Stage 02 — Literature search & synthesis

**Goal:** a verified, theme-organized evidence base spanning *both* fields.

## Steps

1. **Search both worlds.** Biomedical side: PubMed/MEDLINE (MeSH terms), Embase, clinical-trial
   registries. CS side: arXiv, OpenReview, DBLP, IEEE/ACM, top venues. Cross-field: Scopus, Web of
   Science, Google Scholar, Semantic Scholar. Use `scripts/ref_search_verify.py` for a multi-source
   pass + DOI/citation verification and `.bib`/`.ris` export.
2. **Verify every citation** against a primary record (DOI, PubMed, publisher page) — title, authors,
   year, venue. Never cite from a title or a secondary mention (principle: **primary source first**).
3. **Synthesize by theme, not by paper.** Group prior work into 3–5 threads (e.g. clinical task,
   competing methods, datasets/benchmarks, validation practice) and state where each thread stops —
   that gap is your stage-01 claim.
4. For a **systematic review**, switch to PRISMA: pre-register the protocol, log the search string and
   dates, screen with explicit inclusion/exclusion, and build the PRISMA flow diagram
   (`references/reporting-standards/prisma.md`).

## Common pitfalls

- Searching only CS venues and missing the clinical literature (or vice versa) → reviewers from the
  other field will list what you ignored.
- Citing a paper for a claim it never makes; citing reviews instead of the primary study.
- Stale "recent work" — confirm you have the latest; mark `[待补充：近 N 个月新文献]` if unsure.
- MeSH vs free-text mismatch: use both controlled vocabulary and keyword variants.

## Output

A theme-grouped synthesis, a verified reference list / `.bib` path, and the explicit gap statement.
