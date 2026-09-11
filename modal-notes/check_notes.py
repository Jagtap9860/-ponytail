"""Deterministic ship-gate check for modal-notes chapters (stdlib only).

Usage:  python3 modal-notes/check_notes.py
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
CHAPTERS = {
    # file -> required section markers + chapter label
    "chapter-01-notes.md": ([f"1.{i}" for i in range(1, 10)], "Chapter 1"),
}


def check(path: pathlib.Path, sections: list[str], label: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fails: list[str] = []
    for s in sections:  # gate 1: completeness
        if s not in text:
            fails.append(f"{label}: missing section marker {s}")
    for marker, gate in [  # gates 2-5
        ("Primer", "beginner primer"),
        ("Glossary", "glossary"),
        ("Self-test", "self-test"),
        ("Revision", "one-page revision"),
        ("Example", "worked examples"),
        ("|", "tables"),
    ]:
        if marker not in text:
            fails.append(f"{label}: missing {gate} (marker {marker!r})")
    if "TODO" in text:  # gate 6: no unfinished honesty gaps
        fails.append(f"{label}: contains TODO")
    return fails


def main() -> int:
    all_fails: list[str] = []
    for fname, (sections, label) in CHAPTERS.items():
        p = ROOT / fname
        if not p.exists():
            all_fails.append(f"{label}: file {fname} not found")
            continue
        fails = check(p, sections, label)
        all_fails.extend(fails)
        print(f"[{'PASS' if not fails else 'FAIL'}] {fname} ({label})")
    if all_fails:
        print("\n".join(f"  ✗ {f}" for f in all_fails))
        return 1
    print("All ship gates passed. The Council nods (reluctantly).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
