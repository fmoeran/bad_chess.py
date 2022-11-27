import pygame
import random
import time

import move
import display
from board import Board, get_legal_moves, attacks, get_king_pos
import pieces


pygame.init()

starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w QKqk - 0 1"


# converts a fen string into a dict of positions of pieces
def fen_to_board(fen):
    nums = [str(n) for n in range(1, 9)]
    data = fen.split()
    while len(data) < 6:
        data.append("-")
    layout, colour, castles, pawn_move, half_move, full_move = data
    positions = {}
    position = 0
    board = Board()
    for char in layout:
        if char == "/":
            pass
        elif char in nums:
            position += int(char)
        else:
            piece_val = pieces.values[char.upper()]
            piece_colour = "a"<=char<="z"
            positions[position] = pieces.Piece(piece_val, piece_colour)
            position += 1
    board.positions = positions
    if colour == "w":
        board.colour = 0
    elif colour == "b":
        board.colour = 1
    board.can_castle_ks = ["K" in castles, "k" in castles]
    board.can_castle_qs = ["Q" in castles, "q" in castles]
    if pawn_move != "-":
        last_move_end = move.column_letters.index(pawn_move[0]) + 8 * int(pawn_move[1])
        if colour == 0:
            dif = 16
        else:
            dif = -16
        board.last_move = (last_move_end + dif, last_move_end)
    if full_move != "-":
        board.current_move = (int(full_move) - 1) * 2 + board.colour
    else:
        board.current_move = board.colour
    if half_move != "-":
        board.half_moves = int(half_move)

    return board


