from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_phase3 import validate  # noqa: E402


def test_phase3_exit_gate_passes() -> None:
    assert validate() == []
