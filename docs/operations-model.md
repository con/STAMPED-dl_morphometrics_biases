# Campaign and operations model

The prospective campaign configuration and resolved operations history have
separate authorities:

- `config/campaigns/` composes exact dataset, pipeline/SIF, input-condition, and
  cluster-profile identities before initialization.
- `operations/<campaign>/` is an independent DataLad dataset holding the resolved
  campaign snapshot, desired and observed state, inclusion accounting, and
  append-only lifecycle events.
- `studies/<study>/derivatives/<pipeline>-<variant>-attempt-<N>/` is the one BABS
  project, analysis dataset, and provisional derivative. The operations dataset
  points to it and never contains, copies, or replaces it.

## Required campaign record

`config/schemas/campaign.schema.json` requires the exact Study and raw DataLad
IDs and commits; requested-inclusion identity; pipeline configuration and exact
accepted SIF identities; cluster profile and declared host interfaces; immutable
attempt and operations dataset IDs; resources; outputs; retry policy; and access
class. A scientific input, configuration, or SIF change requires a new campaign
or variant, not a retry.

## Append-only commands ledger

Every `commands.jsonl` line conforms to
`config/schemas/operations-event.schema.json`. Events use contiguous sequence
numbers beginning at 1. The first event has a null `previous_event_sha256`; every
later event stores the SHA-256 of the preceding exact UTF-8 JSON line, excluding
the newline. This detects replacement, reordering, or truncation when the ledger
is validated against its committed history.

The literal expanded argv, relevant tool versions, actor, timestamp, desired and
observed state, evidence paths, attempt identity, and access class are mandatory.
Initialization, setup checks, pilot, submission, status, retry decisions, merge,
finalization, validation, and acceptance are separate event types. Secrets,
credentials, and prohibited participant metadata never belong in the ledger.

## Inclusion accounting

Requested inclusion is an immutable campaign input. BABS-realized inclusion,
eligibility exclusions, missing-input exclusions, runtime failures, retry
decisions, and accepted outputs are distinct observed records. A retry does not
overwrite an attempt, and an acceptance event identifies one exact derivative
dataset ID and commit after in-place provenance-captured finalization.
