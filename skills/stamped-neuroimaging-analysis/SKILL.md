---
name: stamped-neuroimaging-analysis
description: Create, execute, debug, assess, and release ideal-oriented STAMPED neuroimaging research objects using BIDS Study datasets, DataLad and DataLad Containers, Pixi, Apptainer or Singularity, BABS, Slurm, and explicit campaign management. Use for public or controlled-data work whenever component identity, committed execution state, provenance, portability, or persistent retrieval matters.
---

# Run a STAMPED neuroimaging analysis

Use the maintained STAMPED paper
[`main.tex`](https://github.com/stamped-principles/stamped-paper/blob/main/main.tex)
as the normative source. Pursue each ideal where practical, but report STAMPED
as a component-by-component spectrum rather than a binary label.

Distinguish these instruction classes:

- **STAMPED requirement:** Enforce every MUST, decide every applicable SHOULD,
  and support relevant MAY choices without making them requirements.
- **Implementation rule:** Follow the BIDS, DataLad, Pixi, SIF, BABS, and Slurm
  conventions below for this class of neuroimaging research object.
- **Hardening:** Record a decision when useful; do not call it a STAMPED
  requirement unless the paper does.

## Apply the operating invariants

1. Make plain `pixi` a prerequisite. Confirm that shell initialization exposes
   the declared Pixi version and that `pixi run --locked ...` discovers the
   project. If it does not, diagnose and fix shell setup before project work.
   Never substitute an absolute Pixi path, private environment `bin` path, or
   recurring `PATH` injection.
2. Separate authoring from execution. Commit coherent environment, code,
   image, pipeline, cluster, and campaign changes before using them. Checkpoint
   every retained transition before starting work that depends on it.
3. Let one root commit identify the pre-execution composition. It must compose
   the selected inputs, configuration, operations state, and registered SIF;
   an environment lock used from a dirty checkout is not an execution identity.
4. Preserve the actual scientific or lifecycle command. A Pixi task is a
   concise entry point, not execution evidence. Use DataLad/BABS records and
   exact component versions as evidence.
5. Inspect interfaces whose mistakes have slow or costly feedback: the
   resolved BABS configuration, generated participant command, Slurm request,
   container binds/isolation, inclusion, and output contract. Do this before a
   pilot or scale-up; do not expand it into a catalog of primitive probes.
6. Assess the root and every execution-essential component. Roll component
   gaps up and keep restricted or unmet ideals visible.

Before defining or changing a component boundary, planning an assessment,
accepting a derivative, or releasing a research object, read
[references/assessment.md](references/assessment.md) completely.
Before any operation that creates retained campaign, scheduler, provenance,
dataset, or result state, read
[references/execution-transactions.md](references/execution-transactions.md)
completely.

## Use each tool at its native boundary

| Tool | Authority |
|---|---|
| Pixi | Locked user-space environments and concise typed project entry points |
| DataLad/git-annex | Dataset identity, composition, content availability, and modification provenance |
| DataLad Containers | Exact registered-container execution and scientific run records |
| BABS | Participant/session expansion, Slurm submission, RIA state, status/retry, and merge |
| Apptainer/Singularity | Execution of the declared SIF with explicit isolation and binds |
| Slurm | Durable compute independent of the browser or interactive shell |
| BIDS | Study, raw, and derivative dataset semantics and metadata |

Use `datalad run` or `datalad containers-run` for content transformations and
`datalad save` for authored structure, metadata, and operational records. Do
not wrap `pixi run <task>` inside a DataLad run record. Pixi may compose explicit
DataLad or BABS leaf commands, but every result-changing leaf must remain
visible and independently attributable. Do not enable Pixi input/output caching
for result-changing tasks.

## Compose the research object

Make the root a DataLad superdataset, not a BIDS dataset. Keep these independent
boundaries:

```text
config/                         # dataset, pipeline, cluster, and campaign intent
envs/                           # committed Pixi manifest/lock and container records
envs/containers/accepted/       # one exact-SIF DataLad registry
studies/<study>/                # BIDS Study dataset
  sourcedata/raw/               # independent raw BIDS dataset
  derivatives/<attempt>/        # independent derivative/BABS dataset
operations/<campaign>/          # campaign state and lifecycle provenance
results/<analysis>/             # genuinely multi-study derivatives
result-manifest.tsv             # authoritative result-to-provenance index
```

Give each boundary a stable DataLad/Git identity, license decision, access
class, and declared retrieval location. Compose exact child commits at the root
and verify promised retrieval from a fresh recursive clone. Treat a controlled
component that others cannot retrieve as a visible D.1 restriction, not an
exemption.

Use one declared annex-backend policy across project-created datasets. This
project selects MD5E for BABS compatibility. Perform the switch from an earlier
backend as a focused authoring transaction; migrate current authoritative
content and configuration together while preserving historical keys in old
records.

Use one accepted-container dataset and one publication pattern. For this
project, publish its Git history through GitHub and annex content through a GIN
storage sibling. Do not create a new registry or storage arrangement per image
or campaign. Never mark D.1 met until exact SIF retrieval has been demonstrated.

## Define environments and runtimes explicitly

Keep the Pixi manifest and lock under `envs/`, with root discovery links. Change
them only in a dependency-authoring transaction; use `pixi run --locked ...`
for ordinary work. Declare the Pixi release/bootstrap and any host-provided
Apptainer, Slurm, kernel, filesystem, or accelerator interface.

Build project-authored SIFs as thin isolation wrappers around an appropriate
locked Pixi environment. Still identify result-producing execution by the exact
registered SIF content, not by the Pixi lock. For external apps, pin and qualify
the exact SIF, application interface, architecture, terms, and retrieval path.

Register every accepted image through DataLad Containers' conventional
`.datalad/environments/<name>/image` layout. Quarantine candidate-image output;
register the image and regenerate before retaining, merging, comparing, or
releasing that output.

Run retained computation with fresh work, output, scratch, home, and cache
locations; explicit read-only inputs/configuration; only required writable
binds; no inherited host home or undeclared working directory; and no network
unless declared. Record unavoidable host interfaces rather than hiding them.

## Preserve scientific and BIDS boundaries

Follow the project's pinned BIDS Study convention; this project pins BIDS
1.11.1. Validate Study, raw, and accepted derivative roots independently with
the Deno BIDS Validator used by project tasks.

Implement project-authored BIDS-facing programs as tested BIDS Apps with the
repository's BIDS App builder skill, the standard positional interface, and
explicit participant selection, operation, parameters, outputs, seeds, and
failure behavior. Keep notebooks non-authority. Record each independently
meaningful result-changing boundary as its own DataLad Containers execution.
Give derivatives complete `DatasetType`, `GeneratedBy`, and placement-independent
`SourceDatasets` metadata.

Point BABS at `sourcedata/raw/` and use direct layout with `analysis_path: "."`.
Keep one dataset identity from BABS initialization through in-place
finalization and accepted derivative status. Preserve BABS-generated code,
archives, logs, and RIA material as operational evidence; never edit generated
code to change science.

Keep post-merge finalization project-controlled and provenance-captured in the
same attempt dataset. Use `datalad add-archive-content`, or a tracked
`unzip`/extraction script followed by the appropriate DataLad record, while
preserving source archives. Use an optional BABS archive helper only after its
pinned release is qualified. Do not copy the payload into another derivative or
hide operational provenance with `.bidsignore`.

## Run campaigns deliberately

Create one operations dataset for each dataset × pipeline/runtime × input
condition × cluster campaign. Resolve exact input, configuration, SIF, tool,
resource, access, and output identities before initialization. Give every
attempt a stable identity; make a new attempt or campaign when scientific state
changes.

Pilot one participant/session. Review the generated command, Slurm interface,
isolation, inclusion, outputs, and run record before submitting a bounded
batch. Keep requested inclusion, realized inclusion, exclusions, and runtime
failures distinct. Advance initialization, submission, status/retry, merge,
finalization, validation, and acceptance as explicit retained transitions.

Keep the reviewed BABS direct-layout checker workaround and project-owned
archive finalization as small, named compatibility debts. Put their upstream
reproducer/issue and removal condition in project documentation; do not spread
their workarounds across tasks or campaign configurations.

## Protect controlled data and credentials

Separate public and controlled datasets, siblings, logs, derivatives, and
publication tests. Stage authenticated retrieval before computation and do not
pass credentials into BABS, Slurm, containers, logs, or provenance. Decide
input access and derivative redistribution independently.

Permit an ignored root `.env` only as a declared local input to the narrow task
that needs it, loaded through a locked dependency. Keep a non-secret
`.env.example`; never commit the real file or treat credentials as part of the
reproducible research object.

## Accept and release evidence, not intent

Accept a result only when its exact dataset commit resolves to actual command
provenance, inputs, configuration, registered SIF, output, validation, and an
executable reproduction entry point in `result-manifest.tsv`. Preserve the same
derivative identity through finalization and acceptance.

Verify recursive retrieval, exact SIF availability, representative replay,
BIDS validity, access separation, license compatibility, result-manifest
resolution, and current component/root STAMPED assessments. Publish the
principle-by-principle achievements and gaps; never scale a campaign to conceal
an unresolved pilot failure.
