# Scent Vector Routing

气味向量不是玄学，而是一种轻量级语义路由机制。

It helps the Agent ask:

> What kind of problem does this task smell like?

## Example Frontmatter

```yaml
scent:
  - critical-thinking
  - evidence-checking
  - hidden-assumption
  - risk-judgment
```

## Common Scent Values

- critical-thinking
- evidence-checking
- hidden-assumption
- credibility-analysis
- risk-judgment
- structured-writing
- conclusion-first
- mece
- scqa
- brand-positioning
- consumer-psychology
- decision-making
- creative-ideation
- review-and-audit
- retrospective-analysis
- business-strategy
- communication-script

## Routing Logic

用户任务
↓
识别任务语义气味
↓
匹配方法卡 scent 字段
↓
选择 1-3 张最相关方法卡
↓
转化为当前任务的分析动作

## Reading Notes Rules

- Each canonical reading note must include 3-5 useful `scent` values in frontmatter.
- The same `scent` values must be mirrored in `.cache/book-learning/{book_slug}/run_manifest.json`.
- If `knowledge_root` exists, update the configured scent index path or `{knowledge_root}/气味索引.md`.

## Rules

- Scent vector routing is optional, not a hard dependency.
- Open-source usage must not require a vector system.
- Support keywords, scene indexes, frontmatter tags, vector similarity, and scent vectors.
- Scent is a routing clue, not the final judgment.
- Final invocation must serve the current user task.
