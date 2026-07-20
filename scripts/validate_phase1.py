#!/usr/bin/env python3
"""Validate the complete Phase 1 repository and BIDS Study guardrails."""

from __future__ import annotations

import configparser
import json
import subprocess
import sys
from pathlib import Path

from validate_bids import validate_all as validate_bids
from validate_publication_boundary import run_simulation
from validate_schemas import validate_all as validate_schemas
from validate_stamped import validate as validate_stamped


ROOT = Path(__file__).resolve().parents[1]
ROOT_ID = "baa2ec91-e618-4bac-b382-ac0daf9f779a"
STUDY_ID = "2d982b94-44a2-49ba-bfcd-97966084b025"
RAW_ID = "787b9dfe-8399-46a2-bdb9-5230a949e88a"
REQUIRED_PATHS = (
    "AGENTS.md",
    "REUSE.toml",
    "LICENSES/MIT.txt",
    "apps/README.md",
    "src/README.md",
    "tests/README.md",
    "notebooks/README.md",
    "envs/containers/repronim/README.md",
    "envs/containers/custom/README.md",
    "envs/containers/accepted/README.md",
    "config/datasets/README.md",
    "config/pipelines/README.md",
    "config/clusters/README.md",
    "config/campaigns/README.md",
    "config/access/data-classes.tsv",
    "config/access/sibling-matrix.tsv",
    "config/schemas/campaign.schema.json",
    "config/schemas/operations-event.schema.json",
    "config/schemas/image-record.schema.json",
    "config/schemas/result-manifest.schema.json",
    "operations/README.md",
    "studies/README.md",
    "results/README.md",
    "studies/toy/dataset_description.json",
    "studies/toy/sourcedata/raw/dataset_description.json",
    "result-manifest.tsv",
    "skills/stamped-neuroimaging-analysis/SKILL.md",
    "skills/bids-app-builder/SKILL.md",
)
REQUIRED_REPORTS = (
    "bids-raw.json",
    "bids-study.json",
    "clean-recursive-clone.json",
    "datalad-subdatasets.jsonl",
    "git-annex-info.json",
    "publication-boundary.json",
    "pytest.txt",
    "reuse-lint.txt",
    "stamped-ideal.txt",
    "tool-versions.txt",
)


def dataset_id(path: Path) -> str:
    config = configparser.ConfigParser()
    config.read(path / ".datalad" / "config")
    return config['datalad "dataset"']["id"]


def output(argv: list[str], *, cwd: Path = ROOT) -> str:
    return subprocess.run(
        argv, cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def validate() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).exists():
            errors.append(f"missing Phase 1 path: {relative}")
    derivatives = ROOT / "studies" / "toy" / "derivatives"
    if derivatives.exists():
        children = [path for path in derivatives.iterdir() if path.is_dir()]
        if not children or any(not (path / ".datalad/config").is_file() for path in children):
            errors.append("toy derivatives must be realized DataLad datasets, not placeholders")

    if dataset_id(ROOT) != ROOT_ID:
        errors.append("top-level DataLad identity changed")
    if dataset_id(ROOT / "studies" / "toy") != STUDY_ID:
        errors.append("toy Study DataLad identity changed")
    if dataset_id(ROOT / "studies" / "toy" / "sourcedata" / "raw") != RAW_ID:
        errors.append("toy raw DataLad identity changed")
    backend_attribute = output(
        [
            "git",
            "check-attr",
            "annex.backend",
            "--",
            "docs/reference/recon_all_recon_any_poster_ohbm2025.pdf",
        ]
    )
    if not backend_attribute.endswith(": SHA256E"):
        errors.append("root annex backend attribute is not SHA256E")
    if output(["git", "config", "--get", "annex.version"]) != "10":
        errors.append("root annex repository version is not 10")

    staged = output(["git", "ls-files", "--stage", "studies/toy"])
    if staged and not staged.startswith("160000 "):
        errors.append("studies/toy is not registered as a gitlink")
    if not staged:
        errors.append("studies/toy is not registered in the root dataset")
    raw_staged = output(
        ["git", "ls-files", "--stage", "sourcedata/raw"],
        cwd=ROOT / "studies" / "toy",
    )
    if not raw_staged.startswith("160000 "):
        errors.append("toy raw child is not registered as a gitlink")

    remotes = {
        "origin": output(["git", "remote", "get-url", "origin"]),
        "gin": output(["git", "remote", "get-url", "gin"]),
    }
    if remotes["origin"] not in {
        "git@github.com:con/STAMPED-dl_morphometrics_biases.git",
        "https://github.com/con/STAMPED-dl_morphometrics_biases.git",
    }:
        errors.append("GitHub origin changed")
    if remotes["gin"] != "https://gin.g-node.org/leej3/STAMPED-dl_morphometrics_biases":
        errors.append("GIN fetch sibling changed")
    if output(["git", "config", "--get", "remote.origin.annex-ignore"]) != "true":
        errors.append("GitHub origin must remain annex-ignore=true")
    if (
        output(["git", "config", "--get", "remote.gin.annex-uuid"])
        != "99822df6-f62f-4161-925a-e444e68c8625"
    ):
        errors.append("GIN annex sibling UUID changed")

    errors.extend(validate_schemas())
    _, bids_errors = validate_bids()
    errors.extend(bids_errors)
    publication = run_simulation()
    errors.extend(str(item) for item in publication["failures"])
    errors.extend(validate_stamped(ideal=False))

    negative = ROOT / "tests" / "fixtures" / "stamped"
    negative_errors = validate_stamped(
        ideal=False,
        assessment_path=negative / "assessment-missing.tsv",
        components_path=negative / "components-missing.tsv",
    )
    if not any("omitted MUST/SHOULD decisions" in item for item in negative_errors):
        errors.append("negative STAMPED fixture did not prove omission failure")

    reuse = subprocess.run(
        ["reuse", "lint"], cwd=ROOT, check=False, capture_output=True, text=True
    )
    if reuse.returncode:
        errors.append("root reuse lint failed")
    for relative in ("studies/toy", "studies/toy/sourcedata/raw"):
        reuse = subprocess.run(
            ["reuse", "lint"],
            cwd=ROOT / relative,
            check=False,
            capture_output=True,
            text=True,
        )
        if reuse.returncode:
            errors.append(f"{relative} reuse lint failed")

    reports = ROOT / "docs" / "reports" / "phase-1"
    if any(reports.glob("*.json")) or any(reports.glob("*.txt")):
        for name in REQUIRED_REPORTS:
            path = reports / name
            if not path.is_file() or not path.read_text(encoding="utf-8").strip():
                errors.append(f"missing or empty Phase 1 report: {name}")
        for name in ("bids-raw.json", "bids-study.json", "publication-boundary.json", "clean-recursive-clone.json"):
            path = reports / name
            if path.is_file() and json.loads(path.read_text(encoding="utf-8")).get("status") != "pass":
                errors.append(f"Phase 1 report is not passing: {name}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Phase 1 repository, Study, schema, licensing, and access guardrails pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
