# Output Schema

## Knowledge Root

`knowledge_root` / `memory_palace_root` is never hard-coded. Resolve it in this priority order:

1. User-provided `--knowledge-root`.
2. Environment variable `BOOK_LEARNING_KNOWLEDGE_ROOT`.
3. `.book-learning/config.json` or `book-learning.config.json`.
4. Agent context with an explicit `knowledge_root` or `memory_palace_root`.
5. Ask the user whether to archive to a knowledge base.
6. Fall back to `outputs/reading_notes.md` if the user skips archival.

Canonical notes path:

```text
{knowledge_root}/L1-事实与语义/02-📚 知识/{book_slug}-阅读笔记.md
outputs/reading_notes.md
```

Only one canonical notes path may exist per run.

## Output Map

```text
raw/books/{book_slug}/{book_slug}.{ext}
raw/books/{book_slug}/{book_slug}.md
.cache/book-learning/{book_slug}/toc.json
.cache/book-learning/{book_slug}/chapters/
.cache/book-learning/{book_slug}/audit.json
.cache/book-learning/{book_slug}/run_manifest.json
{canonical_notes_path}
```

Rules:

- Raw stores only source assets.
- Cache stores only processing artifacts.
- Reading notes are written only to `canonical_notes_path`.
- Do not create or preserve duplicate reading notes under `raw/`, `raw/books/{book_slug}/outputs/`, or both `outputs/` and `knowledge_root`.

## Raw Source

```text
raw/books/{book_slug}/{book_slug}.{ext}
raw/books/{book_slug}/{book_slug}.md
```

Rules:

- Raw files are read-only after creation.
- `{book_slug}.md` is the source of truth for backlinks and audits.
- Do not put `reading_notes.md`, `chapters/`, `audit.json`, `run_manifest.json`, or `outputs/` in `raw/`.

## Cache Artifacts

```text
.cache/book-learning/{book_slug}/toc.json
.cache/book-learning/{book_slug}/chapters/
.cache/book-learning/{book_slug}/audit.json
.cache/book-learning/{book_slug}/run_manifest.json
```

Rules:

- `toc.json` is a processing index.
- `chapters/` is an intermediate split and cannot be a durable backlink target.
- `audit.json` records the audit of the canonical reading notes.
- `run_manifest.json` bridges the run to text indexes, scent routing, vector systems, and future automation.
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
  "filtered_out": [],
  "filters": {
    "min_lines": 15,
    "max_level": 3,
    "include_sidebars": false,
    "include_toc_heading": false
  }
}
```

Line numbers are 1-based and inclusive.

## Reading Notes

Canonical reading notes path:

```text
{canonical_notes_path}
```

Required high-level structure:

```markdown
---
aliases: [示例书]
tags: [书籍, 阅读笔记]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: YYYY-MM-DD
scent:
  - critical-thinking
  - structured-reading
---

# 《示例书》阅读笔记

<div style="background: linear-gradient(135deg, #FAFAFA 0%, #F2F0EB 100%); padding: 28px; border-radius: 16px; margin: 24px 0;">
  <div style="font-size: 11px; color: #CFA76F; font-weight: 600; letter-spacing: 0.08em; margin-bottom: 10px;">全书一句话</div>
  <div style="font-size: 20px; line-height: 1.7; color: #222; font-weight: 600;">这里写全书最核心的主张。</div>
</div>

## 目录

