#!/usr/bin/env python3
"""Audit a canonical consolidated reading notes file against TOC JSON."""

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
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
LEGACY_MODE_SUGGESTED_FIELDS = {
    "mode-0-distillation": ("核心定义/主张", "核心结论", "source_backlink"),
    "mode-1-sop": ("执行步骤", "检查清单", "source_backlink"),
    "mode-2-scene-mapping": ("适用任务", "场景触发词", "使用动作", "source_backlink"),
    "mode-3-cognitive-refresh": ("旧认知", "新认知", "关键机制", "source_backlink"),
    "mode-4-communication-game": ("局面定义", "参与方", "关键变量", "source_backlink"),
}
GENERIC_SCENT_VALUES = {"book", "reading", "书籍", "阅读", "读书", "阅读笔记"}
EMPTY_TEMPLATE_PHRASES = (
    "...",
    "待补充",
    "用 1-2 句话",
    "说明其结构和含义",
    "输出字段 1",
    "Step 1",
    "检查项 1",
)


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


def extract_frontmatter_block(content: str) -> str:
    if not content.startswith("---\n"):
        return ""
    end = content.find("\n---", 4)
    if end == -1:
        return ""
    return content[4:end].strip()


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
        level = len(match.group(1))
        end = len(content)
        for next_match in matches[index + 1 :]:
            if len(next_match.group(1)) <= level:
                end = next_match.start()
                break
        title = clean_heading(match.group(2))
        sections.append(
            {
                "heading": title,
                "level": level,
                "start_line": content[:start].count("\n") + 1,
                "end_line": content[:end].count("\n") + 1,
                "text": content[start:end],
            }
        )
    return sections


def coverage_candidate_sections(sections: list[dict]) -> list[dict]:
    ignored = {"目录", "全书核心框架", "金句"}
    return [section for section in sections if section["level"] >= 2 and section["heading"] not in ignored]


def split_wikilink_target(target: str) -> tuple[str, str]:
    target = target.split("|", 1)[0].strip()
    if "#" not in target:
        return target, ""
    path, heading = target.split("#", 1)
    return path.strip(), heading.strip()


def raw_source_wikilinks(text: str) -> list[dict[str, str]]:
    links = []
    for match in WIKILINK_RE.finditer(text):
        path, heading = split_wikilink_target(match.group(1))
        normalized_path = path.replace("\\", "/")
        if "raw/books/" not in normalized_path:
            continue
        if ".cache/" in normalized_path or "/chapters/" in normalized_path or normalized_path.startswith("chapters/"):
            continue
        if not heading:
            continue
        links.append({"link": match.group(0), "path": path, "heading": heading})
    return links


def heading_matches_title(heading: str, title: str, normalized_is_ambiguous: bool = False) -> bool:
    normalized_heading = normalize_title(heading)
    normalized_title = normalize_title(title)
    if heading == title or title in heading:
        return True
    if normalized_is_ambiguous:
        return False
    return bool(normalized_heading and normalized_title and (normalized_heading == normalized_title or normalized_title in normalized_heading))


def raw_backlinks_for_title(text: str, title: str, normalized_is_ambiguous: bool = False) -> list[dict[str, str]]:
    return [
        link
        for link in raw_source_wikilinks(text)
        if heading_matches_title(link["heading"], title, normalized_is_ambiguous)
    ]


def section_has_required_field(section: str, field: str, title: str, normalized_is_ambiguous: bool = False) -> bool:
    if field == "source_backlink":
        return bool(raw_backlinks_for_title(section, title, normalized_is_ambiguous))
    if field == "核心定义/主张":
        return any(marker in section for marker in CORE_CLAIM_MARKERS)
    if field == "核心结论":
        return any(marker in section for marker in CORE_CONCLUSION_MARKERS)
    return field in section


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


def extract_scent_values(frontmatter_block: str) -> list[str]:
    values: list[str] = []
    in_scent = False
    for line in frontmatter_block.splitlines():
        stripped = line.strip()
        if stripped.startswith("scent:"):
            in_scent = True
            inline = stripped.split(":", 1)[1].strip()
            if inline.startswith("[") and inline.endswith("]"):
                values.extend(value.strip().strip("\"'") for value in inline[1:-1].split(",") if value.strip())
            continue
        if in_scent:
            if stripped.startswith("- "):
                values.append(stripped[2:].strip().strip("\"'"))
                continue
            if stripped and not line.startswith((" ", "\t")):
                in_scent = False
    return [value for value in values if value]


def chapter_sections_for_coverage(sections: list[dict], coverage_details: list[dict]) -> list[dict]:
    covered_by = {detail["covered_by"] for detail in coverage_details if detail.get("covered_by")}
    return [section for section in sections if section["heading"] in covered_by]


