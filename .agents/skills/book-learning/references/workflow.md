# Workflow

## Purpose

Turn a whole book into one durable knowledge artifact with clear lifecycle boundaries:

- `raw` = read-only source assets
- `.cache` = system intermediate artifacts
- `L1 / knowledge` = the only knowledge output when a knowledge base path exists
- `index` = callable entry metadata

Do not keep the same `reading_notes.md` in both `outputs/` and a knowledge base. Each run has exactly one canonical reading notes path.

## Directory Responsibilities

### Raw Layer

Raw stores only source assets:

```text
raw/books/{book_slug}/
├── {book_slug}.epub
└── {book_slug}.md
```

Rules:

- Raw files are read-only after creation.
- `{book_slug}.md` must be retained as the Markdown source of truth for Obsidian backlinks and audits.
- Do not put `reading_notes.md`, `chapters/`, `audit.json`, or `run_manifest.json` under `raw/`.

### Cache Layer

Intermediate artifacts go under:

```text
.cache/book-learning/{book_slug}/
├── toc.json
├── chapters/
├── audit.json
└── run_manifest.json
```

Rules:

- `toc.json` is the processing index.
- `chapters/` is a temporary split for chapter-sized reading.
- `audit.json` is the audit report for the canonical notes.
- `run_manifest.json` bridges the run to text indexes, scent routing, and optional vector systems.
- Cache can be kept for debugging or cleaned later. It is not final Obsidian knowledge content.

### Canonical Reading Notes

If the user provides a knowledge base path, write directly to:

```text
L1-事实与语义/02-📚 知识/{book_slug}-阅读笔记.md
```

If no knowledge base path is provided, write to:

```text
outputs/reading_notes.md
```

Rules:

- The canonical reading notes path is the only final reading output for the run.
- Do not keep a duplicate note under `raw/` or another `outputs/` location when the knowledge base path is used.
- If a temporary note must be moved to the knowledge base, delete the temporary duplicate after moving.
- The completion report must state the canonical reading notes path.

## Workflow Steps

### Step 1: Store Raw Source

Place the original user file under:

```text
raw/books/{book_slug}/{book_slug}.{ext}
```

Treat it as read-only. Do not commit real books, OCR output, private user files, or generated knowledge bases.

### Step 2: Convert To Source Markdown

Convert the source to:

```text
raw/books/{book_slug}/{book_slug}.md
```

Supported inputs:

- `.md`: copy or normalize into the raw book folder
- `.pdf`: convert with `pymupdf4llm`
- `.epub`, `.docx`, `.html`, `.htm`: convert with `pandoc`, falling back to `pypandoc` if available

For scanned PDFs, run OCR before conversion. OCR is detected but not automated in the core conversion path.

### Step 3: Extract TOC To Cache

Run `extract_toc.py` on the raw Markdown source:

```bash
python3 .agents/skills/book-learning/scripts/extract_toc.py raw/books/{book_slug}/{book_slug}.md --out .cache/book-learning/{book_slug}/toc.json --min-lines 15 --max-level 3
```

By default, TOC extraction keeps main chapters and filters out likely non-chapter headings:

- TOC headings containing `目录`
- Sidebar / box headings starting with `方框`, `Box`, or `Sidebar`
- Heading level deeper than `--max-level 3`
- Sections shorter than `--min-lines 15`
- Empty or decorative headings

Use `--include-sidebars` only when the user explicitly wants sidebar / box entries preserved as TOC items. If the Markdown has no headings, stop and ask for a chapter structure or create a proposed structure for user review.

### Step 4: Split Chapters To Cache

Run `split_chapters.py` only for processing:

```bash
python3 .agents/skills/book-learning/scripts/split_chapters.py raw/books/{book_slug}/{book_slug}.md --toc .cache/book-learning/{book_slug}/toc.json --out .cache/book-learning/{book_slug}/chapters
```

`chapters/` is cache. It is not a final product and must not become the long-term backlink target.

### Step 5: Generate Reading Notes To Canonical Path

Read every in-scope chapter and write concise, high-density notes into the canonical reading notes path.

Each chapter note should help a reader who has not read the book quickly understand what the book says. Focus on:

1. Core Definition / Claim
2. Key Framework
3. Core Conclusion
4. Supporting Evidence
5. Source Backlink

Do not create default per-chapter `.notes.md` files, `outputs/notes/`, `outputs/book_summary.md`, or `knowledge_cards/`. Long books may be grouped by part, volume, or theme, but no in-scope chapter may be omitted.

## Reading Notes Structure

Use this structure inside the canonical reading notes path:

```markdown
---
aliases: [示例书]
tags: [书籍, 分类]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: YYYY-MM-DD
---

# 📚 《示例书》— 示例作者

## 目录

- [[#第一章 示例章节]]

## 第一章 示例章节

**核心定义/主张**：用 1-2 句话说明本章最核心的观点。[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

**关键框架**：

- 框架 / 方法 / 分类 / 模型：说明其结构和含义。[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

**核心结论**：用 1-2 句话写出作者在本章得出的最重要结论。[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

**支撑证据**：

- 证据：保留最有力的数据、研究、案例或论证链。

## 全书核心框架

概括全书最重要的模型、框架或方法。

## 金句

> 1. “示例金句。”（第一章）
```

Rules:

- Every in-scope chapter must appear in the canonical reading notes.
- Remove storytelling noise and conversational filler.
- Do not copy long passages from the book.
- Do not fill template fields mechanically.
- If a field is not applicable, omit it.
- Default target length: 15-25 lines per chapter.
- If the author's argument has an obvious dispute, boundary, or counterexample, mention it briefly after the conclusion or evidence.

## Backlink Rules / 双链回链规则

