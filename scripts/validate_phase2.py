#!/usr/bin/env python3
"""Validate the Phase 2 Pixi and exact-SIF registry foundation."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from validate_docs import validate as validate_docs
from validate_schemas import validation_errors
from verify_image_registry import ACCEPTED, RECORDS, read_yaml, verify


ROOT = Path(__file__).resolve().parents[1]
PIXIMANIFEST = ROOT / "envs" / "pixi.toml"
PIXILOCK = ROOT / "envs" / "pixi.lock"
REPRONIM = ROOT / "envs" / "containers" / "repronim"
REPRONIM_COMMIT = "0284fc8ad8b7fa9a76c3c9f03cfb2919708ba2b2"
REQUIRED_ENVIRONMENTS = {
    "dev",
    "analysis",
    "babs",
    "image-analysis",
    "image-authoring",
}


def git_head(path: Path) -> str | None:
    head = path / ".git"
    if not head.exists():
        return None
    import subprocess

    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None


def validate() -> list[str]:
    errors: list[str] = []
    manifest = PIXIMANIFEST.read_text(encoding="utf-8")
    lock = PIXILOCK.read_text(encoding="utf-8")
    if 'requires-pixi = "==0.66.0"' not in manifest:
        errors.append("Pixi 0.66.0 is not pinned")
    if 'platforms = ["osx-arm64", "osx-64", "linux-64"]' not in manifest:
        errors.append("development and Linux target platforms are incomplete")
    for environment in REQUIRED_ENVIRONMENTS:
        if not re.search(rf"^{re.escape(environment)}\s*=", manifest, flags=re.MULTILINE):
            errors.append(f"missing named Pixi environment: {environment}")
    for token in (
        "pandas = \"<2\"",
        "freesurfer-stats = \"==1.2.0\"",
        "2cc536a51282124f3811ffa971f82a7c34116af5",
        "apptainer = \"==1.5.2\"",
        "cosign = \"==3.0.4\"",
        "syft = \"==1.48.0\"",
    ):
        if token not in manifest:
            errors.append(f"missing required Phase 2 dependency declaration: {token}")
    if '[feature.image-linux]\nplatforms = ["linux-64"]' not in manifest:
        errors.append("image execution dependencies must be restricted to linux-64")
    if "PennLINC/babs.git?rev=2cc536a51282124f3811ffa971f82a7c34116af5" not in lock:
        errors.append("Pixi lock does not resolve the pinned BABS revision")
    for link, target in {"pixi.toml": "envs/pixi.toml", "pixi.lock": "envs/pixi.lock", ".pixi": "envs/.pixi"}.items():
        path = ROOT / link
        if not path.is_symlink() or path.readlink().as_posix() != target:
            errors.append(f"missing tracked discovery link: {link} -> {target}")

    errors.extend(validate_docs())
    if git_head(REPRONIM) != REPRONIM_COMMIT:
        errors.append("ReproNim/containers source dataset is not at the pinned commit")
    if not ACCEPTED.joinpath(".datalad", "config").is_file():
        errors.append("accepted container dataset has not been created")

    records = sorted(RECORDS.glob("*.yaml")) if RECORDS.is_dir() else []
    if not records:
        errors.append("no image records are present")
    for record_path in records:
        record = read_yaml(record_path)
        errors.extend(
            f"{record_path.relative_to(ROOT)}: {error}"
            for error in validation_errors("image", record)
        )
        image_id = record.get("image_id")
        if isinstance(image_id, str) and record.get("state") == "accepted-registered":
            errors.extend(verify(image_id))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("Phase 2 Pixi workspace and exact-SIF registry foundation pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
