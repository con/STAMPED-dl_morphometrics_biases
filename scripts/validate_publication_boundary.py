#!/usr/bin/env python3
"""Simulate a public push and prove protected classes remain unreachable."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
PROTECTED_FILES = {
    "inputs/controlled-input.bin": b"PROTECTED_INPUT_MARKER\n",
    "identifiers/participants.tsv": b"participant_id\nPROTECTED_IDENTIFIER_MARKER\n",
    "logs/participant-job.log": b"PROTECTED_LOG_MARKER\n",
    "derivatives/participant-output.bin": b"PROTECTED_DERIVATIVE_MARKER\n",
}
PROTECTED_REMOTE_NAME = "protected-storage"


def run(
    argv: Sequence[str],
    *,
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(
        list(argv),
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )
    if check and result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(argv)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def initialize_annex(path: Path, description: str) -> None:
    path.mkdir(parents=True)
    run(["git", "init", "-b", "main"], cwd=path)
    run(["git", "config", "user.name", "Phase 1 boundary simulation"], cwd=path)
    run(["git", "config", "user.email", "simulation@example.invalid"], cwd=path)
    run(["git", "config", "annex.backend", "SHA256E"], cwd=path)
    run(["git", "annex", "init", description], cwd=path)
    (path / ".gitattributes").write_text(
        "* annex.backend=SHA256E\n"
        "*.bin annex.largefiles=anything\n"
        "*.tsv annex.largefiles=anything\n"
        "*.log annex.largefiles=anything\n",
        encoding="utf-8",
    )


def add_and_commit(path: Path, message: str) -> None:
    run(["git", "annex", "add", "."], cwd=path)
    run(["git", "commit", "-m", message], cwd=path)


def annex_key(path: Path, relative: str) -> str:
    return run(["git", "annex", "lookupkey", relative], cwd=path).stdout.strip()


def run_simulation() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="stamped-phase1-publication-") as temp:
        base = Path(temp)
        public_source = base / "public-source"
        protected_source = base / "protected-source"
        public_git = base / "public.git"
        public_annex = base / "public-annex"
        protected_annex = base / "protected-annex"
        public_clone = base / "public-clone"
        public_annex.mkdir()
        protected_annex.mkdir()

        initialize_annex(public_source, "credential-free public simulation")
        (public_source / "public-policy.txt").write_text(
            "PUBLIC_POLICY_MARKER\n", encoding="utf-8"
        )
        (public_source / "public-payload.bin").write_bytes(b"PUBLIC_ANNEX_MARKER\n")
        add_and_commit(public_source, "Create synthetic public fixture")
        public_key = annex_key(public_source, "public-payload.bin")

        initialize_annex(protected_source, "isolated protected simulation")
        for relative, payload in PROTECTED_FILES.items():
            target = protected_source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        add_and_commit(protected_source, "Create synthetic protected fixture")
        protected_keys = {
            relative: annex_key(protected_source, relative)
            for relative in PROTECTED_FILES
        }

        run(
            [
                "git",
                "annex",
                "initremote",
                PROTECTED_REMOTE_NAME,
                "type=directory",
                f"directory={protected_annex}",
                "encryption=none",
            ],
            cwd=protected_source,
        )
        run(["git", "annex", "copy", "--to", PROTECTED_REMOTE_NAME], cwd=protected_source)

        run(["git", "init", "--bare", str(public_git)], cwd=base)
        run(["git", "remote", "add", "public", str(public_git)], cwd=public_source)
        run(
            [
                "git",
                "annex",
                "initremote",
                "public-storage",
                "type=directory",
                f"directory={public_annex}",
                "encryption=none",
            ],
            cwd=public_source,
        )
        run(["git", "annex", "copy", "--to", "public-storage"], cwd=public_source)
        run(["git", "push", "public", "main", "git-annex"], cwd=public_source)
        dry_run = run(
            ["git", "push", "--dry-run", "public", "main", "git-annex"],
            cwd=public_source,
        )
        run(["git", "clone", str(public_git), str(public_clone)], cwd=base)

        public_names = run(
            ["git", "rev-list", "--objects", "--all"], cwd=public_clone
        ).stdout
        public_refs = run(["git", "show-ref"], cwd=public_clone).stdout
        public_remotes = run(["git", "remote", "-v"], cwd=public_clone).stdout
        annex_paths = "\n".join(
            str(path.relative_to(public_annex))
            for path in public_annex.rglob("*")
            if path.is_file()
        )

        failures: list[str] = []
        for relative, marker in PROTECTED_FILES.items():
            if relative in public_names:
                failures.append(f"protected path reached public Git refs: {relative}")
            marker_text = marker.decode("utf-8").strip()
            grep = run(
                ["git", "grep", "-I", "-F", marker_text, *run(["git", "rev-list", "--all"], cwd=public_clone).stdout.split()],
                cwd=public_clone,
                check=False,
            )
            if grep.returncode == 0:
                failures.append(f"protected marker reached public Git refs: {marker_text}")
        for relative, key in protected_keys.items():
            if key in public_names or key in annex_paths:
                failures.append(f"protected annex key reached public storage: {relative}")
        if PROTECTED_REMOTE_NAME in public_names + public_refs + public_remotes:
            failures.append("protected remote name reached public repository")
        if public_key not in public_names and public_key not in annex_paths:
            failures.append("public annex payload did not reach public publication boundary")

        result: dict[str, object] = {
            "schema_version": 1,
            "simulation": "credential-free-local-git-annex-publication",
            "public_git_push_dry_run": dry_run.returncode == 0,
            "public_clone_succeeded": True,
            "protected_classes_tested": [
                "controlled-input",
                "protected-identifier",
                "protected-log",
                "protected-derivative",
            ],
            "protected_paths_absent": not any(
                relative in public_names for relative in PROTECTED_FILES
            ),
            "protected_annex_keys_absent": not any(
                key in public_names or key in annex_paths
                for key in protected_keys.values()
            ),
            "protected_remote_absent": PROTECTED_REMOTE_NAME
            not in public_names + public_refs + public_remotes,
            "public_annex_payload_present": public_key in public_names
            or public_key in annex_paths,
            "failures": failures,
            "status": "pass" if not failures else "fail",
        }
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = run_simulation()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        report = args.report if args.report.is_absolute() else ROOT / args.report
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
