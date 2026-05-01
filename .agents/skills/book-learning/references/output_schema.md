# Output Schema

## TOC JSON

```json
{
  "source": "outputs/book.md",
  "chapters": [
    {
      "id": "001",
      "title": "Chapter Title",
      "level": 1,
      "start_line": 10,
      "end_line": 85,
      "line_count": 76,
      "slug": "chapter-title"
    }
  ],
  "filtered_out": [
    {
      "id": "004",
      "title": "方框1.1 示例侧栏",
      "reason": "sidebar_or_box"
    }
  ],
  "filters": {
    "min_lines": 15,
    "max_level": 3,
    "include_sidebars": false,
    "include_toc_heading": false
  }
}
```

Line numbers are 1-based and inclusive.

`chapters` should contain main chapters by default. `filtered_out` is retained for debugging and may include TOC headings, sidebars, box fragments, deep headings, short fragments, or decorative headings.

## Raw Source

Default path:

```text
raw/books/{书名}.md
```

The raw source is archived for traceability. Treat it as read-only.

## Reading Notes

Default path:

```text
outputs/reading_notes.md
```

This is the primary reading output.

If the user provides a knowledge base or Obsidian path, the same note may be archived as:

```text
L1-事实与语义/02-📚 知识/{书名}-阅读笔记.md
```

Do not hard-code that path in the open-source workflow.

Required structure:

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

## 全书核心框架

1. 框架 1
2. 框架 2
3. 框架 3

## 金句

> 1. “原文金句。”（第 X 章）
```

Rules:

- Every in-scope chapter must appear in this file.
- Every chapter must include `核心定义/主张` or `核心主张`.
- Every chapter must include `核心结论`.
- Every chapter must include at least one backlink to the raw source.
- `关键框架` is required when the chapter contains a model, method, classification, process, or structure.
- `支撑证据` is required when the chapter contains research, data, cases, or a clear argument chain.
- Do not invent frameworks or evidence just to fill a field.
- Long books may be grouped by part, section, or theme, but chapters must not be omitted.

## Reading Notes Audit JSON

```json
{
  "reading_notes_exists": true,
  "checked_chapters": 2,
  "filtered_out_count": 3,
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
  "has_core_framework": true,
  "has_quotes": true,
  "passed": true
}
```
