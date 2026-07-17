#!/usr/bin/env python3
"""Generate non-sensitive Phase 1 validation evidence from a committed root."""

from __future__ import annotations

import json
import subprocess
import tempfile
from importlib.metadata import version
from pathlib import Path

from validate_bids import validate_all as validate_bids
from validate_publication_boundary import run_simulation


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "docs" / "reports" / "phase-1"


def run(argv: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, check=check, capture_output=True, text=True
    )


def write(name: str, content: str) -> None:
    (REPORTS / name).write_text(content.rstrip() + "\n", encoding="utf-8")


def clean_clone_report() -> dict[str, object]:
    source_commit = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="stamped-phase1-clone-") as temp:
        clone = Path(temp) / "clone"
        result = run(["datalad", "clone", str(ROOT), str(clone)], check=False)
        failures: list[str] = []
        if result.returncode:
            failures.append(f"recursive clone failed: {result.stderr.strip()}")
            return {
                "schema_version": 1,
                "source_commit": source_commit,
                "status": "fail",
                "failures": failures,
            }
        install = run(
            ["datalad", "get", "-n", "-r", "studies/toy"],
            cwd=clone,
            check=False,
        )
        if install.returncode:
            failures.append(f"recursive subdataset installation failed: {install.stderr.strip()}")
            return {
                "schema_version": 1,
                "source_commit": source_commit,
                "status": "fail",
                "failures": failures,
            }
        expected = {
            ".": "baa2ec91-e618-4bac-b382-ac0daf9f779a",
            "studies/toy": "2d982b94-44a2-49ba-bfcd-97966084b025",
            "studies/toy/sourcedata/raw": "787b9dfe-8399-46a2-bdb9-5230a949e88a",
        }
        observed: dict[str, dict[str, str]] = {}
        for relative, expected_id in expected.items():
            path = clone if relative == "." else clone / relative
            dataset_id = run(
                ["git", "config", "-f", ".datalad/config", "--get", "datalad.dataset.id"],
                cwd=path,
            ).stdout.strip()
            commit = run(["git", "rev-parse", "HEAD"], cwd=path).stdout.strip()
            observed[relative] = {"dataset_id": dataset_id, "commit": commit}
            if dataset_id != expected_id:
                failures.append(f"{relative}: unexpected DataLad ID {dataset_id}")
        status = run(["datalad", "status", "-r"], cwd=clone, check=False)
        if status.returncode or "nothing to save, working tree clean" not in status.stdout:
            failures.append("recursive clone is not clean")
        if not (clone / "docs" / "reference" / "recon_all_recon_any_poster_ohbm2025.pdf").is_symlink():
            failures.append("annexed poster identity is absent from clean clone")
        return {
            "schema_version": 1,
            "source_commit": source_commit,
            "recursive_clone": True,
            "annex_content_requested": False,
            "datasets": observed,
            "failures": failures,
            "status": "pass" if not failures else "fail",
        }


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    reports, bids_errors = validate_bids()
    if bids_errors:
        raise SystemExit("BIDS validation failed: " + "; ".join(bids_errors))
    for report in reports:
        write(
            f"bids-{report['dataset_kind']}.json",
            json.dumps(report, indent=2, sort_keys=True),
        )

    publication = run_simulation()
    write("publication-boundary.json", json.dumps(publication, indent=2, sort_keys=True))
    if publication["status"] != "pass":
        raise SystemExit("publication-boundary simulation failed")

    clone = clean_clone_report()
    write("clean-recursive-clone.json", json.dumps(clone, indent=2, sort_keys=True))
    if clone["status"] != "pass":
        raise SystemExit("clean recursive clone failed")

    subdatasets = run(["datalad", "-f", "json", "subdatasets", "-r"]).stdout
    portable_subdatasets = []
    for line in subdatasets.splitlines():
        record = json.loads(line)
        for field in ("path", "parentds", "refds"):
            value = record.get(field)
            if value:
                try:
                    relative = Path(value).relative_to(ROOT)
                    record[field] = str(relative) if str(relative) != "." else "."
                except ValueError:
                    record[field] = "outside-root"
        portable_subdatasets.append(json.dumps(record, sort_keys=True))
    write("datalad-subdatasets.jsonl", "\n".join(portable_subdatasets))
    write("git-annex-info.json", run(["git", "annex", "info", "--json"]).stdout)

    reuse_reports = []
    for relative in (".", "studies/toy", "studies/toy/sourcedata/raw"):
        path = ROOT if relative == "." else ROOT / relative
        result = run(["reuse", "lint"], cwd=path, check=False)
        reuse_reports.append(f"## {relative}\n{result.stdout}{result.stderr}")
        if result.returncode:
            raise SystemExit(f"reuse lint failed for {relative}")
    write("reuse-lint.txt", "\n".join(reuse_reports))

    tests = run(["pytest", "-q"], check=False)
    write("pytest.txt", tests.stdout + tests.stderr)
    if tests.returncode:
        raise SystemExit("pytest failed")

    ideal = run(["python", "scripts/validate_stamped.py", "--ideal"], check=False)
    if ideal.returncode == 0:
        raise SystemExit("ideal validator unexpectedly passed")
    write(
        "stamped-ideal.txt",
        "expected_exit_code=1\n" + ideal.stdout + ideal.stderr,
    )

    pixi = run(["pixi", "--version"]).stdout.strip()
    datalad = run(["datalad", "--version"]).stdout.strip()
    annex = run(["git-annex", "version"]).stdout.splitlines()[0]
    reuse = run(["reuse", "--version"]).stdout.splitlines()[0]
    pytest = run(["pytest", "--version"]).stdout.strip()
    tool_versions = "\n".join(
        (
            pixi,
            datalad,
            annex,
            reuse,
            pytest,
            f"bids-validator-deno {version('bids-validator-deno')}",
        )
    )
    write("tool-versions.txt", tool_versions)
    print(f"Generated {len(tuple(REPORTS.glob('*.*')))} Phase 1 report files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
