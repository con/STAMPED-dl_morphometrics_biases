# Configuration authorities

- `datasets/`: dataset identity, access class, and cohort policy.
- `pipelines/`: scientific arguments, SIF identities, and output contracts.
- `clusters/`: host interfaces, scheduler resources, binds, and site preambles.
- `campaigns/`: prospective dataset × pipeline × cluster composition.
- `access/`: data classes and public/private sibling policy.
- `schemas/`: machine-readable record contracts.

Resolved lifecycle state belongs in an independent `operations/<campaign>/`
dataset, not in this directory.
