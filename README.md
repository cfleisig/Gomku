# Gomku
## Project Description
Implements a simple (and imperfect) AI engine for the game Gomoku using python.

## What is Gomoku
Gomoku is a two plyer game, where one player is claims the black (represented by 'b' in this program) stones and the other claimes the white stones (represented by 'w' in this program). The player who uses black stones always moves first, and the white stone player moves second. After that they take turns moving.

A player wins if they have placed five of their stones in a sequence, either horizontally, vertically or diagonally.

For a more detailed explanation of gomoku see [https://en.wikipedia.org/wiki/Gomoku](https://en.wikipedia.org/wiki/Gomoku) (I used the stadard variant).

## How the program works
The computer (which plays black stones) always moves first. After the first move, the user's and the computer's moves alternate. The computer determines its move by finding the move that maximises the return value of the score function.

The AI engine essentially determines which move will maximize its score on the board for that turn, by testing each possible move. It then plays the move which will give it a maximal score. 

## How to play
1. Run script in terminal to load functions
2. Enter function `play_gomoku(8)`, where 8 indicates that you wish to play on an 8 x 8 board. 

    A board will be printed into the terminal, with the computer's first move and the current score for both the white and black stones. 

3. Enter your move by entering the x and y coordinates of your desired move in terminal, as prompted.

    The comptuter will then automatically play its next move, and the board and scores will once again be printed accounting for both your new move and the computer's new move.
4. Keep entering new moves until the program declares that either you or the computer has won (or the game ended before anyone won)
5. Re-enter function `play_gomoku(8)` to play again if desired.

## Credits
Credit to Prof. Guerzhoy for assigning this project. 
