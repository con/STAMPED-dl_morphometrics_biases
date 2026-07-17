#!/usr/bin/env python3
"""Validate the Phase 1 toy Study and raw child against BIDS 1.11.1."""

from __future__ import annotations

import argparse
import configparser
import json
import os
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BIDS_SCHEMA = "v1.11.1"
BIDS_SCHEMA_URL = "https://bids-specification.readthedocs.io/en/v1.11.1/schema.json"
VALIDATOR_DISTRIBUTION = "bids-validator-deno"
EXPECTED = {
    "raw": {
        ("SUBJECT_FOLDERS", None),
        ("TOO_FEW_AUTHORS", None),
        ("JSON_KEY_RECOMMENDED", "HEDVersion"),
        ("JSON_KEY_RECOMMENDED", "GeneratedBy"),
        ("JSON_KEY_RECOMMENDED", "SourceDatasets"),
    },
    "study": {
        ("TOO_FEW_AUTHORS", None),
        ("JSON_KEY_RECOMMENDED", "HEDVersion"),
        ("JSON_KEY_RECOMMENDED", "GeneratedBy"),
        ("JSON_KEY_RECOMMENDED", "SourceDatasets"),
    },
}
DATASETS = {
    "raw": ROOT / "studies" / "toy" / "sourcedata" / "raw",
    "study": ROOT / "studies" / "toy",
}


def datalad_id(path: Path) -> str:
    config = configparser.ConfigParser()
    config.read(path / ".datalad" / "config")
    return config["datalad \"dataset\""]["id"]


def git_commit(path: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def validate_dataset(kind: str) -> tuple[dict[str, Any], list[str]]:
    path = DATASETS[kind]
    errors: list[str] = []
    description = json.loads((path / "dataset_description.json").read_text(encoding="utf-8"))
    if description.get("BIDSVersion") != "1.11.1":
        errors.append(f"{kind}: BIDSVersion must be 1.11.1")
    if description.get("DatasetType") != kind:
        errors.append(f"{kind}: DatasetType must be {kind}")

    environment = os.environ.copy()
    # bids-validator-deno's CLI normalizes a schema tag before its loader sees
    # it.  Pin the official immutable documentation URL explicitly instead.
    environment["BIDS_SCHEMA"] = BIDS_SCHEMA_URL
    with tempfile.TemporaryDirectory(prefix="stamped-bids-validator-") as sandbox:
        sandbox_path = Path(sandbox)
        for variable, directory in {
            "DENO_DIR": sandbox_path / "deno",
            "XDG_CACHE_HOME": sandbox_path / "cache",
            "XDG_CONFIG_HOME": sandbox_path / "config",
        }.items():
            directory.mkdir(parents=True, exist_ok=True)
            environment[variable] = str(directory)
        result = subprocess.run(
            [
                "bids-validator-deno",
                "--datasetTypes",
                kind,
                "--format",
                "json",
                str(path),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        return {}, [
            f"{kind}: validator did not emit JSON: {error}; stderr={result.stderr.strip()}"
        ]

    issues = output.get("issues", {}).get("issues", [])
    reported_errors = [issue for issue in issues if issue.get("severity") == "error"]
    warnings = [issue for issue in issues if issue.get("severity") == "warning"]
    signatures = {(item.get("code"), item.get("subCode")) for item in warnings}
    if result.returncode != 0 or reported_errors:
        errors.append(f"{kind}: validator reported errors or exit code {result.returncode}")
    if signatures != EXPECTED[kind]:
        errors.append(
            f"{kind}: warning signatures differ; expected {sorted(EXPECTED[kind], key=str)}, "
            f"observed {sorted(signatures, key=str)}"
        )

    report = {
        "schema_version": 1,
        "dataset_kind": kind,
        "dataset_path": str(path.relative_to(ROOT)),
        "dataset_id": datalad_id(path),
        "dataset_commit": git_commit(path),
        "declared_bids_version": description["BIDSVersion"],
        "declared_dataset_type": description["DatasetType"],
        "requested_bids_schema": BIDS_SCHEMA,
        "requested_bids_schema_url": BIDS_SCHEMA_URL,
        "validator_distribution": VALIDATOR_DISTRIBUTION,
        "validator_version": version(VALIDATOR_DISTRIBUTION),
        "validator_internal_schema_version": output.get("summary", {}).get("schemaVersion"),
        "errors": reported_errors,
        "reviewed_warnings": [
            {
                "code": item.get("code"),
                "sub_code": item.get("subCode"),
                "location": item.get("location"),
                "review": (
                    "expected metadata-only fixture warning"
                    if item.get("code") in {"SUBJECT_FOLDERS", "TOO_FEW_AUTHORS"}
                    else "recommended field does not apply to the empty non-produced fixture"
                ),
            }
            for item in warnings
        ],
        "status": "pass" if not errors else "fail",
    }
    return report, errors


def validate_all() -> tuple[list[dict[str, Any]], list[str]]:
    reports: list[dict[str, Any]] = []
    errors: list[str] = []
    for kind in ("raw", "study"):
        report, found = validate_dataset(kind)
        reports.append(report)
        errors.extend(found)
    return reports, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-dir", type=Path)
    args = parser.parse_args()
    reports, errors = validate_all()
    if args.report_dir:
        report_dir = (
            args.report_dir if args.report_dir.is_absolute() else ROOT / args.report_dir
        )
        report_dir.mkdir(parents=True, exist_ok=True)
        for report in reports:
            target = report_dir / f"bids-{report['dataset_kind']}.json"
            target.write_text(
                json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "BIDS 1.11.1 toy validation passed: raw and Study datasets have no "
        "errors and only the reviewed metadata-only warnings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
