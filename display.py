import pygame

import pieces


# A button class used for user selection of a promotion piece
class ImgButton:
    def __init__(self, surface: pygame.Surface, image: pygame.Surface, x: int, y: int):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = image
        self.is_clicked = False
        self.bg_colour = (150, 150, 150)
        self.buffer = 3
        self.curve_buffer = 7
        self.circles = (
            (self.x + self.curve_buffer + self.buffer, self.y + self.curve_buffer + self.buffer),
            (self.x + self.width - self.curve_buffer - self.buffer, self.y + self.curve_buffer + self.buffer),
            (self.x + self.curve_buffer + self.buffer, self.y + self.height - self.curve_buffer - self.buffer),
            (self.x + self.width - self.curve_buffer - self.buffer,
             self.y + self.height - self.curve_buffer - self.buffer)
        )

    # blits the image to the screen
    def display(self):

        pygame.draw.rect(self.surface, self.bg_colour,
                         (self.x + self.curve_buffer + self.buffer, self.y + self.buffer,
                          self.width - self.curve_buffer * 2 - self.buffer * 2, self.height - self.buffer * 2))
        pygame.draw.rect(self.surface, self.bg_colour,
                         (self.x + self.buffer, self.y + self.curve_buffer + self.buffer, self.width - self.buffer * 2,
                          self.height - self.curve_buffer * 2 - self.buffer * 2))
        for circle in self.circles:
            pygame.draw.circle(self.surface, self.bg_colour, circle, self.curve_buffer)

        self.surface.blit(self.image, (self.x, self.y))

        pygame.display.update()

    # checks if the user has clicked on the button, if so it updates the clicked variable
    def update(self):
        self.is_clicked = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(3)[0]:

            if self.x < mouse_x <= self.x + self.width and self.y < mouse_y <= self.y + self.height:
                self.is_clicked = True


