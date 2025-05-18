import rule

testPointReal = 0


def all_in_one_copy(original):
    if original is None:
        return None
    if isinstance(original, list):
        if not original:
            return []
        if isinstance(original[0], list) and original[0] and isinstance(original[0][0], str):
            # board type: list[list[str]]
            return [row[:] for row in original]
        elif isinstance(original[0], list) and original[0] and isinstance(original[0][0], tuple):
            # list of moves: list[list[tuple, tuple]]
            return [move[:] for move in original]
        elif isinstance(original[0], tuple):
            return original[:]  # shallow copy is enough
        else:
            return original[:]  # fallback shallow copy
    elif isinstance(original, Move):
        return original.copy()
    elif isinstance(original, dict):
        return original.copy()
    else:
        return original  # fallback for other types


class Move:
    rowID = {0: "10", 1: "9", 2: "8", 3: "7", 4: "6", 5: "5", 6: "4", 7: "3", 8: "2", 9: "1"}
    colID = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i"}

    def __init__(self, board, first, second):
        self.board = all_in_one_copy(board)
        self.startRow = first[0]
        self.startCol = first[1]
        self.endRow = second[0]
        self.endCol = second[1]
        self.chess_pieceSelected = board[self.startRow][self.startCol]
        self.chess_pieceMoveTo = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def copy(self):
        return Move(self.board, (self.startRow, self.startCol), (self.endRow, self.endCol))

    def getPosition(self, row, col):
        return self.colID[col] + self.rowID[row]

    def __str__(self):
        return f"{self.chess_pieceSelected} {self.getPosition(self.startRow, self.startCol)} ---> {self.getPosition(self.endRow, self.endCol)}"


