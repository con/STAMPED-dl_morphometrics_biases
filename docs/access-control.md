# Access classes and sibling boundaries

`config/access/data-classes.tsv` is the authority for content classes, and
`config/access/sibling-matrix.tsv` is the authority for allowed publication
flows. The current GitHub and GIN siblings remain public. GitHub stores Git
metadata only (`remote.origin.annex-ignore=true`); GIN provides public Git and
annex storage for content that has passed public distribution review.

## Controlled-data composition

A future controlled Study, its raw input, participant-level attempts, logs, and
operations records use independent private datasets and private storage siblings.
The top-level research object may identify their stable component and authorized
retrieval procedure without publishing credentials, participant metadata, or
prohibited endpoint details. Authorized retrieval is staged before scientific
execution; credentials never enter the research object or a SIF.

Input access never implies derivative redistribution. Participant-level
derivatives and logs remain private until an independent policy review permits a
specific class. Approved aggregate outputs cross into a separate
disclosure-reviewed release dataset; they are not pushed directly from a private
attempt.

Arbitrary third parties cannot retrieve controlled components, so their D.1
status and the root roll-up remain `restricted`. This disclosed gap does not
block public code, public pilot data, permitted aggregates, or other distributable
modules.

## Publication guard

The locked `validate-publication-boundary` task creates independent synthetic
public and protected git-annex repositories, performs a credential-free local
public push and clone, and proves that protected input, identifier, log, and
derivative paths, markers, annex keys, and remote names are absent from all
public Git refs and public annex storage. The simulation contains no real
participant or controlled data.

Before any real controlled campaign, the same class checks must be applied to
the actual public sibling from a credential-free environment. Any uncertain
input, log, derivative, identifier, or metadata field stops publication pending
a policy decision.
