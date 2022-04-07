import numpy as np
from collections import defaultdict
from numpy import random


class StudentMinimax:
    def __init__(self, board_state, parent=None, parent_action=None):
        """
        Initializing every variable we need for the implementation of MCST.

        Parameters
        ----------
        chess_board: tuple of the size of the board MxM
        parent: starting configuration of the game
        parent_action: the move chosen for a specific state of the game

        """
        self.board_state = board_state
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

    def all_positions(self, chess_board, my_pos, adv_pos, max_step, cur_step, s):
        """
        ** Cindy's version
        Input:
        - cur_step = count of step up until max_step;
        - s = initial set;
        - visited = set of visited position.
        Output:
        - a set of possible positions to land on. (O(1) with no repetitions)
        """
        # Reached max step so stop
        if cur_step == max_step + 1:
            return s

        my_x, my_y = my_pos
        ad_x, ad_y = adv_pos

        if my_x < 0 or my_x >= len(chess_board) or my_y < 0 or my_y >= len(chess_board):
            return

        s.add(my_pos)
        cur_step += 1

        # Move up
        if not chess_board[my_x, my_y, 0]:
            if not ((my_x - 1 == ad_x) and (my_y == ad_y)):
                self.all_positions(chess_board, (my_x - 1, my_y), adv_pos, max_step, cur_step, s)

        # Move down
        if not chess_board[my_x, my_y, 2]:
            if not ((my_x + 1 == ad_x) and (my_y == ad_y)):
                self.all_positions(chess_board, (my_x + 1, my_y), adv_pos, max_step, cur_step, s)

        # Move right
        if not chess_board[my_x, my_y, 1]:
            if not ((my_x == ad_x) and (my_y + 1 == ad_y)):
                self.all_positions(chess_board, (my_x, my_y + 1), adv_pos, max_step, cur_step, s)

        # Move left
        if not chess_board[my_x, my_y, 3]:
            if not ((my_x == ad_x) and (my_y - 1 == ad_y)):
                self.all_positions(chess_board, (my_x, my_y - 1), adv_pos, max_step, cur_step, s)

        return s

    def all_moves(self, chess_board, my_pos, adv_pos, max_step):
        """
        ** Cindy's version
        Output:
        - a set of possible next moves. (O(1) with no repetitions)
        """
        # print(max_step)
        s = set()  # To store the positions
        all_p = self.all_positions(chess_board, my_pos, adv_pos, max_step, 0, s)  # Get all positions

        # Add all possible walls to the positions
        moves = set()
        for position in all_p:
            for direction in range(4):
                if not chess_board[position[0], position[1], direction]:
                    moves.add((position, direction))

        return moves

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