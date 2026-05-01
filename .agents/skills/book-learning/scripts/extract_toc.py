#!/usr/bin/env python3
"""Extract Markdown headings as a TOC with line ranges."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text.strip().lower())
    return slug.strip("-") or "section"


def clean_title(title: str) -> str:
    title = re.sub(r"\s+#+\s*$", "", title.strip())
    return title.strip()


def extract_toc(markdown_path: Path) -> dict:
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

    return {"source": str(markdown_path), "chapters": headings}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract Markdown headings into TOC JSON.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.source.exists():
        raise SystemExit(f"Source file does not exist: {args.source}")
    toc = extract_toc(args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(toc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out} with {len(toc['chapters'])} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
