# Agent Guide

Use the Skill at `.agents/skills/book-learning/` when the user asks to learn, digest, summarize, or extract reusable knowledge from a whole book.

中文说明：当用户说“学习这本书”“读一下这本书”“逐章做笔记”“提取知识卡片”“检查章节遗漏”时，优先使用 `.agents/skills/book-learning/`。不要一上来写全书总结，先保留目录树和章节边界。

Core rule: extract the table of contents first, create chapter-level notes second, audit for omissions third, and generate full-book summaries or knowledge cards only after that.

核心规则：先提取目录树，再生成逐章笔记，然后做章节遗漏审计；只有审计通过后，才生成全书摘要或原子知识卡片。

Do not commit or expose real book files, copyrighted text, OCR output, or private user content. Keep original files under `raw/books/`, generated work under `outputs/`, and final cards under `knowledge_base/`; these paths are ignored by git.

不要提交或暴露真实书籍、版权文本、OCR 全文或用户私有文件。原始文件放在 `raw/books/`，过程输出放在 `outputs/`，最终卡片放在 `knowledge_base/`；这些路径已经被 git 忽略。

Useful commands:

```bash
python3 .agents/skills/book-learning/scripts/check_tools.py
python3 .agents/skills/book-learning/scripts/convert_to_md.py raw/books/book.pdf --out outputs/book.md
python3 .agents/skills/book-learning/scripts/extract_toc.py outputs/book.md --out outputs/toc.json
python3 .agents/skills/book-learning/scripts/split_chapters.py outputs/book.md --toc outputs/toc.json --out outputs/chapters
python3 .agents/skills/book-learning/scripts/audit_chapters.py --toc outputs/toc.json --chapters outputs/chapters --notes outputs/notes
```
