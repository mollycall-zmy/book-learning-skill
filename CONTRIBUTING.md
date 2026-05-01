# Contributing

Thanks for helping improve `book-learning-skill`. This project is intentionally small and focused: reliable book structure extraction, chapter-by-chapter learning, omission audits, and traceable knowledge cards.

## Issues

Open an issue when you find a bug, confusing documentation, weak converter behavior, or a missing workflow detail. Please include:

- What you tried to do
- The command you ran
- The expected behavior
- The actual behavior or error message
- Your operating system and Python version, if relevant

Do not attach copyrighted books, private files, full OCR output, or generated knowledge bases from copyrighted sources.

## Pull Requests

Before opening a PR:

1. Keep changes focused.
2. Avoid unrelated refactors.
3. Add or update tests for script behavior.
4. Update README or reference docs when behavior changes.
5. Run the local test command.

Local tests:

```bash
python3 -m unittest discover -s tests
```

## Copyright And Privacy

Do not commit:

- Real books, PDFs, EPUBs, MOBI/AZW files, DOCX books, or OCR outputs
- User private files
- `raw/books/`
- `outputs/`
- `knowledge_base/`
- Long copyrighted excerpts

Use synthetic examples like `examples/sample_book.md` for tests and documentation.

## Code Style

- Keep scripts command-line friendly.
- Prefer Python standard library unless a dependency is clearly justified.
- Keep errors actionable: say which tool is missing and how to install it.
- Do not add automatic installation behavior without clear opt-in flags and tests.
- Avoid broad rewrites of working scripts.

## Documentation Style

- Write documentation for people trying the project locally.
- Be explicit about copyright and privacy boundaries.
- Do not promise features that are only on the roadmap.
- Keep Agent Skill instructions concise; put long workflow details in `references/`.

## Good Contribution Areas

- OCR workflow orchestration
- Optional dependency installation with `check_tools.py --install`
- Obsidian-friendly output templates
- Knowledge card indexes
- Better TOC detection for non-standard Markdown
- Resumable processing with `progress.json`
