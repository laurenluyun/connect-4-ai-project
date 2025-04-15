# Connect Four with AI Opponents

A Python implementation of the classic Connect Four game featuring multiple AI opponents of varying difficulty levels powered by different algorithms.

## Overview

This Connect Four implementation offers both Player vs Player (PvP) and Player vs AI (PvAI) modes. In PvAI mode, players can choose from three difficulty levels, each using a different AI algorithm:

- **Easy**: Random move selection with basic tactical awareness
- **Medium**: Minimax algorithm with alpha-beta pruning
- **Hard**: Monte Carlo Tree Search (MCTS)

## Features

- Clean graphical interface built with Pygame
- Multiple game modes (PvP, PvAI)
- Three AI difficulty levels
- Win detection with visual highlighting
- Interactive menus for game setup

## Requirements

- Python 3.6+
- Pygame
- NumPy
- (Optional) tqdm for AI evaluation progress bars

## Installation

1. Clone the repository:
   - git clone https://github.com/yourusername/connect-four-ai.git
   - cd connect-four-ai
2. Install dependencies:
   - pip install pygame numpy tqdm

## How to Play

Run the game: python connect4_game.py

### Controls
- Use the mouse to select columns for dropping pieces
- Click buttons to navigate menus
- Follow on-screen instructions for game mode and difficulty selection

## AI Algorithms

### Random (Easy)
The easy AI makes mostly random moves with occasional tactical awareness to block obvious wins. This provides an appropriate challenge for beginners learning the game mechanics.

### Minimax with Alpha-Beta Pruning (Medium)
The medium AI uses the minimax algorithm with alpha-beta pruning to look ahead several moves and evaluate potential board positions. It features:

- Sophisticated position evaluation
- Effective pruning to improve computational efficiency
- Prioritization of center control and connected pieces

### Monte Carlo Tree Search (Hard)
The hard AI uses Monte Carlo Tree Search, simulating hundreds of random games from each possible move to determine the statistically best option. It features:

- Statistical evaluation of positions through random playouts
- Early detection of winning and blocking moves
- Center column bias for strategic advantage
- Advanced positional understanding

## Project Structure

- `connect4_game.py`: Main game file with GUI implementation
- `ai_algorithm.py`: Implementation of the three AI algorithms
- `button.py`: UI button class for menus
- `ai_evaluator.py`: Tool for evaluating AI performance

## AI Evaluation Results

- The project includes an AI evaluation tool that can be used to assess the relative strength of the algorithms through direct competition. 
- To run your own AI evaluation: python ai_evaluator.py [number_of_games]
