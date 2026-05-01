# Workflow

## Purpose

Turn a whole book into two durable artifacts:

1. Raw source archive: `raw/books/{book-title}.md`
2. Complete reading note: `outputs/reading_notes.md`

If the user provides a knowledge base or Obsidian path, the final note may be archived as:

```text
L1-事实与语义/02-📚 知识/{书名}-阅读笔记.md
```

Do not hard-code a user's knowledge base path in the open-source workflow. `outputs/reading_notes.md` is the default output, and users may move or configure the final destination.

## Step 0: Receive And Convert

Place the original file under `raw/books/` and treat it as read-only.

Supported inputs:

- `.md`: use directly
- `.pdf`: convert with `pymupdf4llm`
- `.epub`, `.docx`, `.html`, `.htm`: convert with `pandoc`, falling back to `pypandoc` if available

For scanned PDFs, run OCR before conversion. OCR is detected but not automated in the core conversion path.

## Step 1: Extract TOC

Run `extract_toc.py` on the Markdown file. The output must include:

- Stable chapter id
- Heading title
- Heading level
- Start line
- End line

By default, TOC extraction keeps main chapters and filters out likely non-chapter headings:

- TOC headings containing `目录`
- Sidebar / box headings starting with `方框`, `Box`, or `Sidebar`
- Heading level deeper than `--max-level 3`
- Sections shorter than `--min-lines 15`
- Empty or decorative headings

Adjust with:

```bash
python3 .agents/skills/book-learning/scripts/extract_toc.py outputs/book.md --out outputs/toc.json --min-lines 15 --max-level 3
```

Use `--include-sidebars` only when the user explicitly wants sidebar / box entries preserved as TOC items.

If the Markdown has no headings, stop and ask for a chapter structure or create a proposed structure for user review.

## Step 2: Review Target Location

Default output is:

```text
outputs/reading_notes.md
```

If the user provides a knowledge base path, archive the final reading note there after local output is complete. Example:

```text
L1-事实与语义/02-📚 知识/{书名}-阅读笔记.md
```

## Step 3: Split For Processing

Run `split_chapters.py` using the TOC JSON if chapter-sized processing is needed. Chapter files are intermediate processing artifacts, not final reading outputs.

Use deterministic filenames based on chapter id and a slugified title.

## Step 4: Chapter Distillation

Read every in-scope chapter, but write concise, high-density notes into one consolidated file:

```text
outputs/reading_notes.md
```

Do not create default per-chapter `.notes.md` files. All chapters must appear in one reading note.

Each chapter note should help a reader who has not read the book quickly understand what the book says.

Focus on:

1. Core Definition / Claim
   - What is the key idea of this chapter?
   - What does the author define, assert, or clarify?
   - Use 1-2 sentences.
2. Key Framework
   - What model, method, classification, process, or structure does the chapter provide?
   - Use bullets or a small table.
   - This is the highest-value part of the reading note.
   - If the chapter has no real framework, omit this part instead of inventing one.
3. Core Conclusion
   - What is the author's most important conclusion in this chapter?
   - Use 1-2 sentences.
4. Supporting Evidence
   - What is the strongest evidence behind the conclusion?
   - Keep only the strongest 1-2 items.
   - Evidence may include research, data, cases, named examples, or a clear argument chain.
   - Do not list every story.
5. Source Backlink
   - Each chapter note should include at least one backlink to the raw source.

Use this structure:

```markdown
---
aliases: [示例书]
tags: [书籍, 分类]
author: 示例作者
source: "[[raw/books/示例书]]"
created: YYYY-MM-DD
---

# 📚 《示例书》— 示例作者

> [!info] 全书一句话
> 用一句话概括本书核心主张。

## 目录

- [[#第一章 示例章节]]
- [[#第二章 示例章节]]

## 第一章 示例章节

**核心定义/主张**：用 1-2 句话说明本章最核心的观点。

**关键框架**：

- 框架 / 方法 / 分类 / 模型 1：说明其结构和含义。
- 框架 / 方法 / 分类 / 模型 2：说明其结构和含义。

**核心结论**：用 1-2 句话写出作者在本章得出的最重要结论。

**支撑证据**：

- 证据 1：最有力的数据、研究、案例或原文论证。
- 证据 2：如果有第二个强证据，再补充；不要罗列弱故事。

**来源回链**：[[raw/books/示例书.md#第一章 示例章节]]

## 第二章 示例章节

同上。

## 全书核心框架

1. 框架 1
2. 框架 2
3. 框架 3

## 金句

> 1. “原文金句。”（第 X 章）
```

Rules:

- Every in-scope chapter must appear in `outputs/reading_notes.md`.
- Remove storytelling noise and conversational filler.
- Do not copy long passages from the book.
- Do not turn anecdotes into key points unless the underlying concept is extracted.
- Do not fill template fields mechanically.
- If a field is not applicable, omit it.
- Notes should be readable, concise, and dense.
- Default target length: 15-25 lines per chapter.
- Long books may be grouped by part, volume, or theme, but no chapter may be omitted.
- If a chapter is intentionally not expanded, mark the reason explicitly.
- If the author's argument has an obvious dispute, boundary, or counterexample, mention it briefly after the conclusion or evidence. Do not create a fixed analysis section for every chapter.

