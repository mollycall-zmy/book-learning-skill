# Card Rules (Deprecated)

Knowledge cards are no longer part of the default book-learning workflow.

Default reading output is:

```text
raw/books/{书名}.md
outputs/reading_notes.md
```

Use this file only if the user explicitly asks to generate cards after the reading note is complete. Card extraction should be an optional archival/review task, not the default reading-stage output.

## Core Rule

Each knowledge card contains one reusable idea. If a draft card needs "and" to join multiple independent claims, split it.

## Required Qualities

- Atomic: one idea, method, model, definition, case, or warning
- Traceable: cites chapter id and title
- Reusable: written so it can help in a future context
- Grounded: no claim that cannot be tied back to the source notes
- Specific: preserves conditions, exceptions, scope, and counterexamples

## Information Density

A knowledge card must contain enough detail to be independently useful.

A card is not valid if it is only a concept name, slogan, short definition, or chapter-title-like summary.

Each card must include:

- Clear idea: what the card is about
- Source: where the idea came from
- Explanation: why this idea matters
- Evidence: cases, data, examples, quotes, or argument chains
- Conditions: when it works, when it may fail, or what assumptions it depends on
- Reusable takeaway: how the idea can be applied elsewhere

知识卡片不是读书笔记标题。一张合格的卡片应该离开原书也能独立使用。

### Concept Cards

Must include:

- Definition
- Reasoning behind the concept
- At least one concrete example
- Source chapter

### Method Cards

Must include:

- Steps
- Applicable conditions
- Failure conditions or limitations
- At least one case study or example

### Model Cards

Must include:

- Components
- Relationships between components
- Causal logic
- Evidence or data that supports the model

### Case Cards

Must include:

- Background
- Action
- Result
- Why it matters
- Reusable insight

### Bad Example

```text
爆品 = 单款、精品、海量、长周期
```

Reason: too shallow. It only names the idea but does not explain how it works, where it came from, or how to reuse it.

### Good Example

```text
爆品四要素：

1. 找准用户需求：直击真实痛点，例如空气质量问题推动空气净化器需求；
2. 超预期产品：产品需要全面优秀，并至少在一个方面明显突出；
3. 惊喜定价：不是简单低价，而是建立在效率和成本结构上的有理由低价；
4. 效率制胜：通过精简 SKU、海量出货、摊薄研发和供应链成本形成优势。
```

This card is better because it includes components, reasoning, example, and reusable logic.

## Depth Requirement

A knowledge card is not valid if it only contains:

- Concept name
- Short definition
- One-line summary
- Chapter-title-like phrase
- Slogan without evidence

A valid knowledge card must contain:

1. Concept / idea
   - The core idea
2. Reasoning
   - Why this idea matters
   - What problem it solves
3. Evidence from the book
   - At least one concrete example, case, data point, argument chain, or quote from the book
4. External connection
   - Connection to another book, framework, discipline, or general knowledge
   - Keep it universal, not user-specific
5. Applicability note
   - When to use this idea
   - When not to use it
   - Assumptions or failure conditions
6. One-sentence distillation
   - One sentence that captures the reusable essence

Each card should remain useful outside the original book. Do not force in user company context.

### Shallow Card Example

```markdown
专注 = 把资源集中在一件事上
```

Problem: only a definition, with no reasoning, case, boundary, counterexample, or transfer value.

### Valid Card Example

```markdown
专注的本质是资源约束下的最优配置。

它重要是因为组织资源有限，什么都做往往意味着什么都做不好。书中可以用具体案例说明：当企业试图同时抓住多个方向时，资源、管理注意力和产品体验都会被稀释。

适用条件：
- 资源有限；
- 目标足够清晰；
- 方向有足够长的验证周期。

失效条件：
- 市场快速变化；
- 新机会窗口极短；
- 企业已有可复用能力，能够支撑多线探索。

外部关联：
这个观点可以连接到定位理论、战略取舍、军事集中兵力原则等。

一句话提炼：
专注不是少做事，而是在资源有限时把胜率最高的事做到足够深。
```

## Card Types

- Concept: defines a term or distinction
- Model: explains a framework or causal structure
- Method: gives a repeatable procedure
- Case: captures an example or data point
- Warning: records a limitation, failure mode, or counterexample
- Quote Note: captures a short, legally safe paraphrase or very short quotation

## Split And Merge

Split when:

- A card contains multiple claims
- A card mixes definition, method, and example
- A card cites unrelated chapters for unrelated reasons

Merge when:

- Two cards restate the same idea
- One card is only an unsupported fragment of another

## Prohibitions

- Do not create cards from unsupported inference.
- Do not paste long copyrighted passages.
- Do not use a chapter summary as a card.
- Do not omit the source chapter.
