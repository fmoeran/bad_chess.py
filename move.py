column_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
piece_letters = ["P", "N", "B", "R", "Q", "K"]


# a class to hold an instance of a type of move
class Move:
    def __init__(self, start: int, end: int, promotion_piece = None, en_passent: bool = False, castle=False):
        self.start = int(start)
        self.end = int(end)
        self.is_promotion = promotion_piece is not None
        self.promotion_piece = promotion_piece
        self.en_passent = en_passent
        self.castle = castle

    def notate(self):
        starting = column_letters[self.start % 8] + str(8 - self.start // 8)
        ending = column_letters[self.end % 8] + str(8 - self.end // 8)
        promotion = ""
        if self.is_promotion:
            promotion = str(self.promotion_piece)
        return starting + ending + promotion

    def __repr__(self):
        out = f"{self.start}-{self.end}"
        if self.is_promotion:
            out += f" +{piece_letters[self.promotion_piece.type]}"
        if self.en_passent:
            out += " ep"
        if self.castle:
            out += " castle"
        return out

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.promotion_piece == other.promotion_piece \
               and self.en_passent == other.en_passent and self.castle == other.castle

    def __hash__(self):
        return self.start + 64*self.end

