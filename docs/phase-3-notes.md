# Phase 3 BABS qualification

The current accepted engineering qualification is
`studies/simbids/derivatives/simbids-fmriprep-three-subject-attempt-001/`,
DataLad dataset `fcdddd73-613b-4ebd-b316-bcbce388099b`, commit
`7f5ea5f8b9784a121c67bc508ecba89b344fe629`. Its separate operations dataset is
`operations/simbids-fmriprep-three-subject/`, dataset
`dbe5af58-7254-4f4e-a19a-fff32e1911a0`.

The campaign used a three-subject raw BIDS fixture generated with SimBIDS and
the exact SimBIDS 0.0.3 SIF registered through `datalad containers-add` at
`.datalad/environments/simbids-0-0-3/image`. Slurm array job `62027866` ran all
three tasks concurrently; every task exited `0:0`, BABS reported three done and
zero failed, and merge succeeded. The final archives and extracted payload use
SHA256E annex keys and are available from the output RIA.

Operator commands use short, locked Pixi tasks. The noninteractive Bash startup
path now exposes `pixi` before `.bashrc` returns, and the generated batch script
activates the locked `babs` environment with `pixi shell-hook`. There is no
absolute environment-bin `PATH`, host `HOME`, or cache override in the campaign.
The repository-root `.env` contract is implemented with locked
`python-dotenv`; it is intentionally not a credential store.

BABS direct layout correctly installed raw data at `sourcedata/raw`. The pinned
checker still has its upstream `inputs/data` assertion, so a temporary tracked
alias was added only for the official `babs check-setup --job-test`, then
removed and synchronized before submission. Checker job `62027613` passed. The
accepted derivative has no `inputs/` compatibility tree.

The stale `babs-unzip` entry point was not used. DataLad
`add-archive-content` was functionally correct but inefficient for thousands of
small synthetic files on Unity, so the selected policy was plain unzip followed
by one DataLad save. Metadata finalization ran under `datalad run`; archives
were retained. Deno BIDS Validator 3.0.0 then found 86 payload files, three
subjects, no errors, and six reviewed synthetic `NIFTI_UNIT` warnings. BABS
operational paths are excluded structurally from that payload view; the narrow
`.bidsignore` names only non-standard fMRIPrep payload extensions.

The earlier toy attempts remain historical evidence in
`operations/toy-bids-app-synthetic/`. They discovered Unity's unsupported
generic `--tmp` directive, the toy wrapper-directory contract, the stale unzip
entry point, and the checker inconsistency. The new SimBIDS campaign is the
active Phase 3 qualification, but remains non-scientific. The exact SimBIDS SIF
still needs independent persistent publication before a fresh clone can be
claimed to retrieve it without this local registry.
