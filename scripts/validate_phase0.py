#!/usr/bin/env python3
"""Validate the Phase 0 evidence and declared result boundary."""

from __future__ import annotations

import csv
import os
import re
import json
import subprocess
from collections import Counter
from pathlib import Path

from validate_stamped import validate as validate_stamped


ROOT = Path(__file__).resolve().parents[1]
POSTER_SHA256 = "9031199b6da81817e157bb3e762cedf349a844444a707cbb6ff97a4acba901f6"
POSTER_KEY = (
    "SHA256E-s943963--"
    "9031199b6da81817e157bb3e762cedf349a844444a707cbb6ff97a4acba901f6.pdf"
)
POSTER_DOI = "doi:10.17605/OSF.IO/P3KNS"
POSTER_DOWNLOAD = "https://osf.io/download/mn47a/"
GIN_URL = "https://gin.g-node.org/leej3/STAMPED-dl_morphometrics_biases"
GIN_UUID = "99822df6-f62f-4161-925a-e444e68c8625"
OLD_SOURCE_COMMIT = "448bf1a311c1ab8310cbab613a8123bb4a4f4a00"
RUNTIME_IDS = {
    "reconall-fs741-repronim-bids",
    "reconall-fs820-repronim-neurodesk",
    "reconall-fs820-project-bidsapp",
    "recon-any-unresolved",
    "recon-all-clinical-unresolved",
    "t1w-resample-1x1x5-unresolved",
    "morphometrics-analysis-custom",
}
MANIFEST_FIELDS = (
    "result_id",
    "target_id",
    "evidence_class",
    "study_id",
    "artifact_type",
    "path",
    "dataset_commit",
    "run_record",
    "container_id",
    "sif_annex_key",
    "sif_sha256",
    "input_ids",
    "code_commit",
    "config_path_and_hash",
    "reproduce_task",
    "validation_status",
    "limitation",
)


