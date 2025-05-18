import os

import pygame as p

import src.ui.setting as s


class Loading:
    def __init__(self):
        self.piece_directory = os.path.join("..", "..", "asset", "images", "pieces")
        self.buttons_directory = os.path.join("..", "..", "asset", "images", "buttons")
        self.misc_directory = os.path.join("..", "..", "asset", "images", "misc")
        self.piece_color = ["b", "r"]
        self.piece_name = ["ad", "ch", "cn", "ep", "gn", "hs", "sd"]
        self.button_mode = ["normal", "active", "click", "hover"]

    def load_pieces(self):
        """Load chess piece images."""
        piece_list = {}
        for c in self.piece_color:
            for n in self.piece_name:
                img_path = os.path.join(os.path.dirname(__file__), self.piece_directory, f"{c}{n}.png")
                if os.path.exists(img_path):
                    piece_list[f"{c}{n}"] = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
                else:
                    piece_list[f"{c}{n}"] = None
                    print(f"Warning: Missing piece image {img_path}")
        return piece_list

    def load_button(self, type):
        """Load button images for all modes."""
        button_list = []
        for m in self.button_mode:
            img_path = os.path.join(os.path.dirname(__file__), self.buttons_directory, f"{type}_{m}.png")
            if os.path.exists(img_path):
                button_list.append(p.transform.scale(p.image.load(img_path), (s.BUT_WIDTH, s.BUT_HEIGHT)))
            else:
                button_list.append(None)
                print(f"Warning: Missing button image {img_path}")
        return button_list

    def load_misc(self, name):
        """Load miscellaneous images."""
        img_path = os.path.join(os.path.dirname(__file__), self.misc_directory, f"{name}.png")
        if os.path.exists(img_path):
            if name in ["menu", "board"]:
                img = p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
            else:
                img = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
            return img
        else:
            print(f"Warning: Missing misc image {img_path}")
            return None
