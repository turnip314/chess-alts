from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from evaluation import Evaluator

from board import Board

class Search():
    def __init__(self, board: Board, evaluator: 'Evaluator', depth: int):
        self.evaluator = evaluator
        self.board = board
        self.depth = depth

    def get_moves(self, getmax: bool = True, n: int = 5) -> list:
        return []
    
class MinMaxSearch(Search):
    def __init__(self, board: Board, evaluator: 'Evaluator', depth: int):
        super().__init__(board, evaluator, depth)

    def get_moves(self, getmax: bool = True, n: int = 5) -> list:
        pieces = self.board.get_pieces(self.board.turn)
        return []
    
    def get_max(self, board: Board, n: int) -> float:
        return 0
    
    def get_min(self, board: Board, n: int) -> float:
        return 0