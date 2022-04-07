# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
from agents.MonteCarloSearchTree import MonteCarloSearchTree
import sys


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
        self.step_count = 0
        self.mcst = MonteCarloSearchTree()

    def set_barrier(self, r, c, direction_given):
        # Set the barrier to True
        self.chess_board[r, c, direction_given] = True
        # Set the opposite barrier to True
        move = self.moves[direction_given]
        self.chess_board[r + move[0], c + move[1], self.opposites[direction_given]] = True

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
        # check if agent is allowed to put a barrier there, if not, choose another direction
        cur_x, cur_y = my_pos
        if not self.set_barrier(cur_x, cur_y, dir):
            self.set_barrier(cur_x, cur_y, dir)


        # dummy return
        return my_pos, self.dir_map["u"]
