import pygame as p
import src.ui.setting as s
import src.engine.chess_engine as chess_engine
import src.ui.button as b
import src.engine.play_with_machine as pwm
import src.engine.rule as rule
import sys
import time

from src.ui.display_ui import DisplayUI as dp
from src.ui.loading import Loading as l


class Game:
    def __init__(self):
        self.game_start = False
        self.return_to_main = False
        self.ai_vs_random_mode = False
        self.game_mode = -1
        self.screen = None
        self.clock = None
        self.game_state = None
        self.player_action_pos_list = []
        self.button_list = []
        self.display = dp()
        self.load = l()
        self.start_time = None

    def start_game(self):
        self.game_start = True

    def return_to_menu(self):
        self.return_to_main = True

    def setup(self):
        p.init()
        self.return_to_main = False
        self.game_start = False
        self.game_mode = -1
        self.screen = p.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        p.display.set_caption("Xiangqi")
        self.clock = p.time.Clock()
        self.game_state = chess_engine.State()
        self.player_action_pos_list = []
        self.ai_vs_random_mode = False
        self.init_buttons()
        self.display.reset_flag()
        self.match_start_time = None

    def get_match_time(self):
        if self.match_start_time is None:
            return 0
        return int(time.time() - self.match_start_time)

    def quit_game(self):
        p.quit()
        sys.exit()

    def init_buttons(self):
        self.button_list = [
            b.Button(s.BACKWARD_X, s.BACKWARD_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "undo", self.load.load_button("undo"), self.game_state.undo_move),
            b.Button(s.NEXTSTEP_X, s.NEXTSTEP_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "redo", self.load.load_button("redo"), self.game_state.redo_move),
            b.Button(s.REVERSE_X, s.REVERSE_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "swap", self.load.load_button("swap"), self.game_state.swap),
            b.Button(s.START_X, s.START_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "start", self.load.load_button("start"), self.start_game),
            b.Button(s.REPLAY_X, s.REPLAY_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "return", self.load.load_button("return"), self.return_to_menu),
        ]

    def handle_mouse_input(self, row, col):
        if not self.player_action_pos_list:
            if (self.game_state.turn_of_red and self.game_state.board[row][col][0] == "b") or (not self.game_state.turn_of_red and self.game_state.board[row][col][0] == "r"):
                return

        self.player_action_pos_list.append((row, col))
        max_row = getattr(s, "DIMENSION", 9)
        max_col = getattr(s, "DIMENSION", 8)
        if 0 <= row <= max_row and 0 <= col <= max_col:
            if self.game_state.board[self.player_action_pos_list[0][0]][self.player_action_pos_list[0][1]] == "---":
                self.player_action_pos_list = []
            else:
                self.game_state.selected_cell = self.player_action_pos_list[0]

            if len(self.player_action_pos_list) == 2:
                if self.player_action_pos_list[0] == self.player_action_pos_list[1]:
                    self.player_action_pos_list = []
                else:
                    valid_move_list = self.game_state.check_valid(self.game_state.selected_cell)
                    if self.player_action_pos_list[1] in valid_move_list:
                        move = chess_engine.Move(self.game_state.board, self.player_action_pos_list[0], self.player_action_pos_list[1])
                        self.game_state.make_move(move)
                        rule.check_illegal_move(self.game_state)
                    self.player_action_pos_list = []
                self.game_state.selected_cell = ()

    def run(self):
        self.setup()
        max_row = getattr(s, "DIMENSION", 9)
        max_col = getattr(s, "DIMENSION", 8)
        while True:
            for e in p.event.get():
                if e.type == p.QUIT:
                    self.quit_game()

                elif e.type == p.MOUSEBUTTONDOWN:
                    if not self.game_start or self.ai_vs_random_mode:
                        continue
                    y_x_margin_and_box_size = s.GRID
                    mouse_coord = p.mouse.get_pos()
                    row = int((mouse_coord[1] - y_x_margin_and_box_size[0]) // y_x_margin_and_box_size[2])
                    col = int((mouse_coord[0] - y_x_margin_and_box_size[1]) // y_x_margin_and_box_size[2])
                    if row > max_row or col > max_col or row < 0 or col < 0:
                        continue
                    self.handle_mouse_input(row, col)

            if self.game_mode == -1:
                self.game_mode = self.display.display_main_menu(self.screen, self.game_state)
            else:
                self.display.display_game_state(self.screen, self.game_state, self.game_start)
                for button in self.button_list:
                    button.process(self.screen, self.game_start, self.game_state)

            if self.game_start:
                if self.game_mode == 1:
                    pwm.game_mode_manager(self.game_state, 1)
                    self.ai_vs_random_mode = False
                elif self.game_mode == 2:
                    pwm.game_mode_manager(self.game_state, 2)
                    self.ai_vs_random_mode = False
                elif self.game_mode == 3:
                    self.ai_vs_random_mode = True
                    if not self.game_state.turn_of_red and not self.game_state.red_is_machine:
                        self.display.display_move(self.screen, self.game_state)
                    move = pwm.ai_vs_random(self.game_state)
                    if move is not None:
                        self.game_state.make_move(move)
                else:
                    self.ai_vs_random_mode = False

            if self.return_to_main:
                self.return_to_main = False
                self.setup()
                continue

            self.clock.tick(s.MAX_FPS)
            p.display.flip()
