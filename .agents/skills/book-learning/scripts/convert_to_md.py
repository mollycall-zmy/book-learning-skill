#!/usr/bin/env python3
"""Convert supported book formats to Markdown."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


SUPPORTED = {".pdf", ".epub", ".docx", ".html", ".htm", ".md", ".markdown"}


def convert_pdf(source: Path, target: Path) -> None:
    try:
        import pymupdf4llm
    except ImportError as exc:
        raise RuntimeError("Missing pymupdf4llm. Install with: python3 -m pip install pymupdf4llm") from exc

    markdown = pymupdf4llm.to_markdown(str(source))
    target.write_text(markdown, encoding="utf-8")


def run_pandoc(source: Path, target: Path) -> None:
    pandoc = shutil.which("pandoc")
    if pandoc:
        result = subprocess.run(
            [pandoc, str(source), "-t", "gfm", "-o", str(target)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            raise RuntimeError(f"pandoc failed: {detail}")
        return

    try:
        import pypandoc
    except ImportError as exc:
        raise RuntimeError("Missing pandoc. Install pandoc with brew/apt, or install pypandoc_binary.") from exc

    try:
        pypandoc.convert_file(str(source), "gfm", outputfile=str(target))
    except OSError as exc:
        raise RuntimeError("pypandoc could not find pandoc. Install pandoc or pypandoc_binary.") from exc


def convert(source: Path, target: Path) -> None:
    suffix = source.suffix.lower()
    if suffix not in SUPPORTED:
        supported = ", ".join(sorted(SUPPORTED))
        raise RuntimeError(f"Unsupported input format '{suffix}'. Supported formats: {supported}")

    target.parent.mkdir(parents=True, exist_ok=True)

    if suffix in {".md", ".markdown"}:
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    elif suffix == ".pdf":
        convert_pdf(source, target)
    else:
        run_pandoc(source, target)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert PDF, EPUB, DOCX, HTML, or Markdown to Markdown.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, required=True, help="Output Markdown path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.source.exists():
        raise SystemExit(f"Source file does not exist: {args.source}")
    try:
        convert(args.source, args.out)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
