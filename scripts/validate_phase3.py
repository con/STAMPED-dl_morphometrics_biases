#!/usr/bin/env python3
"""Validate the accepted three-subject SimBIDS BABS qualification campaign."""

from __future__ import annotations

import configparser
import csv
import json
import subprocess
import sys
from pathlib import Path

from validate_schemas import load_yaml, validate_operations_ledger, validation_errors


ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "operations" / "simbids-fmriprep-three-subject"
STUDY = ROOT / "studies" / "simbids"
ATTEMPT = STUDY / "derivatives" / "simbids-fmriprep-three-subject-attempt-001"
CONTAINERS = ATTEMPT / "containers"
EXPECTED_ID = "fcdddd73-613b-4ebd-b316-bcbce388099b"
EXPECTED_COMMIT = "7f5ea5f8b9784a121c67bc508ecba89b344fe629"
EXPECTED_RAW_ID = "6d1ba89e-a3d5-40fd-925a-4394f0d1e7f6"
EXPECTED_RAW_COMMIT = "76db7f4b0697f32336b5646c09fb16dad286e720"
EXPECTED_IMAGE_KEY = (
    "SHA256E-s344264704--"
    "244af4c6e1708dc10dd1f89f28951c9efa1c01571de778449ed4593ef8e9bbea"
)
EXPECTED_SUBJECTS = {"01", "02", "03"}
EXPECTED_ARCHIVE_KEYS = {
    "sub-01_fmriprep_anat-simbids-0-1-dev27.zip": "SHA256E-s188400--94569aa47b46f78e2848c0156d308d64a1b47f5e467eba405b6c6abf6b865bc4.zip",
    "sub-02_fmriprep_anat-simbids-0-1-dev27.zip": "SHA256E-s188401--6802de9f1925ee155d8275ffad79f07fdfe340ab2c577c38582d488b65154211.zip",
    "sub-03_fmriprep_anat-simbids-0-1-dev27.zip": "SHA256E-s188402--2c625b5984940d2c46b5309774c733842f116f441cc3c7c087b132bceb79e518.zip",
}
EXPECTED_BIDSIGNORE = {
    "**/figures",
    "**/figures/",
    "**/figures/**",
    "**/log",
    "**/log/",
    "**/log/**",
    "**/*_xfm.h5",
    "**/*_xfm.txt",
    "**/*.surf.gii",
    "**/*.shape.gii",
    "**/*.dscalar.nii",
    "**/*.dtseries.nii",
    "**/*_boldref.nii.gz",
    "**/*_boldref.json",
    "**/*_desc-confounds_timeseries.tsv",
}


def git(path: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=path, check=True, text=True, capture_output=True
    ).stdout.strip()


def dataset_id(path: Path) -> str:
    parser = configparser.ConfigParser()
    parser.read(path / ".datalad/config")
    return parser['datalad "dataset"']["id"]


