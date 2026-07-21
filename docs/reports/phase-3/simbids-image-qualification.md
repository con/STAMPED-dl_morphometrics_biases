# SimBIDS 0.0.3 image qualification

Date: 2026-07-21

This is an engineering qualification fixture, not a scientific-runtime
acceptance. It records the exact OCI-to-SIF conversion used by the Phase 3
BABS campaign and the remaining publication and hardening gaps.

| Identity | Value |
|---|---|
| Source | `docker://pennlinc/simbids:0.0.3` |
| Resolved OCI digest | `sha256:3646a27a974f006585201fb1f5237e9c61abc704903c6c282878be81e86687ee` |
| SimBIDS version | `0.1.dev27+g1a8efa3` |
| Conversion tool | DataLad Containers 1.2.5 with Apptainer 1.5.2 |
| Accepted dataset | `8320f911-d110-4c82-b95b-285244cbae13` at `eef3a2edf20c2d3a6ad0cb350aab72fbb5a0725d` |
| Conventional registration | `.datalad/environments/simbids-0-0-3/image` |
| SIF annex key | `SHA256E-s344264704--244af4c6e1708dc10dd1f89f28951c9efa1c01571de778449ed4593ef8e9bbea` |
| SIF SHA-256 | `244af4c6e1708dc10dd1f89f28951c9efa1c01571de778449ed4593ef8e9bbea` |

The image was registered with `datalad containers-add`, not by manually
constructing DataLad configuration. Apptainer inspection records the source
tag, resolved base digest, `amd64` architecture, and Apptainer 1.5.2 builder.
The locked Pixi manifest and lock used for qualification have SHA-256 values
`7f8b6507a4c46b4e5fa1d7b29c9a88751a6b602e7dd4f9bbc6531315930baf7b`
and `0234d4cf48b92db96fdca068baa600b136330579594683a3df6c5eb00aec3dc5`.

## Interface

Pass. BABS resolved the conventional DataLad Containers registration and the
exact SIF ran as a BIDS App for three subjects in Slurm array job `62027866`.
All three tasks exited `0:0`, BABS reported three done and zero failed, and the
three result branches merged.

## Containment

Pass for this synthetic fixture. The generated command used `--containall`, a
writable temporary filesystem, disabled container networking, and bound the
job worktree. This is evidence for the declared fixture boundary, not a general
security certification of the image.

## Fixture

Pass. The SIF consumed three synthetic raw BIDS participants and produced one
archive per participant. After extraction and metadata finalization, the Deno
BIDS validator 3.0.0 found 86 payload files, three subjects, no errors, and six
reviewed `NIFTI_UNIT` warnings. The accepted derivative is DataLad dataset
`fcdddd73-613b-4ebd-b316-bcbce388099b` at
`7f5ea5f8b9784a121c67bc508ecba89b344fe629`.

## Target architecture

Pass. Apptainer inspection reports build architecture `amd64`, matching the
Unity Linux x86-64 execution host, and all three jobs completed there.

## Persistent retrieval

Pending. The exact SIF is present in the local accepted-container dataset and
its key and bytes verify, but no independently persistent annex location has
been published for this 344,264,704-byte object. The image record therefore has
an empty `retrieval_locations` list. Do not infer public retrievability from the
OCI tag: the converted SIF bytes are the execution identity.

## Remaining limitations

- The SimBIDS Python package reports Apache-2.0, but the complete bundled OCI
  dependency license set has not been resolved.
- No SBOM, project signature, or signed conversion attestation exists.
- This image simulates fMRIPrep-shaped output and cannot support a scientific
  result claim.
