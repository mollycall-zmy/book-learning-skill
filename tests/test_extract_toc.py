import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/book-learning/scripts/extract_toc.py"
SAMPLE = ROOT / "examples/sample_book.md"


def load_module():
    spec = importlib.util.spec_from_file_location("extract_toc", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExtractTocTest(unittest.TestCase):
    def test_extract_toc_includes_line_ranges(self):
        module = load_module()
        toc = module.extract_toc(SAMPLE, min_lines=0, max_level=6, include_sidebars=True, include_toc_heading=True)

        self.assertTrue(toc["source"].endswith("examples/sample_book.md"))
        self.assertEqual(len(toc["chapters"]), 12)
        self.assertEqual(toc["chapters"][0]["title"], "The Orchard Of Useful Questions")
        self.assertEqual(toc["chapters"][0]["level"], 1)
        self.assertEqual(toc["chapters"][0]["start_line"], 1)
        self.assertLess(toc["chapters"][0]["end_line"], toc["chapters"][1]["start_line"])
        self.assertTrue(all(entry["end_line"] >= entry["start_line"] for entry in toc["chapters"]))

    def test_extract_toc_filters_non_main_chapters_by_default(self):
        module = load_module()
        source = (
            "# 目录\n"
            "\n"
            "## 第一章 主章节\n"
            + "\n".join(f"第一章正文 {index}" for index in range(20))
            + "\n\n"
            "### 方框1.1 示例侧栏\n"
            + "\n".join(f"侧栏内容 {index}" for index in range(20))
            + "\n\n"
            "#### 极短段落标题\n"
            "短内容。\n"
            "\n"
            "### 短碎片标题\n"
            "短内容。\n"
            "\n"
            "## 第二章 主章节\n"
            + "\n".join(f"第二章正文 {index}" for index in range(20))
            + "\n"
        )

        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample_complex_book.md"
            path.write_text(source, encoding="utf-8")
            toc = module.extract_toc(path)

        titles = [entry["title"] for entry in toc["chapters"]]
        filtered_titles = [entry["title"] for entry in toc["filtered_out"]]
        filtered_reasons = {entry["title"]: entry["reason"] for entry in toc["filtered_out"]}

        self.assertIn("第一章 主章节", titles)
        self.assertIn("第二章 主章节", titles)
        self.assertNotIn("目录", titles)
        self.assertNotIn("方框1.1 示例侧栏", titles)
        self.assertNotIn("极短段落标题", titles)
        self.assertNotIn("短碎片标题", titles)
        self.assertIn("目录", filtered_titles)
        self.assertEqual(filtered_reasons["方框1.1 示例侧栏"], "sidebar_or_box")
        self.assertEqual(filtered_reasons["极短段落标题"], "level_too_deep")
        self.assertEqual(filtered_reasons["短碎片标题"], "too_short")

    def test_extract_toc_can_include_sidebars_when_requested(self):
        module = load_module()
        source = (
            "## 第一章 主章节\n"
            + "\n".join(f"正文 {index}" for index in range(20))
            + "\n\n"
            "### 方框1.1 示例侧栏\n"
            + "\n".join(f"侧栏内容 {index}" for index in range(20))
            + "\n"
        )

        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "complex_toc_sample.md"
            path.write_text(source, encoding="utf-8")
            toc = module.extract_toc(path, include_sidebars=True)

        titles = [entry["title"] for entry in toc["chapters"]]
        self.assertIn("第一章 主章节", titles)
        self.assertIn("方框1.1 示例侧栏", titles)


if __name__ == "__main__":
    unittest.main()
