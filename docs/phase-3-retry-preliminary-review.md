# Phase 3 retry preliminary review

Date: 2026-07-21

## Purpose

This reviews the Phase 3 retry approach from the working conversation, not by
reassessing its outputs. It is intended to inform a later revision of the
STAMPED neuroimaging skill.

The earlier review was too much of an incident catalog. Copying such a catalog
into a skill would increase context while encouraging agents to test every
primitive. The useful lessons are a few constraints that prevent frequent
mistakes or protect operations with slow feedback.

## Revised conclusion

The retry needed stronger high-level interfaces, not more gates.

Pixi, DataLad, BABS, Singularity, and Slurm should each own the work they are
designed to do. The project should expose a small set of Pixi tasks that compose
them. Agents should use those tasks normally and reach for lower-level commands
only when diagnosing a broken abstraction.

The most serious process failure was executing while environment definitions,
launchers, configuration, and nested dataset pointers were still uncommitted.
A phase-sized commit made later cannot identify the mutable state used by
earlier commands.

The central rule is:

> **Commit before execute; checkpoint retained state before the next dependent
> action.** Finish and commit environment or configuration authoring before a
> campaign starts. When execution creates retained state, commit children first
> and then the root composition before another action relies on it.

This is the actionable core of
`neuroimaging-policy-execution-transaction-gap.md`. It should be prominent and
enforced, not distributed through a long checklist.

## Four operating constraints

### 1. Plain Pixi must work first

Finding tools should not be a recurring problem. One setup script should
install the pinned Pixi release when needed, place it in an ignored local or
user location, and make plain `pixi` available in login, noninteractive, Slurm,
and agent shells through minimal startup configuration.

If `pixi` is missing, diagnose and fix shell setup before proceeding, requesting
user help when persistence requires it. Do not continue with an absolute Pixi
path or by prepending a private environment `bin` directory. Those workarounds
bypass the project interface and inflate every command and log afterward.

For project-authored runtimes, Singularity should be a thin isolation wrapper
around the locked Pixi environment rather than a second hand-maintained
dependency specification. External BIDS App images still retain their exact
container identity.

### 2. Use tools at their native boundaries

| Tool | Responsibility |
|---|---|
| Pixi | Install/select tools and provide concise typed entry points. Ordinary use is `pixi run --locked ...`. |
| DataLad | Version and compose datasets. Use `datalad run` for tracked content transformations and `datalad save` for structural or metadata changes. |
| BABS | Own participant fan-out, Slurm submission, RIAs, status, merge, and generated execution provenance. |
| Singularity/Apptainer | Execute the declared image with the required isolation and binds. |
| Slurm | Own durable compute independently of the browser or interactive shell. |

Pixi tasks may compose these tools but should not obscure them. BABS lifecycle
state is not a scientific transformation merely because it is wrapped in
`datalad run`; conversely, a content transformation should record the actual
command rather than only a Pixi task name.

### 3. Inspect interfaces with expensive feedback

The proposal to test every low-level invariant first is rejected. Routine work
should trust the project abstractions. Advance inspection is worthwhile when a
mistake is costly or repeatedly encountered:

- inspect Unity's supported Slurm options and the BABS-rendered batch script
  before submission;
- inspect the rendered BABS input, image, output, resource, and isolation
  arguments because scheduler feedback is slow;
- establish the accepted-container registration and storage pattern once for
  all campaigns;
- establish Pixi discovery once for each shell class because every command
  depends on it.

Use a tiny scheduler job only when documentation and rendered-script inspection
cannot settle compatibility. Do not bypass BABS to test every primitive as a
matter of course.

### 4. Separate authoring and execution transactions

Environment, code, task, image, pipeline, cluster, and campaign changes are
authoring. They may be developed together only as a coherent change that is
validated and committed before execution uses it.

Use this commit cadence:

1. Commit the Pixi release/bootstrap, manifest, lock, tasks, and focused tests
   before using the environment for a campaign.
2. Commit selected inputs and container pointers with pipeline, cluster, and
   campaign configuration before BABS initialization.
3. After initialization creates an attempt and operations state, commit the
   child datasets and root composition before submission.
4. After submission, merge, finalization, validation, acceptance, or a retained
   failure changes durable state, checkpoint it before the next dependent
   action.

Read-only inspection needs no commit. Disposable debugging needs no commit when
its state is quarantined and cannot become evidence. Status polling should be
read-only or summarized at a meaningful transition, not produce a root commit
for every poll.

Each execution record should name the pre-execution root commit. That one
identity composes the committed setup, Pixi manifest and lock, launchers,
configuration, and nested datasets without repeating them in every log. A
locked environment used from a dirty checkout is not an adequate environment
identity.

## Decisions from this review

1. Carry the small BABS direct-layout checker workaround as known technical
   debt until upstream removes the need for it. Do not turn it into a large
   recurring procedure.
2. Keep post-merge extraction and derivative finalization under project
   control. Expose one concise Pixi entry point and provenance-capture the
   actual content transformation with DataLad.
3. Adopt BABS's MD5E annex backend project-wide. Stop migrating campaign
   content to SHA256E. OCI digests or upstream checksums may remain source
   metadata without creating a second annex-backend policy.
4. Use one accepted-container DataLad dataset with a GitHub Git sibling backed
   by a GIN annex-storage sibling. Do not create a storage arrangement per
   image or campaign.
5. An ignored local `.env` may provide a token for GIN setup or publication.
   The publication task must load only the needed variables and must not pass
   the token into BABS, Slurm, containers, con-duct logs, or provenance.
6. Retain FreeSurfer when it is part of the intended fMRIPrep campaign. Do not
   simplify scientifically relevant work to optimize archive extraction;
   improve extraction at its own boundary.
7. The earlier `.bidsignore` question was about preventing operational
   provenance directories from being hidden merely to satisfy BIDS validation.
   That is a validator implementation detail, not a skill-level question. The
   concise rule is that `.bidsignore` describes payload exceptions and must not
   conceal provenance.

## Implications for the skill

Do not add the Phase 3 failure catalog to the skill. Add a short set of
operating invariants instead:

- plain Pixi works before project operations begin;
- tools are used at the native boundaries above;
- rendered interfaces are inspected before slow scheduler feedback;
- campaign execution never crosses uncommitted environment or configuration
  changes;
- retained child state and root composition are checkpointed before the next
  dependent action;
- containers use one declared registry and publication pattern;
- known BABS compatibility debt remains bounded and removable.

One compact pre-execution check should enforce the transaction rule by rejecting
a dirty environment/configuration or a root that does not compose the selected
children. It should report the root commit and a short reason, not emit a large
identity inventory on every command.

This review does not judge the Phase 3 outputs. Work executed across the dirty
authoring state cannot acquire a missing pre-execution root identity through a
later consolidated commit.
