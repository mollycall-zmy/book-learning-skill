#!/usr/bin/env python3
"""Path helpers for knowledge-root aware book-learning outputs."""

from __future__ import annotations

from pathlib import Path


KNOWLEDGE_CATEGORY_RELATIVE = Path("L1-事实与语义") / "02-📚 知识"


def knowledge_category_root(knowledge_root: Path) -> Path:
    return knowledge_root / KNOWLEDGE_CATEGORY_RELATIVE


def list_knowledge_subdirs(knowledge_root: Path) -> list[Path]:
    category_root = knowledge_category_root(knowledge_root)
    if not category_root.exists():
        return []
    return sorted(path for path in category_root.iterdir() if path.is_dir())


def match_knowledge_subdir(
    existing_subdirs: list[Path],
    *,
    reading_mode: str = "mode-0-distillation",
    preferred_category: str | None = None,
    user_category: str | None = None,
) -> dict[str, str | None]:
    names = [path.name for path in existing_subdirs]
    for source, category in (("user", user_category), ("config", preferred_category)):
        if category and category in names:
            return {
                "matched_knowledge_subdir": category,
                "confidence": "high",
                "reason": source,
            }

    mode_hints = {
        "mode-1-sop": ("学习", "方法", "认知", "思维"),
        "mode-2-scene-mapping": ("案例", "商业", "品牌", "行业"),
        "mode-3-cognitive-refresh": ("认知", "思维", "模型"),
        "mode-4-communication-game": ("沟通", "谈判", "决策", "思维"),
    }
    for hint in mode_hints.get(reading_mode, ()):
        for name in names:
            if hint in name:
                return {
                    "matched_knowledge_subdir": name,
                    "confidence": "medium",
                    "reason": f"reading_mode:{reading_mode}; hint:{hint}",
                }

    return {
        "matched_knowledge_subdir": None,
        "confidence": "low",
        "reason": "needs_user_confirmation",
    }


def canonical_notes_path(
    *,
    book_slug: str,
    knowledge_root: Path | None = None,
    matched_knowledge_subdir: str | None = None,
    allow_root_fallback: bool = False,
) -> Path:
    if knowledge_root is None:
        return Path("outputs") / "reading_notes.md"

    category_root = knowledge_category_root(knowledge_root)
    filename = f"{book_slug}-阅读笔记.md"
    if matched_knowledge_subdir:
        return category_root / matched_knowledge_subdir / filename
    if allow_root_fallback:
        return category_root / filename
    raise ValueError("matched_knowledge_subdir is required unless allow_root_fallback is true")
