# Xiangqi Engine using the Minimax algorithm

## Getting Started

### Installation

1. Install python ([https://www.python.org/downloads/](https://www.python.org/downloads/))

2. Create and activate virtual environment
   ```bash
      python -m venv venv
      source venv/bin/activate  # Linux
      venv\Scripts\activate  # Windows
   ```
3. Install packages
   ```bash
      pip install -r rquirements.txt
   ```
4. Run the game

   ```bash
      python main.py
   ```

5. To change the maximum level that the minimax algorithm can go down:

   ```bash
      # 1. Go to src\engine\game_mode_manager.py
      # 2. Find the following method inside class GameModeManager
         def game_mode_manager
      # 3. Find the following:
         minimax = Minimax(2)
      # 4. Change the value
   ```

## Game mechanics

**The game uses traditional Chinese Chess pieces:**

- **General (gn):** Can only move one square horizontally or vertically within its palace.
- **Advisor (ad):** Can only move diagonally within its palace.
- **Elephant (ep):** Can move two squares diagonally, but cannot cross the river (the middle line of the board).
- **Chariot (ch):** Can move horizontally or vertically any number of squares.
- **Cannon (cn):** Can move horizontally or vertically any number of squares, but to capture a piece, it must jump over another piece.
- **Horse (hs):** Can move two squares horizontally or vertically, then one square perpendicularly.
- **Soldier (sd):** Can move one square forward, but cannot move backward.

**Check:** The General is under attack by the opponent's pieces  
**Checkmate:** The General is checked and there is no legal moves to make
