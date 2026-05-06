---
name: book-learning
description: Learn an entire book from PDF, EPUB, DOCX, HTML, or Markdown by preserving the table of contents, producing one complete auditable reading note, and optionally extracting method cards, scene triggers, scent vectors, and callable thinking tools after the note is complete. Use when the user asks to study, digest, summarize, create reading notes, or turn book knowledge into cognitive tools, including Chinese requests such as 喂你一本书, 学习这本书, 帮我逐章消化这个 PDF, 读一下这个 EPUB, 逐章做笔记, 生成读书笔记, 整理成阅读笔记, or 提炼成方法卡.
---

# Book Learning

The goal is to turn a whole book into one useful, traceable, content-driven reading note.

A good reading note should be content-driven, not template-driven.

中文说明：读书笔记不是填表。Agent 应该先理解本章内容，再选择合适的表达结构。模板是提示清单，不是强制字段。如果本章没有某类内容，不要硬填。如果本章更适合用流程、对比、机制、场景、案例、推理链，就使用对应结构。

This is not a generic summary, not performative analysis, and not automatic knowledge-card generation. Method cards and callable thinking tools are optional second-stage artifacts after the canonical reading notes are complete and audited.

Chinese trigger examples: `喂你一本书`, `学习这本书`, `帮我逐章消化这个 PDF`, `读一下这个 EPUB`, `逐章做笔记`, `先提取目录树`, `生成读书笔记`, `整理成阅读笔记`.

## Workflow Order

0. Resolve `knowledge_root` / `memory_palace_root`.
0.5. Audit the knowledge directory structure and resolve `{matched_knowledge_subdir}` before deciding the canonical reading notes path.
0.6. Optional Research Context Preflight, only when the user asks and web/API access is available.
0.7. Select one primary reading lens and optional secondary lenses.
1. Store original user files under `raw/books/{book_slug}/` and do not modify them.
2. Convert the source to `raw/books/{book_slug}/{book_slug}.md`.
3. Extract a table of contents to `.cache/book-learning/{book_slug}/toc.json`.
4. Split chapters to `.cache/book-learning/{book_slug}/chapters/` when chapter-sized processing is needed.
5. Read every in-scope chapter and write all notes directly into one canonical reading notes path.
6. Audit the canonical reading notes for coverage, frontmatter, raw source Markdown backlinks, and structural warnings.
7. Write `.cache/book-learning/{book_slug}/run_manifest.json` and update the optional scent index.
8. Report the raw source path, canonical reading notes path, scent tags, research context status, scent index status, audit status, index status, coverage, and key takeaways.

## Path Rules

Resolve `knowledge_root` in this priority order:

1. User-provided `--knowledge-root`.
2. Environment variable `BOOK_LEARNING_KNOWLEDGE_ROOT`.
3. `.book-learning/config.json` or `book-learning.config.json`.
4. Agent context with an explicit `knowledge_root` or `memory_palace_root`.
5. If none exists, ask: `是否要归档到你的知识库？请提供 knowledge_root 路径。若不提供，将只输出到 outputs/reading_notes.md。`
6. If the user skips archival, use `outputs/reading_notes.md`.

If `knowledge_root` exists, audit `{knowledge_root}/L1-事实与语义/02-📚 知识/` and choose `{matched_knowledge_subdir}` from existing direct subdirectories. Canonical notes path is `{knowledge_root}/L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/{book_slug}-阅读笔记.md`. If no confident match exists, ask: `我发现你的知识目录下有多个子目录，这本书应该归档到哪一个？`

Never hard-code a personal knowledge base path.

Directory responsibility:

- `raw` is only for read-only source assets: original file plus converted full Markdown.
- `.cache` is only for system intermediates: TOC, chapter splits, optional research context, audit report, and run manifest.
- `knowledge_root / memory_palace_root` is the user-provided knowledge base root.
- `outputs/reading_notes.md` is used only when the user does not provide a knowledge base path.
- `run_manifest.json` is the callable index entry for text indexes, scent routing, and optional vector indexing.

Do not create default per-chapter `.notes.md` files, `outputs/notes/`, `outputs/book_summary.md`, `raw/books/{book_slug}/outputs/`, or `knowledge_cards/`. Do not keep duplicate `reading_notes.md` files across `outputs/` and a knowledge base.

## Optional Research Context Preflight

Before reading the book, the Agent may gather external context if:

- the user explicitly asks for it
- web access / API access is available
- the user wants broader reception, critique, or background

Possible sources include publisher descriptions, author interviews, reputable reviews, public summaries, academic or professional discussions, and reader reviews with caution.

Rules:

1. External context must not replace reading the original book.
2. External reviews are second-hand interpretations.
3. Do not let popular reviews decide the structure of the notes.
4. Use external context to identify possible themes, controversies, and high-value sections.
5. The final reading notes must still be grounded in the source text.
6. If web/API access is unavailable, skip this step without failing.
7. If used, create `.cache/book-learning/{book_slug}/research_context.md`.
8. Completion report should state whether research context was used.

