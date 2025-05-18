import pygame as p
import setting as s
import os


class Loading:
    def __init__(self):
        self.pieceDir = "utils/UI/pieces"
        self.buttonsDir = "utils/UI/buttons"
        self.miscDir = "utils/UI/misc"
        self.pieceColor = ["b", "r"]
        self.pieceName = ["ad", "ch", "cn", "ep", "gn", "hs", "sd"]
        self.buttonMode = ["Normal", "Active", "Click", "Hover"]

    # Load chess pieces
    def loadPieces(self):
        pieceList = {}

        for c in self.pieceColor:
            for n in self.pieceName:
                img_path = os.path.join(os.path.dirname(__file__), f"{self.pieceDir}/{c}{n}.png")
                pieceList[f"{c}{n}"] = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE)) if os.path.exists(img_path) else None

        return pieceList

    # Load buttons
    def loadButton(self, type):
        buttonList = []
        for m in self.buttonMode:
            img_path = os.path.join(os.path.dirname(__file__), f"{self.buttonsDir}/{type}{m}.png")
            buttonList.append(p.transform.scale(p.image.load(img_path), (s.BUT_WIDTH, s.BUT_HEIGHT)) if os.path.exists(img_path) else None)

        return buttonList

    # Load others
    def loadMisc(self, name):
        img_path = os.path.join(os.path.dirname(__file__), f"{self.miscDir}/{name}.png")
        img = (p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))) if (name in ["mainMenu", "board"]) else p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
        return img
