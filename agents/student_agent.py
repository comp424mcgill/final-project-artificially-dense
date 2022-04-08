# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
from copy import deepcopy
from student_minimax import StudentMinimax


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

        number_rand_actions = 8  # can change
        number_rand_trials = 8  # can change

        highest_prob = 0
        highest_prob_action = (0, 0), 0

        for _ in range(number_rand_actions):
            ori_board = deepcopy(chess_board)
            ori_pos = deepcopy(my_pos)
            sum = 0
            (rand_x, rand_y), direction = self.random_move(ori_board, ori_pos, adv_pos, max_step)
            ori_board[rand_x, rand_y, direction] = True
            for _ in range(number_rand_trials):
                sum += mcts(ori_board, (rand_x, rand_y), adv_pos, max_step - 1)
            if sum / number_rand_trials > highest_prob:
                highest_prob_action = rand_move

        return highest_prob_action
        return (0, 0), 1
