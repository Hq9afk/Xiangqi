import pygame as p
import setting as s
import loading as l
import chessEngine
import button as b
import playWithMachine as pWM
import displayUI as dp
import rule as r


gameStart = False  # Start game
returnToMain = False  # Return to main menu
AIVSRandomMode = False  # Check if Option "AI vs Random" is chosen
gameMode = -1  # Choose mode


def startGame():
    global gameStart
    gameStart = True


def returnToMenu():
    global returnToMain
    returnToMain = True


def setup():
    global returnToMain
    global gameStart
    global gameMode
    p.init()
    returnToMain = False
    gameStart = False


def quitGame():
    p.quit()


def gameScreenManager():
    p.display.set_caption("Xiangqi")
    screen = p.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))

    gameState = chessEngine.State()
    clock = p.time.Clock()
    run = True
    playerActionPositionList = []

    gameButtonList = ()
    undoButton = b.Button(s.BACKWARD_X, s.BACKWARD_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "undo", l.loadButton("undo"), gameState.undoMove)
    redoButton = b.Button(s.NEXTSTEP_X, s.NEXTSTEP_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "redo", l.loadButton("redo"), gameState.redoMove)
    swapButton = b.Button(s.REVERSE_X, s.REVERSE_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "swap", l.loadButton("swap"), gameState.swap)
    startButton = b.Button(s.START_X, s.START_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "start", l.loadButton("start"), startGame)
    returnButton = b.Button(s.REPLAY_X, s.REPLAY_Y, s.BUT_WIDTH, s.BUT_HEIGHT, "return", l.loadButton("return"), returnToMenu)

    gameButtonList += (undoButton, redoButton, swapButton, startButton, returnButton)

    # gameMode = -1 means no modes are chosen yet, we are at the main menu
    global gameMode
    gameMode = -1
    while run:
        global gameStart
        global returnToMain
        global AIVSRandomMode

        for e in p.event.get():
            if not run:
                break

            if gameMode != -1:
                dp.displayGameState(screen, gameState, gameStart)

                for button in gameButtonList:
                    button.process(screen, gameState)

            if gameMode == -1:
                gameMode = dp.displayMainMenu(screen, gameState)

            if gameStart:
                dp.displayGameState(screen, gameState, gameStart)

                for button in gameButtonList:
                    button.process(screen, gameState)

                clock.tick(s.MAX_FPS)
                p.display.flip()

                if gameMode == 1:
                    pWM.gameModemanager(gameState, 1)
                elif gameMode == 2:
                    pWM.gameModemanager(gameState, 2)
                elif gameMode == 3:
                    AIVSRandomMode = True
                    if not gameState.redTurn and not gameState.redIsMachine:
                        dp.displayMove(screen, gameState)
                    move = pWM.AIVSRandom(gameState)
                    if move is not None:
                        gameState.makeMove(move)
            if e.type == p.QUIT:
                run = False
                break

            elif e.type == p.MOUSEBUTTONDOWN:
                # Hide the buttons in "AI vs Random" mode
                if not gameStart:
                    continue

                y_x_margin_and_boxSize = s.GRID
                mouseCoord = p.mouse.get_pos()
                row = int((mouseCoord[1] - y_x_margin_and_boxSize[0]) // y_x_margin_and_boxSize[2])
                col = int((mouseCoord[0] - y_x_margin_and_boxSize[1]) // y_x_margin_and_boxSize[2])

                if row > 9 or col > 8 or row < 0 or col < 0:
                    break
                if playerActionPositionList == []:
                    if (gameState.redTurn and gameState.board[row][col][0] == "b") or (not gameState.redTurn and gameState.board[row][col][0] == "r"):
                        break

                playerActionPositionList.append((row, col))
                if 0 <= row <= 9 and 0 <= col <= 8:
                    if gameState.board[playerActionPositionList[0][0]][playerActionPositionList[0][1]] == "---":
                        playerActionPositionList = []
                    else:
                        gameState.selectedCell = playerActionPositionList[0]

                    if len(playerActionPositionList) == 2:
                        if playerActionPositionList[0] == playerActionPositionList[1]:
                            playerActionPositionList = []
                        else:
                            validMoveList = gameState.checkValid(gameState.selectedCell)
                            if playerActionPositionList[1] in validMoveList:
                                move = chessEngine.Move(gameState.board, playerActionPositionList[0], playerActionPositionList[1])
                                gameState.makeMove(move)
                                r.checkIllegalMove(gameState)
                                dp.displayGameState(screen, gameState, gameStart)
                                clock.tick(s.MAX_FPS)
                                p.display.flip()
                            playerActionPositionList = []
                        gameState.selectedCell = ()
        # Returns to the main menu
        if returnToMain:
            returnToMain = False
            main()

        clock.tick(s.MAX_FPS)
        p.display.flip()


# Driver code
def main():
    setup()
    gameScreenManager()
    quitGame()


if __name__ == "__main__":
    main()
