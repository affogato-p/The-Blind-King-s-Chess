import pygame
import pieces
import copy

WIDTH = 800
HEIGHT = 800
DEBUG = False

class GameBoard():
    def __init__(self):
        self.board = [["BR","BH","BB","BQ","BK","BB","BH","BR"],
                      ["BP","BP","BP","BP","BP","BP","BP","BP"],
                      ["EE","EE","EE","EE","EE","EE","EE","EE"],
                      ["EE","EE","EE","EE","EE","EE","EE","EE"],
                      ["EE","EE","EE","EE","EE","EE","EE","EE"],
                      ["EE","EE","EE","EE","EE","EE","EE","EE"],
                      ["WP","WP","WP","WP","WP","WP","WP","WP"],
                      ["WR","WH","WB","WQ","WK","WB","WH","WR"]]
        self.black_vision = set()
        self.white_vision = set()
        self.current_player = "W"
        
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece == "EE": continue
                
                color = piece[0]
                p_type = piece[1]
                if p_type == "Q":
                    self.board[x][y] = pieces.Queen(color, x, y)
                elif p_type == "R":
                    self.board[x][y] = pieces.Rook(color, x, y)
                elif p_type == "B":
                    self.board[x][y] = pieces.Bishop(color, x, y)
                elif p_type == "P":
                    self.board[x][y] = pieces.Pawn(color, x, y)
                elif p_type == "K":
                    self.board[x][y] = pieces.King(color, x, y)
                elif p_type == "H":
                    self.board[x][y] = pieces.Knight(color, x, y)
        
        self.white_king = self.board[7][4]
        self.black_king = self.board[0][4]
        
        current_vision = set()
        other_vision = set()
        for y in range(8):
            for x in range(8):
                piece = self.get_piece(x,y)
                
                if str(piece)[0] == self.current_player:
                    current_vision.add((y,x))
                    current_vision = current_vision.union(self.board[y][x].vision(self))
                elif str(piece) != "EE":
                    other_vision.add((y,x))
                    other_vision = other_vision.union(self.board[y][x].vision(self))
        
        self.white_vison = current_vision            
        self.black_vision = other_vision
    
            
    def get_board(self):
        return self.board
    
    def get_piece_str(self, x, y):
        return str(self.board[y][x])
    
    def get_piece(self,x,y):
        return self.board[y][x]
    
    
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The Blind King\'s Chess')

BLACK = (0,0,0,0)
WHITE = (255,255,255,0)

clock = pygame.time.Clock()

game = GameBoard() 

board_png = pygame.image.load('chess_board.png')

black_queen_png = pygame.image.load('QueenBlack.png')
black_pawn_png = pygame.image.load('BlackPawn.png')
black_knight_png = pygame.image.load('BlackKnight.png')
black_king_png = pygame.image.load('BlackKing.png')
black_rook_png = pygame.image.load('BlackRook.png')
black_bishop_png = pygame.image.load('BlackBishop.png')

white_queen_png = pygame.image.load('WhiteQueen.png')
white_pawn_png = pygame.image.load('WhitePawn.png')
white_knight_png = pygame.image.load('WhiteKnight.png')
white_king_png = pygame.image.load('WhiteKing.png')
white_rook_png = pygame.image.load('WhiteRook.png')
white_bishop_png = pygame.image.load('WhiteBishop.png')

darkness_png = pygame.image.load('darkness.png')

def convert_pieces(image):
        if (image == "BQ"): return black_queen_png
        elif (image == "BR"): return black_rook_png
        elif (image == "BB"): return black_bishop_png
        elif (image == "BH"): return black_knight_png
        elif (image == "BP"): return black_pawn_png
        elif (image == "BK"): return black_king_png
        elif (image == "WQ"): return white_queen_png
        elif (image == "WR"): return white_rook_png
        elif (image == "WB"): return white_bishop_png
        elif (image == "WH"): return white_knight_png
        elif (image == "WP"): return white_pawn_png
        elif (image == "WK"): return white_king_png

def blit_alpha(target, source, pos, opacity):
        x = pos[0]
        y = pos[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, pos)


running = True
dragging = False
while running:
            
        gameDisplay.fill(WHITE)
        gameDisplay.blit(board_png, (0,0))
        
        for i in range(8):
            for j in range(8):
                if game.get_piece_str(i,j) != "EE":
                    gameDisplay.blit(convert_pieces(game.get_piece_str(i,j)), (i*100+15,j*100+15))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = int(x//100)
                col = int(y//100)
                piece = game.get_piece_str(row, col)
                if piece[0] == game.current_player and (not dragging):
                    dragging = convert_pieces(game.get_piece_str(row, col))
                    PIECE_TO_MOVE = game.get_piece(row, col)
                
                if DEBUG:
                    print(PIECE_TO_MOVE.vision(game))
                    print(game.get_piece_str(row, col))
                    print("x:", col, "row:", row)
                
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                row = int(x//100)
                col = int(y//100)
                previous_board = copy.deepcopy(game)
                if game.white_king.check(game) and game.current_player == 'W':
                    if dragging:
                        if PIECE_TO_MOVE.move(game,row,col) and not game.white_king.check(game):
                            if game.current_player == "W": game.current_player = "B"
                            else: game.current_player = "W"
                        else:
                            game = previous_board
                            
                    if DEBUG: print("White is in check")
                elif game.black_king.check(game) and game.current_player == 'B':
                    if dragging:
                        if PIECE_TO_MOVE.move(game,row,col) and not game.black_king.check(game):
                            if game.current_player == "W": game.current_player = "B"
                            else: game.current_player = "W"
                        else:
                            game = previous_board
                                
                    if DEBUG: print("Black is in check")
                elif dragging:
                    if PIECE_TO_MOVE.move(game, row, col):
                        if (game.black_king.check(game) and game.current_player == 'B') or (game.white_king.check(game) and game.current_player == 'W'):
                            game = previous_board
                        else:
                            if game.current_player == "W": game.current_player = "B"
                            else: game.current_player = "W"
                dragging = False
                
                    
        # UPDATE VISIBLE SET
        current_vision = set()
        other_vision = set()
        for y in range(8):
            for x in range(8):
                piece = game.get_piece(x,y)
                
                if str(piece)[0] == game.current_player:
                    current_vision.add((y,x))
                    current_vision = current_vision.union(game.get_piece(x,y).vision(game))
                elif str(piece) != "EE":
                    other_vision.add((y,x))
                    other_vision = other_vision.union(game.get_piece(x,y).vision(game))
        
        if game.current_player == "B": 
            game.black_vision = current_vision
            game.white_vision = other_vision
        else: 
            game.white_vision = current_vision
            game.black_vision = other_vision

        for y in range(8):
            for x in range(8):
                if (y,x) not in current_vision:
                    gameDisplay.blit(darkness_png, (x*100,y*100))
        
        pos = list(pygame.mouse.get_pos())
        pos[0] -= 35
        pos[1] -= 35
        if dragging: blit_alpha(gameDisplay, dragging, pos, 128)
        pygame.display.update()
        clock.tick(60)
        
        
        

pygame.quit()
quit()
