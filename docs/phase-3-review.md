# Phase 3 review: BABS qualification on Unity

Initial review: 2026-07-20

Requalification: 2026-07-21

## Purpose and overall judgment

The accepted toy result proved that BABS could initialize a direct Study-layout
project, submit a participant job on Unity, merge the result branch into the
output RIA, and leave a reviewable DataLad history. It did **not** prove that
our BABS interface was ready for a scientific campaign. The subsequent
three-subject SimBIDS rerun now qualifies that engineering interface end to end,
but remains deliberately non-scientific.

The run mixed four kinds of problem that should have been described separately:

1. **Our invocation mistakes:** bypassing Pixi with a hand-written `PATH`, using
   deprecated `babs-*` executables, and exposing long internal argv in the
   working narrative.
2. **Our project-preparation mistakes:** registering the image in DataLad
   configuration without creating BABS's required DataLad Containers image
   entry, and not testing the app/BABS output-directory contract before
   submission.
3. **Unity discovery:** BABS's generic temporary-disk directive is not accepted
   by Unity's Slurm configuration. This is normal site qualification, although
   it should have been discovered with a generated-script preflight.
4. **BABS defects at the pinned revision:** direct-layout initialization and
   `check-setup` disagree, and the installed `babs-unzip` entry point names a
   function that no longer exists.

The rerun corrected the project-owned defects before submission: Pixi 0.73 and
lock format v7 are used through short tasks; noninteractive Bash exposes Pixi
without absolute paths; the exact SIF has a conventional `datalad
containers-add` registration; `.env` loading has a declared non-secret
boundary; and the generated participant script has no ad hoc `PATH`, `HOME`, or
cache exports. Slurm job `62027866` completed all three array tasks and merged
three outputs. Final Deno validation reported three subjects, 86 payload files,
zero errors, and six reviewed synthetic `NIFTI_UNIT` warnings.

Two upstream gaps remain. The official checker was exercised successfully only
by adding a temporary tracked `inputs/data/raw` alias, running its Unity test
job, then removing and synchronizing the alias before submission. The stale
`babs-unzip` entry point remains unusable; this run used the explicit supported
policy of plain unzip followed by one DataLad save and metadata finalization
under `datalad run`.

## Findings and corrective strategy

| Concern | Finding | Ownership | Strategy before the next run |
|---|---|---|---|
| Manual `PATH=.../.pixi/...` | Locked `pixi run -e babs ...` selects the intended interpreter through the root manifest link. Earlier tasks incorrectly assumed the repository root while Pixi started them in `envs/`; the path prefix bypassed rather than fixed that task defect. | Ours | Task working directories are now explicit, and short Pixi tasks are the operator-facing commands. Expanded argv remains only in machine provenance. |
| Container image registration | The accepted image dataset had a `datalad.containers.*` configuration entry but initially lacked `.datalad/environments/<name>/image`, which BABS explicitly requires. | Ours | Build every accepted image entry with `datalad containers-add`; reject a registry commit unless both DataLad Containers and BABS resolve it. |
| `inputs/data` failure | Direct-layout initialization honored `path_in_babs: sourcedata/raw`; `check-setup` still asserted that `inputs/data` contained a directory. | BABS regression | Patch and test the checker to inspect configured input paths. Do not waive `check-setup` for the next run. |
| Lifecycle provenance | Scheduler lifecycle commands were neither scientific transformations nor suitable `datalad run` commands. They were nevertheless invoked through an unnecessarily verbose ad hoc shell command. | Interface design | Use Pixi tasks plus the operations ledger for `init`, `check-setup`, `submit`, `status`, and `merge`. Reserve `datalad run` for commands that transform tracked dataset content. |
| `all_results_in_one_zip` | It is a real BABS option. It creates one wrapper directory so BABS can zip a BIDS-style root output. It does not disable archives. | Correct BABS use, poorly explained | Retain it only while using archive-producing BABS. Test the generated output path against the app before submission. Treat zipless operation as a separate BABS change. |
| Batch preamble | The preamble forced a host tool path and redirected host `HOME`/cache into `/tmp`. The intent was isolation, but it was hard-coded, non-portable, and not tied to verified job-local storage or explicit cleanup. | Ours | Remove `PATH` from campaign YAML. Start with no `HOME` override; add a minimal site-profile bootstrap only for a demonstrated requirement. Keep container isolation flags separate. |
| `.env` warning | The installed con-duct 0.21.0 source contains no dotenv loading, and the current Pixi BABS task reproduces without this warning. Its producer and expected lookup directory are therefore not established. | Unresolved observation | Define the intended `.env` consumer and boundary first; then lock `python-dotenv`, add a non-secret `.env.example`, ignore `.env`, and test loading from the declared location. |
| Finalization | `babs-unzip` is installed but imports missing `babs.cli._enter_unzip`. The custom extractor was a valid recovery and was run under `datalad run`, but is not the desired steady-state workflow. | BABS packaging/API defect; local recovery acceptable | Qualify a patched BABS revision with an end-to-end merge/finalization fixture. Do not silently use the stale entry point. |
| `.bidsignore` | It made the combined BABS-analysis/BIDS-derivative root validator-clean, but it is broader than necessary and exposes tension between BABS operational files and a BIDS derivative root. | Integration workaround | Minimize ignores to exact non-BIDS artifacts; make the toy app emit BIDS-valid derivatives; seek an upstream operational-layout solution rather than accumulating ignores. |
| Validator | The project used `bids-validator-deno` 3.0.0. | Correct | Keep it as the sole BIDS validator and expose it only through the Pixi validation task. |

