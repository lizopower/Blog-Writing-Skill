# Cluster Voice 检查指引

本文说明 `cluster_voice_check.py` 的用途、何时运行、如何解读结果，以及它与 `check_draft.py`、editorial_review 品味评审的关系。

## 解决的问题

`check_draft.py`（机械单篇）和 content-taste-advisor 的七维品味评审都是**逐篇**看的。当你为同一个集群 / 系列一次写三篇文章时，三篇可以各自全过，放在一起却是同一个声音：开头都是同一个套路、都用相同的 AI 套话、复用同样的多词短语、句子节奏一模一样。这一层此前没有任何环节覆盖。

本脚本把集群里 2 篇以上的草稿**互相**比对，报告跨文章的声音撞车。它复用 `_article_type_profiles.py` 里的 `AI_CLICHES_EN` / `AI_CLICHES_ZH` / `CONTRAST_REFRAME_PATTERNS`，与单篇 linter 的判定保持一致。

## 适用场景

| 阶段 | 建议命令 | 说明 |
|------|----------|------|
| 集群内每篇都过了单篇 lint 后 | `cluster_voice_check.py --root . --slugs a,b,c` | 跨文章互比，找共用套路 |
| editorial_review 阶段（集群文章） | 同上 + `--write-report` | 结果并入品味评审第 8 维 |
| 品牌 / 实体 / 关键词天然重复 | 加 `--allow "词1,词2"` | 让这些词不计入短语重复 |

单篇文章无需运行本脚本；它只在集群 / 系列场景下有意义。

## 快速命令

按 slug 解析（工作区在 `content/articles/<slug>/`）：

```bash
python skills/tech-blog-writer/scripts/cluster_voice_check.py \
  --root <project-root> --slugs slug-a,slug-b,slug-c --write-report
```

直接给路径（工作区目录或 `draft.md`）：

```bash
python skills/tech-blog-writer/scripts/cluster_voice_check.py \
  content/articles/a content/articles/b content/articles/c
```

排除天然会重复的词（品牌名、共用主关键词、实体名）：

```bash
python skills/tech-blog-writer/scripts/cluster_voice_check.py \
  --root . --slugs a,b,c --allow "digital twin,ACME"
```

各文章 `article.json` 里的 `primaryKeyword` 会被自动加入豁免，无需手动重复填写。

## 检查项与严重度

| 检查 | 判定 | 严重度 |
|------|------|--------|
| 开头句撞车 | 两篇首句前 4 词相同，或首句词汇重叠 ≥ 60% | ISSUE |
| 开头套路 | 所有文章都以疑问句开场，或首词全相同 | WARN |
| 共用 AI 套话 | 同一条英/中套话出现在**全部**文章 | ISSUE |
| 共用 AI 套话 | 出现在 ≥2 篇但非全部 | WARN |
| 共用对比句式 | 同一种 "It's not X, it's Y" 类模板全部命中 | ISSUE |
| 短语重复 | 跨 ≥2 篇的独特 5 词短语（非停用词/豁免词） | WARN，累计 ≥6 条升 ISSUE |
| 整句复用 | 跨 ≥2 篇的 8 词以上连续片段 | ISSUE |
| 句子节奏 | 各篇平均句长极差 < 1.5 词 | WARN |
| 章节骨架 | 两篇 H2 数量相同且标题按序高度重合 | WARN |

阈值集中定义在脚本顶部常量（`NGRAM_SIZE`、`OPENING_JACCARD_SIMILAR`、`SHARED_NGRAM_ISSUE` 等），按需微调。

## 退出码与产物

- 有任一 ISSUE：退出码 `1`（可用于 CI / 阶段门禁）；否则 `0`。
- `--write-report`：默认在第一个目标的父目录写 `cluster_voice_report.md`；也可 `--write-report <path>` 指定路径。报告为 passes / warns / issues 的 Markdown，格式与 `draft_lint.md` 一致。

## 与 editorial_review 的关系

在 editorial_review 阶段，若文章属于集群：先读同集群其它草稿，再运行本脚本，把结果并入品味评审。评分表新增第 8 维 **Cross-article voice diversity**——脚本报 ISSUE 或人工判断三篇同一个味，打 1-2 分并令 Publishability 判 FAIL；每篇各有其声打 4-5 分；单篇文章该维填 `N/A`。详见 `skills/content-taste-advisor/SKILL.md` 的 Lifecycle Gate。

## 已知边界

- 短语 / 整句重复检测基于英文词元；中文靠套话黑名单覆盖，暂不做中文 n-gram 切分。若集群主要为中文长句复用，需人工复读补足。
- 脚本只测机械可量化的撞车，"气质雷同"这类微妙同质仍依赖品味评审的人工跨读。两层配合使用。
