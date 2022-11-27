from board import Board, get_legal_moves
from locals import *
from evaluate import evaluate
from order_moves import order_moves
import time
import tqdm


# basic minimax https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/


DEFAULT_DEPTH = 4
nodes = 0

# gives the best move from a position
def minimax(p_board):
    maximizing = p_board.colour == 0

    moves_list = list(get_legal_moves(p_board))

    moves_list = order_moves(p_board, moves_list)

    move_score_list = [] # (move, score)

    alpha = float("-inf")
    beta = float("inf")

    for move in tqdm.tqdm(moves_list):

        p_board.make_move(move)
        score = __minimax(p_board, DEFAULT_DEPTH - 1, not maximizing, alpha, beta)
        p_board.undo_move()
        move_score_list.append((move, score))

        if maximizing:
            if alpha < score:
                alpha = score
        else:
            if beta > score:
                beta = score

    func = max if p_board.colour == 0 else min
    best_move, value = func(move_score_list, key=lambda pair: pair[1])
    print("value:", value)
    print("nodes:", nodes)
    return best_move



# gives the value of a given position (called by minimax)
def __minimax(board, depth, maximizing: bool, alpha, beta):
    moves = get_legal_moves(board)

    global nodes


    if depth == 0 or not moves:
        return evaluate(board)

    #moves = order_moves(board, moves)

    if maximizing:
        for move in moves:
            nodes += 1
            board.make_move(move)
            eval = __minimax(board, depth-1, False, alpha, beta)
            board.undo_move()
            if alpha < eval:
                alpha = eval
            if beta <= alpha:
                break
        return alpha
    else:
        for move in moves:
            nodes += 1
            board.make_move(move)
            eval = __minimax(board, depth - 1, True, alpha, beta)
            board.undo_move()
            if beta > eval:
                beta = eval
            if beta <= alpha:
                break
        return beta







