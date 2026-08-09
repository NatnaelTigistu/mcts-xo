def print_board_2d(board):
    """Prints a 2D list (3x3) as a Tic-Tac-Toe grid."""
    print("\n")
    for i, row in enumerate(board):
        # Join the row items with vertical bars
        print(f" {' | '.join(str(char) for char in row)} ")
        
        # Print the horizontal divider after the 1st and 2nd rows
        if i < 2:
            print("---+---+---")
    print("\n")
    
def print_board(board):
    """Prints a 1D list of 9 items as a Tic-Tac-Toe grid.
    0 = empty space, 1 = X, -1 = O"""
    
    def get_symbol(v):
        return "X" if v == 1 else "O" if v == -1 else " "
    
    print("\n")
    print(f" {get_symbol(board[0])} | {get_symbol(board[1])} | {get_symbol(board[2])} ")
    print("---+---+---")
    print(f" {get_symbol(board[3])} | {get_symbol(board[4])} | {get_symbol(board[5])} ")
    print("---+---+---")
    print(f" {get_symbol(board[6])} | {get_symbol(board[7])} | {get_symbol(board[8])} ")
    print("\n")