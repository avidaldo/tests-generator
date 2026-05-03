<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | assignment.md | `.md` | ✅ |
| 3 | ttt_v11_list_of_lists.py | `.py` | ✅ |
| 4 | ttt_v12_dict.py | `.py` | ✅ |

# Content

## [Source: README.md]

The README presents this folder as the first stage of a didactic Tic-Tac-Toe progression focused on Python fundamentals. The two implementations solve the same game requirements but use different board representations so the learner can compare data-structure choices directly.

The comparison is framed pedagogically:

- list of lists emphasizes nested lists and matrix-style indexing,
- dictionary representation emphasizes direct access through cell numbers,
- both versions keep the game simple and random rather than introducing AI.

This makes the folder less about game design and more about basic program structure, control flow, and data representation.

## [Source: assignment.md]

The assignment defines the game contract very explicitly.

- The machine plays `X` and always starts.
- The first machine move is always the center square.
- The human plays `O` by entering a square number from 1 to 9.
- Inputs must be numeric, in range, and point to an unoccupied cell.
- The machine move is random in this version; no AI is required.
- The program must keep checking for four states: continue, draw, human win, machine win.

The sample session also fixes the expected textual interaction style, including numbered empty cells and ASCII board rendering.

## [Source: ttt_v11_list_of_lists.py]

The first implementation follows the assignment closely using a `3 x 3` nested-list board filled with spaces.

Its main functions are small and direct:

- `display_board()` prints the board and shows either symbols or numbered cells,
- `cell_to_row_col()` maps user cell numbers to matrix coordinates,
- `enter_move()` validates input and writes the human move,
- `make_list_of_free_fields()` returns open coordinates,
- `victory_for()` checks rows, columns, and diagonals for a given sign,
- `draw_move()` handles the machine's first-center rule and later random moves.

This version is useful because it teaches how linear cell numbering can be translated into row-column coordinates and how matrix traversal works in practice.

One subtle design point is that draw detection is only checked immediately after the machine move, because the machine always goes first. The implementation therefore reasons about game flow, not just board state.

## [Source: ttt_v12_dict.py]

The second implementation reworks the same game around a dictionary keyed by the visible cell numbers `1` through `9`.

This representation changes the style of the program in several ways:

- no row-column conversion is needed,
- free-cell detection becomes a simple scan over numeric keys,
- winning combinations can be expressed directly as tuples of cell numbers,
- input validation can work in the same number system the user sees on screen.

The file also separates logic and UI more explicitly than the list-based version. It defines constants for player symbols and user-facing messages, logic helpers such as `is_taken_cell()`, `list_of_free_cells()`, `check_winner()`, and `machine_move()`, and then UI helpers like `display_board()` and `enter_move()`.

Compared with the first version, this one is cleaner structurally and more intuitive for beginners because the user-facing cell numbers are also the internal addresses.

# Cross-References

## Assignment to implementation mapping

- The assignment's fixed opening move in the center is implemented in both programs as a special first-move rule for the machine. [Source: assignment.md; Source: ttt_v11_list_of_lists.py; Source: ttt_v12_dict.py]
- The requirement that the machine play randomly after the opening move is also implemented in both versions, using random choice over currently free cells rather than any strategic search. [Source: assignment.md; Source: ttt_v11_list_of_lists.py; Source: ttt_v12_dict.py]
- The assignment's numbered-board interaction model is preserved in both implementations, but each one reaches it through a different internal representation. [Source: assignment.md; Source: ttt_v11_list_of_lists.py; Source: ttt_v12_dict.py]

## Representation trade-offs

- The list-of-lists version is better for learning matrix indexing and coordinate conversion, while the dictionary version is better for direct manipulation of numbered game cells. [Source: README.md; Source: ttt_v11_list_of_lists.py; Source: ttt_v12_dict.py]
- The dictionary version expresses winning patterns more cleanly through explicit cell tuples, whereas the matrix version makes row, column, and diagonal checks feel closer to the board geometry itself. [Source: ttt_v11_list_of_lists.py; Source: ttt_v12_dict.py]
- The second version has a clearer separation between logic and UI concerns through helper functions and string constants, which makes it a natural bridge to later refactorings in the broader Tic-Tac-Toe project. [Source: README.md; Source: ttt_v12_dict.py]

## Decision criteria and pedagogical use

- Use the list-based version when the learning goal is nested lists, coordinate mapping, and two-dimensional traversal. [Source: README.md; Source: ttt_v11_list_of_lists.py]
- Use the dictionary version when the learning goal is cleaner state access and more readable game logic in the same numbering scheme the user sees. [Source: README.md; Source: ttt_v12_dict.py]
- Keep the random machine policy at this stage because the educational objective is core Python structure, not search or game-playing intelligence. [Source: assignment.md; Source: README.md]
