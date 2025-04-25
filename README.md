# Mancala AI Agent – ISAT 480 Final Project
# Authors:
#   Alex Macauley
#   Mason Scofield
#   Ben Fernandez

## Project Overview
This project implements a basic two-player version of the game **Mancala (Kalah)** using Python.
The game includes a human player and an AI opponent powered by the **Minimax algorithm with Alpha-Beta Pruning**.
The goal is to simulate intelligent decision-making and test the agent’s capability against human strategy.

---

## Rules of Mancala (Kalah Variant)

### Game Objective
Each player attempts to collect more stones in their **store** than their opponent by the end of the game.

### Board Layout
- The board consists of **14 pits** in total, each pit is represented by the index in a list:
  - **Player 1** pits: `0 to 5`     [0, 1, 2, 3, 4, ...]
  - **Player 1's store**: `6`       [..., 5, ...]
  - **Player 2** pits: `7 to 12`    [..., 6, 7, 8, 9, 10, 11]
  - **Player 2's store**: `13`      [..., 12]
- Each regular pit starts with **4 stones**.  ---  # of stones is represented by the value in that index
- Stores (also called "Mancalas") start empty.

Example board layout in Python:
```python
[4, 4, 4, 4, 4, 4, 0,   4, 4, 4, 4, 4, 4, 0]
```
**This is the starting board layout and represents 4 marbles in every pit except both player's stores.**

---

## Turn Structure

1. A player selects one of their **non-empty pits** on their side.
2. All stones from that pit are picked up and **distributed counter-clockwise**, placing one stone in each subsequent pit.
3. **Skip the opponent’s store** during distribution.
4. If the **last stone lands in the player's own store**, the player gets **another turn**.
5. If the **last stone lands in an empty pit** on the player's own side, and the opposite pit (on the opponent’s side) has stones, the player **captures both the last stone and the opposite pit’s stones**, placing them in their store.

---

## Game End and Scoring

- The game ends when all **six pits on one player's side are empty**.
- The remaining stones on the opponent's side are **moved to their store**.
- The player with the **most stones in their store** wins.

---

## Python Implementation Details

### Board Representation
The board is represented as a Python list of 14 integers:
```python
# Indexes:
# [0-5]   = Player 1's pits
# [6]     = Player 1's store
# [7-12]  = Player 2's pits
# [13]    = Player 2's store
board = [4, 4, 4, 4, 4, 4, 0,  4, 4, 4, 4, 4, 4, 0]
```

### Classes
- **`MancalaBoard`**: Manages board state, makes moves, checks game end, and handles captures.
- **`HumanPlayer`**: Allows user interaction through the terminal.
- **`AIPlayer`**: Makes decisions using Minimax with Alpha-Beta pruning.

### AI Logic
- **Heuristic Function**: Evaluates board based on store counts:
  ```python
  heuristic = my_store - opponent_store
  ```
- **Fixed Depth**: The Minimax algorithm uses a depth of **6** to balance intelligence and speed.

---

## How to Run

1. Run the main script in terminal:
```bash
python3 main.py
```
2. Follow on-screen prompts to play against the AI.

---
