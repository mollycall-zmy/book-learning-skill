# Workflow

## Purpose

Turn a whole book into one durable, content-driven knowledge artifact that can connect to a user knowledge base or memory palace without hard-coding personal paths.

A good reading note should be content-driven, not template-driven.

中文说明：读书笔记不是填表。Agent 应先理解本章内容，再选择合适的表达结构。模板是提示清单，不是强制字段。如果本章没有某类内容，不要硬填。

Lifecycle boundaries:

- `raw` = read-only source assets
- `.cache` = system intermediate artifacts
- `knowledge_root / memory_palace_root` = user knowledge base root
- `canonical_notes_path` = the only reading notes output path
- `index` = callable entry metadata

Do not keep the same `reading_notes.md` in both `outputs/` and a knowledge base. Each run has exactly one canonical reading notes path.

## Optional Research Context Preflight

Before reading the book, the Agent may gather external context if:

- the user explicitly asks for it
- web access / API access is available
- the user wants broader reception, critique, or background

Possible sources:

- publisher description
- author interviews
- reputable reviews
- public summaries
- academic or professional discussions
- reader reviews, with caution

Rules:

1. External context must not replace reading the original book.
2. External reviews are second-hand interpretations.
3. Do not let popular reviews decide the structure of the notes.
4. Use external context to identify possible themes, controversies, and high-value sections.
5. The final reading notes must still be grounded in the source text.
6. If web/API access is unavailable, skip this step without failing.
7. If used, create `.cache/book-learning/{book_slug}/research_context.md`.
8. Completion report should state whether research context was used.

Use `assets/research_context_template.md`. Do not hard-code any specific website, search engine, or API.

## Path Resolution

Resolve `knowledge_root` in this priority order:

1. User-provided `--knowledge-root`.
2. Environment variable `BOOK_LEARNING_KNOWLEDGE_ROOT`.
3. Project config file `.book-learning/config.json` or `book-learning.config.json`.
4. Agent context with an explicit `knowledge_root` or `memory_palace_root`.
5. If none exists, ask the user: `是否要归档到你的知识库？请提供 knowledge_root 路径。若不提供，将只输出到 outputs/reading_notes.md。`
6. If the user does not provide a path or skips archival, use `outputs/reading_notes.md`.

Canonical notes path:

```text
{knowledge_root}/L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/{book_slug}-阅读笔记.md
outputs/reading_notes.md
```

Rules:

- Use the knowledge path only when `knowledge_root` exists.
- Do not guess a knowledge base path.
- Do not hard-code personal local paths in code, docs, templates, tests, or output.
- If a temporary note must be moved to `knowledge_root`, delete the temporary duplicate after moving.
- `run_manifest.json`, the scent index, and the completion report must point to the final canonical notes path.
- `{matched_knowledge_subdir}` is not fixed. It must come from directory audit, configuration, Agent context, or user confirmation.

## Directory Responsibilities

### Raw Layer

```text
raw/books/{book_slug}/
├── {book_slug}.epub
└── {book_slug}.md
```

Raw stores only read-only source assets. `{book_slug}.md` is the Markdown source of truth for Obsidian backlinks and audits. Do not put `reading_notes.md`, `chapters/`, `audit.json`, `run_manifest.json`, or `outputs/` under `raw/`.

### Cache Layer

```text
.cache/book-learning/{book_slug}/
├── toc.json
├── chapters/
├── research_context.md
├── audit.json
└── run_manifest.json
```

Cache stores processing artifacts only. `chapters/` is not final knowledge content and cannot be used as a durable backlink target.

### Canonical Reading Notes

If `knowledge_root` exists:

```text
{knowledge_root}/L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/{book_slug}-阅读笔记.md
```

If `knowledge_root` does not exist:

```text
outputs/reading_notes.md
```

This is the only final reading note for the run.

## Workflow Steps

### Step 0: Resolve Knowledge Root And Canonical Output

