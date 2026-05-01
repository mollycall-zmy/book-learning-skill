import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTRACT_SCRIPT = ROOT / ".agents/skills/book-learning/scripts/extract_toc.py"
SPLIT_SCRIPT = ROOT / ".agents/skills/book-learning/scripts/split_chapters.py"
SAMPLE = ROOT / "examples/sample_book.md"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SplitChaptersTest(unittest.TestCase):
    def test_split_chapters_writes_expected_files(self):
        extract_toc = load_module("extract_toc", EXTRACT_SCRIPT)
        split_chapters = load_module("split_chapters", SPLIT_SCRIPT)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc_path = tmp_path / "toc.json"
            toc = extract_toc.extract_toc(SAMPLE, min_lines=0, max_level=6, include_sidebars=True, include_toc_heading=True)
            toc_path.write_text(json.dumps(toc), encoding="utf-8")

            out_dir = tmp_path / "chapters"
            written = split_chapters.split_chapters(SAMPLE, toc_path, out_dir)

            self.assertEqual(len(written), len(toc["chapters"]))
            first = out_dir / "001-the-orchard-of-useful-questions.md"
            self.assertTrue(first.exists())
            self.assertTrue(first.read_text(encoding="utf-8").startswith("# The Orchard Of Useful Questions"))


if __name__ == "__main__":
    unittest.main()
