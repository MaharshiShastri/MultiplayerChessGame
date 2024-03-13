import pygame
import importlib


const_module = importlib.import_module("const")
board_module = importlib.import_module("board")
dragger_module = importlib.import_module("dragger")
config_module = importlib.import_module("config")
square_module = importlib.import_module("square")
#from const import *
#from board import Board
#from dragger import Dragger
#from config import Config
#from square import Square

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = board_module.Board()
        self.dragger = dragger_module.Dragger()
        self.config = config_module.Config()

    # blit methods

    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(const_module.ROWS):
            for col in range(const_module.COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * const_module.SQSIZE, row * const_module.SQSIZE, const_module.SQSIZE, const_module.SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(const_module.ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * const_module.SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                # col coordinates
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(square_module.Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * const_module.SQSIZE + const_module.SQSIZE - 20, const_module.HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(const_module.ROWS):
            for col in range(const_module.COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * const_module.SQSIZE + const_module.SQSIZE // 2, row * const_module.SQSIZE + const_module.SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * const_module.SQSIZE, move.final.row * const_module.SQSIZE, const_module.SQSIZE, const_module.SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * const_module.SQSIZE, pos.row * const_module.SQSIZE, const_module.SQSIZE, const_module.SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * const_module.SQSIZE, self.hovered_sqr.row * const_module.SQSIZE, const_module.SQSIZE, const_module.SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
