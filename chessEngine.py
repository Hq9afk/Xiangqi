import rule
from copy import deepcopy
import random
import playWithMachine as pwm

class Move:
    rowID = {0:'10',1:'9', 2:'8', 3:'7', 4:'6', 5:'5', 6:'4', 7:'3', 8:'2', 9:'1'}
    colID = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i'}
    def __init__(self, board, first, second):
        self.board = deepcopy(board)
        self.startRow = first[0]
        self.startCol = first[1]
        self.endRow = second[0]
        self.endCol = second[1]
        self.chess_pieceSelected = board[self.startRow][self.startCol]
        self.chess_pieceMoveTo = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        
    def getChange(self):
        return (
            self.getPosition(self.startRow, self.startCol)
            + "-->"
            + self.getPosition(self.endRow, self.endCol)
        )

    def getPosition(self, row, col):
        return self.colID[col] + self.rowID[row]
    def __str__(self):
       return self.chess_pieceSelected + ' ' + self.getPosition(self.startRow, self.startCol) +'-->'+ self.getPosition(self.endRow, self.endCol) 

class State:
    def __init__(self):
        self.board = [
            [
                "bxe",
                "bma",
                "bvo",
                "bsi",
                "btu",
                "bsi",
                "bvo",
                "bma",
                "bxe",
            ],  # b = black
            ["---", "---", "---", "---", "---", "---", "---", "---", "---"],  # r = red
            [
                "---",
                "bph",
                "---",
                "---",
                "---",
                "---",
                "---",
                "bph",
                "---",
            ],  # ma = horse
            ["bch", "---", "bch", "---", "bch", "---", "bch", "---", "bch"],
            [
                "---",
                "---",
                "---",
                "---",
                "---",
                "---",
                "---",
                "---",
                "---",
            ],  # ph = cannon
            [
                "---",
                "---",
                "---",
                "---",
                "---",
                "---",
                "---",
                "---",
                "---",
            ],  # vo = elephant
            [
                "rch",
                "---",
                "rch",
                "---",
                "rch",
                "---",
                "rch",
                "---",
                "rch",
            ],  # si = advisor
            [
                "---",
                "rph",
                "---",
                "---",
                "---",
                "---",
                "---",
                "rph",
                "---",
            ],  # ch = soldier
            ["---", "---", "---", "---", "---", "---", "---", "---", "---"],
            [
                "rxe",
                "rma",
                "rvo",
                "rsi",
                "rtu",
                "rsi",
                "rvo",
                "rma",
                "rxe",
            ],  # tu = king
        ]

        self.redTurn = True         #  Red side's turn
        self.redIsMachine = False   #  after means when reveses the board, the red side belong to machine
        self.moveLog = []           #  store all the move
        self.pastMoveStorage =[]    #  store all the move when click undo button
        self.selectedCell = ()      #  store the selected cell
        self.blackKing = (0,4)      #  store the position of black king
        self.redKing = (9,4)        #  store the position of red king
        self.isGameStart = False        #  check if the game is start

        self.redMove = True  #  red move is your
        self.after = (
            False  #  after mean when revese the board, the red move belong to machine
        )
        self.moveLog = []  #  store all the move
        self.store = []  #  store all the move when click remove button
        self.selectedCell = ()  #  store the selected cell
        self.blackKing = (0, 4)  #  store the position of black king
        self.redKing = (9, 4)  #  store the position of red king
        self.isStart = False  #  check if the game is start

    # ---------------------------------
    #   use to reverse the board before playing
    # ---------------------------------
    def reverse(self):
        for i in range(10):
            for j in range(9):
                if self.board[i][j][0] == "r":
                    self.board[i][j] = "b" + self.board[i][j][1:]
                elif self.board[i][j][0] == "b":
                    self.board[i][j] = "r" + self.board[i][j][1:]
        self.blackKing, self.redKing = self.redKing, self.blackKing
        self.redIsMachine = not self.redIsMachine
        
    #----------------------------------------------------
    #   This method is used to make a move, it requires a move object as a parameter
    #   It returns nothing, but it will change the board and the moveLog
    # ----------------------------------------------------
    def makeMove(self, move: Move):
        # create a temp board to check if the movement is valid
        tmpBoard = deepcopy(self.board)
        tmpRedTurn = self.redTurn
        tmpBlackKing,  tmpRedKing  = self.blackKing, self.redKing
        
        # update the temp board
        tmpBoard[move.startRow][move.startCol] = '---'                    # empty the start cell
        tmpBoard[move.endRow][move.endCol] = move.chess_pieceSelected     # move the chessman to the end cell

        # update king position
        if move.chess_pieceSelected[1:] == 'tu':
            if tmpRedTurn:
                tmpRedKing = (move.endRow, move.endCol)             
            else:
                tmpBlackKing = (move.endRow, move.endCol)

        # check if the movement is valid
        if not rule.moveCheckValid(tmpBoard, tmpRedTurn, self.redIsMachine):      
            print("Your king is being threaten, protect is must")
            return False
        else:

            # update state when the movement is valid
            self.board = deepcopy(tmpBoard)
            self.redKing, self.blackKing  = tmpRedKing, tmpBlackKing    # update the kings position

            
            self.moveLog.append(deepcopy(move))                         # update the moveLog
            
            self.redTurn = not self.redTurn                             # change the turn
            self.pastMoveStorage =[]                                    # can't use the redo action after making a move
            print(move.getChange(),'---', self.blackKing, self.redKing)
            
    #----------------------------------------------------
    #   This method is used to undo a move
    #   It returns nothing, but it will change the board and the moveLog
    #----------------------------------------------------
    def undoMove(self):
        self.undo()
        self.undo()
    #----------------------------------------------------
    #   This method is used to redo a undo move
    #   It returns nothing, but it will change the board and the moveLog
    #----------------------------------------------------
    def redoMove(self):
        self.redo()
        self.redo()
        
    #----------------------------------------------------
    #   This method is used to undo a move
    #   It returns nothing, but it will change the board and the moveLog
    #----------------------------------------------------
    def undo(self):
        if len(self.moveLog) == 0:
            return
        lastMove = deepcopy(self.moveLog[-1]) #g6h8
        self.board[lastMove.startRow][lastMove.startCol] = lastMove.chess_pieceSelected
        self.board[lastMove.endRow][lastMove.endCol] = lastMove.chess_pieceMoveTo
        isRedLastTurn = not self.redTurn
        
        if lastMove.chess_pieceSelected[1:] == 'tu':
            if isRedLastTurn:
                self.redKing = (lastMove.startRow, lastMove.startCol)
            else:
                self.blackKing = (lastMove.startRow, lastMove.startCol)

        self.pastMoveStorage.append(deepcopy(self.moveLog.pop()))
        self.redTurn = not self.redTurn
        print(lastMove.getChange(),'---', self.blackKing, self.redKing)

    # ----------------------------------------------------
    #   This method is used to undo a undo move
    #   It returns nothing, but it will change the board and the moveLog
    #----------------------------------------------------
    def redo(self):
        if len(self.pastMoveStorage) == 0:
            return
        nextMoveInStorage = deepcopy(self.pastMoveStorage[-1])
        self.board[nextMoveInStorage.startRow][nextMoveInStorage.startCol] = '---'
        self.board[nextMoveInStorage.endRow][nextMoveInStorage.endCol] = nextMoveInStorage.chess_pieceSelected
        isRedNextTurn = not self.redTurn
        if nextMoveInStorage.chess_pieceSelected[1:] == 'tu':
            if isRedNextTurn:
                self.blackKing = (nextMoveInStorage.endRow, nextMoveInStorage.endCol)
            else:
                self.redKing = (nextMoveInStorage.endRow, nextMoveInStorage.endCol)

        self.moveLog.append(deepcopy(self.pastMoveStorage.pop()))
        self.redTurn = not self.redTurn
        print(nextMoveInStorage.getChange(),'---', self.blackKing, self.redKing)
    
    #----------------------------------------------------
    #   This method is used to check if a chess piece on a cell can move to other cells
    #   It returns a list of valid moves
    # ----------------------------------------------------
    def checkValid(self, position):
        return rule.moveRule(self.board, position, self.redIsMachine)
    
    #----------------------------------------------------
    #   This method check if the king is check
    #   It returns true if the king is check
    # ----------------------------------------------------
    def checkMate(self):
        return rule.isKingBeThreaten(self.board, self.blackKing, self.redKing, not self.redTurn, self.redIsMachine)
        
    # ----------------------------------------------------
    # This method check if the game is end
    # It returns a tuple (True/False, 'r'/'b'/'')
    # True if the game is end, False if not
    # 'r' if red win, 'b' if black win, '' if no one win
    # ----------------------------------------------------
    def checkEnd(self):
        if State.getAllValid(self.board, self.redTurn, self.redIsMachine) == []:
            return True, 'b' if self.redTurn else 'r'
        return False,""
    
    # ----------------------------------------------------
    # This method is used to get all valid move
    # ----------------------------------------------------
    @staticmethod
    def getAllValid(board, redTurn, redIsMachine):
        
        candidateMoveList = []
        validMoveList = []
         # == true if red
        turn = 'r' if redTurn else 'b'

        for row in range(10):
            for col in range(9):
                if board[row][col] != '---' and turn == board[row][col][0]:   
                    candidateMoveList = rule.moveRule(board, (row,col), redIsMachine)
                    for cell in candidateMoveList:
                        
                        move = Move(board, (row,col), cell)
                        
                        tmpBoard = deepcopy(board)
                        tmpRedTurn = redTurn
                        
                        tmpBoard[move.startRow][move.startCol] = '---'
                        tmpBoard[move.endRow][move.endCol] = move.chess_pieceSelected

                        if rule.moveCheckValid(tmpBoard, tmpRedTurn, redIsMachine):
                            #listValidMove.append((deepcopy(move)))
                            validMoveList.append([(row,col), cell])
        return validMoveList
    # ----------------------------------------------------
    # This method is used to evaluate the board which is Max is black and Min is red
    # It's used in minimax algorithm
    # ----------------------------------------------------
    @staticmethod
    def evaluate(board, redTurn, redIsMachine, moveCount):
        ePoint = 0
        if State.getAllValid(board, redTurn, redIsMachine) ==[]:    
            return 100000 if redIsMachine else -100000
        
        if moveCount >=0 and moveCount <= 14:
            power = deepcopy(rule.startPower)
        elif moveCount >= 14 and moveCount <= 50:
            power = deepcopy(rule.midPower)
        else:
            power = deepcopy(rule.endPower)

        for row in range(10):
            for col in range(9):
                if board[row][col] != '---':
                    chessPiece = board[row][col][1:]
                    if board[row][col][0] == 'r':
                        ePoint = (ePoint - power[chessPiece] - rule.bottomHalfPosition[chessPiece][row][col]) if not redIsMachine else (ePoint + power[chessPiece] + rule.upperHalfPosition[chessPiece][row][col])
                    else:
                        ePoint = ePoint + power[chessPiece] + rule.upperHalfPosition[chessPiece][row][col] if not redIsMachine else (ePoint - power[chessPiece] - rule.bottomHalfPosition[chessPiece][row][col])
        return ePoint
# ----------------------------------------------------
# This function use to get the next state (board) after a move
# ----------------------------------------------------
def getNextGameState(board, redTurn, redIsMachine, nextMove): 
    tmpBoard = deepcopy(board)
    nextMove = deepcopy(nextMove)

    selectedChess_piece = tmpBoard[nextMove[0][0]][nextMove[0][1]] 
    tmpBoard[nextMove[0][0]][nextMove[0][1]] = '---'       
    tmpBoard[nextMove[1][0]][nextMove[1][1]] = selectedChess_piece

    return tmpBoard
