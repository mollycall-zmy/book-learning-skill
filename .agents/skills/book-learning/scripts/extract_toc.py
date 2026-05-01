#!/usr/bin/env python3
"""Extract Markdown headings as a TOC with line ranges."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SIDEBAR_PREFIXES = ("方框", "box", "sidebar")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text.strip().lower())
    return slug.strip("-") or "section"


def clean_title(title: str) -> str:
    title = re.sub(r"\s+#+\s*$", "", title.strip())
    return title.strip()


def decorative_title(title: str) -> bool:
    return not re.search(r"[a-zA-Z0-9\u4e00-\u9fff]", title)


def filter_reason(
    item: dict,
    *,
    min_lines: int = 15,
    max_level: int = 3,
    include_sidebars: bool = False,
    include_toc_heading: bool = False,
) -> str | None:
    title = item.get("title", "").strip()
    normalized = title.lower()
    line_count = int(item.get("line_count", 0))

    if not title or decorative_title(title):
        return "empty_or_decorative"
    if not include_toc_heading and "目录" in title:
        return "toc_heading"
    if not include_sidebars and (title.startswith("方框") or normalized.startswith(("box", "sidebar"))):
        return "sidebar_or_box"
    if int(item.get("level", 1)) > max_level:
        return "level_too_deep"
    if line_count < min_lines:
        return "too_short"
    return None


def should_include_toc_item(
    item: dict,
    *,
    min_lines: int = 15,
    max_level: int = 3,
    include_sidebars: bool = False,
    include_toc_heading: bool = False,
) -> bool:
    return (
        filter_reason(
            item,
            min_lines=min_lines,
            max_level=max_level,
            include_sidebars=include_sidebars,
            include_toc_heading=include_toc_heading,
        )
        is None
    )


def raw_toc_items(markdown_path: Path) -> list[dict]:
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    headings = []

    for index, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = clean_title(match.group(2))
        headings.append(
            {
                "id": f"{len(headings) + 1:03d}",
                "title": title,
                "level": level,
                "start_line": index,
                "end_line": len(lines),
                "slug": slugify(title),
            }
        )

    for index, heading in enumerate(headings):
        if index + 1 < len(headings):
            heading["end_line"] = headings[index + 1]["start_line"] - 1
        heading["line_count"] = heading["end_line"] - heading["start_line"] + 1

    return headings


def filter_toc_items(
    items: list[dict],
    *,
    min_lines: int = 15,
    max_level: int = 3,
    include_sidebars: bool = False,
    include_toc_heading: bool = False,
) -> tuple[list[dict], list[dict]]:
    chapters = []
    filtered_out = []
    for item in items:
        reason = filter_reason(
            item,
            min_lines=min_lines,
            max_level=max_level,
            include_sidebars=include_sidebars,
            include_toc_heading=include_toc_heading,
        )
        if reason:
            filtered = dict(item)
            filtered["reason"] = reason
            filtered_out.append(filtered)
        else:
            chapter = dict(item)
            chapter["id"] = f"{len(chapters) + 1:03d}"
            chapters.append(chapter)
    return chapters, filtered_out


def main_chapters_from_toc(
    toc: dict,
    *,
    min_lines: int = 15,
    max_level: int = 3,
    include_sidebars: bool = False,
    include_toc_heading: bool = False,
) -> tuple[list[dict], list[dict]]:
    items = []
    for item in toc.get("chapters", []):
        normalized = dict(item)
        if "line_count" not in normalized and "start_line" in normalized and "end_line" in normalized:
            normalized["line_count"] = int(normalized["end_line"]) - int(normalized["start_line"]) + 1
        items.append(normalized)
    return filter_toc_items(
        items,
        min_lines=min_lines,
        max_level=max_level,
        include_sidebars=include_sidebars,
        include_toc_heading=include_toc_heading,
    )


def extract_toc(
    markdown_path: Path,
    *,
    min_lines: int = 15,
    max_level: int = 3,
    include_sidebars: bool = False,
    include_toc_heading: bool = False,
) -> dict:
    items = raw_toc_items(markdown_path)
    chapters, filtered_out = filter_toc_items(
        items,
        min_lines=min_lines,
        max_level=max_level,
        include_sidebars=include_sidebars,
        include_toc_heading=include_toc_heading,
    )
    return {
        "source": str(markdown_path),
        "chapters": chapters,
        "filtered_out": filtered_out,
        "filters": {
            "min_lines": min_lines,
            "max_level": max_level,
            "include_sidebars": include_sidebars,
            "include_toc_heading": include_toc_heading,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract Markdown headings into TOC JSON.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--min-lines", type=int, default=15)
    parser.add_argument("--max-level", type=int, default=3)
    parser.add_argument("--include-sidebars", action="store_true")
    parser.add_argument("--include-toc-heading", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.source.exists():
        raise SystemExit(f"Source file does not exist: {args.source}")
    toc = extract_toc(
        args.source,
        min_lines=args.min_lines,
        max_level=args.max_level,
        include_sidebars=args.include_sidebars,
        include_toc_heading=args.include_toc_heading,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(toc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out} with {len(toc['chapters'])} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
