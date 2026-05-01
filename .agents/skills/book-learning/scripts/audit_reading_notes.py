#!/usr/bin/env python3
"""Audit a consolidated reading_notes.md file against TOC JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_toc import main_chapters_from_toc  # noqa: E402


REQUIRED_FRONTMATTER_FIELDS = ("aliases", "tags", "author", "source", "created")
CORE_CLAIM_MARKERS = ("核心定义/主张", "核心主张")
CORE_CONCLUSION_MARKERS = ("核心结论",)
BACKLINK_RE = re.compile(r"\[\[raw/books/[^#\]]+#[^\]]+\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


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


def clean_heading(title: str) -> str:
    return re.sub(r"\s+#+\s*$", "", title.strip()).strip()


def strip_numbering_prefix(title: str) -> str:
    title = clean_heading(title)
    patterns = [
        r"^第[一二三四五六七八九十百千万零〇两\d]+[章节篇部]\s*",
        r"^第\s*[一二三四五六七八九十百千万零〇两\d]+\s*[章节篇部]\s*",
        r"^(chapter|section)\s+\d+[\s:：.\-—–]*",
        r"^\d+(\.\d+)*[\s:：.\-—–]+",
    ]
    for pattern in patterns:
        title = re.sub(pattern, "", title, flags=re.IGNORECASE)
    return title.strip()


def normalize_title(title: str) -> str:
    title = strip_numbering_prefix(title)
    title = re.sub(r"[*_`#>\[\]（）()]", "", title)
    title = re.sub(r"[\s\u3000]+", " ", title)
    title = re.sub(r"^[：:—–\-]+|[：:—–\-]+$", "", title)
    return title.strip().lower()


def extract_headings_and_sections(content: str) -> list[dict]:
    matches = list(HEADING_RE.finditer(content))
    sections = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        title = clean_heading(match.group(2))
        sections.append(
            {
                "heading": title,
                "level": len(match.group(1)),
                "start_line": content[:start].count("\n") + 1,
                "end_line": content[:end].count("\n") + 1,
                "text": content[start:end],
            }
        )
    return sections


def coverage_candidate_sections(sections: list[dict]) -> list[dict]:
    ignored = {"目录", "全书核心框架", "金句"}
    return [section for section in sections if section["level"] >= 2 and section["heading"] not in ignored]


def backlinks_in_text(text: str) -> list[str]:
    return BACKLINK_RE.findall(text)


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and "|" in stripped[1:-1]


def check_table_formatting(content: str) -> list[str]:
    """Check common table formatting issues that break rendering."""
    issues = []
    lines = content.split("\n")

    for index, line in enumerate(lines):
        stripped = line.strip()
        table_row = is_table_row(line)

        if line.lstrip().startswith("> |") and "|" in line:
            issues.append(f"Line {index + 1}: table row appears inside a callout block")

        if table_row:
            if line != stripped:
                issues.append(f"Line {index + 1}: table row is indented and may not render correctly")

            if index > 0:
                previous = lines[index - 1].strip()
                if previous.startswith("- ") or previous.startswith("* "):
                    issues.append(f"Line {index + 1}: table row immediately follows a list item; add a blank line before the table")

    return issues


def check_mermaid_formatting(content: str) -> list[str]:
    """Check common Mermaid formatting issues that break rendering."""
    issues = []
    lines = content.split("\n")

    for index, line in enumerate(lines):
        stripped = line.strip()
        if line.lstrip().startswith("> ```mermaid"):
            issues.append(f"Line {index + 1}: Mermaid block appears inside a callout block")
            continue

        if stripped != "```mermaid":
            continue

        if line != stripped:
            issues.append(f"Line {index + 1}: Mermaid block is indented and may not render correctly")

        if index > 0 and lines[index - 1].strip():
            issues.append(f"Line {index + 1}: add a blank line before the Mermaid block")

    return issues


def check_formatting(content: str) -> list[str]:
    return check_table_formatting(content) + check_mermaid_formatting(content)


def find_coverage_for_toc_item(toc_item: dict, sections: list[dict], ambiguous_normalized_titles: set[str] | None = None) -> dict:
    title = toc_item["title"]
    normalized = normalize_title(title)
    ambiguous_normalized_titles = ambiguous_normalized_titles or set()
    normalized_is_ambiguous = normalized in ambiguous_normalized_titles
    candidates = coverage_candidate_sections(sections)

    for section in candidates:
        if section["heading"] == title:
            return {"covered": True, "matched_by": "exact", "covered_by": section["heading"], "section": section}

    if not normalized_is_ambiguous:
        for section in candidates:
            if normalized and normalize_title(section["heading"]) == normalized:
                return {"covered": True, "matched_by": "normalized_heading", "covered_by": section["heading"], "section": section}

    for section in candidates:
        for backlink in backlinks_in_text(section["text"]):
            if title in backlink or (not normalized_is_ambiguous and normalized and normalized in normalize_title(backlink)):
                return {"covered": True, "matched_by": "backlink", "covered_by": section["heading"], "section": section}

    if not normalized_is_ambiguous:
        for section in candidates:
            if normalized and normalized in normalize_title(section["text"]):
                return {"covered": True, "matched_by": "keyword", "covered_by": section["heading"], "section": section}

    return {"covered": False, "matched_by": None, "covered_by": None, "section": None}


def section_for_title(content: str, title: str, all_titles: list[str] | None = None) -> str:
    sections = extract_headings_and_sections(content)
    match = find_coverage_for_toc_item({"title": title}, sections)
    return match["section"]["text"] if match["covered"] else ""


def audit_reading_notes(
    toc_path: Path,
    reading_notes_path: Path,
    *,
    min_lines: int = 15,
    max_level: int = 3,
    include_sidebars: bool = False,
) -> dict:
    toc = json.loads(toc_path.read_text(encoding="utf-8"))
    chapters, filtered_out = main_chapters_from_toc(
        toc,
        min_lines=min_lines,
        max_level=max_level,
        include_sidebars=include_sidebars,
        include_toc_heading=False,
    )
    titles = [entry["title"] for entry in chapters]
    normalized_counts: dict[str, int] = {}
    for title in titles:
        normalized = normalize_title(title)
        if normalized:
            normalized_counts[normalized] = normalized_counts.get(normalized, 0) + 1
    ambiguous_normalized_titles = {title for title, count in normalized_counts.items() if count > 1}

    if not reading_notes_path.exists():
        return {
            "reading_notes_exists": False,
            "checked_chapters": len(chapters),
            "filtered_out_count": len(filtered_out),
            "frontmatter_passed": False,
            "missing_frontmatter_fields": list(REQUIRED_FRONTMATTER_FIELDS),
            "chapter_coverage_passed": False,
            "missing_chapters": [entry["id"] for entry in chapters],
            "core_claims_passed": False,
            "chapters_missing_core_claim": [entry["id"] for entry in chapters],
            "core_conclusions_passed": False,
            "chapters_missing_core_conclusion": [entry["id"] for entry in chapters],
            "backlinks_passed": False,
            "chapters_missing_backlinks": [entry["id"] for entry in chapters],
            "format_issues": [],
            "has_core_framework": False,
            "has_quotes": False,
            "passed": False,
        }

    content = reading_notes_path.read_text(encoding="utf-8")
    frontmatter = extract_frontmatter(content)
    missing_fields = [field for field in REQUIRED_FRONTMATTER_FIELDS if field not in frontmatter]
    sections = extract_headings_and_sections(content)

    missing_chapters = []
    missing_core_claim = []
    missing_core_conclusion = []
    missing_backlinks = []
    coverage_details = []

    for entry in chapters:
        title = entry["title"]
        coverage = find_coverage_for_toc_item(entry, sections, ambiguous_normalized_titles)
        coverage_details.append(
            {
                "id": entry["id"],
                "title": title,
                "covered": coverage["covered"],
                "matched_by": coverage["matched_by"],
                "covered_by": coverage["covered_by"],
            }
        )
        section = coverage["section"]["text"] if coverage["covered"] else ""
        if not coverage["covered"]:
            missing_chapters.append(entry["id"])
            missing_core_claim.append(entry["id"])
            missing_core_conclusion.append(entry["id"])
            missing_backlinks.append(entry["id"])
            continue
        if not any(marker in section for marker in CORE_CLAIM_MARKERS):
            missing_core_claim.append(entry["id"])
        if not any(marker in section for marker in CORE_CONCLUSION_MARKERS):
            missing_core_conclusion.append(entry["id"])
        if not BACKLINK_RE.search(section):
            missing_backlinks.append(entry["id"])

    heading_titles = {section["heading"] for section in sections}
    has_core_framework = "全书核心框架" in heading_titles
    has_quotes = "金句" in heading_titles
    format_issues = check_formatting(content)
    report = {
        "reading_notes_exists": True,
        "checked_chapters": len(chapters),
        "covered_chapters": len(chapters) - len(missing_chapters),
        "filtered_out_count": len(filtered_out),
        "frontmatter_passed": not missing_fields,
        "missing_frontmatter_fields": missing_fields,
        "chapter_coverage_passed": not missing_chapters,
        "missing_chapters": missing_chapters,
        "core_claims_passed": not missing_core_claim,
        "chapters_missing_core_claim": missing_core_claim,
        "core_conclusions_passed": not missing_core_conclusion,
        "chapters_missing_core_conclusion": missing_core_conclusion,
        "backlinks_passed": not missing_backlinks,
        "chapters_missing_backlinks": missing_backlinks,
        "format_issues": format_issues,
        "coverage_details": coverage_details,
        "has_core_framework": has_core_framework,
        "has_quotes": has_quotes,
    }
    report["passed"] = all(
        [
            report["reading_notes_exists"],
            report["frontmatter_passed"],
            report["chapter_coverage_passed"],
            report["core_claims_passed"],
            report["core_conclusions_passed"],
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
    parser.add_argument("--min-lines", type=int, default=15)
    parser.add_argument("--max-level", type=int, default=3)
    parser.add_argument("--include-sidebars", action="store_true")
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.toc.exists():
        raise SystemExit(f"TOC file does not exist: {args.toc}")
    report = audit_reading_notes(
        args.toc,
        args.reading_notes,
        min_lines=args.min_lines,
        max_level=args.max_level,
        include_sidebars=args.include_sidebars,
    )
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
