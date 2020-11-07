import gym

class OMN(gym.Env):

    def __init__(self):
        print('init basic')

    def step(self, action):
        print('step')

    def reset(self):
        print('reset')

    def render(self, mode='human'):
        print('render')

    def close(self):
        print('close')
