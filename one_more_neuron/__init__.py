from gym.envs.registration import register

register(
    id='omn-v0',
    entry_point='one_more_neuron.envs:OMN',
)