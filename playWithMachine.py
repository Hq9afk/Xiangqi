import random
import chessEngine as s
import rule
import time

def encode_pos(row, col):
    return row * 10 + col

def decode_pos(pos):
    return pos // 10, pos % 10

def add_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    if piece in data:
        data[piece] = data[piece] | frozenset([pos])
    else:
        data[piece] = frozenset([pos])

def remove_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    if piece in data and pos in data[piece]:
        data[piece] = data[piece] - frozenset([pos])

def search_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    if piece in data and pos in data[piece]:
        return decode_pos(pos)  # return as (row, col)
    return None

def change_piece_position(data, piece, old_row, old_col, new_row, new_col):
    old_pos = encode_pos(old_row, old_col)
    new_pos = encode_pos(new_row, new_col)
    if piece in data and old_pos in data[piece]:
        data[piece] = (data[piece] - frozenset([old_pos])) | frozenset([new_pos])
        
def get_all_chess_piece_positions(data):
    return [decode_pos(pos) for positions in data.values() for pos in positions]


def universal_chess_piece_dict_update(red_data, black_data, chess_pieceSelected, chess_pieceMoveTo, 
                                      startRow, startCol, endRow, endCol):
    if chess_pieceSelected[0] == 'r':
        change_piece_position(red_data, chess_pieceSelected[1:],
                                        startRow, startCol, endRow, endCol)
        if chess_pieceMoveTo != "---":
                remove_piece_position(black_data, chess_pieceMoveTo[1:], endRow, endCol)
    else:
        change_piece_position(black_data, chess_pieceSelected[1:],
                                           startRow, startCol, endRow, endCol)
        if chess_pieceMoveTo != "---":
                remove_piece_position(red_data, chess_pieceMoveTo[1:], endRow, endCol)

testPointReal = 0
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
                first_val = next(iter(original.values()))
                if isinstance(first_val, int):
                    return original.copy()
                elif isinstance(first_val, frozenset):
                    return dict(original)
        else:
            return original  # return as-is for unknown types

