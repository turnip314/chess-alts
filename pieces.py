from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board

class Piece():
    def __init__(self, name: str, rank: int, file: int, player: int, value: int):
        self.name = name
        self.file = file
        self.rank = rank
        self.player = player
        self.value = value
        self.moves = None

    def possible_moves(self, board: 'Board'):
        #if self.moves is None:
            return self.get_moves(board)
        #return self.moves
    
    def get_moves(self, board:'Board'):
        return [(self.rank, self.file)]
    
    def change_position(self, rank: int, file: int):
        self.file = file
        self.rank = rank
    
    def can_capture(self, rank: int, file: int, board: 'Board'):
        return (rank, file) in self.possible_moves(board)
    
    def __str__(self):
        return self.name
    
class Pawn0(Piece):
    def __init__(self, rank, file, player=0, value=1):
        super().__init__("P",rank,file,player,value)

    def get_moves(self, board: 'Board'):
        if self.rank == 7:
            return []
        moves = []
        if self.rank == 1 and not (board.is_occupied(self.rank+1, self.file) or board.is_occupied(self.rank+2, self.file)):
            moves = [(self.rank+2, self.file)]
        if self.file != 0 and board.is_occupied_by(self.rank+1, self.file-1, 1):
            moves.append((self.rank+1, self.file-1))
        if self.file != 7 and board.is_occupied_by(self.rank+1, self.file+1, 1):
            moves.append((self.rank+1, self.file+1))
        if not board.is_occupied(self.rank+1, self.file):
            moves.append((self.rank+1, self.file))
        return moves
    

class Pawn1(Piece):
    def __init__(self, rank, file, player=1, value=1):
        super().__init__("p",rank,file,player,value)

    def get_moves(self, board: 'Board'):
        if self.rank == 0:
            return []
        moves = []
        if self.rank == 6 and not (board.is_occupied(self.rank-1, self.file) or board.is_occupied(self.rank-2, self.file)):
            moves = [(self.rank-2, self.file)]
        if self.file != 0 and board.is_occupied_by(self.rank-1, self.file-1, 0):
            moves.append((self.rank-1, self.file-1))
        if self.file != 7 and board.is_occupied_by(self.rank-1, self.file+1, 0):
            moves.append((self.rank-1, self.file+1))
        if not board.is_occupied(self.rank-1, self.file):
            moves.append((self.rank-1, self.file))
        return moves
    
class Knight(Piece):
    def __init__(self, rank, file, player, value=3):
        super().__init__("n" if player else "N",rank,file,player,value)

    def get_moves(self, board: 'Board'):
        file_ranks = [
            (self.file-1, self.rank-2),
            (self.file+1, self.rank-2),
            (self.file-1, self.rank+2),
            (self.file+1, self.rank+2),
            (self.file-2, self.rank-1),
            (self.file+2, self.rank-1),
            (self.file-2, self.rank+1),
            (self.file+2, self.rank+1),
        ]
        moves = []
        for file, rank in file_ranks:
            if file >= 0 and file <= 7 and rank >= 0 and rank <= 7 and not board.is_occupied_by(rank, file, self.player):
                moves.append((rank, file))
            
        return moves
    
class Bishop(Piece):
    def __init__(self, rank, file, player, value=3):
        super().__init__("b" if player else "B",rank,file,player,value)

    def get_moves(self, board: 'Board'):
        moves = []
        
        for i in range(1, min(self.file, self.rank)+1):
            if not board.is_occupied(self.rank-i, self.file-i):
                moves.append((self.rank-i, self.file-i))
            else:
                if not board.is_occupied_by(self.rank-i, self.file-i, self.player):
                    moves.append((self.rank-i, self.file-i))
                break
        for i in range(1, min(self.file, 7-self.rank)+1):
            if not board.is_occupied(self.rank+i, self.file-i):
                moves.append((self.rank+i, self.file-i))
            else:
                if not board.is_occupied_by(self.rank+i, self.file-i, self.player):
                    moves.append((self.rank+i, self.file-i))
                break
        for i in range(1, min(7-self.file, self.rank)+1):
            if not board.is_occupied(self.rank-i, self.file+i):
                moves.append((self.rank-i, self.file+i))
            else:
                if not board.is_occupied_by(self.rank-i, self.file+i, self.player):
                    moves.append((self.rank-i, self.file+i,))
                break
        for i in range(1, min(7-self.file, 7-self.rank)+1):
            if not board.is_occupied(self.rank+i, self.file+i):
                moves.append((self.rank+i, self.file+i))
            else:
                if not board.is_occupied_by(self.rank+i, self.file+i, self.player):
                    moves.append((self.rank+i, self.file+i))
                break
            
        return moves
    
