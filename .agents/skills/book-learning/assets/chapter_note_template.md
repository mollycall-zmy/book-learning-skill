# Chapter Distillation Prompt / 章节提炼问题清单

Use this as a thinking checklist inside the canonical reading notes.

Do not create separate `.notes.md` files by default.

A good reading note should be content-driven, not template-driven.

读书笔记不是填表。Agent 应先理解本章内容，再选择合适的表达结构。模板是提示清单，不是强制字段。如果本章没有某类内容，不要硬填。

Every chapter must answer this question:

```text
这章最值得带走的知识是什么？
```

Then choose the structure that fits the content.

## Guiding Questions

Read each chapter, then answer only the questions that genuinely fit.

### 1. 核心知识

- 本章定义了什么重要概念？
- 本章提出了什么核心判断？
- 本章澄清了什么容易混淆的问题？

### 2. 关键框架

- 本章有没有模型、分类、步骤、流程、判断标准？
- 这个框架解决什么问题？
- 它由哪些部分组成？

### 3. 支撑证据

- 作者用了什么研究、数据、案例或推理支撑结论？
- 哪些证据最有力？
- 哪些只是故事，不应该被当成核心结论？

### 4. 操作方法

- 本章有没有能直接执行的方法？
- 第一步应该做什么？
- 如何判断自己做对了？
- 常见错误是什么？

### 5. 场景映射

- 本章知识适合用于哪些真实任务？
- 用户在什么情况下应该调用这部分知识？
- 它能帮助评估方案、做决策、写作、沟通还是复盘？

### 6. 认知刷新

- 本章打破了什么常见误解？
- 旧理解是什么？
- 新理解是什么？
- 背后的机制是什么？

### 7. 沟通 / 博弈 / 判断

- 本章是否涉及多方互动？
- 各方的动机是什么？
- 信息差、利益冲突、可信度、风险在哪里？
- 有哪些可以直接使用的提问或反问话术？

### 8. 可复用产物

- 本章最适合沉淀成什么？
  - 定义
  - 框架
  - SOP
  - 清单
  - 判断问题
  - 反问话术
  - 决策表
  - 场景触发器

## Output Principles

- 有定义就写定义。
- 有流程就写流程。
- 有对比就写对比。
- 有机制就写机制。
- 有方法就写 SOP。
- 有博弈就写参与方和变量。
- 没有的内容不要硬填。
- 每个 in-scope 章节必须至少有一个 raw source Markdown backlink。

Backlink examples:

```text
[[raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
[[raw/books/{book_slug}/{book_slug}#{章节标题}|🔗]]
```

Do not backlink to `.cache/book-learning/{book_slug}/chapters/`; chapter files are processing cache, not durable source targets.

## Optional HTML Components

HTML components are optional visual aids, not mandatory structure.

Use `references/html_card_spec.md` when HTML improves readability:

- One-liner card: recommended for the book's central claim.
- Core Framework Grid: use only when the book has 3-8 parallel frameworks or concepts.
- Process Flow: use for clear step-by-step methods.
- Comparison Card: use for contrastive ideas.

Plain Markdown is always acceptable when it better preserves the book's logic.
