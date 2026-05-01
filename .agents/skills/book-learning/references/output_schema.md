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

<div style="background: linear-gradient(135deg, #FAFAFA 0%, #F2F0EB 100%); padding: 28px; border-radius: 16px; margin: 24px 0;">
  <div style="background: #FFFFFF; border-radius: 12px; padding: 22px 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
    <div style="font-size: 11px; color: #CFA76F; font-weight: 600; letter-spacing: 0.08em; margin-bottom: 10px;">
      全书一句话
    </div>
    <div style="font-size: 18px; line-height: 1.7; color: #222; font-weight: 600;">
      这里写全书最核心的主张：用一句话说明这本书到底在讲什么。
    </div>
  </div>
</div>

## 目录

- [[#第一章 示例章节]]
- [[#第二章 示例章节]]

## 第一章 示例章节

**核心定义/主张**：用 1-2 句话说明本章最核心的观点。[[raw/books/示例书#第一章 示例章节|🔗]]

**关键框架**：

- 框架 / 方法 / 分类 / 模型 1：说明其结构和含义。[[raw/books/示例书#子节标题|🔗]]
- 框架 / 方法 / 分类 / 模型 2：说明其结构和含义。[[raw/books/示例书#子节标题|🔗]]

**核心结论**：用 1-2 句话写出作者在本章得出的最重要结论。[[raw/books/示例书#第一章 示例章节|🔗]]

**支撑证据**：

- 证据 1：最有力的数据、研究、案例或原文论证。
- 证据 2：如果有第二个强证据，再补充；不要罗列弱故事。

## 全书核心框架

<div style="background: linear-gradient(135deg, #FAFAFA 0%, #F2F0EB 100%); padding: 28px; border-radius: 16px; margin: 24px 0;">
  <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 18px;">
    全书核心框架
  </div>
  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 16px;">
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Framework 01</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">框架一</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明框架一的作用和含义。</div>
    </div>
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Framework 02</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">框架二</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明框架二的作用和含义。</div>
    </div>
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Framework 03</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">框架三</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明框架三的作用和含义。</div>
    </div>
    <div style="background: #FFFFFF; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; color: #888; margin-bottom: 6px;">Framework 04</div>
      <div style="font-size: 14px; color: #333; font-weight: 600; margin-bottom: 8px;">框架四</div>
      <div style="font-size: 12px; color: #555; line-height: 1.6;">说明框架四的作用和含义。</div>
    </div>
  </div>
</div>

## 金句

> 1. “原文金句。”（第 X 章）
```

Rules:

- Every in-scope chapter must appear in this file.

Reading Notes Section Schema:

- Every chapter must include `核心定义/主张` or `核心主张`.
- Every chapter must include `核心结论`.
- Every chapter must include at least one backlink to the raw source.
- `核心定义/主张` must include a backlink: `[[raw/books/{书名}#{标题}|🔗]]`.
- `核心结论` should include a backlink.
- `关键框架` is required when the chapter contains a model, method, classification, process, or structure.
- If `关键框架` is present, each item should include a backlink.
- `支撑证据` is required when the chapter contains research, data, cases, or a clear argument chain.
- `支撑证据` does not require backlinks.
- Do not invent frameworks or evidence just to fill a field.
- Long books may be grouped by part, section, or theme, but chapters must not be omitted.

Formatting constraints:

- Tables must not be indented.
- Tables must have a blank line before them.
- Tables must not be inside list items.
- Tables must not be inside callout blocks.
- Mermaid blocks must not be indented.
- Mermaid blocks must have a blank line before the opening fence.
- Callouts must not contain tables or Mermaid diagrams.

## HTML Card Components

`outputs/reading_notes.md` may contain inline HTML components for high-level visual sections.

Supported components:

- Book one-liner card
- Process flow card
- Core framework grid card

Rules:

- HTML must use inline style.
- Do not use external CSS.
- Do not use JavaScript.
- Do not use dark card backgrounds.
- Do not use heavy shadows.
- Do not use top border decoration.
- Do not use full border declarations.
- Use warm gradient background only on outer containers.
- Use white cards for content blocks.
- Use gold gradient only for key process nodes.
- Keep ordinary chapter notes in Markdown unless visualization improves readability.

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
  "format_issues": [],
  "has_core_framework": true,
  "has_quotes": true,
  "passed": true
}
```
