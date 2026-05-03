<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | MINIMAX_ALGORITHM.md | `.md` | ✅ |
| 3 | ttt_v13a_minimax.py | `.py` | ✅ |
| 4 | ttt_v13b_minimax.py | `.py` | ✅ |

# Content

## [Source: README.md]

The README presents this unit as the transition from basic random play to adversarial search. The claim is simple and strong: once minimax is implemented correctly for Tic-Tac-Toe, the machine becomes unbeatable.

It distinguishes two implementations of the same algorithmic idea:

- `v13a` as the more didactic version,
- `v13b` as the more efficient version.

The README repeatedly emphasizes that both versions make the same moves and differ only in clarity-versus-efficiency trade-offs. That framing is important because it teaches implementation design, not just the algorithm itself.

## [Source: MINIMAX_ALGORITHM.md]

The conceptual guide explains minimax as adversarial recursive search for two-player, zero-sum, perfect-information games.

Its core principles are:

- maximize your own guaranteed outcome,
- assume the opponent minimizes it,
- recurse through future game states,
- assign terminal states simple scores.

For Tic-Tac-Toe, the scoring convention is explicit:

- AI win: `+1`,
- human win: `-1`,
- draw: `0`.

The guide also gives historical context through von Neumann, Shannon, and early chess/checkers programs, which frames minimax as one of the foundational ideas in classical AI.

Pedagogically, the document makes minimax valuable for more than game playing. It teaches recursion, decision trees, backtracking, state evaluation, and the general idea of adversarial reasoning.

## [Source: ttt_v13a_minimax.py]

The educational implementation keeps the board as a dictionary keyed by cells `1` through `9`, continuing the representation introduced in the previous Tic-Tac-Toe stage.

Its defining design decision is that `minimax()` returns only a score, not a move. That keeps the recursive function conceptually simple:

- detect terminal states,
- recurse over all free cells,
- maximize when it is the AI turn,
- minimize when it is the human turn,
- undo the move after evaluating each branch.

Move selection is then handled by a separate `minimax_move()` function, which tries each legal AI move, calls `minimax()` on the resulting position, and keeps the move with the best score.

This separation makes the algorithm easier to explain because scoring and move choice are split into distinct responsibilities. The trade-off is extra work: the game tree is effectively re-explored while searching for the best move.

The file also extends the earlier basic game in two user-visible ways:

- the player can choose who starts,
- the machine can still be switched to a random level through `machine_move(level="random")`, which makes comparison with non-minimax play possible.

## [Source: ttt_v13b_minimax.py]

The optimized implementation keeps the same board representation, UI flow, and terminal-state logic, but changes the recursive contract.

Here `minimax()` returns a tuple of:

- best score,
- best move.

That means the recursion itself propagates both evaluation and action choice upward through the tree. As a result, `minimax_move()` becomes a thin wrapper that simply extracts the move from `minimax(board, True)`.

The conceptual consequence is important:

- `v13a` computes scores first and then derives the move externally,
- `v13b` computes score and move together in one pass.

This is the implementation the README describes as closer to production style. It is less repetitive and avoids a second top-level search over the move space, but it is slightly more abstract for a learner encountering recursion for the first time.

# Cross-References

## Algorithm to implementation mapping

- The conceptual guide's alternating maximizing and minimizing turns appears directly in both Python files through the `is_maximizing` parameter and the use of `max` versus `min` logic at recursive steps. [Source: MINIMAX_ALGORITHM.md; Source: ttt_v13a_minimax.py; Source: ttt_v13b_minimax.py]
- The guide's terminal-state scoring scheme of win, loss, and draw is implemented almost verbatim in both versions as `1`, `-1`, and `0`. [Source: MINIMAX_ALGORITHM.md; Source: ttt_v13a_minimax.py; Source: ttt_v13b_minimax.py]
- The README's statement that both versions are unbeatable is supported by the fact that both enumerate all legal future states and assume optimal opposing play. [Source: README.md; Source: MINIMAX_ALGORITHM.md; Source: ttt_v13a_minimax.py; Source: ttt_v13b_minimax.py]

## Representation and evolution from the previous unit

- Both minimax implementations keep the dictionary-based board model from the earlier basics stage, which means the new difficulty lies in search logic rather than in changing the state representation again. [Source: ttt_v13a_minimax.py; Source: ttt_v13b_minimax.py]
- The minimax unit therefore reads as an algorithmic upgrade on top of an already-familiar command-line game shell: input handling, board display, and winner checking remain recognizable while move selection becomes strategic. [Source: README.md; Source: ttt_v13a_minimax.py; Source: ttt_v13b_minimax.py]

## Decision criteria and trade-offs

- Use `v13a` when teaching recursion, game-tree evaluation, and single-responsibility function design, because its separation between `minimax()` and `minimax_move()` is easier to reason about. [Source: README.md; Source: ttt_v13a_minimax.py]
- Use `v13b` when you want the cleaner operational version that computes the optimal move in one recursive pass. [Source: README.md; Source: ttt_v13b_minimax.py]
- Keep both versions in the repository because the trade-off between clarity and efficiency is itself part of the lesson; this unit is about algorithm understanding and implementation design, not only about winning Tic-Tac-Toe. [Source: README.md; Source: MINIMAX_ALGORITHM.md]
