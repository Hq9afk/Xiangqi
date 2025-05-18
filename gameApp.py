import pygame as p
import setting as s
import loading as l
import chessEngine
import button as b
import playWithMachine as pWM
import displayUI as dp
import rule
import sys


class Game:
    # Main application class for Xiangqi game

    def __init__(self):
        self.gameStart = False
        self.returnToMain = False
        self.AIVSRandomMode = False
        self.gameMode = -1
        self.screen = None
        self.clock = None
        self.gameState = None
        self.playerActionPositionList = []
        self.gameButtonList = []

    def startGame(self):
        # Callback to start the game.
        self.gameStart = True

    def returnToMenu(self):
        # Callback to return to the main menu.
        self.returnToMain = True

    def setup(self):
        # Initialize or reset the game state and UI.
        p.init()
        self.returnToMain = False
        self.gameStart = False
        self.gameMode = -1
        self.screen = p.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
        p.display.set_caption("Xiangqi")
        self.clock = p.time.Clock()
        self.gameState = chessEngine.State()
        self.playerActionPositionList = []
        self.AIVSRandomMode = False
        self.initButtons()

    def quitGame(self):
        # Quit the game and exit.
        p.quit()
        sys.exit()

    def initButtons(self):
        # Initialize all game control buttons.
        self.gameButtonList = [
            b.Button(s.BACKWARD_X, s.BACKWARD_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "undo", l.loadButton("undo"), self.gameState.undoMove),
            b.Button(s.NEXTSTEP_X, s.NEXTSTEP_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "redo", l.loadButton("redo"), self.gameState.redoMove),
            b.Button(s.REVERSE_X, s.REVERSE_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "swap", l.loadButton("swap"), self.gameState.swap),
            b.Button(s.START_X, s.START_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "start", l.loadButton("start"), self.startGame),
            b.Button(s.REPLAY_X, s.REPLAY_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "return", l.loadButton("return"), self.returnToMenu),
        ]

    def handleMouseInput(self, row, col):
        # Handle mouse input for selecting and moving pieces.
        if not self.playerActionPositionList:
            if (self.gameState.redTurn and self.gameState.board[row][col][0] == "b") or (not self.gameState.redTurn and self.gameState.board[row][col][0] == "r"):
                return

        self.playerActionPositionList.append((row, col))
        max_row = getattr(s, "DIMENSION", 9)
        max_col = getattr(s, "DIMENSION", 8)
        if 0 <= row <= max_row and 0 <= col <= max_col:
            if self.gameState.board[self.playerActionPositionList[0][0]][self.playerActionPositionList[0][1]] == "---":
                self.playerActionPositionList = []
            else:
                self.gameState.selectedCell = self.playerActionPositionList[0]

            if len(self.playerActionPositionList) == 2:
                if self.playerActionPositionList[0] == self.playerActionPositionList[1]:
                    self.playerActionPositionList = []
                else:
                    validMoveList = self.gameState.checkValid(self.gameState.selectedCell)
                    if self.playerActionPositionList[1] in validMoveList:
                        move = chessEngine.Move(self.gameState.board, self.playerActionPositionList[0], self.playerActionPositionList[1])
                        self.gameState.makeMove(move)
                        rule.checkIllegalMove(self.gameState)
                    self.playerActionPositionList = []
                self.gameState.selectedCell = ()

    def run(self):
        # Main game loop
        self.setup()
        max_row = getattr(s, "DIMENSION", 9)
        max_col = getattr(s, "DIMENSION", 8)
        while True:
            for e in p.event.get():
                if e.type == p.QUIT:
                    self.quitGame()

                elif e.type == p.MOUSEBUTTONDOWN:
                    if not self.gameStart or self.AIVSRandomMode:
                        continue
                    y_x_margin_and_boxSize = s.GRID
                    mouseCoord = p.mouse.get_pos()
                    row = int((mouseCoord[1] - y_x_margin_and_boxSize[0]) // y_x_margin_and_boxSize[2])
                    col = int((mouseCoord[0] - y_x_margin_and_boxSize[1]) // y_x_margin_and_boxSize[2])
                    if row > max_row or col > max_col or row < 0 or col < 0:
                        continue
                    self.handleMouseInput(row, col)

            # Main menu and game mode selection
            if self.gameMode == -1:
                self.gameMode = dp.displayMainMenu(self.screen, self.gameState)
            else:
                dp.displayGameState(self.screen, self.gameState, self.gameStart)
                for button in self.gameButtonList:
                    button.process(self.screen, self.gameStart, self.gameState)

            # Game logic for different modes
            if self.gameStart:
                if self.gameMode == 1:
                    pWM.gameModemanager(self.gameState, 1)
                    self.AIVSRandomMode = False
                elif self.gameMode == 2:
                    pWM.gameModemanager(self.gameState, 2)
                    self.AIVSRandomMode = False
                elif self.gameMode == 3:
                    self.AIVSRandomMode = True
                    if not self.gameState.redTurn and not self.gameState.redIsMachine:
                        dp.displayMove(self.screen, self.gameState)
                    move = pWM.AIVSRandom(self.gameState)
                    if move is not None:
                        self.gameState.makeMove(move)
                else:
                    self.AIVSRandomMode = False

            # Return to main menu logic (avoid recursion)
            if self.returnToMain:
                self.returnToMain = False
                self.setup()
                continue

            self.clock.tick(s.MAX_FPS)
            p.display.flip()
