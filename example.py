import stockfish
import chess

#starting FEN; guessed from position obtained by imaging software
start_fen = chess.guess_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", "w")
#new position after moving a pawn; obtained by imaging software
new_position = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR"
#new complete FEN with everything handled
new_fen = chess.get_new_fen(start_fen, new_position)
print(new_fen)

#once we have the new fen, we can pass it to stockfish
#we are passing the current board state, the depth we want stockfish to analyze and number of principle variations (different move options) we want to see.
print(stockfish.evaluate(new_fen, 15, 3))