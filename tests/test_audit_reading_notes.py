import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/book-learning/scripts/audit_reading_notes.py"


def load_module():
    spec = importlib.util.spec_from_file_location("audit_reading_notes", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_toc(path):
    toc = {
        "source": "raw/books/sample.md",
        "chapters": [
            {"id": "001", "title": "Chapter One", "level": 2, "start_line": 1, "end_line": 40, "slug": "chapter-one", "line_count": 40},
            {"id": "002", "title": "Chapter Two", "level": 2, "start_line": 41, "end_line": 80, "slug": "chapter-two", "line_count": 40},
        ],
    }
    path.write_text(json.dumps(toc), encoding="utf-8")
    return toc


def complete_notes():
    return """---
aliases: [Sample]
tags: [书籍, 测试]
author: Test Author
source: "[[raw/books/sample]]"
created: 2026-05-01
---

# 📚 《Sample》— Test Author

## 目录

- [[#Chapter One]]
- [[#Chapter Two]]

## Chapter One

**核心主张**：Chapter one claim.

**关键要点**：
- Point one（[[raw/books/sample#Chapter One]]）

**AI 分析**：
- **跨界关联**：Connects to general learning theory.
- **适用边界**：Works under clear constraints.
- **批判性思考**：May overstate the case.
- **一句话提炼**：Chapter one distilled.

## Chapter Two

**核心主张**：Chapter two claim.

**关键要点**：
- Point two（[[raw/books/sample#Chapter Two]]）

**AI Analysis**：
- Cross-reference: connects to systems thinking.
- Applicability boundary: depends on context.
- Critique: alternative explanations may exist.
- One-sentence distillation: chapter two distilled.

## 全书核心框架

1. Framework one
2. Framework two
3. Framework three

## 金句

> 1. “Synthetic quote.”（Chapter One）
"""


class AuditReadingNotesTest(unittest.TestCase):
    def test_complete_reading_notes_pass(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes(), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertTrue(report["frontmatter_passed"])
            self.assertTrue(report["chapter_coverage_passed"])
            self.assertTrue(report["ai_analysis_passed"])
            self.assertTrue(report["backlinks_passed"])

    def test_missing_frontmatter_fails(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().split("---", 2)[-1], encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertFalse(report["passed"])
            self.assertFalse(report["frontmatter_passed"])
            self.assertIn("aliases", report["missing_frontmatter_fields"])

    def test_missing_chapter_fails(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("## Chapter Two", "## Other Chapter"), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertFalse(report["passed"])
            self.assertFalse(report["chapter_coverage_passed"])
            self.assertIn("002", report["missing_chapters"])

    def test_missing_ai_analysis_fails(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("**AI 分析**", "**分析**"), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertFalse(report["passed"])
            self.assertFalse(report["ai_analysis_passed"])
            self.assertIn("001", report["chapters_missing_ai_analysis"])

    def test_missing_backlink_fails(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("[[raw/books/sample#Chapter Two]]", "raw/books/sample#Chapter Two"), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertFalse(report["passed"])
            self.assertFalse(report["backlinks_passed"])
            self.assertIn("002", report["chapters_missing_backlinks"])

    def test_missing_core_framework_or_quotes_fails(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("## 全书核心框架", "## Framework").replace("## 金句", "## Quotes"), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertFalse(report["passed"])
            self.assertFalse(report["has_core_framework"])
            self.assertFalse(report["has_quotes"])

    def test_filtered_toc_items_do_not_require_independent_sections(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/sample.md",
                "chapters": [
                    {"id": "001", "title": "第一章 主章节", "level": 2, "start_line": 1, "end_line": 40, "slug": "chapter-one", "line_count": 40},
                    {"id": "002", "title": "方框1.1 示例侧栏", "level": 3, "start_line": 41, "end_line": 60, "slug": "box", "line_count": 20},
                    {"id": "003", "title": "短碎片标题", "level": 3, "start_line": 61, "end_line": 65, "slug": "short", "line_count": 5},
                    {"id": "004", "title": "第二章 主章节", "level": 2, "start_line": 66, "end_line": 105, "slug": "chapter-two", "line_count": 40},
                ],
            }
            toc_path.write_text(json.dumps(toc), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                """---
aliases: [示例书]
tags: [书籍, 测试]
author: 示例作者
source: "[[raw/books/示例书]]"
created: 2026-05-01
---

# 📚 《示例书》— 示例作者

## 第一章 主章节

**核心主张**：第一章核心主张。

**关键要点**：
- 要点（[[raw/books/示例书#第一章 主章节]]）

**AI 分析**：
- **跨界关联**：通用关联。
- **适用边界**：通用边界。
- **批判性思考**：通用批判。
- **一句话提炼**：通用提炼。

## 第二章 主章节

**核心主张**：第二章核心主张。

**关键要点**：
- 要点（[[raw/books/示例书#第二章 主章节]]）

**AI 分析**：
- **跨界关联**：通用关联。
- **适用边界**：通用边界。
- **批判性思考**：通用批判。
- **一句话提炼**：通用提炼。

## 全书核心框架

1. 框架一
2. 框架二
3. 框架三

## 金句

> 1. “示例句子。”（第一章）
""",
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertEqual(report["checked_chapters"], 2)
            self.assertEqual(report["filtered_out_count"], 2)
            self.assertEqual(report["missing_chapters"], [])


if __name__ == "__main__":
    unittest.main()
