# Root image records

Each YAML record describes one candidate or registered image and validates
against `config/schemas/image-record.schema.json`. The record names exact
source/build inputs, interface and licensing decisions, qualification evidence,
and—only after registration—the accepted dataset, SIF path, annex key, and
byte hash.

The accepted container dataset is authoritative. `../images.lock.yaml` records
the registry's current commit and mirrors each image's own registration commit
and exact identity fields. Older valid image records therefore remain pinned to
the commit that introduced their bytes; they are not rewritten whenever a new
image is added. The index must never replace a DataLad Containers run record or
result-manifest entry.
