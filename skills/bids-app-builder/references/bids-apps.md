# BIDS Apps reference

Use these as live references when implementing or reviewing an app. Prefer the official specification over assumptions from an old template.

## Official sources

- BIDS Apps specification: <https://bids-standard.github.io/bids-apps/>
- BIDS Apps FAQ/developer guidance: <https://bids.neuroimaging.io/faq/bids-apps.html>
- Example template: <https://github.com/bids-apps/example>
- Example dataset catalog: <https://bids.neuroimaging.io/datasets/>
- BIDS Derivatives specification: <https://bids-specification.readthedocs.io/en/stable/derivatives.html>

## Baseline API

The common invocation is:

```text
app_name bids_dir output_dir analysis_level [app-specific options]
```

The required positional arguments are `bids_dir`, `output_dir`, and `analysis_level`. The usual analysis levels are `participant` and `group`; an app may support only `participant` when there is no group analysis. `--participant_label` values omit `sub-` and may be a space-separated list. `--skip_bids_validator` is a useful optional flag, not a universal requirement.

## Template cues

The example repository is intentionally minimal. Inspect rather than blindly copy:

- `Dockerfile`: pinned base image, dependencies, copied entrypoint/version, direct `ENTRYPOINT`.
- `run.py`: argparse contract, version reporting, validation, participant/group dispatch, and unknown-argument handling.
- `version`: image/app version input.
- `.circleci/config.yml`: build, example-data retrieval, read-only smoke tests, and tag-driven deployment.
- `README.md`: user-facing usage, citation, reporting, special considerations, and examples.

The template is old relative to current tooling, so confirm CI actions, base images, registry behavior, and specification details before adopting them.

## Container test shape

A representative smoke test mounts the BIDS dataset read-only, mounts an output directory separately, runs `--version`, runs participant mode, and then runs group mode when supported. The exact test dataset and command must match the app's modality and expected outputs.
