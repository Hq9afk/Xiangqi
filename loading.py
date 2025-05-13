import pygame as p # xử lý hình ảnh.
import setting as s
import os

def loadChessPiece(): # Tải hình ảnh các quân cờ.
    chessMan = {}
    chessName = ['bch', 'bma', 'bph', 'bxe', 'bvo', 'bsi', 'btu', 'rch', 'rma', 'rph', 'rxe', 'rvo', 'rsi', 'rtu']
    for i in chessName:
        img_path = os.path.join(os.path.dirname(__file__), 'img', i + '.png')
        chessMan[i] = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return chessMan

def loadBoard(): #Tải hình ảnh bàn cờ.
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'board.jpg')
    board = p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
    return board

def loadLight(): #Tải hình ảnh nước đi hợp lệ.
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'light.png')
    light = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return light

def loadButton(type):
    button0, button1, button2, button3 = None, None, None, None
    if type == 'backward':
        button0 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'backward.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button1 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'backwardActive.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button2 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'backwardClick.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button3 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'backwardHover.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
    elif type == 'nextstep':
        button0 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'nextstep.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button1 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'nextstepActive.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button2 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'nextstepClick.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button3 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'nextstepHover.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
    elif type == 'reverse':
        button0 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'exchange.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button1 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'exchangeActive.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button2 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'exchangeClick.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button3 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'exchangeHover.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
    elif type == 'start':
        button0 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'start.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button1 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'startClick.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button2 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'startHover.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
    elif type == 'replay':
        button0 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'replay.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button1 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'replayClick.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
        button2 = p.transform.scale(p.image.load(os.path.join(os.path.dirname(__file__), 'img', 'replayHover.png')), (s.BUT_WIDTH, s.BUT_HEIGHT))
    return [button0, button1, button2, button3]

def loadSquare():
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'squareOrigin.png')
    square = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE, s.CELL_SIZE))
    return square

def loadCheckMate():
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'check.png')
    checkMate = p.transform.scale(p.image.load(img_path), (s.CELL_SIZE * 7.3, s.CELL_SIZE * 1.5))
    return checkMate

def loadMenuBackground():
    img_path = os.path.join(os.path.dirname(__file__), 'img', 'menu_background.png')
    return p.transform.scale(p.image.load(img_path), (s.SCREEN_WIDTH, s.SCREEN_HEIGHT))