# class with the game loop that activates each move and contains a board display and board
class Game:

    def __init__(self, size=60, white_is_ai=0, black_is_ai=0, debug=False):

        self.debug = debug
        self.clock = pygame.time.Clock()

        self.board_position_x = 0
        self.board_position_y = 0
        # the display to show the board
        self.display = display.BoardDisplay(size, debug=self.debug, board_pos_x=self.board_position_x,
                                            board_pos_y=self.board_position_y)

        self.square_size = size

        # which players (if either) are AI
        self.white_is_ai = white_is_ai
        self.black_is_ai = black_is_ai

        # to check if the process (multiprocessing.process) is still running
        self.ai_running = False

        self.board = fen_to_board(starting_fen)

        # True on the frame that they occur
        self.mouse_pressed = False
        self.mouse_released = False

        # the current piece that the player is holding
        self.holding = None
        # where the player picked up their holding from ( if they are holding)
        self.picked_up_position = None

        # holds all the current legal moves for the player whose move it is
        self.current_legal_moves = None

    def __repr__(self):
        out = ""
        for i in range(64):
            if i % 8 == 0:
                out += "\n"
            if self.board.positions.get(i) is not None:
                out += str(self.board.positions[i])
            else:
                out += " "

        return out

    # loads a fen string into the board
    def load_fen(self, fen):
        self.board = fen_to_board(fen)

    # updates self.current_moves to a set with every legal move the current team can make
    def update_current_moves(self):  # runs the first frame a player's move function is called
        self.current_legal_moves = get_legal_moves(self.board)

    # returns a legal Move class (THIS IS WHERE PROMOTION IS DONE ON THE PLAYERS SIDE)
    # NOTE this requires current_legal_moves to be updated
    def generate_move(self, start, end):
        new_move = move.Move(start, end)

        # checks if the normal move is legal
        moves = self.current_legal_moves

        if new_move in moves:
            return new_move
        start_piece = self.board.positions[start]
        #start_piece_char = piece_letters[start_piece].upper()
        if start_piece.type == pieces.king:
            # checks if the move is a castle
            new_move = move.Move(start, end, castle=True)
            if new_move in moves:
                return new_move
        elif start_piece.type == pieces.pawn:
            # checks for en passent
            new_move = move.Move(start, end, en_passent=True)
            if new_move in moves:
                return new_move
            # checks if any promotion is legal
            queen = pieces.Piece(pieces.queen, self.board.colour)

            new_move = move.Move(start, end, promotion_piece=queen)
            if new_move in moves:
                promotion_piece = self.display.ask_user_for_promotion_piece(self.board.colour)
                return move.Move(start, end, promotion_piece=promotion_piece)

        # will return None if there aere no legal moves with those positions

    # ----------------------------------------------------------------------------------------
    # attempts to move a piece via calling outside function (make_move). If it is illegal, raise an exception
    def move_piece(self, move):

        try:
            if move not in self.current_legal_moves:
                raise Exception(f"{move.start}-{move.end} is not in legal moves")
            self.board.make_move(move)
            self.current_legal_moves = None  # resets legal moves
        except Exception as e:
            print(f"Failed to move piece from {move.start} to {move.end}")
            raise e

    # turns a mouse position to a board position
    def get_mouse_position(self, pos):
        x, y = pos
        col = x // self.square_size
        row = y // self.square_size
        board_position = row * 8 + col
        return board_position

    # activates the mouse "holding" a piece
    def grab_position(self, pos):
        if self.board.positions.get(pos) is None:
            return

        piece = self.board.positions[pos]
        if piece.colour == self.board.colour:
            del self.board.positions[pos]
            self.holding = piece
            self.picked_up_position = pos
            self.display.highlight_positions = [move.end for move in self.current_legal_moves
                                                if move.start == self.picked_up_position]

    # places down the current held piece
    def place_holding(self, pos):
        position = self.get_mouse_position(pos)
        self.board.positions[self.picked_up_position] = self.holding
        move = self.generate_move(self.picked_up_position, position)

        if move in self.current_legal_moves:
            self.move_piece(move)
        self.holding = None
        self.picked_up_position = None
        self.display.highlight_positions = []

    def mouse_is_on_board(self):
        pos = pygame.mouse.get_pos()
        if (self.board_position_x <= pos[0] <= self.board_position_x + 8 * self.square_size and
                self.board_position_y <= pos[1] <= self.board_position_y + 8 * self.square_size):
            return True
        else:
            return False

    # ---------------------------------------------------------------------------------
    # MOVE FUNCTIONS
    # activates each frame it is a player's turn to move
    def player_move(self):
        mouse_button = pygame.mouse.get_pressed(3)[0]
        # print(mouse_buttons)
        if mouse_button and not self.mouse_pressed:
            self.mouse_pressed = True
            if self.mouse_is_on_board():
                self.grab_position(self.get_mouse_position(pygame.mouse.get_pos()))

        if not mouse_button and self.mouse_pressed:
            self.mouse_pressed = False
            if self.mouse_is_on_board():
                if self.holding is not None and self.picked_up_position is not None:
                    self.place_holding(pygame.mouse.get_pos())

    # activates each frame it is an AI's turn to move (by default it is set to random)
    # can be changed via self.set_ai(self, function)
    def ai_move(self):
        if self.board.colour == 0:
            new_move = self.white_ai_move(self.board.copy())
        else:
            new_move = self.black_ai_move(self.board.copy())
        self.move_piece(new_move)

    def black_ai_move(self, p_board):
        time.sleep(0.1)
        legal_moves = get_legal_moves(p_board)
        return random.choice(list(legal_moves))

    def white_ai_move(self, p_board):
        time.sleep(0.1)
        legal_moves = get_legal_moves(p_board)
        return random.choice(list(legal_moves))

    def set_ai(self, func, colour=1):
        if colour == 1:
            self.black_ai_move = func
        elif colour == 0:
            self.white_ai_move = func

    # updates the current moves(if not already) and then accesses the current player's move function
    def move(self):
        if self.current_legal_moves is None:
            self.update_current_moves()
            if self.current_legal_moves == set():
                return self.board.colour
            # also make all the boards positions integers (prevents errors)
            self.board.set_ints()
        if self.board.current_move % 2 == 0:
            if self.white_is_ai:
                self.ai_move()
            else:
                self.player_move()
        else:
            if self.black_is_ai:
                self.ai_move()
            else:
                self.player_move()

    # ----------------------------------------------------------------------------------
    # the main loop for the game
    def run(self, display=True, show_fps=False):  # returns 0 for white win, 1 for black win, None for draw
        running = True
        while running:
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        if self.debug and self.board.change_log:
                            self.board.undo_move()
                            self.current_legal_moves = None
            if display:
                self.display.update_screen(self.board, holding=self.holding, fps=self.clock.get_fps(),
                                           show_fps=show_fps)
            move = self.move()

            if move is not None:
                if attacks(self.board.positions, get_king_pos(self.board.positions, self.board.colour),
                           self.board.colour):
                    return 1 - self.board.colour
                else:
                    return None

        pygame.quit()


if __name__ == "__main__":
    game = Game(debug=False, white_is_ai=False, black_is_ai=False)
    result = game.run(show_fps=True)
    print(result)
