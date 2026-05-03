<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | main.py | `.py` | ✅ |
| 3 | ttt_game.py | `.py` | ✅ |
| 4 | game_board.py | `.py` | ✅ |
| 5 | player.py | `.py` | ✅ |
| 6 | symbol.py | `.py` | ✅ |
| 7 | game_messages.py | `.py` | ✅ |

# Content

## [Source: README.md]

The README frames this folder as the architectural refactor of the Tic-Tac-Toe project: the game stops being a set of loose functions and becomes a small object-oriented system.

The main teaching goals are software-design oriented rather than algorithmic:

- encapsulate board state,
- define clear player abstractions,
- orchestrate game flow through a dedicated class,
- centralize symbols and messages,
- make it easy to add new AI strategies later.

The README explicitly names Strategy and Template Method patterns, and it positions the OOP version as the bridge from toy scripts to extensible application structure.

## [Source: main.py]

`main.py` is intentionally minimal. It imports `TicTacToeGame`, instantiates it, and calls `play()`.

This file exists mainly to preserve a clean entry point and keep orchestration logic out of the launch script.

## [Source: ttt_game.py]

`TicTacToeGame` is the coordinator of the application.

Its responsibilities are:

- create the board,
- ask for difficulty,
- ask who starts,
- instantiate the appropriate player objects,
- alternate turns,
- stop on win or draw.

The difficulty prompt returns a player class, not an instance. That is a small but meaningful design choice: the game does not need to know the internals of the AI strategy, only which concrete player type to instantiate for the AI symbol.

The game loop itself is concise because the class delegates behavior outward:

- board rules live in `GameBoard`,
- move logic lives in player objects,
- user-facing text lives in `GameMessages`.

## [Source: game_board.py]

`GameBoard` encapsulates the board state and core board rules behind a small API.

It stores the internal state as a dictionary from cells `1` through `9` to symbols or `None`, and exposes:

- `__getitem__` and `__setitem__` for board-style access,
- `is_cell_taken()`,
- `get_free_cells()`,
- `is_first_move()`,
- `is_board_full()`,
- `check_winner()`,
- `__str__()` for board rendering.

This is one of the clearest examples of encapsulation in the project: higher-level code no longer manipulates raw board dictionaries directly.

The board object also becomes the shared contract between all player strategies, which is why it is central to the later extensibility claims.

## [Source: player.py]

`player.py` implements the project's main abstraction hierarchy.

At the top is `Player`, an abstract base class that requires `make_move(board)`. From there the code branches into:

- `HumanPlayer`, which gets validated input from the user,
- `MachinePlayer`, which defines the template of selecting a move and then applying it,
- `RandomMachinePlayer`, which specializes `_select_move()` with random play,
- `MinimaxMachinePlayer`, which specializes `_select_move()` with recursive search.

This is where the README's pattern claims become concrete.

The Strategy pattern appears because the game can swap AI opponents without changing the game loop. The Template Method pattern appears because `MachinePlayer.make_move()` is fixed while subclasses only provide `_select_move()`.

The minimax implementation here is also better integrated architecturally than in the previous unit because it operates on `GameBoard` methods rather than loose helper functions.

## [Source: symbol.py]

`Symbol` is a small enum that names the human and AI symbols explicitly.

Its main value is not complexity but type clarity: the rest of the program can work with `Symbol.HUMAN` and `Symbol.AI` instead of passing raw strings everywhere.

The custom `__str__()` method keeps the board display simple by rendering enum values as their underlying character.

## [Source: game_messages.py]

`GameMessages` centralizes prompts, validation messages, and endgame messages.

This file matters conceptually because it turns text into configuration-like data rather than scattering strings through the codebase. The README is right to highlight maintainability and possible translation as benefits.

# Cross-References

## Architecture and responsibility boundaries

- The README's claim that each class has a single responsibility is reflected directly in the code split among `TicTacToeGame`, `GameBoard`, player classes, symbols, and message constants. [Source: README.md; Source: ttt_game.py; Source: game_board.py; Source: player.py; Source: symbol.py; Source: game_messages.py]
- `main.py` stays intentionally thin because the actual application boundary is `TicTacToeGame.play()`, not the launch script. [Source: main.py; Source: ttt_game.py]
- `GameBoard` is the shared domain object that lets both human and machine players interact with the same interface without knowing internal representation details. [Source: game_board.py; Source: player.py]

## Design patterns and evolution from earlier units

- The previous procedural implementations used free functions over raw state, while this unit turns the same concerns into explicit classes and interfaces. The gameplay is familiar, but the software structure is much more extensible. [Source: README.md; Source: ttt_game.py; Source: player.py; Source: game_board.py]
- The minimax strategy from the prior unit is now embedded as one concrete machine-player subclass, which demonstrates how algorithms can be inserted into a stable architecture rather than owning the whole program structure themselves. [Source: README.md; Source: player.py]
- The README's claim that future player types will be easy to add is believable because the AI choice in `ttt_game.py` is based on selecting a player class, not branching through algorithm-specific procedural code. [Source: README.md; Source: ttt_game.py; Source: player.py]

## Decision criteria and trade-offs

- Use this unit when the learning goal shifts from basic Python syntax or isolated algorithms to maintainability, extensibility, and clean interfaces. [Source: README.md]
- Use `RandomMachinePlayer` when simplicity or easy difficulty is desired; use `MinimaxMachinePlayer` when perfect play is required. [Source: ttt_game.py; Source: player.py; Source: game_messages.py]
- Centralize board rules and messages when you want localized changes with low coupling; this unit treats those concerns as first-class design decisions instead of incidental implementation details. [Source: README.md; Source: game_board.py; Source: game_messages.py]
