import os
import torch
import torch.nn.functional as F
import math
from torch.optim import Adam
from utils import soft_update, hard_update
from model import GaussianPolicy, QNetwork
import numpy as np


class SAC(object):
    def __init__(self):

        self.gamma = 0.99
        self.tau = 0.005
        self.alpha = 0.2
        self.lr = 0.003

        self.target_update_interval = 1
        self.device = torch.device("cpu")

        # 8 phases
        self.num_inputs = 8
        self.num_actions = 1
        self.hidden_size = 256

        self.critic = QNetwork(self.num_inputs, self.num_actions, self.hidden_size).to(self.device)
        self.critic_optimizer = Adam(self.critic.parameters(), lr=self.lr)

        self.critic_target = QNetwork(self.num_inputs, self.num_actions, self.hidden_size).to(self.device)
        hard_update(self.critic_target, self.critic)
        # Copy the parameters of critic to critic_target

        self.target_entropy = -torch.Tensor([1.0]).to(self.device).item()
        self.log_alpha = torch.zeros(1, requires_grad=True, device=self.device)

        self.alpha_optimizer = Adam([self.log_alpha], lr=self.lr)

        self.policy = GaussianPolicy(self.num_inputs, self.num_actions, self.hidden_size).to(
            self.device)
        self.policy_optimizer = Adam(self.policy.parameters(), lr=self.lr)

    def select_action(self, state):
        state = torch.FloatTensor(state).to(self.device)  # TODO
        _, _, action = self.policy.sample(state)
        return action.detach().cpu().numpy()[0]
        # action is a CUDA tensor, you should do .detach().cpu().numpy(), when
        # you need a numpy

    def update_parameters(self, memory, batch_size, updates):
        # Sample a batch from memory
        state_batch, action_batch, reward_batch, next_state_batch, mask_batch = memory.sample(batch_size=batch_size)
        action_batch = np.expand_dims(action_batch, axis=1)

        state_batch = torch.FloatTensor(state_batch).to(self.device)
        next_state_batch = torch.FloatTensor(next_state_batch).to(self.device)
        action_batch = torch.FloatTensor(action_batch).to(self.device)
        reward_batch = torch.FloatTensor(reward_batch).to(self.device).unsqueeze(1)
        mask_batch = torch.FloatTensor(mask_batch).to(self.device).unsqueeze(1)
        # Unsqueeze: add one dimension to the index

        with torch.no_grad():
            next_state_action, next_state_log_pi, _ = self.policy.sample(next_state_batch)
            qf1_next_target, qf2_next_target = self.critic_target(next_state_batch, next_state_action)
            min_qf_next_target = torch.min(qf1_next_target, qf2_next_target) - self.alpha * next_state_log_pi
            next_q_value = reward_batch + mask_batch * self.gamma * (min_qf_next_target)
        qf1, qf2 = self.critic(state_batch,
                               action_batch)  # Two Q-functions to mitigate positive bias in the policy improvement step
        qf1_loss = F.mse_loss(qf1, next_q_value)  # JQ = 𝔼(st,at)~D[0.5(Q1(st,at) - r(st,at) - γ(𝔼st+1~p[V(st+1)]))^2]
        qf2_loss = F.mse_loss(qf2, next_q_value)  # JQ = 𝔼(st,at)~D[0.5(Q1(st,at) - r(st,at) - γ(𝔼st+1~p[V(st+1)]))^2]
        qf_loss = qf1_loss + qf2_loss

        self.critic_optimizer.zero_grad()
        # Clear the cumulative grad
        qf_loss.backward()
        # Get grad via backward()
        self.critic_optimizer.step()
        # Update the para via grad

        pi, log_pi, _ = self.policy.sample(state_batch)

        qf1_pi, qf2_pi = self.critic(state_batch, pi)
        min_qf_pi = torch.min(qf1_pi, qf2_pi)

        policy_loss = ((self.alpha * log_pi) - min_qf_pi).mean()
        # Jπ = 𝔼st∼D,εt∼N[α * logπ(f(εt;st)|st) − Q(st,f(εt;st))]

        self.policy_optimizer.zero_grad()
        policy_loss.backward()
        self.policy_optimizer.step()

        # automatic_entropy_tuning:
        alpha_loss = -(self.log_alpha * (log_pi + self.target_entropy).detach()).mean()  # TODO

        self.alpha_optimizer.zero_grad()
        alpha_loss.backward()
        self.alpha_optimizer.step()

        self.alpha = self.log_alpha.exp()
        alpha_tlogs = self.alpha.clone()  # For TensorboardX logs

        if updates % self.target_update_interval == 0:
            soft_update(self.critic_target, self.critic, self.tau)

        return qf1_loss.item(), qf2_loss.item(), policy_loss.item(), alpha_loss.item(), alpha_tlogs.item()

    # Save model parameters
    def save_model(self, env_name, suffix="", actor_path=None, critic_path=None):
        # Create a dir package in the current location
        if not os.path.exists('models/'):
            os.makedirs('models/')

        if actor_path is None:
            actor_path = "models/sac_actor_{}_{}".format(env_name, suffix)
        if critic_path is None:
            critic_path = "models/sac_critic_{}_{}".format(env_name, suffix)
        print('Saving models to {} and {}'.format(actor_path, critic_path))
        torch.save(self.policy.state_dict(), actor_path)
        # state_dict() stores the parameters of layers and optimizers which have grad
        torch.save(self.critic.state_dict(), critic_path)

    # Load model parameters
    def load_model(self, actor_path, critic_path):
        print('Loading models from {} and {}'.format(actor_path, critic_path))
        if actor_path is not None:
            self.policy.load_state_dict(torch.load(actor_path))
        if critic_path is not None:
            self.critic.load_state_dict(torch.load(critic_path))

    def get_alpha(self):
        return self.alpha
