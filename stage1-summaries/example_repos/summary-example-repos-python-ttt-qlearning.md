<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | requirements.txt | `.txt` | ✅ |
| 3 | theory/tictactoe_qlearning.ipynb | `.ipynb` | ✅ |
| 4 | training/environment.py | `.py` | ✅ |
| 5 | training/q_learning_agent.py | `.py` | ✅ |
| 6 | training/train_qlearning.py | `.py` | ✅ |
| 7 | standalone/ttt_qlearning.py | `.py` | ✅ |
| 8 | oop_integration/README.md | `.md` | ✅ |
| 9 | oop_integration/q_learning_player.py | `.py` | ✅ |
| 10 | oop_integration/main.py | `.py` | ✅ |

# Content

## [Source: README.md]

The README frames this unit as a full reinforcement-learning extension of the Tic-Tac-Toe project. Unlike the minimax unit, which hard-codes optimal search, this one is about learning from repeated interaction.

Its project structure is intentionally modular:

- a theory notebook for explanation,
- shared training modules for environment and agent,
- a training script,
- a standalone playable interface,
- an adapter layer that integrates the learned agent into the OOP architecture.

The README also makes an operational point that matters for the code layout: scripts are meant to run as Python modules from the project root so that relative imports work correctly.

## [Source: requirements.txt]

The dependency file is notebook- and analysis-oriented rather than web- or deployment-oriented. It includes:

- `numpy` for numerical summaries,
- `matplotlib` and notebook-related packages for explanation and visualization,
- Jupyter stack packages for the theory notebook.

This aligns with the repo's teaching focus: the learner is expected to inspect, train, and analyze the agent rather than only execute a finished program.

## [Source: theory/tictactoe_qlearning.ipynb]

The theory notebook is the conceptual core of the unit. It maps Tic-Tac-Toe into the reinforcement-learning framework:

- the agent is the player being trained,
- the environment is the game board,
- the state is the board configuration,
- the action is selecting an available cell,
- the reward reflects win, loss, draw, and even per-move cost.

It then explains Q-learning as building a Q-table that estimates the quality of each action in each state, using the Bellman equation to update those estimates.

Several ideas are presented clearly and concretely:

- Q-values are learned expectations of future reward,
- epsilon-greedy behavior balances exploration and exploitation,
- the state space is large but manageable for Tic-Tac-Toe,
- per-move penalties encourage faster wins,
- training against only a random opponent creates strategic blind spots.

That last point is especially important: the notebook explains why the learned agent may still fail to block optimally in some positions. The issue is not that Q-learning is broken, but that the training distribution is weak and does not punish all mistakes consistently.

## [Source: training/environment.py]

`TicTacToeEnvironment` is the shared game environment for training and play. It encapsulates:

- board reset,
- available-action discovery,
- move application,
- winner detection,
- draw detection,
- game-over signaling,
- simple board display.

Conceptually, this file is the RL environment side of the agent-environment loop. It is deliberately simpler than the OOP `GameBoard` abstraction because its job is to support training mechanics, not present a broader software-design example.

## [Source: training/q_learning_agent.py]

`QLearningAgent` is the learning core.

It stores:

- symbol,
- learning rate,
- discount factor,
- epsilon,
- training/play mode,
- the Q-table,
- the current episode history.

Its key responsibilities are:

- convert board dictionaries into hashable state keys,
- retrieve and write Q-values,
- choose actions with epsilon-greedy policy,
- update Q-values using the Bellman equation,
- save and load learned Q-tables,
- report statistics about learned entries and states.

The `learn()` method is especially important because it handles both terminal and non-terminal updates with one interface. Terminal states set future value to zero; ongoing states use the maximum future Q-value over available actions.

## [Source: training/train_qlearning.py]

The training script operationalizes the learning process.

`play_training_game()` runs one episode between the agent and either a random opponent or another agent. It resets the environment, alternates turns, applies rewards, updates the Q-table after agent moves, and returns the result from the trained agent's perspective.

`train_agent()` then scales this up across many episodes by:

- initializing the agent,
- decaying epsilon over time,
- alternating who starts,
- tracking wins, losses, and draws,
- printing periodic training statistics,
- saving the final Q-table,
- running a final evaluation phase with exploration disabled.

This file turns the RL theory into a concrete experimental workflow and makes the hyperparameters explicit teaching objects rather than hidden constants.

## [Source: standalone/ttt_qlearning.py]

The standalone script wraps the shared environment in a directly playable CLI.

It subclasses `TicTacToeEnvironment` to add:

- terminal clearing,
- richer ASCII board rendering,
- validated human input,
- an interactive menu,
- optional human-first or agent-first play.

On startup it loads a pre-trained Q-table if available and reports agent statistics. If the table is missing, it warns the user and offers to continue with effectively random play.

