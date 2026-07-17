# Bootstrap DataLad environment

This workspace provides the minimal locked tooling needed to initialize and inspect the research object during Phase 0. Later phases may add the named development, analysis, BABS, testing, and image-authoring environments required by the conversion plan.

## Pixi identity and bootstrap

The workspace requires Pixi `0.66.0`. The checked bootstrap script downloads an exact upstream release asset for macOS arm64 or Linux x86-64, verifies its SHA-256, and installs it in `${PIXI_INSTALL_DIR:-$HOME/.local/bin}`:

```bash
./envs/bootstrap-pixi.sh
```

The Phase 0 initialization used Homebrew Pixi `0.66.0` at `/opt/homebrew/bin/pixi`. Its installed executable had SHA-256 `edfcb61d2367451c6650220c694db8688e06fc0ccdc417d991104400a8ed338b` on 2026-07-16. This records the tool actually used; future installations should use the checked bootstrap script or otherwise verify the same release identity.

## Locked environment

The real manifest and lock live in this directory. Root symlinks support normal Pixi discovery. Realize and inspect the DataLad environment without changing the lock:

```bash
pixi install --locked --environment datalad
pixi run --locked --environment datalad tool-versions
pixi run --locked --environment datalad datalad-status
pixi run --locked --environment datalad validate-phase0
pixi run --locked --environment datalad validate-stamped
```

DataLad `1.6.0` and `datalad-container` `1.2.5` are exact dependencies on both supported platforms. Linux x86-64 also resolves `git-annex` `10.20260601` inside the lock.

Conda-forge does not publish a macOS `git-annex` package. On macOS, commands therefore verify and use an explicitly installed host `git-annex`; Phase 0 used Homebrew `git-annex` `10.20260420`. This is a declared host-tool dependency, not part of the Pixi environment. A macOS checkout must install that exact version or record and review an intentional update before DataLad operations. Authoritative scientific runtime isolation remains a separate SIF requirement.
