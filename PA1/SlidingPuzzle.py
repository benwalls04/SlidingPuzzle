import random

class SlidingPuzzle: 
    
    def __init__(self):
        self.width = 0
        self.max = 0

    # get a list of all possible board states from the next move
    def get_actions(self, curr_state):
        swipe_index = curr_state.index(self.max)
        row, col = divmod(swipe_index, self.width)
        
        actions = []
        # all possible actions that will be checked 
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        for horiz, vert in directions:
            new_row, new_col = row + horiz, col + vert
            # check if the move yields a valid board
            if 0 <= new_row < self.width and 0 <= new_col < self.width:

                # new index of the missing tile 
                new_index = new_row * self.width + new_col
                new_state = list(curr_state)
                
                # swap swiped tile with missing tile 
                new_state[swipe_index], new_state[new_index] = new_state[new_index], new_state[swipe_index]
                actions.append(tuple([tuple(new_state), 1]))

        return actions

    # make random list of integers from 1 - n 
    def get_board(self):
        board = list(range(1, self.max + 1))  
        random.shuffle(board)
        
        return board

    # randomly generate a board of width chosen by the user
    def init_states(self):
        user_input = input("Enter width of the board: ")
        while not user_input.isdigit():
            user_input = input("Please enter a number: ")
        n = int(user_input)
        self.width = n
        self.max = n * n

        board = self.get_board()
        goal = [(i + 1) for i in range(self.max)]
        
        return tuple(board), tuple(goal)

    # print the board at its current state to the terminal 
    def pretty_print(self, board):
        print('-' * (4 * self.width + 1))
        for i in range(self.width):
            row = board[i * self.width:(i + 1) * self.width]
            row_str = "| " + " | ".join(str(entry) if entry != self.max else " " for entry in row) + " |"
            print(row_str)
            print('-' * (4 * self.width + 1))

    # manhattan heuristic (being used by search class)
    def get_heuristic(self, curr_state):
        heuristic = 0

        for indx, value in enumerate(curr_state):
            exp_indx = value - 1

            ## difference in row + difference in column for each tile
            row_diff = abs((indx // self.width) - (exp_indx // self.width))
            col_diff = abs((indx % self.width) - (exp_indx % self.width))
            heuristic += row_diff + col_diff

        return heuristic
    
    # my heuristic function (not in use, but increases performance over UCS)
    def my_heuristic(self, curr_state): 
        heuristic = 0

        # get the row and column that can be moved 
        space_row = curr_state.index(self.max) // self.width
        space_col = curr_state.index(self.max) % self.width

        for indx, value in enumerate(curr_state):
            # get the row and col of the value, and the expected 
            val_row, val_col = indx // self.width,  indx % self.width
            goal_row, goal_col = (value - 1) // self.width, (value - 1) // self.width

            # add to heuristic if tile is in wrong row AND row can't be moved 
            if space_row != val_row and val_row != goal_row: 
                heuristic += 1
            
            # add to heuristic if tile is in wrong column AND column can't be moved 
            if space_col != val_col and val_col != goal_col:
                heuristic += 1

        return heuristic

    def test(self, curr_state, goal_state):
        return curr_state == goal_state        
