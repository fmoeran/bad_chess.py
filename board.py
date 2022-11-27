from move import Move
import pieces

king_moves = [-9, -8, -7, -1, 1, 7, 8, 9]


# returns the positions of the pieces with straight vision to a given position
def get_straights(positions, position):
    row, col = position // 8, position % 8
    out = []
    # look left:
    for d in range(1, col + 1):
        new_position = position - d
        if positions.get(new_position) is not None:
            out.append(new_position)
            break
    # look up:
    for d in range(1, row + 1):
        new_position = position - d * 8
        if positions.get(new_position) is not None:
            out.append(new_position)
            break
    # look right:
    for d in range(1, 8 - col):
        new_position = position + d
        if positions.get(new_position) is not None:
            out.append(new_position)
            break
    # look down:
    for d in range(1, 8 - row):
        new_position = position + d * 8
        if positions.get(new_position) is not None:
            out.append(new_position)
            break

    return out


# returns the positions of the pieces with diagonal vision to a given position
def get_diagonals(positions, position):
    row, col = position // 8, position % 8
    out = []
    # look NW
    for d in range(1, min(row, col) + 1):
        new_position = position - 9 * d
        if positions.get(new_position) is not None:
            out.append(new_position)
            break
    # look SW
    for d in range(1, min(7 - row, col) + 1):
        new_position = position + 7 * d
        if positions.get(new_position) is not None:
            out.append(new_position)
            break
    # look NE
    for d in range(1, min(row, 7 - col) + 1):
        new_position = position - 7 * d
        if positions.get(new_position) is not None:
            out.append(new_position)
            break
    # look SE
    for d in range(1, min(7 - row, 7 - col) + 1):
        new_position = position + 9 * d
        if positions.get(new_position) is not None:
            out.append(new_position)
            break

    return out


# returns the positions of the pieces with L (horse) vision to a given position
def get_ls(positions, position):
    # horse_jumps = [-17, -15, -10, -6, 6, 10, 15, 17] # just a note for each horse jump relative value
    out = []
    row, col = position // 8, position % 8
    # high left
    if row > 1 and col > 0:
        pos = position - 17
        if positions.get(pos) is not None:
            out.append(pos)
    # high right
    if row > 1 and col < 7:
        pos = position - 15
        if positions.get(pos) is not None:
            out.append(pos)
    # medium up left
    if row > 0 and col > 1:
        pos = position - 10
        if positions.get(pos) is not None:
            out.append(pos)
    # medium up right
    if row > 0 and col < 6:
        pos = position - 6
        if positions.get(pos) is not None:
            out.append(pos)
    # medium down left
    if row < 7 and col > 1:
        pos = position + 6
        if positions.get(pos) is not None:
            out.append(pos)
    # medium down right
    if row < 7 and col < 6:
        pos = position + 10
        if positions.get(pos) is not None:
            out.append(pos)
    # low left
    if row < 6 and col > 0:
        pos = position + 15
        if positions.get(pos) is not None:
            out.append(pos)
    # low right
    if row < 6 and col < 7:
        pos = position + 17
        if positions.get(pos) is not None:
            out.append(pos)

    return out


# returns a team's king position
def get_king_pos(positions, colour):
    king_piece = pieces.Piece(pieces.king, colour)
    for position, piece in positions.items():
        if piece == king_piece:
            return position


