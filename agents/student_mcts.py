import numpy as np
from collections import defaultdict


class StudentMcts:
    def __init__(self, board_size, chess_board, my_pos, adv_pos, parent=None, parent_action=None):
        """
        Initializing the game
        chess_board: initial chess_board
        parent: a parent of a move
        parent_action: the move a parent chooses
        """

        self.board_size = board_size
        self.chess_board = chess_board
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.max_step = (self.board_size + 1) // 2
        self.untried_actions = None
        self.p0_pos = my_pos
        self.p1_pos = adv_pos
        self.visit_count = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[-1] = 0

    def q(self):
        """
        Used for UTC to find the proportion of wins for a given node
        """
        wins = self.results[1]
        loss = self.results[-1]
        return wins - loss

    def num_visits(self):
        """
        Returns the total number of visits for a certain node
        """
        return self.visit_count

    def untried_actions(self):
        """
        returns:List of all untried LEGAL actions
        """
        self.untried_actions = self.chess_board.all_moves()
        return self.untried_actions

    def node_expansion(self):
        """
        Expansion of the nodes of a tree
        """
        action = self.untried_actions.pop()
        next_node = self.chess_board.step(action)
        child_node = StudentMcts(self.board_size, next_node, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        """
        Check if we're at a leaf
        """
        res, score_p0, score_p1 = self.is_end()
        if res:
            return True
        if not res:
            return False

    def rollout(self):
        """
        Simulation of the different moves to obtain a better probability of choice
        """

        curr_state = self.chess_board
        res, score_p0, score_p1 = curr_state.is_end()
        while not res:
            moves = curr_state.all_moves()
            action = self.get_a_random_valid_move(moves)
            curr_state = curr_state.step(action)
            res, score_p0, score_p1 = curr_state.is_end()
            if res:
                if score_p0 > score_p1:
                    return 1
                if score_p0 < score_p1:
                    return -1
                if score_p0 == score_p1:
                    return 0

    def backpropagate(self, result):
        """
        Going back into the tree and updating the utilities
        """
        self.visit_count += 1
        # counts the number of losses and wins each 1: win -1: loss
        self.results[result] += 1
        if self.parent:
            # gives my parent node an updated utility value
            self.parent.backpropagate(result)

    def best_node(self):
        """
        Choosing the child with the highest UTC
        """
        q_value = 0
        for c in self.children:
            q_value = (c.q()/c.num_visits()) + np.sqrt(2) * np.sqrt(np.log(self.num_visits())/c.num_visits())
        return self.children[np.argmax(q_value)]

    def tree_policy(self):
        """
        Choosing a node to develop on
        """
        curr_node = self
        while not curr_node.is_terminal_node():
            if curr_node.no_more_actions():
                curr_node = curr_node.best_node()
            else:
                return curr_node.node_expansion()

        return curr_node

    def best_move(self):
        """
        Choose the best course of action depending on the best node
        """
        sim = 100
        for i in range(sim):
            node = self.tree_policy()
            res = node.rollout()
            node.backpropagate(res)

        return self.best_node()

    def get_a_random_valid_move(self, possibilities):
        """
        Choosing only one move to make
        """
        return possibilities[np.ramdom.randint(len(possibilities))]

    def no_more_actions(self):
        """
        Check if we still have some untried actions, if not, then we're done, no more actions left
        """
        return len(self.untried_actions()) == 0

    def is_end(self):
        """
        check if the game has ended and returns the scores of each player 
        """
        m_row, m_col = self.board_size
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
        p0_r = find(tuple(self.p0_pos))
        p1_r = find(tuple(self.p1_pos))
        p0_score = list(father.values()).count(p0_r)
        p1_score = list(father.values()).count(p1_r)
        if p0_r == p1_r:
            return False, p0_score, p1_score

        return True, p0_score, p1_score

    def step(self, action):
        """
        Take a step in the game and return new state of the board
        """
        new_pos, direction = action
        return self.chess_board(new_pos[0], new_pos[1], direction)

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

        my_x, my_y = self.p0_pos
        ad_x, ad_y = self.p1_pos

        # checking if a move is valid or not
        if my_x < 0 or my_x >= len(self.chess_board) or my_y < 0 or my_y >= len(self.chess_board):
            return

        s.add(self.p0_pos)
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
