import xiangqi_cpp as engine
from copy import deepcopy
import numpy as np
import cProfile

def encode_pos(row, col):
    return row * 10 + col

def decode_pos(pos):
    return (pos // 10, pos % 10)

def add_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    data[piece] = np.append(data[piece], pos)

def remove_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    if piece in data:
        arr = data[piece]
        # Find and remove the position
        mask = arr != pos
        data[piece] = arr[mask]  # Keep only positions that don't match

def change_piece_position(data, piece, old_row, old_col, new_row, new_col):
    old_pos = encode_pos(old_row, old_col)
    new_pos = encode_pos(new_row, new_col)
    arr = data[piece]
    # Find and update position
    idx = np.where(arr == old_pos)[0]
    if len(idx) > 0:
        arr[idx[0]] = new_pos
        
def get_all_chess_piece_positions(data):
    return [decode_pos(pos) for positions in data.values() for pos in positions.tolist()]


def universal_chess_piece_dict_update(red_data, black_data, chess_pieceSelected, chess_pieceMoveTo, 
                                      startRow, startCol, endRow, endCol):
    if chess_pieceSelected[0] == 'r':
        change_piece_position(red_data, chess_pieceSelected[1:],
                                        startRow, startCol, endRow, endCol)
        if chess_pieceMoveTo != "---":
                remove_piece_position(black_data, chess_pieceMoveTo[1:], endRow, endCol)
    else:
        change_piece_position(black_data, chess_pieceSelected[1:],
                                           startRow, startCol, endRow, endCol)
        if chess_pieceMoveTo != "---":
                remove_piece_position(red_data, chess_pieceMoveTo[1:], endRow, endCol)

def universal_chess_piece_dict_reverse(red_data, black_data, chess_pieceSelected, chess_pieceMoveTo, 
                                      startRow, startCol, endRow, endCol):
    if chess_pieceSelected[0] == 'r':
        change_piece_position(red_data, chess_pieceSelected[1:],
                                        endRow, endCol, startRow, startCol)
        if chess_pieceMoveTo != "---":
            add_piece_position(black_data, chess_pieceMoveTo[1:], endRow, endCol)
    else:
        change_piece_position(black_data, chess_pieceSelected[1:],
                                           endRow, endCol, startRow, startCol)
        if chess_pieceMoveTo != "---":
            add_piece_position(red_data, chess_pieceMoveTo[1:], endRow, endCol)

testPointReal = 0
        
def copy_pieces_pos_dict(original):
    return {k: v.copy() for k, v in original.items()}


class Move:
    rowID = {
        0: "10",
        1: "9",
        2: "8",
        3: "7",
        4: "6",
        5: "5",
        6: "4",
        7: "3",
        8: "2",
        9: "1",
    }
    colID = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i"}

    def __init__(self, board, first, second):
        self.board = board
        self.startRow = first[0]
        self.startCol = first[1]
        self.endRow = second[0]
        self.endCol = second[1]
        self.chess_pieceSelected = board[self.startRow][self.startCol]
        self.chess_pieceMoveTo = board[self.endRow][self.endCol]
        
        self.moveID = (
            self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        )
    def copy(self):
        return Move(self.board, (self.startRow, self.startCol), (self.endRow, self.endCol))
    def getPosition(self, row, col):
        return self.colID[col] + self.rowID[row]

    def __str__(self):
        return f"{self.chess_pieceSelected} {self.getPosition(self.startRow, self.startCol)} ---> {self.getPosition(self.endRow, self.endCol)}"


class State:
    def __init__(self):
        # Initialize the game state with board setup and state variables
        #    """Initialize the Xiangqi board with NumPy array"""
        # Create empty board (10 rows, 9 columns) with 3-character strings
        self.board = np.full((10, 9), '---', dtype='U3')
        
        # Black pieces (top side)
        self.board[0] = ['bch', 'bhs', 'bep', 'bad', 'bgn', 'bad', 'bep', 'bhs', 'bch']
        self.board[2, [1, 7]] = 'bcn'  # Cannons
        self.board[3, [0, 2, 4, 6, 8]] = 'bsd'  # Soldiers
    
    # Red pieces (bottom side)
        self.board[9] = ['rch', 'rhs', 'rep', 'rad', 'rgn', 'rad', 'rep', 'rhs', 'rch']
        self.board[7, [1, 7]] = 'rcn'  # Cannons
        self.board[6, [0, 2, 4, 6, 8]] = 'rsd'  # Soldiers
        
        self.red_chess_piece_pos_dict =  {
            'ch': np.zeros((2,), dtype=int),    # Chariots (max 2)
            'hs': np.zeros((2,), dtype=int),    # Horses
            'cn': np.zeros((2,), dtype=int),    # Cannons
            'sd': np.zeros((5,), dtype=int),    # Soldiers
            'ep': np.zeros((2,), dtype=int),    # Elephants
            'ad': np.zeros((2,), dtype=int),    # Advisors
            'gn': np.zeros((1,), dtype=int)     # General
        }
        
        self.black_chess_piece_pos_dict = {
            'ch': np.zeros((2,), dtype=int),
            'hs': np.zeros((2,), dtype=int),
            'cn': np.zeros((2,), dtype=int),
            'sd': np.zeros((5,), dtype=int),
            'ep': np.zeros((2,), dtype=int),
            'ad': np.zeros((2,), dtype=int),
            'gn': np.zeros((1,), dtype=int)
        }
        # Red pieces (bottom)
        self.red_chess_piece_pos_dict['ch'][:] = [90, 98]
        self.red_chess_piece_pos_dict['hs'][:] = [91, 97]
        self.red_chess_piece_pos_dict['cn'][:] = [71, 77]
        self.red_chess_piece_pos_dict['sd'][:] = [60, 62, 64, 66, 68]
        self.red_chess_piece_pos_dict['ep'][:] = [92, 96]
        self.red_chess_piece_pos_dict['ad'][:] = [93, 95]
        self.red_chess_piece_pos_dict['gn'][:] = [94]
        
        # Black pieces (top)
        self.black_chess_piece_pos_dict['ch'][:] = [0, 8]
        self.black_chess_piece_pos_dict['hs'][:] = [1, 7]
        self.black_chess_piece_pos_dict['cn'][:] = [21, 27]
        self.black_chess_piece_pos_dict['sd'][:] = [30, 32, 34, 36, 38]
        self.black_chess_piece_pos_dict['ep'][:] = [2, 6]
        self.black_chess_piece_pos_dict['ad'][:] = [3, 5]
        self.black_chess_piece_pos_dict['gn'][:] = [4]
        
        self.redTurn = True  # Red side's turn
        self.redIsMachine = (
            False  # After swapping sides, the red side belong to machine
        )
        self.moveLog = []  # Store all the move
        self.pastMoveStorage = []  # Store all the move when click undo button
        self.selectedCell = ()  # Store the selected cell
        self.blackGeneral = (0, 4)  # Store the position of black General
        self.redGeneral = (9, 4)  # Store the position of red General
        self.isGameStart = False  # Check if the game begins
    
    # Reverse the board before playing
    def swap(self):
        for i in range(10):
            for j in range(9):
                if self.board[i][j][0] == "r":
                    self.board[i][j] = "b" + self.board[i][j][1:]
                elif self.board[i][j][0] == "b":
                    self.board[i][j] = "r" + self.board[i][j][1:]
                    
        self.black_chess_piece_pos_dict = {
            "ch": frozenset([90, 98]),
            "hs": frozenset([91, 97]),
            "cn": frozenset([71, 77]),
            "sd": frozenset([60, 62, 64, 66, 68]),
            "ep": frozenset([92, 96]),
            "ad": frozenset([93, 95]),
            "gn": frozenset([94]),
        }
        
        self.red_chess_piece_pos_dict = {
            "ch": frozenset([0, 8]),
            "hs": frozenset([1, 7]),
            "cn": frozenset([21, 27]),
            "sd": frozenset([30, 32, 34, 36, 38]),
            "ep": frozenset([2, 6]),
            "ad": frozenset([3, 5]),
            "gn": frozenset([4]),
        }
        self.blackGeneral, self.redGeneral = self.redGeneral, self.blackGeneral
        self.redIsMachine = not self.redIsMachine
    
    # Make a move, update the board and moveLog
    def makeMove(self, move: Move):
        tmpBoard = np.copy(self.board)
        tmpRedTurn = self.redTurn
        tmpBlackGeneral, tmpRedGeneral = self.blackGeneral, self.redGeneral
        tmpRed_chess_piece_pos_dict = copy_pieces_pos_dict(self.red_chess_piece_pos_dict)
        tmpBlack_chess_piece_pos_dict = copy_pieces_pos_dict(self.black_chess_piece_pos_dict)
        
        tmpBoard[move.startRow][move.startCol] = "---"
        tmpBoard[move.endRow][move.endCol] = move.chess_pieceSelected

        universal_chess_piece_dict_update(tmpRed_chess_piece_pos_dict, tmpBlack_chess_piece_pos_dict,
                                            move.chess_pieceSelected,
                                            move.chess_pieceMoveTo,
                                            move.startRow, move.startCol, move.endRow, move.endCol)
            
        if move.chess_pieceSelected[1:] == "gn":
            if tmpRedTurn:
                tmpRedGeneral = (move.endRow, move.endCol)
            else:
                tmpBlackGeneral = (move.endRow, move.endCol)

        isHumanMove = (
                (self.redTurn and not self.redIsMachine) or (not self.redTurn and self.redIsMachine)  # Human's turn
                )
        
        if isHumanMove and not engine.moveCheckValid(tmpBoard, tmpRed_chess_piece_pos_dict, tmpBlack_chess_piece_pos_dict, tmpRedTurn, self.redIsMachine):
                print("Check")
        else:
            self.board = tmpBoard
            self.red_chess_piece_pos_dict = tmpRed_chess_piece_pos_dict
            self.black_chess_piece_pos_dict = tmpBlack_chess_piece_pos_dict
            self.redGeneral, self.blackGeneral = (
                tmpRedGeneral,
                tmpBlackGeneral,
            )
            self.pastMoveStorage = []
            
            if len(self.moveLog) >= 0 and len(self.moveLog) <= 14:
                power = engine.startPower
            elif len(self.moveLog) >= 14 and len(self.moveLog) <= 50:
                power = engine.midPower
            else:
                power = engine.endPower
            self.moveLog.append(move.copy())
            global testPointReal
            testChessPiece = move.chess_pieceSelected[1:]
            makeRedMove = self.redTurn
            testPointReal += (   # AI/RED
                                 # player/BLACK
                              (0 - engine.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 + engine.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 + (power[move.chess_pieceMoveTo[1:]] 
                                    + engine.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 if makeRedMove else
                              (0 + engine.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 - engine.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 - (power[move.chess_pieceMoveTo[1:]] 
                                    + engine.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 ) if self.redIsMachine else (
                                 # AI/BLACK
                                 # player/RED
                              (0 + engine.bottomHalfPosition[testChessPiece][move.startRow][move.startCol] 
                                 - engine.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 - (power[move.chess_pieceMoveTo[1:]] 
                                    + engine.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0)) # player turn
                                 if makeRedMove else
                              (0 - engine.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 + engine.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 + (power[move.chess_pieceMoveTo[1:]] 
                                    + engine.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0)) # AI turn
                                 )
            self.redTurn = not self.redTurn
            print(move, " point: ", testPointReal)

    # Undo the last two moves
    def undoMove(self):
        print("Before undo: ", testPointReal)
        self.undo()
        self.undo()
        print("After undo: ", testPointReal)

    # Redo the last two moves
    def redoMove(self):
        print("Before redo: ", testPointReal)
        self.redo()
        self.redo()
        print("After redo: ", testPointReal)

    # Undo the last move
    def undo(self):
        global testPointReal
        if len(self.moveLog) == 0:
            return
        lastMove = Move(self.moveLog[-1]).copy()
        self.board[lastMove.startRow][lastMove.startCol] = lastMove.chess_pieceSelected
        self.board[lastMove.endRow][lastMove.endCol] = lastMove.chess_pieceMoveTo
        undoRedTurn = not self.redTurn

        if lastMove.chess_pieceSelected[1:] == "gn":
            if undoRedTurn:
                self.redGeneral = (lastMove.startRow, lastMove.startCol)
            else:
                self.blackGeneral = (lastMove.startRow, lastMove.startCol)
                
        universal_chess_piece_dict_reverse(self.red_chess_piece_pos_dict, self.black_chess_piece_pos_dict,
                                            lastMove.chess_pieceSelected,
                                            lastMove.chess_pieceMoveTo,
                                            lastMove.startRow, lastMove.startCol, lastMove.endRow, lastMove.endCol)

        self.pastMoveStorage.append(deepcopy(self.moveLog.pop()))
        print("Undo number of moves: ", len(self.moveLog))
        if len(self.moveLog) >= 0 and len(self.moveLog) <= 14:
                power = engine.startPower
        elif len(self.moveLog) >= 14 and len(self.moveLog) <= 50:
                power = engine.midPower
        else:
                power = engine.endPower
        
        testChessPiece = lastMove.chess_pieceSelected[1:]
        undoRedTurn = not self.redTurn
        testPointReal -= (       # AI/RED
                                 # player/BLACK
                              (0 - engine.upperHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                                 + engine.upperHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                                 + (power[lastMove.chess_pieceMoveTo[1:]] 
                                    + engine.bottomHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] 
                                    if lastMove.chess_pieceMoveTo[1:] != "--" else 0))
                                 if undoRedTurn else
                              (0 + engine.bottomHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                                 - engine.bottomHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                                 - (power[lastMove.chess_pieceMoveTo[1:]] 
                                    + engine.upperHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] 
                                    if lastMove.chess_pieceMoveTo[1:] != "--" else 0))
                                 ) if self.redIsMachine else (
                                 # AI/BLACK
                                 # player/RED
                              (0 + engine.bottomHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol] 
                                 - engine.bottomHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                                 - (power[lastMove.chess_pieceMoveTo[1:]] 
                                    + engine.upperHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] 
                                    if lastMove.chess_pieceMoveTo[1:] != "--" else 0))
                                 if undoRedTurn else
                              (0 - engine.upperHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                                 + engine.upperHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                                 + (power[lastMove.chess_pieceMoveTo[1:]] 
                                    + engine.bottomHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] 
                                    if lastMove.chess_pieceMoveTo[1:] != "--" else 0))
                                 )
        self.redTurn = not self.redTurn
        print(lastMove)

    # Redo the next move
    def redo(self):
        global testPointReal
        if len(self.pastMoveStorage) == 0:
            return
        nextMoveInStorage = Move(self.pastMoveStorage[-1]).copy()
        self.board[nextMoveInStorage.startRow][nextMoveInStorage.startCol] = "---"
        self.board[nextMoveInStorage.endRow][nextMoveInStorage.endCol] = nextMoveInStorage.chess_pieceSelected
        redoRedTurn = self.redTurn
        if nextMoveInStorage.chess_pieceSelected[1:] == "gn":
            if redoRedTurn:
                self.redGeneral = (nextMoveInStorage.endRow, nextMoveInStorage.endCol)
            else:
                self.blackGeneral = (nextMoveInStorage.endRow, nextMoveInStorage.endCol)
                
        universal_chess_piece_dict_update(self.red_chess_piece_pos_dict, self.black_chess_piece_pos_dict,
                                            nextMoveInStorage.chess_pieceSelected,
                                            nextMoveInStorage.chess_pieceMoveTo,
                                            nextMoveInStorage.startRow, nextMoveInStorage.startCol, nextMoveInStorage.endRow, nextMoveInStorage.endCol)
                
        print("Redo number of moves: ", len(self.moveLog))
        if len(self.moveLog) >= 0 and len(self.moveLog) <= 14:
                power = engine.startPower
        elif len(self.moveLog) >= 14 and len(self.moveLog) <= 50:
                power = engine.midPower
        else:
                power = engine.endPower
        self.moveLog.append(Move(self.pastMoveStorage.pop()).copy())
        
        testChessPiece = nextMoveInStorage.chess_pieceSelected[1:]
        testPointReal += (       # AI/RED
                                 # player/BLACK
                              (0 - engine.upperHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                                 + engine.upperHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                                 + (power[nextMoveInStorage.chess_pieceMoveTo[1:]] 
                                    + engine.bottomHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] 
                                    if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0))
                                 if redoRedTurn else
                              (0 + engine.bottomHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                                 - engine.bottomHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                                 - (power[nextMoveInStorage.chess_pieceMoveTo[1:]] 
                                    + engine.upperHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] 
                                    if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0))
                                 ) if self.redIsMachine else (
                                 # AI/BLACK
                                 # player/RED
                              (0 + engine.bottomHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol] 
                                 - engine.bottomHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                                 - (power[nextMoveInStorage.chess_pieceMoveTo[1:]] 
                                    + engine.upperHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] 
                                    if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0))
                                 if redoRedTurn else
                              (0 - engine.upperHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                                 + engine.upperHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                                 + (power[nextMoveInStorage.chess_pieceMoveTo[1:]] 
                                    + engine.bottomHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] 
                                    if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0))
                                 )
        self.redTurn = not self.redTurn
        print(nextMoveInStorage)

    # Get all valid moves for a given position
    def checkValid(self, position):
        return engine.moveRule(self.board, position, self.redIsMachine)

    # Check if the current player is in check
    def check(self):
        return engine.isChecked(
            self.board,
            self.blackGeneral,
            self.redGeneral,
            self.red_chess_piece_pos_dict,
            self.black_chess_piece_pos_dict,
            not self.redTurn,
            self.redIsMachine,
        )

    # Check if the current player is in checkmate
    def checkMate(self):
        valid_moves = engine.getAllValid(self.board, self.red_chess_piece_pos_dict, self.black_chess_piece_pos_dict, self.redTurn, self.redIsMachine)
        if not valid_moves:  # more Pythonic to check emptiness
            return True, "b" if self.redTurn else "r"
        return False, ""
    

    # Evaluate the board for the current state
    @staticmethod
    def evaluate(redIsMachine, moveCounter, preGuessMove):
        global testPointReal
        tmpRedTurn = redIsMachine
        testPoint = testPointReal 
        if(preGuessMove != None):      
            for move in preGuessMove:
                if moveCounter >= 0 and moveCounter <= 14:
                    power = engine.startPower
                elif moveCounter >= 14 and moveCounter <= 50:
                    power = engine.midPower
                else:
                    power = engine.endPower
                
                testChessPiece = move.chess_pieceSelected[1:]
                testPoint += ((0 - engine.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 + engine.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 + (( power[move.chess_pieceMoveTo[1:]])
                                    + engine.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 if tmpRedTurn else
                              (0 + engine.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 - engine.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 - (  power[move.chess_pieceMoveTo[1:]] 
                                    + engine.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 ) if redIsMachine else (
                                 # AI/BLACK
                                 # player/RED
                              (0 + engine.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 - engine.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 - (power[move.chess_pieceMoveTo[1:]] 
                                    + engine.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 if tmpRedTurn else
                              (0 - engine.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 + engine.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 + (power[move.chess_pieceMoveTo[1:]] 
                                    + engine.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 )
                moveCounter += 1
                tmpRedTurn = not tmpRedTurn
        return testPoint


# # Get the next game state after a move
# def getNextGameState(board, nextMove):
#     tmpBoard = np.copy(board)
#     # if isinstance(nextMove, Move):
#     #     copyNextMove = nextMove.copy()
#     #     tmpNextMove = [(copyNextMove.startRow, copyNextMove.startCol), (copyNextMove.endRow, copyNextMove.endCol)]
#     # else:
#     tmpNextMove = nextMove
#     selectedChess_piece = tmpBoard[tmpNextMove[0][0]][tmpNextMove[0][1]]
#     tmpBoard[tmpNextMove[0][0]][tmpNextMove[0][1]] = "---"
#     tmpBoard[tmpNextMove[1][0]][tmpNextMove[1][1]] = selectedChess_piece
#     return tmpBoard