#!/usr/bin/env python3
"""Detect optional tools for the book learning workflow."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
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


def install_python_package(package: str) -> ToolStatus:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return ToolStatus(package, True, "Installed with pip.")

    detail = (result.stderr or result.stdout).strip()
    if not detail:
        detail = "pip install failed without output."
    return ToolStatus(package, False, f"Install failed: {detail}")


def install_missing_tools(statuses: list[ToolStatus]) -> list[ToolStatus]:
    install_results = []
    by_name = {status.name: status for status in statuses}

    if not by_name["pymupdf4llm"].available:
        install_results.append(install_python_package("pymupdf4llm"))

    if not by_name["pandoc"].available:
        if not python_module_available("pypandoc"):
            install_results.append(install_python_package("pypandoc_binary"))
        install_results.append(
            ToolStatus(
                "pandoc",
                False,
                "System pandoc is preferred for EPUB/DOCX/HTML. pypandoc_binary is a Python fallback, not a guaranteed equivalent in every environment.",
            )
        )

    if not by_name["ocrmypdf"].available:
        install_results.append(
            ToolStatus(
                "ocrmypdf",
                False,
                "Optional OCR tool for scanned PDFs. Not installed automatically; install manually if needed.",
            )
        )

    return install_results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect optional tools for the book learning workflow.")
    parser.add_argument("--install", action="store_true", help="Attempt conservative installation of missing Python packages.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    statuses = check_tools()
    payload = {"tools": [asdict(status) for status in statuses]}

    if args.install:
        install_results = install_missing_tools(statuses)
        statuses = check_tools()
        payload["install_results"] = [asdict(status) for status in install_results]
        payload["tools_after_install"] = [asdict(status) for status in statuses]

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if all(status.available for status in statuses if status.name != "ocrmypdf") else 1


if __name__ == "__main__":
    raise SystemExit(main())
