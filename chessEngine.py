import rule
import random
from copy import deepcopy
import time

def encode_pos(row, col):
    return row * 10 + col

def decode_pos(pos):
    return pos // 10, pos % 10

def add_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    if piece in data:
        data[piece] = data[piece] | frozenset([pos])
    else:
        data[piece] = frozenset([pos])

def remove_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    if piece in data and pos in data[piece]:
        data[piece] = data[piece] - frozenset([pos])

def search_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    if piece in data and pos in data[piece]:
        return decode_pos(pos)  # return as (row, col)
    return None

def change_piece_position(data, piece, old_row, old_col, new_row, new_col):
    old_pos = encode_pos(old_row, old_col)
    new_pos = encode_pos(new_row, new_col)
    if piece in data and old_pos in data[piece]:
        data[piece] = (data[piece] - frozenset([old_pos])) | frozenset([new_pos])
        
def get_all_chess_piece_positions(data):
    return [decode_pos(pos) for positions in data.values() for pos in positions]


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
def all_in_one_copy(original):
        if original:
            if isinstance(original, list) and isinstance(original[0], list) and isinstance(original[0][0], str):
                # board type: list[list[str]]
                return [row[:] for row in original]
            elif isinstance(original, list) and isinstance(original[0][0], tuple): 
                # list of moves: list[list[tuple, tuple]]
                return [move[:] for move in original]
            elif isinstance(original, list) and isinstance(original[0], tuple): 
                return original[:]  # shallow copy is enough 
            elif isinstance(original, Move):
                return original.copy()
            elif isinstance(original, dict):
                first_val = next(iter(original.values()))
                if isinstance(first_val, int):
                    return original.copy()
                elif isinstance(first_val, frozenset):
                    return dict(original)
        else:
            return original  # return as-is for unknown types

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
        self.board = [
            ["bch","bhs","bep","bad","bgn","bad","bep","bhs","bch",],  # b = Black
            ["---","---","---","---","---","---","---","---","---",],  # r = Red
            ["---","bcn","---","---","---","---","---","bcn","---",],  # hs = Horse
            ["bsd","---","bsd","---","bsd","---","bsd","---","bsd",],
            ["---","---","---","---","---","---","---","---","---",],  # cn = Cannon
            ["---","---","---","---","---","---","---","---","---",],  # ep = Elephant
            ["rsd","---","rsd","---","rsd","---","rsd","---","rsd",],  # ad = Advisor
            ["---","rcn","---","---","---","---","---","rcn","---",],  # sd = Soldier
            ["---","---","---","---","---","---","---","---","---",],
            ["rch","rhs","rep","rad","rgn","rad","rep","rhs","rch",],  # gn = General
        ]

        self.red_chess_piece_pos_dict = {
            "ch": frozenset([90, 98]),
            "hs": frozenset([91, 97]),
            "cn": frozenset([71, 77]),
            "sd": frozenset([60, 62, 64, 66, 68]),
            "ep": frozenset([92, 96]),
            "ad": frozenset([93, 95]),
            "gn": frozenset([94]),
        }
        
        self.black_chess_piece_pos_dict = {
            "ch": frozenset([0, 8]),
            "hs": frozenset([1, 7]),
            "cn": frozenset([21, 27]),
            "sd": frozenset([30, 32, 34, 36, 38]),
            "ep": frozenset([2, 6]),
            "ad": frozenset([3, 5]),
            "gn": frozenset([4]),
        }

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
        self.blackGeneral, self.redGeneral = self.redGeneral, self.blackGeneral
        self.redIsMachine = not self.redIsMachine
    
    # Make a move, update the board and moveLog
    def makeMove(self, move: Move):
        tmpBoard = all_in_one_copy(self.board)
        tmpRedTurn = self.redTurn
        tmpBlackGeneral, tmpRedGeneral = self.blackGeneral, self.redGeneral
        tmpRed_chess_piece_pos_dict = all_in_one_copy(self.red_chess_piece_pos_dict)
        tmpBlack_chess_piece_pos_dict = all_in_one_copy(self.black_chess_piece_pos_dict)
        
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
        
        if isHumanMove and not rule.moveCheckValid(tmpBoard, tmpRed_chess_piece_pos_dict, tmpBlack_chess_piece_pos_dict, tmpRedTurn, self.redIsMachine):
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
                power = rule.startPower
            elif len(self.moveLog) >= 14 and len(self.moveLog) <= 50:
                power = rule.midPower
            else:
                power = rule.endPower
            self.moveLog.append(all_in_one_copy(move))
            global testPointReal
            testChessPiece = move.chess_pieceSelected[1:]
            makeRedMove = self.redTurn
            testPointReal += (   # AI/RED
                                 # player/BLACK
                              (0 - rule.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 + rule.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 + (power[move.chess_pieceMoveTo[1:]] 
                                    + rule.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 if makeRedMove else
                              (0 + rule.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 - rule.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 - (power[move.chess_pieceMoveTo[1:]] 
                                    + rule.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 ) if self.redIsMachine else (
                                 # AI/BLACK
                                 # player/RED
                              (0 + rule.bottomHalfPosition[testChessPiece][move.startRow][move.startCol] 
                                 - rule.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 - (power[move.chess_pieceMoveTo[1:]] 
                                    + rule.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0)) # player turn
                                 if makeRedMove else
                              (0 - rule.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 + rule.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 + (power[move.chess_pieceMoveTo[1:]] 
                                    + rule.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
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
        lastMove = all_in_one_copy(self.moveLog[-1])
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
                power = rule.startPower
        elif len(self.moveLog) >= 14 and len(self.moveLog) <= 50:
                power = rule.midPower
        else:
                power = rule.endPower
        
        testChessPiece = lastMove.chess_pieceSelected[1:]
        undoRedTurn = not self.redTurn
        testPointReal -= (       # AI/RED
                                 # player/BLACK
                              (0 - rule.upperHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                                 + rule.upperHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                                 + (power[lastMove.chess_pieceMoveTo[1:]] 
                                    + rule.bottomHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] 
                                    if lastMove.chess_pieceMoveTo[1:] != "--" else 0))
                                 if undoRedTurn else
                              (0 + rule.bottomHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                                 - rule.bottomHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                                 - (power[lastMove.chess_pieceMoveTo[1:]] 
                                    + rule.upperHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] 
                                    if lastMove.chess_pieceMoveTo[1:] != "--" else 0))
                                 ) if self.redIsMachine else (
                                 # AI/BLACK
                                 # player/RED
                              (0 + rule.bottomHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol] 
                                 - rule.bottomHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                                 - (power[lastMove.chess_pieceMoveTo[1:]] 
                                    + rule.upperHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] 
                                    if lastMove.chess_pieceMoveTo[1:] != "--" else 0))
                                 if undoRedTurn else
                              (0 - rule.upperHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                                 + rule.upperHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                                 + (power[lastMove.chess_pieceMoveTo[1:]] 
                                    + rule.bottomHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] 
                                    if lastMove.chess_pieceMoveTo[1:] != "--" else 0))
                                 )
        self.redTurn = not self.redTurn
        print(lastMove)

    # Redo the next move
    def redo(self):
        global testPointReal
        if len(self.pastMoveStorage) == 0:
            return
        nextMoveInStorage = all_in_one_copy(self.pastMoveStorage[-1])
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
                power = rule.startPower
        elif len(self.moveLog) >= 14 and len(self.moveLog) <= 50:
                power = rule.midPower
        else:
                power = rule.endPower
        self.moveLog.append(all_in_one_copy(self.pastMoveStorage.pop()))
        
        testChessPiece = nextMoveInStorage.chess_pieceSelected[1:]
        testPointReal += (       # AI/RED
                                 # player/BLACK
                              (0 - rule.upperHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                                 + rule.upperHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                                 + (power[nextMoveInStorage.chess_pieceMoveTo[1:]] 
                                    + rule.bottomHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] 
                                    if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0))
                                 if redoRedTurn else
                              (0 + rule.bottomHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                                 - rule.bottomHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                                 - (power[nextMoveInStorage.chess_pieceMoveTo[1:]] 
                                    + rule.upperHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] 
                                    if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0))
                                 ) if self.redIsMachine else (
                                 # AI/BLACK
                                 # player/RED
                              (0 + rule.bottomHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol] 
                                 - rule.bottomHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                                 - (power[nextMoveInStorage.chess_pieceMoveTo[1:]] 
                                    + rule.upperHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] 
                                    if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0))
                                 if redoRedTurn else
                              (0 - rule.upperHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                                 + rule.upperHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                                 + (power[nextMoveInStorage.chess_pieceMoveTo[1:]] 
                                    + rule.bottomHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] 
                                    if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0))
                                 )
        self.redTurn = not self.redTurn
        print(nextMoveInStorage)

    # Get all valid moves for a given position
    def checkValid(self, position):
        return rule.moveRule(self.board, position, self.redIsMachine)

    # Check if the current player is in check
    def check(self):
        return rule.isChecked(
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
        if State.getAllValid(self.board, self.red_chess_piece_pos_dict, self.black_chess_piece_pos_dict, self.redTurn, self.redIsMachine) == []:
            return True, "b" if self.redTurn else "r"
        return False, ""

    # Get all valid moves for the current player
    @staticmethod
    def getAllValid(board, red_chess_piece_pos_dict, black_chess_piece_pos_dict, redTurn, redIsMachine):
        candidateMoveList = []
        validMoveList = []
        chess_piece_pos_dict = red_chess_piece_pos_dict if redTurn else black_chess_piece_pos_dict
        all_positions = get_all_chess_piece_positions(chess_piece_pos_dict)
        for (row, col) in all_positions:
            candidateMoveList = rule.moveRule(board, (row, col), redIsMachine)
            for cell in candidateMoveList:
                move = Move(board, (row, col), cell)
                tmpBoard = all_in_one_copy(board)
                tmpRedTurn = redTurn
                tmpRed_chess_piece_pos_dict = all_in_one_copy(red_chess_piece_pos_dict)
                tmpBlack_chess_piece_pos_dict = all_in_one_copy(black_chess_piece_pos_dict)
                universal_chess_piece_dict_update(tmpRed_chess_piece_pos_dict,
                                                  tmpBlack_chess_piece_pos_dict,
                                                  move.chess_pieceSelected,
                                                  move.chess_pieceMoveTo,
                                                  move.startRow,
                                                  move.startCol,
                                                  move.endRow,
                                                  move.endCol
                                                  )
                tmpBoard[move.startRow][move.startCol] = "---"
                tmpBoard[move.endRow][move.endCol] = move.chess_pieceSelected
                if rule.moveCheckValid(tmpBoard, tmpRed_chess_piece_pos_dict, tmpBlack_chess_piece_pos_dict, tmpRedTurn, redIsMachine):
                    validMoveList.append([(row, col), cell])
        return validMoveList

    
    # Evaluate the board for the current state
    @staticmethod
    def evaluate(redIsMachine, moveCounter, preGuessMove):
        # start_time = time.perf_counter_ns()
        global testPointReal
        # ePoint = 0
        tmpRedTurn = redIsMachine
        testPoint = testPointReal 
        if(preGuessMove != None):      
            for move in preGuessMove:
                # print(f"Move number {moveCounter}")
                if moveCounter >= 0 and moveCounter <= 14:
                    power = rule.startPower
                elif moveCounter >= 14 and moveCounter <= 50:
                    power = rule.midPower
                else:
                    power = rule.endPower
                
                testChessPiece = move.chess_pieceSelected[1:]
                # print(f"{move.chess_pieceSelected} - ", end = '') 
                # if testChessPiece == 'ch':
                #     if(tmpBoard[move.endRow][move.endCol])
                
                testPoint += ((0 - rule.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 + rule.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 + (( power[move.chess_pieceMoveTo[1:]])
                                    + rule.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 if tmpRedTurn else
                              (0 + rule.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 - rule.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 - (  power[move.chess_pieceMoveTo[1:]] 
                                    + rule.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 ) if redIsMachine else (
                                 # AI/BLACK
                                 # player/RED
                              (0 + rule.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 - rule.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 - (power[move.chess_pieceMoveTo[1:]] 
                                    + rule.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 if tmpRedTurn else
                              (0 - rule.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                                 + rule.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                                 + (power[move.chess_pieceMoveTo[1:]] 
                                    + rule.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] 
                                    if move.chess_pieceMoveTo[1:] != "--" else 0))
                                 )
                moveCounter += 1
                tmpRedTurn = not tmpRedTurn
            # if testPoint != ePoint :
            #     print(f"{testPoint} - {ePoint}")
        
        # end_time = time.perf_counter_ns()  # ⏱️ End the timer
        # duration = (end_time - start_time)/(1e9)
        # print(f"Evaluate took {duration:.9f} seconds, E = {testPoint}")
        return testPoint


# Get the next game state after a move
def getNextGameState(board, nextMove):
    tmpBoard = all_in_one_copy(board)
    if isinstance(nextMove, Move):
        copyNextMove = nextMove.copy()
        tmpNextMove = [(copyNextMove.startRow, copyNextMove.startCol), (copyNextMove.endRow, copyNextMove.endCol)]
    else:
        tmpNextMove = nextMove
    selectedChess_piece = tmpBoard[tmpNextMove[0][0]][tmpNextMove[0][1]]
    tmpBoard[tmpNextMove[0][0]][tmpNextMove[0][1]] = "---"
    tmpBoard[tmpNextMove[1][0]][tmpNextMove[1][1]] = selectedChess_piece
    # print("tmpBoard: ", State.evaluate(tmpBoard, redTurn, redIsMachine,  moveCounter , None))
    return tmpBoard
