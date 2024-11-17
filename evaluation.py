from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board
from pieces import King
import numpy as np

from stockfish import Stockfish

class Evaluator():
    def evaluate(self, board: 'Board', player: int) -> int:
        return 0

class PieceEvaluator(Evaluator):
    def evaluate(self, board: 'Board') -> int:
        if board.is_checkmate():
            if board.turn == 0:
                return -float('inf')
            elif board.turn == 1:
                return float('inf')
        val = 0
        for i in range(8):
            for j in range(8):
                if board.grid[i,j] is not None and not isinstance(board.grid[i,j], King):
                    if board.grid[i][j].player == 0:
                        val += board.grid[i][j].value
                    elif board.grid[i][j].player == 1:
                        val -= board.grid[i][j].value
        return val
    
class StockfishEvaluator(Evaluator):
    def evaluate(self, board: 'Board') -> int:
        stockfish = Stockfish(path="E:\Courses\CS 686\Project\stockfish\stockfish-windows-x86-64-avx2")
        stockfish.set_fen_position(board.get_fen())
        eval = stockfish.get_evaluation()
        if eval["type"] == "mate":
            return float("inf") if eval["value"] > 0 else -float('inf')

        return eval["value"]/100
        
