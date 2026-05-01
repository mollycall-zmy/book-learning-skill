# Examples

`examples/sample_book.md` is a synthetic test book written specifically for this repository. It exists only to test TOC extraction, chapter splitting, and audit behavior.

This repository intentionally does not include real PDF, EPUB, MOBI, AZW, DOCX, or other book samples because books may contain copyrighted or private content. Use your own legally obtained files for local testing, and keep them under `raw/books/`, which is ignored by git.

## Test With Your Own File

Convert a source file to Markdown:

```bash
python3 .agents/skills/book-learning/scripts/convert_to_md.py raw/books/my-book.pdf --out outputs/my-book.md
python3 .agents/skills/book-learning/scripts/convert_to_md.py raw/books/my-book.epub --out outputs/my-book.md
python3 .agents/skills/book-learning/scripts/convert_to_md.py raw/books/my-book.docx --out outputs/my-book.md
python3 .agents/skills/book-learning/scripts/convert_to_md.py raw/books/my-page.html --out outputs/my-page.md
```

Extract the table of contents:

```bash
python3 .agents/skills/book-learning/scripts/extract_toc.py outputs/my-book.md --out outputs/toc.json
```

Split chapters:

```bash
python3 .agents/skills/book-learning/scripts/split_chapters.py outputs/my-book.md --toc outputs/toc.json --out outputs/chapters
```

Audit chapter and note coverage:

```bash
python3 .agents/skills/book-learning/scripts/audit_chapters.py --toc outputs/toc.json --chapters outputs/chapters --notes outputs/notes --out outputs/audit.json
```

If no notes exist yet, the audit command should fail and list missing note files. That is expected.
