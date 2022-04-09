# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
from copy import deepcopy
from agents.student_world import StudentWorld
from agents.student_minimax import StudentMinimax
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

    # @staticmethod
    # def random_move(chess_board, my_position, adv_position, max_step):
    #     """
    #     ** Reedited version
    #     Output:
    #     - a random move from the current position
    #     """
    #     # Moves (Up, Right, Down, Left)
    #     ori_pos = deepcopy(my_position)
    #     moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
    #     steps = np.random.randint(0, max_step + 1)  # a random number of steps
    #
    #     # Random Walk
    #     for _ in range(steps):
    #         my_x, my_y = my_position
    #         rand_step = np.random.randint(0, 4)
    #         rand_step_x, rand_step_y = moves[rand_step]
    #         my_position = (my_x + rand_step_x, my_y + rand_step_y)
    #
    #         # Special Case enclosed by Adversary
    #         k = 0
    #         # If there's a wall or there's an adversary at the new place, change step
    #         while chess_board[my_x, my_y, rand_step] or my_position == adv_position:
    #             k += 1
    #             # terminating condition
    #             if k > 300:
    #                 break
    #             rand_step = np.random.randint(0, 4)
    #             rand_step_x, rand_step_y = moves[rand_step]
    #             my_pos = (my_x + rand_step_x, my_y + rand_step_y)
    #
    #         if k > 300:
    #             my_pos = ori_pos
    #             break
    #
    #     # Put Barrier
    #     rand_wall = np.random.randint(0, 4)
    #     my_x, my_y = my_position
    #     while chess_board[my_x, my_y, rand_wall]:
    #         rand_wall = np.random.randint(0, 4)
    #
    #     return my_position, rand_wall
    #
    # @staticmethod
    # def set_barrier(chess_board, x, y, dir):
    #     # Set the barrier to True
    #     chess_board[x, y, dir] = True
    #     # Set the opposite barrier to True
    #     moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
    #     move = moves[dir]
    #     chess_board[x + move[0], y + move[1], self.opposites[dir]] = True
    #
    # @staticmethod
    # def step(chess_board, my_pos, adv_pos, max_step):
    #     """
    #     Implement the step function of your agent here.
    #     You can use the following variables to access the chess board:
    #     - chess_board: a numpy array of shape (x_max, y_max, 4)
    #     - my_pos: a tuple of (x, y)
    #     - adv_pos: a tuple of (x, y)
    #     - max_step: an integer
    #
    #     You should return a tuple of ((x, y), dir),
    #     where (x, y) is the next position of your agent and dir is the direction of the wall
    #     you want to put on.
    #
    #     Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
    #     """
    #
    #     # number_rand_actions = 1  # can change
    #     # number_rand_trials = 1  # can change
    #     #
    #     # highest_prob = 0
    #     # highest_prob_action = (0, 0), 0
    #     #
    #     # for _ in range(number_rand_actions):
    #     #     ori_board = deepcopy(chess_board)
    #     #     ori_pos = deepcopy(my_pos)
    #     #     sum = 0
    #     #     (rand_x, rand_y), direction = random_move(ori_board, ori_pos, adv_pos, max_step)
    #     #     ori_board[rand_x, rand_y, direction] = True
    #     #     for _ in range(number_rand_trials):
    #     #         sum += mcts(ori_board, (rand_x, rand_y), adv_pos, max_step - 1)
    #     #     if sum / number_rand_trials > highest_prob:
    #     #         highest_prob_action = (rand_x, rand_y), direction
    #     #
    #     # return highest_prob_action
    #     print("hi1")
    #     exp = StudentWorld(chess_board, my_pos, adv_pos, max_step)
    #     print("hi2")
    #     action = exp.step()
    #     print("hi3")
    #     print(action)
    #     print("hi")
    #     return action

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
        print("score guess, my_pos & adv_pos:", my_pos, adv_pos)
        adv_possible_pos = {adv_pos}
        adv_tobe_explore_list = [adv_pos]
        my_possible_pos = {my_pos}
        my_tobe_explore_list = [my_pos]

        while len(adv_tobe_explore_list) + len(my_tobe_explore_list):
            adv_tobe_explore_list_copy = adv_tobe_explore_list.copy()
            # print("adv to be explored", adv_tobe_explore_list)
            adv_tobe_explore_list = []
            my_tobe_explore_list_copy = my_tobe_explore_list.copy()
            # print("us to be explored", my_tobe_explore_list)
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

        print("my possible positions:", my_possible_pos)
        print("adv possible positions:", adv_possible_pos)
        return len(my_possible_pos) - len(adv_possible_pos)

    def minimax(self, chess_board, my_pos, adv_pos, max_step, minimax_step=0, minimax_step_max=1):
        """
        Assuming we start at the root of a minimax tree, i.e. we are at depth (or minimax_step) of 0, then the opponent takes turn when we get to depth 1; we play when depth%2 == 0, and the opponent plays when depth%2 == 1
        Input:
        - minimax_step = depth of minimax tree
        - minimax_step_max = max depth of minimax tree
        get the board with the max favorable score guess
        """
        print("---------------------- minimax start: my_pos:", my_pos, "adv_pos:", adv_pos, "minimax_step:", minimax_step)
        if minimax_step == minimax_step_max:
            if minimax_step % 2 == 0:  # to debug
                info = self.score_guess(chess_board, my_pos, adv_pos), (0, 0), 0
                print(info)
                print("===================== minimax end 1")
                return info # score, position, direction
            info = self.score_guess(chess_board, adv_pos, my_pos), (0, 0), 0
            print(info)
            print("===================== minimax end 2")
            return info

        # Get a set of reachable positions within the max step
        possible_pos = self.possible_position(chess_board, my_pos, adv_pos, max_step)
        score_list = []

        # For each position that is reachable, get all possible walls, for which we compute the minimax value (i.e. the utility value of each possible state)
        for pos in possible_pos:
            for dir, new_board in self.possible_board(chess_board, pos):
                # print(pos, dir, self.minimax(new_board, adv_pos, pos, max_step, minimax_step+1))
                print("direction:", dir, "position:", pos)
                score, __, __ = self.minimax(new_board, adv_pos, pos, max_step, minimax_step + 1)
                score_list += [(score, pos, dir)]

        if len(score_list) == 0:
            if minimax_step % 2 == 0:  # to debug
                info = self.score_guess(chess_board, my_pos, adv_pos), (0, 0), 0
                print(info)
                print("===================== minimax end 3")
                return info  # score, position, direction
            info = self.score_guess(chess_board, adv_pos, my_pos), (0, 0), 0
            print(info)
            print("===================== minimax end 4")
            return info

        # print(minimax_step, [x[0] for x in score_list])
        # print("line 238", score_list)
        # print("line 239", max(score_list))
        # print("line 240", min(score_list))
        print("===================== minimax end 5")
        return max(score_list) if minimax_step % 2 == 0 else min(score_list)  # to debug

    def step(self, chess_board, my_pos, adv_pos, max_step):
        # t1 = time.time()
        score, pos, dir = self.minimax(chess_board, my_pos, adv_pos, max_step)
        # print("final score", score)
        # print(time.time() - t1)
        return pos, dir