Every chapter section must include backlinks to the raw source Markdown.

Recommended format:

```text
[[raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
```

Obsidian extensionless format is also accepted:

```text
[[raw/books/{book_slug}/{book_slug}#{章节标题}|🔗]]
```

Rules:

- Backlink targets must point to `raw/books/{book_slug}/{book_slug}.md` or its extensionless Obsidian form.
- Do not point backlinks to `.cache/book-learning/{book_slug}/chapters/`.
- `chapters/` is an intermediate artifact and cannot be used as the long-term source target.
- `核心定义/主张` and `核心结论` should include backlinks at the end.
- If `关键框架` exists, each framework item should include a backlink.
- `支撑证据` does not require backlinks, but may include them when useful.
- Do not add backlinks to `全书核心框架` or `金句`.

## Formatting Audit

Reading notes may include tables, Mermaid diagrams, Obsidian callouts, and inline HTML cards. Keep tables and Mermaid blocks unindented, with a blank line before them, and do not place them inside list items or callouts.

Inline HTML cards are allowed for high-level visual sections such as `全书一句话`, process flows, comparison frameworks, and `全书核心框架`. Use inline style only and keep ordinary chapter content in Markdown when that is easier to maintain.

## Audit Canonical Reading Notes

Audit the canonical reading notes path:

```bash
python3 .agents/skills/book-learning/scripts/audit_reading_notes.py \
  --toc .cache/book-learning/{book_slug}/toc.json \
  --reading-notes {canonical_notes_path} \
  --raw-source raw/books/{book_slug}/{book_slug}.md \
  --out .cache/book-learning/{book_slug}/audit.json
```

The audit checks:

1. Canonical reading notes file exists.
2. Frontmatter includes `aliases`, `tags`, `author`, `source`, and `created`.
3. All in-scope TOC chapter titles appear in the note.
4. Every chapter has `核心定义/主张` or `核心主张`.
5. Every chapter has `核心结论`.
6. Every chapter has at least one raw source Markdown backlink.
7. The note contains `全书核心框架`.
8. The note contains `金句`.
9. HTML / Markdown formatting warnings are reported as `format_issues`.

Do not proceed to completion if the audit fails.

## Update Index Manifest

After audit, write:

```text
.cache/book-learning/{book_slug}/run_manifest.json
```

Example:

```json
{
  "book_slug": "sample-book",
  "raw_original": "raw/books/sample-book/sample-book.epub",
  "raw_markdown": "raw/books/sample-book/sample-book.md",
  "toc": ".cache/book-learning/sample-book/toc.json",
  "chapters": ".cache/book-learning/sample-book/chapters/",
  "audit": ".cache/book-learning/sample-book/audit.json",
  "canonical_notes": "L1-事实与语义/02-📚 知识/sample-book-阅读笔记.md",
  "index_status": "ready_for_index",
  "scent": ["critical-thinking", "structured-reading"],
  "created": "YYYY-MM-DD"
}
```

Rules:

- `run_manifest.json` is the bridge file for text indexes, scent routing, vector systems, and future automation.
- `book-learning-skill` does not require a vector database.
- If a vector search or embedding skill exists, it can read `run_manifest.json` and index `canonical_notes`.
- If no vector system exists, update the text scent index or tell the user that vector indexing is a follow-up.

## Scent Index And Vector Index

Text scent indexing is the baseline capability. Vector indexing is optional enhancement.

Rules:

- The skill outputs index-ready metadata through `run_manifest.json`.
- Scent values are routing hints, not hard dependencies.
- Vector search / embedding is handled by an external skill or user system.
- Do not make vector search a requirement for learning a book.
- The completion report should state whether the text index was updated, the `run_manifest.json` path, and whether vector indexing is still needed.

## Cognitive Toolbox Stage

After the canonical reading notes are complete and audited, the Agent may create a cognitive toolbox from the book only when useful or explicitly requested.

This optional stage can include:

- 3-5 method cards
- Scene trigger index
- Optional scent vectors
- Invocation guide

Rules:

- Do not create method cards before the canonical reading notes are complete.
- Method cards must be actionable and must not replace the reading notes.
- Scent vectors are optional routing hints, not hard dependencies.
- Do not restore default knowledge-card generation or per-chapter note files.

## Completion Report

Use this concise report:

```markdown
### 学习完成报告

- **书名**：《示例书》
- **规模**：X 万字，Y 个章节
- **核心收获**：
  1. xxx
  2. xxx
  3. xxx
- **文件**：
  - 原始文件：`raw/books/示例书/示例书.epub`
  - 原文 Markdown：`raw/books/示例书/示例书.md`
  - 处理缓存：`.cache/book-learning/示例书/`
  - 笔记：`{canonical_notes_path}`
  - Manifest：`.cache/book-learning/示例书/run_manifest.json`
- **审计**：PASS / FAIL + 原因
- **索引**：文本索引已更新 / 未更新；向量索引已执行 / 需要后续执行
```

If only part of the book was studied, explicitly write:

```text
本次只覆盖第 X 章至第 Y 章，未覆盖全书。
```

## Failure Handling

- Missing converter: run `check_tools.py`, then tell the user which tool is missing.
- Bad TOC: inspect Markdown headings and rerun extraction after improving heading structure.
- Huge book: process chapter batches, but keep one global TOC and one final canonical reading notes file.
- OCR quality issue: ask for a better scan or OCR pass before learning.

## Pitfalls

- Do not confuse chapter split files with final notes.
- Do not mark a chapter covered only because its heading exists.
- Do not hide definitions, frameworks, conclusions, or evidence behind generic commentary.
- Do not omit raw source Markdown backlinks.
- Do not keep duplicate `reading_notes.md` files across `outputs/` and a knowledge base.
