import move
import pieces




def printmap(bitmap: int):
    '''
    prints the 64 bits of a bitmap of a bitboard
    '''
    position = 1
    rows = []

    for row in range(8):
        current_row = []
        for col in range(8):
            current_row.append("1" if position & bitmap else ".")
            position <<= 1
        rows.append("".join(current_row[::-1]))
    print("\n".join(rows[::-1]))


class Board:
    def __init__(self, wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk, ep, wlc, wrc, blc, brc, move_count, hm):
        '''
        NOTE this should not usually be used to start up a game, instead use from_fen
        initializes the bitmaps for every type of piece, the colours, the en passent pawn, the rules for castling,
        the current move and colour.
        The en passent pawn is actually the position that another pawn can take it at, not its position but one behind it
        '''
        self.wpawn, self.wbishop, self.wknight, self.wrook, self.wqueen, self.wking = wp, wn, wb, wr, wq, wk
        self.bpawn, self.bbishop, self.bknight, self.brook, self.bqueen, self.bking = bp, bn, bb, br, bq, bk
        self.white = wp | wn | wb | wr | wq | wk
        self.black = bp | bn | bb | br | bq | bk
        self.ep_map = ep
        self.wleft_castle, self.wright_castle, self.bleft_castle, self.bright_castle = wlc, wrc, blc, brc
        self.current_move = move_count
        self.colour = self.current_move % 2
        self.half_moves = hm

    def __repr__(self):
        current_pieces = [self.wpawn, self.wbishop, self.wknight, self.wrook, self.wqueen, self.wking,
                          self.bpawn, self.bbishop, self.bknight, self.brook, self.bqueen, self.bking]
        string = ""
        position = 1
        for row in range(64):
            for i, piece in enumerate(current_pieces):

                if position & piece:
                    string += pieces.coloured_letters[i]
                    break
            else:
                string += "."
            position <<= 1
            if row % 8 == 7:
                string += "\n"
        return string

    def make_move(self, p_move: move.Move):
        '''
        Makes a move on the board and updates logic (e.g. current_move)
        NOTE this does not take legality into account.
        '''

        start, end = p_move.start, p_move.end



    @classmethod
    def from_fen(cls, fen: str):
        '''
        returns a fully initialized instance of a Board from a FEN string
        :param fen: FEN string of board to initialize
        :return: initialized Board
        '''
        data = fen.split()
        while len(data) < 6:
            data.append("-")
        layout, colour, castles, pawn_move, half_move, full_move = data

        # getting positions
        init_pieces = [0 for _ in pieces.coloured_values]  # wp, wn, wb, wr etc...
        position = 1  # will be left shifted to access each position
        for char in layout[::-1]:
            if char == "/":
                continue
            elif "0" < char <= "9":
                position <<= int(char)
            else:
                piece_val = pieces.coloured_values[char]
                init_pieces[piece_val] |= position
                position <<= 1

        # colour
        init_colour = pieces.white if colour == "w" else pieces.black
        # castling rights
        wlc, wrc, blc, brc = "Q" in castles, "K" in castles, "q" in castles, "k" in castles
        # en passent bitmap
        ep = 0
        if pawn_move != "-":
            last_move_end = ((8 - move.column_letters.index(pawn_move[0])) + 8 * (int(pawn_move[1]) - 1)) - 1
            if init_colour == pieces.white:
                ep = 1 << last_move_end >> 8
            else:
                ep = 1 << last_move_end << 8

        # half and full move counts
        hm = 0
        if half_move != "-":
            hm = int(half_move)
        moves = init_colour
        if moves != "-":
            moves = int(full_move)
        return cls(*init_pieces, ep, wlc, wrc, blc, brc, moves, hm)


board = Board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w QKqk - 0 1")
print(board)


