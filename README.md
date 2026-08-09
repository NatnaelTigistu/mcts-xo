# Monte Carlo Tree Search (MCTS) in Python

A from-scratch, Object-Oriented implementation of the Monte Carlo Tree Search algorithm, applied to a game of Tic-Tac-Toe. 

This project demonstrates how a machine learning agent can teach itself to play a perfect game without any hardcoded strategy, heuristics, or prior knowledge of the rules—relying entirely on mathematical exploration and the **Upper Confidence Bound (UCB1)** formula.

## Architecture

This system is built with a strictly decoupled architecture. The "Brain" (MCTS) knows absolutely nothing about the "Rules" (Tic-Tac-Toe). It interacts with the game solely through a standardized interface, meaning you can swap out the Tic-Tac-Toe engine for Chess, Checkers, or Connect 4 without altering the core AI logic.

The codebase is split into three core components:

1. **`GameState` (The Rules):** Handles the logic of the game, applies moves, manages whose turn it is, and detects wins/draws. (Uses `numpy` for fast matrix evaluations).
2. **`Node` (The Memory):** Represents a single frozen state of the board. It stores the win/loss statistics and maintains the links to its parent and children to form the search tree.
3. **`MonteCarloTreeSearch` (The Brain):** Executes the 4-phase algorithm loop thousands of times per turn to calculate the mathematically optimal move.

## How the Algorithm Works

When it is the AI's turn, it executes thousands of simulations. Each simulation consists of four phases:

1. **Selection:** The AI navigates down its known tree of moves, using the **UCB1** formula to balance *Exploitation* (picking moves that already have high win rates) and *Exploration* (testing moves that haven't been visited enough). 
2. **Expansion:** Once the AI reaches a node that hasn't been fully explored, it asks the Game Engine to generate a new valid board state and creates a new child node.
3. **Simulation (Rollout):** From this newly created node, the AI plays a purely random game against itself until a terminal state (win/loss/draw) is reached.
4. **Backpropagation:** The result of the random rollout is carried backward up the exact path the AI took through the tree, updating the visit counts and win rates for every node along the way.

### Subtree Retention
To optimize memory and computation, this implementation retains the search tree between turns. When a human opponent makes a move, the AI simply severs the irrelevant branches and shifts the root of the tree down to the matching child node, preserving all the thousands of loops of math it already calculated for that specific timeline.

## Prerequisites

* Python 3.x
* NumPy (`pip install numpy`)

## Usage

To play a game against the AI, run the main file from your terminal:

```bash
python main.py