#!/usr/bin/env python3
"""Audit TOC entries against chapter files and note files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

MIN_NOTE_CHARS = 200


def expected_chapter_name(entry: dict) -> str:
    return f"{entry['id']}-{entry['slug']}.md"


def expected_note_name(entry: dict) -> str:
    return f"{entry['id']}-{entry['slug']}.notes.md"


def incomplete_note_names(notes_dir: Path | None, expected_notes: set[str], min_chars: int = MIN_NOTE_CHARS) -> list[str]:
    if not notes_dir or not notes_dir.exists():
        return []

    incomplete = []
    for name in sorted(expected_notes):
        path = notes_dir / name
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8").strip()
        if len(content) < min_chars:
            incomplete.append(name)
    return incomplete


def audit(toc_path: Path, chapters_dir: Path, notes_dir: Path | None = None) -> dict:
    toc = json.loads(toc_path.read_text(encoding="utf-8"))
    entries = toc.get("chapters", [])
    expected_chapters = {expected_chapter_name(entry) for entry in entries}
    actual_chapters = {path.name for path in chapters_dir.glob("*.md")} if chapters_dir.exists() else set()

    expected_notes = {expected_note_name(entry) for entry in entries}
    actual_notes = set()
    if notes_dir and notes_dir.exists():
        actual_notes = {path.name for path in notes_dir.glob("*.notes.md")}

    missing_chapters = sorted(expected_chapters - actual_chapters)
    extra_chapter_files = sorted(actual_chapters - expected_chapters)
    missing_notes = sorted(expected_notes - actual_notes) if notes_dir else []
    incomplete_notes = incomplete_note_names(notes_dir, expected_notes - set(missing_notes))

    structural_passed = not missing_chapters and not extra_chapter_files and not missing_notes
    content_passed = not incomplete_notes

    status = "pass" if structural_passed and content_passed else "fail"
    return {
        "status": status,
        "structural_passed": structural_passed,
        "content_passed": content_passed,
        "toc_count": len(entries),
        "chapter_file_count": len(actual_chapters),
        "note_file_count": len(actual_notes),
        "missing_chapters": missing_chapters,
        "extra_chapter_files": extra_chapter_files,
        "missing_notes": missing_notes,
        "incomplete_notes": incomplete_notes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit chapter and note coverage against TOC JSON.")
    parser.add_argument("--toc", type=Path, required=True)
    parser.add_argument("--chapters", type=Path, required=True)
    parser.add_argument("--notes", type=Path)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.toc.exists():
        raise SystemExit(f"TOC file does not exist: {args.toc}")
    report = audit(args.toc, args.chapters, args.notes)
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(output, end="")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