# returns by how many pieces a position is being attacked by in the opposite colour
def attacks(positions, position, colour):
    row, col = position // 8, position % 8
    straights = get_straights(positions, position)
    diagonals = get_diagonals(positions, position)
    ls = get_ls(positions, position)

    attack_arr = []
    for new_position in straights:
        piece = positions[new_position]
        if piece.colour != colour:
            type = piece.type
            if type == pieces.rook or type == pieces.queen:
                attack_arr.append(new_position)
            elif type == pieces.king:
                nrow, ncol = new_position // 8, new_position % 8
                dist = max(abs(nrow - row), abs(ncol - col))
                if dist <= 1:
                    attack_arr.append(new_position)

    for new_position in diagonals:
        piece = positions[new_position]
        if piece.colour != colour:
            type = piece.type
            if type == pieces.bishop or type == pieces.queen:
                attack_arr.append(new_position)
            elif type == pieces.pawn:
                nrow, ncol = new_position // 8, new_position % 8
                if colour == pieces.white:
                    if nrow == row - 1 and abs(col - ncol) == 1:
                        attack_arr.append(new_position)
                elif colour == pieces.black:
                    if nrow == row + 1 and abs(col - ncol) == 1:
                        attack_arr.append(new_position)
            elif type == pieces.king:
                nrow, ncol = new_position // 8, new_position % 8
                dist = max(abs(nrow - row), abs(ncol - col))
                if dist <= 1:
                    attack_arr.append(new_position)

    for new_position in ls:
        piece = positions[new_position]
        if piece.colour != colour:
            type = piece.type
            if type == pieces.knight:
                attack_arr.append(new_position)

    return attack_arr