## Backlink Rule

Key chapter points in `outputs/reading_notes.md` must include Obsidian-style backlinks to the raw source:

```text
[[raw/books/示例书.md#章节标题]]
```

Rules:

- Each chapter must include at least one backlink to the original chapter.
- Prefer backlinks near key concepts, important quotes, and named cases.
- Do not link every sentence; avoid noisy notes.
- If the original heading is not a stable anchor, use the closest chapter heading.
- If the user does not use Obsidian, keep this format as a readable source marker.

Purpose:

- Make source navigation possible.
- Preserve source traceability.
- Prevent reading notes from drifting away from the original text.

## Important Detail Retention

Do not compress these details into generic summary language:

- Definitions and new terms
- Frameworks and steps
- Numbers and data
- Named cases
- Tables and figures
- Contrasts and comparisons
- Causal chains
- Author conclusions
- Conditions and exceptions
- Counterexamples
- Counterintuitive claims
- Ideas repeated across chapters

### Sidebar / Box Content Handling

Some books contain sidebar, box, appendix-like fragments, or very short sub-sections such as `方框3.1`.

These items should not usually become standalone chapters in `outputs/reading_notes.md`.

Rules:

1. Do not create independent reading note sections for sidebars / boxes by default.
2. Integrate important sidebar / box content into the nearest relevant main chapter.
3. If a sidebar contains a model, framework, matrix, table, or important example, summarize it under the corresponding chapter's `关键要点` or `补充说明`.
4. Keep source traceability with backlinks, for example: `[[raw/books/示例书.md#方框3.1 标题]]`.
5. If a sidebar is irrelevant, repetitive, or purely decorative, it may be skipped, but the Agent should not treat it as a missing chapter.
6. If the user explicitly asks to preserve all sidebars, include them as sub-bullets under the related chapter, not as top-level chapters.

## Omission Repair Rule

When an Agent finds that a chapter is missing, skipped, lacks notes, or has abnormal boundaries, it must not only repair the visible chapter. Run a full coverage check:

- Re-read `toc.json` or the current TOC tree.
- Check that every in-scope chapter appears in `outputs/reading_notes.md`.
- Continue checking from the failed chapter to the final chapter.
- Output a repair note describing what was missing and what changed.
- Re-run the audit after repair.

Example: if Chapter 2 was skipped, also check Chapter 3 through the final chapter instead of only filling Chapter 2.

## Content Quality Check

After structure extraction and reading-note writing, audit `outputs/reading_notes.md`.

Check:

1. `outputs/reading_notes.md` exists.
2. Frontmatter includes `aliases`, `tags`, `author`, `source`, and `created`.
3. All in-scope TOC chapter titles appear in the note.
4. Every chapter has `核心定义/主张` or `核心主张`.
5. Every chapter has `核心结论`.
6. Every chapter has at least one backlink like `[[raw/books/示例书.md#章节标题]]`.
7. The note contains `全书核心框架`.
8. The note contains `金句`.

Do not proceed to completion if `audit_reading_notes.py` fails.

## Optional Knowledge Cards

Knowledge cards are not default reading-stage artifacts.

Default output is only:

```text
raw/books/{书名}.md
outputs/reading_notes.md
```

If the user explicitly asks to generate knowledge cards, treat that as a separate optional task after reading. The user should decide which ideas are worth splitting into cards during archival or review.

## Step 9: Completion Report

Use this concise report:

```markdown
### 学习完成报告

- **书名**：《书名》
- **规模**：X 万字，Y 个章节
- **核心收获**：
  1. xxx
  2. xxx
  3. xxx
- **文件**：
  - 原文：`raw/books/示例书.md`
  - 笔记：`outputs/reading_notes.md`
  - 如果已归档到知识库：`L1-事实与语义/02-📚 知识/书名-阅读笔记.md`
- **审计**：PASS / FAIL + 原因
```

Do not report knowledge card counts, per-chapter note counts, or `outputs/notes/`.

If only part of the book was studied, explicitly write:

```text
本次只覆盖第 X 章至第 Y 章，未覆盖全书。
```

## Capability Boundaries

- Large books should still be processed chapter by chapter internally.
- The final reading output remains one file.
- Scanned PDFs depend on OCR quality.
- Automatic card generation is outside the default workflow.

## Pitfalls

- Do not confuse chapter split files with final notes.
- Do not mark a chapter covered only because its heading exists.
- Do not hide the book's definitions, frameworks, conclusions, or evidence behind generic commentary.
- Do not omit backlinks.
- Do not create many default `.notes.md` files unless the user explicitly asks for that style.

## Failure Handling

- Missing converter: run `check_tools.py`, then tell the user which tool is missing.
- Bad TOC: inspect Markdown headings and rerun extraction after improving heading structure.
- Huge book: process chapter batches, but keep one global TOC and one final `outputs/reading_notes.md`.
- OCR quality issue: ask for a better scan or OCR pass before learning.
