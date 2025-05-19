import random
import time

import src.engine.chess_engine as e
from src.utils.utils import all_in_one_copy
from .minimax import Minimax


class GameModeManager:
    def __init__(self, state):
        self.state = state

    def play_with_random(self):
        # Play a random valid move
        move_list = all_in_one_copy(self.state.get_all_valid(self.state.board, self.state.turn_of_red, self.state.red_is_machine))
        if move_list:
            move = random.choice(move_list)
            return e.Move(self.state.board, move[0], move[1])
        return None

    def play_with_ai(self):
        # Play a move using the Minimax AI
        minimax = Minimax(1)
        start_time = time.time()
        minimax.initiate_minimax(
            self.state.board,
            self.state.board,
            self.state.turn_of_red,
            self.state.red_is_machine,
            minimax.max_depth,
            True,
            len(self.state.move_log),
            pre_guess_move=[],
        )
        move = minimax.minimax_suggested_move
        end_time = time.time()
        duration = end_time - start_time
        print(f"Minimax took {duration:.4f} seconds and {minimax.evaluation_counter} evaluations to return a move.")
        if move is not None:
            return e.Move(self.state.board, move[0], move[1])
        return None

    def ai_vs_random(self):
        # Alternate between AI and random moves, return the move to be made
        if self.state.red_is_machine:
            if self.state.turn_of_red:
                return self.play_with_ai()
            else:
                return self.play_with_random()
        else:
            if self.state.turn_of_red:
                return self.play_with_random()
            else:
                return self.play_with_ai()

    def ai_vs_ai(self):
        if self.state.red_is_machine:
            if self.state.turn_of_red:
                return self.play_with_ai()
            else:
                return self.play_with_ai()
        else:
            if self.state.turn_of_red:
                return self.play_with_ai()
            else:
                return self.play_with_ai()

    def game_mode_manager(self, mode):
        # Manage the game mode based on the type
        turn = (self.state.red_is_machine and self.state.turn_of_red) or (not self.state.red_is_machine and not self.state.turn_of_red)
        game_mode = [
            self.play_with_random,
            self.play_with_ai,
            self.ai_vs_random,
        ]
        if turn:
            play = None
            play = game_mode[mode - 1]()
            if play:
                self.state.make_move(play)
