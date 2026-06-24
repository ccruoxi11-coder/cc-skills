# cc-skills

面向真实科研写作的 **Codex / Claude Code 技能集**。当前收录一个技能:

| 技能 | 方向 | 一句话简介 |
|---|---|---|
| [`cs-biomed-paper`](cs-biomed-paper/) | 计算机 × 生物医学 / 医学 AI | 从选题到审稿回复的 SCI 论文写作全流程路由技能,内置医学 AI 报告规范与统计/泄漏硬约束 |

---

## 简介

`cs-biomed-paper` 是一个 **router 型技能**:`SKILL.md` 只做路由,按 5 个轴把请求映射到按需加载的
小片段,核心规则放在 `static/fragments`、深度参考放在 `references`、可运行工具放在 `scripts`。
它专为**计算机 × 生物医学交叉**(医学影像、临床机器学习/预测模型、生物信号/可穿戴、生物信息/组学、
方法基准、系统综述)的真实投稿场景设计,覆盖:

> 选题与创新性定位 → 文献综述 → 方法设计 → 实验与统计设计 → 投稿级配图 → 分章写作 →
> 英文润色(中译英) → 引用/数据代码可用性(FAIR)/伦理 → 投稿前拒稿风险自查 → 逐点审稿回复。

与"纯 CS 写作 / 纯医学写作"的区别(硬约束内置):

- **报告规范按论文类型强制挂载**:医学影像→CLAIM、临床预测模型→TRIPOD+AI、前瞻性 AI 试验→
  CONSORT-AI、诊断准确性→STARD、系统综述→PRISMA。
- **临床/生物有效性 ≠ CS 指标**:强制外部验证、校准、亚组与失败分析。
- **统计严谨**:按被试/中心划分防泄漏、置信区间、效应量、多重比较校正。
- **可复现与伦理**:数据/代码可用性、随机种子、IRB/伦理、脱敏合规;**绝不编造**样本量、p 值、
  AUC、CI、DOI、伦理审批号或引用,缺失一律标 `[待补充：…]`。

流程总览(从选题到审稿回复的 10 阶段管线 + 投稿前自查/审稿回环):

<p align="center">
  <img src="cs-biomed-paper/docs/workflow.svg" alt="cs-biomed-paper 论文写作流程图" width="760">
</p>

详细设计与目录见 [`cs-biomed-paper/README.md`](cs-biomed-paper/README.md)。

---

## 安装

技能就是一个文件夹,放进你的技能目录即可被发现:

```bash
# 1) 克隆本仓库
git clone https://github.com/ccruoxi11-coder/cc-skills.git

# 2) 把技能复制到你的 Claude Code / Codex 技能目录（整文件夹复制，保留结构）
#    Windows 示例：
cp -r cc-skills/cs-biomed-paper ~/.claude/skills/
#    或 macOS/Linux 同理；具体目录以你的客户端为准
```

> 复制时务必保留**整个目录结构**(SKILL.md + manifest.yaml + static/ + references/ + scripts/ +
> examples/ + tests/),技能依赖按需加载这些文件,只拷 `SKILL.md` 会失效。

---

## 操作流程(怎么用)

### 1. 触发
用中文直接描述任务即可,例如:"帮我写这篇医学影像分割论文的引言""润色这段摘要""实验怎么设计""审稿人说
没有外部验证,会不会被拒,怎么回复""画一张投稿级 ROC 图""按这几篇目标期刊文章的风格审改我的稿子"。

### 2. 路由(技能自动完成)
技能读取 `manifest.yaml`,沿 5 个轴判定并回显:
- `stage`(主轴,10 阶段:01 选题 → 10 回复)
- `paper_type` → **强制报告规范**
- `section`(摘要/引言/方法/结果/讨论…)、`venue`(Nature 子刊 / IEEE-TMI/MedIA / MICCAI 等 / 通用 SCI)、
  `language`(中译英默认 / 英文)

### 3. 输出(每次固定 7 段)
1. Detected axes  2. One-sentence argument(claim–evidence–boundary)  3. 实际交付物(正文/表格/图文件/
checklist/回复骨架)  4. Claim–evidence map  5. Assumptions or missing inputs(`[待补充]`)
6. Reporting-standard hooks  7. Next minimal action。

### 4. 可运行工具(output-first;除画图外仅标准库)

```bash
# 文献检索 + DOI 核验 → .bib/.ris
python cs-biomed-paper/scripts/ref_search_verify.py -q "deep learning sepsis ICU" --bib refs.bib

# 报告规范缺项核查（CLAIM/TRIPOD+AI/CONSORT-AI/STARD/PRISMA）
python cs-biomed-paper/scripts/reporting_check.py --standard claim --manuscript paper.txt

# 统计/数据泄漏自查（per-sample 划分、缺 CI、未校正 p、无校准、无外部验证、缺伦理）
python cs-biomed-paper/scripts/stats_leakage_lint.py --manuscript paper.txt --fail-on high

# 目标期刊文风画像 + 稿件比对（先把 3–6 篇目标期刊文章导出为 .txt 放进 refs/）
python cs-biomed-paper/scripts/journal_style_profile.py --exemplars refs/ --manuscript draft.txt

# 投稿级图（ROC/校准/forest/box/bars/heatmap；可 --csv 喂真实数据）
python cs-biomed-paper/scripts/figure_template.py --kind roc --out fig.pdf

# 审稿信 → 逐点回复骨架
python cs-biomed-paper/scripts/rebuttal_build.py --letter decision.txt --out response.md --classify
```

### 5. 自检
```bash
python cs-biomed-paper/tests/routing_smoke_test.py    # 路径/frontmatter/中文路由线索 自检
```

---

## 端到端示例
见 [`cs-biomed-paper/examples/`](cs-biomed-paper/examples/):写影像引言、回复"没有外部验证"、中文摘要
润色、组学差异表达、系统综述、按目标期刊文风审改 —— 每个示例展示「中文请求 → 路由 → 产物骨架」。

## 约定
- 产物**英文在前、中文要点在后**;一切缺失值用 `[待补充：…]`,绝不编造。
- 脚本是**分诊工具**,不替代官方报告规范清单与人工核对。

## License
见各技能目录;如未注明,默认仅供学习与科研写作辅助使用。
