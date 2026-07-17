# Scientific container datasets

- `repronim/` is the pinned ReproNim/containers source dataset. It is evidence
  for candidate discovery, not an execution identity.
- `custom/` stores tracked project image definitions and their declared build
  inputs. Definitions do not become a runtime until their resulting SIF is
  qualified and registered.
- `accepted/` is an independent DataLad dataset of exact registered SIF bytes.
  Its DataLad Containers registration, SIF annex key, and dataset commit are
  authoritative for image identity.

The derived [image index](../images.lock.yaml) is a convenience lookup. If it
conflicts with the accepted dataset, a DataLad Containers run record, or a
result-manifest entry, those provenance-bearing records prevail.
