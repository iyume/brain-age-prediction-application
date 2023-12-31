from __future__ import annotations

import time
from pathlib import Path
from typing import cast

import torch
from torch import nn
from torch.utils.data import DataLoader

from .model import BrainAgePredictionResNet
from .utils import IXIDataset, NormIXIDataset, State

ckpt_dir = Path("ckpt")
ckpt_dir.mkdir(exist_ok=True)


class Trainer:
    def __init__(
        self,
        device: str = "cpu",
        learning_rate: float = 1e-3,
        batch_size: int = 4,
        pth_file: str | None = None,
        dataset: IXIDataset | NormIXIDataset | None = None,
    ) -> None:
        self.model = BrainAgePredictionResNet().train()
        self.device = torch.device(device)
        if dataset is None:
            dataset = NormIXIDataset()
        print(f"loaded {len(dataset)} samples")
        self.dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        self.model.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), learning_rate)
        self.loss_fn = nn.L1Loss()
        if pth_file is None:
            state = State(
                epoch=0,
                model_state_dict=self.model.state_dict(),
                optim_state_dict=self.optimizer.state_dict(),
                loss=0,
                all_losses=[],
            )
        else:
            state = cast(State, torch.load(pth_file, self.device))
            self.model.load_state_dict(state["model_state_dict"])
            self.optimizer.load_state_dict(state["optim_state_dict"])
            # get parameters view
            state["model_state_dict"] = self.model.state_dict()
            state["optim_state_dict"] = self.optimizer.state_dict()
        self.state = state

    def train_one(self, create_checkpoint: bool = True):
        loss_history = []
        for idx, (images, labels) in enumerate(self.dataloader):
            images = images.to(self.device)
            labels = labels.to(self.device)
            self.optimizer.zero_grad()
            out = self.model(images)
            loss = self.loss_fn(out, labels)
            loss.backward()
            loss_history.append(loss.item())
            self.optimizer.step()
            print("iter: {}  loss: {:.4f}".format(idx, loss))
        self.state["epoch"] += 1
        loss_avg = sum(loss_history) / len(loss_history)
        self.state["loss"] = loss_avg
        self.state["all_losses"].append(loss_avg)
        print(f"epoch {self.state['epoch']} training complete")
        print(f"STAT LOSS: {self.state['loss']:.4f}")
        if create_checkpoint:
            checkpoint = (
                ckpt_dir / f"model_{self.model.version}_epoch{self.state['epoch']}.pth"
            )
            torch.save(self.state, checkpoint)
            print(f"model saved at {checkpoint}")

    def train(self, num_epochs: int = 100):
        for _ in range(num_epochs):
            self.train_one(True)
