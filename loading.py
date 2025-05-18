import pygame as p
import setting as s
import os

piecesDir = "utils/UI/pieces"
buttonsDir = "utils/UI/buttons"
miscDir = "utils/UI/misc"


# Load chess pieces
def loadPiece():
    piecesList = {}
    pieces = ["bsd", "bhs", "bcn", "bch", "bep", "bad", "bgn", "rsd", "rhs", "rcn", "rch", "rep", "rad", "rgn"]

    for i in pieces:
        img_path = os.path.join(os.path.dirname(__file__), f"{piecesDir}/{i}.png")
        piecesList[i] = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE)) if os.path.exists(img_path) else None

    return piecesList


# Load button images for different button types
def loadButton(type):
    buttonList = []
    buttonMode = ["Normal", "Active", "Click", "Hover"]

    for mode in buttonMode:
        img_path = os.path.join(os.path.dirname(__file__), f"{buttonsDir}/{type}{mode}.png")
        buttonList.append(p.transform.scale(p.image.load(img_path), (s.BUT_WIDTH, s.BUT_HEIGHT)) if os.path.exists(img_path) else None)

    return buttonList


def loadMisc(type):
    miscList = []
    misc = ["mainMenu", "board", "valid", "indicator"]

    for i in misc:
        img_path = os.path.join(os.path.dirname(__file__), f"{miscDir}/{i}.png")
        miscList.append(p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE)) if os.path.exists(img_path) else None)

    return miscList


# Load main menu background
def loadMainMenu():
    img_path = os.path.join(os.path.dirname(__file__), f"{miscDir}/mainMenu.png")
    return p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))


# Load the board
def loadBoard():
    img_path = os.path.join(os.path.dirname(__file__), f"{miscDir}/board.jpg")
    board = p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
    return board


# Load possible moves for the selected piece
def loadValid():
    img_path = os.path.join(os.path.dirname(__file__), f"{miscDir}/valid.png")
    light = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return light


# Load indicator image
def loadIndicator():
    img_path = os.path.join(os.path.dirname(__file__), f"{miscDir}/indicator.png")
    square = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return square
