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
        toc = module.extract_toc(SAMPLE)

        self.assertTrue(toc["source"].endswith("examples/sample_book.md"))
        self.assertEqual(len(toc["chapters"]), 12)
        self.assertEqual(toc["chapters"][0]["title"], "The Orchard Of Useful Questions")
        self.assertEqual(toc["chapters"][0]["level"], 1)
        self.assertEqual(toc["chapters"][0]["start_line"], 1)
        self.assertLess(toc["chapters"][0]["end_line"], toc["chapters"][1]["start_line"])
        self.assertTrue(all(entry["end_line"] >= entry["start_line"] for entry in toc["chapters"]))


if __name__ == "__main__":
    unittest.main()