Use `assets/research_context_template.md` when this step is used. Do not hard-code any search engine, website, or API.

## Reading Lens Selection

Before writing `reading_notes.md`, choose one primary lens and optional secondary lenses.

If the user specifies a lens, follow it. If not, infer from:

- book type
- table of contents
- user goal
- scent tags
- chapter content

If confidence is low, ask the user. Default primary lens is `distillation`.

Available lenses:

- `distillation`: 干货提炼
- `sop`: 执行手册
- `scene-mapping`: 场景映射 / 生产力转化
- `cognitive-refresh`: 认知刷新 / 反常识洞察
- `communication-game`: 沟通博弈 / 决策推演

Reading lenses are not rigid templates. They are ways of seeing the book. The Agent may use different lenses for different chapters.

Write the selected lens to frontmatter:

```yaml
reading_lens:
  primary: cognitive-refresh
  secondary:
    - scene-mapping
    - sop
```

Also mirror it in `run_manifest.json`.

## Chapter Notes

Each chapter must answer: `这章最值得带走的知识是什么？`

Then choose the structure that fits:

- 有定义就写定义。
- 有流程就写流程。
- 有对比就写对比。
- 有机制就写机制。
- 有方法就写 SOP。
- 有博弈就写参与方和变量。
- 没有的内容不要硬填。

Use `assets/chapter_note_template.md` as a guiding question checklist, not as a mandatory field list.

## HTML Components

HTML components are optional visual aids, not mandatory structure.

Use HTML cards when they improve readability:

- One-liner card: recommended for the book's central claim.
- Core Framework Grid: use only when the book has 3-8 parallel frameworks or concepts.
- Process Flow: use for clear step-by-step methods.
- Comparison Card: use for contrastive ideas.

Do not force HTML cards when the book's structure is narrative, progressive, argumentative, mathematical, or not grid-friendly. Plain Markdown is always acceptable when it better preserves the book's logic.

Use `references/html_card_spec.md` for visual rules. Do not use external CSS, JavaScript, dark card backgrounds, heavy shadows, or `border-top`.

## Scent Tags

After reading notes are complete, extract useful `scent` tags from the book's core methods, problem types, and applicable scenes.

Scent supports English, Chinese, or custom tags. The bundled English list is only a recommended vocabulary, not a required enum.

If the note is for human reading, Chinese scent tags may be more intuitive. If the note is for stable program routing, English tags may be more stable. If both are needed, use both fields:

```yaml
scent:
  - 批判性思考
  - 证据检查
scent_en:
  - critical-thinking
  - evidence-checking
```

Mirror scent tags in `run_manifest.json` and include them in the completion report. Missing or generic scent values should produce audit warnings, not hard failure.

## Backlink Rule

Chapter backlinks must point to the converted raw source Markdown:

```text
[[raw/books/{book_slug}/{book_slug}.md#{章节标题}|🔗]]
[[raw/books/{book_slug}/{book_slug}#{章节标题}|🔗]]
```

Do not backlink to `.cache/book-learning/{book_slug}/chapters/`.

## Audit Boundary

The audit verifies coverage, traceability, frontmatter, and obvious structural issues. It does not pretend to judge deep intellectual quality.

Hard checks:

- reading notes file exists
- frontmatter exists and includes base source metadata
- in-scope chapter coverage passes
- each covered chapter has at least one valid raw source backlink

Soft warnings:

- sections are very short
- repeated empty template phrases
- too many identical headings
- no evidence / examples found
- rigid structure repeated across chapters
- formatting issues
- HTML cards may be overused
- scent missing or too generic
- research context is not clearly separated from source-grounded reading

Do not finish until hard checks pass. Warnings should be reported and improved when useful, but warnings do not automatically fail the run.

## Cognitive Toolbox Extension

After the reading notes are complete, the Agent may extract 3-5 high-quality method cards from the book if the user asks.

Rules:

- Do not let method cards replace the canonical reading notes.
- Do not restore old automatic knowledge-card generation.
- Generate method cards only after the reading note passes audit.
- Method cards must be usable in real tasks.

Use bundled resources:

- `references/workflow.md` for the detailed workflow.
- `references/output_schema.md` before writing TOC files, reading notes, manifests, or audit reports.
- `references/reading_modes.md` before choosing reading lenses.
- `references/html_card_spec.md` when HTML cards improve readability.
- `references/scent_vector_routing.md` when assigning scent values.
- `references/knowledge_invocation.md` before using method cards in user tasks.
- `assets/chapter_note_template.md` as the chapter distillation prompt.
- `assets/reading_mode_templates.md` for compact optional lens snippets.
- `assets/research_context_template.md` for optional research context.
- `scripts/check_tools.py`, `scripts/convert_to_md.py`, `scripts/extract_toc.py`, `scripts/split_chapters.py`, and `scripts/audit_reading_notes.py` for deterministic structure handling.

Do not commit real books, PDFs, EPUBs, OCR output, private files, or generated knowledge bases.
