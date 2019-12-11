import sys

import numpy as np
import pandas as pd

from bandit import Bandit
from slots import Slots


class Game: 

    def __init__(self, epsilon, mus, sigmas, steps): 
        self.bandit = Bandit(epsilon=epsilon, n_levers=len(mus))
        self.slots = Slots(mus=mus, sigmas=sigmas)
        self.steps = steps
        self.summary = {}
    

    def run_sim(self): 
        """Simulate n number of lever pulls."""
        for _ in range(self.steps):  
            lever = self.bandit.get_lever_to_pull()
            reward, optimal = self.slots.get_reward(lever)
            self.bandit.update_lever_rewards(reward, lever, optimal)
        self.game_summary()

    
    def game_summary(self): 
        """
        Return Game Summary for n number of level pulls. 
        Including rewards from bandit and optimal %.
        """
        self.summary['optimal'] = np.mean(self.bandit.optimal)
        self.summary['rewards'] = np.mean(self.bandit.rewards)
        self.summary['epsilon'] = self.bandit.epsilon


    def __repr__(self): 
        """
        Repr function for game class - return summary 
        """
        return f"""
                Game to {self.steps}
                Bandit rewards = {self.summary['rewards']}
                Bandit Optimal = {self.summary['optimal'] * 100}%
                Bandit Epsilon = {self.bandit.epsilon}
                Best Lever = {self.bandit.best_lever}
                """


class Epoch:    
    """
    Run n number of games and record averages of games
    """
    def __init__(self, n_epochs, epsilon, mus, sigmas, steps): 
        self.epsilon = epsilon
        self.mus = mus
        self.sigmas = sigmas
        self.steps = steps
        self.n_epochs = n_epochs
        self.epochs_run = {}
        self.num_runs = 0

    def make_game(self, new_sigmas=None):
        sigmas = self.sigmas
        if new_sigmas: 
            sigmas = new_sigmas
        return Game(epsilon=self.epsilon, mus=self.mus, sigmas=sigmas, steps=self.steps)

    def capture_stats(self, cust_game=None): 
        """Capture all stats for games run n_epoch times.
        params:
        ------
        cust_game (class game): altered form of game - curent iteration is just sigmas
        """
        rewards = []
        optimals = []
        for i in range(self.n_epochs):
            game = self.make_game()
            if cust_game: 
                game = cust_game
            game.run_sim()
            rewards.append(game.bandit.rewards)
            optimals.append(game.bandit.optimal)
            sys.stdout.write(f'\rRunning Epoch: {i}')
        tweak = True if cust_game else False 
        self.epochs_run[str(self.num_runs)] = {'rewards': rewards, 
                                              'optimals': optimals, 
                                              'sigmas': game.slots.sigmas, 
                                              'mus':game.slots.mus, 
                                              'epsilon': game.bandit.epsilon,
                                              'steps': game.steps, 
                                              'tweak': tweak}
        self.num_runs += 1
    
    def tweak_sigmas(self, ratio=None, constant=None): 
        assert ratio == None or constant == None
        if ratio: 
            sigmas = np.array(self.mus) * ratio
        if constant: 
            sigmas = np.array(constant * len(self.mus))
        game = self.make_game(new_sigmas=sigmas)
        self.capture_stats(cust_game=game)
