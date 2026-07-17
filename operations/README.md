# Campaign operations datasets

Every real `operations/<campaign>/` is an independent DataLad dataset with its
own identity and commit history. It records immutable campaign resolution,
desired and observed state, inclusion accounting, literal lifecycle commands,
and acceptance decisions. It points to a BABS attempt under a Study and never
contains or replaces that derivative.

Phase 1 defines the schemas only; it does not create a placeholder operations
dataset.
