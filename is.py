# @author  Wolfie
# @date    2021-05-18

import math
import gym
import numpy as np
from abc import ABC
import traci


class ISpilloverEnv(gym.Env, ABC):
    """
    Description:
        An intersection considers spillover, and you need design a
        signal control strategy to maximum number of vehicles passing
        through the intersection.


    Observation:
        Type: Matrix([])

    Actions:
        Type: Discrete(8)
        Num   Action
        0     north_south_through
        1     north_south_left
        2     east_west_through
        3     east_west_left
        4     north_through_left
        5     west_through_left
        6     south_through_left
        7     east_through_left

    Reward:
        The number of vehicles passing through the intersection in an episode

    Starting State:
        All observations are assigned a matrix with zeros

    Episode Termination:
    """

    def __init__(self):
        self.action_space = gym.spaces.Discrete(8)
        self.observation_space = gym.spaces.Box(low, high=, shape=, dtype=np.float32)

        self.seed()
        self.state = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        sumoBinary = "D:/sumo/bin/sumo-gui"
        sumoCmd = [sumoBinary, "-c", "Metro_Intersection.sumocfg"]
        traci.start(sumoCmd)

        self.state
        reward
        done

