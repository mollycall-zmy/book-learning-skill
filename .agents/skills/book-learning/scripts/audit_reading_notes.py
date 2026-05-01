#!/usr/bin/env python3
"""Audit a consolidated reading_notes.md file against TOC JSON."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_FRONTMATTER_FIELDS = ("aliases", "tags", "author", "source", "created")
AI_MARKERS = ("AI 分析", "AI Analysis")
BACKLINK_RE = re.compile(r"\[\[raw/books/[^#\]]+#[^\]]+\]\]")


def extract_frontmatter(content: str) -> dict[str, str]:
    if not content.startswith("---\n"):
        return {}
    end = content.find("\n---", 4)
    if end == -1:
        return {}
    block = content[4:end].strip()
    fields = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def section_for_title(content: str, title: str, all_titles: list[str]) -> str:
    escaped = re.escape(title)
    match = re.search(rf"^##+\s+{escaped}\s*$", content, flags=re.MULTILINE)
    if not match:
        return ""

    next_starts = []
    for other in all_titles:
        if other == title:
            continue
        other_match = re.search(rf"^##+\s+{re.escape(other)}\s*$", content[match.end() :], flags=re.MULTILINE)
        if other_match:
            next_starts.append(match.end() + other_match.start())
    end = min(next_starts) if next_starts else len(content)
    return content[match.start() : end]


def audit_reading_notes(toc_path: Path, reading_notes_path: Path) -> dict:
    toc = json.loads(toc_path.read_text(encoding="utf-8"))
    chapters = toc.get("chapters", [])
    titles = [entry["title"] for entry in chapters]

    if not reading_notes_path.exists():
        return {
            "reading_notes_exists": False,
            "frontmatter_passed": False,
            "missing_frontmatter_fields": list(REQUIRED_FRONTMATTER_FIELDS),
            "chapter_coverage_passed": False,
            "missing_chapters": [entry["id"] for entry in chapters],
            "core_claims_passed": False,
            "chapters_missing_core_claim": [entry["id"] for entry in chapters],
            "ai_analysis_passed": False,
            "chapters_missing_ai_analysis": [entry["id"] for entry in chapters],
            "backlinks_passed": False,
            "chapters_missing_backlinks": [entry["id"] for entry in chapters],
            "has_core_framework": False,
            "has_quotes": False,
            "passed": False,
        }

    content = reading_notes_path.read_text(encoding="utf-8")
    frontmatter = extract_frontmatter(content)
    missing_fields = [field for field in REQUIRED_FRONTMATTER_FIELDS if field not in frontmatter]

    missing_chapters = []
    missing_core_claim = []
    missing_ai = []
    missing_backlinks = []

    for entry in chapters:
        title = entry["title"]
        section = section_for_title(content, title, titles)
        if not section:
            missing_chapters.append(entry["id"])
            missing_core_claim.append(entry["id"])
            missing_ai.append(entry["id"])
            missing_backlinks.append(entry["id"])
            continue
        if "核心主张" not in section:
            missing_core_claim.append(entry["id"])
        if not any(marker in section for marker in AI_MARKERS):
            missing_ai.append(entry["id"])
        if not BACKLINK_RE.search(section):
            missing_backlinks.append(entry["id"])

    has_core_framework = "全书核心框架" in content
    has_quotes = "金句" in content
    report = {
        "reading_notes_exists": True,
        "frontmatter_passed": not missing_fields,
        "missing_frontmatter_fields": missing_fields,
        "chapter_coverage_passed": not missing_chapters,
        "missing_chapters": missing_chapters,
        "core_claims_passed": not missing_core_claim,
        "chapters_missing_core_claim": missing_core_claim,
        "ai_analysis_passed": not missing_ai,
        "chapters_missing_ai_analysis": missing_ai,
        "backlinks_passed": not missing_backlinks,
        "chapters_missing_backlinks": missing_backlinks,
        "has_core_framework": has_core_framework,
        "has_quotes": has_quotes,
    }
    report["passed"] = all(
        [
            report["reading_notes_exists"],
            report["frontmatter_passed"],
            report["chapter_coverage_passed"],
            report["core_claims_passed"],
            report["ai_analysis_passed"],
            report["backlinks_passed"],
            report["has_core_framework"],
            report["has_quotes"],
        ]
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit consolidated reading notes against TOC JSON.")
    parser.add_argument("--toc", type=Path, required=True)
    parser.add_argument("--reading-notes", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.toc.exists():
        raise SystemExit(f"TOC file does not exist: {args.toc}")
    report = audit_reading_notes(args.toc, args.reading_notes)
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(output, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
