---
name: book-learning
description: Learn an entire book from PDF, EPUB, DOCX, HTML, or Markdown by preserving the table of contents, producing one complete auditable reading note, and optionally extracting method cards, scene triggers, scent vectors, and callable thinking tools after the note is complete. Use when the user asks to study, digest, summarize, create reading notes, or turn book knowledge into cognitive tools, including Chinese requests such as 喂你一本书, 学习这本书, 帮我逐章消化这个 PDF, 读一下这个 EPUB, 逐章做笔记, 生成读书笔记, 整理成阅读笔记, or 提炼成方法卡.
---

# Book Learning

The goal is to distill the book into useful reading notes: definitions, frameworks, conclusions, and supporting evidence. The output should help someone who has not read the book quickly understand what the book actually says.

This is not a generic summary, not performative analysis, and not automatic knowledge-card generation.

Second-stage goal: From book notes to callable thinking tools. After `outputs/reading_notes.md` is complete and audited, the Agent may extract a cognitive toolbox so book knowledge can be invoked in real tasks.

Chinese trigger examples: `喂你一本书`, `学习这本书`, `帮我逐章消化这个 PDF`, `读一下这个 EPUB`, `逐章做笔记`, `先提取目录树`, `生成读书笔记`, `整理成阅读笔记`.

Follow this order strictly:

1. Store original user files under `raw/books/` and do not modify them.
2. Convert the source to Markdown if needed.
3. Extract a table of contents with heading levels and line ranges.
4. Split the Markdown into chapters from the TOC.
5. Read every in-scope chapter and write all chapter notes into one `outputs/reading_notes.md`.
6. Audit `outputs/reading_notes.md` for chapter coverage, core definition / claim, core conclusion, backlinks, and required sections.
7. Report the final raw source path, reading note path, audit status, coverage, and key takeaways.

Never skip chapters. If one chapter is missing, re-audit the whole TOC instead of patching only the visible gap.

If a skipped chapter is found, do not only repair that chapter. Re-scan the TOC and all chapter states, then check from the failed chapter through the final chapter for consecutive omissions or structural shifts.

Do not create default per-chapter `.notes.md` files, `outputs/notes/`, `outputs/book_summary.md`, or `knowledge_cards/`. Knowledge cards are optional only when the user explicitly asks for them after reading.

Each chapter section should focus on:

- Core Definition / Claim
- Key Framework
- Core Conclusion
- Supporting Evidence
- Source Backlink

Do not finish until all in-scope chapters are represented in `outputs/reading_notes.md` and the reading-note audit passes. For Chinese requests, report the output paths and learning summary in Chinese.

## Cognitive Toolbox Extension

After the reading notes are complete, the Agent may extract 3-5 high-quality method cards from the book.

A method card is not a summary. It is a callable thinking tool for real tasks.

Generate method cards only after:

- `outputs/reading_notes.md` is complete.
- Chapter coverage audit passes.
- The book's core definitions, frameworks, conclusions, and evidence are understood.

Default output remains `outputs/reading_notes.md`.

Method cards, scene indexes, scent vectors, and invocation reports are second-stage knowledge invocation artifacts.

Rules:

- Do not let method cards replace `outputs/reading_notes.md`.
- Do not restore old automatic knowledge-card generation.
- Generate method cards only after the reading note passes audit.
- Prefer 3-5 strong method cards per book.
- Method cards must be usable in real tasks.
- Method cards are not reading summaries.

Use bundled resources as needed:

- Read `references/workflow.md` for the detailed end-to-end workflow and failure handling.
- Read `references/output_schema.md` before writing TOC files, reading notes, or audit reports.
- Read `references/html_card_spec.md` before adding inline HTML cards to reading notes.
- Read `references/method_card_design.md` before extracting method cards.
- Read `references/scene_trigger_index.md` when building or updating scene triggers.
- Read `references/scent_vector_routing.md` when assigning optional scent values.
- Read `references/knowledge_invocation.md` before using method cards in user tasks.
- Use `scripts/check_tools.py` to detect optional converters.
- Use `scripts/convert_to_md.py` for PDF, EPUB, DOCX, and HTML conversion.
- Use `scripts/extract_toc.py`, `scripts/split_chapters.py`, and `scripts/audit_reading_notes.py` for deterministic structure handling.
- Use `assets/chapter_note_template.md` as the compact per-section format inside `outputs/reading_notes.md`.
- Use `assets/method_card_template.md`, `assets/scene_index_template.md`, `assets/scent_vector_template.md`, and `assets/invocation_report_template.md` for second-stage artifacts.

Do not commit real books, PDFs, EPUBs, OCR output, private files, or generated knowledge bases.
