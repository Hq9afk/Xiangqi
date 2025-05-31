import random
import xiangqi_cpp as engine
import numpy as np
import chessEngine as s
import time
import cProfile

def encode_pos(row, col):
    return row * 10 + col

def decode_pos(pos):
    return pos // 10, pos % 10

def add_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    data[piece] = np.append(data[piece], pos)

def remove_piece_position(data, piece, row, col):
    pos = encode_pos(row, col)
    if piece in data:
        arr = data[piece]
        # Find and remove the position
        mask = arr != pos
        data[piece] = arr[mask]  # Keep only positions that don't match

def change_piece_position(data, piece, old_row, old_col, new_row, new_col):
    old_pos = encode_pos(old_row, old_col)
    new_pos = encode_pos(new_row, new_col)
    arr = data[piece]
    # Find and update position
    idx = np.where(arr == old_pos)[0]
    if len(idx) > 0:
        arr[idx[0]] = new_pos
        
def get_all_chess_piece_positions(data):
    return [decode_pos(pos) for positions in data.values() for pos in positions.tolist()]


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

def universal_chess_piece_dict_reverse(red_data, black_data, chess_pieceSelected, chess_pieceMoveTo, 
                                      startRow, startCol, endRow, endCol):
    if chess_pieceSelected[0] == 'r':
        change_piece_position(red_data, chess_pieceSelected[1:],
                                        endRow, endCol, startRow, startCol)
        if chess_pieceMoveTo != "---":
            add_piece_position(black_data, chess_pieceMoveTo[1:], endRow, endCol)
    else:
        change_piece_position(black_data, chess_pieceSelected[1:],
                                           endRow, endCol, startRow, startCol)
        if chess_pieceMoveTo != "---":
            add_piece_position(red_data, chess_pieceMoveTo[1:], endRow, endCol)

testPointReal = 0
def all_in_one_copy(original):
    if original:
        return [row[:] for row in original]
    else:
        return original  # return as-is for unknown types
        
def copy_pieces_pos_dict(original):
    return {k: v.copy() for k, v in original.items()}
# Minimax algorithm
# Explain MiniMax algo: If your current best result is better than/equal the current worst result your enemy can bring to you,
# then no need to search that branch anymore because your enemy will definitely only continue to choose the result even more worse than that,
# or at least equal. Hence you can skip that branch because you know now for sure that you already having a better result stored.

# class Minimax:
#     def __init__(self, maxDepth):
#         self.maxDepth = maxDepth
#         self.MinimaxSuggestedMove = None
#         self.evaluationCounter = 0
#         self.miniMaxBranchCounter = 0
#     # Method to initiate Minimax
#     def initiateMinimax(
#         self,
#         MinimaxBoard,
#         red_chess_piece_pos_dict, 
#         black_chess_piece_pos_dict,
#         redTurn,
#         redIsMachine,
#         depth,
#         isMaximizingPlayer,
#         moveCounter,
#         preGuessMove,
#         alpha = float("-inf"),
#         beta = float("inf"),
#     ):
#         MinimaxNextMoveList = rule.getAllValid(MinimaxBoard, red_chess_piece_pos_dict, black_chess_piece_pos_dict, redTurn, redIsMachine)
#         if depth == 0 or MinimaxNextMoveList == []:
#             self.evaluationCounter +=1
#             return s.State.evaluate(
#                 redIsMachine, moveCounter, preGuessMove
#             )
#             # Return value of board which is the score of AI
#         self.miniMaxBranchCounter +=1
#         # random.shuffle(MinimaxNextMoveList)
        
