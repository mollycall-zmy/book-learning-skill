# Reading Modes

Before writing `reading_notes.md`, choose one reading mode. If the user specifies a mode, follow it. If not, infer from book type, user goal, table of contents, and scent tags. If confidence is low, ask:

```text
你希望用哪种模式消化这本书？
0. 教材式干货提炼
1. SOP / 执行手册
2. 场景映射 / 生产力转化
3. 认知刷新 / 反常识洞察
4. 沟通博弈 / 决策推演
```

Default mode is `mode-0-distillation`.

Write the selected mode to reading notes frontmatter:

```yaml
reading_mode: mode-0-distillation
```

Also write it to `.cache/book-learning/{book_slug}/run_manifest.json`.

## Mode 0: 教材式干货提炼

ID: `mode-0-distillation`

Suitable for theory books, methodology books, concept-heavy books, and users who want to quickly know what the book says.

Chapter template:

```markdown
**核心定义/主张**：...

**关键框架**：...

**核心结论**：...

**支撑证据**：...

**来源回链**：[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]
```

Audit fields:

- `核心定义/主张`
- `核心结论`
- `source_backlink`

Preferred HTML: Core Framework Grid.

## Mode 1: SOP / 执行手册

ID: `mode-1-sop`

Suitable for practical books, skill training, workflows, and methods that can be directly executed.

Chapter template:

```markdown
**适用场景**：这个方法用于什么任务。

**执行步骤**：

1. Step 1
2. Step 2
3. Step 3

**检查清单**：

- [ ] 检查项 1
- [ ] 检查项 2

**常见错误**：

- 错误 1
- 错误 2

**输出模板**：

- 输出字段 1：
- 输出字段 2：

**来源回链**：[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]
```

Audit fields:

- `执行步骤`
- `检查清单`
- `source_backlink`

Preferred HTML: Process Flow.

## Mode 2: 场景映射 / 生产力转化

ID: `mode-2-scene-mapping`

Suitable for business thinking, management, branding, decision-making, consulting, and books that can become real task tools.

Chapter template:

```markdown
**核心方法**：本章能转化成什么方法。

**适用任务**：

- 任务 1
- 任务 2

**场景触发词**：

- 用户说“帮我审一下”
- 用户说“这个方案靠谱吗”

**使用动作**：

1. 分析动作 1
2. 分析动作 2

**输出结果**：

- 应该输出什么类型的结果。

**来源回链**：[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]
```

Audit fields:

- `适用任务`
- `场景触发词`
- `使用动作`
- `source_backlink`

Preferred HTML: Comparison + Core Framework Grid.

## Mode 3: 认知刷新 / 反常识洞察

ID: `mode-3-cognitive-refresh`

Suitable for theory popularization, psychology, social science, cognitive upgrades, and worldview-refreshing books.

Chapter template:

```markdown
**旧认知**：读者可能原本怎么理解。

**新认知**：作者提供了什么新的理解。

**关键机制**：这个现象背后的机制是什么。

**反常识点**：最值得改变认知的地方。

**证据依据**：

- 研究 / 数据 / 案例

**我应该如何重新理解这个问题**：

- 新理解 1
- 新理解 2

**来源回链**：[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]
```

Audit fields:

- `旧认知`
- `新认知`
- `关键机制`
- `source_backlink`

Preferred HTML: Comparison.

## Mode 4: 沟通博弈 / 决策推演

ID: `mode-4-communication-game`

Suitable for communication, negotiation, critical thinking, games, questioning, persuasion, and conflict handling.

Chapter template:

```markdown
**局面定义**：当前是什么类型的互动 / 冲突 / 判断局面。

**参与方**：

- A 方：
- B 方：
- 旁观者 / 第三方：

**各方动机**：

- A 方想要什么：
- B 方想要什么：

**关键变量**：

- 信息差：
- 利益冲突：
- 可信度：
- 风险：

**可用策略**：

1. 策略 1
2. 策略 2

**反问话术**：

- 你有什么证据说明...？
- 这个结论是否还有其他解释？

**来源回链**：[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]
```

Audit fields:

- `局面定义`
- `参与方`
- `关键变量`
- `source_backlink`

Preferred HTML: Process Flow + Comparison.

