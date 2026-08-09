import numpy as np

def get_best_child(node, exploration_constant=1.41):
        best_score = -float('inf')
        best_child = None
        
        # Which player just moved to reach this node's children?
        # If it's Player 1's turn to pick, we want to maximize Player 1's wins.
        current_player = node.state.current_player

        for child in node.children:
            # How many times did the current player win from this child?
            wins = child.results[current_player]
            draws = child.results[0]
            plays = child.visits
            
            # The Exploitation Term (Win Rate)
            exploitation = wins / plays + 0.5 * (draws / plays)  # Treat draws as half a win
            
            # The Exploration Term (Curiosity Bonus)
            exploration = exploration_constant * np.sqrt(np.log(node.visits) / plays)
            
            ucb_score = exploitation + exploration
            
            if ucb_score > best_score:
                best_score = ucb_score
                best_child = child
                
        return best_child

def get_most_visited_child(node):
        best_child = None
        most_visits = -1
        
        for child in node.children:
            if child.visits > most_visits:
                most_visits = child.visits
                best_child = child
                
        return best_child