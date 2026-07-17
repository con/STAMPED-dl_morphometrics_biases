from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_stamped import validate  # noqa: E402


FIXTURE = ROOT / "tests" / "fixtures" / "stamped"


def test_tracked_stamped_assessment_is_structurally_valid() -> None:
    assert validate(ideal=False) == []


def test_negative_fixture_rejects_omitted_decisions() -> None:
    errors = validate(
        ideal=False,
        assessment_path=FIXTURE / "assessment-missing.tsv",
        components_path=FIXTURE / "components-missing.tsv",
    )
    assert any("omitted MUST/SHOULD decisions" in error for error in errors)
