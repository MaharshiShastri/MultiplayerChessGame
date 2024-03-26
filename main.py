import pygame
import sys
import importlib
import mysql.connector

const_module = importlib.import_module("const")#no extra modules
game_module = importlib.import_module("game")
square_module = importlib.import_module("square")#no extra modules
move_module = importlib.import_module("move")#no extra modules

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Maharshi#20",
    database = "chess"
    )

cursor = conn.cursor()
class Main:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (const_module.WIDTH, const_module.HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = game_module.Game()
    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        count = 0
        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // const_module.SQSIZE
                    clicked_col = dragger.mouseX // const_module.SQSIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos, piece.name)
                            dragger.drag_piece(piece)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // const_module.SQSIZE
                    motion_col = event.pos[0] // const_module.SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // const_module.SQSIZE
                        released_col = dragger.mouseX // const_module.SQSIZE
                        
                        if board.squares[released_row][released_col].piece != None:
                            captured_piece = board.squares[released_row][released_col].piece.name
                            point = abs(board.squares[released_row][released_col].piece.value)
                            captured = 1
                        else:
                            captured_piece = "None"
                            point = 0
                            captured = 0
                        # create possible move
                        initial = square_module.Square(dragger.initial_row, dragger.initial_col, dragger.piece)
                        final = square_module.Square(released_row, released_col)
                        move = move_module.Move(initial, final)
                        

                        # valid move ?
                        if board.valid_move(dragger.piece, move) and move.has_moved():
                            # normal capture
                            chance_color = "white" if count % 2 ==0 else "black"
                            captured = board.squares[released_row][released_col].has_piece()
                            
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)
                            sql  = ''' INSERT INTO chess.move
                                         (captured, captured_piece, chance_color, finalmovecol, finalmoverow, initialmovecol, initialmoverow,piece)
                                         VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'''
                            values = (captured, captured_piece, chance_color, released_col, released_row, dragger.initial_col, dragger.initial_row, dragger.piece.name)
                            cursor.execute(sql, values)
                            conn.commit()
                            print("Piece: ", dragger.piece.name, " of color: ", chance_color, "moved from row: ", dragger.initial_row, " column: ", dragger.initial_col, "to row: ", released_row, " column: ",  released_col, "and captured piece: ", captured_piece, "of point: ", point, "boolean: ", captured) 
                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            count = main.counter(count)
                            game.next_turn()

                    dragger.undrag_piece()

                # key press
                elif event.type == pygame.KEYDOWN:

                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                     # changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            pygame.display.update()

    @staticmethod
    def counter(count):
        count = count + 1
        return count
    
main = Main()
main.mainloop()
conn.close()
