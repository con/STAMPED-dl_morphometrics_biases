# Phase 1 implementation notes

## Scope and starting point

Phase 1 starts from the accepted Phase 0 state at root commit `c4d37a6`.
Phase 0 evidence, target declarations, unresolved runtime identities, and scientific
gaps are not being recreated or reinterpreted. Historical scientific code remains
outside this research object.

The pre-change audit found:

- a clean top-level DataLad dataset with ID
  `baa2ec91-e618-4bac-b382-ac0daf9f779a`, repository version 10, and SHA256E
  annex policy;
- intact GitHub `origin` and GIN Git/annex siblings, including the public poster
  annex content;
- a locked Pixi 0.66.0 bootstrap environment with DataLad 1.6.0,
  DataLad Containers 1.2.5, and the declared host git-annex 10.20260420;
- passing Phase 0 and structural STAMPED validators, with the ideal validator
  correctly expected to fail;
- complete repository-local copies of both policy skill bundles; and
- no existing subdatasets or Phase 1 skeleton, toy Study, licensing policy,
  access matrix, campaign schemas, publication-boundary test, or Phase 1 gate
  evidence.

The audit commands used the locked `datalad` Pixi environment. The saved Phase 1
reports will supersede this prose as machine-readable evidence.

## Implementation sequence

1. Add a narrowly scoped locked Phase 1 quality environment without performing
   the broader Phase 2 environment design.
2. Establish the canonical directory and authority pattern without placeholder
   derivatives or premature runtime datasets.
3. Create an empty toy BIDS 1.11.1 Study and an independent raw BIDS/DataLad
   child with text-friendly SHA256E policies.
4. Define and test campaign, operations-event, image-record, and result-manifest
   schemas.
5. Define the public/private sibling matrix and prove it with a local,
   credential-free publication simulation.
6. Add a REUSE file-group policy and license texts.
7. Review `babs_demo` and MechaBABS as pinned design references only.
8. Update the component inventory and STAMPED assessment with actual evidence.
9. Run the Phase 1 exit gate, including independent BIDS validation, clean
   recursive clone checks, DataLad/annex reports, REUSE lint, schema tests,
   positive and negative STAMPED validation, and publication-boundary checks.

## Explicit Phase 1 decisions

- **Root identity:** keep the existing DataLad root and history. It remains a
  research-object superdataset, not a BIDS dataset or a BIDS “super-study.”
- **Sibling preservation:** do not rename, remove, or repurpose `origin`, `gin`,
  or the GIN annex common-data-source configuration.
- **Tool boundary:** add only tools needed to prove the Phase 1 gate. Complete
  development, analysis, BABS, and image-authoring environments remain Phase 2.
- **BIDS validator identity:** use the locked `bids-validator-deno` distribution
  metadata (`3.0.0`) as the tool version. Its compiled CLI incorrectly renders
  the current working repository commit for `--version`, so that banner is not
  accepted as tool identity. Every invocation sets the official BIDS 1.11.1
  schema URL (`https://bids-specification.readthedocs.io/en/v1.11.1/schema.json`)
  because the compiled CLI normalizes an explicit schema tag before its loader
  receives it.
- **Toy boundary:** `studies/toy/` is an independent Study dataset and
  `studies/toy/sourcedata/raw/` is an independent raw BIDS dataset. No derivative
  dataset is created until a producing operation exists.
- **Empty raw fixture:** the raw child contains only BIDS metadata and
  documentation. Any validator warning caused solely by having no participant
  data is reviewed and recorded rather than hidden with fake scans.
- **Operations boundary:** `operations/` contains only independent campaign
  datasets created for real campaigns. Phase 1 defines their contract but does
  not create a placeholder campaign dataset.
- **Container boundary:** `envs/containers/repronim/` and
  `envs/containers/accepted/` are reserved paths, not initialized datasets in
  Phase 1. Their identities and registry are Phase 2 work.
- **Access design:** controlled inputs, identifiers, participant-level logs, and
  controlled derivatives belong to separate private datasets and siblings.
  Public roots may contain only non-sensitive policy and opaque component IDs;
  disclosure-reviewed aggregates get a separate release boundary.
- **Project licensing:** the repository owner selected MIT for project-authored
  Phase 1 code, documentation, configuration, schemas, and toy metadata. This
  grant does not relicense the historical repository or external components.
- **Historical federal work:** the repository owner reports that the original
  study is a U.S. Government work and will add a scoped public-domain/CC0 notice
  to the original work separately. Until that exact commit and scope exist, the
  historical repository retains its recorded no-license gap here.
- **Design references:** borrow campaign axes, explicit pins, immutable attempt
  identities, desired/observed state, resumable transitions, and inclusion
  accounting only when they preserve the fixed Study/raw/derivative and
  operations boundaries. Do not install or invoke MechaBABS.

## Decisions intentionally deferred

- Image registry identities and scientific SIF selection (Phase 2 and Phase 5).
- A real BABS attempt and operations dataset (Phase 3).
- Scientific app boundaries and imported historical code (Phase 4).
- ABCD release, DUC, cohort, and derivative-distribution policy (Phase 7).

## Phase 1 checkpoint and assessment

The first Phase 1 foundation checkpoint is root commit
`1b81cde8de1ff18b64efcd7a122e1c357cb0444b`; it registers the Study dataset
without rewriting Phase 0 history. The child Study and raw datasets retain
separate DataLad identities and histories. The final Phase 1 evidence reports
are generated from a committed root state and then committed as evidence, so a
clean recursive clone can independently inspect the registered hierarchy.

The assessment now distinguishes project-controlled MIT material from the
historical repository and poster evidence. The poster has a repository-local
`LicenseRef` describing the limited recorded redistribution authorization; this
does not convert it to MIT, CC0, or a broad public-domain grant. The original
federal-work notice remains intentionally out of scope until it exists with a
specific source commit and scope.
