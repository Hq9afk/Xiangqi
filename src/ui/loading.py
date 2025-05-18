import pygame as p
import src.ui.setting as s
import os


class Loading:
    def __init__(self):
        self.piece_directory = "../../utils/UI/pieces"
        self.buttons_directory = "../../utils/UI/buttons"
        self.misc_directory = "../../utils/UI/misc"
        self.piece_color = ["b", "r"]
        self.piece_name = ["ad", "ch", "cn", "ep", "gn", "hs", "sd"]
        self.button_mode = ["normal", "active", "click", "hover"]

    # Load chess pieces
    def load_pieces(self):
        piece_list = {}

        for c in self.piece_color:
            for n in self.piece_name:
                img_path = os.path.join(os.path.dirname(__file__), f"{self.piece_directory}/{c}{n}.png")
                piece_list[f"{c}{n}"] = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE)) if os.path.exists(img_path) else None

        return piece_list

    # Load buttons
    def load_button(self, type):
        button_list = []
        for m in self.button_mode:
            img_path = os.path.join(os.path.dirname(__file__), f"{self.buttons_directory}/{type}_{m}.png")
            button_list.append(p.transform.scale(p.image.load(img_path), (s.BUT_WIDTH, s.BUT_HEIGHT)) if os.path.exists(img_path) else None)

        return button_list

    # Load others
    def load_misc(self, name):
        img_path = os.path.join(os.path.dirname(__file__), f"{self.misc_directory}/{name}.png")
        img = (p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))) if (name in ["menu", "board"]) else p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
        return img
