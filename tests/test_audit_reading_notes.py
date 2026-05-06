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
        "source": "raw/books/示例书/示例书.md",
        "chapters": [
            {"id": "001", "title": "第一章 示例章节", "level": 2, "start_line": 1, "end_line": 40, "slug": "chapter-one", "line_count": 40},
            {"id": "002", "title": "第二章 示例章节", "level": 2, "start_line": 41, "end_line": 80, "slug": "chapter-two", "line_count": 40},
        ],
    }
    path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
    return toc


def complete_notes():
    return """---
aliases: [示例书]
tags: [书籍]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: 2026-01-01
reading_mode: mode-0-distillation
scent:
  - critical-thinking
  - structured-reading
---

# 📚 《示例书》— 示例作者

## 第一章 示例章节

**核心定义/主张**：本章提出一个核心观点，用于说明示例问题。

**关键框架**：

- 框架一：说明问题如何被拆解。
- 框架二：说明行动如何展开。

**核心结论**：本章结论是，示例问题需要通过结构化方法处理。

**支撑证据**：

- 示例证据：作者用一个案例支撑了该结论。

**来源回链**：[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

## 第二章 示例章节

**核心定义/主张**：本章提出另一个核心观点，用于补充示例问题。

**关键框架**：

- 框架一：说明第二个问题如何被拆解。

**核心结论**：本章结论是，后续问题需要继续用结构化方法处理。

**支撑证据**：

- 示例证据：作者用另一个案例支撑了该结论。

**来源回链**：[[raw/books/示例书/示例书.md#第二章 示例章节|🔗]]

## 全书核心框架

1. 框架一
2. 框架二
3. 框架三

## 金句

> “示例金句。”（第一章）
"""


