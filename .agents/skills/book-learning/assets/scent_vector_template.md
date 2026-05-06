---
card_type: scent-vector
source_note: "{canonical_notes_path}"
scent:
  - 批判性思考
  - 证据检查
scent_en:
  - critical-thinking
  - evidence-checking
---

# Scent Vector / 气味向量

气味向量是一种轻量语义路由线索，用于判断当前任务闻起来像什么问题。

## Scent Tag Rules

`scent` can use Chinese, English, or custom tags.

- 中文标签更适合人读。
- 英文标签更适合稳定程序路由。
- 如果两者都需要，可以同时使用 `scent` 和 `scent_en`。
- 下列英文标签只是推荐词表，不是唯一合法枚举。

## 推荐英文 scent

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

## Routing

用户任务
↓
识别任务语义气味
↓
匹配方法卡 scent 字段
↓
选择 1-3 张最相关方法卡
↓
转化为当前任务的分析动作

## Rules

- scent vector 是可选增强，不是硬依赖。
- scent 只是路由线索，不是最终判断。
- 最终调用方法卡必须服务当前任务。
