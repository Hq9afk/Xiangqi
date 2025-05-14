import rule
from copy import deepcopy


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
        self.board = deepcopy(board)
        self.startRow = first[0]
        self.startCol = first[1]
        self.endRow = second[0]
        self.endCol = second[1]
        self.chess_pieceSelected = board[self.startRow][self.startCol]
        self.chess_pieceMoveTo = board[self.endRow][self.endCol]
        self.moveID = (
            self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        )

    def getPosition(self, row, col):
        return self.colID[col] + self.rowID[row]

    def __str__(self):
        return f"{self.chess_pieceSelected} {self.getPosition(self.startRow, self.startCol)} ---> {self.getPosition(self.endRow, self.endCol)}"


class State:
    def __init__(self):
        # Initialize the game state with board setup and state variables
        self.board = [
            [
                "bch",
                "bhs",
                "bep",
                "bad",
                "bgn",
                "bad",
                "bep",
                "bhs",
                "bch",
            ],  # b = Black
            ["---", "---", "---", "---", "---", "---", "---", "---", "---"],  # r = Red
            [
                "---",
                "bcn",
                "---",
                "---",
                "---",
                "---",
                "---",
                "bcn",
                "---",
            ],  # hs = Horse
            ["bsd", "---", "bsd", "---", "bsd", "---", "bsd", "---", "bsd"],
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
            ],  # cn = Cannon
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
            ],  # ep = Elephant
            [
                "rsd",
                "---",
                "rsd",
                "---",
                "rsd",
                "---",
                "rsd",
                "---",
                "rsd",
            ],  # ad = Advisor
            [
                "---",
                "rcn",
                "---",
                "---",
                "---",
                "---",
                "---",
                "rcn",
                "---",
            ],  # sd = Soldier
            ["---", "---", "---", "---", "---", "---", "---", "---", "---"],
            [
                "rch",
                "rhs",
                "rep",
                "rad",
                "rgn",
                "rad",
                "rep",
                "rhs",
                "rch",
            ],  # gn = General
        ]

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
        tmpBoard = deepcopy(self.board)
        tmpRedTurn = self.redTurn
        tmpBlackGeneral, tmpRedGeneral = self.blackGeneral, self.redGeneral

        tmpBoard[move.startRow][move.startCol] = "---"
        tmpBoard[move.endRow][move.endCol] = move.chess_pieceSelected

        if move.chess_pieceSelected[1:] == "gn":
            if tmpRedTurn:
                tmpRedGeneral = (move.endRow, move.endCol)
            else:
                tmpBlackGeneral = (move.endRow, move.endCol)

        if not rule.moveCheckValid(tmpBoard, tmpRedTurn, self.redIsMachine):
            print("Check")
            return False
        else:
            self.board = deepcopy(tmpBoard)
            self.redGeneral, self.blackGeneral = (
                tmpRedGeneral,
                tmpBlackGeneral,
            )
            self.moveLog.append(deepcopy(move))
            self.redTurn = not self.redTurn
            self.pastMoveStorage = []
            print(move)

    # Undo the last two moves
    def undoMove(self):
        self.undo()
        self.undo()

    # Redo the last two moves
    def redoMove(self):
        self.redo()
        self.redo()

    # Undo the last move
    def undo(self):
        if len(self.moveLog) == 0:
            return
        lastMove = deepcopy(self.moveLog[-1])
        self.board[lastMove.startRow][lastMove.startCol] = lastMove.chess_pieceSelected
        self.board[lastMove.endRow][lastMove.endCol] = lastMove.chess_pieceMoveTo
        isRedLastTurn = not self.redTurn

        if lastMove.chess_pieceSelected[1:] == "gn":
            if isRedLastTurn:
                self.redGeneral = (lastMove.startRow, lastMove.startCol)
            else:
                self.blackGeneral = (lastMove.startRow, lastMove.startCol)

        self.pastMoveStorage.append(deepcopy(self.moveLog.pop()))
        self.redTurn = not self.redTurn
        print(lastMove)

    # Redo the next move
    def redo(self):
        if len(self.pastMoveStorage) == 0:
            return
        nextMoveInStorage = deepcopy(self.pastMoveStorage[-1])
        self.board[nextMoveInStorage.startRow][nextMoveInStorage.startCol] = "---"
        self.board[nextMoveInStorage.endRow][
            nextMoveInStorage.endCol
        ] = nextMoveInStorage.chess_pieceSelected
        isRedNextTurn = not self.redTurn
        if nextMoveInStorage.chess_pieceSelected[1:] == "gn":
            if isRedNextTurn:
                self.blackGeneral = (nextMoveInStorage.endRow, nextMoveInStorage.endCol)
            else:
                self.redGeneral = (nextMoveInStorage.endRow, nextMoveInStorage.endCol)

        self.moveLog.append(deepcopy(self.pastMoveStorage.pop()))
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
            not self.redTurn,
            self.redIsMachine,
        )

    # Check if the current player is in checkmate
    def checkMate(self):
        if State.getAllValid(self.board, self.redTurn, self.redIsMachine) == []:
            return True, "b" if self.redTurn else "r"
        return False, ""

    # Get all valid moves for the current player
    @staticmethod
    def getAllValid(board, redTurn, redIsMachine):
        candidateMoveList = []
        validMoveList = []
        turn = "r" if redTurn else "b"

        for row in range(10):
            for col in range(9):
                if board[row][col] != "---" and turn == board[row][col][0]:
                    candidateMoveList = rule.moveRule(board, (row, col), redIsMachine)
                    for cell in candidateMoveList:
                        move = Move(board, (row, col), cell)
                        tmpBoard = deepcopy(board)
                        tmpRedTurn = redTurn
                        tmpBoard[move.startRow][move.startCol] = "---"
                        tmpBoard[move.endRow][move.endCol] = move.chess_pieceSelected
                        if rule.moveCheckValid(tmpBoard, tmpRedTurn, redIsMachine):
                            validMoveList.append([(row, col), cell])
        return validMoveList

    # Evaluate the board for the current state
    @staticmethod
    def evaluate(board, redTurn, redIsMachine, moveCount):
        ePoint = 0
        if State.getAllValid(board, redTurn, redIsMachine) == []:
            return 100000 if redIsMachine else -100000

        if moveCount >= 0 and moveCount <= 14:
            power = deepcopy(rule.startPower)
        elif moveCount >= 14 and moveCount <= 50:
            power = deepcopy(rule.midPower)
        else:
            power = deepcopy(rule.endPower)

        for row in range(10):
            for col in range(9):
                if board[row][col] != "---":
                    chessPiece = board[row][col][1:]
                    if board[row][col][0] == "r":
                        ePoint = (
                            (
                                ePoint
                                - power[chessPiece]
                                - rule.bottomHalfPosition[chessPiece][row][col]
                            )
                            if not redIsMachine
                            else (
                                ePoint
                                + power[chessPiece]
                                + rule.upperHalfPosition[chessPiece][row][col]
                            )
                        )
                    else:
                        ePoint = (
                            ePoint
                            + power[chessPiece]
                            + rule.upperHalfPosition[chessPiece][row][col]
                            if not redIsMachine
                            else (
                                ePoint
                                - power[chessPiece]
                                - rule.bottomHalfPosition[chessPiece][row][col]
                            )
                        )
        return ePoint


# Get the next game state after a move
def getNextGameState(board, redTurn, redIsMachine, nextMove):
    tmpBoard = deepcopy(board)
    nextMove = deepcopy(nextMove)

    selectedChess_piece = tmpBoard[nextMove[0][0]][nextMove[0][1]]
    tmpBoard[nextMove[0][0]][nextMove[0][1]] = "---"
    tmpBoard[nextMove[1][0]][nextMove[1][1]] = selectedChess_piece

    return tmpBoard
