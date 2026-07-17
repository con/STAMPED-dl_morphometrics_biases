# Phase 2 implementation notes

Phase 2 adds explicit local environments and an exact-image registry before any
scientific code, BABS campaign, or scientific runtime is introduced. A Pixi
lock is an image-build input and development specification, never the identity
of a result-producing runtime.

## Environment decisions

- Pixi remains pinned to `0.66.0`; `envs/bootstrap-pixi.sh` verifies the
  release binary before installation. The workspace resolves macOS arm64,
  macOS x86-64, and Linux x86-64.
- `dev` combines the locked DataLad and quality tooling with Ruff for tests,
  documentation checks, linting, and optional notebook work.
- `analysis` uses Python 3.11 because the currently selected
  `freesurfer-stats` `1.2.0` requires `pandas<2`, while the available pandas
  1.x packages do not support Python 3.12. It is the current analysis
  environment, not a legacy-extraction environment. This constraint is
  reopened when a qualified `freesurfer-stats` release supports pandas 2 or
  later.
- `babs` locks `PennLINC/babs` at
  `2cc536a51282124f3811ffa971f82a7c34116af5`, the reviewed direct-Study-layout
  minimum. It uses a dedicated Python 3.11 DataLad feature because BABS and
  the current validation environment have incompatible Python requirements.
  It also locks `con-duct` `0.21.0` for lifecycle observability. The
  `babs-operation` launcher records stdout/stderr and sampled process-resource
  data under each campaign's `logs/` directory while leaving BABS and
  DataLad/BABS provenance authoritative. BABS execution is deliberately
  deferred until Phase 3.
- `image-analysis` is a Linux-only image-build dependency set. `image-authoring`
  locks Apptainer `1.5.2`, Cosign `3.0.4`, and Syft `1.48.0`; Lima is a declared
  macOS host interface rather than a Pixi package. The host used for this
  checkpoint reports Lima `2.1.0` and Docker Desktop Engine `29.3.0`; those
  host identities are evidence only and must be re-recorded for release work.

Every ordinary install and task invocation uses `--locked`. Updating
`envs/pixi.lock` is allowed only as an intentional dependency-authoring
change, with the manifest, lock, validation, and rationale reviewed together.

## Image registry decisions

`envs/containers/repronim/` is a pinned source DataLad dataset at
`ReproNim/containers` commit `0284fc8ad8b7fa9a76c3c9f03cfb2919708ba2b2`.
`envs/containers/accepted/` is an independent DataLad dataset: it contains
only registered exact SIFs, its DataLad Containers configuration is the
execution registration, and its `images/` content is annexed with SHA256E.

`envs/images.lock.yaml` is a derived convenience index. Each entry must match
the root image record, exact accepted-dataset commit, annex key, and SHA-256.
If these disagree, the accepted dataset and a result's DataLad run record take
precedence. The registry permits these states: `discovered`, `candidate`,
`qualified`, `accepted-registered`, `superseded`, and `rejected`.
"Authoritative" is reserved for an execution or result that also passes the
full provenance and isolation gates; it is not an image state.

The toy BIDS App is an intentionally non-scientific, redistributable registry
fixture. Its retrieval test proves annex-key and byte verification after
content removal. It must not be used to support a scientific result claim.

Signing, SBOM generation, and build attestation remain explicitly deferred by
the recorded hardening decisions. They are reopened for the first scientific
candidate or custom SIF, not silently treated as passed for the toy fixture.
