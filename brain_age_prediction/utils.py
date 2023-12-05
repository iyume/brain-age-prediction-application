from __future__ import annotations

import csv
import operator
import os
import re
from pathlib import Path
from typing import Any, TypedDict

import nibabel as nib
import numpy as np
import scipy.ndimage as nd
import torch
from torch.utils.data import Dataset


def load_nii(file: str) -> np.ndarray:
    data: np.memmap = nib.load(file).get_fdata()  # type: ignore
    inputs = np.array(data, dtype=np.float32)
    return inputs


class State(TypedDict):
    """The training state."""

    epoch: int
    model_state_dict: dict[str, torch.Tensor]
    optim_state_dict: dict[str, Any]
    loss: float
    all_losses: list[float]


class IXIDataset(Dataset):
    def __init__(
        self, path: str = "datasets/IXI", label_path: str = "datasets/IXI.csv"
    ) -> None:
        super().__init__()
        if not os.path.exists(path):
            raise ValueError(f"given path {path} not exist")
        if not os.path.splitext(label_path)[1] == ".csv":
            raise ValueError("need csv label (example at datasets/IXI.csv)")
        self.files: dict[int, str] = {}
        for file in Path(path).iterdir():
            if not file.suffix == ".nii":
                print(f"not .nii file at {file}")
                continue
            match = re.match(r"IXI(\d+)", file.stem)
            if not match:
                print(f"invalid filename format {file}")
                continue
            self.files[int(match.group(1))] = str(file)
        if not self.files:
            raise ValueError("no .nii file in given dataset path")
        self.labels: dict[int, float] = IXIDataset.load_csv_age_label(label_path)
        removed_ixi_ids = []
        for ixi_id in list(self.files):
            if ixi_id not in self.labels:
                del self.files[ixi_id]
                removed_ixi_ids.append(ixi_id)
        # some file no recorded in csv. or age field empty
        if removed_ixi_ids:
            print(f"not associated age to the sample #{removed_ixi_ids}")
        self.indexes = dict(zip(range(len(self.files)), self.files.keys()))

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, float]:
        ixi_id = self.indexes[idx]
        file = self.files[ixi_id]
        inputs = load_nii(file)
        return self.transform(inputs), self.labels[ixi_id]

    def __len__(self) -> int:
        return len(self.files)

    @staticmethod
    def load_csv_age_label(label_path: str) -> dict[int, float]:
        labels: dict[int, float] = {}
        with open(label_path, "r") as f:
            for row in csv.DictReader(f):
                ixi_id = int(row["IXI_ID"])
                age = row["AGE"]
                if not age:
                    continue
                labels[ixi_id] = float(age)
        return labels

    @staticmethod
    def transform(img: np.ndarray) -> torch.Tensor:
        # 1.68s execute time
        # from (256,256,146/150) to (256,256,128)
        new_shape = (256, 256, 128)
        real_resize_factor = tuple(map(operator.truediv, new_shape, img.shape))
        img = nd.zoom(img, real_resize_factor, order=3)
        return torch.from_numpy(img)


class NormIXIDataset(Dataset):
    def __init__(
        self, path: str = "datasets/IXI-norm", label_path: str = "datasets/IXI.csv"
    ) -> None:
        super().__init__()
        if not os.path.exists(path):
            raise ValueError(
                f"given path {path} not exist. use scripts/transform_dataset.py "
                "to generate normalized dataset"
            )
        if not os.path.splitext(label_path)[1] == ".csv":
            raise ValueError("need csv label (example at datasets/IXI.csv)")
        self.files: dict[int, str] = {}
        for file in Path(path).iterdir():
            if not file.suffix == ".npy":
                print(f"not .nii file at {file}")
                continue
            match = re.match(r"IXI(\d+)", file.stem)
            if not match:
                print(f"invalid filename format {file}")
                continue
            self.files[int(match.group(1))] = str(file)
        if not self.files:
            raise ValueError("no .nii file in given dataset path")
        self.labels: dict[int, float] = IXIDataset.load_csv_age_label(label_path)
        removed_ixi_ids = []
        for ixi_id in list(self.files):
            if ixi_id not in self.labels:
                del self.files[ixi_id]
                removed_ixi_ids.append(ixi_id)
        # some file no recorded in csv. or age field empty
        if removed_ixi_ids:
            print(f"not associated age to the sample #{removed_ixi_ids}")
        self.indexes = dict(zip(range(len(self.files)), self.files.keys()))

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, float]:
        ixi_id = self.indexes[idx]
        file = self.files[ixi_id]
        return np.load(file), self.labels[ixi_id]

    def __len__(self) -> int:
        return len(self.files)
