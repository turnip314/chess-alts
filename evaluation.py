from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board
from pieces import King
import numpy as np

from stockfish import Stockfish

class Evaluator():
    def evaluate(self, board: 'Board') -> int:
        return 0

class PieceEvaluator(Evaluator):
    def evaluate(self, board: 'Board') -> int:
        if board.is_checkmate():
            if board.turn == 0:
                return -float('inf')
            elif board.turn == 1:
                return float('inf')
        val = 0
        for piece in board.player0_pieces:
            if piece.name != 'K':
                val += piece.value
        for piece in board.player1_pieces:
            if piece.name != 'k':
                val -= piece.value
        for i in range(8):
            for j in range(8):
                if board.grid[i,j] is not None and not isinstance(board.grid[i,j], King):
                    if board.grid[i][j].player == 0:
                        val += board.grid[i][j].value
                    elif board.grid[i][j].player == 1:
                        val -= board.grid[i][j].value
        return val
    
class StockfishEvaluator(Evaluator):
    def __init__(self, elo=None) -> None:
        super().__init__()
        self.stockfish = Stockfish(path="E:\Courses\CS 686\Project\stockfish\stockfish-windows-x86-64-avx2", depth=6)
        if elo:
            self.stockfish.set_elo_rating(elo)
        
    def evaluate(self, board: 'Board') -> int:
        self.stockfish.set_fen_position(board.get_fen())
        eval = self.stockfish.get_evaluation()
        if eval["type"] == "mate":
            return float("inf") if eval["value"] > 0 else -float('inf')

        return eval["value"]/100
    
class PiecePositionEvaluator(Evaluator):
    def __init__(self):
        self.piece_evaluator = PieceEvaluator()

    def evaluate(self, board: 'Board') -> int:
        #if board.is_stalemate():
            #return 0
        val = 0
        for piece in board.get_pieces(0):
            val += len(piece.possible_moves(board))/10
        for piece in board.get_pieces(1):
            val -= len(piece.possible_moves(board))/10
        
        val += self.piece_evaluator.evaluate(board) + (-1 if board.turn else 1)/2
        val *= (board.stalemate_threshold - board.halfmove_clock + 1)/(board.stalemate_threshold + 1)
        return val
        
import torch
import torch.nn as nn
import torch.nn.functional as F

class CNNEvaluator(nn.Module):
    def __init__(self):
        super(CNNEvaluator, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=6, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 1)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)  # Flatten for fully connected layers
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.tanh(self.fc2(x))  # Output between -1 and 1
        return x
    
    def evaluate(self, board: 'Board'):
        if board.is_checkmate():
            if board.turn == 0:
                return -float('inf')
            elif board.turn == 1:
                return float('inf')
        return self.forward(torch.tensor(board.get_board_tensor()).unsqueeze(0)).item()