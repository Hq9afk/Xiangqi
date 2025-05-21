import csv
import os
import chessEngine as s

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
        
def get_chess_piece_positions(data, piece):
    if piece not in data:
        return []
    # data[piece] is a frozenset of encoded positions
    return [decode_pos(pos) for pos in data[piece]]

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
            elif isinstance(original, s.Move):
                return original.copy()
            elif isinstance(original, dict):
                first_val = next(iter(original.values()))
                if isinstance(first_val, int):
                    return original.copy()
                elif isinstance(first_val, frozenset):
                    return dict(original)
        else:
            return original  # return as-is for unknown types

startPower = {
    "ch": 90,
    "hs": 40,
    "ep": 25,
    "ad": 30,
    "gn": 9000,
    "cn": 45,
    "sd": 10,
}  # Value of pieces at the start of the game
midPower = {
    "ch": 90,
    "hs": 40,
    "ep": 25,
    "ad": 30,
    "gn": 9000,
    "cn": 50,
    "sd": 20,
}  # Value of pieces at the middle of the game
endPower = {
    "ch": 100,
    "hs": 50,
    "ep": 40,
    "ad": 40,
    "gn": 9000,
    "cn": 40,
    "sd": 25,
}  # Value of pieces at the end of the game

# Count score at the bottom half of the board
bottomHalfPosition = {
    "ch": [],
    "hs": [],
    "ep": [],
    "ad": [],
    "gn": [],
    "cn": [],
    "sd": [],
}
for i in bottomHalfPosition.keys():
    name = i + ".csv"
    with open(os.path.join(os.path.dirname(__file__), "unity", name), "r") as f:
        reader = csv.reader(f)
        for row in reader:
            for r in range(len(row)):
                row[r] = float(row[r])
            bottomHalfPosition[i] += [row]

# Count score at the upper half of the board
upperHalfPosition = {
    "ch": [],
    "hs": [],
    "ep": [],
    "ad": [],
    "gn": [],
    "cn": [],
    "sd": [],
}
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
            if (
                col + 2 < 9
                and row + 1 < 10
                and (
                    board[row + 1][col + 2] == "---"
                    or board[row + 1][col + 2][0] != chessSide
                )
            ):
                validMoveList += [(row + 1, col + 2)]
            if (
                col + 2 < 9
                and row - 1 >= 0
                and (
                    board[row - 1][col + 2] == "---"
                    or board[row - 1][col + 2][0] != chessSide
                )
            ):
                validMoveList += [(row - 1, col + 2)]
    if col - 1 >= 0:
        if board[row][col - 1] == "---":
            if (
                col - 2 >= 0
                and row + 1 < 10
                and (
                    board[row + 1][col - 2] == "---"
                    or board[row + 1][col - 2][0] != chessSide
                )
            ):
                validMoveList += [(row + 1, col - 2)]

            if (
                col - 2 >= 0
                and row - 1 >= 0
                and (
                    board[row - 1][col - 2] == "---"
                    or board[row - 1][col - 2][0] != chessSide
                )
            ):
                validMoveList += [(row - 1, col - 2)]
    if row + 1 < 10:
        if board[row + 1][col] == "---":
            if (
                col + 1 < 9
                and row + 2 < 10
                and (
                    board[row + 2][col + 1] == "---"
                    or board[row + 2][col + 1][0] != chessSide
                )
            ):
                validMoveList += [(row + 2, col + 1)]

            if (
                col - 1 >= 0
                and row + 2 < 10
                and (
                    board[row + 2][col - 1] == "---"
                    or board[row + 2][col - 1][0] != chessSide
                )
            ):
                validMoveList += [(row + 2, col - 1)]
    if row - 1 >= 0:
        if board[row - 1][col] == "---":
            if (
                col + 1 < 9
                and row - 2 >= 0
                and (
                    board[row - 2][col + 1] == "---"
                    or board[row - 2][col + 1][0] != chessSide
                )
            ):
                validMoveList += [(row - 2, col + 1)]
            if (
                col - 1 >= 0
                and row - 2 >= 0
                and (
                    board[row - 2][col - 1] == "---"
                    or board[row - 2][col - 1][0] != chessSide
                )
            ):
                validMoveList += [(row - 2, col - 1)]
    return validMoveList


# Function that returns a list of valid Elephant moves
def elephantValidMoveList(board, position, redIsMachine):
    validMoveList = []
    chessSide = board[position[0]][position[1]][0]
    row = position[0]
    col = position[1]
    candidateMoveList = [
        (row + 2, col + 2),
        (row + 2, col - 2),
        (row - 2, col + 2),
        (row - 2, col - 2),
    ]
    if not redIsMachine:
        if chessSide == "b":
            for x in candidateMoveList:
                if 0 <= x[0] < 5 and 0 <= x[1] < 10:
                    if (
                        board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---"
                        and board[x[0]][x[1]][0] != chessSide
                    ):
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 4 < x[0] < 10 and 0 <= x[1] < 10:
                    if (
                        board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---"
                        and board[x[0]][x[1]][0] != chessSide
                    ):
                        validMoveList += [x]
    else:
        if chessSide == "b":
            for x in candidateMoveList:
                if 5 <= x[0] < 10 and 0 <= x[1] < 10:
                    if (
                        board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---"
                        and board[x[0]][x[1]][0] != chessSide
                    ):
                        validMoveList += [x]
        else:
            for x in candidateMoveList:
                if 0 <= x[0] < 6 and 0 <= x[1] < 10:
                    if (
                        board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---"
                        and board[x[0]][x[1]][0] != chessSide
                    ):
                        validMoveList += [x]
    return validMoveList


