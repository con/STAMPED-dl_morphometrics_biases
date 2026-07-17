#!/usr/bin/env python3
"""Check Phase 2 operational documentation and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = (
    ROOT / "README.md",
    ROOT / "envs" / "README.md",
    ROOT / "docs" / "phase-2-notes.md",
)
LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


def validate() -> list[str]:
    errors: list[str] = []
    for path in DOCUMENTS:
        if not path.is_file():
            errors.append(f"missing required Phase 2 documentation: {path.relative_to(ROOT)}")
            continue
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target_path = target.split("#", maxsplit=1)[0]
            if target_path and not (path.parent / target_path).exists():
                errors.append(
                    f"broken local link in {path.relative_to(ROOT)}: {target}"
                )
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Phase 2 documentation valid: {len(DOCUMENTS)} required documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
