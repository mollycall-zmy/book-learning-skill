import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/book-learning/scripts/convert_to_md.py"


def load_module():
    spec = importlib.util.spec_from_file_location("convert_to_md", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConvertToMarkdownTest(unittest.TestCase):
    def test_markdown_to_markdown_copy(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source.md"
            target = tmp_path / "out" / "converted.md"
            source.write_text("# Synthetic Test\n\nThis is local test content.\n", encoding="utf-8")

            module.convert(source, target)

            self.assertTrue(target.exists())
            content = target.read_text(encoding="utf-8")
            self.assertIn("# Synthetic Test", content)
            self.assertIn("This is local test content.", content)


if __name__ == "__main__":
    unittest.main()
