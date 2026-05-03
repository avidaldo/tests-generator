<!-- markdownlint-disable MD024 MD025 MD032 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | qlearning.ipynb | `.ipynb` | ✅ |
| 2 | frozen_lake.ipynb | `.ipynb` | ✅ |
| 3 | bellman_equation.ipynb | `.ipynb` | ✅ |

# Content

## [Source: qlearning.ipynb]

### What is Reinforcement Learning?

Reinforcement learning is introduced as learning through trial and error. The notebook uses everyday analogies such as training a pet with treats, learning to ride a bike through practice, or improving at a video game by repeated play. The core idea is that an agent interacts with an environment, receives rewards, and gradually improves its behavior so that, from any state, it learns to choose the action that maximizes cumulative future reward.

The basic loop is presented as:
- The agent observes the current state.
- The agent chooses an action.
- The environment returns a reward and a new state.
- The agent learns from the transition `(state, action, reward, next state)` and repeats the cycle.

### Understanding Q-Learning Intuitively

Q-learning is explained as building a large cheat sheet called a Q-table. In that table:
- Rows correspond to the different states or situations the agent can encounter.
- Columns correspond to the actions the agent can take.
- Each value estimates how good that action is in that state in terms of expected future reward.

The learning process is described as repeatedly trying an action, observing reward and next state, updating the estimate for that action, and gradually improving the table. A key tension is exploration versus exploitation: the agent must sometimes try unknown actions, but it also needs to use the actions it already believes are best. The notebook states that, over time, good actions accumulate high Q-values and bad actions accumulate low Q-values.

### Environment

The notebook uses a custom 4x4 Grid World with these elements:
- Start state: `(0, 0)`.
- Goal state: `(3, 3)`, treated as a good state with reward `+10`.
- Trap state: `(2, 2)`, treated as a bad state with reward `-10`.
- Ordinary moves: reward `-0.1` per step to encourage shorter paths.
- Actions: up, down, left, right.

The coordinate layout is:
- Row 0: `(0,0)`, `(0,1)`, `(0,2)`, `(0,3)`.
- Row 1: `(1,0)`, `(1,1)`, `(1,2)`, `(1,3)`.
- Row 2: `(2,0)`, `(2,1)`, trap at `(2,2)`, `(2,3)`.
- Row 3: `(3,0)`, `(3,1)`, `(3,2)`, goal at `(3,3)`.

The code-demonstrated setup prints the same environment parameters explicitly: a `4x4` grid, start `(0, 0)`, goal `(3, 3)`, trap `(2, 2)`, and four actions represented as up, down, left, and right.

### The Agent's Brain (The Q-Table)

The Q-table is described as the agent's stored knowledge. In this notebook it is a three-dimensional structure where:
- The first dimension represents grid rows.
- The second dimension represents grid columns.
- The third dimension represents the available actions.

`Q(state, action)` is interpreted as the agent's prediction of the total future reward obtained by taking a particular action from a particular grid position. The notebook emphasizes that the table starts filled with zeros because the agent initially knows nothing. The code-demonstrated initialization confirms a table of shape `(4, 4, 4)` with all values equal to zero.

### The Learning Algorithm (Q-Learning)

The Q-value update is presented with the Bellman equation:

$Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$

The notebook explains the terms conceptually:
- `Q(s, a)` is the current estimate for the old state-action pair.
- `α` is the learning rate, which controls how much of the new information is incorporated each step.
- `r` is the reward just received.
- `γ` is the discount factor, which determines how much future reward matters relative to immediate reward.
- `max Q(s', a')` is the best future value available from the next state.
- The bracketed term is the temporal-difference error, meaning the difference between the new estimate and the old estimate.

The action-selection strategy is epsilon-greedy:
- With probability `1 - epsilon`, the agent exploits and chooses the best known action.
- With probability `epsilon`, it explores by trying a random action.

The stated purpose of epsilon-greedy is to prevent the agent from getting trapped in the first seemingly good path it discovers.

### Helper Functions

