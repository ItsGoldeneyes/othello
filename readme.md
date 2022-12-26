# Othello Game + AI

This is a simple Othello game with an AI that uses the minimax algorithm with alpha-beta pruning.

## The Game

The game is played on an 8x8 board with two colours, black and white. Players take turns placing their pieces on the board. A piece can only be placed on an empty square if it is adjacent to an opponent's piece and there is a straight line of the player's pieces between the opponent's piece and the empty square. The player's pieces are then flipped to the player's colour. The game ends when there are no more empty squares or when neither player can make a move. The player with the most pieces on the board wins.

## The AI

The AI is a simple Minimax implementation with alpha-beta pruning. The AI uses simple heuristics to evaluate the board, including piece count, static weights for each position, the number of possible moves (mobility), and captured corners.

These heuristics are combined to give a score for each board state. The AI then uses the minimax algorithm to find the best move for the current player. The AI uses alpha-beta pruning as well as move ordering to speed up the search.

## Running the Game

The game can be run by running the `main.py` file located in the `/src/` directory. The game can be played against the AI or against another player, based on the function set in `main.py`.