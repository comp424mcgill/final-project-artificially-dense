# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
from copy import deepcopy
from agents.student_world import StudentWorld


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

    @staticmethod
    def random_move(chess_board, my_position, adv_position, max_step):
        """
        ** Reedited version
        Output:
        - a random move from the current position
        """
        # Moves (Up, Right, Down, Left)
        ori_pos = deepcopy(my_position)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        steps = np.random.randint(0, max_step + 1)  # a random number of steps

        # Random Walk
        for _ in range(steps):
            my_x, my_y = my_position
            rand_step = np.random.randint(0, 4)
            rand_step_x, rand_step_y = moves[rand_step]
            my_position = (my_x + rand_step_x, my_y + rand_step_y)

            # Special Case enclosed by Adversary
            k = 0
            # If there's a wall or there's an adversary at the new place, change step
            while chess_board[my_x, my_y, rand_step] or my_position == adv_position:
                k += 1
                # terminating condition
                if k > 300:
                    break
                rand_step = np.random.randint(0, 4)
                rand_step_x, rand_step_y = moves[rand_step]
                my_pos = (my_x + rand_step_x, my_y + rand_step_y)

            if k > 300:
                my_pos = ori_pos
                break

        # Put Barrier
        rand_wall = np.random.randint(0, 4)
        my_x, my_y = my_position
        while chess_board[my_x, my_y, rand_wall]:
            rand_wall = np.random.randint(0, 4)

        return my_position, rand_wall

    @staticmethod
    def set_barrier(chess_board, x, y, dir):
        # Set the barrier to True
        chess_board[x, y, dir] = True
        # Set the opposite barrier to True
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        move = moves[dir]
        chess_board[x + move[0], y + move[1], self.opposites[dir]] = True

    @staticmethod
    def step(chess_board, my_pos, adv_pos, max_step):
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

        # number_rand_actions = 1  # can change
        # number_rand_trials = 1  # can change
        #
        # highest_prob = 0
        # highest_prob_action = (0, 0), 0
        #
        # for _ in range(number_rand_actions):
        #     ori_board = deepcopy(chess_board)
        #     ori_pos = deepcopy(my_pos)
        #     sum = 0
        #     (rand_x, rand_y), direction = random_move(ori_board, ori_pos, adv_pos, max_step)
        #     ori_board[rand_x, rand_y, direction] = True
        #     for _ in range(number_rand_trials):
        #         sum += mcts(ori_board, (rand_x, rand_y), adv_pos, max_step - 1)
        #     if sum / number_rand_trials > highest_prob:
        #         highest_prob_action = (rand_x, rand_y), direction
        #
        # return highest_prob_action
        print("hi1")
        exp = StudentWorld(chess_board, my_pos, adv_pos, max_step)
        print("hi2")
        action = exp.step
        print("hi3")
        print(action)
        print("hi")
        return action
