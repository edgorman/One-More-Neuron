"""One-More-Neuron Game File
"""
import os
import gym
import matplotlib.pyplot as plt
from one_more_neuron.deepqn import DQN
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


if __name__ == "__main__":
    # Generate environment
    env = gym.make('one_more_neuron:omn-v0')
    model_dir = os.getcwd() + "\\models\\"

    # DeepQL variables
    gamma   = 0.9
    epsilon = .95
    trials  = 500
    max_trial_len = 100

    # DepQL history
    rewards_history = []
    level_history = []

    # DeepQL learning loop
    dqn_agent = DQN(env=env)
    max_level = 0
    for trial in range(trials):

        # Reset env and get state
        cur_state = env.reset()
        trial_reward = 0

        for step in range(max_trial_len):
            action = dqn_agent.act(cur_state)
            new_state, reward, done, _ = env.step(action)

            # reward = reward if not done else -20
            dqn_agent.remember(cur_state, action, reward, new_state, done)
            # internally iterates default (prediction) model
            dqn_agent.replay()
            # iterates target model
            dqn_agent.target_train()

            trial_reward += reward
            cur_state = new_state

            print("Trial", trial, "/", trials, "; Max level: ", max_level)
            env.render()
            if done:
                break

        rewards_history.append(trial_reward)
        level_history.append(env.get_level())

        if env.get_level() > max_level:
            max_level = env.get_level()

        if env.get_level() < max_trial_len:
            if trial % 5 == 0:
                print("by", trial, "achieved max level of", max_level)
                # dqn_agent.save_model(model_dir + "trial-{}.model".format(trial))
        else:
            print("Completed in {} trials".format(trial))
            # dqn_agent.save_model(model_dir + "success.model")
            break

    plt.figure(figsize=(14,7))
    plt.plot(range(len(rewards_history)),rewards_history)
    plt.xlabel('Games played')
    plt.ylabel('Reward')
    plt.show()

    plt.figure(figsize=(14,7))
    plt.plot(range(len(level_history)),level_history)
    plt.xlabel('Games played')
    plt.ylabel('Level')
    plt.show()
