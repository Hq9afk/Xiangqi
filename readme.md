# Xiangqi Engine using the Minimax algorithm

## Getting Started

### Installation

1. Install python ([https://www.python.org/downloads/](https://www.python.org/downloads/))

2. Clone this repository to your local device
   `bash`
3. Create virtual environment
   `bash`
4. Install pygame
   `bash`
5. Run the game
   `bash`

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
**Stalemate:** The game ends in a draw if the player has no legal move to make, even though their General is not checked.
