import numpy as np
import json
# start = np.array([0, 0])
# goal = np.array([4, 9])
# grid = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # Row 0
#                  [0, 1, 1, 0, 0, 0, 0, 1, 0, 0],  # Row 1
#                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 2
#                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 3
#                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 4
#                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 5
#                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 6
#                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 7
#                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],  # Row 8
#                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]) # Row 9
#         # Columns 0  1  2  3  4  5  6  7  8  9




class BreadthFirstSearch:
    def __init__(self, start, goal, grid, path):
        self.pos = start
        self.pos_str = str(start)
        self.pos_depth = 0
        self.goal_str = str(goal)
        self.explored = {}
        self.not_explored = {}
        self.not_explored[str(start)] = 0
        self.grid = grid
        self.path = path

    # START - Student Section

    def get_possible_moves(self):
        potential_moves = self.generate_potential_moves(self.pos)
        for move in potential_moves:
            # Check if potential move is valid.
            if not self.valid_move(move):
                continue
            # Check if move has already been explored.
            if (str(move) not in self.explored) and (str(move) not in self.not_explored):
                self.not_explored[str(move)] = self.pos_depth+1
        # Since all next possible moves have been determined,
        # consider current location explored.
        self.explored[self.pos_str] = self.pos_depth

        return True

    def goal_found(self):
        if self.goal_str in self.not_explored:
            # Add goal to path.
            self.pos = self.string_to_array(self.goal_str)
            self.pos_depth = self.not_explored.pop(self.goal_str)
            self.path[self.pos[0], self.pos[1]] = self.pos_depth
            return True
        return False

    def explore_next_move(self):
        # Determine next move to explore.
        sorted_not_explored = sorted(
            self.not_explored,
            key=self.not_explored.get,
            reverse=False)
        if len(sorted_not_explored) == 0:
            return False
        # Determine the pos and depth of next move.
        self.pos_str = sorted_not_explored[0]
        self.pos = self.string_to_array(self.pos_str)
        self.pos_depth = self.not_explored.pop(self.pos_str)
        # Write depth of next move onto path.
        self.path[self.pos[0], self.pos[1]] = self.pos_depth
        return True

    # END - Student Section

    # Helper Functions

    def generate_potential_moves(self, pos):
        u = np.array([-1, 0])
        d = np.array([1, 0])
        l = np.array([0, -1])
        r = np.array([0, 1])

        potential_moves = [pos + u, pos + d, pos + l, pos + r]
        # Students, uncomment the line below,  what happens?
        potential_moves += [pos + u+r, pos + u+l, pos + d+r, pos + d+l]
        return potential_moves

    def valid_move(self, move):
        # Check if out of boundary.
        if (move[0] < 0) or (move[0] > 9):
            return False
        if (move[1] < 0) or (move[1] > 9):
            return False
        # Check if wall or obstacle exists.
        if self.grid[move[0], move[1]] == 1:
            return False
        return True

    def string_to_array(self, string):
        array = [int(string[1]), int(string[3])]
        return np.array(array)
def main(start, goal, grid):
    # Init
    bfs = BreadthFirstSearch(start, goal, grid, path)

    while True:
        # Determine next possible moves.
        bfs.get_possible_moves()
        if bfs.goal_found():
            break
        if not bfs.explore_next_move():
            print('Could not find a path!')
            break


    print('')
    print('Explored Path')
    print('-------------')
    print(path)
    print('')
    print('Fully explored count ' + str(np.count_nonzero(path)))


    def find_best_path(pos):
        best_path[pos[0], pos[1]] = 1
        h_pos = path[pos[0], pos[1]]
        if h_pos == 1:
            return 1

        potential_moves = bfs.generate_potential_moves(pos)
        for move in potential_moves:
            if not bfs.valid_move(move):
                continue
            h_move = path[move[0], move[1]]
            if h_move == (h_pos - 1):
                return find_best_path(move) + 1


    goal_count = find_best_path(goal)
    best_path[start[0], start[1]] = 99
    print('')
    print('Best Path To Goal')
    print('-----------------')
    print(best_path)
    print('')
    print('Moves to Goal: ' + str(goal_count))
    print('')

if __name__ == "__main__":
    with open("starting_states.json", 'r') as in_f:
        starting_states = json.load(in_f)
    for i, state in enumerate(starting_states):
        start = np.array(state['start'])
        goal = np.array(state['goal'])
        grid = np.array(state['grid'])
        # Copies of grid to be used for visualizing results.
        path = np.zeros([len(grid), len(grid)], dtype=int)
        best_path = np.zeros([len(grid), len(grid)], dtype=int)
        print(f'Case {i}:')
        main(start, goal, grid)
        break