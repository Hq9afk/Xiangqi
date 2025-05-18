import csv
import os

scoreDir = "utils/score"

startPower = {"ch": 90, "hs": 40, "ep": 25, "ad": 30, "gn": 9000, "cn": 45, "sd": 10}  # Value of pieces at the start of the game
midPower = {"ch": 90, "hs": 40, "ep": 25, "ad": 30, "gn": 9000, "cn": 50, "sd": 20}  # Value of pieces at the middle of the game
endPower = {"ch": 100, "hs": 50, "ep": 40, "ad": 40, "gn": 9000, "cn": 40, "sd": 25}  # Value of pieces at the end of the game

# Count score at the bottom half of the board
bottomHalfPosition = {"ch": [], "hs": [], "ep": [], "ad": [], "gn": [], "cn": [], "sd": []}
for i in bottomHalfPosition.keys():
    with open(os.path.join(os.path.dirname(__file__), f"{scoreDir}/{i}.csv"), "r") as f:
        reader = csv.reader(f)
        for row in reader:
            for r in range(len(row)):
                row[r] = float(row[r])
            bottomHalfPosition[i] += [row]

# Count score at the upper half of the board
upperHalfPosition = {"ch": [], "hs": [], "ep": [], "ad": [], "gn": [], "cn": [], "sd": []}
for i in bottomHalfPosition.keys():
    upperHalfPosition[i] = bottomHalfPosition[i][::-1]


# Funtion that returns a list of valid Chariot moves
def chariotValidMoveList(board, position, redIsMachine):
    validMoveList = []
    chessSide = board[position[0]][position[1]][0]
    row = position[0]
    col = position[1]

    for x in range(row + 1, 10):
        if board[x][col] == "---":
            validMoveList += [(x, col)]

        elif board[x][col][0] != chessSide:
            validMoveList += [(x, col)]
            break
        else:
            break
    for x in range(row - 1, -1, -1):
        if board[x][col] == "---":
            validMoveList += [(x, col)]
        elif board[x][col][0] != chessSide:
            validMoveList += [(x, col)]
            break
        else:
            break
    for y in range(col + 1, 9):
        if board[row][y] == "---":
            validMoveList += [(row, y)]
        elif board[row][y][0] != chessSide:
            validMoveList += [(row, y)]
            break
        else:
            break
    for y in range(col - 1, -1, -1):
        if board[row][y] == "---":
            validMoveList += [(row, y)]
        elif board[row][y][0] != chessSide:
            validMoveList += [(row, y)]
            break
        else:
            break
    return validMoveList


# Function that returns list of valid Horse moves
def horseValidMoveList(board, position, redIsMachine):
    validMoveList = []
    chessSide = board[position[0]][position[1]][0]  # Chess side are black or red
    row = position[0]
    col = position[1]
    if col + 1 < 9:
        if board[row][col + 1] == "---":
            if col + 2 < 9 and row + 1 < 10 and (board[row + 1][col + 2] == "---" or board[row + 1][col + 2][0] != chessSide):
                validMoveList += [(row + 1, col + 2)]
            if col + 2 < 9 and row - 1 >= 0 and (board[row - 1][col + 2] == "---" or board[row - 1][col + 2][0] != chessSide):
                validMoveList += [(row - 1, col + 2)]
    if col - 1 >= 0:
        if board[row][col - 1] == "---":
            if col - 2 >= 0 and row + 1 < 10 and (board[row + 1][col - 2] == "---" or board[row + 1][col - 2][0] != chessSide):
                validMoveList += [(row + 1, col - 2)]

            if col - 2 >= 0 and row - 1 >= 0 and (board[row - 1][col - 2] == "---" or board[row - 1][col - 2][0] != chessSide):
                validMoveList += [(row - 1, col - 2)]
    if row + 1 < 10:
        if board[row + 1][col] == "---":
            if col + 1 < 9 and row + 2 < 10 and (board[row + 2][col + 1] == "---" or board[row + 2][col + 1][0] != chessSide):
                validMoveList += [(row + 2, col + 1)]

            if col - 1 >= 0 and row + 2 < 10 and (board[row + 2][col - 1] == "---" or board[row + 2][col - 1][0] != chessSide):
                validMoveList += [(row + 2, col - 1)]
    if row - 1 >= 0:
        if board[row - 1][col] == "---":
            if col + 1 < 9 and row - 2 >= 0 and (board[row - 2][col + 1] == "---" or board[row - 2][col + 1][0] != chessSide):
                validMoveList += [(row - 2, col + 1)]
            if col - 1 >= 0 and row - 2 >= 0 and (board[row - 2][col - 1] == "---" or board[row - 2][col - 1][0] != chessSide):
                validMoveList += [(row - 2, col - 1)]
    return validMoveList