- [[#第一章 示例章节]]

## 第一章 示例章节

**核心定义/主张**：用 1-2 句话说明本章最核心的观点。[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

**核心结论**：用 1-2 句话写出作者在本章得出的最重要结论。[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

## 全书核心框架

<div style="background: linear-gradient(135deg, #FAFAFA 0%, #F2F0EB 100%); padding: 28px; border-radius: 16px; margin: 24px 0;">
  <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 18px;">全书核心框架</div>
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Framework 01</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">框架一</div>
      <div style="height: 1px; background: rgba(207,167,111,0.35); margin: 0 0 10px 0;"></div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明框架一的作用。</div>
    </div>
  </div>
</div>

## 金句

> 1. “示例金句。”（第一章）
```

Required rules:

- Frontmatter must include `aliases`, `tags`, `author`, `source`, `created`, and `scent`.
- Each book must have 3-5 useful scent tags when possible.
- Scent tags must come from the book's core methods, problem types, and applicable scenes.
- One-liner HTML component is required.
- Core Framework Grid HTML component is required under `## 全书核心框架`.
- Ordinary chapter notes are Markdown by default.
- Process Flow and Comparison HTML components are used when the content calls for them.
- Every in-scope chapter must appear in this file.
- Every chapter must include `核心定义/主张` or `核心主张`.
- Every chapter must include `核心结论`.
- Every chapter must include at least one backlink to the raw source Markdown.

HTML rules:

- HTML must use inline style.
- Do not use external CSS or JavaScript.
- Do not use dark card backgrounds, heavy shadows, or `border-top`.

## Backlink Schema

Recommended raw source Markdown backlink:

```text
[[raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
```

Accepted forms:

```text
[[raw/books/{book_slug}/{book_slug}#{章节标题}|🔗]]
[[/tmp/example-knowledge-root/raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
[[~/example-knowledge-root/raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
```

Rules:

- Backlinks must target `raw/books/`.
- Backlinks must include the chapter heading.
- Backlinks may be relative or absolute.
- Backlinks may use `.md` or the Obsidian extensionless form.
- Backlinks may use pipe alias syntax such as `|🔗`.
- Backlinks must not target `.cache/` or `chapters/`.

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
  "filtered_out_count": 0,
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

With `knowledge_root`:

```json
{
  "book_slug": "示例书",
  "raw_original": "raw/books/示例书/示例书.epub",
  "raw_markdown": "raw/books/示例书/示例书.md",
  "toc": ".cache/book-learning/示例书/toc.json",
  "chapters": ".cache/book-learning/示例书/chapters/",
  "audit": ".cache/book-learning/示例书/audit.json",
  "canonical_notes": "{knowledge_root}/L1-事实与语义/02-📚 知识/示例书-阅读笔记.md",
  "scent": ["critical-thinking", "structured-reading"],
  "scent_index": "{knowledge_root}/气味索引.md",
  "index_status": "ready_for_vector_index",
  "created": "YYYY-MM-DD"
}
```

Without `knowledge_root`:

```json
{
  "book_slug": "示例书",
  "raw_markdown": "raw/books/示例书/示例书.md",
  "canonical_notes": "outputs/reading_notes.md",
  "scent": ["critical-thinking", "structured-reading"],
  "scent_index": null,
  "index_status": "no_knowledge_root",
  "created": "YYYY-MM-DD"
}
```

Rules:

- `canonical_notes` must point to the only final reading notes path.
- `scent` must match reading notes frontmatter.
- `scent_index` is null when no `knowledge_root` exists.
- `index_status` indicates whether the run is ready for later vector indexing.
- Vector indexing is optional and not executed by default.

## Scent Index Entry

If `knowledge_root` exists, update the configured scent index path or:

```text
{knowledge_root}/气味索引.md
```

Entry format:

```markdown
- [[L1-事实与语义/02-📚 知识/{book_slug}-阅读笔记|示例书]]
  - scent: critical-thinking, structured-reading
  - raw: raw/books/{book_slug}/{book_slug}.md
  - manifest: .cache/book-learning/{book_slug}/run_manifest.json
  - status: ready_for_vector_index
```

Text scent indexing is baseline. Vector indexing is optional and handled by an external skill or user system.

## Cognitive Toolbox Artifacts

Optional second-stage outputs are created only after canonical reading notes are complete and audited:

```text
outputs/cognitive_toolbox/method_cards/
outputs/cognitive_toolbox/scene_trigger_index.md
outputs/cognitive_toolbox/scent_vector.md
outputs/cognitive_toolbox/invocation_report.md
```