## 1. Pixi and command-line usage

The direct invocation

```text
PATH=.../envs/.pixi/envs/babs/bin:/usr/bin:/bin python scripts/run_babs_operation.py ...
```

was a mistake. It bypassed Pixi's task interface, coupled the command to one
checkout path, and made logs harder to read. It also omitted environment setup
that Pixi may add beyond `PATH`.

The environment is healthy. This command resolves the expected interpreter and
BABS revision:

```bash
pixi run --locked -e babs \
  python -c 'import sys, babs; print(sys.executable); print(babs.__version__)'
```

The task layer now sets `cwd = "."` explicitly. The tracked root `pixi.toml`
and `pixi.lock` links provide normal Pixi discovery, and `.bashrc` adds
`$HOME/.pixi/bin` before its noninteractive early return. Tasks therefore work
from interactive shells, noninteractive agent commands, and generated Slurm
scripts without naming Pixi's absolute path or a private environment-bin path.

The operator interface should instead look like:

```bash
pixi run --locked -e babs babs-init <campaign>
pixi run --locked -e babs babs-check <campaign>
pixi run --locked -e babs babs-pilot <campaign>
pixi run --locked -e babs babs-status <campaign>
pixi run --locked -e babs babs-merge <campaign>
```

The task implementation may resolve the long paths and arguments from the
campaign record. Humans should not have to retype them. The exact expanded argv
still belongs in `commands.jsonl` and con-duct logs.

The launcher should also call the supported unified CLI (`babs init`,
`babs check-setup`, `babs submit`, and so on), not the deprecated compatibility
executables (`babs-init`, `babs-submit`, and so on).

### Where `datalad run` belongs

`datalad run` records a transformation of dataset content by declaring inputs,
outputs, and a command. The participant script generated by BABS already uses
it for the BIDS App execution. Our emergency finalizer also correctly used it
because extraction changed tracked derivative content.

`babs submit` is different: its central effect is external scheduler state. A
`datalad run` wrapper would not make that state reproducible and could imply an
output contract that the command does not have. The appropriate layers are:

```text
operator -> Pixi task -> campaign launcher -> BABS lifecycle command
                                      \-> operations event + con-duct evidence

BABS participant job -> datalad run -> containerized BIDS App -> tracked result branch
```