class State:
    def __init__(self):
        self.board = [
            ["bch", "bhs", "bep", "bad", "bgn", "bad", "bep", "bhs", "bch"],
            ["---", "---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "bcn", "---", "---", "---", "---", "---", "bcn", "---"],
            ["bsd", "---", "bsd", "---", "bsd", "---", "bsd", "---", "bsd"],
            ["---", "---", "---", "---", "---", "---", "---", "---", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---", "---"],
            ["rsd", "---", "rsd", "---", "rsd", "---", "rsd", "---", "rsd"],
            ["---", "rcn", "---", "---", "---", "---", "---", "rcn", "---"],
            ["---", "---", "---", "---", "---", "---", "---", "---", "---"],
            ["rch", "rhs", "rep", "rad", "rgn", "rad", "rep", "rhs", "rch"],
        ]
        self.redTurn = True
        self.redIsMachine = False
        self.moveLog = []
        self.pastMoveStorage = []
        self.selectedCell = ()
        self.blackGeneral = (0, 4)
        self.redGeneral = (9, 4)
        self.isGameStart = False

    def swap(self):
        for i in range(10):
            for j in range(9):
                if self.board[i][j][0] == "r":
                    self.board[i][j] = "b" + self.board[i][j][1:]
                elif self.board[i][j][0] == "b":
                    self.board[i][j] = "r" + self.board[i][j][1:]
        self.blackGeneral, self.redGeneral = self.redGeneral, self.blackGeneral
        self.redIsMachine = not self.redIsMachine

    def makeMove(self, move: Move):
        tmpBoard = all_in_one_copy(self.board)
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
            print("Illegal move")
            return False
        else:
            self.board = all_in_one_copy(tmpBoard)
            self.redGeneral, self.blackGeneral = tmpRedGeneral, tmpBlackGeneral
            self.pastMoveStorage = []

            if len(self.moveLog) >= 0 and len(self.moveLog) <= 14:
                power = all_in_one_copy(rule.startPower)
            elif len(self.moveLog) >= 14 and len(self.moveLog) <= 50:
                power = all_in_one_copy(rule.midPower)
            else:
                power = all_in_one_copy(rule.endPower)
            self.moveLog.append(all_in_one_copy(move))
            global testPointReal
            testChessPiece = move.chess_pieceSelected[1:]
            makeRedMove = self.redTurn
            testPointReal += (
                (
                    (
                        0
                        - rule.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                        + rule.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                        + (power[move.chess_pieceMoveTo[1:]] + rule.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] if move.chess_pieceMoveTo[1:] != "--" else 0)
                    )
                    if makeRedMove
                    else (
                        0
                        + rule.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                        - rule.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                        - (power[move.chess_pieceMoveTo[1:]] + rule.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] if move.chess_pieceMoveTo[1:] != "--" else 0)
                    )
                )
                if self.redIsMachine
                else (
                    (
                        0
                        + rule.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                        - rule.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                        - (power[move.chess_pieceMoveTo[1:]] + rule.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] if move.chess_pieceMoveTo[1:] != "--" else 0)
                    )
                    if makeRedMove
                    else (
                        0
                        - rule.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                        + rule.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                        + (power[move.chess_pieceMoveTo[1:]] + rule.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] if move.chess_pieceMoveTo[1:] != "--" else 0)
                    )
                )
            )
            self.redTurn = not self.redTurn
            print(move, " point: ", testPointReal, " ", self.evaluate(self.board, self.redTurn, self.redIsMachine, len(self.moveLog), None))

    def undoMove(self):
        print("Before undo: ", testPointReal)
        self.undo()
        self.undo()
        print("After undo: ", testPointReal)

    def redoMove(self):
        print("Before redo: ", testPointReal)
        self.redo()
        self.redo()
        print("After redo: ", testPointReal)

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

        self.pastMoveStorage.append(all_in_one_copy(self.moveLog.pop()))
        print("Undo number of moves: ", len(self.moveLog))
        if len(self.moveLog) >= 0 and len(self.moveLog) <= 14:
            power = all_in_one_copy(rule.startPower)
        elif len(self.moveLog) >= 14 and len(self.moveLog) <= 50:
            power = all_in_one_copy(rule.midPower)
        else:
            power = all_in_one_copy(rule.endPower)

        testChessPiece = lastMove.chess_pieceSelected[1:]
        undoRedTurn = not self.redTurn
        testPointReal -= (
            (
                (
                    0
                    - rule.upperHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                    + rule.upperHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                    + (power[lastMove.chess_pieceMoveTo[1:]] + rule.bottomHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] if lastMove.chess_pieceMoveTo[1:] != "--" else 0)
                )
                if undoRedTurn
                else (
                    0
                    + rule.bottomHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                    - rule.bottomHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                    - (power[lastMove.chess_pieceMoveTo[1:]] + rule.upperHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] if lastMove.chess_pieceMoveTo[1:] != "--" else 0)
                )
            )
            if self.redIsMachine
            else (
                (
                    0
                    + rule.bottomHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                    - rule.bottomHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                    - (power[lastMove.chess_pieceMoveTo[1:]] + rule.upperHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] if lastMove.chess_pieceMoveTo[1:] != "--" else 0)
                )
                if undoRedTurn
                else (
                    0
                    - rule.upperHalfPosition[testChessPiece][lastMove.startRow][lastMove.startCol]
                    + rule.upperHalfPosition[testChessPiece][lastMove.endRow][lastMove.endCol]
                    + (power[lastMove.chess_pieceMoveTo[1:]] + rule.bottomHalfPosition[lastMove.chess_pieceMoveTo[1:]][lastMove.endRow][lastMove.endCol] if lastMove.chess_pieceMoveTo[1:] != "--" else 0)
                )
            )
        )
        self.redTurn = not self.redTurn
        print(lastMove)

    def redo(self):
        global testPointReal
        if len(self.pastMoveStorage) == 0:
            return
        nextMoveInStorage = all_in_one_copy(self.pastMoveStorage[-1])
        self.board[nextMoveInStorage.startRow][nextMoveInStorage.startCol] = "---"
        self.board[nextMoveInStorage.endRow][nextMoveInStorage.endCol] = nextMoveInStorage.chess_pieceSelected
        self.board[nextMoveInStorage.endRow][nextMoveInStorage.endCol] = nextMoveInStorage.chess_pieceSelected
        redoRedTurn = self.redTurn
        if nextMoveInStorage.chess_pieceSelected[1:] == "gn":
            if redoRedTurn:
                self.redGeneral = (nextMoveInStorage.endRow, nextMoveInStorage.endCol)
            else:
                self.blackGeneral = (nextMoveInStorage.endRow, nextMoveInStorage.endCol)
        print("Redo number of moves: ", len(self.moveLog))
        if len(self.moveLog) >= 0 and len(self.moveLog) <= 14:
            power = all_in_one_copy(rule.startPower)
        elif len(self.moveLog) >= 14 and len(self.moveLog) <= 50:
            power = all_in_one_copy(rule.midPower)
        else:
            power = all_in_one_copy(rule.endPower)
        self.moveLog.append(all_in_one_copy(self.pastMoveStorage.pop()))

        testChessPiece = nextMoveInStorage.chess_pieceSelected[1:]
        testPointReal += (
            (
                (
                    0
                    - rule.upperHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                    + rule.upperHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                    + (power[nextMoveInStorage.chess_pieceMoveTo[1:]] + rule.bottomHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0)
                )
                if redoRedTurn
                else (
                    0
                    + rule.bottomHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                    - rule.bottomHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                    - (power[nextMoveInStorage.chess_pieceMoveTo[1:]] + rule.upperHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0)
                )
            )
            if self.redIsMachine
            else (
                (
                    0
                    + rule.bottomHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                    - rule.bottomHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                    - (power[nextMoveInStorage.chess_pieceMoveTo[1:]] + rule.upperHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0)
                )
                if redoRedTurn
                else (
                    0
                    - rule.upperHalfPosition[testChessPiece][nextMoveInStorage.startRow][nextMoveInStorage.startCol]
                    + rule.upperHalfPosition[testChessPiece][nextMoveInStorage.endRow][nextMoveInStorage.endCol]
                    + (power[nextMoveInStorage.chess_pieceMoveTo[1:]] + rule.bottomHalfPosition[nextMoveInStorage.chess_pieceMoveTo[1:]][nextMoveInStorage.endRow][nextMoveInStorage.endCol] if nextMoveInStorage.chess_pieceMoveTo[1:] != "--" else 0)
                )
            )
        )
        self.redTurn = not self.redTurn
        print(nextMoveInStorage)

    def checkValid(self, position):
        return rule.moveRule(self.board, position, self.redIsMachine)

    def check(self):
        return rule.isChecked(self.board, self.blackGeneral, self.redGeneral, not self.redTurn, self.redIsMachine)

    def checkMate(self):
        if State.getAllValid(self.board, self.redTurn, self.redIsMachine) == []:
            return True, "b" if self.redTurn else "r"
        return False, ""

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
                        tmpBoard = all_in_one_copy(board)
                        tmpRedTurn = redTurn
                        tmpBoard[move.startRow][move.startCol] = "---"
                        tmpBoard[move.endRow][move.endCol] = move.chess_pieceSelected
                        if rule.moveCheckValid(tmpBoard, tmpRedTurn, redIsMachine):
                            validMoveList.append([(row, col), cell])
        return validMoveList

    @staticmethod
    def evaluate(board, redTurn, redIsMachine, moveCounter, preGuessMove):
        global testPointReal
        tmpRedTurn = redIsMachine
        testPoint = testPointReal
        if preGuessMove is not None:
            for move in preGuessMove:
                if moveCounter >= 0 and moveCounter <= 14:
                    power = all_in_one_copy(rule.startPower)
                elif moveCounter >= 14 and moveCounter <= 50:
                    power = all_in_one_copy(rule.midPower)
                else:
                    power = all_in_one_copy(rule.endPower)

                testChessPiece = move.chess_pieceSelected[1:]
                testPoint += (
                    (
                        (
                            0
                            - rule.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                            + rule.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                            + ((power[move.chess_pieceMoveTo[1:]]) + rule.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] if move.chess_pieceMoveTo[1:] != "--" else 0)
                        )
                        if tmpRedTurn
                        else (
                            0
                            + rule.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                            - rule.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                            - (power[move.chess_pieceMoveTo[1:]] + rule.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] if move.chess_pieceMoveTo[1:] != "--" else 0)
                        )
                    )
                    if redIsMachine
                    else (
                        (
                            0
                            + rule.bottomHalfPosition[testChessPiece][move.startRow][move.startCol]
                            - rule.bottomHalfPosition[testChessPiece][move.endRow][move.endCol]
                            - (power[move.chess_pieceMoveTo[1:]] + rule.upperHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] if move.chess_pieceMoveTo[1:] != "--" else 0)
                        )
                        if tmpRedTurn
                        else (
                            0
                            - rule.upperHalfPosition[testChessPiece][move.startRow][move.startCol]
                            + rule.upperHalfPosition[testChessPiece][move.endRow][move.endCol]
                            + (power[move.chess_pieceMoveTo[1:]] + rule.bottomHalfPosition[move.chess_pieceMoveTo[1:]][move.endRow][move.endCol] if move.chess_pieceMoveTo[1:] != "--" else 0)
                        )
                    )
                )
                moveCounter += 1
                tmpRedTurn = not tmpRedTurn
        return testPoint


def getNextGameState(board, nextMove):
    tmpBoard = all_in_one_copy(board)
    if isinstance(nextMove, Move):
        copyNextMove = nextMove.copy()
        tmpNextMove = [(copyNextMove.startRow, copyNextMove.startCol), (copyNextMove.endRow, copyNextMove.endCol)]
    else:
        tmpNextMove = all_in_one_copy(nextMove)
    selectedChess_piece = tmpBoard[tmpNextMove[0][0]][tmpNextMove[0][1]]
    tmpBoard[tmpNextMove[0][0]][tmpNextMove[0][1]] = "---"
    tmpBoard[tmpNextMove[1][0]][tmpNextMove[1][1]] = selectedChess_piece
    return tmpBoard
