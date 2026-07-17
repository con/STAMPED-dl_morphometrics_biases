# STAMPED-dl_morphometrics_biases

Ideal-oriented STAMPED reconstruction of the `dl_morphometrics_biases` analyses summarized in the OHBM 2025 poster.

This repository is now the top-level DataLad research object (dataset ID `baa2ec91-e618-4bac-b382-ac0daf9f779a`). It is not a BIDS dataset or “super-study.” Phase 0 preserves and evaluates evidence without importing historical scientific code:

- [source inventory](docs/source-inventory.tsv) at old-repository main commit `448bf1a311c1ab8310cbab613a8123bb4a4f4a00`, with the later non-main branch recorded separately;
- [annexed poster evidence](docs/reference/recon_all_recon_any_poster_ohbm2025.pdf), with exact SHA-256, annex key, and [OSF DOI](https://doi.org/10.17605/OSF.IO/P3KNS) recorded in the [evidence manifest](docs/evidence-manifest.tsv);
- [stable result targets](docs/result-targets.md) and the 90-row pilot/claim-bearing [result manifest](result-manifest.tsv);
- [runtime candidates](config/runtime-candidates.tsv), with unknown releases, weights, interfaces, and image identities left unresolved;
- [root/component inventory](config/components.tsv), [STAMPED assessment](config/stamped-assessment.tsv), and [hardening decisions](config/hardening-decisions.tsv).

The assessment is deliberately gap-preserving: Phase 0 does not claim that the research object meets the STAMPED ideals or that any scientific result is reproducible yet. Follow [the conversion plan](docs/conversion-plan.md) in order; do not import historical scientific code before the repository, runtime, and toy-campaign guardrails have been proven.

The Phase 0 evidence gate is complete. Phase 1 has established the empty
metadata-only [toy BIDS Study](studies/toy/) and its independent
[raw child](studies/toy/sourcedata/raw/), the campaign/operations contracts,
access-control matrix, file-group licensing policy, and locked validation
environment. No scientific pipeline, container, campaign, derivative, or
claim-bearing result is created in this phase. The public [GIN sibling](https://gin.g-node.org/leej3/STAMPED-dl_morphometrics_biases) provides redundant Git and annex-content storage in addition to the exact OSF web source.

Phase 2 is also complete: the locked Pixi workspace now separates development,
analysis, BABS, Linux image-analysis, and image-authoring environments. The
pinned [ReproNim container source](envs/containers/repronim/) and independent
[accepted container dataset](envs/containers/accepted/) establish the image
registry foundation. Its redistributable toy BIDS App proves exact-SIF
registration, persistent retrieval, and byte verification; it is explicitly
not a scientific runtime. Read [Phase 2 notes](docs/phase-2-notes.md) and the
[accepted image index](envs/images.lock.yaml) before selecting any runtime.

On a new host, clone the complete research object recursively from GitHub,
then configure the public GIN sibling as the annex/content source. Keeping
GitHub as `origin` preserves the repository's publication boundary; GitHub is
Git-only for this dataset, while GIN provides the root annex content.

```bash
datalad clone --recursive \
  https://github.com/con/STAMPED-dl_morphometrics_biases.git \
  STAMPED-dl_morphometrics_biases
cd STAMPED-dl_morphometrics_biases

datalad siblings add --name gin \
  --url https://gin.g-node.org/leej3/STAMPED-dl_morphometrics_biases \
  --as-common-datasrc gin --fetch
git config remote.origin.annex-ignore true
git config remote.gin.annex-ignore false
datalad siblings

datalad get docs/reference/recon_all_recon_any_poster_ohbm2025.pdf
```

The recursive clone installs the tracked Study and container subdatasets but
does not download annex content indiscriminately. Retrieve the exact SIF or
input files needed by the current campaign with `datalad get` after resolving
the campaign's identities. The GIN sibling is a public read source; do not
configure cluster credentials or publish controlled campaign content there.

Read [AGENTS.md](AGENTS.md) before making changes. The complete operating policy is in the repository-local [STAMPED neuroimaging skill](skills/stamped-neuroimaging-analysis/SKILL.md); use the [BIDS App builder skill](skills/bids-app-builder/SKILL.md) whenever a project-authored BIDS App is created or adapted.

The longer decision history and architectural rationale remain in the separate documentation repository. They are intentionally not copied here: the conversion plan and skills are the implementation artifacts for this analysis.

## Locked tooling and validation

The real Pixi manifest and lock are under `envs/`, with root discovery symlinks. The locked bootstrap environment contains DataLad 1.6.0 and DataLad Containers 1.2.5 for macOS arm64 and Linux x86-64. Linux includes git-annex 10.20260601; macOS verifies and uses the explicitly documented Homebrew git-annex 10.20260420 because conda-forge supplies no macOS build.

```bash
pixi install --locked --environment datalad
pixi run --locked --environment datalad tool-versions
pixi run --locked --environment datalad validate-phase0
pixi run --locked --environment datalad validate-stamped
pixi run --locked --environment datalad validate-stamped-ideal
pixi install --locked --environment quality
pixi run --locked --environment quality validate-phase1
pixi install --locked --environment dev
pixi run --locked --environment dev docs-check
pixi run --locked --environment dev test
pixi run --locked --environment dev validate-phase2
pixi run --locked --environment dev verify-toy-image
```

`validate-phase0` checks evidence inventories and complete pilot/claim target coverage. `validate-stamped` checks structural completeness, decisions, evidence, and root/component roll-ups. `validate-stamped-ideal` is expected to fail and enumerate ideal gaps until every applicable MUST is met and every SHOULD is adopted and met.

The locked `quality` environment also supplies the BIDS 1.11.1 validator,
REUSE lint, schema validation, isolated publication-boundary simulation, unit
tests, and Phase 1 report generation. See [Phase 1 notes](docs/phase-1-notes.md)
for the decisions and evidence sequence.
