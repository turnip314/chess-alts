from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from search import Search

from board import Board
from copy import deepcopy
import numpy as np


class Game:
    def __init__(self, search0: 'Search', search1: 'Search', p: float=1, stop_threshold: float = 2000):
        self.initialize()
        self.search0 = search0
        self.search1 = search1
        self.p = p
        self.stop_threshold = stop_threshold

    def initialize(self):
        self.board = Board()
        self.move_history = []

    def play(self, show=False):
        if show:
            print(self.board.get_display())
        self.move_history.append(self.board)

        while True:
            next_state = self.next_state(self.move_history[-1])
            if next_state is None:
                break

            evaluator = self.search1.evaluator if next_state.turn else self.search0.evaluator
            if show:
                print()
                print("Turn:", next_state.turn)
                print("Move:", next_state.fullmove_number)
                print("Evaluation 0:", self.search0.evaluator.evaluate(next_state))
                print("Evaluation 1:", self.search1.evaluator.evaluate(next_state))
                print(next_state.get_display())
                print()
            self.move_history.append(next_state)
            if next_state.is_checkmate() or next_state.fullmove_number > 100:
                break
        
        last_state = self.move_history[-1]
        evaluator = self.search1.evaluator if last_state.turn else self.search0.evaluator
        return self.move_history, last_state.is_checkmate(), evaluator.evaluate(self.move_history[-1])
            
    def next_state(self, cur_state: Board) -> Board:
        search = self.search1 if cur_state.turn else self.search0

        results = search.get_moves_ranked(cur_state)

        if results:
            i = 0
            while np.random.rand() > self.p:
                i += 1
            i %= len(results)
            _, _, initial_rank, initial_file, final_rank, final_file = results[i]
            return cur_state.move(initial_rank, initial_file, final_rank, final_file)
        return None