The helper logic demonstrates two core procedures:
- Action selection uses the epsilon-greedy rule, so the agent alternates between exploration and exploitation depending on the current exploration rate.
- State transition logic applies movement on the grid and handles wall collisions by forcing the agent to remain within grid boundaries. Reaching the goal ends the episode with reward `+10`, reaching the trap ends the episode with reward `-10`, and any other move gives the step penalty `-0.1` and continues the episode.

This means that the environment has two important edge cases:
- Moving into a wall does not leave the grid; the position is clamped back into the valid range.
- Goal and trap states are terminal and stop the episode immediately.

### The Training Loop

The notebook describes training as many episodes in which the agent starts from the start state and repeats the same four-step cycle:
1. Choose an action.
2. Apply the action and observe the next state, reward, and whether the episode ended.
3. Update the Q-table with the Bellman equation.
4. Move to the new state and continue until termination or until the step limit is reached.

The hyperparameters are:
- Learning rate `α = 0.1`.
- Discount factor `γ = 0.9`.
- Initial epsilon `1.0`.
- Maximum epsilon `1.0`.
- Minimum epsilon `0.01`.
- Epsilon decay rate `0.001`.
- Total episodes `10,000`.
- Maximum steps per episode `100`.

The notebook explicitly states that epsilon is decayed over time so the agent explores heavily early in training and exploits more as learning progresses. The printed milestones show that epsilon falls from `0.3746` at episode `1000` to `0.1441` at `2000`, `0.0593` at `3000`, `0.0282` at `4000`, `0.0167` at `5000`, `0.0125` at `6000`, `0.0109` at `7000`, `0.0103` at `8000`, `0.0101` at `9000`, and `0.0100` by episode `10000`.

### Results

The final Q-table is interpreted as a learned policy: for each grid cell, choose the action with the highest Q-value. The displayed table shows several concrete patterns:
- At the start state, the best values are for moving down or right, both about `5.49539`, while moving up or left is worse at about `4.845851`.
- At state `(1, 2)`, the action that would enter the trap has a value very close to `-10`, while the action leading toward the goal has a value around `7.91`.
- At state `(2, 3)`, the action leading directly to the goal has value `10`, while the action pointing toward the trap is strongly negative, about `-9.982`.
- The displayed rows for the trap state and the goal state are all zeros.

The learned policy is printed as arrows and special symbols:
- Top row: `↓  ↓  ↓  ↓`.
- Second row: `→  ↓  →  ↓`.
- Third row: `↓  ↓  🔥  ↓`.
- Bottom row: `→  →  →  🏆`.

The notebook states that successful training should produce a field of arrows pointing toward the goal and steering clear of the trap.

### Watch the Agent Play

The final demonstration runs the learned policy with no exploration. In the displayed run, the agent reaches the goal in `6` steps with total reward `9.5`. This result is consistent with taking several ordinary steps at `-0.1` each and then collecting the terminal reward `+10`. The notebook treats this as a direct visual confirmation that the learned policy follows an optimal route to the goal while avoiding the trap.

## [Source: frozen_lake.ipynb]

### What is Reinforcement Learning?

Reinforcement learning is defined here as a type of machine learning in which an agent learns to make decisions by interacting with an environment. The notebook identifies these components:
- Agent: the learner.
- Environment: the world being navigated.
- State: the current situation.
- Action: a move the agent can make.
- Reward: feedback from the environment.
- Policy: the strategy for choosing actions.

### Q-Learning Overview

Q-learning is described as:
- Model-free: it does not require prior knowledge of environment dynamics.
- Off-policy: the agent can learn the optimal policy while behaving according to another exploratory policy.
- Value-based: the method learns values for state-action pairs.

### The Process

The notebook presents Q-learning as a four-stage workflow.

Initialization:
- Create a Q-table of size `states × actions` filled with zeros.
- This means the agent starts with no knowledge.

Training loop:
- Start each episode at the initial state.
- Choose actions with an epsilon-greedy rule.
- Observe reward and next state.
- Update the Q-value with the Bellman equation.
- Repeat until the episode ends.
- Gradually reduce epsilon over time.

