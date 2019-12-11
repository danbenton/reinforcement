import numpy as np

class Bandit: 
    """
    Bandit - performes decision on which lever to execute based on 
    expected rewards for given levers. 

    params: 
    ------
    epsilon (float): probability with which a non optimal lever 
    will be chosen (exploration)
    """
    def __init__(self, epsilon, n_levers): 
        self.epsilon = epsilon
        self.n_levers = n_levers
        self.expected_rewards = np.zeros(n_levers)
        self.plays = np.zeros(n_levers)
        self.play_order = []
        self.best_lever = None
        self.optimal = []
        self.rewards = []

    def get_lever_to_pull(self): 
        """
        Return value of lever to pull.  Chooses best lever vs. all others 
        based on value of epsilon
        """

        # Return random lever if first pull    
        if not self.best_lever: 
            return np.random.choice(self.n_levers)

        # Return best layer if the bandit never explores
        if self.epsilon == 0:
            return self.best_lever

        if np.random.choice(['exploit', 'explore'], 
                            p=(1-self.epsilon, self.epsilon)) == 'exploit': 
            return self.best_lever
    
        # Explore with a randomly selected lever from uniform distribution 
        return np.random.choice(np.delete(np.arange(self.n_levers), self.best_lever)) 


    def update_lever_rewards(self, reward, lever, optimal): 
        """
        Update lever rewards and plays from output of slots
        params:
        ------
        reward (float): numerical value of reward
        lever (int): value of lever which yielded reward
        """
        self.rewards.append(reward)
        self.plays[lever] += 1
        self.expected_rewards[lever] += \
            ((1 / self.plays[lever]) * (reward - self.expected_rewards[lever]))
        self.best_lever = np.argmax(self.expected_rewards)
        self.optimal.append(optimal)
        self.play_order.append(lever)