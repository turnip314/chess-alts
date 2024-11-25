from board import *
from evaluation import *
from search import *
from game import *
from train import *
from multiprocessing import Pool, cpu_count


SAVE_PATH = "E:\Courses\CS 686\Project\models\\test_model.pth"

model = CNNEvaluator()
model.load_state_dict(torch.load(SAVE_PATH))
model.eval()

def simulate_game(game_id, model, depth, width, stop_threshold=1000):
    # Setup evaluator and search
    mms = DynamicMinMaxSearch(model, depth, width)
    states = []
    values = []

    with torch.no_grad():
        # Create a game instance
        game = Game(mms, mms, 0.65+np.random.random()*0.3, stop_threshold=stop_threshold)
        game.board.turn = game_id % 2  # Alternate starting player

        # Play the game
        move_history, is_checkmate, eval = game.play()

        # Assign value based on evaluation
        val = -1 if eval < -game.stop_threshold else (1 if eval > game.stop_threshold else 0)

        # Collect the last 10 moves
        n = len(move_history)
        weights = np.square(np.linspace(0, 1, n))
        for board, weight in zip(move_history, weights):
            states.append(board.get_board_tensor())
            values.append(np.array([weight]))

        return states, values, game_id

def run_simulation(game_id):
    return simulate_game(game_id, model, 2, 6, 32)

def run_training(multithread=False):
    states = []
    values = []

    if multithread:
        num_games = 2
        num_workers = min(cpu_count(), num_games)
        
        with Pool(num_workers) as pool:
            results = pool.map(run_simulation, range(num_games))

        
        for s, v, game_id in results:
            states.extend(s)
            values.extend(v)
            print(f"Game {game_id + 1} completed.")
    else:
        mms = DynamicMinMaxSearch(model, 2, width=6)
        with torch.no_grad():
            for i in range(20):
                game = Game(mms, mms, 0.65+np.random.random()*0.3, stop_threshold=1000)
                game.board.turn = i%2
                move_history, is_checkmate, eval = game.play()
                val = -1 if eval < -game.stop_threshold else (1 if eval > game.stop_threshold else 0)
                n = len(move_history)
                weights = np.square(np.linspace(0, 1, n))
                for board, weight in zip(move_history, weights):
                    states.append(board.get_board_tensor())
                    values.append(np.array([weight*val]))
                print("Game", i+1)
                print(move_history[-1])
                print(move_history[-1].get_placement_dictionary())
                print(val)
                print(is_checkmate)
                print()

    print(len(states))
    print(len(values))
    dataset = ChessDataset(states, values)
    train_loader = DataLoader(dataset, batch_size=8, shuffle=True)
    trainer = Trainer(model)
    trainer.train_model(train_loader, epochs=100, save_path = SAVE_PATH)

def run_testing():
    #np.random.seed(seed=123)

    mms0 = DynamicMinMaxSearch(model, 2, width=6)
    mms1 = DynamicMinMaxSearch(PiecePositionEvaluator(), 2, width=6)
    game = Game(mms0, mms1, p=1, stop_threshold=1000)
    game.board = Board(placement=None)
    print("Initial eval: ", model.evaluate(game.board))

    with torch.no_grad():
        history, _, _ = game.play(show=True)
    
    last_state = history[-1]
    print(last_state.is_checkmate())

def run_debugging():
    placement = {
        'K': (King, [(0, 4, 0), (6, 4, 1)]), 
        'Q': (Queen, [(3, 7, 0), (7, 4, 1)]), 
        'R': (Rook, [(0, 0, 0), (0, 7, 0), (7, 1, 1), (7, 7, 1)]), 
        'B': (Bishop, [(0, 5, 0), (6, 6, 1), (7, 2, 1)]), 
        'N': (Knight, [(1, 3, 0), (1, 4, 0), (5, 2, 1), (7, 6, 1)]), 
        'P': (Pawn0, [(1, 0, 0), (1, 1, 0), (1, 5, 0), (1, 6, 0), (2, 4, 0), (2, 7, 0), (3, 2, 0), (3, 3, 0)]), 
        'p': (Pawn1, [(2, 5, 1), (3, 0, 1), (4, 3, 1), (5, 4, 1), (6, 1, 1), (6, 2, 1), (6, 7, 1)])}

    bd = Board(placement=placement)
    bd.turn=1
    print(bd)
    print(bd.turn)
    print(bd.is_checkmate())

def compare_against_stockfish(elo=1000):
    stockfish = Stockfish(path="E:\Courses\CS 686\Project\stockfish\stockfish-windows-x86-64-avx2")
    stockfish.update_engine_parameters({
        "UCI_LimitStrength": True,
        "UCI_Elo": 100
    })
    stockfish.set_depth(1)
    stockfish2 = Stockfish(path="E:\Courses\CS 686\Project\stockfish\stockfish-windows-x86-64-avx2")
    stockfish2.update_engine_parameters({
        "UCI_LimitStrength": True,
        "UCI_Elo": 4000
    })
    stockfish2.set_depth(16)
    search = DynamicMinMaxSearch(model, 2, 6)
    board = Board()
    while True:
        
        results = search.get_moves_ranked(board)
        if results:
            _, _, ri, fi, rf, ff = results[0]
            board = board.move(ri, fi, rf, ff)
            print()
            print("Turn:", board.turn)
            print("Move:", board.fullmove_number)
            print(board)
            print(model.evaluate(board))
            print()
        else:
            break
        
        fen = board.get_fen()
        stockfish.set_fen_position(fen)
        move = stockfish.get_best_move()
        print(move)
        print(stockfish.get_top_moves(4))
        if move:
            ri = int(move[1])-1
            fi = ord(move[0])-ord('a')
            rf = int(move[3])-1
            ff = ord(move[2])-ord('a')
            board = board.move(ri, fi, rf, ff)
            print()
            print("Turn:", board.turn)
            print("Move:", board.fullmove_number)
            print(board)
            print(model.evaluate(board))
            print()
        else:
            break
        
        

if __name__ == "__main__":
    run_training()
    #run_testing()
    #run_debugging()
    #print(cpu_count())
    #compare_against_stockfish(elo=200)