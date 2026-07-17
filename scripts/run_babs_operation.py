#!/usr/bin/env python3
"""Launch one declared BABS lifecycle command for a resolved campaign."""

from __future__ import annotations

import argparse
import subprocess
import sys
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
        print(" ".join(argv))
        return 0
    campaign = ROOT / "operations" / args.campaign
    if not campaign.is_dir():
        parser.error(
            f"campaign dataset {campaign.relative_to(ROOT)} does not exist; "
            "Phase 3 must create and resolve it before a BABS operation runs"
        )
    return subprocess.run(argv, cwd=campaign, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
