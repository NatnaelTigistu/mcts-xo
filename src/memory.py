import numpy as np

class Node:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state               # The GameState object
        self.parent = parent             # The Node above this one
        self.parent_action = parent_action # The move that created this node
        
        self.children = []               # List of child Nodes
        
        # We need to track which moves we HAVEN'T expanded yet
        self.untried_actions = state.get_legal_actions() 
        
        # The Math Stats
        self.visits = 0
        self.results = {1: 0, -1: 0, 0: 0} # Tracks wins for P1, P2, and draws

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def is_terminal_node(self):
        return self.state.is_game_over()