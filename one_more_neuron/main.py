import gym

test_gym = gym.make('one_more_neuron:omn-v0')
test_gym.step(None)
test_gym.reset()
test_gym.render()
test_gym.close()
