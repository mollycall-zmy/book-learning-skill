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
{knowledge_root}/L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/{book_slug}-阅读笔记.md
outputs/reading_notes.md
```

Only one canonical notes path may exist per run. `{matched_knowledge_subdir}` is not fixed. It must be obtained through knowledge directory audit, user configuration, Agent context, or user confirmation.

## Output Map

```text
raw/books/{book_slug}/{book_slug}.{ext}
raw/books/{book_slug}/{book_slug}.md
.cache/book-learning/{book_slug}/toc.json
.cache/book-learning/{book_slug}/chapters/
.cache/book-learning/{book_slug}/research_context.md
.cache/book-learning/{book_slug}/audit.json
.cache/book-learning/{book_slug}/run_manifest.json
{canonical_notes_path}
```

Rules:

- Raw stores only source assets.
- Cache stores only processing artifacts.
- Reading notes are written only to `canonical_notes_path`.
- Do not create or preserve duplicate reading notes under `raw/`, `raw/books/{book_slug}/outputs/`, or both `outputs/` and `knowledge_root`.
- `research_context.md` exists only when optional external preflight is used.

## Reading Notes

Canonical reading notes path:

```text
{canonical_notes_path}
```

With `knowledge_root`, this usually expands to:

```text
{knowledge_root}/L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/{book_slug}-阅读笔记.md
```

Required baseline:

1. Frontmatter exists.
2. `source` points to raw source Markdown.
3. A directory or chapter navigation exists.
4. In-scope chapters are covered.
5. Covered chapters have raw source backlinks.
6. Structure is content-driven.
7. Definitions, frameworks, SOPs, comparisons, mechanisms, scenes, evidence, or questions are used only when the content calls for them.
8. The Agent must not invent content to fill a template.

Recommended sections, not mandatory for every chapter:

- `核心定义/主张`
- `核心结论`
- `关键框架`
- `支撑证据`
- `执行步骤`
- `检查清单`
- `场景触发词`
- `旧理解 / 新理解`
- `关键变量`
- `反问话术`

Example:

```markdown
---
aliases: [示例书]
tags: [书籍, 阅读笔记]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: YYYY-MM-DD
reading_lens:
  primary: cognitive-refresh
  secondary:
    - scene-mapping
scent:
  - 批判性思考
  - 证据检查
scent_en:
  - critical-thinking
  - evidence-checking
---

# 《示例书》阅读笔记

## 目录

- [[#第一章 示例章节]]

## 第一章 示例章节

本章首先说明了一个关键问题：……

### 一个重要机制

- 机制 A：……
- 机制 B：……

相关来源：[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]
```

Plain Markdown is valid. HTML cards are optional visual aids.

## Reading Lenses

`reading_lens` describes analytical perspectives, not mutually exclusive templates.

Available lenses:

| Lens | Use |
| --- | --- |
| `distillation` | 干货提炼 |
| `sop` | 执行手册 |
| `scene-mapping` | 场景映射 / 生产力转化 |
| `cognitive-refresh` | 认知刷新 / 反常识洞察 |
| `communication-game` | 沟通博弈 / 决策推演 |

Legacy `reading_mode` can be read for compatibility, but new notes should prefer `reading_lens`.

## HTML Components

HTML components are optional visual aids, not mandatory structure.

Use HTML cards when they improve readability:

- One-liner card: recommended for the book's central claim.
- Core Framework Grid: use only when the book has 3-8 parallel frameworks or concepts.
- Process Flow: use for clear step-by-step methods.
- Comparison Card: use for contrastive ideas.

Do not force HTML cards when the book's structure is narrative, progressive, argumentative, mathematical, or not grid-friendly. Plain Markdown is always acceptable when it better preserves the book's logic.

HTML must use inline style and must not use external CSS, JavaScript, dark card backgrounds, heavy shadows, or `border-top`.

## Scent Tags

Scent supports English, Chinese, or custom tags.

Two valid strategies:

```yaml
scent:
  - 批判性思考
  - 证据检查
```

```yaml
scent:
  - 批判性思考
  - 证据检查
scent_en:
  - critical-thinking
  - evidence-checking
```

Rules:

- The bundled English list is a recommended vocabulary, not an enum.
- Chinese tags are often more intuitive for human readers.
- English tags are often more stable for program routing.
- User systems may define custom tags.
- Missing or overly generic scent values should warn, not hard fail.

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
  "backlinks_passed": true,
  "chapters_missing_backlinks": [],
  "hard_checks": {
    "frontmatter": true,
    "chapter_coverage": true,
    "backlinks": true
  },
  "warnings": [
    "The same structure is repeated across chapters; consider a more content-driven structure."
  ],
  "format_issues": [],
  "coverage_details": [],
  "passed": true
}
```

Compatibility fields such as `core_claims_passed`, `core_conclusions_passed`, `reading_mode`, and `mode_required_fields_passed` may still appear, but fixed template fields are warnings rather than pass/fail requirements.

Audit hard checks verify coverage and traceability. Audit warnings identify obvious structure or formatting problems. Audit does not replace human judgment and `PASS` does not mean the note is intellectually complete.

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
  "research_context": ".cache/book-learning/示例书/research_context.md",
  "audit": ".cache/book-learning/示例书/audit.json",
  "knowledge_root": "{knowledge_root}",
  "knowledge_category_root": "{knowledge_root}/L1-事实与语义/02-📚 知识",
  "matched_knowledge_subdir": "{matched_knowledge_subdir}",
  "category_match_reason": "用户确认",
  "canonical_notes": "{knowledge_root}/L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/示例书-阅读笔记.md",
  "reading_lens": {
    "primary": "cognitive-refresh",
    "secondary": ["scene-mapping"]
  },
  "scent": ["批判性思考", "证据检查"],
  "scent_en": ["critical-thinking", "evidence-checking"],
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
  "reading_lens": {
    "primary": "distillation",
    "secondary": []
  },
  "scent": ["批判性思考", "证据检查"],
  "scent_index": null,
  "index_status": "no_knowledge_root",
  "created": "YYYY-MM-DD"
}
```

Rules:

- `canonical_notes` must point to the only final reading notes path.
- `scent` should match reading notes frontmatter.
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
- [[L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/{book_slug}-阅读笔记|示例书]]
  - scent: 批判性思考, 证据检查
  - raw: raw/books/{book_slug}/{book_slug}.md
  - manifest: .cache/book-learning/{book_slug}/run_manifest.json
  - status: ready_for_vector_index
```

Text scent indexing is baseline. Vector indexing is optional and handled by an external skill or user system.
