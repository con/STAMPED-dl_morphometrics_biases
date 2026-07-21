# Phase 3 retry preliminary review

Date: 2026-07-21

## Scope

This is a process retrospective based only on the working conversation and the
decisions made during the Phase 3 retry. It does not inspect or judge the final
datasets, reports, validation records, or scientific contents. Its purpose is
to capture where the work became fragile, surprising, or unnecessarily costly
so that the next campaign can be designed more deliberately.

The retry was useful because it exposed problems at four distinct boundaries:

1. shell and cluster-session reliability;
2. our project interfaces and operating procedure;
3. Unity-specific integration;
4. behavior or defects in the pinned BABS revision.

Keeping those categories separate matters. A cluster discovery should not be
described as a BABS defect, and a project invocation mistake should not be
worked around as though it were an environmental limitation.

## Preliminary assessment

The largest avoidable cost came from discovering interface assumptions during
campaign execution instead of in small preflight fixtures. The retry crossed
several independently stateful systems—Pixi, Bash startup, DataLad
superdatasets, the accepted-container registry, BABS projects, two RIAs, Slurm,
git-annex, archive extraction, and BIDS validation. A late correction in one
layer often required synchronization or provenance updates in several others.

The next campaign should therefore be treated as a sequence of explicit gates,
not as one long command sequence. Each gate should establish a small invariant
and stop before allocating a campaign identity or submitting work.

## Issue register

