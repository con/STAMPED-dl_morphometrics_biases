# Pixi environments and image-build inputs

The real Pixi manifest and lock live in this directory; the root `pixi.toml`,
`pixi.lock`, and `.pixi` symlinks are discovery links only. Pixi environments
are local tooling and image-build inputs. They never identify the runtime that
produced a retained result: that identity is the exact SIF registered in the
accepted container dataset.

## Pixi identity and bootstrap

The workspace requires Pixi `0.66.0`. The checked bootstrap script downloads an exact upstream release asset for macOS arm64 or Linux x86-64, verifies its SHA-256, and installs it in `${PIXI_INSTALL_DIR:-$HOME/.local/bin}`:

```bash
./envs/bootstrap-pixi.sh
```

The Phase 0 initialization used Homebrew Pixi `0.66.0` at `/opt/homebrew/bin/pixi`. Its installed executable had SHA-256 `edfcb61d2367451c6650220c694db8688e06fc0ccdc417d991104400a8ed338b` on 2026-07-16. This records the tool actually used; future installations should use the checked bootstrap script or otherwise verify the same release identity.

## Locked environments

The real manifest and lock live in this directory. Root symlinks support normal Pixi discovery. Realize and inspect the DataLad environment without changing the lock:

```bash
pixi install --locked --environment dev
pixi run --locked --environment dev dev-tool-versions
pixi run --locked --environment dev test
pixi run --locked --environment dev docs-check
pixi install --locked --environment analysis
pixi run --locked --environment analysis analysis-environment-report
pixi install --locked --environment babs
pixi run --locked --environment babs babs-version
pixi run --locked --environment babs babs-operation init toy-campaign -- --dry-run
pixi run --locked --environment dev validate-phase2
pixi run --locked --environment dev verify-toy-image
```

`datalad` retains the minimal bootstrap interface. `quality` retains the Phase
1 validator interface. `dev` supplies tests, documentation checks, linting,
and optional notebooks; `analysis` supplies extraction, assembly, models,
figures, and validation dependencies; `babs` supplies the direct-layout BABS
revision and orchestration tools; `image-analysis` is a Linux image-build
solution; and `image-authoring` supplies Apptainer plus signing, SBOM, and
verification tools on Linux. Run image-authoring installation and image tasks
only on a Linux x86-64 target; macOS performs the development preflight and
uses Lima as the declared host interface. See [Phase 2 notes](../docs/phase-2-notes.md) for
resolved compatibility decisions and host interfaces.

DataLad `1.6.0` and `datalad-container` `1.2.5` are exact dependencies on both
supported development platforms. Linux x86-64 also resolves git-annex
`10.20260601` inside the lock. The BABS feature uses Python 3.11; the existing
development/quality tooling uses Python 3.12. This is a real dependency
boundary, not an accidental duplication.

Conda-forge does not publish a macOS `git-annex` package. On macOS, commands therefore verify and use an explicitly installed host `git-annex`; Phase 0 used Homebrew `git-annex` `10.20260420`. This is a declared host-tool dependency, not part of the Pixi environment. A macOS checkout must install that exact version or record and review an intentional update before DataLad operations. Authoritative scientific runtime isolation remains a separate SIF requirement.

The `quality` environment composes the DataLad feature with exact REUSE, pytest,
JSON Schema, PyYAML, and official BIDS validator dependencies. Its purpose is
repository validation only. It is not a scientific runtime and does not replace
the exact registered SIF required for a result.

Never bind `.venv/` or realized `envs/.pixi/` into an authoritative execution.
The root ignores both paths. Do not use `pixi pack`: resulting prefixes are not
project runtime artifacts. Use `--locked` for all routine work; edit the
manifest and intentionally run `pixi lock` only for a focused dependency change.
