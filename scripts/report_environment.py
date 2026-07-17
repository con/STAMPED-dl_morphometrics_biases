#!/usr/bin/env python3
"""Report resolved tool identities without confusing them for a SIF identity."""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def command_version(command: tuple[str, ...]) -> str | None:
    executable = shutil.which(command[0])
    if executable is None:
        return None
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    output = (result.stdout or result.stderr).strip().splitlines()
    if not output:
        return f"{' '.join(command)} returned {result.returncode}"
    return next((line for line in output if "version" in line.lower()), output[0])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--environment", required=True)
    args = parser.parse_args()

    report = {
        "environment": args.environment,
        "workspace": str(ROOT),
        "platform": platform.platform(),
        "tools": {
            name: command_version(command)
            for name, command in {
                "pixi": ("pixi", "--version"),
                "python": ("python", "--version"),
                "datalad": ("datalad", "--version"),
                "git-annex": ("git", "annex", "version"),
                "babs": ("babs", "--version"),
                "apptainer": ("apptainer", "--version"),
                "singularity": ("singularity", "--version"),
                "limactl": ("limactl", "--version"),
                "cosign": ("cosign", "version"),
                "syft": ("syft", "--version"),
            }.items()
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
