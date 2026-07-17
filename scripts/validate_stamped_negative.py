#!/usr/bin/env python3
"""Prove that omitted STAMPED decisions fail structural validation."""

from __future__ import annotations

from pathlib import Path

from validate_stamped import ROOT, validate


FIXTURE = ROOT / "tests" / "fixtures" / "stamped"


def main() -> int:
    errors = validate(
        ideal=False,
        assessment_path=FIXTURE / "assessment-missing.tsv",
        components_path=FIXTURE / "components-missing.tsv",
    )
    if not any("omitted MUST/SHOULD decisions" in error for error in errors):
        print("ERROR: negative fixture did not trigger omitted-decision validation")
        return 1
    print("Negative STAMPED fixture correctly rejected omitted MUST/SHOULD decisions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
