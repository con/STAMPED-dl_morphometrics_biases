from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_bids import EXPECTED, validate_all  # noqa: E402


def test_toy_study_and_raw_child_validate_against_bids_1_11_1() -> None:
    reports, errors = validate_all()
    assert errors == []
    assert {report["dataset_kind"] for report in reports} == {"study", "raw"}
    assert all(report["status"] == "pass" for report in reports)
    assert all(report["validator_version"] == "3.0.0" for report in reports)
    assert all(report["requested_bids_schema"] == "v1.11.1" for report in reports)
    observed = {
        report["dataset_kind"]: {
            (warning["code"], warning["sub_code"])
            for warning in report["reviewed_warnings"]
        }
        for report in reports
    }
    assert observed == EXPECTED
