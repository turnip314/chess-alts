import copy
import numpy as np
from pieces import Piece, King, Queen, Rook, Bishop, Knight, Pawn0, Pawn1

BOARD_SIZE = 8
STALEMATE_THRESHOLD = 20

class Board():
    def __init__(self, placement=None):
        self.grid = np.empty([BOARD_SIZE, BOARD_SIZE], dtype=Piece)
        self.turn = 0
        self.halfmove_clock = 0
        self.fullmove_number = 0
        self.stalemate_threshold = 20
        self.initialize(placement)

    def initialize(self, placement=None):
        if placement is None:
            placement = {
                'K': (King, [(0, 4, 0), (7, 4, 1)]),
                'Q': (Queen, [(0, 3, 0), (7, 3, 1)]),
                'R': (Rook, [(0, 0, 0), (0, 7, 0), (7, 0, 1), (7, 7, 1)]),
                'B': (Bishop, [(0, 2, 0), (0, 5, 0), (7, 2, 1), (7, 5, 1)]),
                'N': (Knight, [(0, 1, 0), (0, 6, 0), (7, 1, 1), (7, 6, 1)]),
                'P': (Pawn0, [(1, i, 0) for i in range(BOARD_SIZE)]),
                'p': (Pawn1, [(6, i, 1) for i in range(BOARD_SIZE)])
            }

        self.player0_pieces = []
        self.player1_pieces = []

        for piece_type, (cls, positions) in placement.items():
            for rank, file, player in positions:
                piece = cls(rank, file, player)
                self.grid[rank, file] = piece
                (self.player0_pieces if player == 0 else self.player1_pieces).append(piece)

                if piece_type == 'K':
                    if player == 0:
                        self.King0 = self.grid[rank, file]
                    else:
                        self.King1 = self.grid[rank, file]

    def is_occupied(self, rank: int, file: int) -> bool:
        return self.grid[rank, file] is not None
    
    def is_occupied_by(self, rank: int, file: int, player: int) -> bool:
        if self.grid[rank, file] is None:
            return False
        return self.grid[rank, file].player == player
    
    def get_pieces(self, player: int):
        return self.player1_pieces if player else self.player0_pieces
    
    def is_legal(self, ignore_halfmove=False, verbose=False) -> bool:
        king = self.King0 if self.turn else self.King1
        enemy_pieces = self.get_pieces(self.turn)
        in_check = any(piece.can_capture(king.rank, king.file, self) for piece in enemy_pieces)
        if verbose and in_check:
            print("Player %d can capture the king this turn"%self.turn)
        if verbose and self.halfmove_clock >= STALEMATE_THRESHOLD:
            print("Halfmove clock exceeded")
        return not in_check and (ignore_halfmove or self.halfmove_clock < STALEMATE_THRESHOLD)
    
    def move(self, rank_initial, file_initial, rank_final, file_final):
        board = copy.deepcopy(self)

        if rank_initial == rank_final and file_initial == file_final:
            return board

        piece = board.grid[rank_initial, file_initial]
        if (board.grid[rank_final, file_final] is not None):
            board.halfmove_clock = 0
            if board.grid[rank_final, file_final].player == 0:
                board.player0_pieces.remove(board.grid[rank_final, file_final])
            else:
                board.player1_pieces.remove(board.grid[rank_final, file_final])
        else:
            board.halfmove_clock += 1
        if piece.player:
            board.fullmove_number += 1

        if piece.name == 'P' and rank_final == 7:
            board.player0_pieces.remove(piece)
            board.grid[rank_final,file_final] = Queen(rank_final,file_final,0)
            board.player0_pieces.append(board.grid[rank_final,file_final])
            board.halfmove_clock = 0
        elif piece.name == 'p' and rank_final == 0:
            board.player1_pieces.remove(piece)
            board.grid[rank_final,file_final] = Queen(rank_final,file_final,1)
            board.player1_pieces.append(board.grid[rank_final,file_final])
            board.halfmove_clock = 0
        else:
            board.grid[rank_final, file_final] = piece
            piece.change_position(rank_final, file_final)
        board.grid[rank_initial, file_initial] = None

        for piece in board.player0_pieces + board.player1_pieces:
            piece.moves = piece.get_moves(board)

        board.turn = 1-board.turn

        return board
    
    def is_checkmate(self) -> bool:
        king = self.King1 if self.turn else self.King0
        opp_pieces = self.player0_pieces if self.turn else self.player1_pieces
        if not any([piece.can_capture(king.rank, king.file, self) for piece in opp_pieces]):
            return False

        pieces = self.player1_pieces if self.turn else self.player0_pieces
        for piece in pieces:
            for rank, file in piece.possible_moves(self):
                tmp_board = self.move(piece.rank, piece.file, rank, file)
                if tmp_board.is_legal(ignore_halfmove=True):
                    #print(rank, file)
                    return False
        return True
    
    def is_stalemate(self) -> bool:
        pieces = self.player1_pieces if self.turn else self.player0_pieces
        for piece in pieces:
            moves = piece.possible_moves(self)
            for move in moves:
                if self.move(piece.rank, piece.file, move[0], move[1]).is_legal():
                    return False
        return True

    def get_display(self) -> str:
        piece_symbols = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        }

        def piece_to_symbol(piece):
            return piece.name if piece else " " #piece_symbols.get(piece.name, " ") if piece else " "

        board_lines = []
        for rank in reversed(range(BOARD_SIZE)):
            row = " " + " │ ".join(piece_to_symbol(self.grid[rank, file]) for file in range(BOARD_SIZE))
            board_lines.append(row)
        return "\n───┼───┼───┼───┼───┼───┼───┼───\n".join(board_lines)
    
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
                        counter = 0
                    fen += self.grid[i,j].name
            if (counter > 0):
                fen += str(counter)
            return fen

        return "/".join(
            [row_fen(i) for i in reversed(range(8))]
        ) + " " + ("b" if self.turn else "w") + " - - " + str(self.halfmove_clock) + " " + str(self.fullmove_number)

    def __str__(self):
        return self.get_display()
    
    def get_placement_dictionary(self):
        pd = {
                'K': ('King', []),
                'Q': ('Queen', []),
                'R': ('Rook', []),
                'B': ('Bishop', []),
                'N': ('Knight', []),
                'P': ('Pawn0', []),
                'p': ('Pawn1', [])
            }
        
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.grid[i,j] is not None:
                    piece = self.grid[i,j]
                    if piece.name in "Kk":
                        pd['K'][1].append((i,j,piece.player))
                    if piece.name in "Qq":
                        pd['Q'][1].append((i,j,piece.player))
                    if piece.name in "Rr":
                        pd['R'][1].append((i,j,piece.player))
                    if piece.name in "Bb":
                        pd['B'][1].append((i,j,piece.player))
                    if piece.name in "Nn":
                        pd['N'][1].append((i,j,piece.player))
                    if piece.name in "P":
                        pd['P'][1].append((i,j,piece.player))
                    if piece.name in "p":
                        pd['p'][1].append((i,j,piece.player))
        return pd
    
    def get_board_tensor(self):
        piece_to_encoding = {
            'P': 1,
            'N': 2,
            'B': 3,
            'R': 4,
            'Q': 5,
            'K': 6,
            'p': -1,
            'n': -2,
            'b': -3,
            'r': -4,
            'q': -5,
            'k': -6,
        }

        piece_grid = np.zeros((8, 8), dtype=np.float32)
        diag_grid = np.zeros((8, 8), dtype=np.float32)
        cross_grid = np.zeros((8, 8), dtype=np.float32)
        knight_grid = np.zeros((8, 8), dtype=np.float32)
        king_grid = np.zeros((8, 8), dtype=np.float32)
        for i in range(8):
            for j in range(8):
                piece = self.grid[i, j]
                if piece is not None:
                    marker = -1 if piece.player else 1
                    piece_grid[i, j] = marker
                    if piece.name in "QqBb":
                        diag_grid[i,j] =  marker
                    if piece.name in "QqRr":
                        cross_grid[i,j] = marker
                    if piece.name in "Nn":
                        knight_grid[i,j] = marker
                    if piece.name in "Kk":
                        king_grid[i,j] = marker

        # Channel 2: Halfmove clock (normalized)
        halfmove_channel = np.full((8, 8), self.halfmove_clock / self.stalemate_threshold, dtype=np.float32)

        return np.stack([piece_grid, diag_grid, cross_grid, knight_grid, king_grid, halfmove_channel], axis=0)
    
class EndBoard(Board):
    def __init__(self):
        super().__init__()

    def initialize(self):
        placement = {
            'K': (King, [(0, 1, 0), (6, 6, 1)]),
            'Q': (Queen, [(1, 5, 1)]),
            'R': (Rook, [(1, 6, 1)]),
        }

        self.player0_pieces = []
        self.player1_pieces = []

        for piece_type, (cls, positions) in placement.items():
            for rank, file, player in positions:
                piece = cls(rank, file, player)
                self.grid[rank, file] = piece
                (self.player0_pieces if player == 0 else self.player1_pieces).append(piece)

        self.King0 = self.grid[0,1]
        self.King1 = self.grid[6,6]