This script is pedagogically useful because it turns the trained artifact into something inspectable: the learner can play against the agent and immediately feel both its strengths and its limitations.

## [Source: oop_integration/README.md]

The integration guide explains how the learned agent is adapted into the OOP architecture from the previous unit.

Its strongest architectural point is that Q-learning is added as a new AI strategy without rewriting the original OOP design. The guide explicitly frames `QLearningMachinePlayer` as an adapter that converts between:

- the `GameBoard` plus `Symbol` interface of the OOP game,
- the dictionary-plus-string interface expected by the Q-learning agent.

It also compares the resulting strategy choices: random, minimax, and learned Q-table play.

## [Source: oop_integration/q_learning_player.py]

`QLearningMachinePlayer` is the adapter layer described in the README.

It wraps a `QLearningAgent` in inference mode, optionally loads a saved Q-table, converts the OOP board object into the dictionary representation the agent expects, asks the agent to choose an action, and then writes that move back into the OOP board.

This file matters conceptually because it demonstrates that learned behavior can be integrated through interface adaptation rather than by changing the core game architecture.

## [Source: oop_integration/main.py]

The OOP integration entry point reuses the previous game architecture but swaps the machine-player implementation.

It imports the OOP board, human player, messages, and symbols from the sibling unit, then installs `QLearningMachinePlayer` as the AI participant. The resulting `TicTacToeGame` remains structurally similar to the OOP version: prompt for who starts, alternate turns, check for wins and draws, print the board.

The main difference is therefore strategic, not architectural: the opponent is no longer random or search-based, but policy-based through a learned Q-table.

# Cross-References

## RL concept to code mapping

- The theory notebook's agent-environment loop is implemented concretely by `QLearningAgent` interacting with `TicTacToeEnvironment` during the episode loop in `train_qlearning.py`. [Source: theory/tictactoe_qlearning.ipynb; Source: training/environment.py; Source: training/q_learning_agent.py; Source: training/train_qlearning.py]
- The Bellman-equation discussion in the notebook maps directly onto `QLearningAgent.learn()`, which updates the most recent state-action pair using reward plus discounted future value. [Source: theory/tictactoe_qlearning.ipynb; Source: training/q_learning_agent.py]
- The notebook's explanation of epsilon-greedy exploration is implemented in `choose_action()` through a training-mode random branch and a greedy branch over current Q-values. [Source: theory/tictactoe_qlearning.ipynb; Source: training/q_learning_agent.py]

## Training, evaluation, and limitations

- The README's training workflow and the notebook's explanation of exploration decay are operationalized in `train_agent()` through explicit epsilon decay, periodic reporting, checkpoint saving, and final greedy evaluation. [Source: README.md; Source: theory/tictactoe_qlearning.ipynb; Source: training/train_qlearning.py]
- The notebook's warning that a random training opponent creates defensive blind spots is consistent with the training script, which by default trains only against a random opponent. [Source: theory/tictactoe_qlearning.ipynb; Source: training/train_qlearning.py]
- The standalone script closes the loop from theory to experience by loading the learned Q-table and letting the user directly test the trained policy. [Source: standalone/ttt_qlearning.py; Source: README.md]

## Integration with the broader Tic-Tac-Toe project

- The q-learning unit depends on the earlier OOP unit conceptually, because its integration layer assumes the existence of `GameBoard`, `Symbol`, and the game-loop structure developed there. [Source: oop_integration/README.md; Source: oop_integration/q_learning_player.py; Source: oop_integration/main.py]
- `QLearningMachinePlayer` is the clearest bridge between the learning modules and the architecture modules: it translates board state from the OOP interface into the state encoding used by the RL agent. [Source: oop_integration/README.md; Source: oop_integration/q_learning_player.py]
- Compared with minimax, q-learning does not guarantee perfect play from the code alone; performance depends on the quality of the learned Q-table and the training regime that produced it. [Source: theory/tictactoe_qlearning.ipynb; Source: training/train_qlearning.py; Source: oop_integration/README.md]

## Decision criteria and trade-offs

- Use minimax when you need guaranteed optimal play in a small perfect-information game; use q-learning when the teaching goal is reinforcement learning, experimentation, and learned strategy rather than exact search. [Source: README.md; Source: theory/tictactoe_qlearning.ipynb]
- Keep the shared environment and agent modules separate from the standalone and OOP consumers so training logic stays reusable and duplication stays low. [Source: README.md; Source: training/environment.py; Source: training/q_learning_agent.py; Source: standalone/ttt_qlearning.py; Source: oop_integration/q_learning_player.py]
- Improve the learned policy by changing the training distribution, not just the play wrapper. The notebook and training script both imply that stronger opponents or self-play are the real path to better strategy. [Source: theory/tictactoe_qlearning.ipynb; Source: training/train_qlearning.py]
