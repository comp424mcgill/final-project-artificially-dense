# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
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
        # self.autoplay = True
        # self.step_count = 0

    '''
    def set_barrier(self, r, c, direction_given):
        # Set the barrier to True
        self.chess_board[r, c, direction_given] = True
        # Set the opposite barrier to True
        move = self.moves[direction_given]
        self.chess_board[r + move[0], c + move[1], self.opposites[direction_given]] = True
    '''

    def all_positions(self, chess_board, my_pos, adv_pos, max_step, cur_step, s):
        """
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

        # Move left
        if not chess_board[my_x, my_y, 3]:
            if not ((my_x - 1 == ad_x) and (my_y == ad_y)):
                if (my_x - 1, my_y) not in s:
                    self.all_positions(chess_board, (my_x - 1, my_y), adv_pos, max_step, cur_step, s)
        # Move right
        if not chess_board[my_x, my_y, 1]:
            if not ((my_x + 1 == ad_x) and (my_y == ad_y)):
                if (my_x + 1, my_y) not in s:
                    self.all_positions(chess_board, (my_x + 1, my_y), adv_pos, max_step, cur_step, s)
        # Move up
        if not chess_board[my_x, my_y, 0]:
            if not ((my_x == ad_x) and (my_y + 1 == ad_y)):
                if (my_x, my_y + 1) not in s:
                    self.all_positions(chess_board, (my_x, my_y + 1), adv_pos, max_step, cur_step, s)
        # Move down
        if not chess_board[my_x, my_y, 2]:
            if not ((my_x == ad_x) and (my_y - 1 == ad_y)):
                if (my_x, my_y - 1) not in s:
                    self.all_positions(chess_board, (my_x, my_y - 1), adv_pos, max_step, cur_step, s)

        return s

    def all_moves(self, chess_board, my_pos, adv_pos, max_step):
        """
        Output:
        - a set of possible next moves. (O(1) with no repetitions)
        """
        s = set()  # To store the positions
        all_p = self.all_positions(chess_board, my_pos, adv_pos, max_step, 0, s)  # Get all positions

        # Add all possible walls to the positions
        moves = set()
        for position in all_p:
            for direction in range(4):
                if not chess_board[position[0], position[1], direction]:
                    moves.add((position, direction))

        return moves

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

        # move = random_move(self, chess_board, my_pos, adv_pos, max_step)

        all = self.all_moves(chess_board, my_pos, adv_pos, max_step)
        print(all)
        x = next(iter(all))
        print(x)
        f, s = x
        print(f)
        print(s)
        return f, s