Evaluation:
- Test the learned policy with a greedy strategy and no exploration.
- Measure performance using average reward.

Deployment:
- Use the learned Q-table directly.
- In each state, choose the action with the highest Q-value.

The key insight stated by the notebook is that trial and error gradually turns the Q-table into a cheat sheet for navigating the environment optimally.

### FrozenLake Environment

FrozenLake is described as a task where the player must cross a frozen lake from start to goal without falling into holes. Important environment facts are:
- The player starts at `[0,0]`.
- In the `4x4` setting, the goal is at `[3,3]`.
- The episode ends when the player reaches the goal or falls into a hole.
- In slippery mode, the player may move perpendicular to the intended direction.
- Randomly generated maps are guaranteed to contain a path to the goal.

This notebook disables slipperiness by setting a deterministic environment. It uses the default `4x4` map whose layout is shown conceptually as:
- Row 0: Start, Frozen, Frozen, Frozen.
- Row 1: Frozen, Hole, Frozen, Hole.
- Row 2: Frozen, Frozen, Frozen, Hole.
- Row 3: Hole, Frozen, Frozen, Goal.

The notebook explains the symbols explicitly: `S` for Start, `F` for Frozen, `H` for Hole, and `G` for Goal.

### Observation Space

The observation space is `Discrete(16)`, meaning there are `16` possible states in the `4x4` map. The notebook explains that the environment encodes a position as `current_row * nrows + current_col`, with both indices starting at `0`. A concrete example is given for the goal position:
- Goal state index = `3 * 4 + 3 = 15`.

The state numbering is shown in row-major order:
- Top row: `0, 1, 2, 3`.
- Second row: `4, 5, 6, 7`.
- Third row: `8, 9, 10, 11`.
- Bottom row: `12, 13, 14, 15`.

### Action Space and Rewards

The action space is `Discrete(4)`, with the four actions defined as:
- `0`: go left.
- `1`: go down.
- `2`: go right.
- `3`: go up.

The reward function is sparse:
- Reach the goal: `+1`.
- Reach a hole: `0`.
- Reach an ordinary frozen tile: `0`.

The notebook therefore contrasts sharply with dense-reward examples: most moves provide no positive learning signal unless they eventually lead to the goal.

### Code-demonstrated Environment Interaction

One random-play demonstration runs several short episodes and visually shows the state transitions. The displayed example from the last shown episode ends after only `2` steps when the agent moves from state `4` to state `5` and receives reward `0`, illustrating that falling into a hole terminates the episode without positive reward.

The notebook also prints the size of the problem explicitly:
- `16` possible states.
- `4` possible actions.

### Understanding the Q-Table

The Q-table is described as a lookup table storing the expected reward for every state-action pair.

Its structure is:
- Rows: the `16` grid positions.
- Columns: the `4` available actions.
- Values: expected future reward for taking that action in that state.

Initialization starts every value at `0`. The notebook highlights a useful edge case: state `5` is a hole, so values such as `Q[5][right]` remain `0` because the hole is terminal and there are no useful actions from it. The agent must learn which actions eventually reach the goal and which states represent dead ends.

### Step 3: Define the Policies

The notebook frames policy design as the exploration-exploitation trade-off.

Greedy policy:
- Pure exploitation.
- Always choose the action with the highest Q-value.
- Intended for evaluation, when the goal is to measure what the agent has already learned.

Epsilon-greedy policy:
- With probability `1 - ε`, exploit the best known action.
- With probability `ε`, explore by taking a random action.
- Intended for training, because learning requires discovery of new paths.

The notebook also states that epsilon-greedy is a generalization of greedy policy because it includes greedy behavior in the exploitation branch.

### Hyperparameters Explained

