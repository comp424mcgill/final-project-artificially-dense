import numpy as np
from collections import defaultdict

from numpy import random


class StudentMinimax:
    def __init__(self, board_size, my_pos, adv_pos, chess_board, parent=None):
        """
        Initializing every variable we need for the implementation of minimax.

        Parameters
        ----------
        board_size: tuple of the size of the board MxM
        parent: starting configuration of the game
        """
        self.turn = True
        self.board_state = board_size
        self.chess_board = chess_board
        self.parent = parent
        self.my_pos = my_pos
        self.adv_pos = adv_pos
        self.my_agent = "my agent"
        self.adv_agent = "adversary agent"
        self.scores = defaultdict(int)
        self.scores["win"] = 1
        self.scores["tie"] = 0.5
        self.scores["loss"] = 0

    def all_positions(self, chess_board, my_pos, adv_pos, max_step, cur_step=0, s=None):
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
        if s is None:
            s = set()
        if cur_step == max_step + 1:
            return s

        my_x, my_y = my_pos
        ad_x, ad_y = adv_pos

        # checking if a move is valid or not
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

    def is_end(self):
        """
        check if the game has ended and return the winner
        """
        m_row, m_col = self.board_state
        # Union-Find
        father = dict()
        for r in range(m_row):
            for c in range(m_col):
                father[(r, c)] = (r, c)

        def find(pos):
            if father[pos] != pos:
                father[pos] = find(father[pos])
            return father[pos]

        def union(pos1, pos2):
            father[pos1] = pos2

        for r in range(m_row):
            for c in range(m_col):
                for dir, move in enumerate(self.moves[1:3]):  # Only check down and right
                    if self.chess_board[r, c, dir + 1]:
                        continue
                    pos_a = find((r, c))
                    pos_b = find((r + move[0], c + move[1]))
                    if pos_a != pos_b:
                        union(pos_a, pos_b)

        for r in range(m_row):
            for c in range(m_col):
                find((r, c))
        p0_r = find(tuple(self.p0_pos))
        p1_r = find(tuple(self.p1_pos))
        p0_score = list(father.values()).count(p0_r)
        p1_score = list(father.values()).count(p1_r)
        if p0_r == p1_r:
            return False, p0_score, p1_score

        player_win = None
        win_blocks = -1
        if p0_score > p1_score:
            player_win = 0
            win_blocks = p0_score
        elif p0_score < p1_score:
            player_win = 1
            win_blocks = p1_score
        else:
            player_win = -1  # Tie

        return True, p0_score, p1_score

    def get_current_player(self):
        """
        Get the positions of the current player

        Returns
        -------
        tuple of (current_player_obj, current_player_pos, adversary_player_pos)
        """
        if self.turn:
            return self.my_agent, self.my_pos, self.adv_pos
        else:
            return self.adv_agent, self.adv_pos, self.my_pos

    def minimax_value(self):
        """
        This is the value part of the minimax algorithm which returns a certain value for each move
        """

        # if the game is over, return the scores
        # so 1 for win, 0.5 for tie, 0 for loss
        result, my_score, adv_score = self.is_end()
        if result and my_score > adv_score:
            return self.scores["win"]
        if result and my_score == adv_score:
            return self.scores["tie"]
        if result and my_score < adv_score:
            return self.scores["loss"]

        player_info = self.get_current_player()
        player, cur_player_pos, adv_player_pos = player_info
        for m in player.all_moves():
            res, m_my_score, m_adv_score = m.is_end()
            if not res:
                value = m.minimax_value()
        if player.equals("my agent"):
            max_value = max(value)
            return max_value
        if player.equals("adversary agent"):
            min_value = min(value)
            return min_value

    def minimax(self):
        """
        This is the decision part of the minimax algorithm, where it decides which path is the best
        and returns it.
        """
        threshold = 0
        for m in self.all_moves():
            new_pos, new_dir = m
            self.chess_board = self.chess_board(new_pos[0], new_pos[1], new_dir)
            value = self.minimax_value()
            if value > threshold:
                threshold = value
            return m
