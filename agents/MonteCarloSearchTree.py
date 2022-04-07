import numpy as np
from collections import defaultdict
from numpy import random


class MonteCarloSearchTree:
    def __init__(self, chess_board, parent=None, parent_action=None):
        """
        Initializing every variable we need for the implementation of MCST.

        Parameters
        ----------
        board_state: tuple of the size of the board MXM
        parent: starting configuration of the game
        parent_action: the move chosen for a specific state of the game

        """
        self.chess_board = chess_board
        self.parent = parent
        self.parent_action = parent_action
        self.children = defaultdict(list)
        self.visit_num = 0
        self.scores = defaultdict(int)
        self.scores["win"] = 1
        self.score["tie"] = 0.5
        self.scores["loss"] = 0
        self.actions_not_tried = None
        self.actions_not_tried = self.actions_not_tried

    #def untried(self):
        #"""
        #Gets all the possible moves that can be made from our current state and associate them to all the actions that were not tried yet.
        #"""
        #self.actions_not_tried = self.board_state.get_a_move()
        #return self.actions_not_tried

    def expand(self):
        """
        tree expansion
        """
        action = self.random_move()

    def is_leaf(self):
        """
        Check if we're at the end of our search tree, so we have reached terminal once the game is over.
        """
        return self.chess_board.is_endgame()

    def simulation(self):
        curr_state = self.chess_board

        while not curr_state.is_endgame():
            moves_possible = curr_state.random_move()


    def random_move(self, chess_board, my_pos, adv_pos, max_step):
        """
        Gets a random possible move and return it

        Parameters
        ----------
        chess_board:
            current state of chess_board [row, col, direction of barrier]
        my_pos : tuple
            position of the agent.
        adv_pos: tuple
            position of opponent
        max_step : int
            maximum number of steps allowed.
        """
        # left, up, right, down
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        barrier_direction = ("l", "u", "r", "d")
        steps = random.randint(0, max_step + 1)

        # randomly generating a random number of steps
        for i in range(steps):
            # generate a random move
            move = random.choice(moves)
            barrier = random.choice(barrier_direction)

            my_new_pos = my_pos + move*i
            row_new, col_new = my_new_pos
            # if there is already a barrier at the new position
            if chess_board[row_new, col_new, barrier]:
                barrier = random.choice(barrier_direction)

            return my_new_pos, barrier

    def is_valid(self, cur_pos, end_pos, dir_barrier):
        """
        Checks if a certain step is valid

        Parameters
        ----------
        cur_pos : tuple
            position of the agent right now.
        end_pos: tuple
            position of the agent after a move
        dir_barrier : int
            The direction of the barrier.
        """

        new_row, new_col = end_pos
        if self.chess_board[new_row, new_col, dir_barrier]:
            return False
        if np.array_equal(cur_pos, end_pos):
            return True



