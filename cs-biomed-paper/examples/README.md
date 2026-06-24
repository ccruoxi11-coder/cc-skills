# Worked examples

On-demand worked examples — **not** loaded by default. Each file shows one realistic Chinese request
routed through the skill: the detected axes, the one-sentence argument, the deliverable shape, and the
honesty scaffolding (`[待补充]`, claim–evidence map, reporting-standard hooks).

They are illustrative templates, **not** real results: every number/citation/approval is a
`[待补充：…]` placeholder. Use them to check the router behaves and to see the expected output shape;
they double as the fixtures behind `tests/routing_smoke_test.py`.

| File | Request (中文) | Routes to |
|---|---|---|
| [write-intro-imaging.md](write-intro-imaging.md) | "帮我写这篇医学影像分割论文的引言" | stage 06 + section intro, paper_type medical-imaging → CLAIM |
| [reviewer-no-external-validation.md](reviewer-no-external-validation.md) | "审稿人说没有外部验证，会不会被拒？怎么回复？" | stage 09 + 10, paper_type clinical-ml → TRIPOD+AI |
| [polish-abstract-zh.md](polish-abstract-zh.md) | "帮我润色这段摘要"（中文笔记） | stage 07, language zh-to-en |
| [omics-differential-expression.md](omics-differential-expression.md) | "写差异表达/组学分析的方法和结果" | stage 03 + 06, paper_type bioinformatics-omics (FDR + 批次效应) |
| [systematic-review-prisma.md](systematic-review-prisma.md) | "写一篇 AI 临床任务的系统综述怎么开始" | stage 02 + 06, paper_type systematic-review → PRISMA |
| [match-target-journal-style.md](match-target-journal-style.md) | "按这几篇目标期刊文章的风格审核修改我的稿子" | stage 07 + 09, journal-fit（`journal_style_profile.py`） |

Together these cover all six paper types (imaging, clinical-ml, omics, systematic-review directly;
biosignal & methods-benchmark follow the same shape via their fragments).
