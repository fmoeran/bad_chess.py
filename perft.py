import time

import game
from board import get_legal_moves


fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w QKqk - 0 1"
#fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -"
fen = "rnbqkbnr/pppppppp/8/8/P7/8/1PPPPPPP/RNBQKBNR b KQkq - 0 1"


board = game.fen_to_board(fen)


def perft(search_depth, print_moves=True):
    out = []
    move_list = get_legal_moves(board)
    n_moves = len(move_list)
    node_count = 0

    if search_depth == 1:
        return n_moves

    for move in move_list:
        board.make_move(move)
        count = perft(search_depth - 1, print_moves=False)
        node_count += count

        if print_moves:
            out.append((move.notate(), count))

        board.undo_move()

    if out:
        out = sorted(out, key=lambda x: x[0])
        for line in out:
            print(line[0] + ": " + str(line[1]))
    return node_count

t = time.time()

depth = 4
print(depth, perft(depth))

print(f"finished in {time.time()-t:.2f}s")