def read_tsv(path: Path) -> tuple[tuple[str, ...], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        fields = tuple(reader.fieldnames or ())
        return fields, list(reader)


def main() -> int:
    errors = validate_stamped(ideal=False)

    target_text = (ROOT / "docs" / "result-targets.md").read_text(encoding="utf-8")
    target_matches = re.findall(
        r"^\| ([a-z0-9][a-z0-9-]+) \| (figure|statistic|table|derivative) \|",
        target_text,
        flags=re.MULTILINE,
    )
    targets = dict(target_matches)
    if len(target_matches) != len(targets):
        errors.append("docs/result-targets.md contains duplicate target IDs")
    if len(targets) != 45:
        errors.append(f"expected 45 stable target IDs, found {len(targets)}")

    fields, manifest = read_tsv(ROOT / "result-manifest.tsv")
    if fields != MANIFEST_FIELDS:
        errors.append(f"result-manifest.tsv fields differ from {MANIFEST_FIELDS}")
    if len(manifest) != 90:
        errors.append(f"expected 90 result-manifest rows, found {len(manifest)}")
    result_ids = [row["result_id"] for row in manifest]
    if len(result_ids) != len(set(result_ids)):
        errors.append("result-manifest.tsv contains duplicate result_id values")
    counts = Counter(row["target_id"] for row in manifest)
    if set(counts) != set(targets):
        errors.append("target IDs differ between result-targets.md and result-manifest.tsv")
    for target, count in counts.items():
        if count != 2:
            errors.append(f"{target}: expected pilot and claim rows, found {count}")
    required_cells = (
        "path",
        "dataset_commit",
        "run_record",
        "container_id",
        "sif_annex_key",
        "sif_sha256",
        "input_ids",
        "code_commit",
        "config_path_and_hash",
        "reproduce_task",
        "validation_status",
        "limitation",
    )
    for row in manifest:
        missing = [field for field in required_cells if not row[field]]
        if missing:
            errors.append(f"{row['result_id']}: empty fields {', '.join(missing)}")
        expected_type = targets.get(row["target_id"])
        if expected_type and row["artifact_type"] != expected_type:
            errors.append(
                f"{row['result_id']}: {row['artifact_type']} differs from target {expected_type}"
            )
        expected = (
            ("pilot-ds007116--", "pilot-only", "ds007116")
            if row["study_id"] == "ds007116"
            else ("claim-abcd--", "claim-bearing", "abcd")
        )
        if not row["result_id"].startswith(expected[0]):
            errors.append(f"{row['result_id']}: result prefix and study disagree")
        if (row["evidence_class"], row["study_id"]) != expected[1:]:
            errors.append(f"{row['result_id']}: evidence class and study disagree")
        bare_targets = set(row["input_ids"].split(";")) & set(targets)
        if bare_targets:
            errors.append(
                f"{row['result_id']}: unqualified result dependencies "
                + ", ".join(sorted(bare_targets))
            )

    _, sources = read_tsv(ROOT / "docs" / "source-inventory.tsv")
    source_rows = {row["id"]: row for row in sources}
    if source_rows.get("SRC-REPO", {}).get("snapshot_identity") != OLD_SOURCE_COMMIT:
        errors.append("source inventory does not pin the audited main commit")
    if "BR-REF" not in source_rows:
        errors.append("source inventory omits the material non-main branch")
    if source_rows.get("RESULT-POSTER", {}).get("content_identity") != (
        "sha256:" + POSTER_SHA256
    ):
        errors.append("source inventory poster checksum differs from inspected bytes")

    _, evidence = read_tsv(ROOT / "docs" / "evidence-manifest.tsv")
    poster_rows = [row for row in evidence if row["evidence_id"] == "EVID-POSTER-OHBM2025"]
    if len(poster_rows) != 1 or poster_rows[0]["sha256"] != POSTER_SHA256:
        errors.append("evidence manifest lacks the exact inspected poster identity")
    elif poster_rows[0]["distribution_decision"].startswith("PENDING"):
        errors.append(
            "poster redistribution/persistent-reference decision is still pending"
        )
    else:
        poster = poster_rows[0]
        references = poster["persistent_reference"].split(";")
        if (
            POSTER_DOI not in references
            or POSTER_DOWNLOAD not in references
            or GIN_URL not in references
        ):
            errors.append("evidence manifest omits the exact OSF or GIN reference")
        poster_path = (
            ROOT / "docs" / "reference" / "recon_all_recon_any_poster_ohbm2025.pdf"
        )
        if not poster_path.is_symlink():
            errors.append("poster is not an annex symlink at the declared path")
        elif POSTER_KEY not in os.readlink(poster_path):
            errors.append("poster annex symlink does not resolve to the expected key")
        whereis = subprocess.run(
            ["git", "annex", "whereis", "--json", str(poster_path.relative_to(ROOT))],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if whereis.returncode:
            errors.append("git-annex could not report poster availability")
        else:
            record = json.loads(whereis.stdout)
            uuids = {item["uuid"] for item in record["whereis"]}
            if GIN_UUID not in uuids:
                errors.append("poster availability does not include the recorded GIN UUID")

    _, runtimes = read_tsv(ROOT / "config" / "runtime-candidates.tsv")
    runtime_ids = {row["runtime_id"] for row in runtimes}
    if runtime_ids != RUNTIME_IDS:
        errors.append("runtime-candidate IDs differ from the Phase 0 required set")

    _, components = read_tsv(ROOT / "config" / "components.tsv")
    component_ids = {row["subject_id"] for row in components}
    missing_results = set(result_ids) - component_ids
    if missing_results:
        errors.append(
            "result instances absent from component inventory: "
            + ", ".join(sorted(missing_results))
        )
    if "storage-gin" not in component_ids:
        errors.append("GIN annex sibling is absent from the component inventory")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "Phase 0 structure valid: "
        f"{len(targets)} targets, {len(manifest)} manifest rows, "
        f"{len(sources)} source records, {len(runtimes)} runtime candidates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
