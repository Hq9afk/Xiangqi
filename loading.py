import pygame as p
import setting as s
import os


def loadPiece():  # Load chess pieces.
    chessMan = {}
    chessName = [
        "bsd",
        "bhs",
        "bcn",
        "bch",
        "bep",
        "bad",
        "bgn",
        "rsd",
        "rhs",
        "rcn",
        "rch",
        "rep",
        "rad",
        "rgn",
    ]
    for i in chessName:
        img_path = os.path.join(os.path.dirname(__file__), f"img/pieces/{i}.png")
        chessMan[i] = p.transform.scale(
            p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE)
        )
    return chessMan


def loadBoard():  # Load chessboard
    img_path = os.path.join(os.path.dirname(__file__), "img", "board.jpg")
    board = p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
    return board


def loadValid():  # Load valid move suggestion
    img_path = os.path.join(os.path.dirname(__file__), "img", "valid.png")
    light = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return light


def loadButton(type):
    button0, button1, button2, button3 = None, None, None, None
    if type == "undo":
        button0 = p.transform.scale(
            p.image.load(os.path.join(os.path.dirname(__file__), "img", "undo.png")),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button1 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "undoActive.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button2 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "undoClick.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button3 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "undoHover.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
    elif type == "redo":
        button0 = p.transform.scale(
            p.image.load(os.path.join(os.path.dirname(__file__), "img", "redo.png")),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button1 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "redoActive.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button2 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "redoClick.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button3 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "redoHover.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
    elif type == "swap":
        button0 = p.transform.scale(
            p.image.load(os.path.join(os.path.dirname(__file__), "img", "swap.png")),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button1 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "swapActive.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button2 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "swapClick.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button3 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "swapHover.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
    elif type == "start":
        button0 = p.transform.scale(
            p.image.load(os.path.join(os.path.dirname(__file__), "img", "start.png")),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button1 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "startClick.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button2 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "startHover.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
    elif type == "menu":
        button0 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "menuActive.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button1 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "menuClick.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
        button2 = p.transform.scale(
            p.image.load(
                os.path.join(os.path.dirname(__file__), "img", "menuHover.png")
            ),
            (s.BUT_WIDTH, s.BUT_HEIGHT),
        )
    return [button0, button1, button2, button3]


def loadIndicator():
    img_path = os.path.join(os.path.dirname(__file__), "img", "indicator.png")
    square = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return square


def loadCheckMate():
    img_path = os.path.join(os.path.dirname(__file__), "img", "check.png")
    checkMate = p.transform.scale(
        p.image.load(img_path), (s.CELL_SIZE * 7.3, s.CELL_SIZE * 1.5)
    )
    return checkMate


def loadMainMenu():
    img_path = os.path.join(os.path.dirname(__file__), "img", "mainMenu.png")
    return p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