def read_events() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in (OPS / "commands.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def archive_keys() -> dict[str, str]:
    output = git(
        ATTEMPT,
        "annex",
        "find",
        "--include=*.zip",
        "--format=${file}\\t${key}\\n",
    )
    return dict(line.split("\t", maxsplit=1) for line in output.splitlines() if line)


def validate() -> list[str]:
    errors: list[str] = []
    errors.extend(
        f"campaign.yaml: {error}"
        for error in validation_errors("campaign", load_yaml(OPS / "campaign.yaml"))
    )
    errors.extend(validate_operations_ledger(OPS / "commands.jsonl"))

    acceptance = load_yaml(OPS / "acceptance.yaml")
    if acceptance.get("derivative_dataset_id") != EXPECTED_ID:
        errors.append("acceptance dataset ID is not the accepted SimBIDS attempt ID")
    if acceptance.get("accepted_commit") != EXPECTED_COMMIT:
        errors.append("acceptance commit is not the independently validated commit")
    if acceptance.get("pilot_job_id") != "62027866":
        errors.append("acceptance does not identify the reviewed three-task Slurm job")
    if acceptance.get("pilot_exit_codes") != ["0:0", "0:0", "0:0"]:
        errors.append("acceptance does not record three successful Slurm task exits")
    if acceptance.get("finalization_method") != "plain-unzip-plus-datalad-save":
        errors.append("acceptance does not name the selected finalization policy")

    if dataset_id(ATTEMPT) != EXPECTED_ID:
        errors.append("accepted derivative DataLad identity differs")
    if git(ATTEMPT, "rev-parse", "HEAD") != EXPECTED_COMMIT:
        errors.append("accepted derivative worktree is not at the validated commit")
    if git(ATTEMPT, "status", "--porcelain"):
        errors.append("accepted derivative worktree is dirty")
    child_tree = git(
        STUDY,
        "ls-tree",
        "HEAD",
        "derivatives/simbids-fmriprep-three-subject-attempt-001",
    ).split()
    if len(child_tree) < 3 or child_tree[2] != EXPECTED_COMMIT:
        errors.append(
            "SimBIDS Study does not register the exact accepted derivative commit"
        )

    description = json.loads((ATTEMPT / "dataset_description.json").read_text())
    if description.get("DatasetType") != "derivative":
        errors.append("accepted attempt is not declared as a derivative")
    expected_sources = [
        {"URL": f"urn:uuid:{EXPECTED_RAW_ID}", "Version": EXPECTED_RAW_COMMIT}
    ]
    if description.get("SourceDatasets") != expected_sources:
        errors.append(
            "accepted derivative SourceDatasets is not the exact raw identity"
        )
    generated = description.get("GeneratedBy")
    if not isinstance(generated, list) or {item.get("Name") for item in generated} != {
        "SimBIDS",
        "BABS",
    }:
        errors.append("accepted derivative GeneratedBy metadata is incomplete")

    init_config = load_yaml(ATTEMPT / ".babs/babs_init_config.yaml")
    for key, expected in {
        "analysis_path": ".",
        "input_ria_path": ".babs/input_ria",
        "output_ria_path": ".babs/output_ria",
    }.items():
        if init_config.get(key) != expected:
            errors.append(f"BABS direct-layout setting {key} differs from {expected}")
    raw_config = init_config.get("input_datasets", {}).get("raw", {})
    if raw_config.get("path_in_babs") != "sourcedata/raw":
        errors.append("BABS raw input is not configured at sourcedata/raw")
    if init_config.get("all_results_in_one_zip") is not True:
        errors.append("BABS output wrapper policy is not all_results_in_one_zip")
    if (ATTEMPT / "inputs").exists():
        errors.append(
            "temporary checker compatibility input tree remains in accepted project"
        )

    participant_script = (ATTEMPT / "code/participant_job.sh").read_text()
    run_script = (ATTEMPT / "code/simbids-0-0-3_zip.sh").read_text()
    for token in (
        "pixi shell-hook --locked --environment babs",
        "sourcedata/raw",
        ".datalad/environments/simbids-0-0-3/image",
    ):
        if token not in participant_script:
            errors.append(f"generated participant script lacks required token {token}")
    for token in ("--containall", "--writable-tmpfs", "--network", "none"):
        if token not in run_script:
            errors.append(f"generated container command lacks isolation token {token}")
    for prohibited in (
        "envs/.pixi/envs",
        "export PATH=",
        "export HOME=",
        "XDG_CACHE_HOME",
    ):
        if prohibited in participant_script or prohibited in run_script:
            errors.append(
                f"generated scripts retain prohibited environment override {prohibited}"
            )
    if "#SBATCH --tmp" in participant_script:
        errors.append("accepted Unity participant script retains unsupported --tmp")

    containers_config = configparser.ConfigParser()
    containers_config.read(CONTAINERS / ".datalad/config")
    image_path = containers_config.get(
        'datalad "containers.simbids-0-0-3"', "image", fallback=""
    )
    conventional_image = ".datalad/environments/simbids-0-0-3/image"
    if image_path != conventional_image:
        errors.append(
            "SimBIDS image does not use conventional DataLad Containers registration"
        )
    elif git(CONTAINERS, "annex", "lookupkey", image_path) != EXPECTED_IMAGE_KEY:
        errors.append(
            "BABS container registration does not resolve the accepted SIF key"
        )

    with (OPS / "realized-inclusion.tsv").open(encoding="utf-8", newline="") as stream:
        inclusion = list(csv.DictReader(stream, delimiter="\t"))
    included = {row["sub_id"].removeprefix("sub-") for row in inclusion}
    if included != EXPECTED_SUBJECTS or len(inclusion) != 3:
        errors.append(
            "realized inclusion does not contain exactly subjects 01, 02, and 03"
        )
    for row in inclusion:
        if (
            row.get("eligibility") != "included"
            or row.get("babs_state") != "done"
            or row.get("runtime_state") != "completed"
            or row.get("job_id") != "62027866"
            or row.get("exit_code") != "0:0"
        ):
            errors.append(
                f"realized inclusion row is not successful: {row.get('sub_id')}"
            )

    subject_dirs = {
        path.name.removeprefix("sub-")
        for path in ATTEMPT.glob("sub-*")
        if path.is_dir()
    }
    if subject_dirs != EXPECTED_SUBJECTS:
        errors.append(
            "accepted derivative does not contain exactly three subject payloads"
        )
    if archive_keys() != EXPECTED_ARCHIVE_KEYS:
        errors.append(
            "retained result archives do not have the accepted SHA256E identities"
        )
    all_annex_keys = git(ATTEMPT, "annex", "find", "--format=${key}\\n").splitlines()
    if any(key.startswith("MD5") for key in all_annex_keys):
        errors.append("accepted derivative retains an MD5 annex key")

    bidsignore = {
        line.strip()
        for line in (ATTEMPT / ".bidsignore").read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if bidsignore != EXPECTED_BIDSIGNORE:
        errors.append(".bidsignore differs from the reviewed payload-only exceptions")
    for operational in ("containers", "code", "logs", "sourcedata", ".babs", ".zip"):
        if any(operational in pattern for pattern in bidsignore):
            errors.append(
                f".bidsignore improperly hides operational path {operational}"
            )

    report = json.loads((OPS / "validation-attempt-001.json").read_text())
    root_report = json.loads(
        (ROOT / "docs/reports/phase-3/simbids-derivative-validation.json").read_text()
    )
    report_for_comparison = {
        **report,
        "reviewed_warnings": sorted(
            report.get("reviewed_warnings", []),
            key=lambda item: item.get("location", ""),
        ),
    }
    root_report_for_comparison = {
        **root_report,
        "reviewed_warnings": sorted(
            root_report.get("reviewed_warnings", []),
            key=lambda item: item.get("location", ""),
        ),
    }
    if report_for_comparison != root_report_for_comparison:
        errors.append("operations and root Deno validation reports differ")
    if (
        report.get("dataset_id") != EXPECTED_ID
        or report.get("dataset_commit") != EXPECTED_COMMIT
    ):
        errors.append("Deno report does not identify the accepted derivative")
    if report.get("validator_distribution") != "bids-validator-deno":
        errors.append(
            "Phase 3 report was not produced by the Deno validator distribution"
        )
    if report.get("errors") != [] or report.get("status") != "pass":
        errors.append("Deno validation report is not error-free")
    if set(report.get("subjects", [])) != EXPECTED_SUBJECTS:
        errors.append("Deno report does not cover all three accepted subjects")
    warnings = report.get("reviewed_warnings", [])
    if len(warnings) != 6 or {item.get("code") for item in warnings} != {"NIFTI_UNIT"}:
        errors.append(
            "Deno report warnings differ from the six reviewed synthetic warnings"
        )

    events = read_events()
    event_types = {event.get("event_type") for event in events}
    required_events = {
        "initialize",
        "setup-check",
        "sync",
        "pilot",
        "status",
        "merge",
        "finalize",
        "validate",
        "accept",
    }
    if not required_events.issubset(event_types):
        errors.append(
            "operations ledger lacks one or more required lifecycle transitions"
        )
    if not events or events[-1].get("event_type") != "accept":
        errors.append("operations ledger does not terminate in acceptance")
    pilot_events = [event for event in events if event.get("event_type") == "pilot"]
    if len(pilot_events) != 1 or "3" not in pilot_events[0].get("argv", []):
        errors.append("operations ledger does not record one three-task pilot")
    state = load_yaml(OPS / "state.yaml")
    if state.get("observed_state") != "accepted" or state.get("accepted") is not True:
        errors.append("operations state is not accepted")
    if not (ATTEMPT / ".babs/output_ria/alias/data").is_symlink():
        errors.append("accepted output RIA alias is absent")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("Phase 3 three-subject SimBIDS BABS qualification passes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
