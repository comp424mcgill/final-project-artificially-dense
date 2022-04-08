import numpy as np
from copy import deepcopy
import traceback
from agents import *
from time import sleep, time
import click
import logging
from store import AGENT_REGISTRY
from constants import *
import sys


class StudentWorld(Agent):
    def __init__(self, board, our_position, adv_position, max_step):
        """
        Initialize the world to the board given
        """
        super(StudentWorld, self).__init__()
        # Make a copy of the given information - info to not be modified
        self.chess_board_copy = deepcopy(board)
        self.our_pos_copy = deepcopy(our_position)
        self.adv_pos_copy = deepcopy(adv_position)

        # Load info as given in decorators
        self.chess_board = board
        self.our_pos = our_position
        self.adv_pos = adv_position

        # Moves (Up, Right, Down, Left)
        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

        # Opposite Directions
        self.opposites = {0: 2, 1: 3, 2: 0, 3: 1}

        # Maximum Steps
        self.max_step = max_step

        # Whose turn to step
        self.turn = False  # true being our turn, false being opponent's turn

        # Check initialization
        self.initial_end, _, _ = self.check_endgame()

        # Record the winner
        self.winner = -1  # 1 being we win, 0.5 being tie, 0 being we lose

        # Count how deep we want to go in the random search
        self.depth = 1

        # Moves (Up, Right, Down, Left)
        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """

        number_rand_actions = 1  # can change
        number_rand_trials = 1  # can change

        highest_prob = 0
        highest_prob_action = (0, 0), 0

        for _ in range(number_rand_actions):
            # Start from the same original board
            self.chess_board = deepcopy(self.board_copy)
            self.our_pos = deepcopy(self.our_pos_copy)
            self.adv_pos = deepcopy(self.adv_pos_copy)
            self.winner = -1
            sum = 0
            (rand_x, rand_y), direction = self.random_move(self.our_pos, self.adv_pos)
            ended, score1, score2 = self.check_endgame()
            if not ended:
                for _ in range(number_rand_trials):
                    sum += self.run_experiment()
                if sum / number_rand_trials > highest_prob:
                    highest_prob_action = (rand_x, rand_y), direction
            else:
                if self.winner > highest_prob:
                    highest_prob_action = (rand_x, rand_y), direction

            if highest_prob_action == 1:
                break

        return highest_prob_action

    def run_experiment(self):
        """
        Repeatedly run random walk for both players;
        If the game ended, return the winner; else, use heuristics (or minimax)
        Output:
        - Winning value
        """
        d = 0
        ended, score1, score2 = self.increase_depth()
        while (not ended) or (d < self.depth):
            ended, score1, score2 = self.increase_depth()
            d += 1
        if not ended:
            self.winner = heuristics()

        return self.winner

    def heuristics(self):
        """
        Return an approximate winning value
        """
        self.winner = 1
        return self.winner

    def increase_depth(self):
        """
        Take a Random Walk.

        Returns
        -------
        results: tuple
            The results of the step containing (is_endgame, player_1_score, player_2_score)
        """
        if self.turn:
            our_position = self.our_pos
            adv_position = self.adv_pos
        else:
            our_position = self.adv_pos
            adv_position = self.our_pos

        our_position, dir = self.random_move(our_position, adv_position)

        if self.turn:
            self.our_pos = our_position
        else:
            self.adv_pos = our_position
        # Set the barrier to True
        pos_x, pos_y = our_position
        self.set_barrier(pos_x, pos_y, dir)

        results = self.check_endgame()

        # Change turn
        self.turn = not self.turn

        return results

    def check_endgame(self):
        """
        Check if the game ends and compute the current score of the agents.

        Returns
        -------
        is_endgame : bool
            Whether the game ends.
        our_score : int
            Our score.
        adv_score : int
            The adversary's score.
        """
        # Union-Find
        father = dict()
        for pos_x in range(self.board_size):
            for pos_y in range(self.board_size):
                father[(pos_x, pos_y)] = (pos_x, pos_y)

        def find(pos):
            if father[pos] != pos:
                father[pos] = find(father[pos])
            return father[pos]

        def union(pos1, pos2):
            father[pos1] = pos2

        for pos_x in range(self.board_size):
            for pos_y in range(self.board_size):
                for dir, move in enumerate(self.moves[1:3]):  # Only check down and right
                    # Check if there is a wall between current position and down/right
                    if self.chess_board[pos_x, pos_y, dir + 1]:
                        continue
                    # If no wall, put the two into the same disjoint set
                    root_a = find((pos_x, pos_y))
                    root_b = find((pos_x + move[0], pos_y + move[1]))
                    if root_a != root_b:
                        union(root_a, root_b)

        for pos_x in range(self.board_size):
            for pos_y in range(self.board_size):
                find((pos_x, pos_y))  # Path compression of union find
        our_r = find(tuple(self.our_pos))
        adv_r = find(tuple(self.adv_pos))
        our_score = list(father.values()).count(our_r)
        adv_score = list(father.values()).count(adv_r)
        if our_r == adv_r:
            return False, our_score, adv_score

        if our_score > adv_score:
            if self.turn:
                self.winner = 1
            else:
                self.winner = 0
        elif p0_score < p1_score:
            if self.turn:
                self.winner = 0
            else:
                self.winner = 1
        else:
            self.winner = 0.5
        return True, our_score, adv_score

    def set_barrier(self, x, y, dir):
        # Set the barrier to True
        self.chess_board[x, y, dir] = True
        # Set the opposite barrier to True
        move = self.moves[dir]
        self.chess_board[x + move[0], y + move[1], self.opposites[dir]] = True

    def random_move(self, my_position, adv_position):
        """
        ** Reedited version
        Output:
        - a random move from the current position
        """
        ori_pos = deepcopy(my_position)
        steps = np.random.randint(0, self.max_step + 1)  # a random number of steps

        # Random Walk
        for _ in range(steps):
            my_x, my_y = my_position
            rand_step = np.random.randint(0, 4)
            rand_step_x, rand_step_y = self.moves[rand_step]
            my_position = (my_x + rand_step_x, my_y + rand_step_y)

            # Special Case enclosed by Adversary
            k = 0
            # If there's a wall or there's an adversary at the new place, change step
            while self.chess_board[my_x, my_y, rand_step] or my_position == adv_position:
                k += 1
                # terminating condition
                if k > 300:
                    break
                rand_step = np.random.randint(0, 4)
                rand_step_x, rand_step_y = self.moves[rand_step]
                my_pos = (my_x + rand_step_x, my_y + rand_step_y)

            if k > 300:
                my_pos = ori_pos
                break

        # Put Barrier
        rand_wall = np.random.randint(0, 4)
        my_x, my_y = my_position
        while self.chess_board[my_x, my_y, rand_wall]:
            rand_wall = np.random.randint(0, 4)

        return my_position, rand_wall


if __name__ == "__main__":
    world = World()
    is_end, p0_score, p1_score = world.step()
    while not is_end:
        is_end, p0_score, p1_score = world.step()
    print(p0_score, p1_score)
