# Policy review: execution can outrun committed research-object state

## Status and scope

This document is an input to review of
`skills/stamped-neuroimaging-analysis/SKILL.md`, the conversion plan, and the
execution entry points that implement them. It describes a general policy and
enforcement defect. It is not a proposal merely to clean up one worktree.

## Issue summary

The current policy describes reproducibility well as a desired final state,
but it does not preserve reproducibility as an invariant during execution. A
campaign can be initialized or advanced while its root environment, launchers,
configuration, subdataset pointers, or operations dataset exist only as
uncommitted filesystem state.

In that condition, the command may produce logs and commits inside child
datasets, but no root commit identifies the complete state that launched it.
The resulting work is difficult to audit, reproduce, resume, review, or roll
back. Later consolidation cannot prove exactly which mutable state was used at
the time of execution.

This is especially serious for environment changes. If `envs/pixi.toml`,
`envs/pixi.lock`, the Pixi bootstrap, execution wrappers, or relevant tasks are
dirty, the root `HEAD` does not identify the toolchain used by the operation.
Using a locked environment at runtime does not solve this: the lock itself must
already have a committed identity composed into the executing root commit.

## Triggering observation

On 2026-07-21, during Phase 3 requalification, the repository reached a state
with all of the following characteristics:

- the root was only one commit ahead of its upstream while holding a broad,
  mixed set of uncommitted changes;
- the dirty root set included `envs/pixi.toml`, `envs/pixi.lock`, the Pixi
  bootstrap and documentation, BABS task definitions and launcher code,
  validators, campaign configuration, and new scripts;
- the accepted-container subdataset had advanced commits not yet represented by
  a root gitlink commit;
- the SimBIDS Study had advanced commits and an untracked derivative attempt;
- the BABS operations dataset had its own useful commit history, but the entire
  dataset was still unregistered and untracked by the root.

This pattern demonstrates the defect even if every individual change is later
corrected and committed. Work progressed without a root identity for the
environment and composition that produced it.

## What the existing policy gets right

The skill and conversion plan already contain the intended principles:

- the root commit composes exact code, configuration, Study, operation,
  container, and result subdataset commits;
- authoritative changes must not remain represented only by mutable filesystem
  state;
- Pixi manifests and locks are committed, and lock changes occur only in an
  explicit dependency-authoring session;
- the dependency-update cycle commits the manifest, lock, tests, ledger change,
  and rationale together;
- Phase 3 execution is performed from a clean clone;
- evidence and assessment are recommitted after dependency and campaign
  changes.

These statements should remain. The problem is that they are distributed
across a long policy, mostly describe eventual evidence or acceptance, and do
not define a mandatory transaction boundary before each operation.

## Why the current wording is insufficient

### No hard pre-execution condition

The policy does not explicitly say that BABS initialization, checking,
submission, merge, finalization, or another retained result-changing operation
must refuse to start when the execution checkout or any relevant subdataset is
dirty.

### Ambiguous use of “authoritative”

An operator can interpret the mutable-state prohibition as applying only after
an attempt is accepted. That leaves initialization, pilots, failures, and other
“provisional” work outside the practical guardrail even though those operations
create durable state and guide later decisions.

### No separation between authoring and execution

The policy names dependency-authoring sessions but does not prohibit campaign
execution while such a session remains uncommitted. Environment design and
environment use can therefore overlap in one worktree.

### No nested-dataset commit protocol

The policy does not define the required sequence among child commits,
publication, superdataset gitlink updates, and the next lifecycle operation.
Consequently, useful commits can accumulate in children while the root no
longer describes their composition.

### No failure transaction

It is unclear what must be committed when initialization, checking, or a job
fails. Failure evidence is scientifically and operationally important; it must
not be left in an indefinitely dirty operations dataset while more work
continues.

### No executable enforcement

The launchers rely on a person or agent to interpret policy correctly. The
critical checks are not a mandatory, fail-closed preflight called by every
result-changing entry point. Dense prose cannot make this failure mode
impossible on its own.

## Proposed remediation

### 1. Add a prominent execution-transaction gate to the skill

Add the following normative rule near the beginning of the skill, before the
architectural guidance.

> **Execution transaction gate**
>
> Treat every operation that creates or changes retained campaign, attempt,
> result, provenance, inclusion, scheduler, merge, or acceptance state as a
> transaction. This includes BABS initialization, setup checks that write
> evidence, pilot and batch submission, status/retry recording, merge,
> extraction, finalization, validation that writes evidence, and acceptance.
>
> Before a transaction starts, use a dedicated clean execution checkout. The
> root and every relevant installed subdataset must be clean; every nested
> dataset under an authoritative path must be registered; child `HEAD`s must
> equal the gitlinks recorded by the root; and the root commit must identify the
> exact environment manifest and lock, launcher, pipeline and cluster
> configuration, campaign snapshot, input datasets, accepted container
> dataset, and operations dataset used by the operation.
>
> A dependency-, code-, image-, configuration-, or policy-authoring session
> must be completed, validated, committed, and composed into the root before an
> execution transaction may begin. Do not author and execute from the same
> dirty checkout. Use a separate clean worktree or clone when unrelated
> development must continue.
>
> Execute one lifecycle transition at a time. After the transition, record its
> exact command, versions, pre-state, outcome, and post-state; commit every
> changed child dataset; publish each child and required annex content; update
> and commit the root gitlinks and records; and verify the recursive state is
> clean before beginning the next transition. Record and checkpoint failed
> transitions by the same procedure.
>
> Submission of a long-running job closes one transaction after submission
> evidence is committed and composed at the root. Later status, retry, merge,
> and finalization actions are separate transactions and may not begin from an
> unresolved prior checkpoint.
>
> Disposable debugging is permitted only in an explicitly quarantined location
> whose outputs cannot be retained, merged, compared scientifically, or used as
> campaign evidence. If debugging creates retained state, it is an execution
> transaction and all rules above apply.
>
> Every result-changing launcher must run an automated fail-closed preflight.
> Never bypass the preflight manually. A failed preflight blocks execution; it
> is not a warning to document later.

