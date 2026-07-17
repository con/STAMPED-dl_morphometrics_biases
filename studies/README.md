# BIDS Study datasets

Each `studies/<study>/` is an independent DataLad dataset with a BIDS 1.11.1
`DatasetType: "study"` description. Its `sourcedata/raw/` input is an independent
raw BIDS/DataLad dataset, and each produced derivative retains its own identity.
BABS is pointed at `sourcedata/raw/`, never at the Study root.
