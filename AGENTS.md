# Agent Guide

Use the Skill at `.agents/skills/book-learning/` when the user asks to learn, digest, summarize, or create a complete reading note from a whole book.

中文说明：当用户说“学习这本书”“读一下这本书”“逐章做笔记”“整理成阅读笔记”“检查章节遗漏”时，优先使用 `.agents/skills/book-learning/`。不要默认生成知识卡片，先保留目录树和章节边界，最终写入一份完整的 `outputs/reading_notes.md`。

Core rule: extract the table of contents first, read chapter by chapter second, write one consolidated `outputs/reading_notes.md` third, and audit that reading note before reporting completion.

核心规则：先提取目录树，再逐章阅读，然后把所有章节写进同一份阅读笔记；审计通过后再向用户报告完成情况。

Do not commit or expose real book files, copyrighted text, OCR output, or private user content. Keep original files under `raw/books/` and generated work under `outputs/`; these paths are ignored by git.

不要提交或暴露真实书籍、版权文本、OCR 全文或用户私有文件。原始文件放在 `raw/books/`，过程输出放在 `outputs/`；这些路径已经被 git 忽略。

Useful commands:

```bash
python3 .agents/skills/book-learning/scripts/check_tools.py
python3 .agents/skills/book-learning/scripts/convert_to_md.py raw/books/book.pdf --out outputs/book.md
python3 .agents/skills/book-learning/scripts/extract_toc.py outputs/book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py outputs/book.md --toc outputs/toc.json --out outputs/chapters
python3 .agents/skills/book-learning/scripts/audit_reading_notes.py --toc outputs/toc.json --reading-notes outputs/reading_notes.md
```