class AuditReadingNotesTest(unittest.TestCase):
    def test_complete_reading_notes_pass_without_extra_analysis_section(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes(), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path, Path("raw/books/示例书/示例书.md"))

            self.assertTrue(report["passed"])
            self.assertTrue(report["frontmatter_passed"])
            self.assertTrue(report["chapter_coverage_passed"])
            self.assertTrue(report["core_claims_passed"])
            self.assertTrue(report["core_conclusions_passed"])
            self.assertTrue(report["backlinks_passed"])
            self.assertEqual(report["format_issues"], [])

    def test_exact_heading_match_still_passes(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/示例书/示例书.md",
                "chapters": [
                    {"id": "001", "title": "第一章 示例章节", "level": 2, "start_line": 1, "end_line": 40, "slug": "main", "line_count": 40}
                ],
            }
            toc_path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes(), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["chapter_coverage_passed"])
            self.assertEqual(report["missing_chapters"], [])
            self.assertEqual(report["coverage_details"][0]["matched_by"], "exact")

    def test_section_level_toc_can_be_covered_by_grouped_chapter_section(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/示例书/示例书.md",
                "chapters": [
                    {"id": "001", "title": "第一节 子主题 A", "level": 2, "start_line": 1, "end_line": 30, "slug": "a", "line_count": 30},
                    {"id": "002", "title": "第二节 子主题 B", "level": 2, "start_line": 31, "end_line": 60, "slug": "b", "line_count": 30},
                ],
            }
            toc_path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                """---
aliases: [示例书]
tags: [书籍]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: 2026-01-01
reading_mode: mode-0-distillation
scent:
  - critical-thinking
  - structured-reading
---

# 📚 《示例书》— 示例作者

## 第一章 示例章节

**核心定义/主张**：这一章整合了两个子主题。

**关键框架**：

- 子主题 A：这里覆盖第一节内容（[[raw/books/示例书/示例书.md#第一节 子主题 A|🔗]]）
- 子主题 B：这里覆盖第二节内容（[[raw/books/示例书/示例书.md#第二节 子主题 B|🔗]]）

**核心结论**：两个子主题共同说明示例问题需要被结构化处理。

**支撑证据**：

- 示例证据：作者用案例支撑了两个子主题。

**来源回链**：[[raw/books/示例书/示例书.md#第一节 子主题 A|🔗]]

## 全书核心框架

1. 框架一
2. 框架二
3. 框架三

## 金句

> “示例金句。”（第一章）
""",
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertTrue(report["chapter_coverage_passed"])
            self.assertEqual(report["checked_chapters"], 2)
            self.assertEqual(report["covered_chapters"], 2)
            self.assertEqual(report["missing_chapters"], [])
            matched_by = {detail["matched_by"] for detail in report["coverage_details"]}
            self.assertTrue({"keyword", "backlink"} & matched_by)

    def test_missing_grouped_section_level_toc_item_fails(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/示例书/示例书.md",
                "chapters": [
                    {"id": "001", "title": "第一节 子主题 A", "level": 2, "start_line": 1, "end_line": 30, "slug": "a", "line_count": 30},
                    {"id": "002", "title": "第二节 子主题 B", "level": 2, "start_line": 31, "end_line": 60, "slug": "b", "line_count": 30},
                ],
            }
            toc_path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                """---
aliases: [示例书]
tags: [书籍]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: 2026-01-01
reading_mode: mode-0-distillation
scent:
  - critical-thinking
  - structured-reading
---

# 📚 《示例书》— 示例作者

## 第一章 示例章节

**核心定义/主张**：这一章只覆盖一个子主题。

**关键框架**：

- 子主题 A：这里覆盖第一节内容（[[raw/books/示例书/示例书.md#第一节 子主题 A|🔗]]）

**核心结论**：这个子主题说明示例问题需要被结构化处理。

**支撑证据**：

- 示例证据：作者用案例支撑了该子主题。

**来源回链**：[[raw/books/示例书/示例书.md#第一节 子主题 A|🔗]]

## 全书核心框架

1. 框架一
2. 框架二
3. 框架三

## 金句

> “示例金句。”（第一章）
""",
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertFalse(report["chapter_coverage_passed"])
            self.assertIn("002", report["missing_chapters"])

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

    def test_missing_scent_frontmatter_warns_without_failing(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                complete_notes().replace("scent:\n  - critical-thinking\n  - structured-reading\n", ""),
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertTrue(report["frontmatter_passed"])
            self.assertNotIn("scent", report["missing_frontmatter_fields"])
            self.assertTrue(any("Scent tags are missing" in warning for warning in report["warnings"]))

    def test_missing_reading_mode_is_allowed_for_content_driven_notes(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("reading_mode: mode-0-distillation\n", ""), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertIsNone(report["reading_mode"])

    def test_frontmatter_reading_mode_is_reported(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("reading_mode: mode-0-distillation", "reading_mode: mode-1-sop"), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertEqual(report["reading_mode"], "mode-1-sop")

    def test_mode_1_sop_passes_without_core_claim(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                """---
aliases: [示例书]
tags: [书籍]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: 2026-01-01
reading_mode: mode-1-sop
scent:
  - structured-reading
  - decision-making
---

# 📚 《示例书》— 示例作者

## 第一章 示例章节

**适用场景**：这个方法用于处理示例任务。

**执行步骤**：

1. Step 1
2. Step 2
3. Step 3

**检查清单**：

- [ ] 检查项 1
- [ ] 检查项 2

**来源回链**：[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

## 第二章 示例章节

**适用场景**：这个方法用于处理另一个示例任务。

**执行步骤**：

1. Step 1
2. Step 2
3. Step 3

**检查清单**：

- [ ] 检查项 1
- [ ] 检查项 2

**来源回链**：[[raw/books/示例书/示例书.md#第二章 示例章节|🔗]]

## 全书核心框架

1. 框架一

## 金句

> “示例金句。”（第一章）
""",
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertEqual(report["reading_mode"], "mode-1-sop")
            self.assertTrue(report["mode_required_fields_passed"])
            self.assertFalse(report["core_claims_passed"])

    def test_legacy_mode_field_gaps_warn_without_failing(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes = complete_notes().replace("reading_mode: mode-0-distillation", "reading_mode: mode-1-sop")
            notes = notes.replace("**关键框架**", "**执行步骤**")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(notes, encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertFalse(report["mode_required_fields_passed"])
            self.assertIn("检查清单", report["chapters_missing_mode_required_fields"][0]["missing_fields"])
            self.assertTrue(any("legacy reading_mode" in warning for warning in report["warnings"]))

    def test_missing_chapter_fails(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            second_start = complete_notes().index("## 第二章 示例章节")
            summary_start = complete_notes().index("## 全书核心框架")
            notes_path.write_text(complete_notes()[:second_start] + complete_notes()[summary_start:], encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertFalse(report["passed"])
            self.assertFalse(report["chapter_coverage_passed"])
            self.assertIn("002", report["missing_chapters"])

    def test_missing_core_claim_warns_without_failing(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("**核心定义/主张**：本章提出一个核心观点，用于说明示例问题。", ""), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertFalse(report["core_claims_passed"])
            self.assertIn("001", report["chapters_missing_core_claim"])
            self.assertTrue(any("核心定义/主张" in warning for warning in report["warnings"]))

    def test_missing_core_conclusion_warns_without_failing(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("**核心结论**：本章结论是，示例问题需要通过结构化方法处理。", ""), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertFalse(report["core_conclusions_passed"])
            self.assertIn("001", report["chapters_missing_core_conclusion"])
            self.assertTrue(any("核心结论" in warning for warning in report["warnings"]))

    def test_missing_backlink_fails(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("[[raw/books/示例书/示例书.md#第二章 示例章节|🔗]]", "raw/books/示例书/示例书.md#第二章 示例章节"), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertFalse(report["passed"])
            self.assertFalse(report["backlinks_passed"])
            self.assertIn("002", report["chapters_missing_backlinks"])

    def test_missing_core_framework_or_quotes_warns_without_failing(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes().replace("## 全书核心框架", "## 全书结构").replace("## 金句", "## 句子"), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertFalse(report["has_core_framework"])
            self.assertFalse(report["has_quotes"])
            self.assertTrue(any("全书核心框架" in warning for warning in report["warnings"]))
            self.assertTrue(any("金句" in warning for warning in report["warnings"]))

    def test_filtered_toc_items_do_not_require_independent_sections(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/示例书/示例书.md",
                "chapters": [
                    {"id": "001", "title": "第一章 示例章节", "level": 2, "start_line": 1, "end_line": 40, "slug": "chapter-one", "line_count": 40},
                    {"id": "002", "title": "方框1.1 示例侧栏", "level": 3, "start_line": 41, "end_line": 60, "slug": "box", "line_count": 20},
                    {"id": "003", "title": "短碎片标题", "level": 3, "start_line": 61, "end_line": 65, "slug": "short", "line_count": 5},
                    {"id": "004", "title": "第二章 示例章节", "level": 2, "start_line": 66, "end_line": 105, "slug": "chapter-two", "line_count": 40},
                ],
            }
            toc_path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes(), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertEqual(report["checked_chapters"], 2)
            self.assertEqual(report["filtered_out_count"], 2)
            self.assertEqual(report["missing_chapters"], [])

    def test_raw_source_backlinks_pass_and_no_format_issues(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/示例书/示例书.md",
                "chapters": [
                    {"id": "001", "title": "第一章 示例章节", "level": 2, "start_line": 1, "end_line": 40, "slug": "chapter-one", "line_count": 40}
                ],
            }
            toc_path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                """---
aliases: [示例书]
tags: [书籍]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: 2026-01-01
reading_mode: mode-0-distillation
scent:
  - critical-thinking
  - structured-reading
---

# 📚 《示例书》

## 第一章 示例章节

**核心定义/主张**：这是核心定义。[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

**核心结论**：这是核心结论。[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

## 全书核心框架

1. 框架一
2. 框架二
3. 框架三

## 金句

> “示例金句。”（第一章）
""",
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["backlinks_passed"])
            self.assertEqual(report["format_issues"], [])

    def test_raw_source_extensionless_backlinks_pass(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/示例书/示例书.md",
                "chapters": [
                    {"id": "001", "title": "第一章 示例章节", "level": 2, "start_line": 1, "end_line": 40, "slug": "chapter-one", "line_count": 40}
                ],
            }
            toc_path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                """---
aliases: [示例书]
tags: [书籍]
author: 示例作者
source: "[[raw/books/示例书/示例书]]"
created: 2026-01-01
reading_mode: mode-0-distillation
scent:
  - critical-thinking
  - structured-reading
---

# 📚 《示例书》

## 第一章 示例章节

**核心定义/主张**：这是核心定义。[[raw/books/示例书/示例书#第一章 示例章节|🔗]]

**核心结论**：这是核心结论。[[raw/books/示例书/示例书#第一章 示例章节|🔗]]

## 全书核心框架

1. 框架一
2. 框架二
3. 框架三

## 金句

> “示例金句。”（第一章）
""",
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path, Path("raw/books/示例书/示例书.md"))

            self.assertTrue(report["passed"])
            self.assertTrue(report["backlinks_passed"])
            self.assertEqual(report["chapters_missing_backlinks"], [])

    def test_absolute_raw_source_backlinks_pass(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/示例书/示例书.md",
                "chapters": [
                    {"id": "001", "title": "第一章 示例章节", "level": 2, "start_line": 1, "end_line": 40, "slug": "chapter-one", "line_count": 40}
                ],
            }
            toc_path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                """---
aliases: [示例书]
tags: [书籍]
author: 示例作者
source: "[[/tmp/example-knowledge-root/raw/books/示例书/示例书.md]]"
created: 2026-01-01
reading_mode: mode-0-distillation
scent:
  - critical-thinking
  - structured-reading
---

# 📚 《示例书》

## 第一章 示例章节

**核心定义/主张**：这是核心定义。[[/tmp/example-knowledge-root/raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

**核心结论**：这是核心结论。[[~/example-knowledge-root/raw/books/示例书/示例书.md#第一章 示例章节|🔗]]

## 全书核心框架

1. 框架一
2. 框架二
3. 框架三

## 金句

> “示例金句。”（第一章）
""",
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertTrue(report["backlinks_passed"])
            self.assertEqual(report["chapters_missing_backlinks"], [])

    def test_chapter_cache_backlink_does_not_satisfy_raw_source_requirement(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/示例书/示例书.md",
                "chapters": [
                    {"id": "001", "title": "第一章 示例章节", "level": 2, "start_line": 1, "end_line": 40, "slug": "chapter-one", "line_count": 40}
                ],
            }
            toc_path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                """---
aliases: [示例书]
tags: [书籍]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: 2026-01-01
reading_mode: mode-0-distillation
scent:
  - critical-thinking
  - structured-reading
---

# 📚 《示例书》

## 第一章 示例章节

**核心定义/主张**：这是核心定义。[[.cache/book-learning/示例书/chapters/001-示例章节.md#第一章 示例章节|🔗]]

**核心结论**：这是核心结论。[[.cache/book-learning/示例书/chapters/001-示例章节.md#第一章 示例章节|🔗]]

## 全书核心框架

1. 框架一
2. 框架二
3. 框架三

## 金句

> “示例金句。”（第一章）
""",
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path, Path("raw/books/示例书/示例书.md"))

            self.assertFalse(report["passed"])
            self.assertFalse(report["backlinks_passed"])
            self.assertIn("001", report["chapters_missing_backlinks"])

    def test_indented_table_format_issue_does_not_fail_audit(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes = complete_notes().replace(
                "**核心结论**：本章结论是，示例问题需要通过结构化方法处理。",
                """  | 概念 A | 概念 B |
  |-------|-------|
  | 示例 1 | 示例 2 |

**核心结论**：本章结论是，示例问题需要通过结构化方法处理.""",
            )
            notes_path.write_text(notes, encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertTrue(report["format_issues"])
            self.assertTrue(any("indented" in issue for issue in report["format_issues"]))

    def test_table_after_list_item_format_issue_does_not_fail_audit(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes = complete_notes().replace(
                "- 框架一：说明问题如何被拆解。",
                """- **关键框架**：
| 概念 A | 概念 B |
|-------|-------|
- 框架一：说明问题如何被拆解.""",
            )
            notes_path.write_text(notes, encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertTrue(report["format_issues"])
            self.assertTrue(any("list item" in issue or "blank line" in issue for issue in report["format_issues"]))

    def test_pure_markdown_notes_without_html_cards_pass(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(complete_notes(), encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertNotIn("HTML", " ".join(report["warnings"]))

    def test_content_driven_section_without_fixed_fields_passes(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = {
                "source": "raw/books/示例书/示例书.md",
                "chapters": [
                    {"id": "001", "title": "第一章 示例章节", "level": 2, "start_line": 1, "end_line": 40, "slug": "chapter-one", "line_count": 40}
                ],
            }
            toc_path.write_text(json.dumps(toc, ensure_ascii=False), encoding="utf-8")
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                """---
aliases: [示例书]
tags: [书籍]
author: 示例作者
source: "[[raw/books/示例书/示例书.md]]"
created: 2026-01-01
scent:
  - 机制理解
  - 风险判断
---

# 《示例书》阅读笔记

## 第一章 示例章节

本章首先说明了一个关键问题：示例判断不能只看表面结论，还要看条件、机制和适用边界。

### 一个重要机制

- 机制 A：先识别问题发生的前提。
- 机制 B：再检查结论是否被证据支撑。

相关来源：[[raw/books/示例书/示例书.md#第一章 示例章节|🔗]]
""",
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertFalse(report["core_claims_passed"])
            self.assertFalse(report["core_conclusions_passed"])

    def test_chinese_scent_values_are_accepted(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes = complete_notes().replace(
                "  - critical-thinking\n  - structured-reading",
                "  - 批判性思考\n  - 风险判断",
            )
            notes_path.write_text(notes, encoding="utf-8")

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            self.assertFalse(any("too generic" in warning for warning in report["warnings"]))

    def test_research_context_template_exists(self):
        template_path = ROOT / ".agents/skills/book-learning/assets/research_context_template.md"

        self.assertTrue(template_path.exists())
        self.assertIn(
            "External context is used only as background, not as authority over the source text.",
            template_path.read_text(encoding="utf-8"),
        )

    def test_repetitive_empty_template_structure_warns_without_failing(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            write_toc(toc_path)
            notes_path = tmp_path / "reading_notes.md"
            notes_path.write_text(
                complete_notes().replace(
                    "**核心定义/主张**：本章提出一个核心观点，用于说明示例问题。",
                    "**核心定义/主张**：用 1-2 句话说明本章最核心的观点。",
                ).replace(
                    "**核心定义/主张**：本章提出另一个核心观点，用于补充示例问题。",
                    "**核心定义/主张**：用 1-2 句话说明本章最核心的观点。",
                ),
                encoding="utf-8",
            )

            report = module.audit_reading_notes(toc_path, notes_path)

            self.assertTrue(report["passed"])
            warnings = " ".join(report["warnings"])
            self.assertTrue("template-like" in warnings or "same structure" in warnings)


if __name__ == "__main__":
    unittest.main()
