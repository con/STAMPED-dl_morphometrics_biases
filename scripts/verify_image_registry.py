#!/usr/bin/env python3
"""Retrieve and verify a registered exact SIF against the accepted dataset."""

from __future__ import annotations

import argparse
import configparser
import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = ROOT / "envs" / "containers" / "accepted"
RECORDS = ROOT / "envs" / "images"
INDEX = ROOT / "envs" / "images.lock.yaml"


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain one mapping")
    return value


def command(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(
            f"{' '.join(argv)} failed ({result.returncode}): "
            f"{(result.stderr or result.stdout).strip()}"
        )
    return result.stdout.strip()


def dataset_id(path: Path) -> str:
    config = configparser.ConfigParser()
    config.read(path / ".datalad" / "config")
    return config['datalad "dataset"']["id"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify(image_id: str) -> list[str]:
    errors: list[str] = []
    record_path = RECORDS / f"{image_id}.yaml"
    if not record_path.is_file():
        return [f"missing image record: {record_path.relative_to(ROOT)}"]
    if not INDEX.is_file():
        return [f"missing image index: {INDEX.relative_to(ROOT)}"]
    if not ACCEPTED.is_dir():
        return [f"missing accepted dataset: {ACCEPTED.relative_to(ROOT)}"]

    record = read_yaml(record_path)
    index = read_yaml(INDEX)
    if record.get("image_id") != image_id:
        errors.append("record image_id does not match requested image")
    if record.get("state") != "accepted-registered":
        errors.append("only accepted-registered images may be verified here")

    accepted_id = dataset_id(ACCEPTED)
    accepted_commit = command(["git", "rev-parse", "HEAD"], cwd=ACCEPTED)
    if record.get("accepted_dataset_id") != accepted_id:
        errors.append("record accepted_dataset_id does not match accepted dataset")
    record_commit = record.get("accepted_dataset_commit")
    if not isinstance(record_commit, str):
        errors.append("record accepted_dataset_commit is absent")
    else:
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", record_commit, accepted_commit],
            cwd=ACCEPTED,
            capture_output=True,
            text=True,
            check=False,
        )
        if ancestor.returncode:
            errors.append(
                "record accepted_dataset_commit is not an ancestor of the current "
                "accepted dataset"
            )
    indexed_dataset = index.get("accepted_dataset")
    if indexed_dataset != {"id": accepted_id, "commit": accepted_commit}:
        errors.append("image index accepted_dataset does not match accepted dataset")

    images = index.get("images")
    if not isinstance(images, list):
        errors.append("images.lock.yaml must contain an images list")
        images = []
    matches = [item for item in images if item.get("image_id") == image_id]
    if len(matches) != 1:
        errors.append("images.lock.yaml must contain exactly one matching image")
    elif matches[0] != {
        "image_id": image_id,
        "accepted_dataset_id": record.get("accepted_dataset_id"),
        "accepted_dataset_commit": record.get("accepted_dataset_commit"),
        "sif_annex_key": record.get("sif_annex_key"),
        "sif_sha256": record.get("sif_sha256"),
    }:
        errors.append("image index does not exactly mirror the authoritative record")

    relative = record.get("accepted_image_path")
    if (
        not isinstance(relative, str)
        or relative.startswith("/")
        or ".." in relative.split("/")
    ):
        return [*errors, "record accepted_image_path must be a safe relative path"]
    image_path = ACCEPTED / relative
    if not image_path.exists():
        try:
            command(["datalad", "get", "-d", str(ACCEPTED), str(image_path)])
        except RuntimeError as error:
            errors.append(str(error))
    if not image_path.is_file():
        return [*errors, f"registered SIF is unavailable: {relative}"]

    annex_key = command(["git", "annex", "lookupkey", relative], cwd=ACCEPTED)
    if record.get("sif_annex_key") != annex_key:
        errors.append("record sif_annex_key does not match git-annex")
    if isinstance(record_commit, str):
        try:
            historical_target = command(
                ["git", "show", f"{record_commit}:{relative}"], cwd=ACCEPTED
            )
        except RuntimeError as error:
            errors.append(str(error))
        else:
            if Path(historical_target).name != record.get("sif_annex_key"):
                errors.append(
                    "recorded registry commit does not contain the recorded annex key"
                )
    if record.get("sif_sha256") != sha256(image_path):
        errors.append("record sif_sha256 does not match SIF bytes")

    dataset_config = configparser.ConfigParser()
    dataset_config.read(ACCEPTED / ".datalad" / "config")
    configured_path = dataset_config.get(f'datalad "containers.{image_id}"', "image")
    if configured_path != relative:
        errors.append(
            "DataLad Containers registration does not resolve to the recorded SIF"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    args = parser.parse_args()
    errors = verify(args.image)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"verified accepted SIF identity: {args.image}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
