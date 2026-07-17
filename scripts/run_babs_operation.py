#!/usr/bin/env python3
"""Launch one declared BABS lifecycle command for a resolved campaign.

Normal executions are observed by con-duct. Its logs are written inside the
campaign dataset so they remain alongside the BABS lifecycle evidence and can
be assigned the campaign's access class. The BABS argv remains the inner
command; con-duct is only an execution-observability wrapper.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPERATIONS = {
    "init": "babs-init",
    "check-setup": "babs-check-setup",
    "submit": "babs-submit",
    "status": "babs-status",
    "merge": "babs-merge",
    "unzip": "babs-unzip",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=sorted(OPERATIONS))
    parser.add_argument("campaign", help="Phase 3 operations/<campaign> dataset name")
    parser.add_argument("--dry-run", action="store_true")
    args, babs_args = parser.parse_known_args()

    argv = [OPERATIONS[args.operation], *babs_args]
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
    return subprocess.run(observed_argv, cwd=campaign, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
