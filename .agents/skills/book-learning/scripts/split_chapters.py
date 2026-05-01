#!/usr/bin/env python3
"""Split a Markdown book into chapter files using TOC JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def chapter_filename(entry: dict) -> str:
    return f"{entry['id']}-{entry['slug']}.md"


def split_chapters(markdown_path: Path, toc_path: Path, output_dir: Path) -> list[Path]:
    lines = markdown_path.read_text(encoding="utf-8").splitlines()
    toc = json.loads(toc_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for entry in toc.get("chapters", []):
        start = max(int(entry["start_line"]) - 1, 0)
        end = min(int(entry["end_line"]), len(lines))
        content = "\n".join(lines[start:end]).rstrip() + "\n"
        target = output_dir / chapter_filename(entry)
        target.write_text(content, encoding="utf-8")
        written.append(target)

    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Split Markdown chapters from TOC JSON.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--toc", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.source.exists():
        raise SystemExit(f"Source file does not exist: {args.source}")
    if not args.toc.exists():
        raise SystemExit(f"TOC file does not exist: {args.toc}")
    written = split_chapters(args.source, args.toc, args.out)
    print(f"Wrote {len(written)} chapter files to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