#         if isMaximizingPlayer:
#             best = float("-inf")
#             for move in MinimaxNextMoveList:
#                 moveInfo = s.Move(MinimaxBoard, move[0], move[1])
#                 if moveInfo.chess_pieceSelected[0] == 'r':
#                     nextRed_chess_piece_pos_dict = copy_pieces_pos_dict(red_chess_piece_pos_dict)
#                     nextBlack_chess_piece_pos_dict = black_chess_piece_pos_dict
#                 else:
#                     nextRed_chess_piece_pos_dict = red_chess_piece_pos_dict
#                     nextBlack_chess_piece_pos_dict = copy_pieces_pos_dict(black_chess_piece_pos_dict)
#                 universal_chess_piece_dict_update(nextRed_chess_piece_pos_dict,
#                                                   nextBlack_chess_piece_pos_dict,
#                                                   moveInfo.chess_pieceSelected,
#                                                   moveInfo.chess_pieceMoveTo,
#                                                   moveInfo.startRow,
#                                                   moveInfo.startCol,
#                                                   moveInfo.endRow,
#                                                   moveInfo.endCol
#                                                   )
#                 nextboard = s.getNextGameState(MinimaxBoard, move)
#                 preGuessMove.append(moveInfo)
#                 value = self.initiateMinimax(
#                     nextboard,
#                     nextRed_chess_piece_pos_dict,
#                     nextBlack_chess_piece_pos_dict,
#                     not redTurn,
#                     redIsMachine,
#                     depth - 1,
#                     False,
#                     moveCounter,
#                     preGuessMove,
#                     alpha,
#                     beta,
#                 )
#                 preGuessMove.pop()
#                 if value > best:
#                     best = value
#                     if depth == self.maxDepth:
#                         self.MinimaxSuggestedMove = move[:]
#                 alpha = max(alpha, best)
#                 if alpha >= beta:
#                     break

#             return best

#         else:
#             best = float("inf")
#             for move in MinimaxNextMoveList:
#                 moveInfo = s.Move(MinimaxBoard, move[0], move[1])
#                 if moveInfo.chess_pieceSelected[0] == 'r':
#                     nextRed_chess_piece_pos_dict = copy_pieces_pos_dict(red_chess_piece_pos_dict)
#                     nextBlack_chess_piece_pos_dict = black_chess_piece_pos_dict
#                 else:
#                     nextRed_chess_piece_pos_dict = red_chess_piece_pos_dict
#                     nextBlack_chess_piece_pos_dict = copy_pieces_pos_dict(black_chess_piece_pos_dict)
#                 universal_chess_piece_dict_update(nextRed_chess_piece_pos_dict,
#                                                   nextBlack_chess_piece_pos_dict,
#                                                   moveInfo.chess_pieceSelected,
#                                                   moveInfo.chess_pieceMoveTo,
#                                                   moveInfo.startRow,
#                                                   moveInfo.startCol,
#                                                   moveInfo.endRow,
#                                                   moveInfo.endCol
#                                                   )
#                 nextboard = s.getNextGameState(MinimaxBoard, move)
#                 preGuessMove.append(moveInfo)
#                 value = self.initiateMinimax(
#                     nextboard,
#                     nextRed_chess_piece_pos_dict,
#                     nextBlack_chess_piece_pos_dict,
#                     not redTurn,
#                     redIsMachine,
#                     depth - 1,  
#                     True,
#                     moveCounter,
#                     preGuessMove,
#                     alpha,
#                     beta,
#                 )
#                 preGuessMove.pop()
#                 if value < best:
#                     best = value
#                     if depth == self.maxDepth:
#                         self.MinimaxSuggestedMove = move[:]

#                 beta = min(beta, best)
#                 if alpha >= beta:
#                     break

#             return best


# Function to generate random moves
def playWithRandom(state):
    moveList = engine.getAllValid(state.board, state.red_chess_piece_pos_dict, state.black_chess_piece_pos_dict, state.redTurn, state.redIsMachine)
    if moveList != []:
        move = random.choice(moveList)
        return s.Move(state.board, move[0], move[1])
    return None

def playWithAI(state, depth):
    start_time = time.perf_counter_ns()  # ⏱️ Start the timer
    minimax = engine.Minimax(depth)
    minimax.initiateMinimax(
        state.board,
        state.red_chess_piece_pos_dict,
        state.black_chess_piece_pos_dict,
        state.redTurn,
        state.redIsMachine,
        minimax.maxDepth,
        True,
        len(state.moveLog),
        s.testPointReal
    )
    move = minimax.minimaxSuggestedMove
    end_time = time.perf_counter_ns()  # ⏱️ End the timer
    duration = (end_time - start_time)/(1e9)
    print(f"Minimax took {duration:.6f} seconds to return a move.")
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
            play = playWithAI(state, 4)
        if play:
            state.makeMove(play)
    if type == 3:
        play = AIVSRandom(state, 1)
        if play:
            state.makeMove(play)
