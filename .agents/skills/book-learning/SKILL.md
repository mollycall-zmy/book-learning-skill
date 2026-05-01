---
name: book-learning
description: Learn an entire book from PDF, EPUB, DOCX, HTML, or Markdown by preserving the table of contents, splitting chapters, producing chapter-by-chapter SQ3R notes, auditing omissions, and generating traceable atomic knowledge cards. Use when the user asks to study, digest, summarize, or build a knowledge base from a whole book or long manuscript, including Chinese requests such as 喂你一本书, 学习这本书, 帮我逐章消化这个 PDF, 读一下这个 EPUB, 把这本书整理成知识卡片, 逐章做笔记, 提取知识卡片, 检查章节遗漏, or 建立知识库.
---

# Book Learning

Chinese trigger examples: `喂你一本书`, `学习这本书`, `帮我逐章消化这个 PDF`, `读一下这个 EPUB`, `把这本书整理成知识卡片`, `逐章做笔记`, `先提取目录树`, `生成原子知识卡片`, `检查章节有没有遗漏`.

Follow this order strictly:

1. Store original user files under `raw/books/` and do not modify them.
2. Convert the source to Markdown if needed.
3. Extract a table of contents with heading levels and line ranges.
4. Split the Markdown into chapters from the TOC.
5. Read every chapter and create structured SQ3R notes.
6. Audit TOC, chapter files, and notes for omissions.
7. Only after a clean audit, write the full-book summary and atomic knowledge cards.

Never skip chapters. If one chapter is missing, re-audit the whole TOC instead of patching only the visible gap.

If a skipped chapter is found, do not only repair that chapter. Re-scan the TOC and all chapter states, then check from the failed chapter through the final chapter for consecutive omissions or structural shifts.

Use bundled resources as needed:

- Read `references/workflow.md` for the detailed end-to-end workflow and failure handling.
- Read `references/output_schema.md` before writing TOC files, chapter notes, summaries, audit reports, or card indexes.
- Read `references/card_rules.md` before creating atomic knowledge cards.
- Use `scripts/check_tools.py` to detect optional converters.
- Use `scripts/convert_to_md.py` for PDF, EPUB, DOCX, and HTML conversion.
- Use `scripts/extract_toc.py`, `scripts/split_chapters.py`, and `scripts/audit_chapters.py` for deterministic structure handling.
- Use `assets/` templates for notes, summaries, cards, TOCs, and audit reports.

Do not commit real books, PDFs, EPUBs, OCR output, private files, or generated knowledge bases.
