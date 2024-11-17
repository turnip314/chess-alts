import numpy as np
from pieces import Piece, King, Queen, Rook, Bishop, Knight, Pawn0, Pawn1

class Board():
    def __init__(self):
        self.grid = np.empty([8,8],dtype=Piece)
        self.turn = 0
        self.halfmove_clock = 0
        self.fullmove_number = 0
        self.initialize()

    def initialize(self):
        self.King0 = King(0,4,0)
        self.grid[0,4]=self.King0
        self.King1 = King(7,4,1)
        self.grid[7,4] = self.King1

        self.grid[0,3] = Queen(0,3,0)
        self.grid[7,3] = Queen(7,3,1)

        self.grid[0,2] = Bishop(0,2,0)
        self.grid[0,5] = Bishop(0,5,0)
        self.grid[7,2] = Bishop(7,2,1)
        self.grid[7,5] = Bishop(7,5,1)

        self.grid[0,1] = Knight(0,1,0)
        self.grid[0,6] = Knight(0,6,0)
        self.grid[7,1] = Knight(7,1,1)
        self.grid[7,6] = Knight(7,6,1)

        self.grid[0,0] = Rook(0,0,0)
        self.grid[0,7] = Rook(0,7,0)
        self.grid[7,0] = Rook(7,0,1)
        self.grid[7,7] = Rook(7,7,1)

        for file in range(8):
            self.grid[1, file] = Pawn0(1, file)
            self.grid[6, file] = Pawn1(6, file)

    def is_occupied(self, rank: int, file: int) -> bool:
        return self.grid[rank, file] is not None
    
    def is_occupied_by(self, rank: int, file: int, player: int) -> bool:
        if self.grid[rank, file] is None:
            return False
        return self.grid[rank, file].player == player
    
    def get_pieces(self, player: int):
        pieces = []
        for row in self.grid:
            for piece in row:
                if piece is not None and piece.player == player:
                    pieces.append(piece)

        return pieces
    
    def is_legal(self) -> bool:
        if self.turn == 0:
            for row in self.grid:
                for piece in row:
                    if piece is not None and piece.can_capture(self.King1):
                        return False
        elif self.turn == 1:
            for row in self.grid:
                for piece in row:
                    if piece is not None and piece.can_capture(self.King0):
                        return False
                    
        return True
    
    def move(self, rank_initial, file_initial, rank_final, file_final):
        if (self.grid[rank_final, file_final] is not None):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        if self.grid[rank_initial, file_initial].player:
            self.fullmove_number += 1

        self.grid[rank_final, file_final] = self.grid[rank_initial, file_initial]
        self.grid[rank_initial, file_initial] = None
    
    def is_checkmate(self) -> bool:
        king = None
        if self.turn == 0:
            king = self.King0
        elif self.turn == 1:
            king = self.King1
        
        enemy_pieces = self.get_pieces(1-self.turn)
        for i in range(king.rank-1, king.rank+2):
            for j in range(king.file-1, king.file+2):
                if i < 0 or i > 7 or j < 0 or j > 7:
                    continue
                if not any([piece.can_capture(i,j,self) for piece in enemy_pieces]):
                    return False
        
        return True

    
    def get_display(self) -> str:
        return "\n──┼───┼───┼───┼───┼───┼───┼───\n".join(
            [" │ ".join([str(self.grid[i,j]) if self.grid[i,j] is not None else " " for j in range(8)]) for i in reversed(range(8))]
        )
    
    def get_fen(self) -> str:
        def row_fen(i: int) -> str:
            fen = ""
            counter = 0
            for j in range(8):
                if self.grid[i,j] is None:
                    counter += 1
                else:
                    if (counter > 0):
                        fen += str(counter)
                    fen += self.grid[i,j].name
            if (counter > 0):
                fen += str(counter)
            return fen

        return "/".join(
            [row_fen(i) for i in reversed(range(8))]
        ) + " " + ("b" if self.turn else "w") + " - - " + str(self.halfmove_clock) + " " + str(self.fullmove_number)
