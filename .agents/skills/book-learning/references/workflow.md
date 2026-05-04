# Workflow

## Purpose

Turn a whole book into one durable knowledge artifact that can connect to a user knowledge base or memory palace without hard-coding personal paths.

Lifecycle boundaries:

- `raw` = read-only source assets
- `.cache` = system intermediate artifacts
- `knowledge_root / memory_palace_root` = user knowledge base root
- `canonical_notes_path` = the only reading notes output path
- `index` = callable entry metadata

Do not keep the same `reading_notes.md` in both `outputs/` and a knowledge base. Each run has exactly one canonical reading notes path.

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
{knowledge_root}/L1-事实与语义/02-📚 知识/{book_slug}-阅读笔记.md
outputs/reading_notes.md
```

Rules:

- Use the knowledge path only when `knowledge_root` exists.
- Do not guess a knowledge base path.
- Do not hard-code personal local paths in code, docs, templates, tests, or output.
- If a temporary note must be moved to `knowledge_root`, delete the temporary duplicate after moving.
- `run_manifest.json`, the scent index, and the completion report must point to the final canonical notes path.

## Directory Responsibilities

### Raw Layer

```text
raw/books/{book_slug}/
├── {book_slug}.epub
└── {book_slug}.md
```

Rules:

- Raw files are read-only after creation.
- `{book_slug}.md` must be retained as the Markdown source of truth for Obsidian backlinks and audits.
- Do not put `reading_notes.md`, `chapters/`, `audit.json`, `run_manifest.json`, or `outputs/` under `raw/`.

### Cache Layer

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
- `run_manifest.json` records all run artifact paths.
- Cache can be kept for debugging or cleaned later.
- Cache is not final Obsidian knowledge content.
- `chapters/` cannot be used as a durable backlink target.

### Canonical Reading Notes

If `knowledge_root` exists:

```text
{knowledge_root}/L1-事实与语义/02-📚 知识/{book_slug}-阅读笔记.md
```

If `knowledge_root` does not exist:

```text
outputs/reading_notes.md
```

This is the only final reading note for the run.

## Workflow Steps

### Step 0: Resolve Knowledge Root And Canonical Output

Resolve `knowledge_root` with the priority above. If no path is known, ask the user. If the user skips archival, proceed with `outputs/reading_notes.md` and report that the note was not archived to a knowledge base.

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

Supported inputs:

- `.md`: copy or normalize into the raw book folder
- `.pdf`: convert with `pymupdf4llm`
- `.epub`, `.docx`, `.html`, `.htm`: convert with `pandoc`, falling back to `pypandoc` if available

For scanned PDFs, run OCR before conversion. OCR is detected but not automated in the core conversion path.

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

- Frontmatter with `aliases`, `tags`, `author`, `source`, `created`, and `scent`.
- A required One-liner HTML component for `全书一句话`.
- A directory section.
- Markdown chapter notes for every in-scope chapter.
- A required Core Framework Grid HTML component under `## 全书核心框架`.
- `## 金句`.

HTML card rules:

- `全书一句话` must use the One-liner HTML component, not a callout.
- `全书核心框架` must use the Core Framework Grid HTML component, not a plain list.
- Process-like frameworks should use the Process Flow HTML component.
- Contrastive ideas should use the Comparison HTML component.
- HTML components must use inline style.
- Do not use external CSS, JavaScript, dark card backgrounds, heavy shadows, or `border-top`.
- Ordinary chapter notes may remain Markdown.

Scent rules:

- Extract 3-5 scent tags after understanding the book.
- Scent tags must come from the book's core methods, problem types, and applicable scenes.
- Avoid generic values such as only `book` or `reading`.
- Write scent tags into reading notes frontmatter.
- Mirror the same scent tags in `run_manifest.json`.
- Report scent tags in the completion report.

Do not create default per-chapter `.notes.md` files, `outputs/notes/`, `outputs/book_summary.md`, `raw/books/{book_slug}/outputs/`, or `knowledge_cards/`.

## Reading Notes Structure

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

## Backlink Rules / 双链回链规则

Every chapter section must include backlinks to the raw source Markdown.

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

Rules:

- Backlink targets must point to raw source Markdown under `raw/books/`.
- Backlink targets must include the chapter heading.
- Do not point backlinks to `.cache/book-learning/{book_slug}/chapters/`.
- `chapters/` is an intermediate artifact and cannot be used as the long-term source target.

## Step 6: Audit Canonical Reading Notes

```bash
python3 .agents/skills/book-learning/scripts/audit_reading_notes.py \
  --toc .cache/book-learning/{book_slug}/toc.json \
  --reading-notes {canonical_notes_path} \
  --raw-source raw/books/{book_slug}/{book_slug}.md \
  --out .cache/book-learning/{book_slug}/audit.json
```

The audit checks frontmatter, chapter coverage, core claims, core conclusions, raw source backlinks, required high-level sections, and HTML / Markdown formatting warnings.

## Step 7: Update Run Manifest And Optional Scent Index

Write:

```text
.cache/book-learning/{book_slug}/run_manifest.json
```

If `knowledge_root` exists, also update the configured scent index path or:

```text
{knowledge_root}/气味索引.md
```

Append an entry:

```markdown
- [[L1-事实与语义/02-📚 知识/{book_slug}-阅读笔记|示例书]]
  - scent: critical-thinking, structured-reading
  - raw: raw/books/{book_slug}/{book_slug}.md
  - manifest: .cache/book-learning/{book_slug}/run_manifest.json
  - status: ready_for_vector_index
```

If no `knowledge_root` exists, do not fail. Set `index_status` to `no_knowledge_root`, set `scent_index` to `null`, and report that the scent index was not updated.

Run manifest example with `knowledge_root`:

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

Fallback manifest fields without `knowledge_root`:

```json
{
  "canonical_notes": "outputs/reading_notes.md",
  "scent_index": null,
  "index_status": "no_knowledge_root"
}
```

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
  - TOC：`.cache/book-learning/示例书/toc.json`
  - 审计：`.cache/book-learning/示例书/audit.json`
  - Manifest：`.cache/book-learning/示例书/run_manifest.json`
- **Scent Tags**：critical-thinking, structured-reading
- **气味索引**：已更新 / 未更新（原因）
- **向量索引**：ready_for_vector_index / no_knowledge_root / not_configured
- **审计**：PASS / FAIL + 原因
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
