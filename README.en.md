# book-learning-skill

An Agent Skill for learning a whole book through a structured workflow: convert the source, preserve the table of contents, read chapter by chapter, audit for omissions, and produce traceable atomic knowledge cards.

This repository does not include real books, PDFs, EPUBs, copyrighted excerpts, or private user files.

## Structure

```text
.agents/skills/book-learning/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

Runtime content should stay outside git:

- `raw/books/` for original user-provided files
- `outputs/` for converted markdown, chapter splits, notes, and audit reports
- `knowledge_base/` for generated card archives and indexes

## Install

Python scripts use the standard library for TOC extraction, chapter splitting, auditing, and tests. Optional conversion dependencies are listed in `requirements.txt`:

```bash
python3 -m pip install -r requirements.txt
```

Some converters are external tools:

- PDF: `pymupdf4llm` from pip
- EPUB, DOCX, HTML: `pandoc`
- EPUB/DOCX/HTML fallback through pip: `pypandoc_binary`
- Scanned PDF OCR: `ocrmypdf` from pip, usually with system OCR dependencies

`check_tools.py` only detects tools in v0.1.0. It does not install anything automatically.

## Use

Ask an Agent to use `.agents/skills/book-learning/` when learning a book. The expected flow is:

1. Put the source file in `raw/books/`.
2. Convert it to Markdown in `outputs/`.
3. Extract a TOC with line ranges.
4. Split chapters by TOC.
5. Write chapter notes from the templates.
6. Audit TOC, chapters, and notes before generating a full-book summary.
7. Generate atomic knowledge cards with traceable chapter sources.

Example commands:

```bash
python3 .agents/skills/book-learning/scripts/check_tools.py
python3 .agents/skills/book-learning/scripts/extract_toc.py examples/sample_book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py examples/sample_book.md --toc outputs/toc.json --out outputs/chapters
python3 .agents/skills/book-learning/scripts/audit_chapters.py --toc outputs/toc.json --chapters outputs/chapters --notes outputs/notes --out outputs/audit.json
```

## Local Tests

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

The test fixture `examples/sample_book.md` is artificial content written for this repository. It is not copied from any real book.

## Copyright Boundary

Do not commit:

- Real books, PDFs, EPUBs, MOBI/AZW files, or OCR outputs
- Long copyrighted excerpts
- User private files
- Generated knowledge bases from copyrighted books

Commit only Skill instructions, scripts, templates, synthetic examples, and tests.
