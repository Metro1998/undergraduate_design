# @author  Wolfie
# @date    2021-05-24

import os
import sys
import itertools
import traci
import argparse
import numpy as np
import datetime
import torch
from sac import SAC
from torch.utils.tensorboard import SummaryWriter
from replay_memory import ReplayMemory
from demand_modeling import Demand_Modeling
from reward_modeling import Reward_Modeling
from para_dict import *
from utils import generate_routefile

parser = argparse.ArgumentParser(description='PyTorch Soft Actor-Critic Args')
parser.add_argument('--env-name', default="HalfCheetah-v2",
                    help='Mujoco Gym environment (default: HalfCheetah-v2)')
parser.add_argument('--policy', default="Gaussian",
                    help='Policy Type: Gaussian | Deterministic (default: Gaussian)')
parser.add_argument('--eval', type=bool, default=True,
                    help='Evaluates a policy a policy every 10 episode (default: True)')
parser.add_argument('--gamma', type=float, default=0.99, metavar='G',
                    help='discount factor for reward (default: 0.99)')
parser.add_argument('--tau', type=float, default=0.005, metavar='G',
                    help='target smoothing coefficient(τ) (default: 0.005)')
parser.add_argument('--lr', type=float, default=0.0003, metavar='G',
                    help='learning rate (default: 0.0003)')
parser.add_argument('--alpha', type=float, default=0.2, metavar='G',
                    help='Temperature parameter α determines the relative importance of the entropy\
                            term against the reward (default: 0.2)')
parser.add_argument('--automatic_entropy_tuning', type=bool, default=False, metavar='G',
                    help='Automaically adjust α (default: False)')
parser.add_argument('--seed', type=int, default=123456, metavar='N',
                    help='random seed (default: 123456)')
parser.add_argument('--batch_size', type=int, default=256, metavar='N',
                    help='batch size (default: 256)')
parser.add_argument('--num_steps', type=int, default=1000001, metavar='N',
                    help='maximum number of steps (default: 1000000)')
parser.add_argument('--hidden_size', type=int, default=256, metavar='N',
                    help='hidden size (default: 256)')
parser.add_argument('--updates_per_step', type=int, default=1, metavar='N',
                    help='model updates per simulator step (default: 1)')
parser.add_argument('--start_steps', type=int, default=10000, metavar='N',
                    help='Steps sampling random actions (default: 10000)')
parser.add_argument('--target_update_interval', type=int, default=1, metavar='N',
                    help='Value target update per no. of updates per step (default: 1)')
parser.add_argument('--replay_size', type=int, default=1000000, metavar='N',
                    help='size of replay buffer (default: 10000000)')
parser.add_argument('--cuda', action="store_true",
                    help='run on CUDA (default: False)')
args = parser.parse_args()

# Agent
agent = SAC()

# Tensor_board
writer = SummaryWriter('runs/{}_SAC'.format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

# Memory
memory = ReplayMemory()

# Parameters
maximum_steps = 10000000
maximum_episode_steps = 3600
# agent will act randomly at first
start_steps = 6000
batch_size = 256
updates_per_step = 1
last_time_green = 10
last_time_yellow = 3
last_time_all_red = 3
retrospective_length = 196
blame = 0.8
punish = 0.2  # TODO

# Training Loop
total_steps = 0
updates = 0
for i_episode in itertools.count(1):
    episode_reward = 0
    episode_steps = 0
    done = False

    # Start an instance of env
    # we need to import python modules from the $SUMO_HOME/tools directory
    generate_routefile()
    traci.start(["sumo", "-c", "Data/Metro_Intersection.sumocfg"], label="sim1")

    # we use action_old to store the old action for comparing
    action_old = None
    while not done:
        # state definition
        demand = Demand_Modeling(retrospective_length=retrospective_length, edge_id=edgeID_list, blame=blame,
                                 u_section_anchor=u_section_anchor)
        absolute_demand = demand.get_absolute_demand()
        relative_demand = demand.get_relative_demand()
        total_demand = list(map(lambda x: x[0] + x[1], zip(absolute_demand, relative_demand)))

        # select action
        if start_steps > total_steps:
            action = np.random.randint(1, 8)  # Sample random action
        else:
            if agent.select_action(total_demand) == 8:
                action = 8
            else:
                action = agent.select_action(total_demand) // 1 + 1  # Sample action from policy
        print(action)

        # control the traffic signal according to the action
        # when the phase has been changed, a 3s all red will be conducted
        # at the end of a 10s green, a 3s yellow will be conducted
        if not action_old:
            pass
        else:
            if action == action_old:
                pass
            else:
                traci.trafficlight.setPhase("SmartMetro", 2 * (action_old - 1) + 1)
                for i in range(last_time_yellow):
                    traci.simulationStep()
                    episode_steps += 1
                    total_steps += 1
                traci.trafficlight.setPhase("SmartMetro", 16)
                for i in range(last_time_all_red):
                    traci.simulationStep()
                    episode_steps += 1
                    total_steps += 1

        traci.trafficlight.setPhase("SmartMetro", 2 * (action - 1))
        for i in range(last_time_green):
            traci.simulationStep()
            episode_steps += 1
            total_steps += 1
        action_old = action

        if len(memory) > batch_size:
            # Number of updates per step in environment
            for i in range(updates_per_step):
                # Update parameters of all the networks
                # default 1
                critic_1_loss, critic_2_loss, policy_loss, ent_loss, alpha = agent.update_parameters(memory,
                                                                                                     batch_size,
                                                                                                     updates)
                # updates is just a counting parameter

                writer.add_scalar('loss/critic_1', critic_1_loss, updates)
                writer.add_scalar('loss/critic_2', critic_2_loss, updates)
                writer.add_scalar('loss/policy', policy_loss, updates)
                writer.add_scalar('loss/entropy_loss', ent_loss, updates)
                writer.add_scalar('entropy_temperature/alpha', alpha, updates)
                updates += 1

        # next_state definition
        demand = Demand_Modeling(retrospective_length=retrospective_length, edge_id=edgeID_list, blame=blame,
                                 u_section_anchor=u_section_anchor)
        absolute_demand = demand.get_absolute_demand()
        relative_demand = demand.get_relative_demand()
        total_demand_ = list(map(lambda x: x[0] + x[1], zip(absolute_demand, relative_demand)))

        # reward definition
        reward_model = Reward_Modeling(retrospective_length=retrospective_length, edge_id=edgeID_list, blame=blame,
                                       u_section_anchor=u_section_anchor)
        max_accumulated_waiting_time = reward_model.get_max_veh_accumulated_waiting_time()
        reward = -(punish * max_accumulated_waiting_time + sum(total_demand_))

        # done definition
        # simulation breaks when the time comes to 3600s
        if episode_steps >= maximum_episode_steps:
            done = True

        episode_reward = reward
        queue = sum(total_demand_)

        # Ignore the "done" signal if it comes from hitting the time horizon.
        # (https://github.com/openai/spinningup/blob/master/spinup/algos/sac/sac.py)
        mask = 1 if episode_steps == maximum_episode_steps else float(not done)

        memory.push(total_demand, action, reward, total_demand_, mask)  # Append transition to memory

    if total_steps > maximum_steps:
        break

    traci.close()

    writer.add_scalar('reward/train', episode_reward, i_episode)
    print("Episode: {}, total steps: {}, episode steps: {}, queue: {}, reward: {}".format(i_episode, total_steps,
                                                                                          episode_steps,
                                                                                          round(queue, 2), reward
                                                                                          ))
