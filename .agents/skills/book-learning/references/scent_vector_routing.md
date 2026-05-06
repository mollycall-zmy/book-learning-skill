# Scent Vector Routing

气味向量不是玄学，而是一种轻量级语义路由机制。

It helps the Agent ask:

> What kind of problem does this task smell like?

## Example Frontmatter

```yaml
scent:
  - 批判性思考
  - 证据检查
  - 隐藏假设
  - 风险判断
scent_en:
  - critical-thinking
  - evidence-checking
  - hidden-assumption
  - risk-judgment
```

## Tag Language

`scent` supports English, Chinese, or custom tags.

- If the tags are primarily for human reading, Chinese can be more intuitive.
- If the tags are primarily for program routing, English can be more stable.
- If both are needed, use `scent` for human-readable tags and `scent_en` for stable routing tags.
- Open-source usage does not require one fixed tag vocabulary.
- User systems may define their own tags.

## Recommended Scent Values

These are recommendations, not a required enum.

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

- Each canonical reading note should include useful `scent` values in frontmatter when possible.
- The same `scent` values should be mirrored in `.cache/book-learning/{book_slug}/run_manifest.json`.
- If `knowledge_root` exists, update the configured scent index path or `{knowledge_root}/气味索引.md`.
- Missing or overly generic scent values should produce warnings, not hard failure.

## Rules

- Scent vector routing is optional, not a hard dependency.
- Open-source usage must not require a vector system.
- Support keywords, scene indexes, frontmatter tags, vector similarity, and scent vectors.
- Scent is a routing clue, not the final judgment.
- Final invocation must serve the current user task.
