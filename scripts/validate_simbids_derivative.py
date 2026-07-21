#!/usr/bin/env python3
"""Validate the three-subject SimBIDS derivative payload with the Deno validator."""

from __future__ import annotations

import argparse
import configparser
import json
import os
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DERIVATIVE = (
    ROOT / "studies/simbids/derivatives/simbids-fmriprep-three-subject-attempt-001"
)
BIDS_SCHEMA = "v1.11.1"
BIDS_SCHEMA_URL = "https://bids-specification.readthedocs.io/en/v1.11.1/schema.json"
VALIDATOR_DISTRIBUTION = "bids-validator-deno"
EXPECTED_SUBJECTS = ["01", "02", "03"]


def dataset_id(path: Path) -> str:
    config = configparser.ConfigParser()
    config.read(path / ".datalad/config")
    return config['datalad "dataset"']["id"]


def git_commit(path: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def validate() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    scratch = Path(
        os.environ.get(
            "SLURM_TMPDIR",
            "/scratch4/workspace/f008q9c_dartmouth_edu-stamped-phase3",
        )
    )
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="bids-derivative-", dir=scratch
    ) as temporary:
        payload = Path(temporary) / "payload"
        payload.mkdir()
        for filename in (".bidsignore", "dataset_description.json", "README.md"):
            shutil.copy2(
                DERIVATIVE / filename, payload / filename, follow_symlinks=True
            )
        for subject in ("sub-01", "sub-02", "sub-03"):
            shutil.copytree(DERIVATIVE / subject, payload / subject, symlinks=False)

        environment = os.environ.copy()
        environment["BIDS_SCHEMA"] = BIDS_SCHEMA_URL
        for variable, dirname in {
            "DENO_DIR": "deno",
            "XDG_CACHE_HOME": "cache",
            "XDG_CONFIG_HOME": "config",
        }.items():
            directory = Path(temporary) / dirname
            directory.mkdir()
            environment[variable] = str(directory)
        result = subprocess.run(
            [
                "bids-validator-deno",
                "--datasetTypes",
                "derivative",
                "--format",
                "json",
                str(payload),
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
            f"validator did not emit JSON: {error}; stderr={result.stderr.strip()}"
        ]

    issues = output.get("issues", {}).get("issues", [])
    reported_errors = [issue for issue in issues if issue.get("severity") == "error"]
    warnings = [issue for issue in issues if issue.get("severity") == "warning"]
    summary = output.get("summary", {})
    if result.returncode != 0 or reported_errors:
        errors.append(
            f"validator reported {len(reported_errors)} errors (exit {result.returncode})"
        )
    if sorted(summary.get("subjects", [])) != EXPECTED_SUBJECTS:
        errors.append(f"validator subjects differ: {summary.get('subjects')}")
    if len(warnings) != 6 or {item.get("code") for item in warnings} != {"NIFTI_UNIT"}:
        errors.append("warnings differ from six reviewed synthetic NIfTI-unit warnings")

    report = {
        "schema_version": 1,
        "dataset_kind": "derivative",
        "dataset_path": str(DERIVATIVE.relative_to(ROOT)),
        "dataset_id": dataset_id(DERIVATIVE),
        "dataset_commit": git_commit(DERIVATIVE),
        "payload_view": [
            ".bidsignore",
            "dataset_description.json",
            "README.md",
            "sub-01/",
            "sub-02/",
            "sub-03/",
        ],
        "operational_paths_excluded_from_payload_view": [
            ".babs/",
            "code/",
            "containers/",
            "logs/",
            "sourcedata/",
            "*.zip",
        ],
        "requested_bids_schema": BIDS_SCHEMA,
        "requested_bids_schema_url": BIDS_SCHEMA_URL,
        "validator_distribution": VALIDATOR_DISTRIBUTION,
        "validator_version": version(VALIDATOR_DISTRIBUTION),
        "validator_internal_schema_version": summary.get("schemaVersion"),
        "subjects": sorted(summary.get("subjects", [])),
        "validated_files": summary.get("totalFiles"),
        "errors": reported_errors,
        "reviewed_warnings": [
            {
                "code": item.get("code"),
                "location": item.get("location"),
                "review": "SimBIDS qualification NIfTI has unspecified spatial units; filenames, dimensions, and headers remain validator-readable.",
            }
            for item in warnings
        ],
        "status": "pass" if not errors else "fail",
    }
    return report, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report, errors = validate()
    if args.report and report:
        target = args.report if args.report.is_absolute() else ROOT / args.report
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(
        "Deno BIDS derivative validation passed: 3 subjects, 0 errors, 6 reviewed warnings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
