#!/usr/bin/env python3
"""Append a validated historical lifecycle transition to a campaign ledger."""

from __future__ import annotations

import argparse
import datetime as dt
import getpass
import hashlib
import json
import subprocess
import uuid
from pathlib import Path

from run_babs_operation import ROOT, tool_versions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event_type")
    parser.add_argument("campaign")
    parser.add_argument("attempt_id")
    parser.add_argument("desired_state")
    parser.add_argument("observed_state")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv[:1] == ["--"] else args.argv
    if not argv:
        parser.error("an exact historical argv is required after --")

    campaign = ROOT / "operations" / args.campaign
    ledger = campaign / "commands.jsonl"
    prior = [line for line in ledger.read_bytes().splitlines() if line.strip()]
    event = {
        "schema_version": 1,
        "event_id": str(uuid.uuid4()),
        "campaign_id": args.campaign,
        "attempt_id": args.attempt_id,
        "sequence": len(prior) + 1,
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "event_type": args.event_type,
        "actor": getpass.getuser(),
        "argv": argv,
        "tool_versions": tool_versions(),
        "desired_state": args.desired_state,
        "observed_state": args.observed_state,
        "evidence": args.evidence,
        "access_class": "public",
        "previous_event_sha256": hashlib.sha256(prior[-1]).hexdigest(),
    }
    with ledger.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
    message = (
        f"Record {args.event_type} transition for {args.attempt_id}\n\n"
        "Co-Authored-By: codex-cli 0.144.6 / gpt-5.6-sol <codex@openai.com>"
    )
    subprocess.run(["git", "add", "commands.jsonl"], cwd=campaign, check=True)
    subprocess.run(["git", "commit", "-m", message], cwd=campaign, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
