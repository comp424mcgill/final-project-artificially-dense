# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
from copy import deepcopy
import time


@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }
        self.autoplay = True

    @staticmethod
    def possible_step(chess_board, my_pos, adv_pos):
        """
        Output:
        - all next possible steps
        """
        # If can go up
        if my_pos[0] > 0 and not chess_board[my_pos[0], my_pos[1], 0] and adv_pos != (my_pos[0] - 1, my_pos[1]):
            yield (my_pos[0] - 1, my_pos[1])
        # If can go right
        if my_pos[1] < chess_board.shape[1] - 1 and not chess_board[my_pos[0], my_pos[1], 1] and adv_pos != (
        my_pos[0], my_pos[1] + 1):
            yield (my_pos[0], my_pos[1] + 1)
        # If can go down
        if my_pos[0] < chess_board.shape[0] - 1 and not chess_board[my_pos[0], my_pos[1], 2] and adv_pos != (
        my_pos[0] + 1, my_pos[1]):
            yield (my_pos[0] + 1, my_pos[1])
        # If can go left
        if my_pos[1] > 0 and not chess_board[my_pos[0], my_pos[1], 3] and adv_pos != (my_pos[0], my_pos[1] - 1):
            yield (my_pos[0], my_pos[1] - 1)

    def possible_position(self, chess_board, my_pos, adv_pos, max_step):
        """
        Output:
        - all reachable positions within max steps BFS
        """
        possible_pos = {my_pos}
        tobe_explore_list = [my_pos]
        for _ in range(max_step):
            tobe_explore_list_copy = tobe_explore_list.copy()
            tobe_explore_list = []
            for pos in tobe_explore_list_copy:
                for s in self.possible_step(chess_board, pos, adv_pos):
                    if s not in possible_pos:
                        possible_pos |= {s}
                        tobe_explore_list += [s]
        return possible_pos

    @staticmethod
    def possible_board(chess_board, new_pos):
        """
        Input:
        - new_pos = a position that we could reach
        Output:
        - all possible next board states
        """
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        for dir in range(4):
            # Get the neighboring position of the new_pos
            nei_new_pos = (new_pos[0] + moves[dir][0], new_pos[1] + moves[dir][1])
            # Check if the neighboring position is within the boundaries of the board and if there's no wall in between
            if nei_new_pos[0] >= 0 and nei_new_pos[0] <= chess_board.shape[0] - 1 and nei_new_pos[1] >= 0 and nei_new_pos[1] <= chess_board.shape[1] - 1 and not chess_board[new_pos[0], new_pos[1], dir]:
                # Set the wall of the new state (on both sides)
                new_board = deepcopy(chess_board)
                new_board[new_pos[0], new_pos[1], dir] = True
                new_board[nei_new_pos[0], nei_new_pos[1], (dir + 2) % 4] = True
                # Yield the direction of the current position and the new state board
                yield dir, new_board

    def score_guess(self, chess_board, my_pos, adv_pos):
        """
        run BFS, from my/adv position, whichever reached a cell first appropriates that cell
        the one that has more cell is more likely to win
        Output:
        - the difference between the cells appropriated; the highest the better for us, the lowest the better for the opponent
        """
        adv_possible_pos = {adv_pos}
        adv_tobe_explore_list = [adv_pos]
        my_possible_pos = {my_pos}
        my_tobe_explore_list = [my_pos]

        while len(adv_tobe_explore_list) + len(my_tobe_explore_list):
            adv_tobe_explore_list_copy = adv_tobe_explore_list.copy()
            adv_tobe_explore_list = []
            my_tobe_explore_list_copy = my_tobe_explore_list.copy()
            my_tobe_explore_list = []
            for pos in adv_tobe_explore_list_copy:
                for s in self.possible_step(chess_board, pos, my_pos):
                    if s not in adv_possible_pos and s not in my_possible_pos:
                        adv_possible_pos |= {s}
                        adv_tobe_explore_list += [s]
            for pos in my_tobe_explore_list_copy:
                for s in self.possible_step(chess_board, pos, adv_pos):
                    if s not in adv_possible_pos and s not in my_possible_pos:
                        my_possible_pos |= {s}
                        my_tobe_explore_list += [s]

        return len(my_possible_pos) - len(adv_possible_pos)

    def minimax(self, chess_board, my_pos, adv_pos, max_step, minimax_step=0, minimax_step_max=1):
        """
        Assuming we start at the root of a minimax tree, i.e. we are at depth (or minimax_step) of 0, then the opponent takes turn when we get to depth 1; we play when depth%2 == 0, and the opponent plays when depth%2 == 1
        Input:
        - minimax_step = depth of minimax tree
        - minimax_step_max = max depth of minimax tree
        get the board with the max favorable score guess
        """

        if minimax_step == minimax_step_max:
            if minimax_step % 2 == 0:  # to debug
                info = self.score_guess(chess_board, my_pos, adv_pos), (0, 0), 0
                return info # score, position, direction
            info = self.score_guess(chess_board, adv_pos, my_pos), (0, 0), 0
            return info

        # Get a set of reachable positions within the max step
        possible_pos = self.possible_position(chess_board, my_pos, adv_pos, max_step)
        score_list = []

        # For each position that is reachable, get all possible walls, for which we compute the minimax value (i.e. the utility value of each possible state)
        for pos in possible_pos:
            for dir, new_board in self.possible_board(chess_board, pos):
                score, __, __ = self.minimax(new_board, adv_pos, pos, max_step, minimax_step + 1)
                score_list += [(score, pos, dir)]

        if len(score_list) == 0:
            if minimax_step % 2 == 0:  # to debug
                info = self.score_guess(chess_board, my_pos, adv_pos), (0, 0), 0
                return info  # score, position, direction
            info = self.score_guess(chess_board, adv_pos, my_pos), (0, 0), 0
            return info

        return max(score_list) if minimax_step % 2 == 0 else min(score_list)  # to debug

    def step(self, chess_board, my_pos, adv_pos, max_step):
        score, pos, dir = self.minimax(chess_board, my_pos, adv_pos, max_step)
        return pos, dir