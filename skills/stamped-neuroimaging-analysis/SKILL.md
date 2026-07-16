---
name: stamped-neuroimaging-analysis
description: Perform and assess an ideal-oriented STAMPED neuroimaging analysis using BIDS Study datasets, DataLad and DataLad Containers, Pixi, Apptainer or Singularity, BABS, and explicit campaign management. Use when creating, migrating, executing, debugging, auditing, or releasing a scientific neuroimaging research object, including controlled-data and Slurm workflows.
---

# Perform and assess a STAMPED neuroimaging analysis

Implement the [STAMPED principles paper](https://github.com/stamped-principles/stamped-paper) with the objective of achieving each ideal where practical. Use the paper's maintained [`main.tex`](https://github.com/stamped-principles/stamped-paper/blob/main/main.tex) as the normative basis. Clone the paper repository when local inspection is useful, and read included TeX sources when relevant; do not infer requirements from PDF text extraction.

Distinguish three kinds of instruction:

- **STAMPED requirement:** Enforce every MUST, explicitly decide every SHOULD, and support relevant MAY choices without urging their adoption.
- **Implementation rule:** Follow the opinionated BIDS, DataLad, Pixi, SIF, and BABS choices in this skill. They operationalize STAMPED for neuroimaging but are not universal STAMPED requirements.
- **Hardening:** Consider the measure and record a decision when it is relevant; do not present it as necessary for STAMPED unless the paper says so.

Do not reduce STAMPED to a binary label. Report achievement and gaps principle by principle, for both the complete research object and its components. Follow the released [BIDS 1.11.1 Study dataset convention](https://bids-specification.readthedocs.io/en/v1.11.1/common-principles.html#study-dataset), and record that exact BIDS version.

## Assess the research object and every component

Create a tracked `config/stamped-assessment.tsv` before execution. Inventory the research-object root and every code, configuration, input, derivative, container, environment, model, license, result, and operational module or component. Give each subject a stable identifier and record its parent so the complete boundary is auditable.

Use at least these fields:

```text
subject_id  parent_id  subject_kind  requirement_id  level  decision  status  evidence  limitation
```

Apply these rules:

- Assess each requirement at the research-object level and for every component to which it applies. Do not exempt a component merely because the root is assessed. Use `not-applicable` only with a concrete scope reason.
- Use `met`, `partial`, `unmet`, `restricted`, or `not-applicable` as assessment statuses. `partial` never satisfies a MUST.
- Set every MUST decision to `adopt`. Require evidence before marking it `met`. If law, ethics, access terms, or an external limitation prevents it, mark it `unmet` or `restricted`; explain the gap and never turn it into a pass or an exemption.
- Set every applicable SHOULD decision to `adopt`, `defer`, or `decline`, with a rationale. Prefer `adopt` when practical. A deferred decision must name the condition that will reopen it; use `not-applicable` only with a scope reason.
- Add MAY rows only when the option is useful to the analysis. Support the choice without treating omission as a deficiency.
- Use evidence from committed identities, files, validation reports, or actual run records. A task definition, plan, or intended command is not execution evidence.
- Roll an applicable component failure up to the research-object assessment. The root cannot receive a stronger status than a component on which it depends.
- Reassess after dependency changes, each pilot and campaign, derivative acceptance, and release preparation. Commit the assessment with the state it evaluates.
- Provide a `validate-stamped` Pixi task that fails on missing subjects, omitted MUST/SHOULD decisions, invalid statuses, missing evidence for `met`, or inconsistent roll-ups. Provide a stricter `validate-stamped-ideal` task that fails while any applicable MUST is not `met` and reports every SHOULD that is not both adopted and met.

Assess the normative requirements as follows:

| ID | Level | Criterion to assess |
|---|---|---|
| S.1 | MUST | Every execution-essential module and component is reachable through one top-level research object, with no implicit lookup. |
| S.2 | MUST | License declarations are retrievable with every component they govern. |
| T.1 | MUST | Every component has a persistent content identity. |
| T.2 | SHOULD | Components use the same compatible content-addressed version-control system. |
| T.3 | MUST | Provenance records every modification. |
| T.4-programmatic | SHOULD | Code-driven provenance is captured programmatically. |
| T.4-versions | MUST | Code-driven provenance identifies the versions of all involved components. |
| A.1 | MUST | The object contains unambiguous instructions sufficient to reproduce every computational result. |
| A.2 | SHOULD | Procedures are executable specifications rather than prose alone. |
| M.1 | SHOULD | Components have independent, composable boundaries. |
| M.2 | MAY | Components may be stored directly or linked as subdatasets. |
| M.3 | SHOULD | Modules declare licenses independently and check compatibility where they are combined. |
| P.1 | MUST | Procedures use no undocumented host state. |
| P.2 | MUST | Computational environments are explicit. |
| P.3 | MUST | Environment definitions are version-controlled. |
| E.1 | SHOULD | Results are produced in newly created, disposable execution environments. |
| D.1 | MUST | Referenced components remain persistently retrievable by others. |
| D.2 | SHOULD | Environment specifications support reproducible builds. |
| D.3 | SHOULD | Each module has an explicit license with a resolvable identifier. |

## Establish the research-object boundary

Make the research-object root a DataLad superdataset, not a BIDS dataset. Use this organization:

```text
<research-object>/
├── AGENTS.md                     # points agents to repository-local policy
├── README.md
├── pyproject.toml
├── result-manifest.tsv             # authoritative-result reproduction index
├── src/                          # canonical authored library code
├── apps/                         # canonical authored BIDS App entrypoints
├── tests/
├── skills/                       # complete repository-local skill bundles
├── notebooks/                    # optional and non-authoritative
├── envs/
│   ├── pixi.toml
│   ├── pixi.lock
│   └── containers/
│       ├── repronim/             # pinned source container dataset
│       ├── custom/               # custom definitions when required
│       └── accepted/             # registered exact SIF dataset
├── config/
│   ├── stamped-assessment.tsv
│   ├── datasets/
│   ├── pipelines/
│   ├── clusters/
│   └── campaigns/
├── studies/<study>/              # independent BIDS Study/DataLad dataset
├── operations/<campaign>/        # campaign state and meta-provenance dataset
├── results/<analysis>-<variant>/ # independent multi-study derivative dataset
├── docs/
└── LICENSES/
```

Make the root commit compose the exact commits of all code, configuration, Study, operation, container, and result subdatasets. Do not call the root a BIDS “super-study.”

Put every component under Git, git-annex, and DataLad as appropriate. Record each modification as a human-authored commit or provenance-captured run with authorship and time; never leave an authoritative change represented only by mutable filesystem state.

Assign one authority to each concern:

| Concern | Authority |
|---|---|
| Repository-local agent operating policy | Root `AGENTS.md` and complete bundles under `skills/` |
| Authored package metadata, libraries, apps, and tests | Root `pyproject.toml`, `src/`, `apps/`, and `tests/` |
| Dataset identity, access class, and cohort policy | `config/datasets/` |
| Scientific arguments, application/SIF identity, and output contract | `config/pipelines/` |
| Scheduler resources, binds, scratch, and site preamble | `config/clusters/` |
| Prospective dataset × pipeline × cluster composition | `config/campaigns/` |
| Resolved campaign state and lifecycle provenance | `operations/<campaign>/` |
| Local environments and locked resolution used to construct images | `envs/pixi.toml` and `envs/pixi.lock` |
| Existing scientific runtimes | Exact qualified SIF from a pinned ReproNim/containers dataset |
| Custom SIF construction | Tracked definition and recorded build inputs |
| Result-producing runtime identity | Exact SIF content registered in `envs/containers/accepted/` |
| Code, configuration, data identity, and command provenance | Git, git-annex, DataLad, and DataLad Containers |
| Participant/session fan-out and Slurm execution | BABS |
| Raw/derivative composition and domain metadata | Version-pinned BIDS Study datasets |

Treat a Pixi lock as a local environment specification and an image-build input. Never claim that it identifies the runtime used for a result; the registered SIF content does.

## Compose each scientific Study

Create one BIDS Study/DataLad dataset for each independently governed source study or cohort:

```text
studies/<study>/
├── dataset_description.json       # DatasetType: "study"; BIDSVersion: "1.11.1"
├── README.md
├── code/                          # optional Study-local index/configuration
├── sourcedata/
│   ├── raw/                       # independent raw BIDS/DataLad dataset
│   └── <original-source>/         # optional non-BIDS source material
└── derivatives/
    └── <pipeline>-<variant>-attempt-<N>/
```

- Give the Study, raw dataset, and each accepted derivative its own metadata, DataLad dataset ID, commit, persistent retrieval location, and validation result.
- Set derivative `DatasetType`, `GeneratedBy`, and exact placement-independent `SourceDatasets` metadata. Treat metadata inheritance as local to each BIDS dataset root.
- Point BABS to `sourcedata/raw/`, never the Study root.
- Pin and qualify a BABS revision that supports direct Study layout with `analysis_path: "."`; the reviewed minimum is [`2cc536a`](https://github.com/PennLINC/babs/commit/2cc536a51282124f3811ffa971f82a7c34116af5). Keep its RIA and initialization state under `.babs/`.
- Make each BABS project, DataLad analysis dataset, and provisional derivative the same root. Finalize and validate that same dataset; do not copy its payload into a second derivative, create a filesystem symlink, or change its identity during promotion.
- Treat running, failed, and incomplete attempts as provisional. Mark an exact commit accepted only after merge, provenance-captured finalization, metadata completion, and independent validation.
- Keep BABS-generated `code/` as operational evidence. Never edit it to implement science; change the canonical app or configuration and create a new attempt.
- Keep the operations dataset separate. It records lifecycle decisions and points to attempt datasets but does not contain or replace a derivative.
- Put single-Study group analyses and postprocessing derivatives under that Study's `derivatives/`, each with an independent DataLad/BIDS identity and the same provenance and acceptance gates.
- Put genuinely multi-study analyses in independent derivatives under `results/`, with every exact upstream derivative identified.

Treat the visible `containers/` directory in a BABS derivative as a known BIDS-layout concern. Validate the exact layout as a hard acceptance gate; record a reviewed upstream exception or fix the upstream layout rather than hiding the mismatch with copying or undocumented ignores.

## Isolate controlled data without hiding the gap

- Inventory access rules, licenses or DUC versions, permitted metadata, stable access locations, selection procedures, and derivative-redistribution policy before processing.
- Track exact identities and executable authorized-retrieval procedures. Use access-controlled DataLad remotes or suitable scientific data platforms when available so tooling is never the reason permitted sharing fails.
- Keep public and controlled Studies, derivatives, logs, credentials, and storage siblings separate. Test public publication without credentials or controlled annex content.
- Never infer permission to redistribute derivatives from permission to access inputs. Never embed credentials or prohibited license files in code, images, logs, or public metadata.
- When arbitrary third parties cannot retrieve a controlled component, mark D.1 `restricted` for that component and the research object. State who can retrieve it, under what process, and which permitted portions remain publicly distributable. This is a disclosed gap, not an exemption.
- Do not let a D.1 restriction prevent permitted analysis or distribution of the remaining modules. It prevents only a claim that D.1, or the complete ideal, has been achieved.
- Stop and request a policy decision when any input, log, derivative, or participant-level record may violate an agreement.

## Implement BIDS-facing programs as BIDS Apps

- Build every project-authored program whose primary input is BIDS from the reviewed [`bids-apps/example` template](https://github.com/bids-apps/example/tree/2ef3f19268135273aa49bd2a61c72eaac56f5cef). Record the exact template commit.
- Preserve positional `bids_dir`, `output_dir`, and `analysis_level`; implement only supported levels; add `--participant_label` when selection is meaningful; expose help and version; declare BIDS-validation behavior; and reject unknown arguments.
- Give each operation explicit accepted dataset types, outputs, configuration, seeds, and failure behavior. Do not reuse domain names or participant/group semantics from an unrelated project.
- Invoke each independently meaningful result-changing boundary as its own provenance-captured BIDS App execution. Do not hide a scientific workflow graph inside one nominal operation.
- Apply the same image, provenance, metadata, and testing gates to authored and external apps.
- Keep notebooks exploratory or explanatory. Never make notebook state the sole implementation or provenance of a result.
- Keep scientific parameters in tracked pipeline configuration and scheduler/site settings in separate cluster profiles.

## Use Pixi for environments and actionable entry points

- Keep all Pixi environments in `envs/pixi.toml`, commit `envs/pixi.lock`, track root discovery symlinks, and ignore realized `envs/.pixi/` and `.venv/` contents.
- Record and make retrievable the exact Pixi release and its bootstrap procedure. Supply DataLad and other user-space orchestration tools through locked Pixi environments; declare Apptainer/Singularity, Slurm, kernel, and accelerator requirements that remain host-provided.
- Name environments by responsibility and real dependency boundary. Separate incompatible dependency sets. Change the manifest and lock only in an explicit dependency-authoring session; use `--locked` for ordinary realization and testing.
- Do not use `pixi pack` or `pixi-pack` for the scientific runtime.
- Use typed, described Pixi tasks for validation, development, retrieval, builds, BABS lifecycle operations, and reproducible scientific entry points.
- Make each result-changing leaf task invoke an explicit `datalad containers-run` command or a declared BABS operation. For BIDS Apps, pass the resolved standard arguments and every critical app option to the registered SIF. For other programs, expose the executable and arguments. Ensure the resulting run record shows the actual scientific operation.
- Permit a Pixi meta-task or `depends-on` graph as the discoverable command for reproducing a result set. Make every scientific dependency a provenance-producing leaf task. Treat the graph as an executable specification, not as evidence that any child ran.
- Do not enable Pixi `inputs`/`outputs` caching for result-changing tasks. A cache hit is not scientific provenance.
- Never wrap `pixi run <task>` inside `datalad run` or `datalad containers-run`; that records task indirection instead of the scientific command.
- For a graph requiring dynamic fan-out, conditional recovery, or durable scheduler state, use BABS or a tracked orchestration program that invokes and verifies the same provenance-producing leaf operations. Do not encode opaque control flow in task-shell text.

Prefer this direction:

```text
pixi run --locked reproduce-<result-set>
    -> Pixi dependency graph
    -> explicit DataLad Containers or BABS leaf executions
    -> one intelligible provenance record per result-changing boundary
```

Maintain root `result-manifest.tsv` with at least these fields:

```text
result_id  path  dataset_commit  run_record  container_id  input_ids  reproduce_task
```

Map every authoritative figure, table, statistic, and derivative. The manifest and run records, not the task graph alone, are the reproduction authority. Do not place participant identifiers or prohibited controlled metadata in the root manifest.

## Acquire, register, and distribute scientific runtimes

For each runtime:

1. Search the pinned ReproNim/containers dataset first. If an image has the required app, version, architecture, interface, and terms, pin its dataset commit and annex key, retrieve the exact SIF, and qualify it with project fixtures.
2. Build a custom SIF only when no existing image is suitable. Track its definition under `envs/containers/custom/<runtime>/`, adapt reviewed ReproNim, BIDS Apps, or NeuroDesk patterns where useful, and pin or checksum every build input.
3. For an authored image, copy the reviewed Pixi manifest and lock into the definition and run `pixi install --locked` at the final in-image path.
4. Build the SIF with a recorded Apptainer/Singularity version and target architecture. On macOS, build inside Linux with Lima; on Apple Silicon, use an x86_64 guest for an x86_64 Slurm target.
5. Record source dataset/annex identities or definition/lock hashes, tool versions, target platform, command, smoke tests, SIF SHA-256, and annex key. A lock does not make every external build input deterministic or guarantee byte-identical rebuilding.
6. Register the qualified SIF with `datalad containers-add` in `envs/containers/accepted/`, and publish its annex content to persistent storage.
7. Distribute required license files when terms permit. Otherwise record acquisition and verification and provide them through a declared runtime bind. Never embed credentials or secrets.

Apptainer builds the image; DataLad Containers identifies, retrieves, and executes it. A Pixi task can make build and registration commands actionable but does not identify the result-producing container.

Quarantine outputs from candidate SIFs as disposable and non-authoritative. Before retaining, merging, comparing scientifically, or releasing an output, register the exact SIF and regenerate the output through BABS or `datalad containers-run`.

**Hardening:** Consider signing and verifying each accepted SIF and attaching an SBOM or build attestation. Record the decision and evidence; identify and sign any intentionally distributed OCI artifact separately.

## Execute in disposable environments

- Stage authenticated retrieval before the scientific execution. Allow the execution to receive only the exact SIF, declared input datasets, a new output location, tracked configuration, a declared application license file when required, and explicit host resource interfaces; do not give it retrieval credentials.
- Start from fresh work and scratch directories. Use `--cleanenv` and `--containall` or equivalent controls. If full containment is unavailable, use `--no-home` or `--no-mount home,cwd` with equivalent isolation. Never mount the host home or inherit an undeclared working directory; provide an empty temporary home or an intentional read-only home from the image.
- Disable persistent container and application caches. If software requires a cache directory, point it to fresh scratch and destroy it after execution.
- Declare every project bind and disable configured host bind paths where the platform permits. Mount inputs and configuration read-only, expose only the required output and scratch paths as writable, inspect the realized mount table during the pilot, and record unavoidable system binds as P.1 limitations.
- Disable network access when the computation does not require it. When it does, record the endpoint and purpose as an explicit input or host dependency.
- Record unavoidable host coupling, such as kernel, accelerator, scheduler, filesystem, or security policy, in the cluster profile and P.1 assessment.
- Retain only declared outputs, required logs, and provenance. Destroy work, scratch, temporary home, and cache state after the run.
- Apply equivalent controls in BABS job templates and inspect the expanded participant script during the pilot. Test a representative execution from a clean clone with an empty home/cache and no prior output.

## Run and account for BABS campaigns

Create one operations dataset per dataset × pipeline/runtime × input-condition × cluster campaign. Resolve the exact dataset, pipeline, cluster, tool, and access identities into an immutable campaign snapshot.

For every campaign:

- Give each attempt a stable identity. Never overwrite it. Treat a scientific input, SIF, or pipeline change as a new variant or campaign rather than a retry.
- Preserve requested inclusion separately from BABS-realized inclusion. Record runtime failures separately from eligibility and missing-input exclusions.
- Keep desired and observed state distinct. Advance through small, recorded transitions based on BABS, RIA, log, and output evidence.
- Record initialization, setup checks, submission, status inspection, retry decisions, merge, finalization, validation, and acceptance as operational meta-provenance.
- Pilot one participant/session. Inspect the run record, SIF identity, input commits, expanded execution command, isolation controls, outputs, and resource request before scaling.
- Use the campaign-axis, clean-pin, attempt, state-ledger, resumable-transition, and inclusion-accounting patterns credited to [mechababs](https://github.com/asmacdo/mechababs), without installing or invoking mechababs unless the skill is explicitly revised to adopt it.

BABS's generated wrapper and zip/merge layer add provenance indirection. Preserve the generated execution material, inspect the expanded command, test representative historical replay, and do not reproduce this indirection in authored steps.

## Validate, accept, and release

Require evidence for these gates:

- A clean recursive clone resolves every permitted component or gives exact authorized controlled-access instructions.
- Every retained result-changing step resolves to code, configuration, input commits, exact SIF content, explicit command, and output through an intelligible DataLad/BABS record.
- Each accepted BABS attempt retains one dataset identity from initialization through provenance-captured finalization.
- Parent registration and a clean recursive clone preserve each accepted attempt and its required input/output RIA retrieval paths.
- Representative historical replay and clean-room SIF execution reproduce fixture outputs and pass domain checks.
- The Study, raw input, and each accepted derivative validate independently against BIDS 1.11.1 or carry a reviewed upstream exception.
- Public release tests cannot retrieve controlled annex content or reveal credentials, prohibited metadata, or participant-level logs.
- Code, documentation, data, models, containers, and distributed license files have compatible license/DUC records at every composition boundary.
- Every result-manifest entry resolves to present files, exact provenance, exact inputs, the accepted SIF, and an executable reproduction entry point.
- Every MUST row in the current component and root assessments is `met`, or remains visibly `restricted`/`unmet` with evidence. Never describe the latter as achieved.
- Every SHOULD row has a recorded decision and rationale. Report adopted, deferred, and declined SHOULDs separately.

Publish the seven-principle assessment with the release. State the intended scope, component roll-up, evidence, controlled-access limitations, and remaining gaps. Report failed gates with evidence, and never scale a campaign to compensate for an unresolved pilot failure.
