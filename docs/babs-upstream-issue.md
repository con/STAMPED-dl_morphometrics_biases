# Draft BABS upstream issue

Filing note, not part of the issue body: the direct-layout checker defect is
already tracked by [PennLINC/babs#325](https://github.com/PennLINC/babs/issues/325),
“`babs check-setup` ignores `path_in_babs` config.” It remains reproducible on
current `main`, but should receive a reproducer or confirmation comment rather
than a duplicate issue. A GitHub issue search on 2026-07-20 found no report for
the separate stale `_enter_unzip` entry point described below.

## Proposed title

`babs-unzip` entry point raises ImportError on current main

## Proposed issue body

### Summary

The installed `babs-unzip` console script fails before argument parsing on
current `main`:

```text
ImportError: cannot import name '_enter_unzip' from 'babs.cli'
```

At commit `2cc536a51282124f3811ffa971f82a7c34116af5`, `pyproject.toml` still
declares:

```toml
babs-unzip = "babs.cli:_enter_unzip"
```

but `babs.cli` no longer defines `_enter_unzip`, and `babs --help` does not list
an `unzip` subcommand. This appears to be a stale package entry point left after
the unzip implementation was removed during the interaction-class refactor.

This matters because the command is installed successfully and therefore looks
like the supported post-merge/finalization interface. Failure is deferred until
the user invokes it.

### Self-contained reproducer

Prerequisites are POSIX `sh`, `git`, `uv`, a Python supported by BABS (3.10 or
newer), and network access. The BABS source is pinned to the exact commit under
test. Every run uses a fresh temporary directory and leaves it available for
inspection, following the
[ephemeral shell reproducer pattern](https://examples.stamped-principles.org/examples/ephemeral-shell-reproducer/).

```sh
#!/bin/sh
# Reproducer for the stale babs-unzip console entry point.

set -eux
PS4='> '

BABS_REV=2cc536a51282124f3811ffa971f82a7c34116af5
WORKDIR=$(mktemp -d "${TMPDIR:-/tmp}/babs-unzip-repro-XXXXXXX")
cd "$WORKDIR"

PYTHON=$(command -v python3)
"$PYTHON" -c 'import sys; assert sys.version_info >= (3, 10), sys.version'

uv venv --python "$PYTHON" .venv
uv pip install --python .venv/bin/python \
  "babs @ git+https://github.com/PennLINC/babs.git@${BABS_REV}"

.venv/bin/python -c \
  'import sys; from importlib.metadata import version; print(sys.version); print("babs", version("babs"))'
.venv/bin/babs --help

if .venv/bin/babs-unzip --help >babs-unzip.stdout 2>babs-unzip.stderr; then
    echo "babs-unzip unexpectedly succeeded" >&2
    exit 1
fi

grep "cannot import name '_enter_unzip'" babs-unzip.stderr
cat babs-unzip.stderr
echo "REPRODUCED babs-unzip entry-point defect"
echo "Workspace retained at: $WORKDIR"
```

The script exits successfully only when the expected import failure is present.

### Actual behavior

The final command reports a traceback of this form:

```text
Traceback (most recent call last):
  File ".../.venv/bin/babs-unzip", line 4, in <module>
    from babs.cli import _enter_unzip
ImportError: cannot import name '_enter_unzip' from 'babs.cli' (.../babs/cli.py)
```

The unified CLI currently advertises these commands:

```text
{init,check-setup,submit,status,merge,sync-code,update-input-data}
```

There is no `unzip` command.

### Expected behavior

The installed console entry points and documented lifecycle should agree. One
of the following would resolve the ambiguity:

1. If unzip/finalization remains supported, restore a tested `babs unzip`
   subcommand and make `babs-unzip` a functioning deprecated alias; or
2. if merged ZIP archives are now intentionally BABS's terminal output, remove
   the stale `babs-unzip` entry point and document the intended post-merge
   workflow and migration from older `babs unzip` usage.

An installation-level smoke test that executes `--help` for every declared
`[project.scripts]` entry point would catch this class of packaging mismatch.

### Source references

- Current `main` / tested revision:
  [`2cc536a`](https://github.com/PennLINC/babs/commit/2cc536a51282124f3811ffa971f82a7c34116af5)
- Stale entry-point declaration:
  [`pyproject.toml`](https://github.com/PennLINC/babs/blob/2cc536a51282124f3811ffa971f82a7c34116af5/pyproject.toml#L63-L70)
- Current command registry without unzip:
  [`babs/cli.py`](https://github.com/PennLINC/babs/blob/2cc536a51282124f3811ffa971f82a7c34116af5/babs/cli.py)
- Refactor that removed `_enter_unzip`:
  [`b0d8179`](https://github.com/PennLINC/babs/commit/b0d81797afc93514606373a62d0f01bffbb7c227)
- Related but already reported direct-layout checker defect:
  [#325](https://github.com/PennLINC/babs/issues/325)

### Environment where independently observed

```text
BABS: 0.5.5.dev26+g2cc536a51
Python: 3.11
DataLad: 1.6.0
Platform: Linux x86_64
```
