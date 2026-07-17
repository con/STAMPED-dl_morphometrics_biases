from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_docs import validate as validate_docs  # noqa: E402
from validate_phase2 import validate  # noqa: E402


def test_phase2_documentation_is_routable() -> None:
    assert validate_docs() == []


def test_phase2_exit_gate_passes() -> None:
    assert validate() == []