# Function that returns a list of valid Advisor moves
def advisorValidMoveList(board, position, redIsMachine):
    validMoveList = []
    row = position[0]
    col = position[1]
    chessSide = board[position[0]][position[1]][0]
    candidateMoveList = [
        (row + 1, col + 1),
        (row + 1, col - 1),
        (row - 1, col + 1),
        (row - 1, col - 1),
    ]
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
def moveRule(board, position, redIsMachine):  # (), redIsMachine is after
    chessPiece = board[position[0]][position[1]][1:]
    validMoveList = []
    if chessPiece == "ch":
        validMoveList = chariotValidMoveList(board, position, redIsMachine)
    elif chessPiece == "hs":
        validMoveList = horseValidMoveList(board, position, redIsMachine)
    elif chessPiece == "cn":
        validMoveList = cannonValidMoveList(board, position, redIsMachine)
    elif chessPiece == "gn":
        validMoveList = GeneralValidMoveList(board, position, redIsMachine)
    elif chessPiece == "ad":
        validMoveList = advisorValidMoveList(board, position, redIsMachine)
    elif chessPiece == "sd":
        validMoveList = soldierValidMoveList(board, position, redIsMachine)
    elif chessPiece == "ep":
        validMoveList = elephantValidMoveList(board, position, redIsMachine)
    return validMoveList


# Function that returns list of valid move with some rules of this game
def moveCheckValid(board, red_chess_piece_pos_dict, black_chess_piece_pos_dict, redTurn, redIsMachine):
    Check = False
    blackGeneral = get_chess_piece_positions(black_chess_piece_pos_dict, "gn")[0]
    redGeneral = get_chess_piece_positions(red_chess_piece_pos_dict, "gn")[0]
        
    step = 1 if blackGeneral[0] < redGeneral[0] else -1
    if blackGeneral[1] == redGeneral[1]:
        for i in range(blackGeneral[0] + step, redGeneral[0] + step, step):
            if board[i][blackGeneral[1]] == "---":
                continue
            elif board[i][blackGeneral[1]][1:] == "gn":
                Check = True
                break
            else:
                break
        if Check:
            return False
    if isChecked(board, blackGeneral, redGeneral, red_chess_piece_pos_dict, black_chess_piece_pos_dict, not redTurn, redIsMachine):
        return False
    return True
    # check it later


# Function to check if the General is being checked
def isChecked(board, blackGeneral, redGeneral, red_chess_piece_pos_dict, black_chess_piece_pos_dict, redTurn, redIsMachine):
    # Check if the red General is being checked
    x = 0
    y = 0
    chessSide = ''
    chess_piece_pos_dict = {}
    if redTurn:
        x = blackGeneral[0]
        y = blackGeneral[1]
        chessSide = "b"
        chess_piece_pos_dict = red_chess_piece_pos_dict
    else:
        x = redGeneral[0]
        y = redGeneral[1]
        chessSide = "r"
        chess_piece_pos_dict = black_chess_piece_pos_dict

    # Horse check
    horsePositionList = get_chess_piece_positions(chess_piece_pos_dict, "hs")
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
                validHorseThreatList = horseValidMoveList(
                    board, (i[0], i[1]), redIsMachine
                )
                if (x, y) in validHorseThreatList:
                    return True

    # Chariot check
    chariotPositionList = get_chess_piece_positions(chess_piece_pos_dict, "ch")
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
    cannonPositionList = get_chess_piece_positions(chess_piece_pos_dict, "cn")
    if cannonPositionList != []:
        stayaway = [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        candidateGeneralThreatenList = [
            (a, y) for a in range(10) if (a, y) not in stayaway
        ] + [(x, b) for b in range(9) if (x, b) not in stayaway]

        for i in cannonPositionList:
            if i in candidateGeneralThreatenList:
                validCanonThreatList = cannonValidMoveList(board, i, redIsMachine)
                if (x, y) in validCanonThreatList:
                    return True

    # Soldier check
    soldierPostionList = get_chess_piece_positions(chess_piece_pos_dict, "sd")
    if soldierPostionList != []:
        candidateGeneralThreatenList = [(x, y + 1), (x, y - 1)] + (
            [(x - 1, y)] if chessSide == "r" else [(x + 1, y)]
        )
        for i in soldierPostionList:
            if i in candidateGeneralThreatenList:
                validSoldierThreatList = soldierValidMoveList(board, i, redIsMachine)
                if (x, y) in validSoldierThreatList:
                    return True
    return False
