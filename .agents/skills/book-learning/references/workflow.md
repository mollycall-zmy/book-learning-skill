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

### AI Analysis Layer

After SQ3R, every chapter note must include an `AI Analysis / AI 分析` section. This section is required. It is the Agent's own analysis, not only extracted text or a restatement of the source.

AI Analysis must include:

1. Cross-reference / 跨界关联
   - Connect the chapter's ideas to other books, fields, frameworks, or general knowledge.
   - Use broad transferable knowledge, not user-specific company or personal context.
2. Applicability boundary / 适用边界
   - State when the idea works, when it may fail, and what assumptions it depends on.
3. Critique / 批判性思考
   - Identify blind spots, survivorship bias, sample-selection bias, logic leaps, over-attribution, counterexamples, or alternative explanations.
4. One-sentence distillation / 一句话提炼
   - Write the one sentence that would teach the chapter's most important idea to someone who has not read the book.

Do not turn AI Analysis into company-specific consulting. Avoid claims like "this means X for the user's company." Keep the analysis general, transferable, and reusable.

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

## Consolidated Reading Notes

In addition to per-chapter notes, create a consolidated reading note:

```text
outputs/reading_notes.md
```

`outputs/reading_notes.md` is the primary reading output. Per-chapter notes are audit and traceability outputs.

Required structure:

```markdown
# 《书名》阅读笔记

## 大目录

| 章节 | 核心主张 | 页数/行数 |
|------|----------|-----------|
| 第一章 xxx | 一句话概括 | L1-L100 |
| 第二章 xxx | 一句话概括 | L101-L200 |

## 分章节笔记

### 第一章 xxx

#### 核心主张

作者在这一章的主要论点是什么？

#### 关键要点

- 要点 1：xxx（原文依据：xxx）
- 要点 2：xxx（原文依据：xxx）
- 要点 3：xxx（原文依据：xxx）

#### AI 分析

- 跨界关联：xxx
- 适用边界：xxx
- 批判性思考：xxx
- 一句话总结：xxx

### 第二章 xxx

同上格式。

## 全书核心框架

从所有章节中提炼 3-7 个核心框架、模型或方法论。

## 金句集

摘录最有价值的 10-20 句话，并标注来源章节。
```

Rules:

- `outputs/reading_notes.md` must cover every in-scope chapter.
- For books with 100+ chapters, related chapters may be grouped, but every chapter must still be listed with at least one core claim.
- If only part of the book was studied, state the covered range at the top of the file.

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

## Content Quality Check

After structural audit passes, verify content quality.

The Agent must check:

1. Each chapter note contains `AI Analysis` or `AI 分析`.
2. Each chapter note contains core claims, key points, and evidence / cases / examples.
3. `outputs/reading_notes.md` exists.
4. `outputs/reading_notes.md` covers all in-scope chapters.
5. `outputs/reading_notes.md` contains `全书核心框架`.
6. `全书核心框架` contains at least 3 items unless the source is very short.
7. Chapter notes that are only headings, templates, empty shells, or too short are marked incomplete.

Do not proceed to full-book summary or knowledge cards if any in-scope chapter fails the content quality check.

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

1. Book overview
   - Title
   - Author if available
   - Chapter count
   - Total lines/pages if available
2. Coverage
   - Which chapters were studied
   - Whether this was full-book learning or subset learning
3. Key takeaways
   - 3-5 most important insights from the book
   - These must be Agent synthesis, not only chapter titles
4. Output files
   - Consolidated reading notes path + line count
   - Per-chapter notes count
   - Knowledge cards count + list
   - Audit result path and pass/fail status
5. Skipped chapters
   - List skipped chapters and reasons
   - If none, say none
6. Archiving status
   - Whether files were saved to `raw/books`, `outputs`, `knowledge_cards`, or an external knowledge base

Example:

```text
📚 学习完成：《书名》

📖 概览：作者 | X 章 | X 万字

✅ 覆盖范围：全书 / 第 X 章至第 Y 章

📝 核心收获：
1. xxx
2. xxx
3. xxx

📁 文件：
- 阅读笔记：outputs/reading_notes.md（X 行）
- 章节笔记：X 个，位于 outputs/notes/
- 全书摘要：outputs/book_summary.md
- 知识卡片：X 张
  - `knowledge_cards/001-xxx.md`
  - `knowledge_cards/002-xxx.md`
- 审计报告：outputs/audit.json，通过 / 未通过

⏭️ 跳过章节：无 / xxx（原因）

📦 归档状态：已保存到 xxx
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
