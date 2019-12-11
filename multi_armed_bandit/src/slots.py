import numpy as np

class Slots: 
    """
    k armed slots with normal payout.  
    params: 
    ------
    mus (array): mean of payout per arm
    sigmas (array): variance of payout per arm
    """
    def __init__(self, mus, sigmas): 
        self.mus = mus
        self.sigmas = sigmas

    def get_reward(self, lever):
        """
        Return value of reward given lever.
        params:
        ------
        k (int): number of levers to build for slot class

        returns: 
        ------
        Value (float) given distribution according to mus and sigmas for given lever.  
        """
        rewards = [np.random.normal(mu, sigma) for mu, sigma in zip(self.mus, self.sigmas)]
        reward = rewards[lever]
        if lever == np.argmax(rewards): 
            return reward, True
        return reward, False