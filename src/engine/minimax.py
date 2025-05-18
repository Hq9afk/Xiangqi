import random

import src.engine.chess_engine as e
from src.utils.utils import all_in_one_copy


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
        # Create a State instance for move generation and evaluation
        state = e.State()
        state.board = minimax_board
        state.turn_of_red = red_turn
        state.red_is_machine = red_is_machine
        minimax_next_move_list = all_in_one_copy(state.get_all_valid(state.board, state.turn_of_red, state.red_is_machine))
        if depth == 0 or minimax_next_move_list == []:
            self.evaluation_counter += 1
            return state.evaluate(unpredicted_board, red_turn, red_is_machine, move_counter, pre_guess_move)
        random.shuffle(minimax_next_move_list)

        if is_maximizing_player:
            best = float("-inf")
            for move in minimax_next_move_list:
                move_info = e.Move(minimax_board, move[0], move[1])
                next_board = all_in_one_copy(e.get_next_game_state(minimax_board, move))
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
                move_info = e.Move(minimax_board, move[0], move[1])
                next_board = all_in_one_copy(e.get_next_game_state(minimax_board, move))
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
