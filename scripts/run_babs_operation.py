#!/usr/bin/env python3
"""Launch one declared BABS lifecycle command for a resolved campaign.

Normal executions are observed by con-duct. Its logs are written inside the
campaign dataset so they remain alongside the BABS lifecycle evidence and can
be assigned the campaign's access class. The BABS argv remains the inner
command; con-duct is only an execution-observability wrapper.
"""

from __future__ import annotations

import argparse
import datetime as dt
import getpass
import hashlib
import json
import os
import subprocess
import uuid
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
OPERATIONS = {
    "init": "init",
    "check-setup": "check-setup",
    "sync-code": "sync-code",
    "pilot": "submit",
    "submit": "submit",
    "status": "status",
    "merge": "merge",
}
EVENT_TYPES = {
    "init": "initialize",
    "check-setup": "setup-check",
    "sync-code": "sync",
    "pilot": "pilot",
    "submit": "submit",
    "status": "status",
    "merge": "merge",
}


def tool_versions() -> dict[str, str]:
    commands = {
        "babs": ["babs", "--version"],
        "con-duct": ["con-duct", "--version"],
        "datalad": ["datalad", "--version"],
        "git-annex": ["git-annex", "version", "--raw"],
        "singularity": ["singularity", "--version"],
    }
    versions = {}
    for name, command in commands.items():
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        versions[name] = (result.stdout or result.stderr).strip().splitlines()[0]
    return versions


def append_event(
    campaign: Path,
    campaign_id: str,
    attempt_id: str,
    operation: str,
    argv: list[str],
    rc: int,
) -> None:
    ledger = campaign / "commands.jsonl"
    prior = (
        [line for line in ledger.read_bytes().splitlines() if line.strip()]
        if ledger.exists()
        else []
    )
    evidence = sorted(
        str(path.relative_to(campaign))
        for path in (campaign / "logs").glob("*")
        if path.is_file()
    )
    event = {
        "schema_version": 1,
        "event_id": str(uuid.uuid4()),
        "campaign_id": campaign_id,
        "attempt_id": attempt_id,
        "sequence": len(prior) + 1,
        "timestamp": dt.datetime.now(dt.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "event_type": EVENT_TYPES[operation],
        "actor": getpass.getuser(),
        "argv": argv,
        "tool_versions": tool_versions(),
        "desired_state": f"{operation} completes successfully for {attempt_id}",
        "observed_state": f"command exited with status {rc}",
        "evidence": evidence,
        "access_class": "public",
        "previous_event_sha256": hashlib.sha256(prior[-1]).hexdigest()
        if prior
        else None,
    }
    with ledger.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
    message = (
        f"Record BABS {operation} operation\n\n"
        "Co-Authored-By: codex-cli 0.144.6 / gpt-5.6-sol <codex@openai.com>"
    )
    subprocess.run(["git", "add", "commands.jsonl", "logs"], cwd=campaign, check=True)
    subprocess.run(["git", "commit", "-m", message], cwd=campaign, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=sorted(OPERATIONS))
    parser.add_argument("campaign", help="Phase 3 operations/<campaign> dataset name")
    parser.add_argument("--attempt-id", default="attempt-001")
    parser.add_argument("--dry-run", action="store_true")
    args, babs_args = parser.parse_known_args()

    env_file = ROOT / ".env"
    load_dotenv(env_file, override=False)
    os.environ.setdefault("DUCT_CONFIG_PATHS", str(env_file))
    if babs_args[:1] == ["--"]:
        babs_args = babs_args[1:]
    argv = ["babs", OPERATIONS[args.operation], *babs_args]
    if args.dry_run:
        print(" ".join(["con-duct", "run", "--mode", "current-session", *argv]))
        return 0
    campaign = ROOT / "operations" / args.campaign
    if not campaign.is_dir():
        parser.error(
            f"campaign dataset {campaign.relative_to(ROOT)} does not exist; "
            "Phase 3 must create and resolve it before a BABS operation runs"
        )
    output_prefix = campaign / "logs" / f"duct-{args.operation}-{{datetime}}-{{pid}}_"
    observed_argv = [
        "con-duct",
        "run",
        "--mode",
        "current-session",
        "--fail-time",
        "0",
        "--capture-outputs",
        "all",
        "--outputs",
        "all",
        "--output-prefix",
        str(output_prefix),
        "--message",
        f"BABS {args.operation} lifecycle operation for {args.campaign}",
        *argv,
    ]
    rc = subprocess.run(observed_argv, cwd=campaign, check=False).returncode
    append_event(campaign, args.campaign, args.attempt_id, args.operation, argv, rc)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
