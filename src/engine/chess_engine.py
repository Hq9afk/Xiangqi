from src.utils.utils import all_in_one_copy
from src.engine.rule import Rule as r

test_point_real = 0


class Move:
    row_id = {0: "10", 1: "9", 2: "8", 3: "7", 4: "6", 5: "5", 6: "4", 7: "3", 8: "2", 9: "1"}
    col_id = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h", 8: "i"}

    def __init__(self, board, start, end):
        self.board = all_in_one_copy(board)
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]
        self.piece_selected = board[self.start_row][self.start_col]
        self.piece_move_to = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def copy(self):
        return Move(self.board, (self.start_row, self.start_col), (self.end_row, self.end_col))

    def get_position(self, row, col):
        return self.col_id[col] + self.row_id[row]

    def __str__(self):
        return f"{self.piece_selected} {self.get_position(self.start_row, self.start_col)} ---> {self.get_position(self.end_row, self.end_col)}"


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
        self.turn_of_red = True
        self.red_is_machine = False
        self.move_log = []
        self.past_move_list = []
        self.selected_cell = ()
        self.black_general = (0, 4)
        self.red_general = (9, 4)
        self.is_game_start = False
        self.rule = r()

    def swap(self):
        for i in range(10):
            for j in range(9):
                if self.board[i][j][0] == "r":
                    self.board[i][j] = "b" + self.board[i][j][1:]
                elif self.board[i][j][0] == "b":
                    self.board[i][j] = "r" + self.board[i][j][1:]
        self.black_general, self.red_general = self.red_general, self.black_general
        self.red_is_machine = not self.red_is_machine

    def make_move(self, move: Move):
        tmp_board = all_in_one_copy(self.board)
        tmp_red_turn = self.turn_of_red
        tmp_black_general, tmp_red_general = self.black_general, self.red_general

        tmp_board[move.start_row][move.start_col] = "---"
        tmp_board[move.end_row][move.end_col] = move.piece_selected

        if move.piece_selected[1:] == "gn":
            if tmp_red_turn:
                tmp_red_general = (move.end_row, move.end_col)
            else:
                tmp_black_general = (move.end_row, move.end_col)

        if not self.rule.move_check_valid(tmp_board, tmp_red_turn, self.red_is_machine):
            print("Illegal move")
            return False
        else:
            self.board = all_in_one_copy(tmp_board)
            self.red_general, self.black_general = tmp_red_general, tmp_black_general
            self.past_move_list = []

            if len(self.move_log) >= 0 and len(self.move_log) <= 14:
                power = all_in_one_copy(self.rule.start_power)
            elif len(self.move_log) >= 14 and len(self.move_log) <= 50:
                power = all_in_one_copy(self.rule.mid_power)
            else:
                power = all_in_one_copy(self.rule.end_power)
            self.move_log.append(all_in_one_copy(move))
            global test_point_real
            test_chess_piece = move.piece_selected[1:]
            make_red_move = self.turn_of_red
            test_point_real += (
                (
                    (
                        0
                        - self.rule.upper_half_position[test_chess_piece][move.start_row][move.start_col]
                        + self.rule.upper_half_position[test_chess_piece][move.end_row][move.end_col]
                        + (power[move.piece_move_to[1:]] + self.rule.bottom_half_position[move.piece_move_to[1:]][move.end_row][move.end_col] if move.piece_move_to[1:] != "--" else 0)
                    )
                    if make_red_move
                    else (
                        0
                        + self.rule.bottom_half_position[test_chess_piece][move.start_row][move.start_col]
                        - self.rule.bottom_half_position[test_chess_piece][move.end_row][move.end_col]
                        - (power[move.piece_move_to[1:]] + self.rule.upper_half_position[move.piece_move_to[1:]][move.end_row][move.end_col] if move.piece_move_to[1:] != "--" else 0)
                    )
                )
                if self.red_is_machine
                else (
                    (
                        0
                        + self.rule.bottom_half_position[test_chess_piece][move.start_row][move.start_col]
                        - self.rule.bottom_half_position[test_chess_piece][move.end_row][move.end_col]
                        - (power[move.piece_move_to[1:]] + self.rule.upper_half_position[move.piece_move_to[1:]][move.end_row][move.end_col] if move.piece_move_to[1:] != "--" else 0)
                    )
                    if make_red_move
                    else (
                        0
                        - self.rule.upper_half_position[test_chess_piece][move.start_row][move.start_col]
                        + self.rule.upper_half_position[test_chess_piece][move.end_row][move.end_col]
                        + (power[move.piece_move_to[1:]] + self.rule.bottom_half_position[move.piece_move_to[1:]][move.end_row][move.end_col] if move.piece_move_to[1:] != "--" else 0)
                    )
                )
            )
            self.turn_of_red = not self.turn_of_red
            # print(move)

    def undo_move(self):
        print("Before undo: ", test_point_real)
        self.undo()
        self.undo()
        print("After undo: ", test_point_real)

    def redo_move(self):
        print("Before redo: ", test_point_real)
        self.redo()
        self.redo()
        print("After redo: ", test_point_real)

    def undo(self):
        global test_point_real
        if len(self.move_log) == 0:
            return
        last_move = all_in_one_copy(self.move_log[-1])
        self.board[last_move.start_row][last_move.start_col] = last_move.piece_selected
        self.board[last_move.end_row][last_move.end_col] = last_move.piece_move_to
        undo_red_turn = not self.turn_of_red

        if last_move.piece_selected[1:] == "gn":
            if undo_red_turn:
                self.red_general = (last_move.start_row, last_move.start_col)
            else:
                self.black_general = (last_move.start_row, last_move.start_col)

        self.past_move_list.append(all_in_one_copy(self.move_log.pop()))
        print("Undo number of moves: ", len(self.move_log))
        if len(self.move_log) >= 0 and len(self.move_log) <= 14:
            power = all_in_one_copy(self.rule.start_power)
        elif len(self.move_log) >= 14 and len(self.move_log) <= 50:
            power = all_in_one_copy(self.rule.mid_power)
        else:
            power = all_in_one_copy(self.rule.end_power)

        test_chess_piece = last_move.piece_selected[1:]
        undo_red_turn = not self.turn_of_red
        test_point_real -= (
            (
                (
                    0
                    - self.rule.upper_half_position[test_chess_piece][last_move.start_row][last_move.start_col]
                    + self.rule.upper_half_position[test_chess_piece][last_move.end_row][last_move.end_col]
                    + (power[last_move.piece_move_to[1:]] + self.rule.bottom_half_position[last_move.piece_move_to[1:]][last_move.end_row][last_move.end_col] if last_move.piece_move_to[1:] != "--" else 0)
                )
                if undo_red_turn
                else (
                    0
                    + self.rule.bottom_half_position[test_chess_piece][last_move.start_row][last_move.start_col]
                    - self.rule.bottom_half_position[test_chess_piece][last_move.end_row][last_move.end_col]
                    - (power[last_move.piece_move_to[1:]] + self.rule.upper_half_position[last_move.piece_move_to[1:]][last_move.end_row][last_move.end_col] if last_move.piece_move_to[1:] != "--" else 0)
                )
            )
            if self.red_is_machine
            else (
                (
                    0
                    + self.rule.bottom_half_position[test_chess_piece][last_move.start_row][last_move.start_col]
                    - self.rule.bottom_half_position[test_chess_piece][last_move.end_row][last_move.end_col]
                    - (power[last_move.piece_move_to[1:]] + self.rule.upper_half_position[last_move.piece_move_to[1:]][last_move.end_row][last_move.end_col] if last_move.piece_move_to[1:] != "--" else 0)
                )
                if undo_red_turn
                else (
                    0
                    - self.rule.upper_half_position[test_chess_piece][last_move.start_row][last_move.start_col]
                    + self.rule.upper_half_position[test_chess_piece][last_move.end_row][last_move.end_col]
                    + (power[last_move.piece_move_to[1:]] + self.rule.bottom_half_position[last_move.piece_move_to[1:]][last_move.end_row][last_move.end_col] if last_move.piece_move_to[1:] != "--" else 0)
                )
            )
        )
        self.turn_of_red = not self.turn_of_red
        print(last_move)

    def redo(self):
        global test_point_real
        if len(self.past_move_list) == 0:
            return
        next_move_in_storage = all_in_one_copy(self.past_move_list[-1])
        self.board[next_move_in_storage.start_row][next_move_in_storage.start_col] = "---"
        self.board[next_move_in_storage.end_row][next_move_in_storage.end_col] = next_move_in_storage.piece_selected
        redo_red_turn = self.turn_of_red
        if next_move_in_storage.piece_selected[1:] == "gn":
            if redo_red_turn:
                self.red_general = (next_move_in_storage.end_row, next_move_in_storage.end_col)
            else:
                self.black_general = (next_move_in_storage.end_row, next_move_in_storage.end_col)
        print("Redo number of moves: ", len(self.move_log))
        if len(self.move_log) >= 0 and len(self.move_log) <= 14:
            power = all_in_one_copy(self.rule.start_power)
        elif len(self.move_log) >= 14 and len(self.move_log) <= 50:
            power = all_in_one_copy(self.rule.mid_power)
        else:
            power = all_in_one_copy(self.rule.end_power)
        self.move_log.append(all_in_one_copy(self.past_move_list.pop()))

        test_chess_piece = next_move_in_storage.piece_selected[1:]
        test_point_real += (
            (
                (
                    0
                    - self.rule.upper_half_position[test_chess_piece][next_move_in_storage.start_row][next_move_in_storage.start_col]
                    + self.rule.upper_half_position[test_chess_piece][next_move_in_storage.end_row][next_move_in_storage.end_col]
                    + (power[next_move_in_storage.piece_move_to[1:]] + self.rule.bottom_half_position[next_move_in_storage.piece_move_to[1:]][next_move_in_storage.end_row][next_move_in_storage.end_col] if next_move_in_storage.piece_move_to[1:] != "--" else 0)
                )
                if redo_red_turn
                else (
                    0
                    + self.rule.bottom_half_position[test_chess_piece][next_move_in_storage.start_row][next_move_in_storage.start_col]
                    - self.rule.bottom_half_position[test_chess_piece][next_move_in_storage.end_row][next_move_in_storage.end_col]
                    - (power[next_move_in_storage.piece_move_to[1:]] + self.rule.upper_half_position[next_move_in_storage.piece_move_to[1:]][next_move_in_storage.end_row][next_move_in_storage.end_col] if next_move_in_storage.piece_move_to[1:] != "--" else 0)
                )
            )
            if self.red_is_machine
            else (
                (
                    0
                    + self.rule.bottom_half_position[test_chess_piece][next_move_in_storage.start_row][next_move_in_storage.start_col]
                    - self.rule.bottom_half_position[test_chess_piece][next_move_in_storage.end_row][next_move_in_storage.end_col]
                    - (power[next_move_in_storage.piece_move_to[1:]] + self.rule.upper_half_position[next_move_in_storage.piece_move_to[1:]][next_move_in_storage.end_row][next_move_in_storage.end_col] if next_move_in_storage.piece_move_to[1:] != "--" else 0)
                )
                if redo_red_turn
                else (
                    0
                    - self.rule.upper_half_position[test_chess_piece][next_move_in_storage.start_row][next_move_in_storage.start_col]
                    + self.rule.upper_half_position[test_chess_piece][next_move_in_storage.end_row][next_move_in_storage.end_col]
                    + (power[next_move_in_storage.piece_move_to[1:]] + self.rule.bottom_half_position[next_move_in_storage.piece_move_to[1:]][next_move_in_storage.end_row][next_move_in_storage.end_col] if next_move_in_storage.piece_move_to[1:] != "--" else 0)
                )
            )
        )
        self.turn_of_red = not self.turn_of_red
        print(next_move_in_storage)

    def check_valid(self, position):
        return self.rule.move_rule(self.board, position, self.red_is_machine)

    def check(self):
        return self.rule.is_checked(self.board, self.black_general, self.red_general, not self.turn_of_red, self.red_is_machine)

    def check_mate(self):
        if self.get_all_valid(self.board, self.turn_of_red, self.red_is_machine) == []:
            return True, "b" if self.turn_of_red else "r"
        return False, ""

    def get_all_valid(self, board, red_turn, red_is_machine):
        candidate_move_list = []
        valid_move_list = []
        turn = "r" if red_turn else "b"

        for row in range(10):
            for col in range(9):
                if board[row][col] != "---" and turn == board[row][col][0]:
                    candidate_move_list = self.rule.move_rule(board, (row, col), red_is_machine)
                    for cell in candidate_move_list:
                        move = Move(board, (row, col), cell)
                        tmp_board = all_in_one_copy(board)
                        tmp_red_turn = red_turn
                        tmp_board[move.start_row][move.start_col] = "---"
                        tmp_board[move.end_row][move.end_col] = move.piece_selected
                        if self.rule.move_check_valid(tmp_board, tmp_red_turn, red_is_machine):
                            valid_move_list.append([(row, col), cell])
        return valid_move_list

    def evaluate(self, board, red_turn, red_is_machine, move_counter, pre_guess_move):
        global test_point_real
        tmp_red_turn = red_is_machine
        test_point = test_point_real
        if pre_guess_move is not None:
            for move in pre_guess_move:
                if move_counter >= 0 and move_counter <= 14:
                    power = all_in_one_copy(self.rule.start_power)
                elif move_counter >= 14 and move_counter <= 50:
                    power = all_in_one_copy(self.rule.mid_power)
                else:
                    power = all_in_one_copy(self.rule.end_power)

                test_chess_piece = move.piece_selected[1:]
                test_point += (
                    (
                        (
                            0
                            - self.rule.upper_half_position[test_chess_piece][move.start_row][move.start_col]
                            + self.rule.upper_half_position[test_chess_piece][move.end_row][move.end_col]
                            + ((power[move.piece_move_to[1:]]) + self.rule.bottom_half_position[move.piece_move_to[1:]][move.end_row][move.end_col] if move.piece_move_to[1:] != "--" else 0)
                        )
                        if tmp_red_turn
                        else (
                            0
                            + self.rule.bottom_half_position[test_chess_piece][move.start_row][move.start_col]
                            - self.rule.bottom_half_position[test_chess_piece][move.end_row][move.end_col]
                            - (power[move.piece_move_to[1:]] + self.rule.upper_half_position[move.piece_move_to[1:]][move.end_row][move.end_col] if move.piece_move_to[1:] != "--" else 0)
                        )
                    )
                    if red_is_machine
                    else (
                        (
                            0
                            + self.rule.bottom_half_position[test_chess_piece][move.start_row][move.start_col]
                            - self.rule.bottom_half_position[test_chess_piece][move.end_row][move.end_col]
                            - (power[move.piece_move_to[1:]] + self.rule.upper_half_position[move.piece_move_to[1:]][move.end_row][move.end_col] if move.piece_move_to[1:] != "--" else 0)
                        )
                        if tmp_red_turn
                        else (
                            0
                            - self.rule.upper_half_position[test_chess_piece][move.start_row][move.start_col]
                            + self.rule.upper_half_position[test_chess_piece][move.end_row][move.end_col]
                            + (power[move.piece_move_to[1:]] + self.rule.bottom_half_position[move.piece_move_to[1:]][move.end_row][move.end_col] if move.piece_move_to[1:] != "--" else 0)
                        )
                    )
                )
                move_counter += 1
                tmp_red_turn = not tmp_red_turn
        return test_point

    def get_next_game_state(self, board, next_move):
        tmp_board = all_in_one_copy(board)
        if isinstance(next_move, Move):
            copy_next_move = next_move.copy()
            tmp_next_move = [(copy_next_move.start_row, copy_next_move.start_col), (copy_next_move.end_row, copy_next_move.end_col)]
        else:
            tmp_next_move = all_in_one_copy(next_move)
        selected_chess_piece = tmp_board[tmp_next_move[0][0]][tmp_next_move[0][1]]
        tmp_board[tmp_next_move[0][0]][tmp_next_move[0][1]] = "---"
        tmp_board[tmp_next_move[1][0]][tmp_next_move[1][1]] = selected_chess_piece
        return tmp_board
