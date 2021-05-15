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

#Hyperparameters
learning_rate = 0.01
gamma = 0.99
episodes = 20000
render = False
eps = np.finfo(np.float32).eps.item()
SavedAction = namedtuple('SavedAction',['log_prob', 'value'])

class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()

        self.save_actions = []
        self.rewards = []
        os.makedirs('./AC_SmartMetro-v0', exist_ok=True)

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
        # x:(batch_size,16,6,30)

        # action_score & state_value
        x1, x2 = x.chunk(2, dim=0)      # (batch_size,8,6,30)
        x_ = torch.stack([x1, x2], dim=0)
        state_value = torch.zeros(1, 16)
        for i in range(0,2,1):
            x_i = x_[i,:]
            x_i = self.conv1(x_i)
            for j in range(0,8,1):
                x_j = x_i[j,:]
                state_value[0,j+i*8] = self.linear1(x_j)
        action_score_ = F.softmax(state_value[:,0:7], dim=2)+F.softmax(state_value[:,8:15], dim=2)
        probs = F.softmax(action_score_, dim=2)
        return probs, state_value
model = Policy()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

     def select_action(state):
         state = torch.from_numpy(state).float()
         probs, state_value = model(state)
         m = Categorical(probs)
         action = m.sample()
         model.save_actions.append(SavedAction(m.log_prob(action), state_value))

         return action.item()


     def finish_episode():
         R = 0
         save_actions = model.save_actions
         policy_loss = []
         value_loss = []
         rewards = []

         for r in model.rewards[::-1]:
             R = r + gamma * R
             rewards.insert(0, R)  # [.....r+gamma*R, R]

         rewards = torch.tensor(rewards)
         rewards = (rewards - rewards.mean()) / (rewards.std() + eps)

         for (log_prob, value), r in zip(save_actions, rewards):
             reward = r - value.item()
             policy_loss.append(-log_prob * reward)
             value_loss.append(F.smooth_l1_loss(value_loss, torch.tensor([r])))

         optimizer.zero_grad()
         loss = torch.stack(policy_loss).sum() + torch.stack(value_loss).sum()
         loss.backward()
         optimizer.step()

         del model.rewards[:]
         del model.save_actions[:]