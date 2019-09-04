import numpy as np
from collections import defaultdict, Counter
import math

class Dice:
    """
    A Dice - Fill in with right class names.
    """
    def __init__(self):
        self.value = self._get_value()

    def _get_value(self):
        """ :return: random number between 1-6 """
        return np.random.randint(1, 7)

    @staticmethod
    def get_points(n):
        """ :return: dice points if either a 5 or 1 is rolled """
        if n == 5:
            return 50
        if n == 1:
            return 100

    def __call__(self):
        """ Makes object callable - returns value of object """
        return self.value


class Hand:
    """
    A Hand - score combining n number of dice.
    """
    def __init__(self, n_dice):
        """
        :param n_dice: integer
        """
        self.roll = []
        self._get_roll(n_dice)

    def _get_roll(self, n_dice):
        """
        Occurance of n number of Dice.
        :param n_dice: n number of dice values

        :return:
        """
        for _ in np.arange(n_dice):
            dice = Dice()
            self.roll.append(dice())

    def __call__(self):
        """ Make Class callable"""
        return sorted(self.roll)


class Player:
    """
    A Player - has a hand, score and decision
    """

    def __init__(self, name):
        self.score = 0
        self.name = name
        self.n_dice = 6
        self.hand = None
        self.turn_score = 0
        self.cHand = None

    def roll(self, n_dice):
        self.hand = Hand(n_dice)
        self.cHand = Counter(self.hand())

    def _get_score(self, groups):
        """
        Calculate score of dice distribution.
        :param groups: itertools.Counter object - represents hand distribution
        :return: score of passed counter object.
        """
        score = 0
        for number in groups.keys():
            number_is_one = False
            val = 100
            if number == 1:
                val = 1000
                number_is_one = True
            score += number * val * math.floor(groups[number]/3)
            if number == 5 or number_is_one:
                num_times = groups[number] % 3
                score += Dice.get_points(number) * num_times
        return score

    def check_roll(self):
        """
        checks for cetain 6 dice combos
        :return: True if reroll is possible
        """
        if self.n_dice != 6:
            return False
        group_vals = set(self.cHand.values())
        if set(self.cHand.keys()).pop() == 6:
            self.score = 10000
            return True
        if group_vals == {1}:
            self.turn_score += 2000
            return True
        if group_vals == {2, 4} or\
                group_vals == {2} or\
                group_vals == {3}:
            self.turn_score += 1500
            return True

    def take(self):
        """
        List of integers on which to generate a temp score
        Remove n number of integers from self.n_dice
        :return: Nothing, update both score and self.n_dice
        """
        user_input = input('Take what dice? :')
        input_list = [int(x.strip()) for x in user_input.split(",")]
        self.turn_score += self._get_score(Counter(input_list))
        if len(input_list) == self.n_dice:
            self.n_dice = 6
        else:
            self.n_dice -= len(input_list)

    @staticmethod
    def re_roll():
        user_input = input('Re-Roll? [Yes / No] ')
        if 'y' in user_input.lower():
            return True
        return False


class Game:
    """
    A - game, with players and a score
    """
    def __init__(self, players, game_limit=10000):
        """

        :param args: player names
        """
        self.players = []
        for player_name in players:
            self.players.append(Player(player_name))
        self.score_audit = defaultdict(dict)
        self.game_limit = game_limit
        self.game_over = False

    def _get_player(self):
        """Get next player turn, append player to end."""
        player = self.players[0]
        self.players.append(self.players.pop(0))
        return player

    def turn(self):
        """

        :return:
        """
        player = self._get_player()
        turn_status = True
        player.turn_score = 0
        player.n_dice = 6
        roll_num = 0
        crap_out = False

        while turn_status:
            roll_num += 1
            player.roll(player.n_dice)
            check_5 = True if 5 in player.hand() else False
            check_1 = True if 1 in player.hand() else False
            check_multi = True if max(player.cHand.values()) > 2 else False
            print(f'\n######## Roll Number {roll_num} for {player.name} ########')
            print(f'Player Points: {player.score}')
            print(f'Roll: {player.hand()}')
            print('- -- --- ' * 4)
            if player.check_roll():
                print('BOOM!')
            elif check_1 or check_5 or check_multi:
                player.take()
                turn_status = player.re_roll()
            else:
                print('\nWhaa, whaaaa - Crap out!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                turn_status = False
                crap_out = True
            if player.score >= 10000:
                break
            print(f'Player Turn Points: {player.turn_score}')
        if not crap_out:
            player.score += player.turn_score

        if player.score > self.game_limit:
            self.end_game(player)

    def end_game(self, player):
        """
        Set game over variable to True, indicating winning condition met.
        :param player: Player Class
        :return: set game.game_over to True.  This value is checkec after every turn.
        """
        print(f'Game Over: {player.name} wins with {player.score} points!')
        self.game_over = True


def main():
    num_players = [x for x in input('Enter Player names ').split(',')]
    game_limit = int(input('Game Limit? '))
    game = Game(num_players, game_limit=game_limit)
    while not game.game_over:
       game.turn()


if __name__ == "__main__":
    main()
