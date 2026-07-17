# Licensing and file-group policy

Phase 1 makes license coverage explicit without extending a project permission
grant to external material whose rights remain unresolved.

| File group | Current identifier | Policy |
|---|---|---|
| Project-authored code, apps, scripts, tests, and installers | `MIT` | Permissive project license selected by the repository owner. |
| Project-authored documentation and repository-local policy skills | `MIT` | The repository owner selected one consistent permissive license for the Phase 1 project material. |
| Project-authored configuration, schemas, generated metadata, and manifests | `MIT` | The repository owner selected one consistent permissive license for the Phase 1 project material. |
| OHBM 2025 poster evidence | `LicenseRef-OHBM2025-Poster-Evidence` | Exact-byte redistribution is recorded; broader reuse terms remain unresolved. |
| External BIDS inputs and derivatives | Component-specific license or DUC | Every Study/raw/derivative dataset carries its own declaration; access never implies derivative redistribution. |
| Models, weights, external installers, and container contents | Component-specific terms | Record and check each composition boundary before acceptance; do not embed prohibited license files or secrets. |
| Non-redistributable application license files | Governing vendor terms | Keep outside public Git/annex and provide only by a declared read-only runtime bind. |
| SPDX/custom license texts under `LICENSES/` | REUSE-exempt license files | Include only texts referenced by current file annotations. |

The root `REUSE.toml` gives every covered root file a machine-readable current
status. Git subdatasets are separate REUSE projects: the toy Study and raw child
each retrieve their own `REUSE.toml` and governing license text. Future
container, Study, operations, and result datasets must do the same.

The poster's repository-local notice is
`docs/reference/poster-license-notice.md`; it and the adjacent `.pdf.license`
sidecar make the limited evidence terms discoverable even where an annexed
symlink cannot be parsed directly by REUSE.

MIT applies only to rights controlled by the project contributors. It does not
relicense the historical repository, the poster, external data, model weights,
installers, SIF contents, or produced derivatives. Every such component needs
its own retrievable terms and compatibility decision.

The repository owner reports that the original federal study is a U.S.
Government work and intends to add a scoped public-domain/CC0 notice to that
original work separately. This research object does not make that change or
infer that contractors, collaborators, third-party material, privacy rights, or
rights outside the United States are covered. When the original repository
records the notice, its exact commit and scope become evidence for later import
and compatibility review.
