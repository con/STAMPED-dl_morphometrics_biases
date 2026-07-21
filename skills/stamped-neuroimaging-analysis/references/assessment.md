# Assess and release a STAMPED research object

Read the maintained STAMPED paper `main.tex` when interpreting a requirement.
Treat this matrix as a routing summary, not a replacement for the normative
source.

| ID | Level | Criterion |
|---|---|---|
| S.1 | MUST | Reach every execution-essential component through one top-level research object without implicit lookup. |
| S.2 | MUST | Retrieve license declarations with the components they govern. |
| T.1 | MUST | Give every component a persistent content identity. |
| T.2 | SHOULD | Use the same compatible content-addressed version-control system across components. |
| T.3 | MUST | Record provenance for every modification. |
| T.4-programmatic | SHOULD | Capture code-driven provenance programmatically. |
| T.4-versions | MUST | Identify every component version involved in code-driven provenance. |
| A.1 | MUST | Provide unambiguous instructions sufficient to reproduce every computational result. |
| A.2 | SHOULD | Express procedures as executable specifications. |
| M.1 | SHOULD | Give components independent, composable boundaries. |
| M.2 | MAY | Store components directly or link them as subdatasets. |
| M.3 | SHOULD | Declare module licenses independently and check compatibility at composition boundaries. |
| P.1 | MUST | Use no undocumented host state. |
| P.2 | MUST | Specify computational environments explicitly. |
| P.3 | MUST | Version-control environment definitions. |
| E.1 | SHOULD | Produce results in newly created, disposable execution environments. |
| D.1 | MUST | Keep referenced components persistently retrievable by others. |
| D.2 | SHOULD | Make environment specifications support reproducible builds. |
| D.3 | SHOULD | Give each module an explicit, resolvable license. |

## Maintain the assessment

Create `config/stamped-assessment.tsv` before execution with at least:

```text
subject_id  parent_id  subject_kind  requirement_id  level  decision  status  evidence  limitation
```

- Inventory the root and every execution-essential code, configuration, input,
  derivative, container, environment, model, license, result, and operations
  component. Give each a stable ID and parent.
- Use `met`, `partial`, `unmet`, `restricted`, or `not-applicable`. Never let
  `partial` satisfy a MUST.
- Set MUST decisions to `adopt`. Require committed evidence for `met`; report
  legal, ethical, access, or external limits as `restricted` or `unmet`.
- Set each applicable SHOULD to `adopt`, `defer`, or `decline` with a rationale
  and, for deferral, a reopening condition. Add MAY rows only when useful.
- Use actual committed identities, validation reports, publication evidence,
  and run records. Never use a planned command as execution evidence.
- Roll a component gap up to every dependent aggregate. Do not assign the root
  a stronger status than a component it needs.
- Reassess with the committed state after dependency or component changes,
  retained campaigns, derivative acceptance, and release preparation.

Expose `validate-stamped` as the structural check for subjects, decisions,
statuses, evidence, and roll-ups. Expose `validate-stamped-ideal` as the honest
report of every applicable MUST not met and every SHOULD not adopted and met.

## Verify acceptance and release

Require evidence that:

- a fresh recursive clone retrieves every permitted component or provides the
  exact authorized procedure and visible D.1 restriction;
- each result resolves through `result-manifest.tsv` to its dataset commit,
  run record, exact inputs, configuration, registered SIF, output, and
  reproduction entry point;
- Study, raw, and derivative roots validate independently with the project's
  pinned BIDS specification and Deno validator, or carry a reviewed upstream
  exception;
- controlled content, credentials, prohibited metadata, and participant-level
  logs cannot reach public siblings;
- licenses and data-use terms are compatible at each composition boundary;
- representative historical replay and clean-room container execution pass
  the declared fixture and domain checks.

Publish the seven-principle assessment with scope, component roll-up, evidence,
controlled-access limitations, and remaining gaps. Never describe a restricted
or unmet MUST as achieved.
