from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from evaluation import Evaluator

from board import Board
import numpy as np

class Search():
    def __init__(self, evaluator: 'Evaluator', depth: int, width: int = 1000):
        self.evaluator = evaluator
        self.depth = depth
        self.width = width

    def get_moves_ranked(self, board: Board, get_max: bool = True) -> list:
        return []
    
class NaiveMinMaxSearch(Search):
    def __init__(self, evaluator: 'Evaluator', depth: int, width: int = 1000):
        super().__init__(evaluator, depth, width)

    def get_moves_ranked(self, board: Board) -> list:
        pieces = board.get_pieces(board.turn)
        board_states = []
        visited_fens = set()

        for piece in pieces:
            moves = piece.possible_moves(board)
            for move in moves:
                new_board = board.move(piece.rank, piece.file, move[0], move[1])
                if new_board.is_legal() and new_board.get_fen() not in visited_fens:
                    visited_fens.add(new_board.get_fen())
                    eval_score = self.evaluator.evaluate(new_board)
                    board_states.append((new_board, eval_score, piece.rank, piece.file, move[0], move[1]))

        board_states.sort(key=lambda x: x[1], reverse=not board.turn)
        board_states = board_states[:self.width]

        # Prioritize mate in 1
        if board_states and (1 if board_states[0][0].turn else -1) * board_states[0][1] == float('inf'):
            return [board_states[0]]

        for _ in range(self.depth - 1):
            # check if checkmate here
            new_board_states = []
            for board, _, ri, fi, rf, ff in board_states:
                pieces = board.get_pieces(board.turn)
                for piece in pieces:
                    moves = piece.possible_moves(board)
                    for move in moves:
                        new_board = board.move(piece.rank, piece.file, move[0], move[1])
                        if new_board.is_legal() and new_board.get_fen() not in visited_fens:
                            visited_fens.add(new_board.get_fen())
                            new_eval = self.evaluator.evaluate(new_board)
                            new_board_states.append((new_board, new_eval, ri, fi, rf, ff))
            new_board_states.sort(key=lambda x: x[1], reverse=not board.turn)
            if not new_board_states:
                break
            board_states = new_board_states[:self.width]
            if (1 if board_states[0][0].turn else -1) * board_states[0][1] == float('inf'):
                return [board_states[0]]

        return board_states
    
class DynamicMinMaxSearch(NaiveMinMaxSearch):
    def __init__(self, evaluator: 'Evaluator', depth: int, width: int = 1000):
        super().__init__(evaluator, depth, width)
        self.first_expand = False
        self.second_expand = False
        self.third_expand = False

    def get_moves_ranked(self, board: Board) -> list:
        if not self.first_expand and len(board.player0_pieces) + len(board.player1_pieces) <  15:
            self.depth += 2
            self.width *= 2
            self.first_expand = True
        if not self.second_expand and len(board.player0_pieces) + len(board.player1_pieces) < 8:
            self.depth += 2
            self.width *= 2
            self.second_expand = True
        if not self.third_expand and board.fullmove_number > 100:
            self.depth += 4
            self.width *= 2
            self.third_expand = True
        return super().get_moves_ranked(board)