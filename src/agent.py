""" Agent File
"""
from abc import ABC, abstractmethod

class Agent(ABC):
    """ This is the Agent class, parent to AI classes """

    def __init__(self):
        pass

    @abstractmethod
    def on_round_start(self):
        """ this method is called before the round is started """

    @abstractmethod
    def on_game_finish(self):
        """ this method is called each time a game is finishe """

    @abstractmethod
    def on_round_end(self):
        """ this method is called each time a round is finished """
