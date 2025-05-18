import csv
import os

score_directory = "utils/score"

start_power = {"ch": 90, "hs": 40, "ep": 25, "ad": 30, "gn": 9000, "cn": 45, "sd": 10}
mid_power = {"ch": 90, "hs": 40, "ep": 25, "ad": 30, "gn": 9000, "cn": 50, "sd": 20}
end_power = {"ch": 100, "hs": 50, "ep": 40, "ad": 40, "gn": 9000, "cn": 40, "sd": 25}

bottom_half_position = {"ch": [], "hs": [], "ep": [], "ad": [], "gn": [], "cn": [], "sd": []}
for i in bottom_half_position.keys():
    with open(os.path.join(os.path.dirname(__file__), f"{score_directory}/{i}.csv"), "r") as f:
        reader = csv.reader(f)
        for row in reader:
            for r in range(len(row)):
                row[r] = float(row[r])
            bottom_half_position[i] += [row]

upper_half_position = {"ch": [], "hs": [], "ep": [], "ad": [], "gn": [], "cn": [], "sd": []}
for i in bottom_half_position.keys():
    upper_half_position[i] = bottom_half_position[i][::-1]


def chariot_valid_move_list(board, position, red_is_machine):
    valid_move_list = []
    chess_side = board[position[0]][position[1]][0]
    row = position[0]
    col = position[1]

    for x in range(row + 1, 10):
        if board[x][col] == "---":
            valid_move_list += [(x, col)]
        elif board[x][col][0] != chess_side:
            valid_move_list += [(x, col)]
            break
        else:
            break
    for x in range(row - 1, -1, -1):
        if board[x][col] == "---":
            valid_move_list += [(x, col)]
        elif board[x][col][0] != chess_side:
            valid_move_list += [(x, col)]
            break
        else:
            break
    for y in range(col + 1, 9):
        if board[row][y] == "---":
            valid_move_list += [(row, y)]
        elif board[row][y][0] != chess_side:
            valid_move_list += [(row, y)]
            break
        else:
            break
    for y in range(col - 1, -1, -1):
        if board[row][y] == "---":
            valid_move_list += [(row, y)]
        elif board[row][y][0] != chess_side:
            valid_move_list += [(row, y)]
            break
        else:
            break
    return valid_move_list


def horse_valid_move_list(board, position, red_is_machine):
    valid_move_list = []
    side = board[position[0]][position[1]][0]
    row = position[0]
    col = position[1]
    if col + 1 < 9:
        if board[row][col + 1] == "---":
            if col + 2 < 9 and row + 1 < 10 and (board[row + 1][col + 2] == "---" or board[row + 1][col + 2][0] != side):
                valid_move_list += [(row + 1, col + 2)]
            if col + 2 < 9 and row - 1 >= 0 and (board[row - 1][col + 2] == "---" or board[row - 1][col + 2][0] != side):
                valid_move_list += [(row - 1, col + 2)]
    if col - 1 >= 0:
        if board[row][col - 1] == "---":
            if col - 2 >= 0 and row + 1 < 10 and (board[row + 1][col - 2] == "---" or board[row + 1][col - 2][0] != side):
                valid_move_list += [(row + 1, col - 2)]
            if col - 2 >= 0 and row - 1 >= 0 and (board[row - 1][col - 2] == "---" or board[row - 1][col - 2][0] != side):
                valid_move_list += [(row - 1, col - 2)]
    if row + 1 < 10:
        if board[row + 1][col] == "---":
            if col + 1 < 9 and row + 2 < 10 and (board[row + 2][col + 1] == "---" or board[row + 2][col + 1][0] != side):
                valid_move_list += [(row + 2, col + 1)]
            if col - 1 >= 0 and row + 2 < 10 and (board[row + 2][col - 1] == "---" or board[row + 2][col - 1][0] != side):
                valid_move_list += [(row + 2, col - 1)]
    if row - 1 >= 0:
        if board[row - 1][col] == "---":
            if col + 1 < 9 and row - 2 >= 0 and (board[row - 2][col + 1] == "---" or board[row - 2][col + 1][0] != side):
                valid_move_list += [(row - 2, col + 1)]
            if col - 1 >= 0 and row - 2 >= 0 and (board[row - 2][col - 1] == "---" or board[row - 2][col - 1][0] != side):
                valid_move_list += [(row - 2, col - 1)]
    return valid_move_list


