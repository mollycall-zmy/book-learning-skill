# Scene Trigger Index

The scene trigger index helps the Agent decide which method cards to invoke for a user task.

It should map task types to semantic trigger conditions, typical user expressions, primary method cards, and backup method cards.

## Rules

- Do not rely only on keyword matching.
- Include semantic trigger conditions.
- Include typical user expressions.
- For each task type, call 1-2 primary method cards by default.
- Call at most 3 method cards for one task.
- If no method card fits, complete the task directly and note that a future card may be useful.

## Common Task Types

- 方案评估
- 观点判断
- 决策建议
- 结构化写作
- 复盘归因
- 风险判断
- 沟通话术
- 审计检查

## Invocation Guidance

Use scene triggers as a first pass, then refine selection with task semantics, frontmatter tags, and optional scent vectors.
