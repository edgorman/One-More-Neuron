""" Reinforcement Learning file
"""
import numpy as np
from .agent import Agent


class ReinforcementLearning(Agent):
    """ This is the Reinforcement Learning class """
    # https://colab.research.google.com/drive/1E2RViy7xmor0mhqskZV14_NUj2jMpJz3

    def __init__(self, episode=10, env_rows=9, env_cols=16):
        self.episode = episode
        self.epsilon = 0.3
        self.dis_fact = 0.9
        self.learn_rate = 0.9
        self.env_rows = env_rows
        self.env_cols = env_cols

        self.actions = [x for x in range(10, 180, 10)]
        self.q_values = np.zeros((self.env_rows * self.env_cols, len(self.actions)), dtype=np.int8)

    def get_env_state(self, block_info):
        """ Return the state of the env as a 1D array """
        # Convert environment to 1D array
        env_array = np.zeros((self.env_rows * self.env_cols), dtype=np.int8)
        last_block_pos = 0
        for block in block_info:
            x, y = block.get_position()
            curr_block_pos = (y * self.env_cols) + x

            if curr_block_pos >= self.env_rows * self.env_cols:
                break

            empty_indexes = [i for i in range(last_block_pos, curr_block_pos)]
            last_block_pos = curr_block_pos

            np.put(env_array, empty_indexes, [0]*len(empty_indexes))
            np.put(env_array, [curr_block_pos], [1])
        return env_array

    def on_round_start(self, block_info):
        """ this method is called before the round is started """
        env_array = self.get_env_state(block_info)

        # Determine next move
        if np.random.random() < self.epsilon:
            return self.actions[np.argmax(self.q_values[env_array])]
        else:
            return self.actions[np.random.randint(len(self.actions))]

    def on_game_finish(self):
        """ this method is called each time a game is finished """
        # Return whether a new round should be started
        self.episode -= 1
        return self.episode > 0

    def on_round_end(self, block_info, ball_info, action):
        """ this method is called each time a round is finished """
        reward = 0

        # Check if game is in end state
        for block in block_info:
            _, y = block.get_position()
            if y >= self.env_rows:
                reward -= 100
                break

        # Reward number of blocks hit per ball
        for ball in ball_info:
            reward += ball.get_hit_count()

        # Update q value with reward
        env_array = self.get_env_state(block_info)
        action_index = self.actions.index(action)
        self.q_values[env_array, action_index] = self.q_values[env_array, action_index] + self.learn_rate \
            * (reward + (self.dis_fact * np.max(self.q_values[env_array])) \
            - self.q_values[env_array, action_index])
