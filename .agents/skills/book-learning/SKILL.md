---
name: book-learning
description: Learn an entire book from PDF, EPUB, DOCX, HTML, or Markdown by preserving the table of contents, producing one complete auditable reading note, and optionally extracting method cards, scene triggers, scent vectors, and callable thinking tools after the note is complete. Use when the user asks to study, digest, summarize, create reading notes, or turn book knowledge into cognitive tools, including Chinese requests such as 喂你一本书, 学习这本书, 帮我逐章消化这个 PDF, 读一下这个 EPUB, 逐章做笔记, 生成读书笔记, 整理成阅读笔记, or 提炼成方法卡.
---

# Book Learning

The goal is to distill the book into useful reading notes: definitions, frameworks, conclusions, and supporting evidence. The output should help someone who has not read the book quickly understand what the book actually says.

This is not a generic summary, not performative analysis, and not automatic knowledge-card generation.

Second-stage goal: From book notes to callable thinking tools. After the canonical reading notes are complete and audited, the Agent may extract a cognitive toolbox so book knowledge can be invoked in real tasks.

Chinese trigger examples: `喂你一本书`, `学习这本书`, `帮我逐章消化这个 PDF`, `读一下这个 EPUB`, `逐章做笔记`, `先提取目录树`, `生成读书笔记`, `整理成阅读笔记`.

Follow this order strictly:

0. Resolve `knowledge_root` / `memory_palace_root` and the canonical reading notes path.
1. Store original user files under `raw/books/{book_slug}/` and do not modify them.
2. Convert the source to `raw/books/{book_slug}/{book_slug}.md`.
3. Extract a table of contents to `.cache/book-learning/{book_slug}/toc.json`.
4. Split chapters to `.cache/book-learning/{book_slug}/chapters/` when chapter-sized processing is needed.
5. Read every in-scope chapter and write all chapter notes directly into one canonical reading notes path.
6. Audit the canonical reading notes for chapter coverage, core definition / claim, core conclusion, raw source Markdown backlinks, scent frontmatter, and required sections.
7. Write `.cache/book-learning/{book_slug}/run_manifest.json` and update the optional scent index.
8. Report the raw source path, canonical reading notes path, scent tags, scent index status, audit status, index status, coverage, and key takeaways.

Resolve `knowledge_root` in this priority order:

1. User-provided `--knowledge-root`.
2. Environment variable `BOOK_LEARNING_KNOWLEDGE_ROOT`.
3. `.book-learning/config.json` or `book-learning.config.json`.
4. Agent context with an explicit `knowledge_root` or `memory_palace_root`.
5. If none exists, ask: "是否要归档到你的知识库？请提供 knowledge_root 路径。若不提供，将只输出到 outputs/reading_notes.md。"
6. If the user skips archival, use `outputs/reading_notes.md`.

If `knowledge_root` exists, canonical notes path is `{knowledge_root}/L1-事实与语义/02-📚 知识/{book_slug}-阅读笔记.md`. Otherwise it is `outputs/reading_notes.md`. Never hard-code a personal knowledge base path.

Directory responsibility:

- `raw` is only for read-only source assets: original file plus converted full Markdown.
- `.cache` is only for system intermediates: TOC, chapter splits, audit report, and run manifest.
- `knowledge_root / memory_palace_root` is the user-provided knowledge base root.
- `L1 / knowledge` is the only final knowledge output when `knowledge_root` exists.
- `outputs/reading_notes.md` is used only when the user does not provide a knowledge base path.
- `run_manifest.json` is the callable index entry for text indexes, scent routing, and optional vector indexing.

Never skip chapters. If one chapter is missing, re-audit the whole TOC instead of patching only the visible gap.

If a skipped chapter is found, do not only repair that chapter. Re-scan the TOC and all chapter states, then check from the failed chapter through the final chapter for consecutive omissions or structural shifts.