def elephant_valid_move_list(board, position, red_is_machine):
    valid_move_list = []
    side = board[position[0]][position[1]][0]
    row = position[0]
    col = position[1]
    candidate_move_list = [(row + 2, col + 2), (row + 2, col - 2), (row - 2, col + 2), (row - 2, col - 2)]
    if not red_is_machine:
        if side == "b":
            for x in candidate_move_list:
                if 0 <= x[0] < 5 and 0 <= x[1] < 10:
                    if board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---" and board[x[0]][x[1]][0] != side:
                        valid_move_list += [x]
        else:
            for x in candidate_move_list:
                if 4 < x[0] < 10 and 0 <= x[1] < 10:
                    if board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---" and board[x[0]][x[1]][0] != side:
                        valid_move_list += [x]
    else:
        if side == "b":
            for x in candidate_move_list:
                if 5 <= x[0] < 10 and 0 <= x[1] < 10:
                    if board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---" and board[x[0]][x[1]][0] != side:
                        valid_move_list += [x]
        else:
            for x in candidate_move_list:
                if 0 <= x[0] < 6 and 0 <= x[1] < 10:
                    if board[int((row + x[0]) / 2)][int((col + x[1]) / 2)] == "---" and board[x[0]][x[1]][0] != side:
                        valid_move_list += [x]
    return valid_move_list


def advisor_valid_move_list(board, position, red_is_machine):
    valid_move_list = []
    row = position[0]
    col = position[1]
    side = board[position[0]][position[1]][0]
    candidate_move_list = [(row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)]
    if not red_is_machine:
        if side == "b":
            for x in candidate_move_list:
                if 0 <= x[0] < 3 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != side:
                        valid_move_list += [x]
        else:
            for x in candidate_move_list:
                if 7 <= x[0] < 10 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != side:
                        valid_move_list += [x]
    else:
        if side == "b":
            for x in candidate_move_list:
                if 7 <= x[0] < 10 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != side:
                        valid_move_list += [x]
        else:
            for x in candidate_move_list:
                if 0 <= x[0] < 3 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != side:
                        valid_move_list += [x]
    return valid_move_list


def general_valid_move_list(board, position, red_is_machine):
    valid_move_list = []
    row = position[0]
    col = position[1]
    chess_side = board[position[0]][position[1]][0]
    candidate_move_list = [(row + 1, col), (row, col + 1), (row, col - 1), (row - 1, col)]
    if not red_is_machine:
        if chess_side == "b":
            for x in candidate_move_list:
                if 0 <= x[0] < 3 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chess_side:
                        valid_move_list += [x]
        else:
            for x in candidate_move_list:
                if 7 <= x[0] < 10 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chess_side:
                        valid_move_list += [x]
    else:
        if chess_side == "b":
            for x in candidate_move_list:
                if 7 <= x[0] < 10 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chess_side:
                        valid_move_list += [x]
        else:
            for x in candidate_move_list:
                if 0 <= x[0] < 3 and 3 <= x[1] < 6:
                    if board[x[0]][x[1]][0] != chess_side:
                        valid_move_list += [x]
    return valid_move_list


def cannon_valid_move_list(board, position, red_is_machine):
    valid_move_list = []
    row = position[0]
    j = position[1]
    chess_side = board[position[0]][position[1]][0]
    for x in range(row + 1, 10):
        if board[x][j] == "---":
            valid_move_list += [(x, j)]
        else:
            for y in range(x + 1, 10):
                if board[y][j][0] != chess_side and board[y][j] != "---":
                    valid_move_list += [(y, j)]
                    break
                if board[y][j][0] == chess_side:
                    break
            break
    for x in range(row - 1, -1, -1):
        if board[x][j] == "---":
            valid_move_list += [(x, j)]
        else:
            for y in range(x - 1, -1, -1):
                if board[y][j][0] != chess_side and board[y][j] != "---":
                    valid_move_list += [(y, j)]
                    break
                if board[y][j][0] == chess_side:
                    break
            break
    for y in range(j + 1, 9):
        if board[row][y] == "---":
            valid_move_list += [(row, y)]
        else:
            for x in range(y + 1, 9):
                if board[row][x][0] != chess_side and board[row][x] != "---":
                    valid_move_list += [(row, x)]
                    break
                if board[row][x][0] == chess_side:
                    break
            break
    for y in range(j - 1, -1, -1):
        if board[row][y] == "---":
            valid_move_list += [(row, y)]
        else:
            for x in range(y - 1, -1, -1):
                if board[row][x][0] != chess_side and board[row][x] != "---":
                    valid_move_list += [(row, x)]
                    break
                if board[row][x][0] == chess_side:
                    break
            break
    return valid_move_list


