# Reading Lenses

Reading lenses are not rigid templates. They are ways of seeing the book.

Before writing `reading_notes.md`, choose one primary lens and optional secondary lenses.

If the user specifies a lens, follow it. If not, infer from:

- book type
- table of contents
- user goal
- scent tags
- chapter content

If confidence is low, ask the user which lens should lead the note.

Frontmatter example:

```yaml
reading_lens:
  primary: cognitive-refresh
  secondary:
    - scene-mapping
    - sop
```

Also write the lens decision to `.cache/book-learning/{book_slug}/run_manifest.json`.

中文说明：

读书视角不是固定模板，而是理解这本书的角度。一本书可以混合多个视角：有些章节适合认知刷新，有些章节适合 SOP，有些章节适合场景映射，有些章节适合沟通博弈。Agent 应根据内容灵活组织笔记。

## Available Lenses

### `distillation` / 干货提炼

Use when the book is theory-heavy, concept-heavy, or the user mainly wants to know what the book says.

Useful structures:

- definition
- claim
- framework
- conclusion
- evidence

### `sop` / 执行手册

Use when the chapter contains practical methods, workflows, skill training, or repeatable execution steps.

Useful structures:

- applicable scene
- steps
- checklist
- common mistakes
- output template

### `scene-mapping` / 场景映射

Use when the knowledge can become a real task tool for work, strategy, decisions, writing, review, or consulting.

Useful structures:

- applicable tasks
- scene triggers
- usage actions
- expected outputs
- decision or review checklist

### `cognitive-refresh` / 认知刷新

Use when the chapter changes how a reader understands a problem, mechanism, or common assumption.

Useful structures:

- old understanding
- new understanding
- mechanism
- counterintuitive point
- evidence basis

### `communication-game` / 沟通博弈

Use when the content involves persuasion, negotiation, questioning, conflict, credibility, or multi-party judgment.

Useful structures:

- situation definition
- participants
- motivations
- key variables
- usable strategies
- questions or counter-questions

## Mixing Lenses

Do not force one lens across the whole book.

- A chapter with a method can use `sop`.
- A chapter with a contrast can use `cognitive-refresh`.
- A chapter about applying the idea to real work can use `scene-mapping`.
- A chapter about interaction, persuasion, or judgment can use `communication-game`.

The note should preserve the book's logic. Plain Markdown is acceptable when a lens does not require a special visual structure.

## HTML Guidance

HTML cards are optional visual aids:

- `distillation`: Core Framework Grid can help when the book has 3-8 parallel concepts.
- `sop`: Process Flow can help when the method has clear steps.
- `scene-mapping`: Comparison or Core Framework Grid can help when mapping tasks or choices.
- `cognitive-refresh`: Comparison can help old vs new understanding.
- `communication-game`: Process Flow or Comparison can help strategies and tradeoffs.

Use HTML only when it improves readability. Do not force cards into narrative, progressive, argumentative, mathematical, or non-grid-friendly books.