# class used to display a board onto a screen
class BoardDisplay:

    def __init__(self, square_size=60, debug=False, board_pos_x=0, board_pos_y=0):
        pygame.font.init()
        self.fps_font = pygame.font.SysFont("Consolas", 24)
        self.square_font = pygame.font.SysFont("Consolas", 16)
        self.square_size = square_size
        # set up screen
        self.board_position_x = board_pos_x
        self.board_position_y = board_pos_y
        self.width = self.square_size * 8
        self.height = self.square_size * 8
        self.screen = pygame.display.set_mode((self.width, self.height))

        # constants
        self.bg_colour = (0, 0, 0)
        self.light_colour = (255, 255, 255)

        # self.dark_colour = (101, 71, 0)
        self.dark_colour = (112, 62, 4)

        # whether to display dfebug numbers
        self.debug = debug

        # cached squares (colour, rect)
        self.squares = []
        # cached nums
        self.debug_nums = []

        # cach the squares
        for row in range(8):
            for col in range(8):
                colour = self.light_colour
                dcolour = self.dark_colour
                if (row % 2 + col) % 2 == 0:
                    colour = self.dark_colour
                    dcolour = self.light_colour
                self.squares.append((colour, pygame.Rect(self.board_position_x + col * self.square_size,
                                                         self.board_position_y + row * self.square_size,
                                                         self.square_size, self.square_size)))
                text = self.square_font.render(str(row * 8 + col), True, dcolour)
                self.debug_nums.append((text, (self.board_position_x + col * self.square_size,
                                               self.board_position_y + row * self.square_size)))

        try:
            self.images = {
                # lights
                pieces.Piece(pieces.bishop, pieces.white): pygame.image.load("piece_images/Chess_blt60.png"),
                pieces.Piece(pieces.king, pieces.white): pygame.image.load("piece_images/Chess_klt60.png"),
                pieces.Piece(pieces.knight, pieces.white): pygame.image.load("piece_images/Chess_nlt60.png"),
                pieces.Piece(pieces.pawn, pieces.white): pygame.image.load("piece_images/Chess_plt60.png"),
                pieces.Piece(pieces.queen, pieces.white): pygame.image.load("piece_images/Chess_qlt60.png"),
                pieces.Piece(pieces.rook, pieces.white): pygame.image.load("piece_images/Chess_rlt60.png"),

                # darks
                pieces.Piece(pieces.bishop, pieces.black): pygame.image.load("piece_images/Chess_bdt60.png"),
                pieces.Piece(pieces.king, pieces.black): pygame.image.load("piece_images/Chess_kdt60.png"),
                pieces.Piece(pieces.knight, pieces.black): pygame.image.load("piece_images/Chess_ndt60.png"),
                pieces.Piece(pieces.pawn, pieces.black): pygame.image.load("piece_images/Chess_pdt60.png"),
                pieces.Piece(pieces.queen, pieces.black): pygame.image.load("piece_images/Chess_qdt60.png"),
                pieces.Piece(pieces.rook, pieces.black): pygame.image.load("piece_images/Chess_rdt60.png"),
            }
        except FileNotFoundError:
            self.images = {
                # lights
                pieces.Piece(pieces.bishop, pieces.white): pygame.image.load("engine/piece_images/Chess_blt60.png"),
                pieces.Piece(pieces.king, pieces.white): pygame.image.load("engine/piece_images/Chess_klt60.png"),
                pieces.Piece(pieces.knight, pieces.white): pygame.image.load("engine/piece_images/Chess_nlt60.png"),
                pieces.Piece(pieces.pawn, pieces.white): pygame.image.load("engine/piece_images/Chess_plt60.png"),
                pieces.Piece(pieces.queen, pieces.white): pygame.image.load("engine/piece_images/Chess_qlt60.png"),
                pieces.Piece(pieces.rook, pieces.white): pygame.image.load("engine/piece_images/Chess_rlt60.png"),

                # darks
                pieces.Piece(pieces.bishop, pieces.black): pygame.image.load("engine/piece_images/Chess_bdt60.png"),
                pieces.Piece(pieces.king, pieces.black): pygame.image.load("engine/piece_images/Chess_kdt60.png"),
                pieces.Piece(pieces.knight, pieces.black): pygame.image.load("engine/piece_images/Chess_ndt60.png"),
                pieces.Piece(pieces.pawn, pieces.black): pygame.image.load("engine/piece_images/Chess_pdt60.png"),
                pieces.Piece(pieces.queen, pieces.black): pygame.image.load("engine/piece_images/Chess_qdt60.png"),
                pieces.Piece(pieces.rook, pieces.black): pygame.image.load("engine/piece_images/Chess_rdt60.png"),
            }


        # make instance's scaled images
        self.images = self.scale_images(self.square_size)

        # colour square for showing the legal moves for a piece
        self.highlight_colour = (200, 50, 20)
        self.highlight_positions = []  # what positions to highlight

    # scales all images to the current size (declared in __init__)
    def scale_images(self, scale):
        new_images = {}
        for piece, image in self.images.items():
            new_images[piece] = pygame.transform.scale(image, (scale, scale))
        return new_images

    # draws a piece type to a row&col
    def draw_piece(self, piece: pieces.Piece, coord):
        x, y = map(lambda i: i - self.square_size // 2, coord)
        pygame.Surface.blit(self.screen, self.images[piece], (x, y))

    # shows the squares of the board
    def display_squares(self, debug=False):
        for i in range(64):
            square = self.squares[i]
            pygame.draw.rect(self.screen, *square)
            if debug:
                text = self.debug_nums[i]
                pygame.Surface.blit(self.screen, *text)

    # displays all possible moves for the current held piece
    def display_moves(self):
        if self.highlight_positions:
            for position in self.highlight_positions:
                row, col = position // 8, position % 8
                pygame.draw.rect(self.screen, self.highlight_colour,
                                 (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    # blits the current piece being held
    def display_holding(self, holding):
        if holding is not None:
            self.draw_piece(holding, pygame.mouse.get_pos())

    def ask_user_for_promotion_piece(self, colour):
        piece_vals = [pieces.queen, pieces.rook, pieces.knight, pieces.bishop]
        size = self.square_size
        midpoint = self.square_size * 4
        positions = [(midpoint - size, midpoint - size), (midpoint, midpoint - size),
                     (midpoint - size, midpoint), (midpoint, midpoint)]
        buttons = [ImgButton(self.screen, self.images[pieces.Piece(piece_val, colour)], x, y)
                   for piece_val, (x, y) in zip(piece_vals, positions)]

        # TODO fix pls9
        while True:
            pygame.event.get()
            for button, piece_val in zip(buttons, piece_vals):
                button.display()
                button.update()
                if button.is_clicked:
                    return pieces.Piece(piece_val, colour)

    # blits all current pieces to the board
    def display_pieces(self, board):
        for position, piece in board.positions.items():
            row, col = position // 8, position % 8
            pygame.Surface.blit(self.screen, self.images[piece],
                                (self.board_position_x + col * self.square_size,
                                 self.board_position_y + row * self.square_size))

    # duh
    def display_fps(self, fps):

        img = self.fps_font.render(str(int(fps)), True, (20, 255, 30))
        self.screen.blit(img, (0, 0))

    def update_screen(self, board, holding=None, fps=0.0, show_fps=False):

        self.display_squares(debug=self.debug)
        self.display_moves()
        self.display_pieces(board)
        self.display_holding(holding)

        if show_fps:
            self.display_fps(fps)
        pygame.display.update()

