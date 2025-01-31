# Chessir

**Chessir** is a fork of [Chessnut](https://github.com/cgearhart/Chessnut), which is a chess board model written in Python that is intentionally simple.

Like Chessnut, **Chessir** is not written for speed, but it is about twenty times faster than Chessnut at generating valid chess moves from a given position on a chess board.

**Chessir** is not as simple as Chessnut: it has about 30% more lines of code.

**Chessir** is an alternative to Chessnut--it is faster, but a bit more complicated.

## What is the Same and what is Different from Chessnut

**Chessir** is used in much the same way as Chessnut. As with Chessnut, only the Game class needs to be imported. Methods and properties of Chessnut's Game class are available in **Chessir**, as described [below](#using-chessir).

**Chessir** creates a move list differently than Chessnut. Specifically, the differences relate to the evaluation of moves to exclude check for the active player, moves when the active player's king is in check, and how potential castling moves are evaluated.

**Chessir** will determine draws via three-fold repetition, insufficient material, and the 50-move rule, which Chessnut does not do.

## Installation

### PIP

`pip` is the easiest way to install **Chessir**. It can be installed directly from the [pypi](https://pypi.python.org/) [package](https://pypi.python.org/pypi/Chessir):

`pip install chessir`

### As a Module

**Chessir** can be a standalone module, so if you place the `Chessir` directory within your project folder, you don't need to install the package, you can just import the module as usual.

```
from Chessir import Game
```

## Testing

Unit tests can be run with the `pytest` package.

Additionally the [GitHub repository for **Chessir**](https://github.com/stuart-rickard/Chessir) includes scripts for comparing Chessir to Chessnut for both moves generated and for the speed at which moves are generated. These scripts are in the files `chessnut_moves_comparison.py` and `chessnut_speed_comparison.py`, respectively.

## Using Chessir

There are only two real classes in the **Chessir** package: `Board` and `Game`. `Board` is only used internally by `Game` to keep track of pieces and perform string formatting to and from [FEN notation](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation), so `Game` should be the only class you need to import. After installing the Chessir package, you can import and use it as you would expect:

```
from Chessir import Game

chessgame = Game()
print(chessgame)  # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
```

The `get_moves` method of Game will provide a List of valid moves:

```
print(chessgame.get_moves())
"""
['a2a3', 'a2a4', 'b2b3', 'b2b4', 'c2c3', 'c2c4', 'd2d3', 'd2d4', 'e2e3',
 'e2e4', 'f2f3', 'f2f4', 'g2g3', 'g2g4', 'h2h3', 'h2h4', 'b1c3', 'b1a3',
 'g1h3', 'g1f3']
"""
```

Note that **Chessir** uses simple algebraic notation, which has four characters identifying the starting and ending squares. In the case of castling, the starting and ending squares of the king are used (e.g., 'e1g1' for white kingside castle). In the case of a pawn promotion, a fifth character is provided to describe the type of promotion (e.g., 'e7e8q').

The `apply_moves` method will update the state of the chess game.

If the move could be invalid, the argument `validate=True` should be supplied. In this case, the method can be used in a `try-except` block, and it will raise an exception if the move is invalid.

```
chessgame.apply_move('e2e4')
print(chessgame)  # 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'

try:
    chessgame.apply_move('d8e4', validate=True)
except Exception as e:
    print(e) # 'Illegal move: d8e4'
```

The `reset` method updates the game state, either to the standard starting position or, if a FEN argument is supplied, to a specific state.

```
chessgame.reset()
print(chessgame)  # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

chessgame.reset('8/8/8/8/8/k7/7p/K7 b - - 1 40')
print(chessgame)  # '8/8/8/8/8/k7/7p/K7 b - - 1 40'

```

Game has a `status` property, which can be used to determine whether checkmate has been achieved. It also will detect check, stalemate, and draws due to three-fold repetition, insufficient material, and the 50-move rule. The statuses have values as follows: NORMAL = 0, CHECK = 1, CHECKMATE = 2, STALEMATE = 3, and DRAW = 4.

```
chessgame.reset('r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 b - - 1 23')
print(chessgame.status) # 2
print(chessgame.status == chessgame.CHECKMATE) # True

```

<!-- test -->
