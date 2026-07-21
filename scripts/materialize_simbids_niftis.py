#!/usr/bin/env python3
"""Replace SimBIDS skeleton placeholders with deterministic valid NIfTI files."""

from __future__ import annotations

import argparse
from pathlib import Path

import nibabel as nib
import numpy as np


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    args = parser.parse_args()

    dataset = args.dataset.resolve()
    paths = sorted(dataset.glob("sub-*/*/*.nii.gz"))
    if not paths:
        parser.error(f"no SimBIDS NIfTI placeholders found under {dataset}")

    for path in paths:
        shape = (2, 2, 2, 2) if path.name.endswith("_bold.nii.gz") else (2, 2, 2)
        image = nib.Nifti1Image(np.zeros(shape, dtype=np.uint8), np.eye(4))
        if len(shape) == 4:
            image.header.set_zooms((1.0, 1.0, 1.0, 2.0))
        nib.save(image, path)
        print(path.relative_to(dataset))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
