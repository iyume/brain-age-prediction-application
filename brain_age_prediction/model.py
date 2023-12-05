from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import nn


class Bottleneck(nn.Module):
    def __init__(
        self, inc: int, outc: int, *, midc: int | None = None, stride: int = 1
    ) -> None:
        super().__init__()
        if midc is None:
            midc = inc
        self.conv = nn.Sequential(
            nn.Conv3d(inc, midc, 1),
            nn.BatchNorm3d(midc),
            nn.ReLU(True),
            nn.Conv3d(midc, midc, 3, stride, 1),
            nn.ReLU(True),
            nn.Conv3d(midc, outc, 1),
        )
        self.downsample = None
        if inc != outc or stride != 1:
            self.downsample = nn.Conv3d(inc, outc, 1, stride)

    def forward(self, x):
        identity = x
        if self.downsample is not None:
            identity = self.downsample(identity)
        residual = self.conv(x)
        identity = identity + residual
        identity = F.relu_(identity)
        return identity


class BrainAgePredictionResNet(nn.Module):
    version = "v1"

    # def __init__(self) -> None:
    #     super().__init__()
    #     # (N,1,256,256,128)
    #     self.conv0 = Bottleneck(1, 8, midc=8)
    #     self.conv1 = Bottleneck(8, 16, stride=2)
    #     # (N,16,128,128,64)
    #     self.conv2 = Bottleneck(16, 32, stride=2)
    #     # (N,32,64,64,32)
    #     self.conv3 = Bottleneck(32, 64, stride=2)
    #     # (N,64,32,32,16)
    #     self.conv4 = Bottleneck(64, 128, stride=2)
    #     # (N,128,16,16,8)
    #     self.linear1 = nn.Linear(128 * 16 * 16 * 8, 1)

    def __init__(self) -> None:
        super().__init__()
        # (N,1,256,256,128)
        self.conv0 = nn.Conv3d(1, 8, 1)
        self.conv1 = Bottleneck(8, 16, stride=2)
        # (N,16,128,128,64)
        self.conv2 = Bottleneck(16, 32, stride=2)
        # (N,32,64,64,32)
        self.conv3 = Bottleneck(32, 64, stride=2)
        # (N,64,32,32,16)
        self.conv4 = Bottleneck(64, 128, stride=2)
        # (N,128,16,16,8)
        self.fc1 = nn.Linear(128 * 16 * 16 * 8, 1)

    def forward(self, x: torch.Tensor):
        if x.ndim != 4:
            raise ValueError(f"input should be (N,D,H,W)")
        x.unsqueeze_(1)  # add channel for 3d generation
        x = self.conv0(x)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x.squeeze_(1)
        return x
