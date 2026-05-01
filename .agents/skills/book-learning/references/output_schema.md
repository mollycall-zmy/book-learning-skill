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
aliases: [书名别名]
tags: [书籍, 分类]
author: 作者名
source: "[[raw/books/书名]]"
created: YYYY-MM-DD
---

# 📚 《书名》— 作者

> [!info] 全书一句话
> 用一句话概括本书核心主张。

## 目录

- [[#第一章 标题]]
- [[#第二章 标题]]

## 第一章 标题

**核心主张**：一句话概括本章。

**关键要点**：

- 要点 1（[[raw/books/书名#第一章 标题]]）
- 要点 2
- 要点 3

**AI 分析**：

- **跨界关联**：xxx
- **适用边界**：xxx
- **批判性思考**：xxx
- **一句话提炼**：xxx

## 全书核心框架

1. 框架 1
2. 框架 2
3. 框架 3

## 金句

> 1. “原文金句。”（第 X 章）
```

Rules:

- Every in-scope chapter must appear in this file.
- Every chapter must include at least one core claim.
- Every chapter must include AI Analysis / AI 分析.
- Every chapter must include at least one backlink to the raw source.
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
  "ai_analysis_passed": true,
  "chapters_missing_ai_analysis": [],
  "backlinks_passed": true,
  "chapters_missing_backlinks": [],
  "has_core_framework": true,
  "has_quotes": true,
  "passed": true
}
```
