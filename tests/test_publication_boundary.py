from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_publication_boundary import run_simulation  # noqa: E402


def test_protected_classes_cannot_reach_public_sibling() -> None:
    result = run_simulation()
    assert result["status"] == "pass", result["failures"]
    assert result["public_git_push_dry_run"] is True
    assert result["public_clone_succeeded"] is True
    assert result["protected_paths_absent"] is True
    assert result["protected_annex_keys_absent"] is True
    assert result["protected_remote_absent"] is True
    assert result["public_annex_payload_present"] is True
