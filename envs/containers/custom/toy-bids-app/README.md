# Toy BIDS App image

This small Alpine-based definition exists only to exercise the Phase 2 accepted
container registry. Its runscript implements the standard `bids_dir`,
`output_dir`, and `analysis_level` interface, supports `--help` and
`--version`, and writes only a minimal derivative fixture. It is not a
scientific runtime and no output produced from it is authoritative.

The base digest is pinned in the definition. The release record stores the
builder version, definition and Pixi hashes, exact SIF bytes, annex key, and
qualification evidence. Scientific images remain Phase 5 work.
