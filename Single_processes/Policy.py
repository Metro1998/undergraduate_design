# @author  Wolfie
# @date    2021-05-13

import numpy as np
from itertools import count
from collections import namedtuple

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical

class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(                       # (8,6,60)
                in_channels=8,
                out_channels=8,
                kernel_size=3,
                stride=1,
                padding=1,
            )
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1,2))  # (8,6,30)
        )
        self.linear1 = nn.Linear(6*30,1)

    def forward(self, x):
        action_score1 = torch.zeros(1,8)
        action_score2 = torch.zeros(1,8)
        x1 = x[0:7, :, :]               # (batch_size,8,6,30)
        x2 = x[8:15, :, :]
        x1 = self.conv1(x1)
        x2 = self.conv1(x2)
        for i in range(0,8,1):
            x1 = x1[i, :, :]
            x2 = x2[i, :, :]
            action_score1[i] = self.linear1(x1)
            action_score2[i] = self.linear1(x2)


        x = x.view(8, -1)     # (batch_size,8,6*30)
        out = self.m(x)  # (batch_size,8)