Thus the problem was the missing concise Pixi interface, not the absence of
`datalad run` around every BABS management command.

## 2. Container registration must follow BABS convention

There was no good reason to omit BABS's conventional registration. The phrase
“the newer config entry” overstated what we had: the configuration entry was a
DataLad Containers execution record, but it was not a complete BABS-compatible
image registration.

BABS derives the image path as

```text
containers/.datalad/environments/<container_name>/image
```

and checks that path during initialization. Its own preparation guide creates
the entry with `datalad containers-add`. We should do the same in the
authoritative accepted-container dataset, rather than manufacture a config
entry or repair a symlink after BABS rejects it.

The image-acceptance gate should prove all of the following from a fresh clone:

1. `datalad containers-list` reports the expected name.
2. `.datalad/environments/<name>/image` exists as the registered image or
   symlink.
3. The annex key and SHA-256 agree with the image record.
4. `datalad containers-run -n <name> ...` executes the fixture.
5. BABS `Container.sanity_check()` resolves the same name.

The attempt-001 cleanup failure was secondary. BABS tried to remove its partial
project after the registration assertion, but read-only annex object
permissions prevented recursive removal. Preserving the remnant and not reusing
the briefly assigned DataLad UUID was cautious. Preventing the invalid
registration from reaching `babs init` would have avoided the situation.

