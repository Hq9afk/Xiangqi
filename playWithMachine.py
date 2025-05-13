import random
from copy import deepcopy
import chessEngine as s

#this is the function generate random move
def playingRandom(state):
    moveList = deepcopy(s.State.getAllValid(state.board, state.redTurn, state.redIsMachine))
    if moveList != []:
        move = random.choice(moveList)
        return s.Move(state.board, move[0], move[1])
    return None

# This is Minimax algorithm
moveCounter = 0    # keep number step of state (for defind start, mid, end game)
class Minimax:
    def __init__(self, maxDepth):
        self.maxDepth = maxDepth
        self.nodeExpand = 0
        self.MinimaxSuggestedMove = None
        self.path = []

    # this is the function to play Minimax
    def initiateMinimax(self, board, redTurn, redIsMachine, depth, isMaximizingPlayer, c, alpha = float('-inf'), beta = float('inf')):
        global moveCounter
        MinimaxBoard = deepcopy(board)
        MinimaxNextMoveList = deepcopy(s.State.getAllValid(MinimaxBoard, redTurn , redIsMachine)) # = [ [(),()],[(),()],[(),()] ]
        if depth == 0 or MinimaxNextMoveList == []:
            return s.State.evaluate(MinimaxBoard, redTurn, redIsMachine, c)*(1 if isMaximizingPlayer else -1), None #*(1 if isMaximizingPlayer else -1)      # return value of board which is the score of AI
        self.nodeExpand += 1
        random.shuffle(MinimaxNextMoveList)
        if isMaximizingPlayer:
            best = float('-inf')
            for move in MinimaxNextMoveList:
                nextboard = deepcopy(s.getNextGameState(MinimaxBoard, not isMaximizingPlayer, redIsMachine, move))
                value, path = self.initiateMinimax(nextboard, not redTurn, redIsMachine, depth-1, False, c, alpha, beta)
                if value > best:
                    best = value
                    if depth == self.maxDepth:
                        self.MinimaxSuggestedMove = deepcopy(move)
                alpha = max(alpha, best)
                if alpha >= beta:
                    break

            return best, self.path
        else:
            best = float('inf')
            for move in MinimaxNextMoveList:
                nextboard = deepcopy(s.getNextGameState(MinimaxBoard, redTurn, redIsMachine, move))
                value, path = self.initiateMinimax(nextboard, not redTurn , redIsMachine, depth-1, True, c, alpha, beta)
                if value < best:
                    best = value
                    if depth == self.maxDepth:
                        self.MinimaxSuggestedMove = deepcopy(move)
                        
                beta = min(beta, best)
                if alpha >= beta:
                    break

            return best, self.path


# this is the function that call CHACAPRO in UI
def playWithChaCaPro(state):
    minimax = Minimax(2) 
    minimax.initiateMinimax(state.board, state.redTurn, state.redIsMachine, minimax.maxDepth, True, len(state.moveLog))
    move = minimax.MinimaxSuggestedMove
    if move != None:
        m = s.Move(state.board, move[0], move[1])
        return m
    return None


# this is the entring function of AI which decide which AI will play
def gameModemanager(state, type):
    turn = True if (state.redIsMachine and state.redTurn) or (not state.redIsMachine and not state.redTurn) else False
    if turn:
        play = None
        if type == 1:
            play = playingRandom(state)
        elif type == 2:
            play = playWithChaCaPro(state)
        if play:
            state.makeMove(play)


# this is the function to test AI (all win with random machine)
def AI_VS_RANDOM_Mode(state):
    play = None
    if state.redIsMachine:
        if state.redTurn:
            play = None
            play = playWithChaCaPro(state)
            if play:
                state.makeMove(play)
        else:
            play = None
            play = playingRandom(state)
            if play:
                state.makeMove(play)
    else:
        if state.redTurn:
            play = None
            play = playingRandom(state)
        else:
            play = None    
            play = playWithChaCaPro(state)
        return play
