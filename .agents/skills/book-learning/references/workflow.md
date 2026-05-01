# Workflow

## Purpose

Turn a whole book into reliable learning artifacts:

1. Preserved structure
2. Complete chapter coverage
3. Chapter-level understanding
4. Traceable summaries
5. Atomic knowledge cards

## Step 0: Receive And Convert

Place the original file under `raw/books/` and treat it as read-only.

Supported MVP inputs:

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

If the Markdown has no headings, stop and ask for a chapter structure or create a proposed structure for user review.

## Step 2: Review Target Categories

Before creating cards, inspect the existing `knowledge_base/` structure if present. Reuse existing categories when possible.

## Step 3: Split Chapters

Run `split_chapters.py` using the TOC JSON. Each heading range becomes one Markdown file.

Use deterministic filenames based on chapter id and a slugified title.

## Step 4: Read Chapter By Chapter

For each chapter, apply SQ3R:

- Survey: identify the chapter structure and central topic
- Question: write the questions the chapter tries to answer
- Read: extract claims, definitions, evidence, examples, data, and caveats
- Recite: restate the argument in your own words
- Review: note implications, weak points, and links to other chapters

Use `assets/chapter_note_template.md`.

Must preserve these detail types in chapter notes:

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

Do not compress these details into generic summary language. Keep enough source-specific detail for later audit, synthesis, and card extraction.

## Step 5: Preserve Details

Do not drop definitions, data, cases, constraints, exceptions, counterexamples, or surprising claims. These details often become the most useful cards.

## Step 6: Layer Summaries

Move from source to abstraction:

- L0: source Markdown
- L1: chapter excerpts or evidence notes
- L2: chapter notes
- L3: full-book summary
- L4: atomic knowledge cards

Never create L3 or L4 before L2 exists for every chapter.

## Step 7: Audit Omissions

Run `audit_chapters.py` before summarizing the whole book. A clean audit means:

- Every TOC entry has a chapter file
- Every chapter file maps to a TOC entry
- Every required chapter has a note file

Chapter audit is stricter than TOC coverage or chapter-file existence. Every chapter must enter one of these valid states:

1. Read + has chapter notes
2. Read + explicitly marked with the reason it will not be expanded

Invalid states:

- Unread + covered by TOC
- Unread + chapter file exists
- Unread + only mentioned in the full-book summary
- No notes + direct knowledge-card generation

Only create the full-book summary and knowledge cards after every chapter has a valid state.

If any chapter is missing, scan the whole TOC again.

## Omission Repair Rule

When an Agent finds that a chapter is missing, skipped, lacks notes, or has abnormal boundaries, it must not only repair the visible chapter. Run a full chapter coverage check:

- Re-read `toc.json` or the current TOC tree
- Check that all chapter files exist
- Check that all chapters have notes or an explicit non-expansion reason
- Continue checking from the failed chapter to the final chapter
- Output a repair note describing what was missing and what changed
- Re-run the audit after repair

Example: if Chapter 2 was skipped, also check Chapter 3 through the final chapter instead of only filling Chapter 2.

## Content Audit

After structural audit passes, verify that notes are not empty shells.

A chapter note is considered complete only if it contains at least:

- Core Questions
- Main Claims
- Evidence / Cases / Examples
- Important Details
- Source Chapter

A chapter note is incomplete if:

- It only contains headings with no substantial content
- It only repeats the chapter title
- It has no evidence, cases, examples, data, or argument chain
- It was generated without actually reading the chapter
- It is marked as covered only because the chapter file exists

Do not proceed to the full-book summary or knowledge cards if any chapter note is incomplete.

内容性审计不是检查“有没有文件”，而是检查“有没有真正学过”。如果某章笔记只是空壳、标题、模板占位、泛泛摘要，必须标记为 incomplete，并重新阅读该章。

## Completion Criteria

Before generating final knowledge cards, confirm all of the following:

- Every chapter has been read, not just split into a file.
- Chapter notes exist for every chapter that is in scope.
- Each chapter note contains meaningful content, not only headings.
- The full-book summary references content from all major sections, not only the first few chapters.
- Knowledge cards are generated from complete understanding, not from partial reading.
- If only a subset of chapters was studied because the user explicitly requested it, clearly mark the scope.

生成知识卡片前必须确认：

- 每一章都已经实际阅读，不只是存在章节文件。
- 每一章都有有效笔记。
- 全书总结覆盖所有主要章节。
- 知识卡片必须来自完整理解，而不是只读前几章后的局部总结。

If the user explicitly asks to study only part of the book, generate cards only for that range and state:

```text
以下卡片仅覆盖第 X 章至第 Y 章，未覆盖全书。
```

## Step 8: Create Knowledge Cards

Read `references/card_rules.md` first. Each card must contain exactly one idea and cite its source chapter.

## Step 9: Completion Report

After all artifacts are created, report to the user:

1. Raw source location: where the original or converted source file is stored.
2. Chapter coverage: which chapters were covered.
3. Chapter notes: how many notes were created and where they are stored.
4. Full-book summary: path to the summary file.
5. Knowledge cards: list each card with its path.
6. Audit result: whether structural and content audits passed.
7. Skipped chapters: list any skipped chapters and explain why.
8. Index updates: if any index was updated, mention the path.

Example:

```text
学习完成！归档路径如下：

- 原文：`raw/books/书名.md`
- 目录树：`outputs/toc.json`
- 章节拆分：`outputs/chapters/`
- 章节笔记：共 12 篇，位于 `outputs/notes/`
- 全书摘要：`outputs/book_summary.md`
- 知识卡片：共 8 张，位于 `knowledge_cards/`
  - `knowledge_cards/001-xxx.md`
  - `knowledge_cards/002-xxx.md`
- 审计结果：结构性审计通过，内容性审计通过
- 跳过章节：无
```

If only part of the book was studied, explicitly write:

```text
本次只覆盖第 X 章至第 Y 章，未覆盖全书。
```

## Failure Handling

- Missing converter: run `check_tools.py`, then tell the user which tool is missing.
- Bad TOC: inspect Markdown headings and rerun extraction after improving heading structure.
- Huge book: process chapter batches, but keep one global TOC and audit report.
- OCR quality issue: ask for a better scan or OCR pass before learning.
