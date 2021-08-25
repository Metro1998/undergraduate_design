import random
import numpy as np


class ReplayMemory(object):
    def __init__(self, buffer_size, seed):
        random.seed(seed)
        self.capacity = buffer_size
        self.buffer = []
        self.position = 0

    def push(self, state, action, reward, next_state, done):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = map(np.stack, zip(*batch))
        # road_network_doc from zip(*batch) do np.stack
        return state, action, reward, next_state, done

    def __len__(self):
        return len(self.buffer)
