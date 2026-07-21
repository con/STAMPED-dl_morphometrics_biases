# Conversion plan for `STAMPED-dl_morphometrics_biases`

## Objective

Create a new DataLad research object, `STAMPED-dl_morphometrics_biases`, that reconstructs the analyses summarized in the OHBM 2025 poster (`recon_all_recon_any_poster_ohbm2025.pdf`), which Phase 0 must register as evidence. Begin with all eligible scans in the open `ds007116` BIDS dataset, then scale the proven pattern to controlled ABCD data.

This is an opinionated implementation intended to achieve the STAMPED ideals where practical. Enforce every STAMPED MUST, make and record an explicit decision for every applicable SHOULD, and support relevant MAY choices without treating them as required. Assess both the complete research object and every component; a component gap rolls up to the research object. Repository organization, data boundaries, environment policy, image identity, provenance capture, access controls, and campaign operations must exist and pass a toy proof before historical scientific code is imported. The old `dl_morphometrics_biases` repository remains read-only evidence; it is not cleaned up in place.

Include the complete repository-local [STAMPED neuroimaging skill](../skills/stamped-neuroimaging-analysis/SKILL.md) and [BIDS App builder skill](../skills/bids-app-builder/SKILL.md) in the first commit. Make `AGENTS.md` require the STAMPED skill for research-object work and the BIDS App builder in addition whenever an authored BIDS App is created or adapted. Treat this plan and the copied skills as current project policy. Record every required SHOULD and hardening choice in `config/stamped-assessment.tsv` or linked implementation evidence; resolve any conflict by updating the affected policy artifact explicitly before implementation changes.

## Fixed decisions