Do not create default per-chapter `.notes.md` files, `outputs/notes/`, `outputs/book_summary.md`, `raw/books/{book_slug}/outputs/`, or `knowledge_cards/`. Knowledge cards are optional only when the user explicitly asks for them after reading.

Each chapter section should focus on:

- Core Definition / Claim
- Key Framework
- Core Conclusion
- Supporting Evidence
- Source Backlink

When generating `reading_notes.md`, the Agent MUST use the bundled HTML card components for high-level visual sections:

- The book one-liner MUST use the One-liner HTML component.
- The `全书核心框架` section MUST use the Core Framework Grid HTML component.
- Process-like frameworks SHOULD use the Process Flow HTML component.
- Contrastive ideas SHOULD use the Comparison HTML component.

生成阅读笔记时必须使用 HTML 卡片组件：

- “全书一句话”必须使用 One-liner HTML 卡片；
- “全书核心框架”必须使用 Core Framework Grid；
- 流程型方法优先使用 Process Flow；
- 对比型内容优先使用 Comparison；
- 普通章节内容仍可使用 Markdown。

Use `references/html_card_spec.md` and `assets/chapter_note_template.md` for the exact inline HTML components. Do not use external CSS, JavaScript, dark card backgrounds, heavy shadows, or `border-top`.

After reading notes are complete, extract 3-5 useful `scent` tags from the book's core methods, problem types, and applicable scenes. Write them into reading notes frontmatter, mirror them in `run_manifest.json`, and include them in the completion report.

Do not finish until all in-scope chapters are represented in the canonical reading notes, scent frontmatter exists, raw source Markdown backlinks pass audit, and the reading-note audit passes. For Chinese requests, report the output paths and learning summary in Chinese.

Backlink rule: chapter backlinks must point to the converted raw source Markdown, using `[[raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]` or the Obsidian extensionless form `[[raw/books/{book_slug}/{book_slug}#{章节标题}|🔗]]`. Do not backlink to `.cache/book-learning/{book_slug}/chapters/`.

## Cognitive Toolbox Extension

After the reading notes are complete, the Agent may extract 3-5 high-quality method cards from the book.

A method card is not a summary. It is a callable thinking tool for real tasks.

Generate method cards only after:

- The canonical reading notes are complete.
- Chapter coverage audit passes.
- The book's core definitions, frameworks, conclusions, and evidence are understood.

Default output remains `outputs/reading_notes.md` only when no knowledge base path is provided.

Method cards, scene indexes, scent vectors, and invocation reports are second-stage knowledge invocation artifacts.

Rules:

- Do not let method cards replace the canonical reading notes.
- Do not restore old automatic knowledge-card generation.
- Generate method cards only after the reading note passes audit.
- Prefer 3-5 strong method cards per book.
- Method cards must be usable in real tasks.
- Method cards are not reading summaries.

Use bundled resources:

- Read `references/workflow.md` for the detailed end-to-end workflow and failure handling.
- Read `references/output_schema.md` before writing TOC files, reading notes, or audit reports.
- Read `references/html_card_spec.md` before writing reading notes. High-level HTML cards are mandatory.
- Read `references/method_card_design.md` before extracting method cards.
- Read `references/scene_trigger_index.md` when building or updating scene triggers.
- Read `references/scent_vector_routing.md` when assigning required reading-note scent values.
- Read `references/knowledge_invocation.md` before using method cards in user tasks.
- Use `scripts/check_tools.py` to detect optional converters.
- Use `scripts/convert_to_md.py` for PDF, EPUB, DOCX, and HTML conversion.
- Use `scripts/extract_toc.py`, `scripts/split_chapters.py`, and `scripts/audit_reading_notes.py` for deterministic structure handling.
- Use `assets/chapter_note_template.md` as the compact per-section format inside the canonical reading notes.
- Use `assets/method_card_template.md`, `assets/scene_index_template.md`, `assets/scent_vector_template.md`, and `assets/invocation_report_template.md` for second-stage artifacts.

Do not commit real books, PDFs, EPUBs, OCR output, private files, or generated knowledge bases.
