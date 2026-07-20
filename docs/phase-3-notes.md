# Phase 3 toy BABS proof

The accepted direct-layout derivative is
`studies/toy/derivatives/toy-bids-app-synthetic-attempt-003/`, DataLad dataset
`44bd0b3a-e03d-46bf-b0dc-a5e47bdb95c7`, commit
`bef0f2f585e3dcb02ff9101b4eef2850592e1f89`. The separate operations dataset
is `operations/toy-bids-app-synthetic/`, dataset
`e329577a-ae6b-454c-8a76-50ab1530c0a3`.

Attempt 001 demonstrated that Unity rejects BABS's generic Slurm `--tmp`
request. Attempt 002 reached the exact container but exposed a wrapper output
directory mismatch. Attempt 003 used allocated workspace scratch and
`all_results_in_one_zip: true`; Slurm job `61988356` completed, BABS status
reported one done and zero failed, and merge succeeded. Every attempt has a
separate immutable DataLad identity and its decision/evidence remains in the
operations ledger.

The participant command used `--cleanenv`, `--containall`, `--no-home`, disabled
default home/cwd mounts and container networking, and bound only the declared
job worktree. Host-side DataLad used GitHub to obtain the public raw subdataset;
the container itself had no network. Job-scoped scratch was removed by the
generated cleanup trap.

The pinned BABS check-setup implementation still assumes legacy `inputs/data`
and its `babs-unzip` entry point raises an import error. These failures are
retained. Finalization therefore ran as a tracked `datalad run` in the same
attempt dataset. The visible BABS `containers/` directory is covered by an
explicit, reviewed `.bidsignore` exception; independent BIDS validation then
passed with only the expected empty-toy subject/author warnings.

A clean recursive clone from the public Study sibling reproduced the accepted
dataset ID and commit and retrieved both payload and archive. Their annex keys
also have public GitHub release URLs, independent of the in-place output RIA.
