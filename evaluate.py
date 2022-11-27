#from locals import *
from board import Board, get_legal_moves
import pieces


piece_worths = {
    pieces.pawn: 100,
    pieces.knight: 300,
    pieces.bishop: 350,
    pieces.rook: 500,
    pieces.queen: 900,
}


piece_square = {
    pieces.Piece(pieces.pawn, pieces.white):
         [0, 0, 0, 0, 0, 0, 0, 0,
          50, 50, 50, 50, 50, 50, 50, 50,
          10, 10, 20, 30, 30, 20, 10, 10,
          5, 5, 10, 25, 25, 10, 5, 5,
          0, 0, 0, 20, 20, 0, 0, 0,
          5, -5, -10, 0, 0, -10, -5, 5,
          5, 10, 10, -20, -20, 10, 10, 5,
          0, 0, 0, 0, 0, 0, 0, 0],
    pieces.Piece(pieces.knight, pieces.white):
         [-50, -40, -30, -30, -30, -30, -40, -50,
          -40, -20, 0, 5, 5, 0, -20, -40,
          -30, 5, 10, 15, 15, 10, 5, -30,
          -30, 0, 15, 20, 20, 15, 0, -30,
          -30, 5, 15, 20, 20, 15, 5, -30,
          -30, 0, 10, 15, 15, 10, 0, -30,
          -40, -20, 0, 0, 0, 0, -20, -40,
          -50, -40, -30, -30, -30, -30, -40, -50],
    pieces.Piece(pieces.bishop, pieces.white):
         [-20, -10, -10, -10, -10, -10, -10, -20,
          -10, 0, 0, 0, 0, 0, 0, -10,
          -10, 0, 5, 10, 10, 5, 0, -10,
          -10, 5, 5, 10, 10, 5, 5, -10,
          -10, 0, 10, 10, 10, 10, 0, -10,
          -10, 10, 10, 10, 10, 10, 10, -10,
          -10, 5, 0, 0, 0, 0, 5, -10,
          -20, -10, -10, -10, -10, -10, -10, -20],
    pieces.Piece(pieces.rook, pieces.white):
         [0, 0, 0, 0, 0, 0, 0, 0,
          5, 10, 10, 10, 10, 10, 10, 5,
          -5, 0, 0, 0, 0, 0, 0, -5,
          -5, 0, 0, 0, 0, 0, 0, -5,
          -5, 0, 0, 0, 0, 0, 0, -5,
          -5, 0, 0, 0, 0, 0, 0, -5,
          -5, 0, 0, 0, 0, 0, 0, -5,
           0, 0, 0, 5, 5, 0, 0, 0],
    pieces.Piece(pieces.queen, pieces.white):
         [-20, -10, -10, -5, -5, -10, -10, -20,
          -10, 0, 0, 0, 0, 5, 0, -10,
          -10, 0, 5, 5, 5, 5, 5, -10,
          -5, 0, 5, 5, 5, 5, 0, 0,
          -5, 0, 5, 5, 5, 5, 0, -5,
          -10, 0, 5, 5, 5, 5, 0, -10,
          -10, 0, 0, 0, 0, 0, 0, -10,
          -20, -10, -10, -5,-5, -10, -10, -20],
    pieces.Piece(pieces.king, pieces.white):
         [-30, -40, -40, -50, -50, -40, -40, -30,
          -30, -40, -40, -50, -50, -40, -40, -30,
          -30, -40, -40, -50, -50, -40, -40, -30,
          -30, -40, -40, -50, -50, -40, -40, -30,
          -20, -30, -30, -40, -40, -30, -30, 20,
          -10, -20, -20, -20, -20, -20, -20, -10,
          20, 20, 0, 0, 0, 0, 20, 20,
          20, 30, 10, 0, 0, 10, 30, 20],

}
# make the black versions
black_piece_squares = [(pieces.Piece(piece.type, pieces.black), table[::-1]) for piece, table in piece_square.items()]
for piece, table in black_piece_squares:
    piece_square[piece] = table


# memoizing is actually slower
def static_evaluate(p_board: Board): # statically estimates a board's value
    # if eval_memo.get(p_board) is not None:
    #     return eval_memo[p_board]
    if p_board.is_checkmate():
        if p_board.colour == 0:
            return float("-inf")
        else:
            return float("inf")
    elif not get_legal_moves(p_board):
        return 0

    # the total sum of the baord's pieces values
    score_sum = 0
    for position, piece in p_board.positions.items():
        if piece.type == pieces.king:
            continue
        mult = piece.colour*-2+1 # -1 if black, 1 if white
        score_sum += piece_worths[piece.type] * mult

    # the total sum of the value of positions on the board
    position_sum = 0
    for position, piece in p_board.positions.items():
        mult = piece.colour * -2 + 1  # -1 if black, 1 if white
        position_sum += piece_square[piece][position] * mult

    total = score_sum + position_sum
    return total


# returns how good the board is for it's current colour to play (aka, you always want it to be positive)
def evaluate(board):
    eval = static_evaluate(board)
    if board.colour == 1:
        eval *= -1
    return eval
