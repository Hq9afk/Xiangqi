import random
import chessEngine as s
import time


def all_in_one_copy(original):
    if original:
        if isinstance(original, list) and isinstance(original[0], list) and isinstance(original[0][0], str):
            # board type: list[list[str]]
            return [row[:] for row in original]
        elif isinstance(original, list) and isinstance(original[0][0], tuple):
            # list of moves: list[list[tuple, tuple]]
            return [move[:] for move in original]
        elif isinstance(original, list) and isinstance(original[0], tuple):
            return original[:]  # shallow copy is enough
        elif isinstance(original, s.Move):
            return original.copy()
        elif isinstance(original, dict):
            # dict[str, int]
            return original.copy()
    else:
        return original[:]  # fallback shallow copy for simple lists


# Minimax algorithm
# Explain MiniMax algo: If your current best result is better than/equal the current worst result your enemy can bring to you,
# then no need to search that branch anymore because your enemy will definitely only continue to choose the result even more worse than that,
# or at least equal. Hence you can skip that branch because you know now for sure that you already having a better result stored.
class Minimax:
    def __init__(self, maxDepth):
        self.maxDepth = maxDepth
        self.MinimaxSuggestedMove = None
        self.evaluationCounter = 0

    # Method to initiate Minimax
    def initiateMinimax(
        self,
        board,
        unPredictedBoard,  # the real board before Minimax
        redTurn,
        redIsMachine,
        depth,
        isMaximizingPlayer,
        moveCounter,
        preGuessMove,
        alpha=float("-inf"),
        beta=float("inf"),
    ):
        MinimaxBoard = all_in_one_copy(board)
        MinimaxNextMoveList = all_in_one_copy(s.State.getAllValid(MinimaxBoard, redTurn, redIsMachine))  # = [ [(),()],[(),()],[(),()] ]
        if depth == 0 or MinimaxNextMoveList == []:
            self.evaluationCounter += 1
            return s.State.evaluate(unPredictedBoard, redTurn, redIsMachine, moveCounter, preGuessMove)
            # Return value of board which is the score of AI
        random.shuffle(MinimaxNextMoveList)

        if isMaximizingPlayer:
            best = float("-inf")
            for move in MinimaxNextMoveList:
                # print("Max------------------")
                moveInfo = s.Move(MinimaxBoard, move[0], move[1])

                nextboard = all_in_one_copy(s.getNextGameState(MinimaxBoard, move))
                preGuessMove.append(moveInfo)
                value = self.initiateMinimax(
                    nextboard,
                    unPredictedBoard,
                    not redTurn,
                    redIsMachine,
                    depth - 1,
                    False,
                    moveCounter,
                    preGuessMove,
                    alpha,
                    beta,
                )
                preGuessMove.pop()
                if value > best:
                    best = value
                    if depth == self.maxDepth:
                        self.MinimaxSuggestedMove = all_in_one_copy(move)
                alpha = max(alpha, best)
                if alpha >= beta:
                    break

            return best

        else:
            best = float("inf")
            for move in MinimaxNextMoveList:
                # print("Min------------------")
                moveInfo = s.Move(MinimaxBoard, move[0], move[1])

                nextboard = all_in_one_copy(s.getNextGameState(MinimaxBoard, move))
                preGuessMove.append(moveInfo)
                value = self.initiateMinimax(
                    nextboard,
                    unPredictedBoard,
                    not redTurn,
                    redIsMachine,
                    depth - 1,
                    True,
                    moveCounter,
                    preGuessMove,
                    alpha,
                    beta,
                )
                preGuessMove.pop()
                if value < best:
                    best = value
                    if depth == self.maxDepth:
                        self.MinimaxSuggestedMove = all_in_one_copy(move)

                beta = min(beta, best)
                if alpha >= beta:
                    break

            return best


# Function to generate random moves
def playWithRandom(state):
    moveList = all_in_one_copy(s.State.getAllValid(state.board, state.redTurn, state.redIsMachine))
    if moveList != []:
        move = random.choice(moveList)
        return s.Move(state.board, move[0], move[1])
    return None


# Function to play using Minimax algorithm
def playWithAI(state):
    minimax = Minimax(1)
    start_time = time.time()  # ⏱️ Start the timer
    minimax.initiateMinimax(
        state.board,
        state.board,
        state.redTurn,
        state.redIsMachine,
        minimax.maxDepth,
        True,
        len(state.moveLog),
        preGuessMove=[],
    )
    move = minimax.MinimaxSuggestedMove
    end_time = time.time()  # ⏱️ End the timer
    duration = end_time - start_time
    print(f"Minimax took {duration:.4f} seconds and {minimax.evaluationCounter} evaluations to return a move.")
    if move is not None:
        m = s.Move(state.board, move[0], move[1])
        return m
    return None


# Function to let the Minimax algorithm play against the random move generator
def AIVSRandom(state):
    play = None
    if state.redIsMachine:
        if state.redTurn:
            play = None
            play = playWithAI(state)
            if play:
                state.makeMove(play)
        else:
            play = None
            play = playWithRandom(state)
            if play:
                state.makeMove(play)
    else:
        if state.redTurn:
            play = None
            play = playWithRandom(state)
        else:
            play = None
            play = playWithAI(state)
        return play


# Function to Manage game modes
def gameModemanager(state, type):
    turn = True if (state.redIsMachine and state.redTurn) or (not state.redIsMachine and not state.redTurn) else False
    if turn:
        play = None
        if type == 1:
            play = playWithRandom(state)
        elif type == 2:
            play = playWithAI(state)
        elif type == 3:
            play = AIVSRandom(state)
        if play:
            state.makeMove(play)
