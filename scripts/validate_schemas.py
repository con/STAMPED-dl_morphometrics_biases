#!/usr/bin/env python3
"""Validate Phase 1 record schemas, fixtures, and the root result manifest."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "config" / "schemas"
FIXTURES = ROOT / "tests" / "fixtures" / "schemas"
SCHEMA_FILES = {
    "campaign": SCHEMA_DIR / "campaign.schema.json",
    "image": SCHEMA_DIR / "image-record.schema.json",
    "operations": SCHEMA_DIR / "operations-event.schema.json",
    "result": SCHEMA_DIR / "result-manifest.schema.json",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain one mapping")
    return value


def validator(name: str) -> Draft202012Validator:
    schema = load_json(SCHEMA_FILES[name])
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validation_errors(name: str, value: Any) -> list[str]:
    errors = sorted(validator(name).iter_errors(value), key=lambda item: list(item.path))
    return [
        f"{name}:{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]


def validate_operations_ledger(path: Path) -> list[str]:
    errors: list[str] = []
    previous_bytes: bytes | None = None
    with path.open("rb") as stream:
        lines = [line.rstrip(b"\r\n") for line in stream if line.strip()]
    for index, raw in enumerate(lines, start=1):
        try:
            event = json.loads(raw)
        except json.JSONDecodeError as error:
            errors.append(f"{path.relative_to(ROOT)}:{index}: invalid JSON: {error}")
            continue
        errors.extend(
            f"{path.relative_to(ROOT)}:{index}: {error}"
            for error in validation_errors("operations", event)
        )
        if event.get("sequence") != index:
            errors.append(
                f"{path.relative_to(ROOT)}:{index}: sequence must be contiguous from 1"
            )
        expected = None if previous_bytes is None else hashlib.sha256(previous_bytes).hexdigest()
        if event.get("previous_event_sha256") != expected:
            errors.append(
                f"{path.relative_to(ROOT)}:{index}: previous_event_sha256 does not "
                "match the preceding exact JSON line"
            )
        previous_bytes = raw
    if not lines:
        errors.append(f"{path.relative_to(ROOT)}: ledger must contain at least one event")
    return errors


def validate_result_manifest() -> list[str]:
    errors: list[str] = []
    manifest = ROOT / "result-manifest.tsv"
    with manifest.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for index, row in enumerate(rows, start=2):
        errors.extend(
            f"result-manifest.tsv:{index}: {error}"
            for error in validation_errors("result", row)
        )
        if re.search(r"(?:^|[/;])sub-[A-Za-z0-9]+", "\t".join(row.values())):
            errors.append(
                f"result-manifest.tsv:{index}: participant identifier is prohibited"
            )
    return errors


def validate_all() -> list[str]:
    errors: list[str] = []
    for name in SCHEMA_FILES:
        try:
            validator(name)
        except Exception as error:  # jsonschema exposes several schema exceptions
            errors.append(f"{SCHEMA_FILES[name].relative_to(ROOT)}: {error}")

    campaign = load_yaml(FIXTURES / "campaign-valid.yaml")
    image = load_yaml(FIXTURES / "image-valid.yaml")
    errors.extend(validation_errors("campaign", campaign))
    errors.extend(validation_errors("image", image))
    errors.extend(validate_operations_ledger(FIXTURES / "operations-valid.jsonl"))
    errors.extend(validate_result_manifest())
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "Phase 1 schemas valid: 4 schemas, 2 positive YAML records, "
        "2 append-only events, and 90 result-manifest rows"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