class Rook(Piece):
    def __init__(self, rank, file, player, value=5):
        super().__init__("r" if player else "R",rank,file,player,value)

    def get_moves(self, board: 'Board'):
        moves = []
        
        for i in range(1, self.file+1):
            if not board.is_occupied(self.rank, self.file-i):
                moves.append((self.rank, self.file-i))
            else:
                if not board.is_occupied_by(self.rank, self.file-i, self.player):
                    moves.append((self.rank, self.file-i))
                break
        for i in range(1, 7-self.file+1):
            if not board.is_occupied(self.rank, self.file+i):
                moves.append((self.rank, self.file+i))
            else:
                if not board.is_occupied_by(self.rank, self.file+i, self.player):
                    moves.append((self.rank, self.file+i))
                break
        for i in range(1, self.rank+1):
            if not board.is_occupied(self.rank-i, self.file):
                moves.append((self.rank-i, self.file))
            else:
                if not board.is_occupied_by(self.rank-i, self.file, self.player):
                    moves.append((self.rank-i, self.file))
                break
        for i in range(1, 7-self.rank+1):
            if not board.is_occupied(self.rank+i, self.file):
                moves.append((self.rank+i, self.file))
            else:
                if not board.is_occupied_by(self.rank+i, self.file, self.player):
                    moves.append((self.rank+i, self.file))
                break
        #if ((4, 7) in moves):
            #print("!!!")
            #print(board.get_display())
            #return None
            
        return moves
    
class Queen(Piece):
    def __init__(self, rank, file, player,value=9):
        super().__init__("q" if player else "Q",rank,file,player,value)

    def get_moves(self, board: 'Board'):
        moves = []
        
        for i in range(1, min(self.file, self.rank)+1):
            if not board.is_occupied(self.rank-i, self.file-i):
                moves.append((self.rank-i, self.file-i))
            else:
                if not board.is_occupied_by(self.rank-i, self.file-i, self.player):
                    moves.append((self.rank-i, self.file-i))
                break
        for i in range(1, min(self.file, 7-self.rank)+1):
            if not board.is_occupied(self.rank+i, self.file-i):
                moves.append((self.rank+i, self.file-i))
            else:
                if not board.is_occupied_by(self.rank+i, self.file-i, self.player):
                    moves.append((self.rank+i, self.file-i))
                break
        for i in range(1, min(7-self.file, self.rank)+1):
            if not board.is_occupied(self.rank-i, self.file+i):
                moves.append((self.rank-i, self.file+i))
            else:
                if not board.is_occupied_by(self.rank-i, self.file+i, self.player):
                    moves.append((self.rank-i, self.file+i,))
                break
        for i in range(1, min(7-self.file, 7-self.rank)+1):
            if not board.is_occupied(self.rank+i, self.file+i):
                moves.append((self.rank+i, self.file+i))
            else:
                if not board.is_occupied_by(self.rank+i, self.file+i, self.player):
                    moves.append((self.rank+i, self.file+i))
                break
        for i in range(1, self.file+1):
            if not board.is_occupied(self.rank, self.file-i):
                moves.append((self.rank, self.file-i))
            else:
                if not board.is_occupied_by(self.rank, self.file-i, self.player):
                    moves.append((self.rank, self.file-i))
                break
        for i in range(1, 7-self.file+1):
            if not board.is_occupied(self.rank, self.file+i):
                moves.append((self.rank, self.file+i))
            else:
                if not board.is_occupied_by(self.rank, self.file+i, self.player):
                    moves.append((self.rank, self.file+i))
                break
        for i in range(1, self.rank+1):
            if not board.is_occupied(self.rank-i, self.file):
                moves.append((self.rank-i, self.file))
            else:
                if not board.is_occupied_by(self.rank-i, self.file, self.player):
                    moves.append((self.rank-i, self.file))
                break
        for i in range(1, 7-self.rank+1):
            if not board.is_occupied(self.rank+i, self.file):
                moves.append((self.rank+i, self.file))
            else:
                if not board.is_occupied_by(self.rank+i, self.file, self.player):
                    moves.append((self.rank+i, self.file))
                break
            
        return moves
    
class King(Piece):
    def __init__(self, rank, file, player, value=float('inf')):
        super().__init__("k" if player else "K",rank,file,player,value)

    def get_moves(self, board: 'Board'):
        moves = []
        rank_files = [
            (self.rank-1, self.file-1),
            (self.rank-1, self.file+1),
            (self.rank+1, self.file-1),
            (self.rank+1, self.file+1),
            (self.rank, self.file-1),
            (self.rank, self.file+1),
            (self.rank-1, self.file),
            (self.rank+1, self.file)
        ]
        for rank, file in rank_files:
            if rank >= 0 and rank <= 7 and file >= 0 and file <= 7 and not board.is_occupied_by(rank, file, self.player):
                moves.append((rank, file))
            
        return moves