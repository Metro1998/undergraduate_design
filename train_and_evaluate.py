# @author  Wolfie
# @date    2021-05-24
# @date_seconddly_revise 2021-08-25

import itertools
import traci
import numpy as np
import datetime
from sac import SAC
from torch.utils.tensorboard import SummaryWriter
from utilities.replay_memory import ReplayMemory
from utilities.demand_modeling import Demand_Modeling
from utilities.reward_modeling import Reward_Modeling
from utilities.para_dict import *
from utilities.utilities import generate_routefile, plot1, plot2, plot3


class Train_and_Evaluate(object):
    def __init__(self, config):
        self.config = config

    def train_and_evaluate(self):
        # constant
        maximum_episode_steps = self.config.maximum_episode_steps
        last_time_green = self.config.last_time_green
        last_time_yellow = self.config.last_time_yellow

        # Hypaarameters
        maximum_total_steps = self.config.maximum_total_steps
        start_steps = self.config.start_steps
        batch_size = self.config.batch_size
        updates_per_step = self.config.updates_per_step
        retrospective_length = self.config.retrospective_length
        blame = self.config.blame
        punish = self.config.punish
        buffer_size = self.config.buffer_size
        seed = self.config.seed

        # Agent
        agent = SAC()

        # Tensor_board
        writer = SummaryWriter('runs/{}_SAC'.format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

        # Memory
        memory = ReplayMemory(buffer_size=buffer_size, seed=seed)

        # Training Loop
        total_steps = 0
        updates = 0
        avg_queue_list = []
        avg_waiting_list = []
        alpha_list = []

        for i_episode in itertools.count(1):

            episode_reward = 0
            episode_steps = 0
            episode_queue = 0
            action_count = 0
            done = False
            episode_max_accumulated_waiting_time = 0
            avg_accumulated_waiting_time = 0
            reward = 0
            light = 0

            # Start an instance of env
            # we need to import python modules from the $SUMO_HOME/tools directory
            # generate_routefile()
            traci.start(["sumo", "-c", "road_network_doc/Metro_Intersection.sumocfg"], label="sim1")

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
                action_count += 1

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
                        """
                        traci.trafficlight.setPhase("SmartMetro", 16)
                        for i in range(last_time_all_red):
                            traci.simulationStep()
                            episode_steps += 1
                            total_steps += 1
                        """
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
                absolute_demand = demand.get_absolute_demand()
                relative_demand = demand.get_relative_demand()
                total_demand_ = list(map(lambda x: x[0] + x[1], zip(absolute_demand, relative_demand)))

                # evaluation
                # once an action is chosen, the evaluation starts

                # 1.queue
                queue = Demand_Modeling(retrospective_length=196, edge_id=edgeID_list, blame=0,
                                        u_section_anchor=u_section_anchor)
                absolute_queue = queue.get_absolute_demand()
                relative_queue = queue.get_relative_demand()
                queue_list = list(map(lambda x: x[0] + x[1], zip(absolute_demand, relative_demand)))
                queue_for_one_action = sum(queue_list)
                episode_queue += queue_for_one_action

                # 2.waiting time
                reward_model = Reward_Modeling(retrospective_length=retrospective_length, edge_id=edgeID_list,
                                               u_section_anchor=u_section_anchor)
                max_accumulated_waiting_time = reward_model.get_max_veh_accumulated_waiting_time()
                if max_accumulated_waiting_time > episode_max_accumulated_waiting_time:
                    episode_max_accumulated_waiting_time = max_accumulated_waiting_time

                if episode_steps > 1800 and light == 0:
                    avg_accumulated_waiting_time = reward_model.get_avg_veh_accumulated_waiting_time()
                    light = 1

                # reward definition

                reward = -(punish * max_accumulated_waiting_time + sum(total_demand_))

                # done definition
                # simulation breaks when the time comes to 3600s
                if episode_steps >= maximum_episode_steps:
                    done = True

                episode_reward = reward

                # Ignore the "done" signal if it comes from hitting the time horizon.
                # (https://github.com/openai/spinningup/blob/master/spinup/algos/sac/sac.py)
                mask = 1 if episode_steps == maximum_episode_steps else float(not done)

                memory.push(total_demand, action, reward, total_demand_, mask)  # Append transition to memory

            if total_steps > maximum_total_steps:
                break

            traci.close()
            avg_queue = episode_queue / action_count
            avg_queue_list.append(avg_queue)
            avg_waiting_list.append(avg_accumulated_waiting_time)
            alpha = agent.get_alpha()
            alpha_list.append(alpha)

            writer.add_scalar('reward/train', episode_reward, i_episode)
            print(
                "Episode: {}, total steps: {}, episode steps: {}, avg_queue: {}, avg_ac_waiting_time: {}, reward: {}".format(
                    i_episode, total_steps, episode_steps, round(avg_queue, 2), avg_accumulated_waiting_time, reward))
            plot1(avg_queue_list)
            plot2(avg_waiting_list)
            plot3(alpha_list)

