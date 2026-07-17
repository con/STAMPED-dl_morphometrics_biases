# Root image records

Each YAML record describes one candidate or registered image and validates
against `config/schemas/image-record.schema.json`. The record names exact
source/build inputs, interface and licensing decisions, qualification evidence,
and—only after registration—the accepted dataset, SIF path, annex key, and
byte hash.

The accepted container dataset is authoritative. `../images.lock.yaml` mirrors
only the accepted identity fields so humans and tooling can look up an image
without resolving the full record. It must never replace a DataLad Containers
run record or result-manifest entry.
