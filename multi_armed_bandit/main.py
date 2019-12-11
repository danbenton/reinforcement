import argparse

import numpy as np

from bandit import Bandit
from game_ops import Game
from slots import Slots

mus = [2, 4, 6, 8, 100]
sigmas = [.1, .1, .1, .1, .1]
epsilon = .4
steps = 2000
game = Game(mus=mus, sigmas=sigmas, epsilon=epsilon, steps=steps)
def main(): 
    pass



if __name__ == "__main__": 


    main()