# returns a set of every position a piece can move to (though might stil be illegal as it doesn't take the king into
# account
def get_moveable_positions(positions, position, piece):
    position = int(position)
    moveable_positions = set()
    row, col = position // 8, position % 8

    # diagonally
    if piece.type == pieces.queen or piece.type == pieces.bishop:
        # look NW
        for d in range(1, min(row, col) + 1):
            new_position = position - 9 * d
            new_piece = positions.get(new_position)
            if new_piece is None:
                moveable_positions.add(new_position)
            else:
                if new_piece.colour != piece.colour:
                    moveable_positions.add(new_position)
                break

        # look SW
        for d in range(1, min(7 - row, col) + 1):
            new_position = position + 7 * d
            new_piece = positions.get(new_position)
            if new_piece is None:
                moveable_positions.add(new_position)
            else:
                if new_piece.colour != piece.colour:
                    moveable_positions.add(new_position)
                break

        # look NE
        for d in range(1, min(row, 7 - col) + 1):
            new_position = position - 7 * d
            new_piece = positions.get(new_position)
            if new_piece is None:
                moveable_positions.add(new_position)
            else:
                if new_piece.colour != piece.colour:
                    moveable_positions.add(new_position)
                break

        # look SE
        for d in range(1, min(7 - row, 7 - col) + 1):
            new_position = position + 9 * d
            new_piece = positions.get(new_position)
            if new_piece is None:
                moveable_positions.add(new_position)
            else:
                if new_piece.colour != piece.colour:
                    moveable_positions.add(new_position)
                break
    # horizontal/vertical
    if piece.type == pieces.rook or piece.type == pieces.queen:
        # look left:
        for d in range(1, col + 1):
            new_position = position - d
            new_piece = positions.get(new_position)
            if new_piece is None:
                moveable_positions.add(new_position)
            else:
                if new_piece.colour != piece.colour:
                    moveable_positions.add(new_position)
                break
        # look up:
        for d in range(1, row + 1):
            new_position = position - d * 8
            new_piece = positions.get(new_position)
            if new_piece is None:
                moveable_positions.add(new_position)
            else:
                if new_piece.colour != piece.colour:
                    moveable_positions.add(new_position)
                break
        # look right:
        for d in range(1, 8 - col):
            new_position = position + d
            new_piece = positions.get(new_position)
            if new_piece is None:
                moveable_positions.add(new_position)
            else:
                if new_piece.colour != piece.colour:
                    moveable_positions.add(new_position)
                break
        # look down:
        for d in range(1, 8 - row):
            new_position = position + d * 8
            new_piece = positions.get(new_position)
            if new_piece is None:
                moveable_positions.add(new_position)
            else:
                if new_piece.colour != piece.colour:
                    moveable_positions.add(new_position)
                break
    # knight
    if piece.type == pieces.knight:
        # high left
        if row > 1 and col > 0:
            pos = position - 17
            new_piece = positions.get(pos)
            if new_piece is None or new_piece.colour != piece.colour:
                moveable_positions.add(pos)
        # high right
        if row > 1 and col < 7:
            pos = position - 15
            new_piece = positions.get(pos)
            if new_piece is None or new_piece.colour != piece.colour:
                moveable_positions.add(pos)
        # medium up left
        if row > 0 and col > 1:
            pos = position - 10
            new_piece = positions.get(pos)
            if new_piece is None or new_piece.colour != piece.colour:
                moveable_positions.add(pos)
        # medium up right
        if row > 0 and col < 6:
            pos = position - 6
            new_piece = positions.get(pos)
            if new_piece is None or new_piece.colour != piece.colour:
                moveable_positions.add(pos)
        # medium down left
        if row < 7 and col > 1:
            pos = position + 6
            new_piece = positions.get(pos)
            if new_piece is None or new_piece.colour != piece.colour:
                moveable_positions.add(pos)
        # medium down right
        if row < 7 and col < 6:
            pos = position + 10
            new_piece = positions.get(pos)
            if new_piece is None or new_piece.colour != piece.colour:
                moveable_positions.add(pos)
        # low left
        if row < 6 and col > 0:
            pos = position + 15
            new_piece = positions.get(pos)
            if new_piece is None or new_piece.colour != piece.colour:
                moveable_positions.add(pos)
        # low right
        if row < 6 and col < 7:
            pos = position + 17
            new_piece = positions.get(pos)
            if new_piece is None or new_piece.colour != piece.colour:
                moveable_positions.add(pos)
    # pawn NOTE we do not do en passent here. Done in the main legal moves function
    if piece.type == pieces.pawn:
        if piece.colour == pieces.white:  # white
            # 1 step ahead
            if positions.get(position - 8) is None:
                moveable_positions.add(position - 8)
                # 2 steps ahead
                if row == 6:  # second last row
                    if positions.get(position - 16) is None:
                        moveable_positions.add(position - 16)
            # upper right
            new_piece = positions.get(position - 7)
            if new_piece is not None and new_piece.colour != piece.colour and col < 7:
                moveable_positions.add(position - 7)
            # upper left
            new_piece = positions.get(position - 9)
            if new_piece is not None and new_piece.colour != piece.colour and col > 0:
                moveable_positions.add(position - 9)

        elif piece.colour == pieces.black:  # black
            # 1 step
            if positions.get(position + 8) is None:
                moveable_positions.add(position + 8)
                if row == 1:
                    if positions.get(position + 16) is None:
                        moveable_positions.add(position + 16)
            new_piece = positions.get(position + 9)
            # lower right
            if new_piece is not None and new_piece.colour != piece.colour and col < 7:
                moveable_positions.add(position + 9)
            # lower left
            new_piece = positions.get(position + 7)
            if new_piece is not None and new_piece.colour != piece.colour and col > 0:
                moveable_positions.add(position + 7)

    return moveable_positions


