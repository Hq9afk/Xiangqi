import os
import time

import pygame as p

import src.engine.chess_engine as chess_engine
import src.ui.setting as s
from src.ui.loading import Loading as l


class DisplayUI:
    def __init__(self):
        self.load = l()
        self.piece_img = self.load.load_pieces()
        self.board_img = self.load.load_misc("board")
        self.valid_img = self.load.load_misc("valid")
        self.indicator_img = self.load.load_misc("indicator")
        self.font_path = os.path.join(os.path.dirname(__file__), "../../asset/Font/impact.ttf")
        self.check_start_time = None
        self.checkmate_printed = False

    def reset_flag(self):
        # Reset checkmate printed flag
        self.checkmate_printed = False

    def display_valid(self, screen, gs):
        # Display valid moves for the selected piece
        list_valid = gs.check_valid(gs.selected_cell)
        start = s.GRID
        for i in list_valid:
            screen.blit(self.valid_img, p.Rect(start[1] + i[1] * start[2], start[0] + i[0] * start[2], s.CELL_SIZE, s.CELL_SIZE))

    def display_game_state(self, screen, game_state: chess_engine.State, st):
        # Display the current game state, including board, pieces, and banners
        screen.blit(self.board_img, (0, 0))

        # Checkmate
        if game_state.check_mate()[0]:
            self.display_result(screen, game_state)

        # Check banner logic
        elif game_state.check():
            current_time = p.time.get_ticks()
            if self.check_start_time is None:
                self.check_start_time = current_time
            if current_time - self.check_start_time < 2000:
                self.display_check(screen, game_state)
            else:
                self.check_start_time = None
        else:
            self.check_start_time = None

        # AI processing banner
        if (game_state.red_is_machine and game_state.turn_of_red) or (not game_state.red_is_machine and not game_state.turn_of_red):
            if st:
                self.display_processing(screen)

        self.display_pieces(screen, game_state.board)

        if game_state.selected_cell != ():
            self.display_valid(screen, game_state)
            screen.blit(self.indicator_img, p.Rect(s.GRID[1] + game_state.selected_cell[1] * s.GRID[2], s.GRID[0] + game_state.selected_cell[0] * s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))

        self.display_move(screen, game_state)

    def display_pieces(self, screen, board):
        # Display all pieces on the board
        y_x_margin_and_box_size = s.GRID
        for i in range(s.DIMENSION + 1):
            for j in range(s.DIMENSION):
                chess_man = board[i][j]
                if chess_man != "---":
                    screen.blit(self.piece_img[chess_man], p.Rect(y_x_margin_and_box_size[1] + j * y_x_margin_and_box_size[2], y_x_margin_and_box_size[0] + i * y_x_margin_and_box_size[2], s.CELL_SIZE, s.CELL_SIZE))

    def display_move(self, screen, game_state: chess_engine.State):
        # Highlight the last move
        if game_state.move_log == []:
            return
        start_row = game_state.move_log[-1].start_row
        start_col = game_state.move_log[-1].start_col
        end_row = game_state.move_log[-1].end_row
        end_col = game_state.move_log[-1].end_col
        screen.blit(self.indicator_img, p.Rect(s.GRID[1] + start_col * s.GRID[2], s.GRID[0] + start_row * s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))
        screen.blit(self.indicator_img, p.Rect(s.GRID[1] + end_col * s.GRID[2], s.GRID[0] + end_row * s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))

    def display_check(self, screen, game_state):
        # Display 'CHECK' banner
        my_font = p.font.SysFont("Comic Sans MS", 30)
        text_surface = my_font.render("CHECK", False, (0, 0, 0))
        screen.blit(text_surface, (s.WIDTH / 2 - text_surface.get_width() / 2, s.START_Y + 5))

    def display_result(self, screen, game_state: chess_engine.State):
        # Display checkmate result
        winner = "RED" if game_state.check_mate()[1] == "r" else "BLACK"
        if not self.checkmate_printed:
            print(f"CHECKMATE, {winner} WINS")
            self.checkmate_printed = True
        p.font.init()
        my_font = p.font.SysFont("Comic Sans MS", 30)
        text_surface = my_font.render(f"CHECKMATE, {winner} WINS", False, (0, 0, 0))
        screen.blit(text_surface, (s.WIDTH / 2 - text_surface.get_width() / 2, s.START_Y + 5))

    def display_processing(self, screen):
        # Display 'Processing' banner for AI moves
        p.font.init()
        my_font = p.font.SysFont("Comic Sans MS", 30)
        text_surface = my_font.render("Processing", False, (167, 133, 96))
        screen.blit(text_surface, (s.WIDTH / 2 - text_surface.get_width() / 2, s.START_Y + 5))

    def display_title(self, screen, x, y, width, height, text):
        # Display a title on the screen
        p.font.init()
        t_font = p.font.SysFont("Comic Sans MS", 30)
        title = t_font.render(text, True, (55, 255, 255))
        rect = title.get_rect()
        rect.center = ((x + width / 2), (y + height / 2))
        screen.blit(title, rect)
        return title

    def display_button(self, screen, x, y, width, height, text):
        # Display a button with text
        button_surface = p.Surface((width, height), p.SRCALPHA)
        p.font.init()
        t_font = p.font.Font(self.font_path, 30)
        content = t_font.render(text, True, (230, 200, 100))
        rect = content.get_rect()
        rect.center = (width // 2, height // 2)
        button_surface.blit(content, rect)
        screen.blit(button_surface, (x, y))
        return p.Rect(x, y, width, height)

    def display_main_menu(self, screen, game_state):
        # Display the main menu and handle button clicks
        background = self.load.load_misc("menu")
        screen.blit(background, (0, 0))

        random_button = self.display_button(screen, s.BUTTEXT_X, s.BUTTEXT_Y, s.BUT_TEXT, s.BUT_TEXT / 6, "Play with Random")
        ai_button = self.display_button(screen, s.BUTTEXT_X, s.BUTTEXT_Y + 110, s.BUT_TEXT, s.BUT_TEXT / 6, "Play with AI")
        random_vs_ai_button = self.display_button(screen, s.BUTTEXT_X, s.BUTTEXT_Y + 220, s.BUT_TEXT, s.BUT_TEXT / 6, "Random vs AI")
        ai_vs_ai_button = self.display_button(screen, s.BUTTEXT_X, s.BUTTEXT_Y + 220, s.BUT_TEXT, s.BUT_TEXT / 6, "AI vs AI")

        click = p.mouse.get_pressed()[0]
        if click == 1:
            mouse = p.mouse.get_pos()
            if random_button.collidepoint(mouse):
                time.sleep(0.2)
                return 1
            elif ai_button.collidepoint(mouse):
                time.sleep(0.2)
                return 2
            elif random_vs_ai_button.collidepoint(mouse):
                time.sleep(0.2)
                return 3
        return -1
