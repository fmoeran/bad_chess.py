from evaluate import piece_worths, piece_square
from board import Board
from move import Move
import pieces


# gives a estimated value of how good a move is
def estimate_value(board: Board, move: Move):
    score = 0
    start_piece = board.positions[move.start]
    end_piece = board.positions.get(move.end)

    # if we take a piece, get the worth of that piece - worth of taking piece
    if end_piece is not None:
        score += piece_worths[end_piece.type]-piece_worths.get(start_piece.type, 0)

    # if the move is a promotion
    if move.is_promotion:
        score += piece_worths[move.promotion_piece.type]

    # if it's attacked by a pawn
    if move.end in board.get_enemy_pawn_attacks():
        score -= piece_worths[start_piece.type] + piece_worths[pieces.pawn]

    score -= piece_square[start_piece][move.start]
    score += piece_square[start_piece][move.end]

    return score


def order_moves(board, moves):
    move_value_pairs = [(move, estimate_value(board, move)) for move in moves]
    move_value_pairs = sorted(move_value_pairs, key=lambda pair: pair[1], reverse=True)
    sorted_list = list(map(lambda pair: pair[0], move_value_pairs))
    #print(sorted_list)
    return sorted_list