# returns all the legal moves for a team(colour) at a current position(positions)
legal_moves_memo = dict() # memoized list of legal moves for certain boards
def get_legal_moves(board):
    moves = set()
    if legal_moves_memo.get(board) is not None:
        return legal_moves_memo[board]

    positions = board.positions
    colour = board.colour
    king_pos = get_king_pos(positions, colour)
    if board.last_move is not None:
        lm_start, lm_end = board.last_move
        was_en_passent = positions[lm_end].type == pieces.pawn and abs(lm_end - lm_start) == 16
    else:
        was_en_passent = False
    # the friendly pieces that could be blocking the king from attack
    king_neighbours = set(filter(lambda x: positions[x].colour == colour,
                                 get_straights(positions, king_pos) + get_diagonals(positions, king_pos)))
    # the positions attacking the king
    king_attack_neighbours = attacks(positions, king_pos, colour)

    attack_positions = set()

    # KING
    krow, kcol = king_pos // 8, king_pos % 8
    for dif in king_moves:
        new_position = king_pos + dif
        new_row, new_col = new_position // 8, new_position % 8
        new_piece = positions.get(new_position)
        distance = max(abs(new_row - krow), abs(new_col - kcol))

        if 0 <= new_position < 64 and 0 <= new_row <= 7 and 0 <= new_col <= 7 \
                and (new_piece is None or new_piece.colour != colour) and distance == 1:
            new_positions = positions.copy()
            new_positions.pop(king_pos)
            if not attacks(new_positions, new_position, colour):
                moves.add(Move(king_pos, new_position))
    # CASTLING
    if not king_attack_neighbours:
        if board.can_castle_ks[colour]:
            spaces = [positions.get(king_pos + 1), positions.get(king_pos + 2)]
            if spaces == [None, None]:
                if not attacks(positions, king_pos + 1, colour) and not attacks(positions, king_pos + 2, colour):
                    moves.add(Move(king_pos, king_pos + 2, castle=True))

        if board.can_castle_qs[colour]:

            spaces = [positions.get(king_pos - 1), positions.get(king_pos - 2), positions.get(king_pos - 3)]
            if spaces == [None, None, None]:
                if not attacks(positions, king_pos - 1, colour) and not attacks(positions, king_pos - 2, colour):
                    moves.add(Move(king_pos, king_pos - 2, castle=True))

    # makes the set "attack_positions" that holds all the positions any piece is allowed to move
    # (it will be every position if the king is not in check but nothing if the king is attacked twice)
    # if the king is attacked by oine position, a piece must be moved to block, take the attacking piece, or king moved
    if len(king_attack_neighbours) == 1:
        attack_pos = king_attack_neighbours[0]
        attack_piece = positions[attack_pos]
        attack_row, attack_col = attack_pos // 8, attack_pos % 8
        king_row, king_col = king_pos // 8, king_pos % 8
        # if attacker is a knight
        if attack_piece.type == pieces.knight:
            attack_positions.add(attack_pos)
        # if the attacker is horizontal
        elif attack_row == king_row or attack_col == king_col:
            if attack_row > king_row:
                dif = 8
            elif attack_row < king_row:
                dif = -8
            elif attack_col > king_col:
                dif = 1
            else:
                dif = -1
            for pos in range(king_pos + dif, attack_pos + dif, dif):
                attack_positions.add(pos)

        # if it's diagonal
        else:
            if attack_row > king_row:
                if attack_col > king_col:
                    dif = 9
                else:
                    dif = 7
            else:
                if attack_col < king_col:
                    dif = -9
                else:
                    dif = -7
            for pos in range(king_pos + dif, attack_pos + dif, dif):
                attack_positions.add(pos)
    elif len(king_attack_neighbours) == 0:
        attack_positions = {i for i in range(64)}


    # main loop through each piece
    for position, piece in positions.items():
        if piece.colour != colour:
            continue
        if piece.type == pieces.king:
            continue

        # all the positions that this type of piece can move to
        # THIS IGNORES WHETHER THE KING WILL BE IN CHECK
        moveable_positions = get_moveable_positions(positions, position, piece)

        possible_moves = {Move(position, end) for end in moveable_positions}

        if piece.type == pieces.pawn:
# EN PASSENT
            if was_en_passent:
                end_row, end_col, row, col = lm_end // 8, lm_end % 8, position // 8, position % 8
                if end_row == row and abs(col - end_col) == 1:
                    midpoint = (lm_start + lm_end) / 2
                    possible_moves.add(Move(position, midpoint, en_passent=True))
