# Execute from committed research-object state

Use this protocol for any operation that creates retained campaign, attempt,
scheduler, provenance, dataset, result, merge, validation, or acceptance state.
Treat read-only inspection separately.

## Establish the project interface

Require plain `pixi` to resolve in the current shell and use
`pixi run --locked ...` as the normal entry point. If shell initialization does
not expose Pixi, stop project work and fix the login/noninteractive/Slurm shell
setup. Do not continue with absolute binary paths or environment-`bin` path
injection.

Use Slurm, not the browser shell, as the durability boundary for compute. Verify
the cluster's submission and cancellation policy, then let accepted jobs run
independently of the interactive shell. Use `tmux` only for operator
convenience; never make a result depend on an attached terminal or a keepalive
loop.

## Separate authoring and execution

Treat changes to dependencies, locks, code, tasks, images, pipeline arguments,
cluster profiles, campaign configuration, and dataset composition as an
authoring transaction. Develop and test one coherent change, then commit it and
compose affected child commits at the root before execution consumes it.

Treat each retained lifecycle transition as an execution transaction:

1. Start from the committed root state intended to identify the operation.
2. Resolve the selected input, configuration, operations dataset, registered
   SIF, and existing attempt identities; for initialization, resolve the
   declared new-attempt location instead.
3. Inspect the rendered BABS/Slurm/container interface when it changed or when
   feedback will be costly.
4. Execute one declared transition and preserve its actual command and outcome.
5. Save content transformations with DataLad run provenance; save authored
   metadata and structure with `datalad save`.
6. Commit changed child datasets from the leaves inward, update the root
   composition and concise operations record, and commit that checkpoint before
   starting a dependent transition.

Checkpoint a retained failure by the same rule when it informs retry or later
decisions. Do not retroactively present a later aggregate commit as the
pre-execution identity of earlier work.

Use this minimum cadence:

| Retained change | Checkpoint before |
|---|---|
| Pixi manifest/lock, code, task, image, pipeline, or cluster profile | Any campaign uses it |
| Selected input, SIF, and campaign configuration | BABS initialization |
| Initialized attempt and operations state | Setup check, pilot, or submission |
| Submission and scheduler evidence | Retry, merge, or replacement submission |
| Merge state | Extraction or finalization |
| Finalized and validated derivative | Acceptance or downstream use |

Status polling may remain read-only. Summarize it only at a meaningful state
transition. Keep truly disposable debugging in a quarantined location and
never retain, merge, compare scientifically, or cite its outputs.

## Keep enforcement compact

Provide one repository-owned pre-execution check for retained entry points. It
should reject only the expensive, recurring transaction defects:

- relevant environment, code, or configuration differs from the committed
  root state;
- a selected child `HEAD` differs from the commit composed by its parent;
- a selected input, campaign, operations dataset, or SIF identity cannot be
  resolved;
- a previous retained transition lacks its required checkpoint.

Emit the root commit and a short actionable reason. Do not dump a complete
identity inventory, probe every low-level command, or replace native tool
validation. Test this check with focused positive and negative fixtures.

## Inspect slow-feedback interfaces

Before a pilot, inspect the resolved BABS input layout, conventional container
registration, output handling, generated participant command, Slurm options,
resource request, and containment/bind configuration. Before scaling, inspect
the pilot's actual run record, inclusion, outputs, failure classification, and
resource use.

Consult cluster documentation before using unfamiliar Slurm options. Submit a
tiny scheduler probe only when documentation and rendered-script inspection
cannot establish compatibility. Do not bypass BABS merely to test every
primitive.

## Publish durable checkpoints deliberately

Commit checkpoints immediately; publish them at the project's declared
durability, collaboration, and release boundaries. Publish child Git history
and required annex content before advertising a root composition to others.
Verify fresh recursive retrieval before claiming distributability.

Record concise decision provenance: hypothesis or purpose, method/configuration,
pre-execution root commit, actual command and component versions, outcome, and
post-state. Preserve useful generated records, but do not substitute an entire
shell transcript for targeted provenance.
