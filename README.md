# Chess
# Goal
This project is meant to serve as a backend for an AI chess bot which takes input data from a camera rather than a website.

## Motivation
Naturally, you cannot simply get the state of a chess board in Forsyth–Edwards Notation (FEN) from an image. Of course, if you had a bunch of images in a row and were able to get the board position each time, you would be able to construct the FEN yourself. 

## Implementation
The way this project works is very simple. You start off by guessing the initial FEN of a board. If you make this guess sooner to the start of the game, you will likely be correct. Then, as each move occurs, you manually update the FEN and pass the data to stockfish to find the best move. 

## Testing
I have tested this for every move in one of my own chess games and it was able to perfectly reconstruct the FEN given each move as a new board state.

## Example
