from train_and_evaluate import Train_and_Evaluate
from config import Config

config = Config()
config.punish = 0.2
config.blame = 0.3
config.batch_size = 256
config.updates_per_step = 1
config.start_steps = 7200
config.maximum_total_steps = 10000000
config.retrospective_length = 120
config.seed = 123
config.buffer_size = 100000

if __name__ == "__main__":
    trainer_and_evaluater = Train_and_Evaluate(config)
    trainer_and_evaluater.train_and_evaluate()