The training and evaluation settings are justified in detail:
- Training episodes: `10,000`, so the agent gets many attempts to learn.
- Learning rate `α = 0.7`: high enough to learn relatively quickly, but still a partial update rather than a full replacement.
- Discount factor `γ = 0.95`: close to `1`, which is appropriate when future reward matters and the agent must plan ahead.
- Maximum steps per episode: `99`, used to prevent infinite loops.
- Maximum epsilon `1.0`: start with complete exploration because the agent initially knows nothing.
- Minimum epsilon `0.05`: keep some exploration even after learning, so the agent does not become completely rigid.
- Decay rate `0.0005`: controls the speed of the transition from exploration to exploitation.
- Evaluation episodes: `100`, giving a larger sample for performance measurement and better statistical confidence.

The notebook explicitly contrasts parameter regimes. A high learning rate learns faster but can overshoot stable values, while a low learning rate is slower but steadier. A gamma near `1` emphasizes future rewards, while a gamma near `0` makes the agent care mostly about immediate reward.

### Step 4: The Training Algorithm - Q-Learning

The Q-learning update rule is presented as the core of training. The notebook explains it term by term:
- `Q(s,a)`: current value estimate.
- `α`: learning rate, where `0` means no learning and `1` means fully adopting the new information.
- `R(s,a)`: immediate reward.
- `γ`: discount factor for future reward.
- `max Q(s',a')`: best value available from the next state.
- Temporal-difference error: the gap between the expected value based on new information and the current stored estimate.

The training structure is described as an outer loop over episodes and an inner loop over steps within an episode. In each episode, epsilon is reduced, the environment is reset, actions are chosen with epsilon-greedy behavior, rewards and next states are observed, the Q-table is updated, and the episode ends when the goal is reached, a hole is entered, or the step cap is reached.

### Training Complete

After training, the notebook expects the Q-table to contain meaningful values instead of zeros. It explains how to interpret them:
- High positive values indicate state-action pairs that tend to lead toward the goal.
- Low or zero values indicate poor choices, holes, or dead ends.
- Values represent expected cumulative discounted reward, not just immediate reward.

An example interpretation given by the notebook is that a Q-value around `0.5` can be read as meaning that the action has roughly a `50%` chance of eventually reaching the goal under the learned dynamics.

### Step 5: Evaluation

The notebook insists on a strict separation between training and evaluation.

During training:
- Exploration is still active.
- Observed performance does not necessarily reflect the true quality of the learned policy.

During evaluation:
- The agent uses greedy actions only.
- The result is intended to answer the question: what would the agent do if it relied only on what it has learned?

The evaluation procedure runs multiple greedy episodes, collects episode rewards, and reports the mean and standard deviation.

### Interpretation of Results

The printed evaluation result is `Mean_reward = 1.00 +/- 0.00`.

The notebook interprets this as:
- Mean reward `1.00`: the agent reaches the goal in `100%` of evaluation episodes.
- Standard deviation `0.00`: there is no observed variability; the policy behaves consistently.
- The policy is optimal for this deterministic environment.

The notebook also explains why this perfect result is expected in context:
- The environment is deterministic because slipperiness is disabled.
- `10,000` training episodes are enough for a simple `4x4` task.
- The learned Q-table has had enough experience to encode the optimal path from start to goal.

### Visualizing the Result

The last part of the notebook converts the learned policy into an animated replay. Conceptually, it resets the environment, follows the greedy policy from the start, renders each visited state, stores the frames, and combines them into a GIF at one frame per second. The purpose of this section is not to introduce new learning theory, but to give a visible confirmation of the path implied by the learned Q-table.

## [Source: bellman_equation.ipynb]

### Notebook Scope

This notebook is dedicated to the Bellman equation as the core update rule of Q-learning. It explicitly frames the Q-table as the agent's brain and uses a very small FrozenLake-inspired example so the update can be inspected numerically step by step.

### What is the Bellman Equation?

The Bellman equation is introduced as the rule for improving the estimated value of a state-action pair using newly observed information:

