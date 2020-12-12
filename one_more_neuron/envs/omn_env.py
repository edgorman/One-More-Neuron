"""One-More-Neuron Environment File
"""
import math
import random
from datetime import datetime
import numpy as np
import gym
from .block import Block
from .ball import Ball

SCREEN_WIDTH = 1205
SCREEN_HEIGHT = 720

GAME_TICK_SPEED = 60

BLOCK_WIDTH = 70
BLOCK_WIDTH_MAX = 16
BLOCK_HEIGHT = 70
BLOCK_HEIGHT_MAX = 9
BLOCK_BETWEEN_GAP = 5
BLOCK_SPAWN_THRESHOLD = 0.5

BALL_RADIUS = 10
BALL_START_X = ((BLOCK_WIDTH_MAX+1)/2) * BLOCK_WIDTH
BALL_START_Y = (BLOCK_HEIGHT_MAX+1) * BLOCK_HEIGHT

class OMN(gym.Env):
    """ This is the game environment for One More Neuron based off the Gym environment class """

    def __init__(self):
        # Render variables
        self.size = (SCREEN_WIDTH, SCREEN_HEIGHT)

        # Game variables
        self.game_running = True
        self.blocks = []
        self.balls = []
        self.balls_left = 0
        self.level = 0
        self.level_active = False
        self.level_start_time = None

        # Agent variables
        self.reward = 0
        self.actions = [x for x in range(10, 180, 10)]

    def get_actions(self):
        return self.actions

    def get_n_actions(self):
        return len(self.actions)

    def get_obs_space(self):
        return self._get_obs()

    def get_level(self):
        return self.level

    @property
    def _n_actions(self):
        return len(self.actions)

    def _get_obs(self):
        # Convert environment to 2D np array
        env_array = np.zeros((BLOCK_HEIGHT_MAX * BLOCK_WIDTH_MAX), dtype=np.int8)
        block_indexes = []

        # Get pos index of each block
        for block in self.blocks:
            x, y = block.get_position()
            if y >= BLOCK_HEIGHT_MAX:
                break
            block_indexes.append((y * BLOCK_WIDTH_MAX) + x)

        # Update array with block positions
        np.put(env_array, block_indexes, np.ones((len(block_indexes)), dtype=np.int8))
        env_array = env_array.reshape(BLOCK_HEIGHT_MAX, BLOCK_WIDTH_MAX)
        return env_array

    def step(self, action):
        # Process action
        action_angle = math.radians(self.actions[action])
        action_vector = np.array([math.cos(action_angle), math.sin(action_angle)])
        action_norm = np.linalg.norm(action_vector)
        action_output = action_vector / action_norm

        # Set up new round
        self.level += 1
        self.level_active = True
        self.level_start_time = datetime.now()

        # Set up balls
        self.balls.append(
            Ball(
                BALL_START_X,
                BALL_START_Y,
                BALL_RADIUS,
                self.level,
                (255, 255, 255)
            )
        )
        self.balls_left = len(self.balls)
        for ball in self.balls:
            ball.set_velocity(action_output[0], action_output[1])
            ball.set_delay(self.level_start_time)

        # Set up blocks
        for index in range(BLOCK_WIDTH_MAX):
            if random.random() <= BLOCK_SPAWN_THRESHOLD:
                self.blocks.append(
                    Block(
                        index,
                        0,
                        BLOCK_WIDTH,
                        BLOCK_HEIGHT,
                        BLOCK_BETWEEN_GAP,
                        self.level,
                        (255, 255, 255)
                    )
                )

        # While round is active
        while self.level_active:

            # Update balls
            for ball in self.balls:
                # if ball has pased delay
                if ball.get_delay() <= datetime.now():
                    new_x, new_y = ball.get_new_position()
                    max_x, max_y = self.size
                    ball_r = ball.get_radius()
                    invert_x, invert_y = False, False

                    # if ball hit corner of screen
                    if (new_x - ball_r <= 0 or new_x + ball_r >= max_x) and \
                    (new_y - ball_r <= 0 or new_y + ball_r >= max_y):
                        invert_x = True
                        invert_y = True
                    # if ball hit left or right sides of screen
                    elif new_x - ball_r <= 0 or new_x + ball_r >= max_x:
                        invert_x = True
                    # if ball hit top or bottom sides of screen
                    elif new_y - ball_r <= 0 or new_y + ball_r >= max_y:
                        if new_y + ball_r >= max_y:
                            ball.hit_floor()
                        invert_y = True

                    # for each block check if hit
                    for block in self.blocks:
                        # https://stackoverflow.com/a/402010
                        block_center_x, block_center_y = block.get_center_position()
                        block_distance_x, block_distance_y = (
                            abs(new_x - block_center_x),
                            abs(new_y - block_center_y)
                        )

                        # if ball is far beyond block
                        if (block_distance_x > (BLOCK_WIDTH/2 + ball.get_radius())) or \
                            (block_distance_y > (BLOCK_HEIGHT/2 + ball.get_radius())):
                            continue
                        # if ball is intersecting in x direction
                        elif block_distance_x <= (BLOCK_WIDTH/2):
                            ball.hit_block()
                            block.hit_ball()
                            invert_y = True
                        # if block is intersection in y direction
                        elif block_distance_y <= (BLOCK_HEIGHT/2):
                            ball.hit_block()
                            block.hit_ball()
                            invert_x = True
                        # else block is intersecting ?
                        else:
                            ball.hit_block()
                            block.hit_ball()
                            if block_distance_x > block_distance_y:
                                invert_x = True
                            else:
                                invert_y = True

                    # if ball has ran out of health
                    if ball.get_health() <= 0:
                        ball.reset()
                        self.balls_left -= 1
                    # else get next position of ball
                    else:
                        if invert_x:
                            ball.invert_x_velocity()
                        if invert_y:
                            ball.invert_y_velocity()
                        new_x, new_y = ball.get_new_position()
                        ball.set_position((new_x, new_y))

            # Update blocks
            for block in list(self.blocks):
                if block.get_health() <= 0:
                    self.blocks.remove(block)

            # Check if round ended
            if self.balls_left <= 0:
                self.level_active = False

        # Round has ended
        # Calculate reward
        self.reward = 0
        for ball in self.balls:
            self.reward += ball.get_hit_count()

        # Move blocks down
        for block in self.blocks:
            block.move_down()

        # Check if game is over
        for block in self.blocks:
            _, y = block.get_position()
            if y >= BLOCK_HEIGHT_MAX:
                self.reward = -100
                self.game_running = False

        # Return observation, reward, done, info
        return self._get_obs(), self.reward, int(not self.game_running), None


    def reset(self):
        # Reset the environment
        self.game_running = True
        self.blocks = []
        self.balls = []
        self.balls_left = 0
        self.level = 0
        self.level_active = False
        self.level_start_time = None

        # Return observation
        return self._get_obs()

    def render(self, mode='human'):
        state = self._get_obs()

        print("One More Neuron. Level", self.level, "; Reward", self.reward)
        print(state)
        print("----------------------------------")

    def close(self):
        print('close')
