"""One-More-Neuron Game File
"""
import gym

test_gym = gym.make('one_more_neuron:omn-v0')

running = 1
while running == 1:
    _, _, running, _ = test_gym.step(0)
    test_gym.render()

# test_gym.step(None)
# test_gym.reset()
# test_gym.render()
# test_gym.close()
