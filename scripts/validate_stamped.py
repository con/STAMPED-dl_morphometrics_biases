#!/usr/bin/env python3
"""Validate the tracked STAMPED component inventory and assessment."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT = ROOT / "config" / "stamped-assessment.tsv"
COMPONENTS = ROOT / "config" / "components.tsv"

ASSESSMENT_FIELDS = (
    "subject_id",
    "parent_id",
    "subject_kind",
    "requirement_id",
    "level",
    "decision",
    "status",
    "evidence",
    "limitation",
)
COMPONENT_FIELDS = (
    "subject_id",
    "parent_id",
    "subject_kind",
    "location",
    "identity",
    "access_class",
    "license_status",
    "lifecycle_status",
    "notes",
)
REQUIREMENTS = {
    "S.1": "MUST",
    "S.2": "MUST",
    "T.1": "MUST",
    "T.2": "SHOULD",
    "T.3": "MUST",
    "T.4-programmatic": "SHOULD",
    "T.4-versions": "MUST",
    "A.1": "MUST",
    "A.2": "SHOULD",
    "M.1": "SHOULD",
    "M.3": "SHOULD",
    "P.1": "MUST",
    "P.2": "MUST",
    "P.3": "MUST",
    "E.1": "SHOULD",
    "D.1": "MUST",
    "D.2": "SHOULD",
    "D.3": "SHOULD",
}
OPTIONAL_REQUIREMENTS = {"M.2": "MAY"}
NORMATIVE_REQUIREMENTS = REQUIREMENTS | OPTIONAL_REQUIREMENTS
STATUSES = {"met", "partial", "unmet", "restricted", "not-applicable"}
STATUS_RANK = {"unmet": 0, "restricted": 0, "partial": 1, "met": 2}


def display_path(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def read_tsv(path: Path, fields: tuple[str, ...]) -> list[dict[str, str]]:
    if not path.is_file():
        raise ValueError(f"missing required file: {display_path(path)}")
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if tuple(reader.fieldnames or ()) != fields:
            raise ValueError(
                f"{display_path(path)} has fields {reader.fieldnames}; expected {fields}"
            )
        rows = list(reader)
    if not rows:
        raise ValueError(f"{display_path(path)} has no records")
    return rows


def validate(
    ideal: bool,
    assessment_path: Path = ASSESSMENT,
    components_path: Path = COMPONENTS,
) -> list[str]:
    errors: list[str] = []
    try:
        components = read_tsv(components_path, COMPONENT_FIELDS)
        assessment = read_tsv(assessment_path, ASSESSMENT_FIELDS)
    except ValueError as error:
        return [str(error)]

    component_ids = [row["subject_id"] for row in components]
    component_set = set(component_ids)
    if len(component_ids) != len(component_set):
        errors.append("components.tsv contains duplicate subject_id values")
    roots = [row for row in components if not row["parent_id"]]
    if len(roots) != 1:
        errors.append("components.tsv must contain exactly one root with an empty parent_id")
    root_id = roots[0]["subject_id"] if len(roots) == 1 else "ro-root"

    for row in components:
        parent = row["parent_id"]
        if parent and parent not in component_set:
            errors.append(f"{row['subject_id']}: unknown parent_id {parent}")
        if not row["location"] or not row["lifecycle_status"]:
            errors.append(f"{row['subject_id']}: location and lifecycle_status are required")
        visited = {row["subject_id"]}
        cursor = parent
        while cursor:
            if cursor in visited:
                errors.append(f"{row['subject_id']}: component parent cycle reaches {cursor}")
                break
            visited.add(cursor)
            cursor = next(
                (
                    candidate["parent_id"]
                    for candidate in components
                    if candidate["subject_id"] == cursor
                ),
                "",
            )

    seen: set[tuple[str, str]] = set()
    requirements_by_subject: dict[str, set[str]] = {}
    by_requirement: dict[str, list[dict[str, str]]] = {}
    root_rows: dict[str, dict[str, str]] = {}

    for row in assessment:
        subject = row["subject_id"]
        requirement = row["requirement_id"]
        key = (subject, requirement)
        if key in seen:
            errors.append(f"duplicate assessment row: {subject}/{requirement}")
        seen.add(key)
        requirements_by_subject.setdefault(subject, set()).add(requirement)
        if subject not in component_set:
            errors.append(f"{subject}/{requirement}: subject is absent from components.tsv")
        elif row["parent_id"] != next(
            item["parent_id"] for item in components if item["subject_id"] == subject
        ):
            errors.append(f"{subject}/{requirement}: parent_id differs from components.tsv")
        elif row["subject_kind"] != next(
            item["subject_kind"] for item in components if item["subject_id"] == subject
        ):
            errors.append(f"{subject}/{requirement}: subject_kind differs from components.tsv")
        if row["parent_id"] and row["parent_id"] not in component_set:
            errors.append(f"{subject}/{requirement}: unknown parent_id {row['parent_id']}")
        expected_level = NORMATIVE_REQUIREMENTS.get(requirement)
        if expected_level is None:
            errors.append(f"{subject}/{requirement}: unknown normative requirement")
        elif row["level"] != expected_level:
            errors.append(
                f"{subject}/{requirement}: level {row['level']} does not match {expected_level}"
            )
        if row["status"] not in STATUSES:
            errors.append(f"{subject}/{requirement}: invalid status {row['status']}")
        if row["level"] == "MUST" and row["decision"] != "adopt":
            errors.append(f"{subject}/{requirement}: every MUST decision must be adopt")
        if row["level"] == "SHOULD" and row["decision"] not in {
            "adopt",
            "defer",
            "decline",
        }:
            errors.append(f"{subject}/{requirement}: invalid SHOULD decision {row['decision']}")
        if row["level"] == "SHOULD" and not row["limitation"]:
            errors.append(f"{subject}/{requirement}: SHOULD decision requires a rationale")
        if row["level"] == "MAY" and row["decision"] not in {"adopt", "decline"}:
            errors.append(f"{subject}/{requirement}: invalid MAY decision {row['decision']}")
        if row["status"] == "met" and (
            not row["evidence"] or row["evidence"].startswith(("PENDING", "PLANNED"))
        ):
            errors.append(f"{subject}/{requirement}: met requires concrete evidence")
        if row["status"] == "not-applicable" and not row["limitation"]:
            errors.append(f"{subject}/{requirement}: not-applicable requires a scope reason")
        if row["decision"] == "defer" and not row["limitation"]:
            errors.append(f"{subject}/{requirement}: defer requires a reopening condition")
        by_requirement.setdefault(requirement, []).append(row)
        if subject == root_id:
            root_rows[requirement] = row

    for subject in sorted(component_set):
        assessed = requirements_by_subject.get(subject, set())
        missing = set(REQUIREMENTS) - assessed
        if missing:
            errors.append(
                f"{subject}: omitted MUST/SHOULD decisions: "
                + ", ".join(sorted(missing))
            )

    missing_root = set(REQUIREMENTS) - set(root_rows)
    if missing_root:
        errors.append("root omits requirements: " + ", ".join(sorted(missing_root)))

    rows_by_key = {
        (row["subject_id"], row["requirement_id"]): row for row in assessment
    }
    for row in assessment:
        parent = row["parent_id"]
        if not parent or row["status"] == "not-applicable":
            continue
        parent_row = rows_by_key.get((parent, row["requirement_id"]))
        if not parent_row:
            continue
        if parent_row["status"] == "not-applicable":
            errors.append(
                f"{parent}/{row['requirement_id']}: parent is not-applicable while "
                f"child {row['subject_id']} is applicable"
            )
            continue
        if STATUS_RANK[parent_row["status"]] > STATUS_RANK[row["status"]]:
            errors.append(
                f"{parent}/{row['requirement_id']}: parent status is stronger than "
                f"child {row['subject_id']}"
            )

    if ideal:
        for row in assessment:
            if row["status"] == "not-applicable":
                continue
            if row["level"] == "MUST" and row["status"] != "met":
                errors.append(
                    f"ideal gap: {row['subject_id']}/{row['requirement_id']} is {row['status']}"
                )
            if row["level"] == "SHOULD" and not (
                row["decision"] == "adopt" and row["status"] == "met"
            ):
                errors.append(
                    "ideal gap: "
                    f"{row['subject_id']}/{row['requirement_id']} is "
                    f"{row['decision']}+{row['status']}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ideal", action="store_true")
    parser.add_argument("--assessment", type=Path, default=ASSESSMENT)
    parser.add_argument("--components", type=Path, default=COMPONENTS)
    args = parser.parse_args()
    errors = validate(args.ideal, args.assessment, args.components)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("STAMPED assessment structure and roll-ups are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
