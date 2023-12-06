from __future__ import annotations

import statistics
from typing import cast

import numpy as np
import torch
from torch.utils.data import DataLoader

from .model import BrainAgePredictionResNet
from .utils import IXIDataset, NormIXIDataset, State, load_nii

transform = IXIDataset.transform


class Evaluator:
    def __init__(
        self,
        device: str = "cpu",
        pth_file: str | None = None,
    ) -> None:
        self.device = torch.device(device)
        self.model = BrainAgePredictionResNet().eval()
        self.model.to(self.device)
        if pth_file is not None:
            state = cast(State, torch.load(pth_file, self.device))
            self.model.load_state_dict(state["model_state_dict"])

    def test(self, dataset: NormIXIDataset | None = None, batch_size: int = 5) -> float:
        # test among dataset and report to terminal
        if dataset is None:
            dataset = NormIXIDataset("datasets/IXI-test")
        # each batch mae
        mae_errors = []
        dataloader = DataLoader(dataset, batch_size=batch_size)
        for images, labels in dataloader:
            images = images.to(self.device)
            out = self.model(images)
            out = out.numpy(force=True)
            labels = labels.numpy(force=True)
            mae_errors.append(np.mean(np.abs(out - labels)))
        return np.mean(mae_errors)

    def evaluate_files(self, nii_files: str | list[str]) -> list[float]:
        # file -> ndarray -> transform
        images: list[torch.Tensor] = []  # (D,H,W)
        if isinstance(nii_files, str):
            nii_files = [nii_files]
        for file in nii_files:
            data = load_nii(file)
            images.append(transform(data))
        inputs = torch.stack(images)
        inputs = inputs.to(self.device)
        out = self.model(inputs)
        out = out.numpy(force=True)
        assert out.ndim == 1
        out = [i.item() for i in out]
        return out

    def evaluate_ndarray(self, arrs: np.ndarray | list[np.ndarray]) -> list[float]:
        if not isinstance(arrs, list):
            arrs = [arrs]
        tensors = [transform(i) for i in arrs]
        tensors = torch.stack(tensors)
        if tensors.ndim == 3:
            tensors = tensors.unsqueeze_(0)
        elif tensors.ndim != 4:
            raise ValueError(f"expect 3 or 4 dim, got {tensors.shape}")
        tensors = tensors.to(self.device)
        out = self.model(tensors)
        out = out.numpy(force=True)
        assert out.ndim == 1
        out = [i.item() for i in out]
        return out