# Function that returns a list of valid Elephant moves
def elephantValidMoveList(board, position, redIsMachine):
    validMoveList = []
    chessSide = board[position[0]][position[1]][0]
    row = position[0]
    col = position[1]
    candidateMoveList = [(row + 2, col + 2), (row + 2, col - 2), (row - 2, col + 2), (row - 2, col - 2)]
    if not redIsMachine:
        if chessSide == "b":
            for x in candidateMoveList:
                if 0 <= x[0] < 5 and 0 <= x[1] < 10:
                    if board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---" and board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 4 < x[0] < 10 and 0 <= x[1] < 10:
                    if board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---" and board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    else:
        if chessSide == "b":
            for x in candidateMoveList:
                if 5 <= x[0] < 10 and 0 <= x[1] < 10:
                    if board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---" and board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 0 <= x[0] < 6 and 0 <= x[1] < 10:
                    if board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---" and board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    return validMoveList


# Function that returns a list of valid Advisor moves
def advisorValidMoveList(board, position, redIsMachine):
    validMoveList = []
    row = position[0]
    col = position[1]
    chessSide = board[position[0]][position[1]][0]
    candidateMoveList = [(row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)]
    if not redIsMachine:
        if chessSide == "b":
            for x in candidateMoveList:
                if 0 <= x[0] < 3 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 7 <= x[0] < 10 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    else:
        if chessSide == "b":
            for x in candidateMoveList:
                if 7 <= x[0] < 10 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 0 <= x[0] < 3 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    return validMoveList


# # Function that returns a list of valid General moves
def GeneralValidMoveList(board, position, redIsMachine):
    validMoveList = []
    row = position[0]
    col = position[1]
    chessSide = board[position[0]][position[1]][0]
    candidateMoveList = [(row + 1, col), (row, col + 1), (row, col - 1), (row - 1, col)]
    if not redIsMachine:
        if chessSide == "b":
            for x in candidateMoveList:
                if 0 <= x[0] < 3 and 3 <= x[1] < 6:  # Row from 0 to 3, Col from 3 to 5
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]    
        else:
            for x in candidateMoveList:
                if 7 <= x[0] < 10 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    else:
        if chessSide == "b":
            for x in candidateMoveList:
                if 7 <= x[0] < 10 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 0 <= x[0] < 3 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    return validMoveList


# # Function that returns a list of valid Cannon moves
def cannonValidMoveList(board, position, redIsMachine):
    validMoveList = []
    row = position[0]
    j = position[1]
    chessSide = board[position[0]][position[1]][0]
    for x in range(row + 1, 10):
        if board[x][j] == "---":
            validMoveList += [(x, j)]
        else:  # meet the stone
            for y in range(x + 1, 10):
                if board[y][j][0] != chessSide and board[y][j] != "---":
                    validMoveList += [(y, j)]
                    break
                if board[y][j][0] == chessSide:
                    break
            break
    for x in range(row - 1, -1, -1):
        if board[x][j] == "---":
            validMoveList += [(x, j)]
        else:
            for y in range(x - 1, -1, -1):
                if board[y][j][0] != chessSide and board[y][j] != "---":
                    validMoveList += [(y, j)]
                    break
                if board[y][j][0] == chessSide:
                    break
            break
    for y in range(j + 1, 9):
        if board[row][y] == "---":
            validMoveList += [(row, y)]
        else:
            for x in range(y + 1, 9):
                if board[row][x][0] != chessSide and board[row][x] != "---":
                    validMoveList += [(row, x)]
                    break
                if board[row][x][0] == chessSide:
                    break
            break
    for y in range(j - 1, -1, -1):
        if board[row][y] == "---":
            validMoveList += [(row, y)]
        else:
            for x in range(y - 1, -1, -1):
                if board[row][x][0] != chessSide and board[row][x] != "---":
                    validMoveList += [(row, x)]
                    break
                if board[row][x][0] == chessSide:
                    break
            break
    return validMoveList


# # Function that returns a list of valid Soldier moves
def soldierValidMoveList(board, position, redIsMachine):
    validMoveList = []
    row = position[0]
    col = position[1]
    chessSide = board[position[0]][position[1]][0]

    if not redIsMachine:
        if chessSide == "b":
            candidate = [(row + 1, col)]
            if row > 4:
                candidate += [(row, col + 1), (row, col - 1)]
            for x in candidate:
                if 0 <= x[0] < 10 and 0 <= x[1] < 9:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]  # [(),(),(),()]
        else:
            candidate = [(row - 1, col)]
            if row < 5:
                candidate += [(row, col + 1), (row, col - 1)]
            for x in candidate:
                if 0 <= x[0] < 10 and 0 <= x[1] < 9:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    else:
        if chessSide == "b":
            candidate = [(row - 1, col)]
            if row < 5:
                candidate += [(row, col + 1), (row, col - 1)]
            for x in candidate:
                if 0 <= x[0] < 10 and 0 <= x[1] < 9:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
        else:
            candidate = [(row + 1, col)]
            if row > 4:
                candidate += [(row, col + 1), (row, col - 1)]
            for x in candidate:
                if 0 <= x[0] < 10 and 0 <= x[1] < 9:
                    if board[x[0]][x[1]][0] != chessSide:
                        validMoveList += [x]
    return validMoveList


