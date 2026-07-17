from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_schemas import (  # noqa: E402
    FIXTURES,
    load_yaml,
    validate_all,
    validate_operations_ledger,
    validation_errors,
)


def test_phase1_schema_gate_accepts_tracked_records() -> None:
    assert validate_all() == []


def test_campaign_schema_rejects_omitted_boundaries() -> None:
    errors = validation_errors("campaign", load_yaml(FIXTURES / "campaign-invalid.yaml"))
    joined = "\n".join(errors)
    assert "access_class" in joined
    assert "scientific_change_requires_new_campaign" in joined
    assert "True was expected" in joined


def test_operations_schema_rejects_overwrite_and_broken_chain() -> None:
    errors = validate_operations_ledger(FIXTURES / "operations-invalid.jsonl")
    joined = "\n".join(errors)
    assert "overwrite" in joined
    assert "argv" in joined
    assert "sequence must be contiguous" in joined
    assert "previous_event_sha256" in joined
