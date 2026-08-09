from game import GameTicTacToe
from memory import Node
from mcts_brain import MonteCarloTreeSearch
from simulation import print_board
from visualization import visualize_mcts_tree

def play_game():
    current_state = GameTicTacToe(current_player=1)  # Player 1 starts
    
    # 1. Create the root node ONCE, outside the game loop
    root = Node(current_state)
    
    while not current_state.is_game_over():
        print_board(current_state.board)
        
        if current_state.current_player == 1:
            print("AI is thinking...")
            mcts = MonteCarloTreeSearch(root)
            best_child = mcts.best_action(simulations_count=500)
            visualize_mcts_tree(root, max_depth=3, top_children=3)
            
            # 2. Advance the game state
            current_state = best_child.state
            
            # 3. Slide the root down to the AI's chosen move
            root = best_child
            root.parent = None # Disconnect the old tree to free up computer memory
            
        else:
            while True:
                try:
                    move = int(input("Your turn! Enter your move (0-8): "))
                    if move in current_state.get_legal_actions():
                        break
                    else:
                        print("Invalid move. Try again.")
                        input() # Wait for user to press Enter before continuing and for clearing the buffer
                except ValueError:
                    print("Please enter a valid integer between 0 and 8.")
            current_state = current_state.move(move)
            
            # 4. Search the AI's memory for the move the human just made
            node_found = False
            for child in root.children:
                if child.parent_action == move:
                    root = child
                    root.parent = None # Disconnect the old tree
                    node_found = True
                    break
            
            # 5. Fallback: If the human made a move the AI NEVER explored 
            # (Extremely rare with 10k loops, but necessary for safety)
            if not node_found:
                root = Node(current_state)

    print_board(current_state.board)
    print("Game Over! Result:", "Draw" if current_state.game_result() == 0 else "AI wins! Next time!" if current_state.game_result() == 1 else "You win! Congrats!")