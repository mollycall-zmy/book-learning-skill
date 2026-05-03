# Output Schema

## Output Map

Each run has these output locations:

```text
raw/books/{book_slug}/{book_slug}.md
.cache/book-learning/{book_slug}/toc.json
.cache/book-learning/{book_slug}/chapters/
.cache/book-learning/{book_slug}/audit.json
.cache/book-learning/{book_slug}/run_manifest.json
{canonical_notes_path}
```

`canonical_notes_path` is one of:

```text
{user_provided_knowledge_path}/{book_slug}-阅读笔记.md
outputs/reading_notes.md
```

Use `outputs/reading_notes.md` only when the user has not provided a knowledge base path. Do not create or preserve duplicate reading notes under `raw/`, `raw/books/{book_slug}/outputs/`, or both `outputs/` and `L1`.

## Raw Source

Raw source paths:

```text
raw/books/{book_slug}/{book_slug}.{ext}
raw/books/{book_slug}/{book_slug}.md
```

Rules:

- Raw stores only the original source asset and converted full Markdown.
- Raw files are treated as read-only after creation.
- `{book_slug}.md` is the source of truth for Obsidian backlinks and audits.
- Do not put `reading_notes.md`, `chapters/`, `audit.json`, or `run_manifest.json` in `raw/`.

## Cache Artifacts

Cache paths:

```text
.cache/book-learning/{book_slug}/toc.json
.cache/book-learning/{book_slug}/chapters/
.cache/book-learning/{book_slug}/audit.json
.cache/book-learning/{book_slug}/run_manifest.json
```

Rules:

- `toc.json` is a processing index.
- `chapters/` is the chapter split used for internal reading.
- `audit.json` records the audit of the canonical reading notes.
- `run_manifest.json` is the bridge file for text indexes, scent routing, vector systems, and future automation.
- Cache is not final Obsidian knowledge content.

## TOC JSON

```json
{
  "source": "raw/books/示例书/示例书.md",
  "chapters": [
    {
      "id": "001",
      "title": "第一章 示例章节",
      "level": 2,
      "start_line": 10,
      "end_line": 85,
      "line_count": 76,
      "slug": "chapter-title"
    }
  ],
  "filtered_out": [
    {
      "id": "004",
      "title": "方框1.1 示例侧栏",
      "reason": "sidebar_or_box"
    }
  ],
  "filters": {
    "min_lines": 15,
    "max_level": 3,
    "include_sidebars": false,
    "include_toc_heading": false
  }
}
```

Line numbers are 1-based and inclusive. `chapters` should contain main chapters by default. `filtered_out` is retained for debugging and may include TOC headings, sidebars, box fragments, deep headings, short fragments, or decorative headings.

## Reading Notes

Canonical reading notes path:

```text
{canonical_notes_path}
```

Required structure:

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

- 证据：最有力的数据、研究、案例或原文论证。

## 全书核心框架

概括全书最重要的模型、框架或方法。

## 金句

> 1. “示例金句。”（第一章）
```

Rules:

- Every in-scope chapter must appear in this file.
- Every chapter must include `核心定义/主张` or `核心主张`.
- Every chapter must include `核心结论`.
- Every chapter must include at least one backlink to the raw source Markdown.
- `核心定义/主张` must include a backlink.
- `核心结论` should include a backlink.
- `关键框架` is required when the chapter contains a model, method, classification, process, or structure.
- If `关键框架` is present, each item should include a backlink.
- `支撑证据` is required when the chapter contains research, data, cases, or a clear argument chain.
- `支撑证据` does not require backlinks.
- Do not invent frameworks or evidence just to fill a field.
- Long books may be grouped by part, section, or theme, but chapters must not be omitted.

## Backlink Schema

Recommended raw source Markdown backlink:

```text
[[raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
```

Accepted Obsidian extensionless backlink:

```text
[[raw/books/{book_slug}/{book_slug}#{章节标题}|🔗]]
```

Rules:

- Backlinks must target the converted full Markdown source under `raw/books/{book_slug}/`.
- Do not target `.cache/book-learning/{book_slug}/chapters/`.
- Do not use chapter split files as durable source links.

## Formatting Constraints

- Tables must not be indented.
- Tables must have a blank line before them.
- Tables must not be inside list items.
- Tables must not be inside callout blocks.
- Mermaid blocks must not be indented.
- Mermaid blocks must have a blank line before the opening fence.
- Callouts must not contain tables or Mermaid diagrams.

## HTML Card Components

The canonical reading notes may contain inline HTML components for high-level visual sections.

Supported components:

- Book one-liner card
- Process flow card
- Core framework grid card
- Comparison card

Rules:

- HTML must use inline style.
- Do not use external CSS or JavaScript.
- Do not use dark card backgrounds, heavy shadows, top border decoration, or large decorative color blocks.
- Keep ordinary chapter notes in Markdown unless visualization improves readability.

## Reading Notes Audit JSON

Path:

```text
.cache/book-learning/{book_slug}/audit.json
```

Schema:

```json
{
  "reading_notes_exists": true,
  "checked_chapters": 2,
  "covered_chapters": 2,
  "filtered_out_count": 3,
  "frontmatter_passed": true,
  "missing_frontmatter_fields": [],
  "chapter_coverage_passed": true,
  "missing_chapters": [],
  "core_claims_passed": true,
  "chapters_missing_core_claim": [],
  "core_conclusions_passed": true,
  "chapters_missing_core_conclusion": [],
  "backlinks_passed": true,
  "chapters_missing_backlinks": [],
  "format_issues": [],
  "coverage_details": [],
  "has_core_framework": true,
  "has_quotes": true,
  "passed": true
}
```

## Run Manifest

Path:

```text
.cache/book-learning/{book_slug}/run_manifest.json
```

Schema:

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

- `run_manifest.json` is for indexers, scent routing, vector systems, and later automation.
- `index_status` should be `ready_for_index` after audit passes.
- `scent` is optional metadata for text routing.
- The skill does not require a vector database.

## Cognitive Toolbox Artifacts

These are optional second-stage outputs created only after the canonical reading notes are complete and audited.

Recommended paths:

```text
outputs/cognitive_toolbox/method_cards/
outputs/cognitive_toolbox/scene_trigger_index.md
outputs/cognitive_toolbox/scent_vector.md
outputs/cognitive_toolbox/invocation_report.md
```

Rules:

- Method cards should include the canonical reading notes path as their source note.
- Scent vectors are optional semantic routing hints.
- Invocation reports are only for testing whether method cards improve real task outputs.