def detect_warning_issues(content: str, frontmatter_block: str, sections: list[dict], coverage_details: list[dict]) -> list[str]:
    warnings: list[str] = []
    chapter_sections = chapter_sections_for_coverage(sections, coverage_details)
    short_sections = [
        section["heading"]
        for section in chapter_sections
        if len([line for line in section["text"].splitlines() if line.strip()]) < 5
    ]
    if short_sections:
        warnings.append("Several covered chapter sections appear very short.")

    if any(phrase in content for phrase in EMPTY_TEMPLATE_PHRASES):
        warnings.append("Some sections still contain empty template-like phrases; replace prompts with real notes.")

    heading_patterns: dict[tuple[str, ...], int] = {}
    for section in chapter_sections:
        markers = tuple(re.findall(r"^\*\*(.+?)\*\*[:：]", section["text"], flags=re.MULTILINE))
        if markers:
            heading_patterns[markers] = heading_patterns.get(markers, 0) + 1
    if any(count >= 2 and len(pattern) >= 3 for pattern, count in heading_patterns.items()):
        warnings.append("The same structure is repeated across chapters; consider a more content-driven structure.")

    if not any(marker in content for marker in ("证据", "案例", "数据", "研究", "推理")):
        warnings.append("No obvious evidence, example, data, study, or reasoning section was found.")

    html_card_count = content.count("<div style=")
    if chapter_sections and html_card_count > max(6, len(chapter_sections) * 3):
        warnings.append("HTML cards may be overused; plain Markdown is acceptable when it preserves the book logic better.")

    scent_values = extract_scent_values(frontmatter_block)
    if "scent:" not in frontmatter_block:
        warnings.append("Scent tags are missing; add useful Chinese, English, or custom routing tags when possible.")
    elif scent_values and all(value.lower() in GENERIC_SCENT_VALUES for value in scent_values):
        warnings.append("Scent tags look too generic; prefer tags tied to methods, problem types, or usage scenes.")

    if "research_context" in frontmatter_block or "research_context" in content:
        if "外部背景" not in content and "Research Context" not in content:
            warnings.append("Research context is referenced but not clearly separated from source-grounded reading.")

    return warnings


def find_coverage_for_toc_item(
    toc_item: dict,
    sections: list[dict],
    ambiguous_normalized_titles: set[str] | None = None,
) -> dict:
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
        if raw_backlinks_for_title(section["text"], title, normalized_is_ambiguous):
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
    raw_source_path: Path | None = None,
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
            "hard_checks": {"frontmatter": False, "chapter_coverage": False, "backlinks": False},
            "warnings": ["Reading notes file does not exist."],
            "has_core_framework": False,
            "has_quotes": False,
            "passed": False,
        }

    content = reading_notes_path.read_text(encoding="utf-8")
    frontmatter = extract_frontmatter(content)
    frontmatter_block = extract_frontmatter_block(content)
    missing_fields = [field for field in REQUIRED_FRONTMATTER_FIELDS if field not in frontmatter]
    sections = extract_headings_and_sections(content)

    missing_chapters = []
    missing_core_claim = []
    missing_core_conclusion = []
    missing_backlinks = []
    missing_mode_required_fields = []
    coverage_details = []
    reading_mode = frontmatter.get("reading_mode", "").strip().strip('"')
    required_mode_fields = LEGACY_MODE_SUGGESTED_FIELDS.get(reading_mode, ())

    for entry in chapters:
        title = entry["title"]
        normalized_is_ambiguous = normalize_title(title) in ambiguous_normalized_titles
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
            if required_mode_fields:
                missing_mode_required_fields.append({"id": entry["id"], "missing_fields": list(required_mode_fields)})
            continue
        if not any(marker in section for marker in CORE_CLAIM_MARKERS):
            missing_core_claim.append(entry["id"])
        if not any(marker in section for marker in CORE_CONCLUSION_MARKERS):
            missing_core_conclusion.append(entry["id"])
        if not raw_backlinks_for_title(section, title, normalized_is_ambiguous):
            missing_backlinks.append(entry["id"])
        if required_mode_fields:
            missing_fields_for_section = [
                field
                for field in required_mode_fields
                if not section_has_required_field(section, field, title, normalized_is_ambiguous)
            ]
            if missing_fields_for_section:
                missing_mode_required_fields.append({"id": entry["id"], "missing_fields": missing_fields_for_section})

    heading_titles = {section["heading"] for section in sections}
    has_core_framework = "全书核心框架" in heading_titles
    has_quotes = "金句" in heading_titles
    format_issues = check_formatting(content)
    warnings = detect_warning_issues(content, frontmatter_block, sections, coverage_details)
    if format_issues:
        warnings.append("Markdown or HTML formatting issues were found; review format_issues for details.")
    if missing_core_claim:
        warnings.append("Some chapters do not use the legacy 核心定义/主张 marker; this is allowed for content-driven notes.")
    if missing_core_conclusion:
        warnings.append("Some chapters do not use the legacy 核心结论 marker; this is allowed for content-driven notes.")
    if missing_mode_required_fields:
        warnings.append("Some legacy reading_mode suggested fields are missing; treat this as a template guidance warning, not a failure.")
    if not has_core_framework:
        warnings.append("No 全书核心框架 section was found; add one only if it improves the note.")
    if not has_quotes:
        warnings.append("No 金句 section was found; add quotes only when they are useful and source-grounded.")
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
        "reading_mode": reading_mode or None,
        "mode_required_fields": list(required_mode_fields),
        "mode_required_fields_passed": not missing_mode_required_fields,
        "chapters_missing_mode_required_fields": missing_mode_required_fields,
        "has_core_framework": has_core_framework,
        "has_quotes": has_quotes,
        "hard_checks": {
            "frontmatter": not missing_fields,
            "chapter_coverage": not missing_chapters,
            "backlinks": not missing_backlinks,
        },
        "warnings": warnings,
    }
    report["passed"] = all(
        [
            report["reading_notes_exists"],
            report["frontmatter_passed"],
            report["chapter_coverage_passed"],
            report["backlinks_passed"],
        ]
    )
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit canonical consolidated reading notes against TOC JSON.")
    parser.add_argument("--toc", type=Path, required=True, help="TOC JSON, usually .cache/book-learning/{book_slug}/toc.json")
    parser.add_argument("--reading-notes", type=Path, required=True, help="Canonical reading notes path")
    parser.add_argument("--raw-source", type=Path, help="Raw source Markdown, usually raw/books/{book_slug}/{book_slug}.md")
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
        args.raw_source,
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
