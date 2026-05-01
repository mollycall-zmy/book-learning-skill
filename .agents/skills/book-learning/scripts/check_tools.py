#!/usr/bin/env python3
"""Detect optional tools for the book learning workflow."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
from dataclasses import asdict, dataclass


@dataclass
class ToolStatus:
    name: str
    available: bool
    detail: str


def python_module_available(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def command_version(command: str, args: list[str]) -> str | None:
    executable = shutil.which(command)
    if not executable:
        return None
    try:
        result = subprocess.run([executable, *args], check=False, capture_output=True, text=True)
    except OSError:
        return None
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else executable


def check_tools() -> list[ToolStatus]:
    statuses = []

    if python_module_available("pymupdf4llm"):
        statuses.append(ToolStatus("pymupdf4llm", True, "Python module is importable."))
    else:
        statuses.append(ToolStatus("pymupdf4llm", False, "Install with: python3 -m pip install pymupdf4llm"))

    pandoc_version = command_version("pandoc", ["--version"])
    if pandoc_version:
        statuses.append(ToolStatus("pandoc", True, pandoc_version))
    elif python_module_available("pypandoc"):
        statuses.append(ToolStatus("pandoc", True, "pypandoc is importable; it may provide a bundled pandoc."))
    else:
        statuses.append(ToolStatus("pandoc", False, "Install pandoc with brew/apt, or install pypandoc_binary."))

    ocr_version = command_version("ocrmypdf", ["--version"])
    if ocr_version:
        statuses.append(ToolStatus("ocrmypdf", True, ocr_version))
    else:
        statuses.append(ToolStatus("ocrmypdf", False, "Optional for scanned PDFs. Install with: python3 -m pip install ocrmypdf"))

    return statuses


def main() -> int:
    statuses = check_tools()
    print(json.dumps([asdict(status) for status in statuses], ensure_ascii=False, indent=2))
    return 0 if all(status.available for status in statuses if status.name != "ocrmypdf") else 1


if __name__ == "__main__":
    raise SystemExit(main())