- Make the repository's organizational and provenance decisions at the start. Draw useful patterns from `babs_demo` and MechaBABS without allowing either project to determine the repository layout after scientific code has been imported.
- Pin [BIDS 1.11.1 Study datasets](https://bids-specification.readthedocs.io/en/v1.11.1/common-principles.html#study-dataset). Each study root has `DatasetType: "study"`; its raw BIDS input and every claimed derivative are independently described and validated DataLad datasets composed into that study.
- Maintain `config/stamped-assessment.tsv` for the research-object root and every component. Require evidence for `met`, roll component limitations up to the root, fail structural omissions with `pixi run validate-stamped`, and reserve `pixi run validate-stamped-ideal` for the stricter all-MUST-met gate.
- Reassess and commit the STAMPED state after dependency changes, every pilot and campaign, derivative acceptance, and release preparation.
- Separate authoring from execution according to the skill's [execution-transaction protocol](../skills/stamped-neuroimaging-analysis/references/execution-transactions.md). Commit environment, code, image, pipeline, cluster, campaign, and selected-component state before it is consumed; checkpoint retained child and root state before the next dependent transition.
- Use DataLad/git-annex for data and SIF identity, availability, provenance, and replay.
- Adopt MD5E as the project-wide backend for BABS compatibility. Migrate the current root and project-created datasets from their earlier SHA256E policy in one focused authoring transaction before another retained campaign; preserve historical SHA256E keys in prior records rather than rewriting history.
- Use BABS for BIDS participant/session expansion, Slurm submission, audit/retry, and merge. Target generic Slurm and keep host-specific policy in profiles.
- Treat MechaBABS as a pinned design reference only. Reuse suitable campaign, pinning, state, transition, and inclusion-accounting patterns, but do not install or invoke MechaBABS unless the copied STAMPED skill and this plan are explicitly revised to adopt it.
- Use Pixi for named development, analysis, BABS/tooling, test, and image-authoring environments; exact bootstrap and user-space tools; locked Linux dependency installation during custom SIF construction; typed project tasks; validation; and static reproduction meta-graphs. Pixi is not the image builder, provenance authority, result-runtime identity, distribution artifact, or dynamic/durable workflow-state engine.
- Require plain `pixi` discovery in login, noninteractive, Slurm, and agent shells before project work. Diagnose shell initialization instead of using absolute Pixi paths or private environment `bin` paths.
- Store the real Pixi manifest and lock under `envs/`, with tracked root symlinks for discovery. Do not use `pixi pack` or another packed-prefix artifact.
- Use one `analysis` environment with `pandas<2` while the selected `freesurfer-stats` release requires it. This is the analysis environment, not a legacy extraction environment. When a qualified release supports `pandas>=2`, review the dependency update, produce a new lock and analysis SIF, and rerun affected results.
- Let Pixi tasks provide local and actionable interfaces. A task may wrap a BABS lifecycle operation, an image operation, or a complete `datalad containers-run` command. A typed Pixi meta-task or dependency graph may provide the one-command reproduction entry point only when every result-changing leaf invokes BABS or an explicit DataLad Containers operation and produces its own intelligible provenance. Never record only `pixi run <task>` inside DataLad, never let a scientific task bypass DataLad, and never enable Pixi input/output caching for result-changing tasks.
- Build project-authored BIDS Apps with the copied `bids-app-builder` skill from the reviewed [`bids-apps/example@2ef3f19`](https://github.com/bids-apps/example/tree/2ef3f19268135273aa49bd2a61c72eaac56f5cef). Their SIF runscripts invoke tracked app entrypoints accepting the standard BIDS App arguments; Pixi tasks may launch them but do not define their interfaces. DataLad records must expose the app arguments and any project-specific operation.
- Use exact registered SIFs for every retained, merged, compared, or released result. Candidate images may run in quarantined debugging campaigns, but their outputs are disposable and must be regenerated after image registration.
- Use one accepted-container DataLad dataset, with Git history published through GitHub and annex content through a GIN storage sibling. Allow an ignored root `.env` only for the narrow publication task; never pass its credentials into BABS, Slurm, containers, logs, or provenance.
- Prefer an exact SIF already distributed through ReproNim/containers when its tool version, BIDS App interface, architecture, licensing, and behavior qualify. Pin the ReproNim DataLad commit and image annex key, compute a project SHA-256, and validate the image; a name or upstream OCI tag is not sufficient identity.
- Build a SIF directly from a tracked Apptainer/Singularity definition when no existing image qualifies.
- Pin and qualify a BABS revision with direct Study-layout support using `analysis_path: "."`; the reviewed minimum is [`2cc536a`](https://github.com/PennLINC/babs/commit/2cc536a51282124f3811ffa971f82a7c34116af5). Make each BABS project, DataLad analysis dataset, and provisional derivative the same root from initialization through acceptance. Accept and document the remaining wrapper and zip/merge indirection, test representative replay, and do not reproduce that indirection in authored operations.
- Run every scientific execution with clean environment and containment controls: no host-home mount, no inherited undeclared working directory, no persistent container or application cache, explicit read-only input/configuration binds, and only fresh output/scratch paths writable. Record unavoidable host mounts and interfaces.
- Treat `ds007116` as an engineering and scientific pilot. ABCD is the later claim-bearing analysis.
- Ignore the old `balanced_scans.csv` until ABCD access exists, then replace it with a tracked cohort BIDS App operation using the permitted release and query.
- Do not retrieve old NIH cluster derivatives until their DUC status is resolved. They are not required to begin.

## Migration strategy

Use gated phases. A phase is complete only when its evidence is committed to the new DataLad research object. Do not import historical scientific code until the empty repository, environments, image registry, and toy BABS campaign have proved the intended organization and guardrails.

Before Phase 0 evidence was saved, the existing non-empty Git repository was initialized in place as the top-level DataLad research object. A minimal checksummed, locked Pixi environment was created first and used for the initialization. This preserves the original Git history and remote; it does not require a repository wipe or force push. The broader named environments and image registry remain Phase 2 work.

## Phase 0 — preserve evidence and declare targets

### Work

1. Create a read-only inventory of the old repository at its current commit.
2. Record the source commit for every module or script that may later be imported, even though it is not the historical result-generating commit.
3. Copy the poster into a documentation/reference dataset or register a persistent reference if redistribution is not permitted.
4. Import the reviewed poster-derived targets into `docs/result-targets.md` and assign stable result IDs.
5. Record runtime knowledge:
   - FreeSurfer `recon-all` 7.4.1 is an intended comparison;
   - FreeSurfer `recon-all` 8.2.0 is the second intended comparison; the [ReproNim NeuroDesk 8.2.0 image](https://github.com/ReproNim/containers/blob/0284fc8ad8b7fa9a76c3c9f03cfb2919708ba2b2/.datalad/config#L303-L305) is an installation/runtime candidate that still needs the required BIDS App interface and project qualification;
   - exact `recon-any` and `recon-all-clinical` distributions, builds, and weights remain qualification gates.
6. Record the intended native and 1×1×5 mm input conditions without copying notebook-generated command files.
7. Create the initial root `result-manifest.tsv`, with one row per authoritative figure, table, statistic, or derivative and exact links to its dataset commit, run record, registered SIF, inputs, and Pixi reproduction entry point. Distinguish pilot-only from claim-bearing outputs.
8. Create the initial root and component inventory for `config/stamped-assessment.tsv`. Record every MUST and SHOULD decision even when its initial status is `unmet`, `restricted`, or `not-applicable` with a scope reason.

### Evidence

- `docs/source-inventory.tsv`;
- `docs/result-targets.md`;
- initial STAMPED assessment, result manifest, and runtime-candidate manifest;
- recorded SHOULD and hardening decisions, with their rationale and linked implementation evidence.

### Exit gate

Every intended poster panel has an ID, expected inputs and outputs, a reproduction entry-point placeholder, and a declared evidence class. Every uncertain runtime is explicitly unresolved rather than assigned a guessed version. Every inventoried root/component MUST and SHOULD has an explicit initial decision and status.

## Phase 1 — establish the repository and BIDS Study guardrails

### Work

1. Verify and extend the initialized top-level DataLad superdataset. It began with a text-friendly SHA256E configuration; preserve that historical fact and complete the fixed-decision MD5E migration as its own authoring transaction. It is the research-object root, not a BIDS dataset or “super-study,” and its commits compose exact component/subdataset commits.
2. Verify and commit both complete repository-local skill bundles and the `AGENTS.md` pointer requiring them in the appropriate work.
3. Establish the complete directory pattern from the copied [STAMPED skill](../skills/stamped-neuroimaging-analysis/SKILL.md), including repository-local `skills/`, canonical `src/` and `apps/`, `envs/containers/{repronim,custom,accepted}/`, `config/`, `operations/`, `studies/`, multi-study `results/`, tests, documentation, licenses, root `result-manifest.tsv`, and access-control metadata.
4. Record BIDS 1.11.1 as the pinned specification. Create an empty toy Study dataset immediately so the organization is executable rather than aspirational.
5. Give every outer `studies/<study>/` dataset a `dataset_description.json` with `DatasetType: "study"` and a README. Install `sourcedata/raw/` as an independent raw BIDS/DataLad dataset. Do not create placeholder derivative datasets before their producing operation exists.
6. Create every BABS attempt directly at `studies/<study>/derivatives/<pipeline>-<variant>-attempt-<N>/`. Treat it as provisional while running and as accepted only after provenance-captured finalization, complete derivative metadata, independent validation, and an acceptance record. Require `GeneratedBy` and exact placement-independent `SourceDatasets`; keep `.babs/`, generated code, logs, and container material distinct from the declared scientific payload.
7. Add Git attributes so SIFs and large outputs are annexed rather than committed to Git.
8. Define the public/private sibling matrix before any ABCD content exists. Include a protected-data simulation that proves a public push cannot reach protected inputs, identifiers, logs, or derivatives.
9. Add `REUSE.toml`, required SPDX license texts, and file-group policy for code, documentation, configuration, generated metadata, externally governed data, models, installers, and license files.
10. Add `config/stamped-assessment.tsv` with stable root/component IDs, parent relationships, normative requirement IDs, levels, decisions, statuses, evidence, and limitations. Include DataLad IDs, URLs, versions/commits, licenses or DUCs, BIDS descriptions, and distribution status in the component inventory or linked evidence.
11. Define the campaign record and append-only operations-ledger schemas now. Require every `operations/<campaign>/` to be an independent DataLad dataset with its own identity and commit history. A campaign must identify exact dataset, pipeline/SIF, input condition, cluster profile, resources, outputs, retry policy, and access class before initialization. It points to the BABS attempt under the Study and never contains or replaces that derivative.
12. Review `babs_demo` and MechaBABS only against these established invariants. Adopt useful patterns; reject any pattern that would blur Study/raw/derivative boundaries, hide commands, or make the repository depend on unqualified tooling.

### Evidence

- a clean recursive clone of the empty skeleton;
- saved `datalad subdatasets` and `git annex info` reports;
- BIDS validation or reviewed expected exceptions for the toy Study root and raw child, plus every provisional or accepted derivative once it exists;
- `reuse lint` passing for project-owned files;
- a credential-free publication dry run that cannot reach protected siblings;
- schema tests for campaign records, image records, result manifests, and operations events;
- `validate-stamped` passing the current complete assessment and a negative fixture proving it fails on omissions, while `validate-stamped-ideal` accurately reports the initial unmet ideal gates.

### Exit gate

A collaborator can understand and validate the research object's root/component STAMPED posture, Study/raw/provisional-derivative composition, operations model, licensing, and access boundaries before any historical analysis code is present.

## Phase 2 — establish Pixi and image-source foundations

### Pixi workspace

1. Keep `pyproject.toml` focused on package metadata and importable code where packaging is useful. Keep BIDS App entrypoints under `apps/` and project launchers in Pixi tasks rather than treating either as package metadata.
2. Extend the bootstrap `envs/pixi.toml`, `envs/pixi.lock`, and tracked root discovery symlinks with the complete named environment set.
3. Declare `linux-64` for runtime-dependency environments and the relevant macOS platforms for development.
4. Define at least:
   - `dev` for tests, documentation, linting, and optional notebooks;
   - `analysis` for extraction, assembly, models, figures, and validation, initially including the required `pandas<2` constraint;
   - `babs` for pinned BABS, DataLad, datalad-container, git-annex, and orchestration tools;
   - named Linux image environments where dependency graphs genuinely differ;
   - an image-authoring environment for Apptainer/Lima, signing, SBOM, and verification tools when useful.
5. Pin the supported Pixi release and provide a bootstrap procedure. Record exact Pixi, DataLad, BABS, Apptainer/Singularity, and Lima versions/configuration used for release work.
6. Ignore `.venv/` and realized `envs/.pixi/`; never bind them into authoritative runs.
7. Add typed, described Pixi tasks for validation, tests, documentation, `reuse lint`, environment reports, explicit image operations, parameterized BABS operations, and complete DataLad-container invocations. Add `validate-stamped`, `validate-stamped-ideal`, and a `reproduce-<result-set>` meta-task or dependency graph. Every result-changing leaf must produce a DataLad/BABS record; the graph is an executable specification, not execution evidence, and result-changing tasks must not use Pixi input/output caching.
8. Run routine work and image installation with `--locked`. Only dependency-authoring changes may update the lock.

### Image-source registry

1. Create the single accepted DataLad container dataset at `envs/containers/accepted/`, publish its Git history through GitHub and annex content through GIN, and maintain the derived convenience index `envs/images.lock.yaml` before selecting production images. Every index entry must resolve to the accepted dataset commit and exact SIF annex identity; the accepted dataset, run record, and result manifest prevail on conflict. Install the pinned ReproNim/containers source dataset at `envs/containers/repronim/`; reserve `envs/containers/custom/` for project definitions.
2. Define image states: discovered, candidate, qualified, accepted/registered, superseded, and rejected. Reserve “authoritative” for executions and results that satisfy the complete provenance and isolation gates.
3. For external images, record the source DataLad dataset ID and commit, annex key, original source reference, local SHA-256, architecture, licenses, expected BIDS App interface, and retrieval locations.
4. For project-built images, reserve tracked definition paths and record the manifest/lock, base, non-Pixi inputs, builder versions, architecture, build command, SIF hash, annex key, and tests. Record an explicit hardening decision for an SBOM, signature, and build attestation; attach them when adopted and supported.
5. Add retrieval and verification tests using a small redistributable toy SIF. Do not wait for the scientific runtimes to test the registry.

### Dependency update cycle

1. Make a focused dependency/image change.
2. Edit `envs/pixi.toml`, run `pixi lock` intentionally, and inspect the manifest and lock diff.
3. Test relevant macOS environments with `--locked` and realize the reviewed Linux solution on the target architecture.
4. If the change affects a runtime, create a new SIF identity; never mutate an accepted SIF in place.
5. Commit the manifest, lock, tests, image-ledger change, and rationale together. There is no freshness requirement for an otherwise working lock.

### Exit gate

A clean macOS checkout can realize development environments, Linux can realize selected image environments without rewriting the lock, and an exact toy SIF can be registered, removed, retrieved, and verified from persistent storage.

## Phase 3 — prove the organization with a toy BABS campaign

### Work

1. Install a small redistributable raw BIDS/DataLad dataset at `studies/toy/sourcedata/raw/`.
2. Register a small exact SIF with a BIDS App interface in the container dataset. Record its commit, annex key, SHA-256, and retrieval location.
3. From a committed root composition, pin and qualify BABS at the direct-layout revision. Initialize the BABS project directly at `studies/toy/derivatives/<pipeline>-<variant>-attempt-001/` with `analysis_path: "."`, hidden `.babs/input_ria` and `.babs/output_ria` paths, and the raw child installed at `sourcedata/raw/` within the BABS project.
4. Make that one root the BABS project, DataLad analysis dataset, and provisional BIDS derivative. Register and checkpoint it in the parent Study and root before setup checks, pilot submission, or other dependent execution; prove that a clean recursive clone preserves the dataset and required RIA retrieval paths.
5. Create `operations/toy-<campaign>/` as a separate DataLad dataset. Add a schema-valid resolved `campaign.yaml`, desired/observed state, requested/realized inclusion, attempt identity, reviewed BABS configuration, literal command renderings, and append-only `commands.jsonl`.
6. Use a Pixi task to make each BABS lifecycle operation actionable, but record actual expanded initialization, setup check, pilot, submission, status/retry, merge, finalization, validation, and acceptance argv plus tool versions and before/after state in the operations ledger.
7. Run from a clean clone with no host-home mount, no persistent cache, fresh work/output/scratch, explicit read-only inputs/configuration, declared binds, and no network unless declared. Inspect the realized BABS participant script and mount table during the pilot.
8. Keep BABS-generated wrappers, archives, logs, RIA state, and `code/` as operational evidence within the attempt boundary, distinct from the scientific payload. Preserve the known wrapper and zip/merge indirection and test representative historical replay.
9. Perform archive extraction or other finalization through an explicit provenance-captured operation in that same attempt dataset. Do not copy or symlink the payload into a second derivative and do not change the attempt's DataLad identity during promotion.
10. Complete the same dataset's README and `dataset_description.json`, including `DatasetType: "derivative"`, `GeneratedBy`, and exact placement-independent `SourceDatasets`. Validate the attempt and containing Study independently. Treat BABS's visible top-level `containers/` path as a hard validation gate requiring an upstream fix or reviewed exception rather than an undocumented ignore.
11. Record acceptance of the exact attempt dataset ID and commit in the operations dataset. Test SIF retrieval, failed-job retry as a new attempt, merge audit, operations-ledger recovery, assessment roll-up, and a clean recursive clone.
12. Compare the implementation with useful `babs_demo` and MechaBABS patterns. Adopt the direct-layout, campaign-axis, pinning, attempt, state-ledger, transition, and inclusion-accounting patterns that preserve these boundaries; do not make authoritative execution depend on MechaBABS without an explicit later adoption decision.

### Exit gate

The toy campaign proves, before scientific code import, that one direct-layout BABS dataset can remain identifiable from initialization through provenance-captured finalization and accepted derivative status; exact images are retrievable; lifecycle commands are recorded; disposable execution excludes home/cache state; protected and public state remain separated; and merged/extracted outputs carry intelligible DataLad provenance.

## Phase 4 — import and refactor scientific code as tested BIDS Apps

### Application and operation design

Import one scientific boundary at a time with the copied `bids-app-builder` skill. Each import records its old-repository source commit, removes notebook and host assumptions, receives tests, and passes a toy containerized invocation before the next operation is imported.

Implement closed, documented project operations such as:

| Operation | Allowed analysis level | Accepted inputs | Declared outputs |
|---|---|---|---|
| `cohort` | `group` | raw BIDS metadata and tracked selection configuration | ordered cohort and exclusion tables |
| `resample` | `participant` | declared BIDS structural images | BIDS derivative images plus transformation metadata |
| `extract` | `participant` | a qualified reconstruction derivative | stable morphometric tables and completeness records |
| `assemble` | `group` | declared extraction derivatives | keyed cross-pipeline analysis tables |
| `model` | `group` | declared analysis tables and model configuration | model estimates, diagnostics, and statistical tables |
| `figures` | `group` | declared model/statistical outputs and result IDs | only the requested figures and table renderings |
| `validate` | `participant` or `group` | a declared dataset, derivative, or result set | machine-readable validation report |

Before importing each operation, decide whether it is its own BIDS App or a coherent mode of another app. Default to a separate app for an independently versioned scientific transformation; combine operations only when they share one meaningful input/output contract and lifecycle. Each app follows [`bids-apps/example@2ef3f19`](https://github.com/bids-apps/example/tree/2ef3f19268135273aa49bd2a61c72eaac56f5cef): its container entrypoint accepts `bids_dir`, `output_dir`, and an implemented `analysis_level`, provides participant selection where meaningful, documents validation behavior, exposes help/version information, and rejects unknown arguments. Any additional operation selector must be closed and explicit. Reconstruction and downstream apps follow the same image, testing, DataLad, and metadata rules.

The SIF runscript invokes the tracked `apps/<app-name>/run.py` entrypoint. Pixi tasks may expose local invocations, wrap a complete `datalad containers-run` command, or compose provenance-producing leaf tasks into a reproduction graph, but they do not define the BIDS App interface or prove execution. Do not let one operation silently invoke a hidden operation DAG. Record each result-changing operation as its own explicit DataLad operation.

### Refactoring requirements

- Replace hard-coded `/data/ABCD_*`, NIH paths, and user cache paths with declared inputs and tracked configuration.
- Remove inline `uv` metadata and installation instructions.
- Keep the current `freesurfer-stats` compatibility constraint in the `analysis` environment. Do not label the work `extract-legacy`; qualify a newer dependency and image when available.
- Replace path-only pickle caches. Disposable caches must include content identities and remain outside provenance; scientific tables are declared outputs.
- Prevent authoritative executions from reading host home, persistent application caches, inherited working directories, or undeclared binds. Stage reference resources such as TemplateFlow as exact declared inputs rather than downloading them during execution.
- Replace implicit output directories and path-parent inference with explicit operation arguments and derivative metadata.
- Remove shell-driven `ls`, interactive `freeview`, scheduler submission, and unique notebook logic from authoritative paths.
- Emit structured exclusions and completeness tables. Make atlases, metrics, hemispheres, transformations, statistical models, seeds, and figure IDs reviewed configuration.
- Pin TemplateFlow and other reference resources by content and record their licenses.
- Use tiny synthetic or redistributable FreeSurfer-like fixtures for unit and integration tests.

Notebooks may remain only when they consume tracked outputs, contain no unique scientific logic, do not submit or write authoritative results, and can be deleted without preventing reconstruction.

### Iteration gate for each operation

1. Import the minimum reviewed code and record its source commit.
2. Add schema and unit tests.
3. Run the operation locally through the locked Pixi environment for development.
4. Add it to the selected `apps/<app-name>/run.py` entrypoint, expose that entrypoint through the BIDS App SIF runscript, and build a candidate SIF.
5. Run a toy `datalad containers-run` invocation with explicit inputs, outputs, operation, and arguments.
6. Review the resulting BIDS derivative metadata and DataLad record.
7. Only then import the next operation.
8. Add or update root `result-manifest.tsv` and the component/root STAMPED assessment rows with actual run and validation evidence.

### Phase exit gate

The fixture path from a reconstruction-like derivative through extraction, assembly, modeling, one declared figure, and validation works through explicit BIDS App executions. No result depends on notebook order, shell history, an institutional path, or interpretation of an old Pixi task definition.

## Phase 5 — qualify, reuse, or build scientific images

### Candidate hierarchy

1. Prefer an exact ReproNim SIF when it implements the required BIDS App behavior.
2. Otherwise qualify another exact redistributable SIF and register it in the project container dataset.
3. Otherwise build a project SIF from a tracked definition and locked Pixi environment.
4. Never substitute a similarly named version or reconstruct authoritative results from a mutable tag when exact SIF bytes are available.

### FreeSurfer candidates

- FreeSurfer 7.4.1: begin with ReproNim/containers' registered [`bids-freesurfer--7.4.1-unstable.sif`](https://github.com/ReproNim/containers/blob/0284fc8ad8b7fa9a76c3c9f03cfb2919708ba2b2/images/bids/Singularity.bids-freesurfer--7.4.1-unstable). The `unstable` source tag is not the runtime identity. Pin the ReproNim DataLad commit and annex key, compute SHA-256, inspect licensing, and validate the exact SIF on a fixture and full pilot subject before promotion.
- FreeSurfer 8.2.0: evaluate ReproNim's registered NeuroDesk image as an installation/runtime candidate. It exposes FreeSurfer tools rather than the required BIDS App interface, so either qualify a tracked wrapper or build a project BIDS App.
- For a project FreeSurfer 8.2.0 BIDS App, reuse audited ideas from [BIDS-Apps/freesurfer](https://github.com/BIDS-Apps/freesurfer) and the [NeuroDesk FreeSurfer recipe](https://github.com/NeuroDesk/neurocontainers/blob/aa4b9af982ce409c91258281b551a06bf7028fb4/recipes/freesurfer/build.yaml). Update the wrapper for FreeSurfer 8.2.0 semantics, use the project's Pixi lock, checksum every fetched input, and add a real BIDS participant integration test. Do not merely change the old generator's version string.

Qualify exact `recon-any` and `recon-all-clinical` releases, weights, licenses, architecture, and BIDS App interfaces separately. Build the downstream analysis SIF from the apps and operations proven in Phase 4.

### Qualification gate

For every candidate:

- retrieve and verify the exact SIF from a clean clone;
- record tool, wrapper, and embedded dependency versions;
- inspect the runscript, environment sanitation, binds, architecture, and license behavior;
- prove that execution prevents host-home and persistent-cache use, starts from fresh work/scratch/output state, and exposes only declared binds and required host interfaces;
- run interface, version, fixture, invalid-operation, and expected-output tests;
- run one complete representative subject when the application is participant-level;
- validate derivative metadata and stable output naming;
- confirm that BABS-generated execution identifies the registered SIF path;
- compute SHA-256, record the annex key/DataLad commit, generate an SBOM where feasible, and apply the project's signature/verification policy;
- reject or wrap the image explicitly if its interface does not meet the app contract.

### Project SIF construction

1. Store definitions under `envs/containers/custom/<image>/`.
2. Pin/checksum the base and every non-Pixi input.
3. Install the selected Linux environment from `envs/pixi.toml` and `envs/pixi.lock` with a pinned Pixi and `--locked` at its final in-image path.
4. Build directly for the target Slurm architecture. On macOS, use Apptainer inside Lima; use an x86-64 guest on Apple Silicon for x86-64 Slurm targets.
5. Record the builder, architecture, definition and lock hashes, command, tests, and all inputs.
6. Smoke-test the final SIF and compute its exact content checksum. Apply the recorded signing, SBOM, and attestation hardening decisions.
7. Register it with `datalad containers-add` in `envs/containers/accepted/`, publish annex content to persistent storage, and update `envs/images.lock.yaml`.

Candidate SIFs may be used to debug in quarantined local or Slurm space. Retained outputs must be regenerated through the promoted registered SIF according to the copied STAMPED skill.

### Licensing

- Record redistribution terms for software, installers, weights, and required license files.
- Distribute license files with the repository or SIF when permitted and when they contain no secret or inappropriate personal information.
- When redistribution is prohibited, document acquisition and verification and bind the supplied file read-only.
- If the exact image cannot lawfully be hosted, publish only permitted definitions/components and a tracked retrieval/build adapter; do not imply public availability.

### Exit gate

Every image admitted to a scientific campaign has a qualified interface, exact SIF identity, persistent retrieval test, license decision, target-architecture test, and registered DataLad identity. Unresolved image families remain blocked without delaying already qualified pilots.

## Phase 6 — run the `ds007116` pilot

### Work

1. Install a pinned `ds007116` snapshot at `studies/ds007116/sourcedata/raw/` and validate it.
2. Generate an all-eligible cohort manifest with the tested `cohort` operation; do not reuse the old ABCD balance file.
3. Start a direct-layout attempt at `studies/ds007116/derivatives/<pipeline>-<variant>-attempt-001/` with the qualified FreeSurfer 7.4.1 ReproNim BIDS App on one participant/session.
4. Inspect the complete BABS operation record, exact SIF, expanded command, binds and mount table, home/cache/network isolation, outputs, logs, RIA state, merge, and zip behavior.
5. Finalize zipped BABS output through an explicit provenance-captured operation in the same attempt dataset. Complete metadata, validate the derivative and Study independently, and record acceptance of that exact dataset ID and commit without copying or replacement.
6. Run `extract`, `assemble`, `model`, `figures`, and `validate` as separate explicit DataLad-container operations for the one-case or smallest meaningful fixture. Put their single-Study derivatives under `studies/ds007116/derivatives/`.
7. Test representative historical replay, clean recursive retrieval, and the one-command Pixi reproduction graph while confirming that each leaf record exposes the actual command. Document the remaining BABS wrapper/zip indirection.
8. Scale FreeSurfer 7.4.1 only after the one-case gate passes.
9. Repeat the one-case and scale gates for FreeSurfer 8.2.0 and for qualified `recon-any` and `recon-all-clinical` images.
10. Add native/resampled variants only when the required input exists and the `resample` operation has passed unit and integration tests. Freeze each accepted derivative and operations dataset commit before downstream comparisons, then update the root result manifest and STAMPED assessments.

### Expected result

The pilot should generate the same kinds of tables and figures as the poster but is not expected to reproduce ABCD effect sizes. It validates the research object, app interfaces, completeness policy, storage needs, and Slurm resource estimates.

### Exit gate

- all eligible scans are accounted for;
- failures and retries have structured reasons;
- every derivative resolves to input, code/config, operations, and exact SIF identities;
- downstream operations replay through DataLad with explicit leaf commands; a Pixi reproduction meta-task may orchestrate them but cannot replace their provenance;
- the Study/raw/derivative composition survives a clean recursive clone;
- clean executions use no host home or persistent cache and expose only reviewed binds and host interfaces;
- every authoritative pilot output resolves through root `result-manifest.tsv`;
- a second Slurm site can adapt only the host profile, or remaining coupling is documented.

## Phase 7 — prepare controlled ABCD data

Do not begin until access and derivative handling have been reviewed against the current ABCD DUC.

### Work

1. Record the allowed release, access endpoint, DUC version, project approval, and permitted outputs.
2. Create a private DataLad input dataset or tracked executable retrieval adapter. Record exact controlled identities and stable authorized-access locations without credentials in Git, and stage authenticated retrieval before scientific execution.
3. Use the tested `cohort` operation to regenerate the intended selection from release metadata.
4. Permit an all-eligible systems-test cohort only if policy and compute allow; create the poster-like unrelated/four-wave selection as a separate versioned cohort.
5. Test relationship exclusion, wave balancing, modality pairing, duplicates, age derivation, missingness, and stable ordering.
6. Store protected cohort manifests, logs, derivatives, extracted morphometrics, and QC only on declared private siblings.
7. Establish a separate disclosure-reviewed aggregate-output sibling.
8. Run a credential-free public push test before submitting jobs.
9. Decide input and derivative redistribution separately. Mark D.1 `restricted` for every component that arbitrary third parties cannot retrieve, roll it up to the root assessment, and state who can retrieve it and how. Do not treat the restriction as a pass, but do not let it block permitted analysis or release of distributable modules.
10. Keep participant identifiers and prohibited metadata out of root `result-manifest.tsv`. Stop for a policy decision whenever an input, log, derivative, participant record, or metadata field may violate an agreement.

### Exit gate

The approved release and cohort can be regenerated, protected content cannot leak through any public sibling, and every input/output class has a documented distribution decision.

## Phase 8 — run ABCD campaigns and reconstruct the poster

Use only campaign and image patterns that passed the toy and `ds007116` gates. The intended comparison families are:

1. qualified FreeSurfer 7.4.1 reference on declared T1w/T2w inputs;
2. qualified FreeSurfer 8.2.0;
3. qualified `recon-all-clinical` on native T1w;
4. qualified `recon-all-clinical` on 1×1×5 mm T1w;
5. qualified `recon-any` on native T1w;
6. qualified `recon-any` on 1×1×5 mm T1w.

For each campaign:

- run one participant/session and inspect;
- submit in bounded batches;
- record lifecycle commands, status, retries, exclusions, and commits;
- merge only audited successes;
- preserve merged BABS zips and generated material as protected operational/scientific evidence in the direct attempt dataset, not in the operations dataset;
- finalize each payload through an explicit provenance-captured operation in that same attempt dataset, then complete metadata, validate, and accept its exact commit without copying or replacement;
- emit completeness and exclusion tables;
- freeze both the accepted derivative and operations commits before cross-pipeline analysis.

Then run the closed downstream operations separately for extraction, cross-pipeline assembly, cohort/age joins, global and regional models, milestone joins, figure/table generation, continuous result-manifest updates, numeric validation, and disclosure review. Use the Pixi reproduction graph only to compose these provenance-producing leaves.

### Exit gate

Every poster target has a result-manifest row and regenerates from exact permitted data, derivative commits, code/configuration, recorded operations, and registered SIFs. Deviations from poster reference observations receive written analysis rather than silent parameter changes.

## Phase 9 — verify and release

### Verification matrix

- Fresh recursive public DataLad clone.
- Fresh private clone with authorized ABCD credentials.
- SIF retrieval and verification from every promised location.
- One clean Slurm participant replay per image family.
- Empty host home/cache and no-prior-output replay with explicit bind and network inspection.
- One downstream DataLad replay per scientific operation boundary.
- Verification that every accepted BABS attempt retains one dataset identity and that parent registration plus clean cloning preserve required input/output RIA paths.
- Independent BIDS validation, or reviewed exceptions, for every Study root, raw input, and claimed derivative.
- Schema and checksum validation for every authoritative table and figure.
- Cross-host pilot on a second Slurm system when available.
- macOS/Lima build and smoke-test path where used, followed by acceptance on representative Slurm.
- Public-release scan for subject identifiers, credentials, absolute paths, controlled/private annex URLs, and prohibited derivatives.
- REUSE compliance and license/DUC review.
- `validate-stamped` passing structurally and `validate-stamped-ideal` reporting every remaining restricted/unmet MUST and non-adopted SHOULD without concealment.

### Release objects

- tagged and signed top-level DataLad dataset state;
- pinned subdataset commits;
- public code/documentation archive with persistent identifier;
- permitted private ABCD dataset state identifier;
- exact SIFs in DataLad/annex storage with checksums and the verification, signing, attestation, and SBOM material adopted by the recorded hardening decisions;
- root result manifest and validation report;
- current seven-principle assessment for the root and every component;
- known limitations, including BABS wrapper/zip indirection and unavailable or non-redistributable runtimes.

## Risks and controls

| Risk | Control |
|---|---|
| The generic FreeSurfer 8.2.0 tool image is mistaken for the required BIDS App | Build or qualify the tracked BIDS App entrypoint and test the exact registered SIF |
| A ReproNim image name is mistaken for sufficient identity | Pin DataLad commit and annex key, compute SHA-256, retrieve, inspect, and validate exact bytes |
| `recon-any` or clinical version remains ambiguous | Block that image family while proceeding with qualified FreeSurfer pilots |
| MechaBABS maturity changes during conversion | Reuse credited design patterns only; do not install or invoke it until the skill and plan explicitly adopt it |
| Pixi rewrites a lock during ordinary work | Require `--locked`; permit lock changes only during reviewed dependency authoring |
| Scientific command is hidden behind a Pixi task | Permit a reproduction graph only when every leaf exposes an explicit DataLad/BABS command and record; prohibit DataLad → Pixi task and result-changing Pixi caching |
| A BIDS App operation hides an internal scientific DAG | Use closed operations and one explicit DataLad record per result-changing boundary |
| Current BABS record contains wrapper/zip indirection | Pin BABS; record lifecycle operations; test representative replay; do not copy the pattern elsewhere |
| A BABS result is copied or promoted into a second derivative identity | Use the direct attempt dataset from initialization through in-place finalization and exact-commit acceptance |
| An attempted retry overwrites history or a scientific change masquerades as a retry | Give attempts stable identities; create a new attempt, variant, or campaign as appropriate |
| A BABS lifecycle command is missing | Append expanded argv and before/after state to the operations ledger |
| A direct SIF rebuild differs | Treat the registered exact bytes as the accepted runtime identity and preserve all build inputs and the exact artifact |
| Candidate output enters the research object | Quarantine candidate campaigns; register the image and regenerate every retained output |
| A license is unlawfully withheld or redistributed | Record terms; distribute when permitted; otherwise use a documented read-only bind |
| Study/raw/derivative boundaries blur | Pin BIDS 1.11.1 and independently describe, compose, and validate every dataset root |
| ABCD content becomes public | Separate datasets/siblings and run credential-free publication tests |
| Host home, cache, working-directory, network, or bind state changes a result | Enforce clean containment, disposable cache/scratch/output, explicit binds/network, pilot mount inspection, and P.1 evidence |
| Root manifests or assessments reveal controlled metadata | Use stable non-participant IDs, scan public state, and keep protected evidence in private datasets |
| A D.1-restricted controlled component is reported as fully distributable | Mark it `restricted` at component and root levels and publish the authorized-retrieval scope and remaining public modules |
| Pilot data cannot support poster inference | Use the pilot for workflow/scientific validation and reserve claims for ABCD |
| Notebooks regain authority | Require tested BIDS App operations and reject unique notebook logic |
| External reference data drift | Register exact content with DataLad, license, citation, and checksum |

## Definition of done

The conversion is complete when a collaborator can install the top-level DataLad dataset, obtain every component they are authorized to access, verify every exact SIF, inspect the explicit operation and data lineage of each result, and run the root reproduction entry point so that every result-changing leaf remains visible and replayable. Every accepted BABS derivative retains one identity from initialization through acceptance; every result-manifest row resolves; root/component assessments are committed and consistent; and every restricted/unmet MUST and deferred/declined SHOULD is reported. No result relies on old notebooks, NIH paths, shell history, a historical Pixi task definition, host home/cache state, an untracked environment, or a guessed software version.
