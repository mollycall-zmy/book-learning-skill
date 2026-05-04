import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/book-learning/scripts/path_routing.py"


def load_module():
    spec = importlib.util.spec_from_file_location("path_routing", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PathRoutingTest(unittest.TestCase):
    def test_canonical_notes_path_uses_matched_knowledge_subdir(self):
        module = load_module()
        path = module.canonical_notes_path(
            book_slug="示例书",
            knowledge_root=Path("/tmp/example-knowledge-root"),
            matched_knowledge_subdir="{matched_knowledge_subdir}",
        )

        self.assertEqual(
            path.as_posix(),
            "/tmp/example-knowledge-root/L1-事实与语义/02-📚 知识/{matched_knowledge_subdir}/示例书-阅读笔记.md",
        )

    def test_canonical_notes_path_requires_subdir_unless_root_fallback_allowed(self):
        module = load_module()
        with self.assertRaises(ValueError):
            module.canonical_notes_path(book_slug="示例书", knowledge_root=Path("/tmp/example-knowledge-root"))

    def test_canonical_notes_path_can_fallback_to_outputs_without_knowledge_root(self):
        module = load_module()
        path = module.canonical_notes_path(book_slug="示例书")

        self.assertEqual(path.as_posix(), "outputs/reading_notes.md")

    def test_list_knowledge_subdirs_reads_direct_children_only(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            category_root = root / "L1-事实与语义" / "02-📚 知识"
            (category_root / "学习方法").mkdir(parents=True)
            (category_root / "思维与认知").mkdir()
            (category_root / "学习方法" / "二级目录").mkdir()

            subdirs = [path.name for path in module.list_knowledge_subdirs(root)]

            self.assertEqual(subdirs, ["学习方法", "思维与认知"])

    def test_mode_1_sop_matches_method_like_subdir(self):
        module = load_module()
        subdirs = [Path(name) for name in ["行业案例", "学习方法", "跨界灵感"]]

        match = module.match_knowledge_subdir(subdirs, reading_mode="mode-1-sop")

        self.assertEqual(match["matched_knowledge_subdir"], "学习方法")
        self.assertEqual(match["confidence"], "medium")

    def test_user_category_wins_when_present(self):
        module = load_module()
        subdirs = [Path(name) for name in ["行业案例", "学习方法", "跨界灵感"]]

        match = module.match_knowledge_subdir(subdirs, reading_mode="mode-1-sop", user_category="跨界灵感")

        self.assertEqual(match["matched_knowledge_subdir"], "跨界灵感")
        self.assertEqual(match["confidence"], "high")


if __name__ == "__main__":
    unittest.main()