| Area | What occurred | Preliminary ownership | Better approach |
|---|---|---|---|
| Browser shell lifetime | The browser shell was believed to disconnect after approximately 15 minutes of inactivity, and a compute allocation was later killed while work was in progress. | Unity/session integration | Use `tmux` for interactive continuity, but rely on `sbatch`, recorded job IDs, and durable logs for work that must survive a browser disconnect. Do not assume a running agent counts as browser activity or that `tmux` preserves a scheduler allocation. |
| Remote sibling access | The execution context could not initially reach remote sibling state that was accessible from the original source repository. Permission and sandbox changes interrupted diagnosis. | Environment/access setup | Run one read/write/credential/sibling preflight at the beginning, from the intended authoritative clone. Resolve remote configuration there before campaign work begins. |
| Pixi discovery | Commands repeatedly named `$HOME/.pixi/bin/pixi` or directly prefixed a private Pixi environment's `bin` directory. | Ours | Put `$HOME/.pixi/bin` on `PATH` before `.bashrc`'s noninteractive early return. Invoke plain `pixi`; let `pixi run --locked -e <environment> <task>` select tools. |
| Pixi task working directory | Tasks in `envs/pixi.toml` initially resolved paths relative to `envs/`, while commands assumed the repository root. The direct environment-bin workaround concealed this. | Ours | Give repository tasks an explicit root `cwd`, retain root manifest/lock discovery links, and test every operator-facing task from a fresh noninteractive shell. |
| CLI verbosity and layering | Lifecycle operations were launched with long ad hoc commands, and there was uncertainty over whether every command should be wrapped in `datalad run`. | Ours/interface design | Use short Pixi tasks for BABS lifecycle operations and keep expanded argv in machine logs. Use `datalad run` only for transformations of tracked dataset content, not for scheduler state changes such as submit or status. |
| BABS CLI selection | Deprecated compatibility executables and the unified `babs <subcommand>` interface were mixed. | Ours | Expose only the unified CLI through project tasks. Reject unsupported lifecycle operations before invoking BABS. |
| Container registration | The first accepted-container state had a DataLad configuration entry but not BABS's conventional `.datalad/environments/<name>/image` registration. | Ours | Register accepted images with `datalad containers-add` and verify both DataLad Containers and BABS resolution before initialization. Do not manually synthesize only part of the convention. |
| Failed initialization cleanup | A failed BABS initialization attempted cleanup, but read-only annex object permissions left a remnant and raised concern about accidentally reusing a briefly assigned UUID. A later initialization also failed because the derivative parent did not yet exist. | Mixed: our preflight plus BABS cleanup behavior | Create and verify destination parents before init. Initialize in a disposable path first when qualifying a new integration. Retain failures explicitly and never reuse a partial project's identity silently. |
| Direct-layout checker | Initialization correctly used `analysis_path: "."` and `sourcedata/raw`, while `check-setup` still asserted the historical `inputs/data` layout. | BABS | Report with a self-contained reproducer. Until fixed, isolate any temporary compatibility alias to the checker step, record it, remove it before submission, and verify that it is absent afterward. |
| BABS version assumptions | The broken behavior was initially discussed as though the project might simply be pinned too far behind, but the selected commit was also current upstream `main` at review time. | Review discipline | Compare the pin to upstream before attributing a defect to age. Update a pin only for a demonstrated fix, not as a speculative remedy. |
| Unity Slurm profile | BABS's generic temporary-disk directive was not accepted by Unity. This was learned through a campaign attempt rather than a tiny scheduler test. | Unity qualification | Qualify generated `#SBATCH` directives with a minimal job before campaign initialization. Keep the Unity profile limited to options actually supported at the site. |
| Batch preamble | An absolute environment `PATH` and temporary `HOME`/cache overrides were added to the participant preamble to make host tools available and isolate state. They were hard-coded and not justified by a demonstrated need. | Ours | Source the account startup file and activate the locked Pixi environment normally. Add host `HOME` or cache redirection only if a reproducible failure requires it and verified job-local storage and cleanup are available. |
| `.env` behavior | `con-duct` warned that `python-dotenv` was absent even though `.env` files were expected. The intended loader and lookup boundary were initially unclear. | Ours/dependency contract | Lock `python-dotenv`, load exactly the repository-root `.env`, supply a non-secret `.env.example`, and ignore the real file. Treat it as operational configuration, not a credential store, because process-observability tooling may record environment values. |
| Output ZIP semantics | `all_results_in_one_zip` was initially surprising and risked being conflated with a proposed zipless BABS workflow. | Explanation and interface review | Decide the application-to-BABS output-directory contract before submission. Treat `all_results_in_one_zip` as an archive-layout option, not as a way to disable archives. Handle zipless BABS as a separate upstream feature decision. |
| Broken finalization entry point | The installed `babs-unzip` entry point imported a function that no longer exists. | BABS | Do not invoke or hide the failure. Select a project-owned finalization policy in advance: `datalad add-archive-content`, the tracked unzip script plus one DataLad save, or a tested upstream replacement. |
| Annex backend | BABS initialized the analysis dataset with MD5E despite the root project's SHA256E policy. This was noticed only after merged archives existed and required migration. | Integration policy | Check and, if necessary, configure the annex backend immediately after initialization and before any result branches are produced. Add a pre-submit gate rejecting MD5-family keys. |
| Archive extraction performance | `datalad add-archive-content` was semantically appropriate but very slow for thousands of small files on the shared filesystem. An interrupted partial extraction then had to be cleaned carefully. | Workload/site interaction | Benchmark finalization on one fixture archive before the campaign. For tiny-file trees, use plain unzip followed by one DataLad save when provenance requirements permit it. Avoid generating unnecessary FreeSurfer-shaped trees, for example with `--fs-no-reconall`, when they are not part of the qualification objective. |
| BIDS and operational layout | A BABS direct-layout project combines operational paths with derivative payload. Earlier `.bidsignore` handling risked hiding operational directories merely to make validation pass. | Integration design | Validate a structurally defined derivative payload view. Reserve `.bidsignore` for reviewed payload extensions that are genuinely outside the selected BIDS schema; do not use it to conceal BABS, container, log, or source-data directories. |
| Three-task qualification | Moving from a one-subject toy to three SimBIDS participants increased confidence but also amplified every shared-filesystem and synchronization problem. | Test design | Keep the three-task concurrency check, but make its input and output trees intentionally small. First prove the exact image and wrapper contract with one local fixture, then submit the bounded array. |
| Persistent publication | The exact converted SIF was usable locally, but an OCI tag or digest is not a persistent location for the exact SIF bytes. | Publication planning | Establish annex publication and clean-clone retrieval before calling an image independently reusable. Keep local qualification and persistent publication as separate recorded gates. |

## Themes that made the retry harder than necessary

### 1. Preflight happened too late

Several failures could have been discovered without a campaign attempt:

- missing destination parents;
- unsupported Slurm directives;
- incomplete container registration;
- Pixi tasks starting from the wrong directory;
- whether the generated participant script could find host tools;
- the app/BABS output-directory contract;
- the selected annex backend;
- the stale unzip entry point.

The recurring pattern was to let a high-level command discover a low-level
invariant. The next procedure should test those invariants directly first.

### 2. Recovery commands became part of the apparent interface

Long absolute paths, manual `PATH` construction, temporary environment
variables, and narrow repair scripts were sometimes necessary to diagnose or
recover. The problem was not their temporary use; it was allowing them to look
like the intended steady-state workflow.

Recovery commands should be labeled as such in the ledger or review. Once the
cause is understood, the normal interface should be repaired and re-exercised
through its concise Pixi task.

### 3. Configuration, execution, and evidence were easy to conflate

The retry involved three different command classes:

- environment and registry preparation;
- BABS lifecycle management and scheduler interaction;
- transformations of tracked content.

Pixi should select the environment for all three. The BABS operations ledger
should record the second class. `datalad run` should capture the third class.
Forcing all commands into one provenance mechanism makes the logs noisier
without making scheduler side effects reproducible.

### 4. Compatibility workarounds need an expiration condition

The direct-layout checker alias and project-owned archive finalizer are bounded
compatibility measures. Each should record:

- the exact upstream defect it addresses;
- where it is introduced;
- how its absence from accepted state is checked, when applicable;
- what upstream change allows its removal.

Without those conditions, a narrow workaround can quietly become permanent
project architecture.

### 5. Interactive continuity and computational durability are different

`tmux` can preserve an interactive shell or agent process when the browser
connection drops, provided the host session itself remains alive. It does not
guarantee that an interactive compute allocation survives, nor does a running
process necessarily count as activity to a browser gateway.

Long-running scientific work should therefore be represented by scheduler jobs
whose identifiers and logs are durable. Interactive sessions should only
prepare, submit, inspect, and resume them. A continuation note should state the
last completed gate, active job IDs, authoritative dataset paths, and the exact
next command.

## Proposed gate sequence for the next campaign

### Gate 1: shell and Pixi bootstrap

- A clean noninteractive Bash shell resolves plain `pixi`.
- The exact required Pixi version is reported.
- `pixi lock --check` passes.
- The BABS and quality environments run through short locked tasks.
- No operator command names a private `.pixi/envs/.../bin` directory.

### Gate 2: input and image identities

- Study, raw input, and accepted-container dataset IDs and commits are fixed.
- The requested inclusion file has the expected bounded row count.
- `datalad containers-list` resolves the intended name.
- `.datalad/environments/<name>/image` resolves the expected SHA256E key.
- Exact SIF content is locally available; persistent retrieval status is stated
  separately and honestly.

### Gate 3: disposable BABS initialization

- Destination parents exist and are writable.
- Direct-layout paths resolve to `sourcedata/raw` and `.babs/*_ria`.
- The generated scheduler directives are accepted by a tiny Unity test.
- The generated app command has the expected image, input, output, isolation,
  and wrapper arguments.
- The analysis dataset's annex backend is SHA256E before work is submitted.

### Gate 4: official setup check

- Run the official checker and its Unity job test.
- If the upstream direct-layout defect still exists, introduce only the
  documented compatibility alias, synchronize it, run the check, remove it,
  synchronize again, and assert its absence.
- A checker failure stops the campaign; it is not waived informally.

### Gate 5: bounded execution

- Exercise the exact SIF and wrapper contract on one minimal fixture first.
- Submit the three-task array only after that contract passes.
- Record the job ID immediately and make status collection resumable from a new
  shell.
- Keep scratch cleanup in the generated job and avoid dependence on the browser
  session or interactive allocation.

### Gate 6: merge and finalization

- Select the archive policy before submission.
- Retrieve and merge through normal BABS lifecycle tasks.
- Confirm archive annex keys use SHA256E.
- Apply the chosen extractor once, followed by a bounded DataLad save or
  `datalad run` transformation as appropriate.
- Do not call a known-broken compatibility entry point.

### Gate 7: independent validation and publication readiness

- Validate only the declared derivative payload with the Deno validator.
- Review warnings explicitly; do not suppress operational paths with
  `.bidsignore`.
- Confirm exact dataset ID and commit, content availability, and RIA state.
- Test persistent image and derivative retrieval independently before making a
  clean-clone or publication claim.

## Questions to resolve before another scientific campaign

1. Will BABS fix the configured-input checker, or will the project carry a
   narrow tested patch instead of repeating the alias procedure?
2. Is project-owned post-merge finalization the intended long-term policy, or
   should BABS regain a supported finalization command?
3. Should SHA256E be configured by a BABS project template, a post-init task,
   or an upstream BABS option?
4. Which exact SIF storage sibling will provide independent persistent
   retrieval, and who owns publication?
5. Which SimBIDS outputs are necessary for qualification? Can expensive
   FreeSurfer-shaped output be omitted from future fixtures?
6. What is the minimal Unity bootstrap that works from login, noninteractive,
   and Slurm shells without embedding checkout-specific binary paths?
7. What automated test will prevent BABS operational paths from being hidden by
   future `.bidsignore` changes?

## Non-conclusions

This preliminary review does not establish that the resulting derivative is
scientifically valid, publication-ready, or independently reproducible. It also
does not reassess the final validation evidence. Those judgments require an
explicit review of the outputs and their recorded identities, which is outside
the scope requested here.
