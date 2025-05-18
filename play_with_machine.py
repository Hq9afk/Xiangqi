import random
import chess_engine as s
import time


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
            # dict[str, int]
            return original.copy()
    else:
        return original[:]  # fallback shallow copy for simple lists


class Minimax:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.minimax_suggested_move = None
        self.evaluation_counter = 0

    # Minimax algorithm
    # Explain MiniMax algo: If your current best result is better than/equal the current worst result your enemy can bring to you,
    # then no need to search that branch anymore because your enemy will definitely only continue to choose the result even more worse than that,
    # or at least equal. Hence you can skip that branch because you know now for sure that you already having a better result stored.
    def initiate_minimax(
        self,
        board,
        unpredicted_board,
        red_turn,
        red_is_machine,
        depth,
        is_maximizing_player,
        move_counter,
        pre_guess_move,
        alpha=float("-inf"),
        beta=float("inf"),
    ):
        minimax_board = all_in_one_copy(board)
        minimax_next_move_list = all_in_one_copy(s.State.get_all_valid(minimax_board, red_turn, red_is_machine))
        if depth == 0 or minimax_next_move_list == []:
            self.evaluation_counter += 1
            return s.State.evaluate(unpredicted_board, red_turn, red_is_machine, move_counter, pre_guess_move)
        random.shuffle(minimax_next_move_list)

        if is_maximizing_player:
            best = float("-inf")
            for move in minimax_next_move_list:
                move_info = s.Move(minimax_board, move[0], move[1])
                next_board = all_in_one_copy(s.get_next_game_state(minimax_board, move))
                pre_guess_move.append(move_info)
                value = self.initiate_minimax(
                    next_board,
                    unpredicted_board,
                    not red_turn,
                    red_is_machine,
                    depth - 1,
                    False,
                    move_counter,
                    pre_guess_move,
                    alpha,
                    beta,
                )
                pre_guess_move.pop()
                if value > best:
                    best = value
                    if depth == self.max_depth:
                        self.minimax_suggested_move = all_in_one_copy(move)
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
            return best
        else:
            best = float("inf")
            for move in minimax_next_move_list:
                move_info = s.Move(minimax_board, move[0], move[1])
                next_board = all_in_one_copy(s.getNextGameState(minimax_board, move))
                pre_guess_move.append(move_info)
                value = self.initiate_minimax(
                    next_board,
                    unpredicted_board,
                    not red_turn,
                    red_is_machine,
                    depth - 1,
                    True,
                    move_counter,
                    pre_guess_move,
                    alpha,
                    beta,
                )
                pre_guess_move.pop()
                if value < best:
                    best = value
                    if depth == self.max_depth:
                        self.minimax_suggested_move = all_in_one_copy(move)
                beta = min(beta, best)
                if alpha >= beta:
                    break
            return best


def play_with_random(state):
    move_list = all_in_one_copy(s.State.get_all_valid(state.board, state.turn_of_red, state.red_is_machine))
    if move_list != []:
        move = random.choice(move_list)
        return s.Move(state.board, move[0], move[1])
    return None


def play_with_ai(state):
    minimax = Minimax(1)
    start_time = time.time()
    minimax.initiate_minimax(
        state.board,
        state.board,
        state.turn_of_red,
        state.red_is_machine,
        minimax.max_depth,
        True,
        len(state.move_log),
        pre_guess_move=[],
    )
    move = minimax.minimax_suggested_move
    end_time = time.time()
    duration = end_time - start_time
    print(f"Minimax took {duration:.4f} seconds and {minimax.evaluation_counter} evaluations to return a move.")
    if move is not None:
        m = s.Move(state.board, move[0], move[1])
        return m
    return None


def ai_vs_random(state):
    play = None
    if state.red_is_machine:
        if state.turn_of_red:
            play = play_with_ai(state)
            if play:
                state.make_move(play)
        else:
            play = play_with_random(state)
            if play:
                state.makeMove(play)
    else:
        if state.turn_of_red:
            play = play_with_random(state)
        else:
            play = play_with_ai(state)
        return play


def game_mode_manager(state, type):
    turn = True if (state.red_is_machine and state.turn_of_red) or (not state.red_is_machine and not state.turn_of_red) else False
    if turn:
        play = None
        if type == 1:
            play = play_with_random(state)
        elif type == 2:
            play = play_with_ai(state)
        elif type == 3:
            play = ai_vs_random(state)
        if play:
            state.makeMove(play)