# valid move list of two tuple [[(),()],...]
def moveRule(board, position, redIsMachine):
    piece_funcs = {
        "ch": chariotValidMoveList,
        "hs": horseValidMoveList,
        "cn": cannonValidMoveList,
        "gn": GeneralValidMoveList,
        "ad": advisorValidMoveList,
        "sd": soldierValidMoveList,
        "ep": elephantValidMoveList,
    }
    chessPiece = board[position[0]][position[1]][1:]
    func = piece_funcs.get(chessPiece)
    return func(board, position, redIsMachine) if func else []


# Function that returns list of valid move with some rules of this game
def moveCheckValid(board, redTurn, redIsMachine):
    Check = False
    blackGeneral, redGeneral = findGenerals(board)
    if redIsMachine:
        blackGeneral, redGeneral = redGeneral, blackGeneral
    if blackGeneral[1] == redGeneral[1]:
        for i in range(blackGeneral[0] + 1, redGeneral[0] + 1):
            if board[i][blackGeneral[1]] == "---":
                continue
            elif board[i][blackGeneral[1]][1:] == "gn":
                Check = True
                break
            else:
                break
        if Check:
            return False
    if isChecked(board, blackGeneral, redGeneral, not redTurn, redIsMachine):
        return False
    return True
    # check it later


def checkIllegalMove(gameState):
    # Find generals' positions
    blackGeneral, redGeneral = findGenerals(gameState.board)
    if isChecked(
        gameState.board,
        blackGeneral,
        redGeneral,
        gameState.redTurn,
        gameState.redIsMachine,
    ):
        print("Illegal move")
        gameState.undo()
        return True  # Move was illegal
    return False  # Move was legal


def findGenerals(board):
    blackGeneral = ()
    redGeneral = ()
    for i in range(0, 3):
        for j in range(3, 6):
            if board[i][j][1:] == "gn":
                blackGeneral = (i, j)
    for i in range(7, 10):
        for j in range(3, 6):
            if board[i][j][1:] == "gn":
                redGeneral = (i, j)
    return blackGeneral, redGeneral


# Function to check if the General is being checked
def isChecked(board, blackGeneral, redGeneral, redTurn, redIsMachine):
    # Check if the red General is being checked
    x = blackGeneral[0]
    y = blackGeneral[1]
    chessSide = "b"

    if not redTurn:
        x = redGeneral[0]
        y = redGeneral[1]
        chessSide = "r"

    # Horse check
    horsePositionList = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == "hs" and board[row][col][0] != chessSide:
                horsePositionList += [(row, col)]
    if horsePositionList != []:
        candidateGeneralThreatenList = [
            (x + 1, y + 2),
            (x + 1, y - 2),
            (x - 1, y + 2),
            (x - 1, y - 2),
            (x + 2, y + 1),
            (x + 2, y - 1),
            (x - 2, y + 1),
            (x - 2, y - 1),
        ]
        for i in horsePositionList:
            if i in candidateGeneralThreatenList:
                validHorseThreatList = horseValidMoveList(board, (i[0], i[1]), redIsMachine)
                if (x, y) in validHorseThreatList:
                    return True

    # Chariot check
    chariotPositionList = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == "ch" and board[row][col][0] != chessSide:
                chariotPositionList += [(row, col)]
    if chariotPositionList != []:
        for i in chariotPositionList:
            if i[0] == x:
                if i[1] < y:
                    for j in range(i[1], y):
                        if j == y - 1:
                            return True
                        if board[x][j + 1] != "---":
                            break
                if i[1] > y:
                    for j in range(y, i[1]):
                        if j == i[1] - 1:
                            return True
                        if board[x][j + 1] != "---":
                            break
            if i[1] == y:
                if i[0] < x:
                    for j in range(i[0], x):
                        if j == x - 1:
                            return True
                        if board[j + 1][y] != "---":
                            break
                if i[0] > x:
                    for j in range(x, i[0]):
                        if j == i[0] - 1:
                            return True
                        if board[j + 1][y] != "---":
                            break

    # Cannon check
    cannonPositionList = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == "cn" and board[row][col][0] != chessSide:
                cannonPositionList += [(row, col)]
    if cannonPositionList != []:
        stayaway = [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        candidateGeneralThreatenList = [(a, y) for a in range(10) if (a, y) not in stayaway] + [(x, b) for b in range(9) if (x, b) not in stayaway]

        for i in cannonPositionList:
            if i in candidateGeneralThreatenList:
                validCanonThreatList = cannonValidMoveList(board, i, redIsMachine)
                if (x, y) in validCanonThreatList:
                    return True

    # Soldier check
    soldierPostionList = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == "sd" and board[row][col][0] != chessSide:
                soldierPostionList += [(row, col)]
    if soldierPostionList != []:
        candidateGeneralThreatenList = [(x, y + 1), (x, y - 1)] + ([(x - 1, y)] if chessSide == "r" else [(x + 1, y)])
        for i in soldierPostionList:
            if i in candidateGeneralThreatenList:
                validSoldierThreatList = soldierValidMoveList(board, i, redIsMachine)
                if (x, y) in validSoldierThreatList:
                    return True
    return False
