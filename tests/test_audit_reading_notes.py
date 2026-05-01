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
            {"id": "001", "title": "Chapter One", "level": 2, "start_line": 1, "end_line": 10, "slug": "chapter-one"},
            {"id": "002", "title": "Chapter Two", "level": 2, "start_line": 11, "end_line": 20, "slug": "chapter-two"},
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


if __name__ == "__main__":
    unittest.main()