$Q(s, a) \leftarrow Q(s, a) + \alpha [r + \gamma \max_{a'} Q(s', a') - Q(s, a)]$

The notebook rewrites this in plain English as:
- New Q-value = old Q-value + learning rate × temporal-difference error.

Each term is explained conceptually:
- `Q(s, a)`: the old estimate for taking action `a` in state `s`.
- `α`: the learning rate. Small values mean slow, conservative updates; large values mean faster, stronger updates.
- `r`: the immediate reward from the action.
- `γ`: the discount factor. Values close to `1` make future reward important, while values close to `0` emphasize immediate reward.
- `max Q(s', a')`: the best value available from the next state.
- `r + γ max Q(s', a')`: the improved estimate formed from immediate reward plus discounted future potential.
- The bracketed difference from the old value: the temporal-difference error, interpreted as how surprising the new information is relative to the agent's previous belief.

### A Step-by-Step Example

The example environment is reduced to three states in a line:
- `S0`: Start.
- `S1`: Frozen intermediate state.
- `S2`: Goal.

There are only two actions, left and right. The reward structure is:
- `+1` for reaching the goal state `S2`.
- `0` for any other move.

The worked example fixes these hyperparameters:
- Learning rate `α = 0.1`.
- Discount factor `γ = 0.9`.

### Initial Q-Table

The initial Q-table is a `3 × 2` matrix of zeros because the agent begins with no information about which actions are good.

### Step 1: Agent Moves from S0 to S1

The first worked transition is:
- Current state: `S0`.
- Action: move right.
- Next state: `S1`.
- Immediate reward: `0`.

Because the next-state values are still all zero, the update leaves `Q(S0, right)` equal to `0`. The notebook stresses that this is common early in training: if the agent has not yet discovered a reward, the first few updates may appear to do nothing.

### Step 2: Agent Moves from S1 to S2 (The Goal)

The second transition is:
- Current state: `S1`.
- Action: move right.
- Next state: `S2`, which is the goal.
- Immediate reward: `+1`.

Since the goal is terminal, the best future value from `S2` is `0`. The update therefore changes `Q(S1, right)` from `0` to `0.1`. This is highlighted as the first meaningful learned value: moving right from `S1` is now known to be beneficial.

### Step 3: A New Episode - Agent Moves from S0 to S1 Again

The third worked transition repeats the move from `S0` to `S1`, still with immediate reward `0`. This time, however, the next state `S1` already has a learned value because `Q(S1, right) = 0.1`.

The update now increases `Q(S0, right)` from `0` to `0.009`. The notebook uses this to explain a central idea of Q-learning: reward information propagates backward through the state space. Even without receiving an immediate reward at `S0`, the agent learns that moving right from `S0` is valuable because it leads to a state with known positive future value.

### How the Update Looks in the Training Procedure

The notebook then maps the same numerical example back to the variables used in a training loop. The displayed values are:
- Old Q-value: `0.0`.
- Best future Q-value from `S1`: `0.1`.
- Temporal-difference error: `0.090`.
- New Q-value for `Q(S0, right)`: `0.009`.

This section is important because it connects the abstract equation to the concrete update steps performed during training.

### Conclusion

The notebook concludes that repeated Bellman updates over many episodes create a complete Q-table that predicts long-term reward for each state-action pair. The main qualitative claim is that reward values spread backward from the goal through the states that lead to it, gradually carving out the optimal path. It explicitly connects this miniature example to larger Q-learning notebooks by explaining that a full learned Q-table is simply the result of this same update process being repeated thousands of times.

# Cross-References

## Comparisons and distinctions

- `qlearning.ipynb` uses a custom `4x4` grid with dense rewards: `-0.1` per ordinary step, `+10` at the goal, and `-10` at the trap. `frozen_lake.ipynb` uses FrozenLake with sparse rewards: `+1` only for the goal and `0` for holes and ordinary frozen tiles. [Source: qlearning.ipynb §Environment] [Source: frozen_lake.ipynb §Action Space and Rewards]
- `frozen_lake.ipynb` separates training-time epsilon-greedy behavior from evaluation-time greedy behavior, while `qlearning.ipynb` emphasizes training followed by a single greedy demonstration of the learned policy. [Source: frozen_lake.ipynb §Step 3: Define the Policies] [Source: frozen_lake.ipynb §Step 5: Evaluation] [Source: qlearning.ipynb §Watch the Agent Play]
- `bellman_equation.ipynb` reduces the problem to a three-state chain so the Bellman update can be inspected numerically. `qlearning.ipynb` and `frozen_lake.ipynb` apply the same update rule to full environments with many more states and actions. [Source: bellman_equation.ipynb §A Step-by-Step Example] [Source: qlearning.ipynb §The Learning Algorithm (Q-Learning)] [Source: frozen_lake.ipynb §Step 4: The Training Algorithm - Q-Learning]
- `qlearning.ipynb` indexes the Q-table by row, column, and action because states are stored as grid coordinates. `frozen_lake.ipynb` uses a flattened integer state index from `0` to `15`, so the Q-table is described as a `16 × 4` lookup table. [Source: qlearning.ipynb §The Agent's Brain (The Q-Table)] [Source: frozen_lake.ipynb §Observation Space] [Source: frozen_lake.ipynb §Understanding the Q-Table]

## Dependencies and prerequisites

- Understanding the reinforcement-learning loop of state, action, reward, and next state is a prerequisite for understanding why a Q-table can store long-term action values. [Source: qlearning.ipynb §What is Reinforcement Learning?] [Source: frozen_lake.ipynb §What is Reinforcement Learning?]
- The Bellman equation explained in `bellman_equation.ipynb` is the mathematical basis for the Q-table updates performed in both `qlearning.ipynb` and `frozen_lake.ipynb`. [Source: bellman_equation.ipynb §What is the Bellman Equation?] [Source: qlearning.ipynb §The Learning Algorithm (Q-Learning)] [Source: frozen_lake.ipynb §Step 4: The Training Algorithm - Q-Learning]
- In `frozen_lake.ipynb`, interpreting Q-values depends on first understanding how the environment encodes positions as integers, including the row-major mapping and the example that the goal is state `15`. [Source: frozen_lake.ipynb §Observation Space] [Source: frozen_lake.ipynb §Understanding the Q-Table]
- The backward propagation described in `bellman_equation.ipynb` explains why `qlearning.ipynb` can learn a field of arrows that points toward the goal even from states that do not themselves immediately receive reward. [Source: bellman_equation.ipynb §Step 3: A New Episode - Agent Moves from S0 to S1 Again] [Source: qlearning.ipynb §Results]

## Decision criteria and context-dependent choices

- Both `qlearning.ipynb` and `frozen_lake.ipynb` choose high exploration at the start and lower exploration later because early discovery of the environment is necessary before stable exploitation becomes meaningful. [Source: qlearning.ipynb §The Training Loop] [Source: frozen_lake.ipynb §Hyperparameters Explained]
- All three notebooks treat `γ` as a choice about how much future reward matters. A gamma close to `1` is appropriate when the agent must value future outcomes and plan ahead, while a small gamma would make the agent focus on immediate reward. [Source: qlearning.ipynb §The Learning Algorithm (Q-Learning)] [Source: frozen_lake.ipynb §Hyperparameters Explained] [Source: bellman_equation.ipynb §What is the Bellman Equation?]
- `frozen_lake.ipynb` argues that evaluation should use greedy actions only, because exploration noise would hide the real quality of the learned policy. [Source: frozen_lake.ipynb §Step 3: Define the Policies] [Source: frozen_lake.ipynb §Step 5: Evaluation]
- `frozen_lake.ipynb` explains the perfect result `1.00 +/- 0.00` by combining three conditions: a deterministic environment, enough training episodes, and a small enough task. [Source: frozen_lake.ipynb §Interpretation of Results]
- `qlearning.ipynb` uses a step penalty to encourage shorter paths, while `frozen_lake.ipynb` uses zero reward for ordinary movement and therefore depends more heavily on eventual success versus failure to shape learning. [Source: qlearning.ipynb §Environment] [Source: frozen_lake.ipynb §Action Space and Rewards]
