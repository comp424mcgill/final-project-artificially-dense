import numpy as np
from collections import defaultdict


class StudentMinimax:
    def __init__(self, board_size, my_pos, adv_pos, chess_board):
        """
        Initializing every variable we need for the implementation of minimax.

        Parameters
        ----------
        board_size: tuple of the size of the board MxM
        my_pos: my agent's current position, which is a tuple (x coord, y coord)
        adv_pos: other agent's current position, which is a tuple (x coord, y coord)
        chess_board: a numpy array of shape (x_max, y_max, 4)
        """
        self.turn = True
        self.board_state = board_size
        self.chess_board = chess_board

        self.my_pos = my_pos
        self.adv_pos = adv_pos
        self.my_agent = "my agent"
        self.adv_agent = "adversary agent"
        self.scores = defaultdict(float)
        self.scores["win"] = 1
        self.scores["tie"] = 0.5
        self.scores["loss"] = 0
        # Maximum Steps
        self.max_step = ((self.board_state + 1) // 2).ndim
        # Moves (Up, Right, Down, Left)
        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

    def check_valid_step(self, start_pos, end_pos, barrier_dir):
        """
        Check if the step the agent takes is valid (reachable and within max steps).

        Parameters
        ----------
        start_pos : tuple
            The start position of the agent.
        end_pos : np.ndarray
            The end position of the agent.
        barrier_dir : int
            The direction of the barrier.
        """
        # Endpoint already has barrier or is boarder
        r, c = end_pos
        if self.chess_board[r, c, barrier_dir]:
            return False
        if np.array_equal(start_pos, end_pos):
            return True

        # Get position of the adversary
        adv_pos = self.adv_pos if self.my_agent.equals("my agent") else self.my_pos

        # BFS
        state_queue = [(start_pos, 0)]
        visited = {tuple(start_pos)}
        is_reached = False
        while state_queue and not is_reached:
            cur_pos, cur_step = state_queue.pop(0)
            r, c = cur_pos
            if cur_step == self.max_step:
                break
            for dir, move in enumerate(self.moves):
                if self.chess_board[r, c, dir]:
                    continue

                next_pos = cur_pos + move
                if np.array_equal(next_pos, adv_pos) or tuple(next_pos) in visited:
                    continue
                if np.array_equal(next_pos, end_pos):
                    is_reached = True
                    break

                visited.add(tuple(next_pos))
                state_queue.append((next_pos, cur_step + 1))

        return is_reached

    def all_positions(self, cur_step=0):
        """
        Input:
        - cur_step = count of step up until max_step;

        Output:
        - a set of possible positions to land on. (O(1) with no repetitions)
        """
        s = set()
        # Reached max step so stop
        if cur_step == self.max_step:
            return s

        my_x, my_y = self.my_pos
        ad_x, ad_y = self.adv_pos

        # checking if a move is valid or not
        if my_x < 0 or my_x >= len(self.chess_board) or my_y < 0 or my_y >= len(self.chess_board):
            return

        s.add(self.my_pos)
        cur_step += 1

        # Move up
        if not self.chess_board[my_x, my_y, 0]:
            if not ((my_x - 1 == ad_x) and (my_y == ad_y)):
                cur_step += 1
                new_pos = (my_x - 1, my_y)
                s.add(new_pos)
                self.all_positions(cur_step)

        # Move down
        if not self.chess_board[my_x, my_y, 2]:
            if not ((my_x + 1 == ad_x) and (my_y == ad_y)):
                cur_step += 1
                new_pos = (my_x + 1, my_y)
                s.add(new_pos)
                self.all_positions(cur_step)

        # Move right
        if not self.chess_board[my_x, my_y, 1]:
            if not ((my_x == ad_x) and (my_y + 1 == ad_y)):
                cur_step += 1
                new_pos = (my_x, my_y + 1)
                s.add(new_pos)
                self.all_positions(cur_step)

        # Move left
        if not self.chess_board[my_x, my_y, 3]:
            if not ((my_x == ad_x) and (my_y - 1 == ad_y)):
                cur_step += 1
                new_pos = (my_x, my_y - 1)
                s.add(new_pos)
                self.all_positions(cur_step)

        return s

    def all_moves(self):
        """
        Output:
        - a set of possible next moves. (O(1) with no repetitions)
        """
        all_p = self.all_positions()  # Get all positions

        # Add all possible walls to the positions
        moves = set()
        for position in all_p:
            for direction in range(4):
                if not self.chess_board[position[0], position[1], direction]:
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
                for dir, move in enumerate(self.all_moves[1:3]):  # Only check down and right
                    if self.chess_board[r, c, dir + 1]:
                        continue
                    pos_a = find((r, c))
                    pos_b = find((r + move[0], c + move[1]))
                    if pos_a != pos_b:
                        union(pos_a, pos_b)

        for r in range(m_row):
            for c in range(m_col):
                find((r, c))
        p0_r = find(tuple(self.my_pos))
        p1_r = find(tuple(self.adv_pos))
        p0_score = list(father.values()).count(p0_r)
        p1_score = list(father.values()).count(p1_r)
        if p0_r == p1_r:
            return False, p0_score, p1_score

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
        value = 0
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
        if player.equals("adv agent"):
            min_value = min(value)
            return min_value

    def minimax(self):
        """
        This is the decision part of the minimax algorithm, where it decides which path is the best
        and returns it.
        """
        for m in self.all_moves():
            threshold = 0
            new_pos, new_dir = m
            self.chess_board = self.chess_board(new_pos[0], new_pos[1], new_dir)
            value = self.minimax_value()
            if value > threshold:
                threshold = value
            return m
