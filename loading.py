import pygame as p
import setting as s
import os


# Load chess pieces
def loadPiece():
    chessMan = {}
    chessName = ["bsd", "bhs", "bcn", "bch", "bep", "bad", "bgn", "rsd", "rhs", "rcn", "rch", "rep", "rad", "rgn"]
    for i in chessName:
        img_path = os.path.join(os.path.dirname(__file__), f"img/pieces/{i}.png")
        chessMan[i] = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return chessMan


# Load button images for different button types
def loadButton(type):
    buttonMode = ["Normal", "Active", "Click", "Hover"]
    buttonList = []

    for mode in buttonMode:
        img_path = os.path.join(os.path.dirname(__file__), f"img/buttons/{type}{mode}.png")
        buttonList.append(p.transform.scale(p.image.load(img_path), (s.BUT_WIDTH, s.BUT_HEIGHT)) if os.path.exists(img_path) else None)

    return buttonList


# Load main menu background
def loadMainMenu():
    img_path = os.path.join(os.path.dirname(__file__), "img/mainMenu.png")
    return p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))


# Load the board
def loadBoard():
    img_path = os.path.join(os.path.dirname(__file__), "img/board.jpg")
    board = p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
    return board


# Load possible moves for the selected piece
def loadValid():
    img_path = os.path.join(os.path.dirname(__file__), "img/valid.png")
    light = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return light


# Load indicator image
def loadIndicator():
    img_path = os.path.join(os.path.dirname(__file__), "img/indicator.png")
    square = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return square
