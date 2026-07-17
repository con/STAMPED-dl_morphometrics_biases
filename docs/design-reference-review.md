# Phase 1 BABS design-reference review

This review is bounded by the repository organization fixed in the conversion
plan and STAMPED skill. It adopts design patterns, not dependencies or layouts.

## Exact references inspected

| Reference | Identity | Role |
|---|---|---|
| `djarecka/babs_demo` | `7d46f3763cbf8f76b17e5f345160a07d042446e8` | Local clean checkout of the BIDS Study-layout merge, inspected on 2026-07-17. |
| `asmacdo/mechababs` | `4a4deb8f01c8837a5481d497140a3bb41c450f09` | Clean shallow upstream checkout inspected on 2026-07-17; not installed or invoked. |
| `PennLINC/babs` direct-layout minimum | `2cc536a51282124f3811ffa971f82a7c34116af5` | Minimum revision named by project policy; qualification remains Phase 2/3 work. |

`babs_demo` declares unpinned `babs`, `con-duct`, `git-annex`, and `datalad`
requirements, so its checkout identifies the demo text but not a result runtime.
MechaBABS is an evolving design reference and does not become part of this
research object by being reviewed.

## Adopted patterns

- Compose one exact dataset axis, pipeline/SIF axis, input-condition axis, and
  cluster axis before campaign initialization.
- Keep pipeline science and cluster/site policy in separate configuration
  authorities, then save the exact resolved composition.
- Use BABS direct Study layout with `analysis_path: "."`, raw input at
  `sourcedata/raw/`, and RIA state under `.babs/`.
- Make the BABS project root, DataLad analysis dataset, and provisional
  derivative one identity from initialization through acceptance.
- Allocate immutable `attempt-<N>` identities at creation; never overwrite a
  failed attempt or disguise a scientific change as a retry.
- Pin the exact code/tool identity and refuse execution when the realized tool
  differs from the recorded pin.
- Keep desired and observed state separate, advance through small resumable
  transitions, and reconcile observations from BABS/RIA evidence.
- Preserve requested inclusion independently from BABS-realized inclusion, and
  account separately for eligibility, missing inputs, runtime failures, retries,
  and accepted outputs.
- Retain generated BABS configuration, code, wrappers, logs, archives, and RIA
  state as operational evidence while keeping them distinct from the declared
  scientific payload.
- Provide dry-run behavior for lifecycle mutations, but record actual literal
  argv, versions, before/after state, and evidence for every executed transition.

## Rejected or replaced patterns

- **Campaign contains inputs and derivatives:** MechaBABS's self-contained
  campaign root conflicts with the fixed boundary. Here the operations dataset
  is separate and only points to the Study's BABS attempt.
- **URL as dataset identity:** a URL is a retrieval location, not sufficient
  identity. Campaigns require DataLad IDs and exact commits.
- **Branch or tag as code pin:** mutable names are insufficient. Exact commits
  are required even when a branch/tag is used for retrieval.
- **Campaign-local `uv` virtual environment:** user-space orchestration comes
  from the reviewed Pixi lock; result-producing dependencies come from the exact
  registered SIF.
- **Deleting or rewriting a state ledger to reset:** lifecycle events are
  append-only and hash-chained. A reset creates a new attempt or campaign.
- **Derived state without literal event history:** re-derivable summaries are
  useful, but they do not replace command and transition meta-provenance.
- **Moving or copying accepted output elsewhere:** the direct attempt dataset is
  finalized and accepted in place without a second derivative identity.
- **Placeholder derivative directory:** `babs_demo` creates
  `derivatives/.gitkeep`; this project creates no derivative dataset or placeholder
  before its producing operation exists.
- **Unpinned host environment, mutable OCI build, or path-only SIF reference:**
  these do not meet the locked-tooling and exact-image gates.
- **Shell-generated authoritative configuration and implicit environment files:**
  resolved configurations are schema-validated tracked records with explicit
  hashes and access class.
- **Manual lifecycle steps without a ledger:** every initialization, check,
  pilot, submission, status/retry, merge, finalization, validation, and acceptance
  action receives an operations event.
- **Home access, inherited working directory, or undeclared host paths:** later
  BABS qualification must prove clean containment, fresh home/cache/scratch, and
  reviewed binds.
- **Ignoring BABS's visible `containers/` directory during BIDS validation:** the
  exact derivative layout remains a hard gate requiring an upstream fix or a
  reviewed exception.

## Phase 3 follow-up

The toy campaign must test these adopted patterns against the pinned direct-layout
BABS revision. This review is design evidence only: it does not qualify BABS,
MechaBABS, the demo's SIMBIDS image, a Slurm profile, or any scientific runtime.
