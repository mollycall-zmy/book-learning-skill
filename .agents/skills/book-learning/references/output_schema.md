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
- Open Questions

## Audit JSON

```json
{
  "status": "pass",
  "toc_count": 3,
  "chapter_file_count": 3,
  "note_file_count": 3,
  "missing_chapters": [],
  "extra_chapter_files": [],
  "missing_notes": []
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
