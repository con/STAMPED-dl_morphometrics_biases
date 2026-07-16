---
name: bids-app-builder
description: Build, adapt, test, document, and release containerized BIDS Apps from an existing pipeline or new analysis code. Use when creating a BIDS App, adapting a pipeline to the bids-apps/example template, implementing the standard BIDS Apps CLI, writing container/CI tests, or preparing a tagged BIDS App release.
---

# BIDS App Builder

Build a reproducible command-line container around an analysis pipeline while preserving the BIDS Apps interface. Treat the local repository and the official BIDS Apps specification as the source of truth; use the example template as a structural starting point, not as an unexamined copy.

## Workflow

### 1. Inspect before changing

- Read `AGENTS.md`, the README, build files, entrypoint, dependency manifests, CI configuration, and existing tests.
- Identify the pipeline's actual inputs, outputs, analysis stages, external binaries, expected permissions, and version source.
- Check the current [BIDS Apps specification and FAQ](references/bids-apps.md) when requirements are ambiguous or may have changed.
- Preserve the repository's language, package manager, CI provider, and naming conventions unless the task asks for a migration.

### 2. Define the public contract

Every app must accept these positional arguments in this order:

```text
app_name bids_dir output_dir analysis_level
```

- `bids_dir`: input BIDS dataset; document that it is mounted read-only.
- `output_dir`: writable output directory. For group analysis, explain whether it consumes participant-level results.
- `analysis_level`: use `participant` and `group` when both stages exist; if the pipeline has no group stage, expose only `participant`.
- Add pipeline-specific options after the required arguments. Include `--help` and `--version`.
- Support `--participant_label` when participant-level selection is meaningful. Labels are values such as `01`, without the `sub-` prefix; accept multiple labels when practical.
- Offer `--skip_bids_validator` if validation is integrated. Validation is recommended, not mandatory; make failures clear and allow the documented bypass.
- Reject unknown arguments deterministically and return a conventional nonzero usage error.

Do not silently change the meaning of `participant` or `group`. Explain stage dependencies, parallelism, reruns, and output naming in the README and CLI help.

### 3. Build the app

- Make the container's `ENTRYPOINT` invoke the app directly, so users run `image bids_dir output_dir analysis_level ...`.
- Pin important base images and dependencies where reproducibility matters. Keep the image minimal and remove package-manager caches.
- Add a `/version` file or equivalent version mechanism and ensure `image --version` reports it.
- Make input mounts read-only and write only to the output directory, temporary space, or explicitly documented locations.
- Handle paths with spaces and shell metacharacters safely; prefer argument arrays/subprocess APIs over interpolated shell strings.
- Ensure the app works in a read-only container except for intended writable mounts, because Singularity/Apptainer commonly imposes this constraint.
- If outputs are derivatives, follow the relevant BIDS Derivatives naming and metadata rules rather than inventing an opaque layout.

### 4. Test proportionally

At minimum, test:

1. `image --help` and `image --version`.
2. Invalid/missing required arguments and unknown options.
3. Participant mode on a small valid BIDS example, both all participants and a selected label.
4. Group mode after participant outputs exist, if supported.
5. Read-only input and read-only container behavior, with only the output mount writable.
6. Re-running a participant, selected-subject, or group job according to the documented policy.

Use a lightweight BIDS example dataset for CI when possible. Keep tests deterministic and check meaningful outputs, not only exit status. Run the repository's formatters, linters, unit tests, container build, and smoke tests. If Docker or Apptainer is unavailable, report the unrun checks explicitly.

### 5. Document and release

Update the README with purpose, citation/acknowledgment, documentation and issue links, requirements, complete usage examples, input/output behavior, analysis levels, resource requirements, and special stages.

Before release, verify the image name, version source, license, CI tag behavior, and registry credentials/configuration. Use a Git tag such as `vX.Y.Z`; if the wrapped pipeline version is unchanged but the app/container changed, use the project's documented build-suffix convention. Add release notes describing user-visible changes. Never claim a deployment succeeded without checking the CI/registry result.

## Decision points

- **Existing template repository:** compare its files with the current upstream template and update only what the app needs. Inspect `.circleci/`, `.github/`, `Dockerfile`, `run.py` (or equivalent), `version`, and test-data helpers.
- **Pipeline with no group analysis:** expose only `participant`; do not add a fake group stage.
- **Multiple map/reduce stages:** document and implement explicit stage names only if the pipeline genuinely needs them; preserve the mandatory API and explain ordering.
- **Non-container local development:** keep a direct entrypoint usable for tests, but make container execution the documented distribution path.
- **Missing test data or runtime:** add/locate a small fixture or report the exact external prerequisite; do not weaken tests to make CI green.

## References

Read [references/bids-apps.md](references/bids-apps.md) for official links, the template file map, and the baseline contract.
