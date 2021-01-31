class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

class Pawn(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.first_move = True
        if color == "W":
            self.valid_moves = [(0,-1), (0,1), (-1,1), (1,1), (0,2)]
        if color == "B":
            self.valid_moves = [(0,1), (0,-1), (-1,-1), (1,-1), (0,-2)]
        
    def __str__(self):
        if self.color == "W":
            return "WP"
        else:
            return "BP"
        
    def move(self, board, x, y):
        valid = False
        # move up to 2 spaces
        
        move = (self.col-x, self.row-y)
        if move in self.valid_moves:
            # NORMAL MOVE
            if board.get_board()[y][x] == "EE" and ((move == self.valid_moves[0]) or (move == self.valid_moves[1])):
                valid = True
            # KILL
            elif (board.get_board()[y][x] != "EE" and str(board.get_board()[y][x])[0] != self.color) and ((move == self.valid_moves[2]) or (move == self.valid_moves[3])):
                valid = True
            
            # FIRST MOVE
            elif self.first_move and (move == self.valid_moves[4] and (board.get_board()[self.row+self.valid_moves[0][1]][self.col] == "EE") and (board.get_board()[y][x] == "EE")):
                valid = True

                
        if valid:
            board.get_board()[self.row][self.col] = "EE"
            board.get_board()[y][x] = self
            self.col = x
            self.row = y
            # Promotion
            if self.row == 7 and self.color == "B":
                self.promote(board)
            elif self.row == 0 and self.color == "W":
                self.promote(board)
            self.first_move = False
            return True
        
        return False
        
        
        
    def promote(self, board):
        board.get_board()[self.row][self.col] = Queen(self.color, self.row, self.col)
    
    def vision(self, board):
        visible = set()
        for i in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
            r = self.row + i[0]
            c = self.col + i[1]
            if 0 <=r < 8 and 0 <=c < 8:
                visible.add((r,c))
        if self.first_move:
            if self.color == "W":
                visible.add((self.row-2,self.col))
            else:
                visible.add((self.row+2,self.col))
        return visible

class King(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.moved = False
        
    def __str__(self):
        if self.color == "W":
            return "WK"
        else:
            return "BK"
        
    def check(self, board):
        if len(self.vision(board)) == 0:
            return False
        else:
            return True
    
    def castle(self, board, rook):
        rook_view = rook.vision(board)
        king_pos = (self.row, self.col)
        
        if king_pos in rook_view:
            board.get_board()[self.row][self.col] = "EE"
            board.get_board()[rook.row][rook.col] = "EE"
            if (7,2) in rook_view or (0,2) in rook_view:
                self.col = 2
                rook.col = 3
                board.get_board()[self.row][2] = self
                board.get_board()[rook.row][3] = rook
                self.moved = True
                rook.moved = True
                return True
            elif (7,6) in rook_view or (0,6) in rook_view:
                self.col = 6
                rook.col = 5
                board.get_board()[self.row][6] = self
                board.get_board()[rook.row][5] = rook
                self.moved = True
                rook.moved = True
                return True
            
        return False
    
    def move(self, board, x, y):
        valid_moves = set()
        # Check for castling
        piece = board.get_board()[y][x]
        if (not self.moved) and str(piece)[0] == self.color and str(piece)[1] == "R" and (not piece.moved):
            return self.castle(board, piece)
        
        for i in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            r = self.row + i[0]
            c = self.col + i[1]
            if 0 <= r < 8 and 0 <= c < 8:
                valid_moves.add((r, c))
        
        if self.color == 'W':
            valid_moves = valid_moves.intersection(board.white_vision)
            threats = board.black_vision
            valid_moves.difference_update(threats)
        else:
            valid_moves = valid_moves.intersection(board.black_vision)
            threats = board.white_vision
            valid_moves.difference_update(threats)
            
        print(valid_moves)
        
        if(y, x) in valid_moves and str(board.get_board()[y][x])[0] != self.color :
            board.get_board()[self.row][self.col] = "EE"
            board.get_board()[y][x] = self
            self.row = y
            self.col = x
            self.moved = True
            return True
        return False
            
    
    def vision(self, board):
        visible = set()
        for i in range(8):
            for j in range(8):
                if board.get_board()[j][i] != "EE" and str(board.get_board()[j][i])[0] != self.color and str(board.get_board()[j][i])[1] != "K":
                    
                    if str(board.get_board()[j][i])[1] == "P" and (self.row,self.col) in board.get_board()[j][i].vision(board):
                        pawn = board.get_board()[j][i]
                        relative_pos = (self.row-pawn.row, self.col-pawn.col)
                        if self.color == 'W' and relative_pos in ((1,-1),(1,1)):
                            visible.add((board.get_board()[j][i].row, board.get_board()[j][i].col))
                        elif relative_pos in ((-1,1),(-1,-1)):
                            visible.add((board.get_board()[j][i].row, board.get_board()[j][i].col))
                            
                    elif str(board.get_board()[j][i])[1] == "H" and (self.row,self.col) in board.get_board()[j][i].vision(board):
                        horse = board.get_board()[j][i]
                        relative_pos = (abs(self.row-horse.row), abs(self.col-horse.col))
                        if relative_pos in ((2,1),(1,2)):
                            visible.add((board.get_board()[j][i].row, board.get_board()[j][i].col))
                        
                    elif (self.row,self.col) in board.get_board()[j][i].vision(board):
                        visible.add((board.get_board()[j][i].row, board.get_board()[j][i].col))
        return visible

class Queen(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.valid_moves = []
    
    def __str__(self):
        if self.color == "W":
            return "WQ"
        else:
            return "BQ"    
    def move(self, board, x, y):
        self.valid_moves = self.vision(board)
        
        if (y,x) in self.valid_moves and (board.get_board()[y][x] == "EE" or board.get_board()[y][x].color != self.color):
            board.get_board()[self.row][self.col] = "EE"
            board.get_board()[y][x] = self
            self.row = y
            self.col = x
            return True
        return False
            
    
    def vision(self, board):
        visible = set()
        for i in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
            r = self.row + i[0]
            c = self.col + i[1]
            while 0 <=r < 8 and 0 <=c < 8:
                if board.get_board()[r][c] != "EE":
                    visible.add((r,c))
                    break
                visible.add((r,c))
                r = r + i[0]
                c = c + i[1]
        return visible 
    
class Rook(Piece):
    def __init__(self, color, row, col):
        self.moved = False
        Piece.__init__(self, color, row, col)
        
    def __str__(self):
        if self.color == "W":
            return "WR"
        else:
            return "BR"   
         
    def move(self, board, x, y):
        self.valid_moves = self.vision(board)
        piece = board.get_board()[y][x]
        if (not self.moved) and str(piece)[0] == self.color and str(piece)[1] == "K" and (not piece.moved):
            return piece.castle(board, self)
        
        if (y,x) in self.valid_moves and (board.get_board()[y][x] == "EE" or board.get_board()[y][x].color != self.color):
            board.get_board()[self.row][self.col] = "EE"
            board.get_board()[y][x] = self
            self.row = y
            self.col = x
            self.moved = True
            return True
        return False
    
    def vision(self, board):
        visible = set()
        for i in [(1,0),(-1,0),(0,1),(0,-1)]:
            r = self.row + i[0]
            c = self.col + i[1]
            while 0 <=r < 8 and 0 <=c < 8:
                if board.get_board()[r][c] != "EE":
                    visible.add((r,c))
                    break
                visible.add((r,c))
                r = r + i[0]
                c = c + i[1]
        return visible
    
class Bishop(Piece):
    def __init__(self, color, row, col):
        Piece.__init__(self, color, row, col)
        self.valid_moves = []
    def __str__(self):
        if self.color == "W":
            return "WB"
        else:
            return "BB"
        
    def move(self, board, x, y):
        self.valid_moves = self.vision(board)
        if (y, x) in self.valid_moves and str(board.get_board()[y][x])[0] != self.color:
            board.get_board()[self.row][self.col] = "EE"
            board.get_board()[y][x] = self
            self.row = y
            self.col = x
            return True
        return False
    
    def vision(self, board):
        visible = set()
        for i in [(1,1),(-1,1),(1,-1),(-1,-1)]:
            r = self.row + i[0]
            c = self.col + i[1]
            while 0 <=r < 8 and 0 <=c < 8:
                if board.get_board()[r][c] != "EE":
                    visible.add((r,c))
                    break
                visible.add((r,c))
                r = r + i[0]
                c = c + i[1]
        return visible 

class Knight(Piece):
    def init(self, color, row, col):
        Piece.init(self, color, row, col)
        
    def __str__(self):
        if self.color == "W":
            return "WH"
        else:
            return "BH"
        
    def move(self, board, x, y):
        valid_moves = set()
        for i in [(-2,1),(-2,-1),(-1,-2),(-1,2),(1,2),(2,1),(1,-2),(2,-1)]:
            r = self.row + i[0]
            c = self.col + i[1]
            if 0 <=r < 8 and 0 <=c < 8:
                valid_moves.add((r,c))
        if (y, x) in valid_moves and str(board.get_board()[y][x])[0] != self.color:
            board.get_board()[self.row][self.col] = "EE"
            board.get_board()[y][x] = self
            self.row = y
            self.col = x
            return True
        return False  

    def vision(self, board):
        visible = set()
        for i in [(-2,1),(-2,-1),(-1,-2),(-1,2),(1,2),(2,1),(1,-2),(2,-1)]:
            r = self.row + i[0]
            c = self.col + i[1]
            if 0 <=r < 8 and 0 <=c < 8:
                visible.add((r,c))
        for i in [(0,-1),(0,-2),(-1,-1),(0,1),(0,2),(-1,1),(1,1),(1,-1)]:
            r = self.row + i[0]
            c = self.col + i[1]
            if 0 <=r < 8 and 0 <=c < 8:
                visible.add((r,c))
        return visible

    