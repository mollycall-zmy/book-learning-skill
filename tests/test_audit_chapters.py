import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTRACT_SCRIPT = ROOT / ".agents/skills/book-learning/scripts/extract_toc.py"
SPLIT_SCRIPT = ROOT / ".agents/skills/book-learning/scripts/split_chapters.py"
AUDIT_SCRIPT = ROOT / ".agents/skills/book-learning/scripts/audit_chapters.py"
SAMPLE = ROOT / "examples/sample_book.md"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuditChaptersTest(unittest.TestCase):
    def test_audit_detects_missing_notes(self):
        extract_toc = load_module("extract_toc", EXTRACT_SCRIPT)
        split_chapters = load_module("split_chapters", SPLIT_SCRIPT)
        audit_chapters = load_module("audit_chapters", AUDIT_SCRIPT)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc = extract_toc.extract_toc(SAMPLE)
            toc_path = tmp_path / "toc.json"
            toc_path.write_text(json.dumps(toc), encoding="utf-8")

            chapters_dir = tmp_path / "chapters"
            notes_dir = tmp_path / "notes"
            notes_dir.mkdir()
            split_chapters.split_chapters(SAMPLE, toc_path, chapters_dir)

            report = audit_chapters.audit(toc_path, chapters_dir, notes_dir)

            self.assertEqual(report["status"], "fail")
            self.assertFalse(report["structural_passed"])
            self.assertEqual(report["toc_count"], 12)
            self.assertEqual(report["chapter_file_count"], 12)
            self.assertEqual(len(report["missing_notes"]), 12)
            self.assertEqual(report["incomplete_notes"], [])

    def test_audit_detects_incomplete_notes(self):
        extract_toc = load_module("extract_toc", EXTRACT_SCRIPT)
        split_chapters = load_module("split_chapters", SPLIT_SCRIPT)
        audit_chapters = load_module("audit_chapters", AUDIT_SCRIPT)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc = extract_toc.extract_toc(SAMPLE)
            toc_path = tmp_path / "toc.json"
            toc_path.write_text(json.dumps(toc), encoding="utf-8")

            chapters_dir = tmp_path / "chapters"
            notes_dir = tmp_path / "notes"
            notes_dir.mkdir()
            split_chapters.split_chapters(SAMPLE, toc_path, chapters_dir)

            for entry in toc["chapters"]:
                note = notes_dir / f"{entry['id']}-{entry['slug']}.notes.md"
                note.write_text("# Note\n", encoding="utf-8")

            report = audit_chapters.audit(toc_path, chapters_dir, notes_dir)

            self.assertEqual(report["status"], "fail")
            self.assertTrue(report["structural_passed"])
            self.assertFalse(report["content_passed"])
            self.assertEqual(len(report["incomplete_notes"]), 12)

    def test_audit_passes_with_complete_notes(self):
        extract_toc = load_module("extract_toc", EXTRACT_SCRIPT)
        split_chapters = load_module("split_chapters", SPLIT_SCRIPT)
        audit_chapters = load_module("audit_chapters", AUDIT_SCRIPT)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            toc = extract_toc.extract_toc(SAMPLE)
            toc_path = tmp_path / "toc.json"
            toc_path.write_text(json.dumps(toc), encoding="utf-8")

            chapters_dir = tmp_path / "chapters"
            notes_dir = tmp_path / "notes"
            notes_dir.mkdir()
            split_chapters.split_chapters(SAMPLE, toc_path, chapters_dir)

            note_body = (
                "# Note\n\n"
                "## Core Questions\nWhat does this section explain?\n\n"
                "## Main Claims\nThe section develops a concrete learning point with context.\n\n"
                "## Evidence / Cases / Examples\nIt includes an example, evidence trail, and source-aware details for audit.\n\n"
                "## Important Details\nDefinitions, caveats, and reusable observations are preserved.\n"
            )
            for entry in toc["chapters"]:
                note = notes_dir / f"{entry['id']}-{entry['slug']}.notes.md"
                note.write_text(note_body, encoding="utf-8")

            report = audit_chapters.audit(toc_path, chapters_dir, notes_dir)

            self.assertEqual(report["status"], "pass")
            self.assertTrue(report["structural_passed"])
            self.assertTrue(report["content_passed"])
            self.assertEqual(report["missing_chapters"], [])
            self.assertEqual(report["missing_notes"], [])
            self.assertEqual(report["incomplete_notes"], [])


if __name__ == "__main__":
    unittest.main()
