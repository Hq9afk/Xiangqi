import pygame as p
import setting as s
import loading as l
import chessEngine
import button as b
import playWithMachine as pWM
import time

chessManImg = l.loadChessPiece()
boardImg = l.loadBoard()
lightImg = l.loadLight()
squareImg = l.loadSquare()


'''
This function draw the valid move of the selected chessman
'''
def drawValid(screen,gs):
    listValid = gs.checkValid(gs.selectedCell)
    start = s.GRID
    for i in listValid:
        screen.blit(lightImg, p.Rect(start[1]+ i[1]*start[2],start[0]+i[0]*start[2], s.CELL_SIZE, s.CELL_SIZE))

check = True

'''
This function draw all the game state
'''
def drawGameState(screen, gameState: chessEngine.State, st):
    screen.blit(boardImg,(0,0))
    global check
    if gameState.checkEnd()[0]:
        drawEndGame(screen,gameState)
        
    elif gameState.checkMate() and check:
        startTime = p.time.get_ticks()
        drawCheckMate(screen,gameState)
        if p.time.get_ticks() - startTime >= 2000:
            check = False
        
    elif (gameState.redIsMachine and gameState.redTurn) or (not gameState.redIsMachine and not gameState.redTurn):
        drawAIThink(screen) if st else None
    drawChessPiece(screen, gameState.board)
    
    if gameState.selectedCell != ():
        drawValid(screen, gameState)
        screen.blit(squareImg, p.Rect(s.GRID[1]+ gameState.selectedCell[1]*s.GRID[2],s.GRID[0]+gameState.selectedCell[0]*s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))
    drawLastMove(screen, gameState)
    
    
'''
This function draw the chessman on the board
'''
def drawChessPiece(screen,board):
    y_x_margin_and_boxSize = s.GRID
    for i in range(s.DIMENSION+1):
        for j in range(s.DIMENSION):
            chessMan = board[i][j]
            if chessMan != '---':  
                screen.blit(chessManImg[chessMan],p.Rect(y_x_margin_and_boxSize[1] + j*y_x_margin_and_boxSize[2], 
                                                         y_x_margin_and_boxSize[0] + i*y_x_margin_and_boxSize[2],
                                                         s.CELL_SIZE, s.CELL_SIZE))


'''
This function draw the last move 
'''
def drawLastMove(screen, gameState: chessEngine.State):
    if gameState.moveLog == []:
        return
    startRow = gameState.moveLog[-1].startRow
    startCol = gameState.moveLog[-1].startCol
    endRow = gameState.moveLog[-1].endRow
    endCol = gameState.moveLog[-1].endCol
    screen.blit(squareImg, p.Rect(s.GRID[1]+ startCol*s.GRID[2],s.GRID[0]+startRow*s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))
    screen.blit(squareImg, p.Rect(s.GRID[1]+ endCol*s.GRID[2],s.GRID[0]+endRow*s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))
    
'''
This function is draw when the King is checked
'''
def drawCheckMate(screen, gameState: chessEngine.State):
    checkMateImg = l.loadCheckMate()
    screen.blit(checkMateImg,(s.WIDTH/2 - checkMateImg.get_width()/2, s.SCREEN_HEIGHT/2 - checkMateImg.get_height()/2))


'''
This function draw the end game
'''
def drawEndGame(screen, gameState: chessEngine.State):
    print("End game")
    if gameState.checkEnd()[0]:
        winner= 'RED' if gameState.checkEnd()[1] =='r' else 'BLACK'
        p.font.init()
        print(winner," WIN")
        myFont = p.font.SysFont('Comic Sans MS', 30)
        textSurface = myFont.render(winner + " WIN", False, (0, 0, 0))
        screen.blit(textSurface,(s.WIDTH/2 - textSurface.get_width()/2, s.SCREEN_HEIGHT/2 - textSurface.get_height()/2))
        
'''
This is the function draw the UI when AI is thinking
'''
def drawAIThink(screen):
    p.font.init()
    myFont = p.font.SysFont('Comic Sans MS', 30)
    textSurface = myFont.render("ChaCa is thinking...", False, (0, 0, 0))
    screen.blit(textSurface,(s.WIDTH/2 - textSurface.get_width()/2, s.SCREEN_HEIGHT/2 - textSurface.get_height()/2))


def drawTitle(screen, x, y, width, height, text):
    p.font.init()
    tFont = p.font.SysFont('Comic Sans MS', 30)
    
    Title = tFont.render(text, True, (55, 255, 255))
    Rect = Title.get_rect()
    Rect.center = ((x + width/2), (y + height/2))
    screen.blit(Title, Rect)
    return Title


'''
This is the function draw the initial button
'''
def drawButton(screen, x, y, width, height, text):
    button_surface = p.Surface((width, height), p.SRCALPHA)
    
    p.font.init()
    font_path = "impact.ttf"  
    tFont = p.font.Font(font_path, 30) 
    content = tFont.render(text, True, (230, 200, 100))  # Màu chữ trắng
    Rect = content.get_rect()
    Rect.center = Button.center
    p.draw.rect(screen, (255, 255, 255), Button)
    screen.blit(content, Rect)
    return Button


'''
This is the function draw the start screen
'''
def drawGameMenuScreen(screen, gs):
    drawTitle(screen, s.TITLE_WIDTH_X, s.TITLE_HEIGHT_Y, 0, 0, "Chinese Chess")
    randomModeButton = drawButton(screen, s.BUTTEXT_X , s.BUTTEXT_Y, s.BUT_TEXT, s.BUT_TEXT/6, "Play with Random")
    ChaCaModeButton = drawButton(screen, s.BUTTEXT_X,  s.BUTTEXT_Y + s.BUT_TEXT/3, s.BUT_TEXT, s.BUT_TEXT/6, "Play with ChaCa")
    
    ChaCaProModeButton = drawButton(screen, s.BUTTEXT_X , s.BUTTEXT_Y + 2*s.BUT_TEXT/3, s.BUT_TEXT, s.BUT_TEXT/6, "Play with ChaCaPro")
    AI_VS_RANDOM_ModeButton = drawButton(screen, s.BUTTEXT_X , s.BUTTEXT_Y + s.BUT_TEXT, s.BUT_TEXT, s.BUT_TEXT/6, "Watch them play")
    
    isMouseClicked = p.mouse.get_pressed()[0]
    if isMouseClicked:
        clickPosition = p.mouse.get_pos()
        if randomModeButton.collidepoint(clickPosition):
            time.sleep(0.2)
            return 1
        elif ChaCaProModeButton.collidepoint(clickPosition):
            time.sleep(0.2)
            return 2
        elif AI_VS_RANDOM_ModeButton.collidepoint(clickPosition):
            time.sleep(0.2)
            return 3
    return -1
