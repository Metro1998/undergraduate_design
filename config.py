class Config(object):
    """ Object to hold the config requirements for an agent/game """
    def __init__(self):
        self.seed = None
        self.batch_size = None
        self.buffer_size = None
        self.maximum_total_steps = None
        self.start_steps = None
        self.updates_per_step = None
        self.retrospective_length = None
        self.blame = None
        self.punish = None

        # static constant
        self.maximum_episode_steps = 3600
        self.last_time_green = 10
        self.last_time_yellow = 3
