---
name: unity-hpc-operations
description: Operate safely and efficiently on the Unity HPC cluster. Use for any task that plans, configures, executes, monitors, troubleshoots, or documents work on Unity, especially storage placement, scratch workspaces, quota management, software environments and caches, Slurm jobs, resource requests, data staging, and persistent operational state.
---

# Operate on Unity HPC

Treat Unity as a managed, shared HPC system. Resolve storage, compute, account,
and data-lifecycle choices before writing files or launching work. Prefer the
current [Unity documentation](https://docs.unityhpc.org/documentation/) over
remembered cluster details; cluster policy, partitions, quotas, and paths can
change.

## Establish the operating context

Before changing state:

1. Confirm that the host is Unity and identify whether the session is on a
   login or compute node.
2. Identify the user, PI account/group, project access class, expected data
   volume, I/O pattern, runtime, and required retention period.
3. Inspect the candidate filesystem and quota rather than inferring them from a
   path name. Use read-only checks such as `df -h <path>`, `du -sh <path>`,
   `squota`, and `ws_list -v` as applicable.
4. Resolve explicit source, active-work, scratch, output, log, cache, and archive
   paths. Do not proceed with guessed PI, project, or scratch paths.
5. Check the current Unity pages relevant to the operation when the action is
   costly, destructive, long-running, or depends on a current partition,
   feature, quota, retention, or snapshot rule.

## Select storage by purpose

Apply the [Unity storage policy](https://docs.unityhpc.org/documentation/cluster_specs/storage/):

| Location | Use | Operational rule |
|---|---|---|
| `/home/<user>` | Small shell startup files and user configuration | Keep active data, large repositories, environments, caches, and job I/O elsewhere. |
| `/work/pi_<PI>/...` | Active projects, job I/O, environments, durable logs, and working state shared with the PI group | Use as the primary persistent work location; verify group and permissions before writing. |
| `/project/...` | Large, persistent, warm or inactive data | Stage active subsets into `/work` or scratch; do not use for job I/O. |
| `/scratch/workspace/...` | High-performance temporary staging, caches, extracted archives, and regenerable intermediates | Allocate and manage with HPC Workspace; record expiration and never keep the only valuable copy here. |
| `/nese`, `/nas`, `/gypsum` | Existing legacy workflows only | Do not select for new workflow design. |

Treat snapshots as short recovery aids, not backups. Scratch has no snapshots.
Maintain an independent durable copy of valuable data and record how it can be
reconstructed or retrieved.

Use [HPC Workspace](https://docs.unityhpc.org/documentation/managing-files/hpc-workspace/)
for scratch:

- Allocate with `ws_allocate <name> <days>` and capture the returned path; do
  not construct a scratch path by hand.
- Choose a duration that covers the job plus validation and copy-out time. The
  documented maximum initial duration is 30 days.
- Check usage and expiration with `squota` and `ws_list -v`; extend deliberately
  with `ws_extend` when justified.
- Copy and verify retained outputs before releasing the workspace with
  `ws_release`.
- Treat release or expiration as eventual deletion with no recovery guarantee.

## Place software and caches deliberately

Keep reproducible environment definitions and lock files in version control.
Place persistent realized environments and tools under an appropriate `/work`
project path. Redirect package, model, application, and build caches out of
`/home`:

- Use scratch for caches and build intermediates that are safe to recreate.
- Use `/work` for expensive reusable state that must survive scratch expiration.
- Use `/project` for large, persistent collections that are staged before
  computation.
- Set each tool's supported cache/environment variable explicitly; examples
  include `PIXI_CACHE_DIR`, `XDG_CACHE_HOME`, `HF_HOME`, `CONDA_PKGS_DIRS`, and
  `CONDA_ENVS_PATH`.
- Heed warnings that a cache or database is on a network or parallel
  filesystem. Check the application's shared-filesystem and locking support;
  do not suppress the warning without evidence.

Check quota before installation and after large operations. A full quota can
surface as misleading application failures. For large trees or many small
files, use a batch job when practical and avoid noisy per-file output. Follow
Unity's [quota guidance](https://docs.unityhpc.org/documentation/managing-files/quotas/).

## Run work through Slurm

Do not run jobs on login nodes. Use login nodes for editing, lightweight
inspection, submission, and monitoring only, as required by Unity's
[acceptable-use policy](https://docs.unityhpc.org/about/terms-of-service/).

- Use `sbatch` for unattended work and `salloc` for interactive allocations;
  use `srun` for job steps inside an allocation.
- Declare time, CPUs, memory, GPUs, partition/QoS, account, job name, and log
  paths explicitly. Specify `--account=pi_...` when account selection matters.
- Request the minimum resources that the workload can use effectively. Do not
  request a GPU for CPU-only work or multiple nodes for software without
  distributed-memory support.
- Pilot one small representative job before arrays or campaign-scale
  submission. Use arrays for homogeneous fan-out and dependencies for explicit
  ordering.
- Put logs and final outputs on persistent work storage. Use scratch only for
  staged inputs and intermediates whose loss is acceptable or recoverable.
- Capture the submitted script, resolved parameters, environment/container
  identity, input identities, Slurm job ID, and output paths when provenance or
  reproducibility matters.

Consult the current [Slurm guide](https://docs.unityhpc.org/documentation/jobs/slurm/)
and partition/node documentation before hard-coding scheduler choices.

## Monitor, validate, and close out

- Use `squeue --me` for current jobs without tight polling loops; use `sacct`
  for completed or older jobs.
- Inspect efficiency with `seff`, `sstat`, and application metrics. Attach to an
  allocated node with the documented `srun --overlap --pty --jobid ...` pattern
  when direct inspection is necessary.
- Distinguish scheduler failure, resource exhaustion, quota failure,
  application failure, and data-staging failure before retrying.
- Adjust future CPU, memory, GPU, and time requests from observed utilization.
- Validate retained outputs before copying them from scratch. Verify size,
  expected files, checksums or content identities, and permissions as the
  workflow requires.
- Remove or release disposable state only after durable outputs and required
  logs are verified. Report what was removed and whether it is recoverable.

## Preserve safety and governance

- Keep credentials, tokens, private keys, and restricted-data metadata out of
  job scripts, logs, repositories, and shared scratch.
- Confirm group ownership and access mode before placing controlled or shared
  data under `/work`, `/project`, or a shared workspace.
- Do not broaden permissions or share a workspace without authorization.
- Stop before destructive cleanup when the exact path, ownership, retention,
  or durable-copy status is uncertain.
- Escalate current-policy questions to Unity support rather than inventing a
  cluster rule.