Resolve `knowledge_root` with the priority above. If no path is known, ask the user. If the user skips archival, proceed with `outputs/reading_notes.md` and report that the note was not archived to a knowledge base.

### Step 0.5: Audit Knowledge Directory Structure

If `knowledge_root` exists, inspect:

```text
{knowledge_root}/L1-事实与语义/02-📚 知识/
```

List direct subdirectories only. Select `{matched_knowledge_subdir}` using user-specified category, `preferred_category` from config, Agent context, book topic, user intent, reading lens, scent tags, and semantic fit with existing subdir names.

If confidence is low, ask: `我发现你的知识目录下有多个子目录，这本书应该归档到哪一个？`

Record `knowledge_root`, `knowledge_category_root`, `matched_knowledge_subdir`, `category_match_reason`, and `canonical_notes` in `run_manifest.json`.

### Step 0.6: Optional Research Context Preflight

Run only when the user explicitly asks and web/API access is available. Store the result at:

```text
.cache/book-learning/{book_slug}/research_context.md
```

Use it as background only. It must not decide the reading note structure or override source text.

### Step 0.7: Select Reading Lens

Select one primary lens and optional secondary lenses.

Available lenses:

- `distillation`
- `sop`
- `scene-mapping`
- `cognitive-refresh`
- `communication-game`

Reading lenses are not mutually exclusive templates. They are analytical views. Different chapters may use different lenses.

Write to frontmatter:

```yaml
reading_lens:
  primary: cognitive-refresh
  secondary:
    - scene-mapping
    - sop
```

Default primary lens is `distillation` when the user does not specify and there is no strong reason to choose another.

### Step 1: Store Raw Source

Place the original user file under:

```text
raw/books/{book_slug}/{book_slug}.{ext}
```

Treat it as read-only. Do not commit real books, OCR output, private user files, generated knowledge bases, or generated outputs.

### Step 2: Convert To Source Markdown

Convert the source to:

```text
raw/books/{book_slug}/{book_slug}.md
```

### Step 3: Extract TOC To Cache

```bash
python3 .agents/skills/book-learning/scripts/extract_toc.py raw/books/{book_slug}/{book_slug}.md --out .cache/book-learning/{book_slug}/toc.json --min-lines 15 --max-level 3
```

If the Markdown has no headings, stop and ask for a chapter structure or create a proposed structure for user review.

### Step 4: Split Chapters To Cache

```bash
python3 .agents/skills/book-learning/scripts/split_chapters.py raw/books/{book_slug}/{book_slug}.md --toc .cache/book-learning/{book_slug}/toc.json --out .cache/book-learning/{book_slug}/chapters
```

`chapters/` is cache. It is not a final product and must not become the long-term backlink target.

### Step 5: Generate Reading Notes Directly To Canonical Path

Read every in-scope chapter and write concise, high-density notes into `canonical_notes_path`.

Reading notes must include:

- frontmatter with base source metadata
- `source` pointing to raw source Markdown
- `reading_lens`
- useful `scent` tags when possible
- a directory or chapter navigation
- Markdown chapter notes for every in-scope chapter
- at least one raw source Markdown backlink per covered chapter

Recommended sections, not mandatory for every chapter:

- definitions or claims
- frameworks or mechanisms
- evidence, examples, or reasoning chains
- SOP steps or checklists
- scene triggers or task mappings
- old vs new understanding
- participants, motivations, variables, strategies, or questions

Do not invent content to satisfy a template.

HTML card rules:

- HTML components are optional visual aids, not mandatory structure.
- One-liner cards are recommended for the book's central claim.
- Core Framework Grid should be used only when the book has 3-8 parallel frameworks or concepts.
- Process Flow should be used for clear step-by-step methods.
- Comparison Card should be used for contrastive ideas.
- Plain Markdown is always acceptable when it better preserves the book's logic.
- HTML components must use inline style and must not use external CSS, JavaScript, dark card backgrounds, heavy shadows, or `border-top`.

