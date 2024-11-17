from board import Board
from evaluation import *

bd = Board()
print(bd.grid[1,0].possible_moves(bd))
print(bd.get_display())
print(bd.get_fen())
print(PieceEvaluator().evaluate(bd))
print(StockfishEvaluator().evaluate(bd))