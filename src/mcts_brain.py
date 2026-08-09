from memory import Node
import numpy as np

from uct import get_best_child, get_most_visited_child

class MonteCarloTreeSearch:
    def __init__(self, root_node):
        self.root = root_node

    def best_action(self, simulations_count):
        # Run the loop thousands of times
        for _ in range(simulations_count):
            leaf_node = self.selection(self.root) 
            simulation_result = self.simulation(leaf_node)
            self.backpropagation(leaf_node, simulation_result)
            
        # When time is up, pick the child we visited the most
        return get_most_visited_child(self.root)

    # --- THE 4 PHASES ---

    def selection(self, node):
        current = node
        while not current.is_terminal_node():
            if not current.is_fully_expanded():
                return self.expansion(current)
            else:
                # If fully expanded, use UCB1 to pick the smartest child
                current = get_best_child(current, exploration_constant=1.41)
        return current

    def expansion(self, node):
        # Pop one of the untried actions
        action = node.untried_actions.pop()
        
        # Ask the Game Engine what the new board looks like
        new_state = node.state.move(action)
        
        # Create a new Node, link it to the parent, and return it
        child_node = Node(state=new_state, parent=node, parent_action=action)
        node.children.append(child_node)
        return child_node

    def simulation(self, node):
        # Play a completely random game until it ends
        current_state = node.state # Doesn't modify the original node's state, just a reference to it
        while not current_state.is_game_over():
            possible_moves = current_state.get_legal_actions()
            
            random_action = np.random.choice(possible_moves)
            current_state = current_state.move(random_action)
            
        # Return who won (1, -1, or 0)
        return current_state.game_result()

    def backpropagation(self, node, result):
        current = node
        while current is not None:
            current.visits += 1
            current.results[result] += 1
            # Step back up the tree
            current = current.parent