# promotion
            promotion_types = [pieces.queen, pieces.rook, pieces.knight, pieces.bishop]
            promotion_pieces = [pieces.Piece(type, colour) for type in promotion_types]
            if colour == 0:
                end_row = 1
            else:
                end_row = 6

            if position // 8 == end_row:  # if they are on the second last row
                possible_moves = set()
                for end in moveable_positions:
                    for promotion_piece in promotion_pieces:
                        possible_moves.add(Move(position, end, promotion_piece=promotion_piece))

        for move in possible_moves:
            if move.end in attack_positions:  # check if this is one of the required move positions
                # TODO THIS IS SLOW
                if position in king_neighbours:  # check that it doesn't open a check from a pinned piece
                    dummy_dict = positions.copy()
                    dummy_dict.pop(position)
                    dummy_dict[move.end] = piece

                    if len(attacks(dummy_dict, king_pos, colour)) >= 1:
                        continue
                if move.en_passent:
                    new_board = board.copy()
                    new_board.make_move(move)
                    if attacks(new_board.positions, get_king_pos(new_board.positions, 1 - new_board.colour),
                               1 - new_board.colour):
                        del new_board
                        continue
                    else:
                        del new_board

                moves.add(move)
            elif move.en_passent:
                new_board = board.copy()
                new_board.make_move(move)
                if not attacks(new_board.positions, get_king_pos(new_board.positions, 1 - new_board.colour),1 - new_board.colour):
                    moves.add(move)
    legal_moves_memo[board.copy()] = moves
    return moves


def get_legal_captures(board):
    moves = get_legal_moves(board)
    enemy_positions = {position for position, piece in board.positions.items() if piece.colour != board.colour}
    captures = {move for move in moves if move.end in enemy_positions or move.en_passent}
    return captures


class Log:
    def __init__(self, logs, current_move, can_castle_ks, can_castle_qs, last_move, half_moves):
        self.logs = logs # holds a list of pairs: (position to change back to, what to change it to)
        self.current_move = current_move
        self.can_castle_ks = can_castle_ks
        self.can_castle_qs = can_castle_qs
        self.last_move = last_move
        self.half_moves = half_moves

    def replace(self, board):
        for position, change in self.logs:
            if change is None:
                board.positions.pop(int(position))
            else:
                board.positions[int(position)] = change
        board.current_move = self.current_move
        board.colour = self.current_move % 2
        board.can_castle_ks = self.can_castle_ks.copy()
        board.can_castle_qs = self.can_castle_qs.copy()
        board.last_move = self.last_move
        board.half_moves = self.half_moves


