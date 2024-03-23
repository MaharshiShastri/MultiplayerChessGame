import importlib

const_module = importlib.import_module("const")#no extra module
square_module = importlib.import_module("square")#no extra module
piece_module = importlib.import_module("piece")#no extra module
move_module = importlib.import_module("move")#no extra module
sound_module = importlib.import_module("sound")#no extra module

#from const import *
#from square import Square
#from piece import *
#from move import Move
#from sound import Sound
import copy
import os
import mysql.connector

"""conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Maharshi#20",
    database = "chess"
    )"""
#cursor = conn.cursor()
class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(const_module.COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        
    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final
        
        en_passant_empty = self.squares[final.row][final.col].isempty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        if isinstance(piece, piece_module.Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
               #command = ''' INSERT INTO moves(initial_move, final_move, capture, piece) VALUES(%s,%s,%s,%s)'''
               # values = (initial, final, True, "Pawn")
                #cursor.execute(command, values)
                #cursor.commit()
                if not testing:
                    sound = sound_module.Sound(
                        os.path.join('assets/sounds/capture.wav'))
                    sound.play()
            
            # pawn promotion
            else:
                self.check_promotion(piece, final)
                #command = ''' INSERT INTO moves(initial_move, final_move, capture, piece) VALUES(%s,%s,%s,%s)'''
                #values = (initial, final, False, "Pawn")

        # king castling
        if isinstance(piece, piece_module.King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = piece_module.Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        
        if not isinstance(piece, piece_module.Pawn):
            return

        for row in range(const_module.ROWS):
            for col in range(const_module.COLS):
                if isinstance(self.squares[row][col].piece, piece_module.Pawn):
                    self.squares[row][col].piece.en_passant = False
        
        piece.en_passant = True

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        
        for row in range(const_module.ROWS):
            for col in range(const_module.COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, piece_module.King):
                            return True
        
        return False

    def calc_moves(self, piece, row, col, bool=True):
        '''
            Calculate all the possible (valid) moves of an specific piece on a specific position
        '''
        
        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if square_module.Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = square_module.Square(row, col)
                        final = square_module.Square(possible_move_row, col)
                        # create a new move
                        move = move_module.Move(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if square_module.Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = square_module.Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = square_module.Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move
                        move = move_module.Move(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

            # en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en pessant
            if square_module.Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, piece_module.Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = square_module.Square(row, col)
                            final = square_module.Square(fr, col-1, p)
                            # create a new move
                            move = move_module.Move(initial, final)
                            
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
            
            # right en pessant
            if square_module.Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, piece_module.Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = square_module.Square(row, col)
                            final = square_module.Square(fr, col+1, p)
                            # create a new move
                            move = move_module.Move(initial, final)
                            
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)


        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if square_module.Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = square_module.Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = square_module.Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = move_module.Move(initial, final)
                        #if final_piece != None and square_module.Square.has_enemy_piece(final,piece.color):
                          #  captured_piece = self.got_captured(final_piece)
                            #print("New move at ",possible_move_row, possible_move_col, "and has ",captured_piece)
                        #enter the move in DB
                        #captured_piece = get_piece()
                        #sql = """ INSERT INTO chess.move(initialmovecol,initialmoverow, finalmoverow, finalmovecol, captured, piece, captued_piece)
                        #              % VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                        #if captured_piece == None:
                            #values = (col, row, possible_move_row, possible_move_col, 0, self.piece, captured_piece)
                            #cursor.execute(sql, values)
                            #conn.commit()
                        #else:
                            #values = (col, row, possible_move_row, possible_move_col, 1, self.piece, captured_piece)
                            #cursor.execute(sql, values)
                            #conn.commit()

                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if square_module.Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = square_module.Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = square_module.Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = move_module.Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # not in range
                    else: break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if square_module.Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = square_module.Square(row, col)
                        final = square_module.Square(possible_move_row, possible_move_col) # piece=piece
                        # create new move
                        move = move_module.Move(initial, final)
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, piece_module.Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = square_module.Square(row, 0)
                                final = square_module.Square(row, 3)
                                moveR = move_module.Move(initial, final)

                                # king move
                                initial = square_module.Square(row, col)
                                final = square_module.Square(row, 2)
                                moveK = move_module.Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, piece_module.Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between ?
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = square_module.Square(row, 7)
                                final = square_module.Square(row, 5)
                                moveR = move_module.Move(initial, final)

                                # king move
                                initial = square_module.Square(row, col)
                                final = square_module.Square(row, 6)
                                moveK = move_module.Move(initial, final)

                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

        if isinstance(piece, piece_module.Pawn): 
            pawn_moves()

        elif isinstance(piece, piece_module.Knight): 
            knight_moves()

        elif isinstance(piece, piece_module.Bishop): 
            straightline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
            ])

        elif isinstance(piece, piece_module.Rook): 
            straightline_moves([
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1), # left
            ])

        elif isinstance(piece, piece_module.Queen): 
            straightline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1) # left
            ])

        elif isinstance(piece, piece_module.King): 
            king_moves()

    def _create(self):
        for row in range(const_module.ROWS):
            for col in range(const_module.COLS):
                self.squares[row][col] = square_module.Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(const_module.COLS):
            self.squares[row_pawn][col] = square_module.Square(row_pawn, col, piece_module.Pawn(color))

        # knights
        self.squares[row_other][1] = square_module.Square(row_other, 1, piece_module.Knight(color))
        self.squares[row_other][6] = square_module.Square(row_other, 6, piece_module.Knight(color))

        # bishops
        self.squares[row_other][2] = square_module.Square(row_other, 2, piece_module.Bishop(color))
        self.squares[row_other][5] = square_module.Square(row_other, 5, piece_module.Bishop(color))

        # rooks
        self.squares[row_other][0] = square_module.Square(row_other, 0, piece_module.Rook(color))
        self.squares[row_other][7] = square_module.Square(row_other, 7, piece_module.Rook(color))

        # queen
        self.squares[row_other][3] = square_module.Square(row_other, 3, piece_module.Queen(color))

        # king
        self.squares[row_other][4] = square_module.Square(row_other, 4, piece_module.King(color))

    @staticmethod
    def got_captured(piece):
        return piece.name
    '''color1, color2'''
#sconn.close()
