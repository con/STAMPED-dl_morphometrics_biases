# STAMPED-dl_morphometrics_biases

Ideal-oriented STAMPED reconstruction of the `dl_morphometrics_biases` analyses summarized in the OHBM 2025 poster.

## Effort overview

This effort is rebuilding the poster analysis as an inspectable, portable
research object rather than attempting to preserve the original notebooks and
institutional execution environment in place. The root DataLad dataset composes
independently versioned Study, raw-data, derivative, operations, and container
datasets. Git histories are hosted in the
[project GitHub organization](https://github.com/STAMPED-dl-morphometrics-biases);
public annex content is stored separately where declared.

The work proceeds through gated phases: preserve the historical evidence,
establish data and provenance boundaries, prove the execution pattern with
synthetic data, import scientific operations as tested BIDS Apps, qualify exact
runtime images, run an open-data pilot, and only then reconstruct the
claim-bearing ABCD analysis. Synthetic outputs are engineering evidence, not
scientific results.

### Progress

| Phase | Scope | Status |
|---|---|---|
| 0 | Preserve source evidence and declare poster-derived result targets | Complete |
| 1 | Establish the DataLad/BIDS organization, access controls, licensing, and validation guardrails | Complete |
| 2 | Establish locked Pixi environments and the accepted-container registry foundation | Complete |
| 3 | Prove BABS/Slurm execution, merge, finalization, and validation with synthetic data | In progress: the SimBIDS campaign is accepted; independent SIF publication, clean-clone retrieval, and the direct-layout checker debt remain |
| 4–5 | Import scientific operations as tested BIDS Apps and qualify exact scientific SIFs | Not started |
| 6 | Run the open `ds007116` engineering and scientific pilot | Not started |
| 7–8 | Prepare controlled ABCD inputs and reconstruct the poster analyses | Not started |
| 9 | Verify, assess, and release the complete research object | Not started |

See the [conversion plan](docs/conversion-plan.md) for phase gates,
[Phase 3 notes](docs/phase-3-notes.md) for the current engineering
qualification, and the [STAMPED assessment](config/stamped-assessment.tsv) for
principle-by-principle achievements and gaps.

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

## Quick start

Pixi can install DataLad and git-annex into a global, user-level environment;
this does not require a project directory. On Linux, install the versions used
by this repository with:

```bash
pixi global install \
  --environment datalad \
  datalad==1.6.0 \
  git-annex==10.20260601
```

Verify the tools before cloning:

```bash
datalad --version
git-annex version
```

On macOS, install DataLad globally with the same Pixi command but install
git-annex with Homebrew because conda-forge does not provide the required
macOS build:

```bash
pixi global install --environment datalad datalad==1.6.0
brew install git-annex
```

On a new host, clone the root research object from GitHub,
then configure the public GIN sibling as the annex/content source. Keeping
GitHub as `origin` preserves the repository's publication boundary; GitHub is
Git-only for this dataset, while GIN provides the root annex content.

```bash
# Apply this once per user account if recursive installs will include
# GitHub-backed subdatasets. It prevents git-annex from probing GitHub's
# Git-only `origin` remotes, including nested origins.
git config --global remote.origin.annex-ignore true

datalad clone \
  https://github.com/STAMPED-dl-morphometrics-biases/STAMPED-dl_morphometrics_biases.git \
  STAMPED-dl_morphometrics_biases
cd STAMPED-dl_morphometrics_biases

# GitHub stores Git metadata only. Set this before any recursive DataLad
# operation so git-annex does not probe GitHub for annex content.
git config remote.origin.annex-ignore true

GIN_URL=https://gin.g-node.org/leej3/STAMPED-dl_morphometrics_biases

# `configure` is safe when this setup has already been applied. The `add`
# branch is needed only for clones that do not already have a GIN sibling.
if datalad siblings -s gin query >/dev/null 2>&1; then
  datalad siblings configure --name gin --url "$GIN_URL" --fetch
else
  datalad siblings add --name gin --url "$GIN_URL" --fetch
fi
git config remote.gin.annex-ignore false

# Recent published clones already carry the `gin-content` common data source.
# Enable it if it is present; do not try to create it a second time.
if datalad siblings -s gin-content query >/dev/null 2>&1; then
  datalad siblings enable --name gin-content --url "$GIN_URL"
else
  datalad siblings configure --name gin --url "$GIN_URL" \
    --as-common-datasrc gin-content --fetch
fi
datalad siblings

datalad get -n -r .
datalad get docs/reference/recon_all_recon_any_poster_ohbm2025.pdf
```

`datalad clone` obtains only the root dataset. `datalad get -n -r .` then
installs the tracked Study and container subdatasets without downloading annex
content indiscriminately. Retrieve the exact SIF or input files needed by the
current campaign with `datalad get` after resolving the campaign's identities.
The GIN sibling is a public read source; do not configure cluster credentials
or publish controlled campaign content there. The setup above is intentionally
safe to rerun: it configures an existing sibling instead of trying to add it,
and it reuses an existing `gin-content` annex source instead of trying to
initialize a duplicate special remote.

### Temporary BABS RIA storage

BABS may use a local or cluster RIA store as temporary staging while jobs run
and outputs are aggregated. That store is operational infrastructure, not a
required public dependency. After merge and finalization, the accepted output
must be present in the derivative dataset's committed tree (with its
provenance and validation records); a fresh clone must not require access to
the temporary RIA. Historical commits may retain the original RIA path as
operational provenance, even when that path is no longer reachable.

Before accepting or publishing an attempt, verify the final state in a fresh
clone. Confirm that the merged payload is present, save the finalization and
acceptance records, and remove only the temporary RIA siblings from the local
configuration if they are no longer needed:

```bash
datalad siblings
for sibling in output-storage output; do
  if datalad siblings -s "$sibling" query >/dev/null 2>&1; then
    datalad siblings remove --name "$sibling"
  fi
done
datalad save -m "Finalize merged BABS output"
```

The sibling names depend on the BABS configuration. Removing a sibling here
does not delete the RIA store or rewrite history; it only prevents a future
clone of the finalized dataset from treating temporary storage as a required
location. Do not commit absolute home-directory paths or credentials in
`.babs/` or other tracked operational files.

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
