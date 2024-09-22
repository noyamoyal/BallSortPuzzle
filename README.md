# Ball Sort Puzzle Game

## Introduction
The **Ball Sort Puzzle** is a color-sorting game where the goal is to arrange balls of various colors in tubes such that each tube contains balls of a single color. The game offers two modes: **Manual Play**, where the user manually moves the balls, and **AI Play**, where an AI agent uses either **A* search** or **Graph Planning** with heuristic functions to solve the puzzle.

This project demonstrates how AI algorithms can be applied to solve complex planning problems in an interactive and fun environment.

## Features
- **Manual Play Mode**: Solve the puzzle by dragging and dropping the balls between tubes.
- **AI Play Mode**: Watch an AI agent solve the puzzle using A* search or graph planning.
- **Heuristic Search**: The AI agent uses heuristics like `level_sum` and `max_level` to efficiently plan and solve the puzzle.
- **Graphical Interface**: The game provides a GUI with clear visuals, ball colors, and tubes.
- **Real-time Visualization**: See each step made by the AI or the player in real-time.

## Prerequisites

To run this game, you will need:
- **Python 3.x**
- **Tkinter** (for the graphical interface)
- **PIL (Pillow)** (for image processing)

Install the required packages using pip:
```bash
pip install tkinter pillow
```
## Running the Game

### Manual Play Mode

To play manually, run the following command:

```bash
python BallSortPuzzle.py <number_of_colors> human
```
Use the mouse to move balls between tubes to match all the colors in each tube.
### AI Play Mode
To let the AI solve the puzzle using A* search or graph planning, run:

```bash
python BallSortPuzzle.py <number_of_colors> ai search/planning
```
The AI will solve the puzzle step by step, and you'll see the solution visualized in real-time.
## Game Logic

### Puzzle Rules

- **Movement**: You can only move the top ball from one tube to another if the target tube is either empty or contains a ball of the same color on top.
- **Objective**: The goal is to sort the tubes so that each contains balls of only one color.

### AI Algorithms

- A* Search:
  - Utilizes a heuristic and cost function to explore moves, ensuring the most efficient solution is found.

- Graph Planning:
  - Builds a planning graph with actions and propositions, using heuristics like `max_level` and `level_sum` to optimize the search for a solution.

## Conclusion

The Ball Sort Puzzle Game combines interactive gameplay with powerful AI capabilities. Whether solving the puzzle yourself or letting the AI handle it, this game demonstrates the application of search algorithms and heuristics to solve complex, engaging problems.

