# @author  Wolfie
# @date    2021-05-24

import itertools
import traci

# Training Loop
total_numsteps = 0
updates = 0
for i_episode in itertools.count(1):
    # step = 1
    episode_reward = 0
    episode_steps = 0
    done = False
    state = # env.reset()

    sumoBinary = "D:/sumo/bin/sumo-gui"
    sumoCmd = [sumoBinary, "-c", "Metro_Intersection.sumocfg"]
    traci.start(sumoCmd)
    # Start an instance of env

    while not done:
        if args.start_steps > total_numsteps:
            action = env.action_space.sample()  # Sample random action
            # TODO
        else:
            action = agent.select_action(state)  # Sample action from policy

        if len(memory) > args.batch_size:
            # Number of updates per step in environment
            for i in range(args.updates_per_step):
                # Update parameters of all the networks
                # default 1
                critic_1_loss, critic_2_loss, policy_loss, ent_loss, alpha = agent.update_parameters(memory, args.batch_size, updates)
                # updates is just a counting parameter

                writer.add_scalar('loss/critic_1', critic_1_loss, updates)
                writer.add_scalar('loss/critic_2', critic_2_loss, updates)
                writer.add_scalar('loss/policy', policy_loss, updates)
                writer.add_scalar('loss/entropy_loss', ent_loss, updates)
                writer.add_scalar('entropy_temprature/alpha', alpha, updates)
                updates += 1
        # next_state definition

        # reward definition

        # done definition
        if episode_steps >= 3600:
            done = True


        next_state, reward, done, _ = env.step(action) # Step
        episode_steps += 1
        total_numsteps += 1
        episode_reward += reward

        # Ignore the "done" signal if it comes from hitting the time horizon.
        # (https://github.com/openai/spinningup/blob/master/spinup/algos/sac/sac.py)
        mask = 1 if episode_steps == env._max_episode_steps else float(not done)

        memory.push(state, action, reward, next_state, mask) # Append transition to memory

        state = next_state

    if total_numsteps > args.num_steps:
        break

    writer.add_scalar('reward/train', episode_reward, i_episode)
    print("Episode: {}, total numsteps: {}, episode steps: {}, reward: {}".format(i_episode, total_numsteps, episode_steps, round(episode_reward, 2)))