Primary BABS references: [container preparation](https://github.com/PennLINC/babs/blob/2cc536a51282124f3811ffa971f82a7c34116af5/docs/preparation_container.rst) and [container path sanity check](https://github.com/PennLINC/babs/blob/2cc536a51282124f3811ffa971f82a7c34116af5/babs/container.py#L74-L105).

## 3. Direct layout, “legacy” layout, and the checker defect

“Legacy” in the earlier status update meant BABS's historical project layout,
not a legacy BIDS standard:

```text
<BABS project>/
  analysis/
    inputs/data/<input dataset>/
    containers/
    code/
  input_ria/
  output_ria/
```

STAMPED is using the new direct Study layout introduced by BABS
[commit `2cc536a`](https://github.com/PennLINC/babs/commit/2cc536a51282124f3811ffa971f82a7c34116af5):

```text
<Study derivative attempt>/          # analysis_path: "."
  sourcedata/raw/                    # configured path_in_babs
  containers/
  code/
  .babs/input_ria/
  .babs/output_ria/
```

This is the layout we intended. Initialization correctly read `analysis_path`,
the RIA paths, and each input's `path_in_babs`, then installed the raw dataset at
`sourcedata/raw`.

The failure was inside the same newly merged direct-layout revision. At
[`check_setup.py` lines 86–91](https://github.com/PennLINC/babs/blob/2cc536a51282124f3811ffa971f82a7c34116af5/babs/check_setup.py#L86-L91),
the checker still requires a subdirectory of `inputs/data`; immediately
afterward it correctly iterates the configured input dataset paths. That stale
assertion is inconsistent with initialization and should be replaced by checks
over the configured inputs.

Calling this an “upstream direct-layout bug” was accurate but insufficiently
explained. More importantly, continuing after it was expedient rather than the
standard we want. The next campaign must run a patched checker successfully,
including its cluster test job, before pilot submission.

## 4. Output archives and `all_results_in_one_zip`

`all_results_in_one_zip: true` is documented and implemented in this BABS
revision. It is intended for BIDS Apps that write files directly at the output
root instead of creating one wrapper directory. BABS creates the single
directory named by `zip_foldernames`, directs the app there, and then archives
that directory. Only one `zip_foldernames` entry is permitted in this mode.

For the toy app this was the correct setting under the current archive-based
BABS contract. Attempt 002 exposed the mismatch because the app wrote directly
to its supplied output directory while BABS later looked for an expected
`toy-bids-app/` wrapper.

This setting has no connection to eliminating output ZIP files. A future
zipless workflow requires a BABS implementation that tracks derivative outputs
directly and adjusts merge/finalization semantics. It should be evaluated as a
separate upstream feature or maintained patch, not inferred from this option.

Primary reference: [BABS output-layout documentation](https://github.com/PennLINC/babs/blob/2cc536a51282124f3811ffa971f82a7c34116af5/docs/preparation_config_yaml_file.rst#L420-L530).

## 5. Batch preamble and environment isolation

The preamble attempted two different things:

- the `PATH` line made host-side `datalad`, `git-annex`, and related commands
  available in the compute job;
- the `HOME` and `XDG_CACHE_HOME` lines tried to prevent the host-side job from
  reading or writing a persistent user home and cache.

The intent does not justify this implementation. The absolute `PATH` belongs to
one checkout and leaks environment internals into scientific configuration.
The fallback `${SLURM_TMPDIR:-/tmp}` was not established as private job scratch
on Unity, and the created directories had no explicit cleanup. Meanwhile,
Apptainer's `--cleanenv`, `--containall`, and `--no-home` already address the
container boundary; they do not require changing host `HOME`.

For the next run:

1. Remove all three exports from campaign science configuration.
2. Verify a generated no-op participant job using Unity's normal login/batch
   environment.
3. If host tools are unavailable, use one reviewed, tracked Unity bootstrap or
   site profile. It may invoke Pixi or a stable launcher, but the operator still
   uses a Pixi task and the campaign YAML remains portable.
4. Override `HOME` or caches only in response to a demonstrated write/isolation
   requirement. Use verified job-local storage and a cleanup trap.
5. Keep container environment/network controls in the BABS container
   configuration, where their scientific meaning is reviewable.

The rejected `#SBATCH --tmp=1G` directive was a separate Unity compatibility
finding. The next cluster profile should omit BABS's generic
`temporary_disk_space` field unless Unity documents a supported equivalent.
Generated `sbatch` directives should be syntax-checked with a tiny job before
initializing a campaign attempt.

## 6. `.env` support

The requalification implements this explicit `.env` contract:

- which process loads the file (campaign launcher, BABS, participant script, or
  application);
- which directory owns it;
- which variables may cross into Slurm and the container;
- which values are secret and must never enter Git, logs, or `commands.jsonl`.

`python-dotenv` `1.2.2` is locked in the BABS feature. The lifecycle launcher
loads exactly the repository-root `.env` with `override=False` before starting
con-duct and BABS; `.env.example` contains only non-secret operational names,
and `.env` is ignored. Because con-duct may record the child environment, this
file is explicitly not a credential store. Slurm propagation is checked in the
generated test job before submission.

## 7. Merge, unzip, and finalization

The pin is not merely “possibly old.” As of this review, upstream `main` is the
same `2cc536a` commit selected by the lock. The package metadata declares:

```text
babs-unzip = babs.cli:_enter_unzip
```

but `babs.cli` has no `_enter_unzip`, and `babs --help` has no `unzip`
subcommand. The unzip implementation was removed during an earlier BABS class
refactor while its compatibility entry point remained. This is an upstream
packaging/API defect, not shell configuration.

The tracked `code/finalize_derivative.py` recovery was appropriately narrow:
it preserved the archive, extracted the payload, wrote derivative metadata with
exact `SourceDatasets`, and ran under `datalad run`. It should remain part of the
historical accepted attempt, but the general launcher must not pretend
`babs-unzip` works.

Before the next campaign, decide and test one supported policy:

1. patch current BABS to restore a tested finalization command;
2. treat merged ZIP archives as BABS's terminal output and run a separately
   versioned STAMPED finalizer under `datalad run`; or
3. qualify a zipless BABS branch if that work is ready.

Whichever policy is selected must have a fixture test from init through merge
and finalization. Merely changing the pin is ineffective because current
upstream `main` has the same defect.

Primary references: [declared entry point](https://github.com/PennLINC/babs/blob/2cc536a51282124f3811ffa971f82a7c34116af5/pyproject.toml#L63-L70) and [current CLI commands](https://github.com/PennLINC/babs/blob/2cc536a51282124f3811ffa971f82a7c34116af5/babs/cli.py).

## 8. `.bidsignore` and the direct derivative root

The visible `containers/` directory was not caused by the missing image
registration. BABS intentionally installs its container dataset at
`<analysis_path>/containers`, so direct layout places it at the derivative root.
The registration defect concerned the expected path *inside* that dataset.

The `.bidsignore` was therefore an explicit integration workaround, not an
informal hidden file. Still, the current version is too broad:

- BIDS already defines `code/` and `sourcedata/` as conventional directories;
- both `containers/` and `containers` are redundant patterns;
- ignoring `toy-bids-app.txt` hides the fact that the toy app does not emit a
  BIDS-conforming derivative filename;
- ignoring archives and BABS operational files is required only because those
  files share the derivative root.

For the next fixture, minimize `.bidsignore` to exact unavoidable BABS
operational artifacts and make the toy app produce valid derivative filenames.
Longer term, direct-layout BABS should offer a hidden or BIDS-compatible location
for its operational container and archive material. Until then, any ignored
paths must be listed as a reviewed compatibility exception and validation must
still inspect the intended derivative payload.

The SimBIDS requalification implements that separation without hiding BABS
operational paths in `.bidsignore`: validation constructs a payload view from
only derivative metadata and the three `sub-*` trees. Its `.bidsignore` covers
only reviewed fMRIPrep extensions that the current BIDS Derivatives schema does
not accept. The operational root remains fully visible to provenance checks.

## Requalification result

The 2026-07-21 rerun closed or explicitly bounded these gates:

- [x] All documented BABS operations run through short locked Pixi tasks; no
      manual environment `PATH` appears in commands or campaign YAML.
- [x] The launcher uses the unified `babs` CLI and rejects unsupported lifecycle
      operations at preflight.
- [x] The accepted container dataset is created with `datalad containers-add`
      and passes the five-part registration gate above.
- [x] The official BABS checker and Unity test job pass with the temporary,
      recorded compatibility alias; the accepted project keeps raw data only at
      `sourcedata/raw`.
- [ ] BABS itself checks configured direct-layout input paths without requiring
      that compatibility alias.
- [x] The generated participant script is reviewed before submission: Slurm
      directives, scratch path, image path, input path, app output directory,
      `datalad run` inputs/outputs, and container isolation flags all match the
      campaign.
- [x] A tiny Unity `sbatch` checker job qualifies the cluster profile without
      consuming a campaign attempt.
- [x] The dotenv consumer, exact path, non-secret boundary, and dependency are
      declared; propagation is included in the generated-job check.
- [x] The app/BABS output contract executes through the exact SIF for three
      subjects.
- [x] Merge and the selected archive/finalization policy pass end to end.
- [x] Only `bids-validator-deno` is used, via Pixi, and `.bidsignore` contains
      the minimum reviewed exceptions.
- [x] The failed missing-parent initialization is retained in the operations
      ledger and did not create an accepted derivative identity.
- [ ] Publish the exact SimBIDS SIF to independent persistent annex storage and
      prove retrieval from a fresh recursive clone.

## Remaining work before a scientific campaign

1. Resolve the configured-input checker defect upstream or carry a narrow,
   tested patch; remove the compatibility-alias procedure afterward.
2. Publish and clean-clone-test the exact SimBIDS SIF, or replace it with a
   separately qualified scientific image that passes retrieval, licensing,
   SBOM, signature, and attestation decisions.
3. Keep finalization as a declared STAMPED policy until BABS exposes a working,
   tested command. For large tiny-file trees, avoid per-file archive commits;
   consider SimBIDS/fMRIPrep `--fs-no-reconall` when FreeSurfer-shaped output is
   not part of the test objective.
4. Repeat the same gates for the first claim-bearing pipeline without treating
   this synthetic fixture as scientific evidence.
