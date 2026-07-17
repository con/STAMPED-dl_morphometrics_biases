# STAMPED-dl_morphometrics_biases

Ideal-oriented STAMPED reconstruction of the `dl_morphometrics_biases` analyses summarized in the OHBM 2025 poster.

This repository is now the top-level DataLad research object (dataset ID `baa2ec91-e618-4bac-b382-ac0daf9f779a`). It is not a BIDS dataset or “super-study.” Phase 0 preserves and evaluates evidence without importing historical scientific code:

- [source inventory](docs/source-inventory.tsv) at old-repository main commit `448bf1a311c1ab8310cbab613a8123bb4a4f4a00`, with the later non-main branch recorded separately;
- [annexed poster evidence](docs/reference/recon_all_recon_any_poster_ohbm2025.pdf), with exact SHA-256, annex key, and [OSF DOI](https://doi.org/10.17605/OSF.IO/P3KNS) recorded in the [evidence manifest](docs/evidence-manifest.tsv);
- [stable result targets](docs/result-targets.md) and the 90-row pilot/claim-bearing [result manifest](result-manifest.tsv);
- [runtime candidates](config/runtime-candidates.tsv), with unknown releases, weights, interfaces, and image identities left unresolved;
- [root/component inventory](config/components.tsv), [STAMPED assessment](config/stamped-assessment.tsv), and [hardening decisions](config/hardening-decisions.tsv).

The assessment is deliberately gap-preserving: Phase 0 does not claim that the research object meets the STAMPED ideals or that any scientific result is reproducible yet. Follow [the conversion plan](docs/conversion-plan.md) in order; do not import historical scientific code before the repository, runtime, and toy-campaign guardrails have been proven.

The Phase 0 evidence gate is complete. The public [GIN sibling](https://gin.g-node.org/leej3/STAMPED-dl_morphometrics_biases) provides redundant Git and annex-content storage in addition to the exact OSF web source.

Clone directly from GIN and retrieve the poster without credentials:

```bash
datalad clone https://gin.g-node.org/leej3/STAMPED-dl_morphometrics_biases
cd STAMPED-dl_morphometrics_biases
datalad get docs/reference/recon_all_recon_any_poster_ohbm2025.pdf
```

Read [AGENTS.md](AGENTS.md) before making changes. The complete operating policy is in the repository-local [STAMPED neuroimaging skill](skills/stamped-neuroimaging-analysis/SKILL.md); use the [BIDS App builder skill](skills/bids-app-builder/SKILL.md) whenever a project-authored BIDS App is created or adapted.

The longer decision history and architectural rationale remain in the separate documentation repository. They are intentionally not copied here: the conversion plan and skills are the implementation artifacts for this analysis.

## Phase 0 tooling

The real Pixi manifest and lock are under `envs/`, with root discovery symlinks. The locked bootstrap environment contains DataLad 1.6.0 and DataLad Containers 1.2.5 for macOS arm64 and Linux x86-64. Linux includes git-annex 10.20260601; macOS verifies and uses the explicitly documented Homebrew git-annex 10.20260420 because conda-forge supplies no macOS build.

```bash
pixi install --locked --environment datalad
pixi run --locked --environment datalad tool-versions
pixi run --locked --environment datalad validate-phase0
pixi run --locked --environment datalad validate-stamped
pixi run --locked --environment datalad validate-stamped-ideal
```

`validate-phase0` checks evidence inventories and complete pilot/claim target coverage. `validate-stamped` checks structural completeness, decisions, evidence, and root/component roll-ups. `validate-stamped-ideal` is expected to fail and enumerate ideal gaps until every applicable MUST is met and every SHOULD is adopted and met.