class Board:
    def __init__(self, positions=None, current_move=0, can_castle_ks=(True, True), can_castle_qs=(True, True),
                 last_move=None, half_moves=0):
        self.positions = positions
        self.current_move = current_move
        self.colour = current_move % 2
        self.can_castle_ks = can_castle_ks
        self.can_castle_qs = can_castle_qs
        self.last_move = last_move
        self.half_moves = half_moves
        # change log to say which positions to change to go back one position
        self.change_log = [] # holds a list of pairs: (position to change back to, what to change it to)

        # holds the positions of where enemy pawns attack
        self.enemy_pawn_attacks = set()

    def copy(self):
        return Board(self.positions.copy(), self.current_move, self.can_castle_ks.copy(), self.can_castle_qs.copy(),
                     self.last_move)

    def __repr__(self):
        return " ".join(map(str, self.get_current_board_info()))

    def __hash__(self):
        num = 0
        for i in range(64):
            if self.positions.get(i) is not None:
                num += 1
            num = num << 1
        return num

    def __eq__(self, other):
        return self.positions.copy() == other.positions.copy() and self.colour == other.colour \
               and self.can_castle_ks[:] == other.can_castle_ks[:] and self.can_castle_qs[:] == other.can_castle_qs[:]

    def get_current_board_info(self):
        return (tuple(self.positions.items()), self.current_move, self.colour,
                tuple(self.can_castle_ks), tuple(self.can_castle_qs), self.last_move, self.half_moves)

    # makes a move on a game THIS IS WHERE EN PASSENT AND CASTLING LOGIC GOES
    # NOTE THIS REQUIRES A LEGAL MOVE TO WORK AND DOES NOT CHECK LEGALITY
    def make_move(self, move):
        new_log = Log([(move.start, self.positions[move.start]),(move.end, self.positions.get(move.end))],
                      self.current_move, self.can_castle_ks.copy(), self.can_castle_qs.copy(), self.last_move, self.half_moves)


        start, end = move.start, move.end

        # whether a piece was taken in the move (changed to True if en-passent)
        took_piece = self.positions.get(end) is not None

        # CASTLE LOGIC
        colour = self.colour
        moved_piece = self.positions[start]

        if moved_piece.type == pieces.king:  # if the move is by a king

            if move.castle:  # if the move is castling

                if colour == pieces.white:  # WHITE
                    if end > start:  # king side
                        new_rook_pos = 61
                        past_rook_pos = 63
                    else:  # queen side
                        new_rook_pos = 59
                        past_rook_pos = 56
                else:  # BLACK
                    if end > start:  # king side
                        new_rook_pos = 5
                        past_rook_pos = 7
                    else:  # queen side
                        new_rook_pos = 3
                        past_rook_pos = 0
                # change log
                new_log.logs.append((new_rook_pos, None))
                new_log.logs.append((past_rook_pos, self.positions[past_rook_pos]))
                self.positions[new_rook_pos] = self.positions.pop(past_rook_pos)


            self.can_castle_qs[colour] = False
            self.can_castle_ks[colour] = False
        # if a rook is taken or moved, no castling on that side
        if moved_piece.type == pieces.rook:  # if the move is by a rook
            if colour == 0:
                if start == 63:
                    self.can_castle_ks[colour] = False
                elif start == 56:
                    self.can_castle_qs[colour] = False
            else:
                if start == 7:
                    self.can_castle_ks[colour] = False
                elif start == 0:
                    self.can_castle_qs[colour] = False
        if self.positions.get(end) is not None:
            if self.positions[end].type == pieces.rook:  # if it takes the other rook
                colour = 1 - colour
                if colour == pieces.white:
                    if end == 63:
                        self.can_castle_ks[colour] = False
                    elif end == 56:
                        self.can_castle_qs[colour] = False
                else:
                    if end == 7:
                        self.can_castle_ks[colour] = False
                    elif end == 0:
                        self.can_castle_qs[colour] = False

        # EN PASSENT (assumes its legal)
        if move.en_passent:
            took_piece = True
            if self.colour == 0:
                dif = 8
            else:
                dif = -8
            if self.last_move == (end - dif, end + dif):
                # change log
                new_log.logs.append((end + dif, self.positions[end + dif]))

                self.positions.pop(end + dif)




        # PROMOTION
        if move.is_promotion:
            self.positions[start] = move.promotion_piece

        self.positions[end] = self.positions.pop(start)

        self.current_move += 1
        self.colour = 1 - self.colour
        self.last_move = (start, end)
        if took_piece:
            self.half_moves = 0
        else:
            self.half_moves += 1

        self.change_log.append(new_log)

        self.enemy_pawn_attacks = set()

    def undo_move(self):
        if not self.change_log:
            raise Exception("No past positions in memory")
        log = self.change_log.pop()
        log.replace(self)
        self.enemy_pawn_attacks = set()

    def is_checkmate(self):
        if not get_legal_moves(self):
            if attacks(self.positions, get_king_pos(self.positions, self.colour), self.colour):
                return True
        return False

    def get_enemy_pawn_attacks(self):
        if self.enemy_pawn_attacks:
            return self.enemy_pawn_attacks

        direction = 8 if self.colour == 0 else -8
        for position, piece in self.positions.items():
            if piece.type == pieces.pawn and piece.colour != self.colour:
                col = position % 8
                if col != 7:
                    self.enemy_pawn_attacks.add(position+direction+1)
                if col != 0:
                    self.enemy_pawn_attacks.add(position+direction-1)
        return self.enemy_pawn_attacks

    # makes every position in positions intigers
    def set_ints(self):
        new_positions = {}
        for position, piece in self.positions.items():
            position = int(position)
            new_positions[position] = piece
        self.positions = new_positions