# Minimax algorithm
# Explain MiniMax algo: If your current best result is better than/equal the current worst result your enemy can bring to you,
# then no need to search that branch anymore because your enemy will definitely only continue to choose the result even more worse than that,
# or at least equal. Hence you can skip that branch because you know now for sure that you already having a better result stored.
class Minimax:
    def __init__(self, maxDepth):
        self.maxDepth = maxDepth
        self.MinimaxSuggestedMove = None
        self.evaluationCounter = 0
        self.miniMaxBranchCounter = 0
    # Method to initiate Minimax
    def initiateMinimax(
        self,
        MinimaxBoard,
        red_chess_piece_pos_dict, 
        black_chess_piece_pos_dict,
        redTurn,
        redIsMachine,
        depth,
        isMaximizingPlayer,
        moveCounter,
        preGuessMove,
        alpha = float("-inf"),
        beta = float("inf"),
    ):
        # leafSartTime = time.perf_counter_ns()
        # # MinimaxBoard = all_in_one_copy(board)
        # nextMoveListStart = time.perf_counter_ns()
        MinimaxNextMoveList = s.State.getAllValid(MinimaxBoard, red_chess_piece_pos_dict, black_chess_piece_pos_dict, redTurn, redIsMachine)
          # = [ [(),()],[(),()],[(),()] ]
        # nextMoveListEnd = time.perf_counter_ns()
        # duration = (nextMoveListEnd - nextMoveListStart)/(1e9)
        if depth == 0 or MinimaxNextMoveList == []:
            self.evaluationCounter +=1
            # if self.miniMaxBranchCounter == 3:
            #     # print(f"Branch {self.miniMaxBranchCounter}'s ", end="")
            #     leafEndTime = time.perf_counter_ns()
            #     preEvaluateTime = (leafEndTime - leafSartTime)/(1e9)
            #     print(f"PreEvaluate time: {preEvaluateTime}s, get next moves time: {duration}s, ", end = "")
                # self.miniMaxBranchCounter +=1
            return s.State.evaluate(
                redIsMachine, moveCounter, preGuessMove
            )
            # Return value of board which is the score of AI
        self.miniMaxBranchCounter +=1
        random.shuffle(MinimaxNextMoveList)
        
        if isMaximizingPlayer:
            best = float("-inf")
            for move in MinimaxNextMoveList:
                # print("Max------------------")
                moveInfo = s.Move(MinimaxBoard, move[0], move[1])
                nextRed_chess_piece_pos_dict = all_in_one_copy(red_chess_piece_pos_dict)
                nextBlack_chess_piece_pos_dict = all_in_one_copy(black_chess_piece_pos_dict)
                universal_chess_piece_dict_update(nextRed_chess_piece_pos_dict,
                                                  nextBlack_chess_piece_pos_dict,
                                                  moveInfo.chess_pieceSelected,
                                                  moveInfo.chess_pieceMoveTo,
                                                  moveInfo.startRow,
                                                  moveInfo.startCol,
                                                  moveInfo.endRow,
                                                  moveInfo.endCol
                                                  )
                nextboard = s.getNextGameState(MinimaxBoard, move)
                preGuessMove.append(moveInfo)
                # branchStartTime = time.perf_counter_ns()
                value = self.initiateMinimax(
                    nextboard,
                    nextRed_chess_piece_pos_dict,
                    nextBlack_chess_piece_pos_dict,
                    not redTurn,
                    redIsMachine,
                    depth - 1,
                    False,
                    moveCounter,
                    preGuessMove,
                    alpha,
                    beta,
                )
                # branchEndTime = time.perf_counter_ns()
                # branchDuration = (branchEndTime - branchStartTime)/(1e9)
                # print(f"---Branch Max {self.miniMaxBranchCounter} take {branchDuration}s to return, get next moves time: {duration}s")
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
                nextRed_chess_piece_pos_dict = all_in_one_copy(red_chess_piece_pos_dict)
                nextBlack_chess_piece_pos_dict = all_in_one_copy(black_chess_piece_pos_dict)
                universal_chess_piece_dict_update(nextRed_chess_piece_pos_dict,
                                                  nextBlack_chess_piece_pos_dict,
                                                  moveInfo.chess_pieceSelected,
                                                  moveInfo.chess_pieceMoveTo,
                                                  moveInfo.startRow,
                                                  moveInfo.startCol,
                                                  moveInfo.endRow,
                                                  moveInfo.endCol
                                                  )
                nextboard = s.getNextGameState(MinimaxBoard, move)
                preGuessMove.append(moveInfo)
                # branchStartTime = time.perf_counter_ns()
                value = self.initiateMinimax(
                    nextboard,
                    nextRed_chess_piece_pos_dict,
                    nextBlack_chess_piece_pos_dict,
                    not redTurn,
                    redIsMachine,
                    depth - 1,  
                    True,
                    moveCounter,
                    preGuessMove,
                    alpha,
                    beta,
                )
                # branchEndTime = time.perf_counter_ns()
                # branchDuration = (branchEndTime - branchStartTime)/(1e9)
                # print(f"---Branch Min {self.miniMaxBranchCounter} take {branchDuration}s to return, get next moves time: {duration}s")
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
    moveList = all_in_one_copy(
        s.State.getAllValid(state.board, state.red_chess_piece_pos_dict, state.black_chess_piece_pos_dict, state.redTurn, state.redIsMachine)
    )
    if moveList != []:
        move = random.choice(moveList)
        return s.Move(state.board, move[0], move[1])
    return None


# Function to play using Minimax algorithm
import time  # Add this at the top of your file if not already imported

def playWithAI(state, depth):
    minimax = Minimax(depth)

    start_time = time.time()  # ⏱️ Start the timer
    minimax.initiateMinimax(
        state.board,
        state.red_chess_piece_pos_dict,
        state.black_chess_piece_pos_dict,
        state.redTurn,
        state.redIsMachine,
        minimax.maxDepth,
        True,
        len(state.moveLog),
        preGuessMove = [],
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
def AIVSRandom(state, depth):
    play = None
    if state.redIsMachine:
        if state.redTurn:
            play = None
            play = playWithAI(state, depth)
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
            play = playWithAI(state, depth)
        return play


# Function to Manage game modes
def gameModemanager(state, type):
    turn = (
        True
        if (state.redIsMachine and state.redTurn)
        or (not state.redIsMachine and not state.redTurn)
        else False
    )
    if turn:
        play = None
        if type == 1:
            play = playWithRandom(state)
        elif type == 2:
            play = playWithAI(state, 3)
        if play:
            state.makeMove(play)
    if type == 3:
        play = AIVSRandom(state, 3)
        if play:
            state.makeMove(play)
