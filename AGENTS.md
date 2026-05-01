# Agent Guide

Use the Skill at `.agents/skills/book-learning/` when the user asks to learn, digest, summarize, or extract reusable knowledge from a whole book.

Core rule: extract the table of contents first, create chapter-level notes second, audit for omissions third, and generate full-book summaries or knowledge cards only after that.

Do not commit or expose real book files, copyrighted text, OCR output, or private user content. Keep original files under `raw/books/`, generated work under `outputs/`, and final cards under `knowledge_base/`; these paths are ignored by git.

Useful commands:

```bash
python3 .agents/skills/book-learning/scripts/check_tools.py
python3 .agents/skills/book-learning/scripts/convert_to_md.py raw/books/book.pdf --out outputs/book.md
python3 .agents/skills/book-learning/scripts/extract_toc.py outputs/book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py outputs/book.md --toc outputs/toc.json --out outputs/chapters
python3 .agents/skills/book-learning/scripts/audit_chapters.py --toc outputs/toc.json --chapters outputs/chapters --notes outputs/notes
```
