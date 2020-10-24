""" Main File
"""
from src.game import Game
from src.rflearn import ReinforcementLearning

if __name__ == "__main__" :
    agent = ReinforcementLearning()
    game = Game(agent)
    game.on_start()
