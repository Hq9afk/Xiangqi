import pygame as p
import setting as s
import loading as l
import chessEngine
import time

pieceImg = l.loadPiece()
boardImg = l.loadBoard()
validImg = l.loadValid()
indicatorImg = l.loadIndicator()


# Display valid move suggestions
def displayValid(screen, gs):
    listValid = gs.checkValid(gs.selectedCell)
    start = s.GRID
    for i in listValid:
        screen.blit(validImg, p.Rect(start[1] + i[1] * start[2], start[0] + i[0] * start[2], s.CELL_SIZE, s.CELL_SIZE))


check = True


# Display game state
def displayGameState(screen, gameState: chessEngine.State, st):
    screen.blit(boardImg, (0, 0))
    global check
    if gameState.checkMate()[0]:
        displayResult(screen, gameState)

    elif gameState.check() and check:
        startTime = p.time.get_ticks()
        displayCheck(screen, gameState)
        if p.time.get_ticks() - startTime >= 2000:
            check = False

    elif (gameState.redIsMachine and gameState.redTurn) or (not gameState.redIsMachine and not gameState.redTurn):
        displayProcessing(screen) if st else None
    displayPieces(screen, gameState.board)

    if gameState.selectedCell != ():
        displayValid(screen, gameState)
        screen.blit(indicatorImg, p.Rect(s.GRID[1] + gameState.selectedCell[1] * s.GRID[2], s.GRID[0] + gameState.selectedCell[0] * s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))
    displayMove(screen, gameState)


# Display the pieces
def displayPieces(screen, board):
    y_x_margin_and_boxSize = s.GRID
    for i in range(s.DIMENSION + 1):
        for j in range(s.DIMENSION):
            chessMan = board[i][j]
            if chessMan != "---":
                screen.blit(pieceImg[chessMan], p.Rect(y_x_margin_and_boxSize[1] + j * y_x_margin_and_boxSize[2], y_x_margin_and_boxSize[0] + i * y_x_margin_and_boxSize[2], s.CELL_SIZE, s.CELL_SIZE))


# Display the most recent move
def displayMove(screen, gameState: chessEngine.State):
    if gameState.moveLog == []:
        return
    startRow = gameState.moveLog[-1].startRow
    startCol = gameState.moveLog[-1].startCol
    endRow = gameState.moveLog[-1].endRow
    endCol = gameState.moveLog[-1].endCol
    screen.blit(indicatorImg, p.Rect(s.GRID[1] + startCol * s.GRID[2], s.GRID[0] + startRow * s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))
    screen.blit(indicatorImg, p.Rect(s.GRID[1] + endCol * s.GRID[2], s.GRID[0] + endRow * s.GRID[2], s.CELL_SIZE, s.CELL_SIZE))


# Display a banner when the player General gets checked
def displayCheck(screen, gameState: chessEngine.State):
    myFont = p.font.SysFont("Comic Sans MS", 30)
    textSurface = myFont.render("CHECK", False, (0, 0, 0))
    screen.blit(textSurface, (s.WIDTH / 2 - textSurface.get_width() / 2, s.START_Y + 5))


# Display the game result
def displayResult(screen, gameState: chessEngine.State):
    if gameState.checkMate()[0]:
        winner = "RED" if gameState.checkMate()[1] == "r" else "BLACK"
        print(f"CHECKMATE, {winner} WINS")
        p.font.init()
        myFont = p.font.SysFont("Comic Sans MS", 30)
        textSurface = myFont.render(f"CHECKMATE, {winner} WINS", False, (0, 0, 0))
        screen.blit(textSurface, (s.WIDTH / 2 - textSurface.get_width() / 2, s.START_Y + 5))


# Display a banner when the AI is processing
def displayProcessing(screen):
    p.font.init()
    myFont = p.font.SysFont("Comic Sans MS", 30)
    textSurface = myFont.render("Processing", False, (167, 133, 96))
    screen.blit(textSurface, (s.WIDTH / 2 - textSurface.get_width() / 2, s.START_Y + 5))


def displayTitle(screen, x, y, width, height, text):
    p.font.init()
    tFont = p.font.SysFont("Comic Sans MS", 30)

    Title = tFont.render(text, True, (55, 255, 255))
    Rect = Title.get_rect()
    Rect.center = ((x + width / 2), (y + height / 2))
    screen.blit(Title, Rect)
    return Title


# Display the initial buttons
def displayButton(screen, x, y, width, height, text):
    button_surface = p.Surface((width, height), p.SRCALPHA)

    p.font.init()
    font_path = "impact.ttf"
    tFont = p.font.Font(font_path, 30)
    content = tFont.render(text, True, (230, 200, 100))
    Rect = content.get_rect()
    Rect.center = (width // 2, height // 2)
    button_surface.blit(content, Rect)
    screen.blit(button_surface, (x, y))
    return p.Rect(x, y, width, height)


# Display the main menu
def displayMainMenu(screen, gs):
    background = l.loadMainMenu()
    screen.blit(background, (0, 0))

    randomBut = displayButton(screen, s.BUTTEXT_X, s.BUTTEXT_Y, s.BUT_TEXT, s.BUT_TEXT / 6, "Play with Random")
    AIBut = displayButton(screen, s.BUTTEXT_X, s.BUTTEXT_Y + 110, s.BUT_TEXT, s.BUT_TEXT / 6, "Play with AI")
    testBut = displayButton(screen, s.BUTTEXT_X, s.BUTTEXT_Y + 220, s.BUT_TEXT, s.BUT_TEXT / 6, "Random vs AI")

    click = p.mouse.get_pressed()[0]
    if click == 1:
        mouse = p.mouse.get_pos()
        if randomBut.collidepoint(mouse):
            time.sleep(0.2)
            return 1
        elif AIBut.collidepoint(mouse):
            time.sleep(0.2)
            return 2
        elif testBut.collidepoint(mouse):
            time.sleep(0.2)
            return 3
    return -1
