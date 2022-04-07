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


class StudentWorld:
    def __init__(
            self,
            board=board,
            player_1_position=position1,
            player_2_position=position2,
            max_step=max_step,
    ):
        """
        Initialize the world to the board given
        """
        # Load agents as defined in decorators
        self.p1_pos = player_1_position
        self.p2_pos = player_2_position

        # Moves (Up, Right, Down, Left)
        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

        # Opposite Directions
        self.opposites = {0: 2, 1: 3, 2: 0, 3: 1}

        # Index in dim2 represents [Up, Right, Down, Left] respectively
        # Record barriers and boarders for each block
        self.chess_board = deepcopy(board)

        # Maximum Steps
        self.max_step = max_step

        # Whose turn to step
        self.turn = 0

        # Check initialization
        self.initial_end, _, _ = self.check_endgame()

    def get_current_player(self):
        """
        Get the positions of the current player

        Returns
        -------
        tuple of (current_player_obj, current_player_pos, adversary_player_pos)
        """
        if not self.turn:
            return self.p0, self.p0_pos, self.p1_pos
        else:
            return self.p1, self.p1_pos, self.p0_pos

    def step(self):
        """
        Take a step in the game world.
        Runs the agents' step function and update the game board accordingly.
        If the agents' step function raises an exception, the step will be replaced by a Random Walk.

        Returns
        -------
        results: tuple
            The results of the step containing (is_endgame, player_1_score, player_2_score)
        """
        cur_player, cur_pos, adv_pos = self.get_current_player()

        try:
            # Run the agents step function
            start_time = time()
            next_pos, dir = cur_player.step(
                deepcopy(self.chess_board),
                tuple(cur_pos),
                tuple(adv_pos),
                self.max_step,
            )
            self.update_player_time(time() - start_time)

            next_pos = np.asarray(next_pos, dtype=cur_pos.dtype)
            if not self.check_boundary(next_pos):
                raise ValueError("End position {} is out of boundary".format(next_pos))
            if not 0 <= dir <= 3:
                raise ValueError(
                    "Barrier dir should reside in [0, 3], but your dir is {}".format(
                        dir
                    )
                )
            if not self.check_valid_step(cur_pos, next_pos, dir):
                raise ValueError(
                    "Not a valid step from {} to {} and put barrier at {}, with max steps = {}".format(
                        cur_pos, next_pos, dir, self.max_step
                    )
                )
        except BaseException as e:
            ex_type = type(e).__name__
            if (
                    "SystemExit" in ex_type and isinstance(cur_player, HumanAgent)
            ) or "KeyboardInterrupt" in ex_type:
                sys.exit(0)
            print(
                "An exception raised. The traceback is as follows:\n{}".format(
                    traceback.format_exc()
                )
            )
            print("Execute Random Walk!")
            next_pos, dir = self.random_walk(tuple(cur_pos), tuple(adv_pos))
            next_pos = np.asarray(next_pos, dtype=cur_pos.dtype)

        # Print out each step
        # print(self.turn, next_pos, dir)
        logger.info(
            f"Player {self.player_names[self.turn]} moves to {next_pos} facing {self.dir_names[dir]}"
        )
        if not self.turn:
            self.p0_pos = next_pos
        else:
            self.p1_pos = next_pos
        # Set the barrier to True
        r, c = next_pos
        self.set_barrier(r, c, dir)

        # Change turn
        self.turn = 1 - self.turn

        results = self.check_endgame()

        return results

    def check_endgame(self):
        """
        Check if the game ends and compute the current score of the agents.

        Returns
        -------
        is_endgame : bool
            Whether the game ends.
        player_1_score : int
            The score of player 1.
        player_2_score : int
            The score of player 2.
        """
        # Union-Find
        father = dict()
        for r in range(self.board_size):
            for c in range(self.board_size):
                father[(r, c)] = (r, c)

        def find(pos):
            if father[pos] != pos:
                father[pos] = find(father[pos])
            return father[pos]

        def union(pos1, pos2):
            father[pos1] = pos2

        for r in range(self.board_size):
            for c in range(self.board_size):
                for dir, move in enumerate(
                        self.moves[1:3]
                ):  # Only check down and right
                    if self.chess_board[r, c, dir + 1]:
                        continue
                    pos_a = find((r, c))
                    pos_b = find((r + move[0], c + move[1]))
                    if pos_a != pos_b:
                        union(pos_a, pos_b)

        for r in range(self.board_size):
            for c in range(self.board_size):
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
        if player_win >= 0:
            logging.info(
                f"Game ends! Player {self.player_names[player_win]} wins having control over {win_blocks} blocks!"
            )
        else:
            logging.info("Game ends! It is a Tie!")
        return True, p0_score, p1_score

    def check_boundary(self, pos):
        r, c = pos
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def set_barrier(self, r, c, dir):
        # Set the barrier to True
        self.chess_board[r, c, dir] = True
        # Set the opposite barrier to True
        move = self.moves[dir]
        self.chess_board[r + move[0], c + move[1], self.opposites[dir]] = True

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

    def random_move(self, my_pos, adv_pos):
        """
        ** Reedited version
        Output:
        - a random move from the current position
        """
        # Moves (Up, Right, Down, Left)
        ori_pos = deepcopy(my_pos)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        steps = np.random.randint(0, self.max_step + 1)  # a random number of steps

        # Random Walk
        for _ in range(steps):
            my_x, my_y = my_pos
            rand_step = np.random.randint(0, 4)
            rand_step_x, rand_step_y = self.moves[rand_step]
            my_pos = (my_x + rand_step_x, my_y + rand_step_y)

            # Special Case enclosed by Adversary
            k = 0
            # If there's a wall or there's an adversary at the new place, change step
            while self.chess_board[my_x, my_y, rand_step] or my_pos == adv_pos:
                k += 1
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
        my_x, my_y = my_pos
        while self.chess_board[my_x, my_y, rand_wall]:
            rand_wall = np.random.randint(0, 4)

        return my_pos, rand_wall


if __name__ == "__main__":
    world = World()
    is_end, p0_score, p1_score = world.step()
    while not is_end:
        is_end, p0_score, p1_score = world.step()
    print(p0_score, p1_score)