def soldier_valid_move_list(board, position, red_is_machine):
    valid_move_list = []
    row = position[0]
    col = position[1]
    chess_side = board[position[0]][position[1]][0]

    if not red_is_machine:
        if chess_side == "b":
            candidate = [(row + 1, col)]
            if row > 4:
                candidate += [(row, col + 1), (row, col - 1)]
            for x in candidate:
                if 0 <= x[0] < 10 and 0 <= x[1] < 9:
                    if board[x[0]][x[1]][0] != chess_side:
                        valid_move_list += [x]
        else:
            candidate = [(row - 1, col)]
            if row < 5:
                candidate += [(row, col + 1), (row, col - 1)]
            for x in candidate:
                if 0 <= x[0] < 10 and 0 <= x[1] < 9:
                    if board[x[0]][x[1]][0] != chess_side:
                        valid_move_list += [x]
    else:
        if chess_side == "b":
            candidate = [(row - 1, col)]
            if row < 5:
                candidate += [(row, col + 1), (row, col - 1)]
            for x in candidate:
                if 0 <= x[0] < 10 and 0 <= x[1] < 9:
                    if board[x[0]][x[1]][0] != chess_side:
                        valid_move_list += [x]
        else:
            candidate = [(row + 1, col)]
            if row > 4:
                candidate += [(row, col + 1), (row, col - 1)]
            for x in candidate:
                if 0 <= x[0] < 10 and 0 <= x[1] < 9:
                    if board[x[0]][x[1]][0] != chess_side:
                        valid_move_list += [x]
    return valid_move_list


def move_rule(board, position, red_is_machine):
    piece_funcs = {
        "ch": chariot_valid_move_list,
        "hs": horse_valid_move_list,
        "cn": cannon_valid_move_list,
        "gn": general_valid_move_list,
        "ad": advisor_valid_move_list,
        "sd": soldier_valid_move_list,
        "ep": elephant_valid_move_list,
    }
    chess_piece = board[position[0]][position[1]][1:]
    func = piece_funcs.get(chess_piece)
    return func(board, position, red_is_machine) if func else []


def move_check_valid(board, red_turn, red_is_machine):
    check = False
    black_general, red_general = find_generals(board)
    if red_is_machine:
        black_general, red_general = red_general, black_general
    if black_general[1] == red_general[1]:
        for i in range(black_general[0] + 1, red_general[0] + 1):
            if board[i][black_general[1]] == "---":
                continue
            elif board[i][black_general[1]][1:] == "gn":
                check = True
                break
            else:
                break
        if check:
            return False
    if is_checked(board, black_general, red_general, not red_turn, red_is_machine):
        return False
    return True


def check_illegal_move(game_state):
    black_general, red_general = find_generals(game_state.board)
    if is_checked(
        game_state.board,
        black_general,
        red_general,
        game_state.red_turn,
        game_state.red_is_machine,
    ):
        print("Illegal move")
        game_state.undo()
        return True
    return False


def find_generals(board):
    black_general = ()
    red_general = ()
    for i in range(0, 3):
        for j in range(3, 6):
            if board[i][j][1:] == "gn":
                black_general = (i, j)
    for i in range(7, 10):
        for j in range(3, 6):
            if board[i][j][1:] == "gn":
                red_general = (i, j)
    return black_general, red_general


def is_checked(board, black_general, red_general, red_turn, red_is_machine):
    x = black_general[0]
    y = black_general[1]
    chess_side = "b"

    if not red_turn:
        x = red_general[0]
        y = red_general[1]
        chess_side = "r"

    horse_position_list = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == "hs" and board[row][col][0] != chess_side:
                horse_position_list += [(row, col)]
    if horse_position_list != []:
        candidate_general_threaten_list = [
            (x + 1, y + 2),
            (x + 1, y - 2),
            (x - 1, y + 2),
            (x - 1, y - 2),
            (x + 2, y + 1),
            (x + 2, y - 1),
            (x - 2, y + 1),
            (x - 2, y - 1),
        ]
        for i in horse_position_list:
            if i in candidate_general_threaten_list:
                valid_horse_threat_list = horse_valid_move_list(board, (i[0], i[1]), red_is_machine)
                if (x, y) in valid_horse_threat_list:
                    return True

    chariot_position_list = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == "ch" and board[row][col][0] != chess_side:
                chariot_position_list += [(row, col)]
    if chariot_position_list != []:
        for i in chariot_position_list:
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

    cannon_position_list = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == "cn" and board[row][col][0] != chess_side:
                cannon_position_list += [(row, col)]
    if cannon_position_list != []:
        stayaway = [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        candidate_general_threaten_list = [(a, y) for a in range(10) if (a, y) not in stayaway] + [(x, b) for b in range(9) if (x, b) not in stayaway]

        for i in cannon_position_list:
            if i in candidate_general_threaten_list:
                valid_canon_threat_list = cannon_valid_move_list(board, i, red_is_machine)
                if (x, y) in valid_canon_threat_list:
                    return True

    soldier_position_list = []
    for row in range(10):
        for col in range(9):
            if board[row][col][1:] == "sd" and board[row][col][0] != chess_side:
                soldier_position_list += [(row, col)]
    if soldier_position_list != []:
        candidate_general_threaten_list = [(x, y + 1), (x, y - 1)] + ([(x - 1, y)] if chess_side == "r" else [(x + 1, y)])
        for i in soldier_position_list:
            if i in candidate_general_threaten_list:
                valid_soldier_threat_list = soldier_valid_move_list(board, i, red_is_machine)
                if (x, y) in valid_soldier_threat_list:
                    return True
    return False
