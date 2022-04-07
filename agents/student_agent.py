# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
from copy import deepcopy


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

    def random_move(self, chess_board, my_pos, adv_pos, max_step):
        """
        Output:
        - a random move from the current position
        """
        # Moves (Up, Right, Down, Left)
        ori_pos = deepcopy(my_pos)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        steps = np.random.randint(0, max_step + 1)  # a random number of steps

        # Random Walk
        for _ in range(steps):
            my_x, my_y = my_pos
            rand_step = np.random.randint(0, 4)
            rand_step_x, rand_step_y = moves[rand_step]
            my_pos = (my_x + rand_step_x, my_y + rand_step_y)

            # Special Case enclosed by Adversary
            k = 0
            # If there's a wall or there's an adversary at the new place, change step
            while chess_board[my_x, my_y, rand_step] or my_pos == adv_pos:
                k += 1
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
        my_x, my_y = my_pos
        while chess_board[my_x, my_y, rand_wall]:
            rand_wall = np.random.randint(0, 4)

        return my_pos, rand_step

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
            ori_board[rand_x, rand_y, direction] = true
            for _ in range(number_rand_trials):
                sum += mcts(ori_board, (rand_x, rand_y), adv_pos, max_step - 1)
            if sum / number_rand_trials > highest_prob:
                highest_prob_action = rand_move

        return highest_prob_action
        return (0, 0), 1
