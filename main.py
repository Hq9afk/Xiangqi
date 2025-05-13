import pygame as p
import setting as s
import loading as l
import chessEngine
import button as b
import playWithMachine as pWM
import drawUI as draw


gameStart = False      # START GAME OR NOT
returnToMain = False      # PLAY AGAIN OR NOT
AI_VS_RANDOM_Mode = False    # ROBOT OR NOT USE TO AI PLAY WITH RAMDOM
gameMode = -1          # CHOOSE MODE

'''
    FUNCTION: startGame
    use to start create the board
'''
def startGame():
    global gameStart
    gameStart= True

'''
    FUNCTION: playAgainGame
    use to play again
'''
def replayGame():
    global returnToMain
    returnToMain = True
    
'''
    FUNCTION: setup
    use to setup the game before play
'''
def setup():
    global returnToMain
    global gameStart
    global gameMode
    p.init()
    returnToMain = False
    gameStart = False

'''
    FUNCTION: quitGame
    use to quit the game
'''
def quitGame():
    p.quit()

'''
    FUNCTION: gameScreenManager
    use to run the game    
'''
def gameScreenManager():
    p.display.set_caption('Chinese Chess')
    screen = p.display.set_mode((s.SCREEN_WIDTH,s.SCREEN_HEIGHT))
    
    gameState = chessEngine.State()
    clock = p.time.Clock()
    run = True
    playerActionPositionList=[]

    # this is the list of button    
    gameButtonList=()
    undoButton = b.Button(s.BACKWARD_X, s.BACKWARD_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'re', l.loadButton('backward'), gameState.undoMove)
    redoButton = b.Button(s.NEXTSTEP_X, s.NEXTSTEP_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'ne', l.loadButton('nextstep'), gameState.redoMove)
    changeChessSideButton = b.specialButton(s.REVERSE_X, s.REVERSE_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'ex', l.loadButton('reverse'), gameState.reverse)
    startButton = b.Button(s.START_X, s.START_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'st', l.loadButton('start'), startGame)
    returnToMenuButton = b.specialButton(s.REPLAY_X, s.REPLAY_Y, s.BUT_WIDTH, s.BUT_HEIGHT,'pa', l.loadButton('replay'), replayGame)

    gameButtonList += (undoButton, redoButton, changeChessSideButton, startButton, returnToMenuButton)

    # create the mode = -1 mean not choose mode
    global gameMode
    gameMode = -1
    while run:
        global gameStart
        global returnToMain
        global AI_VS_RANDOM_Mode

        for e in p.event.get():
            if gameMode != -1:  
                draw.drawGameState(screen,gameState,gameStart)

                for btn in gameButtonList:
                    btn.process(screen,gameState)

            if gameMode == -1:
                gameMode = draw.drawGameMenuScreen(screen, gameState)
            if gameStart:
                draw.drawGameState(screen,gameState,gameStart)
                clock.tick(s.MAX_FPS)
                p.display.flip()
                    
                if gameMode == 1:
                        pWM.gameModemanager(gameState, 1)            # play with random
                elif gameMode == 2:
                        pWM.gameModemanager(gameState, 2)            # play with chaca
                elif gameMode == 3:
                    AI_VS_RANDOM_Mode = True
                    if not gameState.redTurn and not gameState.redIsMachine:
                        draw.drawLastMove(screen,gameState)
                    move = pWM.AI_VS_RANDOM_Mode(gameState)              # watch them play
                    if move != None:
                        gameState.makeMove(move)
            if e.type == p.QUIT:
                run = False
            
            elif e.type == p.MOUSEBUTTONDOWN:
                
                if gameStart == False or AI_VS_RANDOM_Mode: continue  # if game not start yet or in AI vs Random mode, click event not use
                
                y_x_margin_and_boxSize = s.GRID                              
                mouseCoord = p.mouse.get_pos()                   # get the position of mouse
                row = int((mouseCoord[1] - y_x_margin_and_boxSize[0]) // y_x_margin_and_boxSize[2])
                col = int((mouseCoord[0] - y_x_margin_and_boxSize[1]) // y_x_margin_and_boxSize[2])

                if row > 9 or col > 8 or row < 0 or col < 0:
                    break
                if playerActionPositionList ==[]:
                    if (gameState.redTurn and gameState.board[row][col][0] == 'b') or (not gameState.redTurn and gameState.board[row][col][0] == 'r'): break
                
                playerActionPositionList.append((row,col))
                if 0 <= row <= 9 and 0 <= col <= 8:
                    if gameState.board[playerActionPositionList[0][0]][playerActionPositionList[0][1]]=='---':
                        playerActionPositionList =[]
                    else:
                        gameState.selectedCell = playerActionPositionList[0]
                        
                    if len(playerActionPositionList) ==2:
                        if playerActionPositionList[0] == playerActionPositionList[1]:
                            playerActionPositionList =[]
                        else:
                            validMoveList = gameState.checkValid(gameState.selectedCell)
                            if playerActionPositionList[1] in validMoveList:
                                move = chessEngine.Move(gameState.board, playerActionPositionList[0], playerActionPositionList[1])
                                gameState.makeMove(move)
                                draw.drawGameState(screen,gameState,gameStart)
                                clock.tick(s.MAX_FPS)
                                p.display.flip()
                            playerActionPositionList =[]
                        gameState.selectedCell = ()
        # if click play again
        if returnToMain:
            returnToMain = False
            main()    

        clock.tick(s.MAX_FPS)
        p.display.flip()
        
def main():
    setup()
    gameScreenManager()
    quitGame()
        
if __name__ == '__main__':
    main()