Scent rules:

- Scent supports English, Chinese, or custom tags.
- The recommended English list is not an enum.
- If both human readability and stable routing are needed, use `scent` and `scent_en`.
- Mirror scent tags in `run_manifest.json`.

## Backlink Rules / 双链回链规则

Every covered chapter section must include backlinks to the raw source Markdown.

Recommended format:

```text
[[raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
```

Accepted formats:

```text
[[raw/books/{book_slug}/{book_slug}#{章节标题}|🔗]]
[[/tmp/example-knowledge-root/raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
[[~/example-knowledge-root/raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
```

Do not point backlinks to `.cache/book-learning/{book_slug}/chapters/`.

## Step 6: Audit Canonical Reading Notes

```bash
python3 .agents/skills/book-learning/scripts/audit_reading_notes.py \
  --toc .cache/book-learning/{book_slug}/toc.json \
  --reading-notes {canonical_notes_path} \
  --raw-source raw/books/{book_slug}/{book_slug}.md \
  --out .cache/book-learning/{book_slug}/audit.json
```

Audit hard checks:

- reading notes file exists
- frontmatter exists and includes base source metadata
- chapter coverage passes
- each covered chapter has at least one valid raw source backlink

Soft warnings:

- section too short
- repeated empty template phrases
- too many identical headings
- no evidence / examples found
- too rigid structure repeated across all chapters
- format issues
- HTML card may be overused
- scent missing or too generic
- research context used but not clearly separated from source reading

Audit should verify coverage, traceability, and obvious structural issues. It should not pretend to judge deep intellectual quality.

## Step 7: Update Run Manifest And Optional Scent Index

Write:

```text
.cache/book-learning/{book_slug}/run_manifest.json
```

If `knowledge_root` exists, also update the configured scent index path or:

```text
{knowledge_root}/气味索引.md
```

Append an entry pointing to the canonical notes path, raw source Markdown, manifest path, scent tags, and vector-index readiness.

Text scent indexing is the baseline capability. Vector indexing is optional enhancement handled by an external skill or user system. `book-learning-skill` outputs index-ready metadata but does not require vector search or embeddings.

## Step 8: Completion Report

```markdown
### 学习完成报告

- **书名**：《示例书》
- **规模**：X 万字，Y 个章节
- **核心收获**：
  1. xxx
  2. xxx
  3. xxx
- **文件**：
  - 原文：`raw/books/示例书/示例书.md`
  - 笔记：`{canonical_notes_path}`
  - 知识分类：`{matched_knowledge_subdir}` / 未归档
  - TOC：`.cache/book-learning/示例书/toc.json`
  - 外部背景：`.cache/book-learning/示例书/research_context.md` / 未使用
  - 审计：`.cache/book-learning/示例书/audit.json`
  - Manifest：`.cache/book-learning/示例书/run_manifest.json`
- **Reading Lens**：primary + secondary
- **Scent Tags**：批判性思考, 证据检查 / critical-thinking, evidence-checking
- **气味索引**：已更新 / 未更新（原因）
- **向量索引**：ready_for_vector_index / no_knowledge_root / not_configured
- **审计**：PASS / FAIL + warnings
```

Do not report per-chapter notes as final artifacts. Do not report knowledge card counts.

## Failure Handling

- Missing converter: run `check_tools.py`, then tell the user which tool is missing.
- Bad TOC: inspect Markdown headings and rerun extraction after improving heading structure.
- Huge book: process chapter batches, but keep one global TOC and one final canonical reading notes file.
- OCR quality issue: ask for a better scan or OCR pass before learning.

## Pitfalls

- Do not confuse chapter split files with final notes.
- Do not mark a chapter covered only because its heading exists.
- Do not omit raw source Markdown backlinks.
- Do not keep duplicate `reading_notes.md` files across `outputs/` and a knowledge base.
- Do not hard-code personal knowledge base paths.
- Do not let external reviews replace source reading.
