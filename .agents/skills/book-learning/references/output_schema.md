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
      "slug": "chapter-title"
    }
  ]
}
```

Line numbers are 1-based and inclusive.

## Chapter File

Filename:

```text
001-chapter-title.md
```

Body:

```markdown
# Chapter Title

...
```

## Chapter Note

Filename:

```text
001-chapter-title.notes.md
```

Required sections:

- Source
- Core Questions
- Main Claims
- Argument Chain
- Concepts And Definitions
- Evidence, Cases, And Data
- Easy-To-Miss Details
- Transferable Insights
- AI Analysis / AI 分析
- Open Questions

## Consolidated Reading Notes

Path:

```text
outputs/reading_notes.md
```

This is the primary reading output. Per-chapter notes are audit and traceability files.

Required sections:

- 大目录
- 分章节笔记
- Each chapter's core claim
- Each chapter's key points
- Each chapter's AI Analysis / AI 分析
- 全书核心框架
- 金句集

For long books:

- Chapters may be grouped by part, section, or theme.
- Chapters must not be omitted.
- Every chapter must have at least one core claim.

Minimal structure:

```markdown
# 《书名》阅读笔记

## 大目录

| 章节 | 核心主张 | 页数/行数 |
| --- | --- | --- |

## 分章节笔记

### 第一章 xxx

#### 核心主张

#### 关键要点

#### AI 分析

## 全书核心框架

## 金句集
```

## Audit JSON

```json
{
  "status": "pass",
  "toc_count": 3,
  "chapter_file_count": 3,
  "note_file_count": 3,
  "missing_chapters": [],
  "extra_chapter_files": [],
  "missing_notes": [],
  "incomplete_notes": [],
  "notes_missing_ai_analysis": [],
  "reading_notes_exists": true,
  "reading_notes_has_core_framework": true,
  "reading_notes_has_chapter_notes": true
}
```

`status` is `pass` only when every list is empty.

## Knowledge Card

Filename:

```text
card-YYYYMMDD-short-slug.md
```

Required fields:

- Title
- Type
- Atomic Idea
- Source
- Explanation
- Reuse Context
- Related Cards

Source format:

```text
chapter_id: 003
chapter_title: Example Chapter
lines: 42-68
```
