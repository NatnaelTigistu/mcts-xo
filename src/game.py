import numpy as np

class GameTicTacToe:
    def __init__(self, board=None, current_player=1):
        if board is None:
            self.board = [0,0,0,0,0,0,0,0,0]  # 3x3 board flattened to a 1D list
        else:
            self.board = board
        self.current_player = current_player

    def get_legal_actions(self):
        # Returns a list of all possible valid moves right now.
        return [index for index, value in enumerate(self.board) if value == 0]

        '''
        legal_actions = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    legal_actions.append((i, j))
        '''

    def move(self, action):
        # Takes an action, applies it, and returns a BRAND NEW GameTicTacToe object.
        # It is crucial to return a new object, not modify the current one, 
        # because the tree needs to remember all past states.

        new_game = GameTicTacToe()
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        new_game.board[action] = new_game.current_player
        new_game.current_player *= -1   
        return new_game

    def is_game_over(self):
        # Returns True if someone won or it's a draw.
        if self.game_result() != 0:
            return True
        if len(self.get_legal_actions()) == 0:
            return True
        return False

    def game_result(self):
        # Returns 1 if Player 1 won.
        # Returns -1 if Player 2 won.
        # Returns 0 for a draw.
        board_2d = np.array(self.board).reshape(3, 3)
     
        if np.any(np.all(board_2d == 1, axis=0)) or np.any(np.all(board_2d == 1, axis=1)) or np.all(np.diag(board_2d) == 1) or np.all(np.diag(np.fliplr(board_2d)) == 1):
                    return 1
        elif np.any(np.all(board_2d == -1, axis=0)) or np.any(np.all(board_2d == -1, axis=1)) or np.all(np.diag(board_2d) == -1) or np.all(np.diag(np.fliplr(board_2d)) == -1):
            return -1
        else:
            return 0
        '''
        # Check rows
        for i in range(3):
                    if self.board[i, 0] == self.board[i, 1] == self.board[i, 2] != 0:
                        return self.board[i, 0]
                # Check columns
                for j in range(3):
                    if self.board[0, j] == self.board[1, j] == self.board[2, j] != 0:
                        return self.board[0, j]
                # Check diagonals
                if self.board[0, 0] == self.board[1, 1] == self.board[2, 2] != 0:
                    return self.board[0, 0]
                if self.board[0, 2] == self.board[1, 1] == self.board[2, 0] != 0:
                    return self.board[0, 2]
                return 0
        '''

if __name__ == "__main__":
    class GameTicTacToe:  # Python won't see this when imported!
        ...
