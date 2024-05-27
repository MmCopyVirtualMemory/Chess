# Chess
## Goal
This project is meant to serve as a backend for an AI chess bot which takes input data from a camera rather than a website such as chess.com or lichess.org.

## Motivation
Naturally, you cannot simply get the state of a chess game from only a board position. This is where Forsyth–Edwards Notation (FEN) comes into play. A FEN can fully describe the state of a chess game. Here is a breakdown of the FEN.
```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
position(white=upper,black=lower) turn castling(k=kingside,q=queenside) enpassant(potential enpassant square if pawn moves two squares) halfmoves fullmoves
```
The most important parts of the FEN are the position, turn, castling and enpassant. Halfmoves and fullmoves rarely come into play but I still handle them properly.



in Forsyth–Edwards Notation (FEN) from an image. Of course, if you had a bunch of images in a row and were able to get the board position each time, you would be able to construct the FEN yourself. 

## Implementation
The way this project works is very simple. You start off by guessing the initial FEN of a board. If you make this guess sooner to the start of the game, you will likely be correct. Then, as each move occurs, you manually update the FEN and pass the data to stockfish to find the best move. 

## Testing
I have tested this for every move in one of my own chess games and it was able to perfectly reconstruct the FEN given each move as a new board state. It is possible I missed an edge case somewhere. Please open an issue with such edge case if you it.

## Example
#### Code
```py
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
```
#### Output
```
rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1
[['g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'c7c5', 'e2e3', 'c5d4', 'e3d4', 'f8e7', 'c1f4', 'b8c6'], ['e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'f8b4', 'd1a4', 'b8c6', 'e2e3', 'c8d7', 'f1d3'], ['d7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'c1g5', 'c7c5', 'c4d5', 'c5d4', 'd1d4', 'f8e7', 'e2e4', 'e6d5', 'g5f6', 'e7f6', 'd4d5', 'e8g8', 'd5d8', 'f8d8', 'f1c4', 'f6c3', 'b2c3']]
```