### 2. Define “clean” and “relevant” precisely

The skill should define a clean execution state as:

- no staged, unstaged, or untracked files in the root or relevant registered
  subdatasets, except explicitly ignored disposable host state;
- no unregistered Git or DataLad dataset below `studies/`, `operations/`,
  `results/`, or `envs/containers/`;
- every installed child dataset at the exact commit recorded by its parent;
- every required child commit published to its declared reachable sibling, with
  required annex content available;
- no unresolved merge, rebase, cherry-pick, annex journal, or interrupted
  DataLad operation;
- a Pixi environment that realizes with `--locked` without changing the
  manifest or lock;
- a campaign snapshot containing exact root, input, pipeline, cluster,
  operations, BABS, and accepted-SIF identities.

Relevant datasets include the root, the campaign operations dataset, the BABS
attempt, its containing Study and raw input, the accepted-container dataset,
and any other code, configuration, or result dataset consumed or changed by the
transition.

### 3. Specify checkpoint ordering for nested datasets

For each lifecycle transition, require this order:

1. Verify the prior root checkpoint and recursive clean state.
2. Render and save the exact prospective identities and command.
3. Execute exactly one declared transition.
4. Record success or failure and all resulting state.
5. Save and commit changed leaf/child datasets.
6. Validate and publish those commits and required annex content.
7. Save parent datasets from the inside out.
8. Commit the root composition and assessment/ledger updates.
9. Verify recursive cleanliness and retrievability.
10. Permit the next transition.

This makes the root commit a sequence of durable campaign checkpoints rather
than an eventual summary assembled after several operations.

### 4. Add a mandatory automated preflight

Provide one repository-owned preflight command and require every Pixi BABS or
result-changing task to invoke it before calling BABS, DataLad Containers,
Slurm, or another scientific executable. It should fail before the underlying
operation starts when any invariant is violated.

At minimum, it should check:

- recursive Git/DataLad cleanliness;
- unregistered nested repositories in authoritative paths;
- child `HEAD` versus recorded parent gitlink identity;
- root composition of the campaign, Study, attempt, operations, and container
  datasets;
- committed identity of `envs/pixi.toml`, `envs/pixi.lock`, launchers, and all
  selected configuration;
- successful locked Pixi realization with no lock rewrite;
- exact BABS revision and accepted SIF identity/content availability;
- campaign snapshot consistency with the current root commit;
- expected new or resumable attempt identity and output location;
- absence of an unresolved prior lifecycle transition.

The preflight should emit a compact machine-readable record containing the
resolved identities. The operations ledger should reference that record.

### 5. Test the guardrail negatively

Add automated fixtures proving that no underlying BABS or scientific command is
invoked when any of these conditions exists:

- dirty `envs/pixi.toml`;
- dirty or rewritten `envs/pixi.lock`;
- dirty launcher or campaign configuration;
- an untracked campaign file;
- a child dataset ahead of its recorded gitlink;
- an unregistered nested Study, attempt, operations, or container dataset;
- an unpublished required child commit or unavailable required SIF content;
- campaign snapshot identities that differ from the executing root commit;
- an unresolved prior failed or successful transition.

Also test a clean positive fixture and assert that the preflight record contains
all identities required to reconstruct the operation.

### 6. Make checkpoint cadence visible in campaign state

Each operations-ledger transition should identify at least:

- pre-transition root commit;
- post-transition root commit once composed;
- operations-dataset commit;
- attempt-dataset commit when applicable;
- input and accepted-container commits;
- Pixi manifest and lock commit;
- exact command and tool versions;
- transition result and failure classification;
- publication and annex-availability evidence.

The campaign state machine should refuse a transition whose predecessor lacks a
completed root checkpoint.

## Acceptance criteria for the remediation

The policy and implementation are adequate when:

1. The transaction gate is prominent and uses `must`, `must not`, and `refuse`
   rather than relying on eventual acceptance language.
2. Every retained result-changing entry point shares the same mandatory
   preflight.
3. All negative fixtures stop before BABS, Slurm, DataLad Containers, or another
   scientific executable is invoked.
4. A clean positive fixture records the exact root and component identities
   before execution.
5. Every lifecycle transition, including a failure, ends in a recursively clean
   root checkpoint before another transition can start.
6. An environment update cannot overlap a campaign execution transaction.
7. A clean recursive clone at any completed checkpoint can recover the campaign
   state and determine exactly which committed toolchain and inputs were used.

## Handling work that exposes this defect

Do not repair an affected campaign by silently committing the accumulated
filesystem state and treating it as if the root identity had existed before
execution. Preserve the observed commands and child histories, classify the
attempt as non-authoritative or qualification/debugging evidence, and regenerate
any retained output from a committed clean checkpoint after the policy and
preflight are corrected.

The immediate cleanup of any particular attempt is a separate decision. The
priority of this review is to make recurrence structurally difficult and
automatically blocked.
