#!/usr/bin/env python3
"""Validate the accepted Phase 3 direct-layout toy BABS campaign."""

from __future__ import annotations

import configparser
import json
import subprocess
import sys
from pathlib import Path

from validate_schemas import load_yaml, validate_operations_ledger, validation_errors


ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "operations" / "toy-bids-app-synthetic"
ATTEMPT = ROOT / "studies/toy/derivatives/toy-bids-app-synthetic-attempt-003"
EXPECTED_ID = "44bd0b3a-e03d-46bf-b0dc-a5e47bdb95c7"
EXPECTED_COMMIT = "bef0f2f585e3dcb02ff9101b4eef2850592e1f89"


def git(path: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=path, check=True, text=True, capture_output=True
    ).stdout.strip()


def dataset_id(path: Path) -> str:
    parser = configparser.ConfigParser()
    parser.read(path / ".datalad/config")
    return parser['datalad "dataset"']["id"]


def validate() -> list[str]:
    errors: list[str] = []
    for campaign in ("campaign.yaml", "campaign-attempt-002.yaml", "campaign-attempt-003.yaml"):
        errors.extend(
            f"{campaign}: {error}"
            for error in validation_errors("campaign", load_yaml(OPS / campaign))
        )
    errors.extend(validate_operations_ledger(OPS / "commands.jsonl"))

    acceptance = load_yaml(OPS / "acceptance.yaml")
    if acceptance.get("derivative_dataset_id") != EXPECTED_ID:
        errors.append("acceptance dataset ID is not the accepted attempt ID")
    if acceptance.get("accepted_commit") != EXPECTED_COMMIT:
        errors.append("acceptance commit is not the validated derivative commit")
    if dataset_id(ATTEMPT) != EXPECTED_ID or git(ATTEMPT, "rev-parse", "HEAD") != EXPECTED_COMMIT:
        errors.append("accepted derivative worktree identity or commit differs")

    description = json.loads((ATTEMPT / "dataset_description.json").read_text())
    if description.get("DatasetType") != "derivative":
        errors.append("accepted attempt is not declared as a derivative")
    if not description.get("GeneratedBy") or not description.get("SourceDatasets"):
        errors.append("accepted derivative provenance metadata is incomplete")

    init_config = load_yaml(ATTEMPT / ".babs/babs_init_config.yaml")
    expected_paths = {
        "analysis_path": ".",
        "input_ria_path": ".babs/input_ria",
        "output_ria_path": ".babs/output_ria",
    }
    for key, expected in expected_paths.items():
        if init_config.get(key) != expected:
            errors.append(f"BABS direct-layout setting {key} differs from {expected}")
    script = (ATTEMPT / "code/participant_job.sh").read_text()
    run_script = (ATTEMPT / "code/toy-bids-app_zip.sh").read_text()
    for token in ("--cleanenv", "--containall", "--no-home", "home,cwd", "--network", "none"):
        if token not in run_script:
            errors.append(f"generated container command lacks isolation token {token}")
    if "#SBATCH --tmp" in script:
        errors.append("accepted Unity participant script retains unsupported --tmp")
    if not (ATTEMPT / ".bidsignore").is_file():
        errors.append("reviewed BABS BIDS-layout exception is absent")
    if not (ATTEMPT / ".babs/output_ria/alias/data").is_symlink():
        errors.append("accepted output RIA alias is absent")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("Phase 3 direct-layout toy BABS campaign passes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
