<!-- markdownlint-disable MD024 MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | 01_intro_neural_networks.ipynb | `.ipynb` | ✅ |
| 3 | 02_pytorch_basics.ipynb | `.ipynb` | ✅ |
| 4 | 03_first_neural_network.ipynb | `.ipynb` | ✅ |
| 5 | 04_training_dynamics.ipynb | `.ipynb` | ✅ |
| 6 | complementary/gradient_descent_from_scratch.ipynb | `.ipynb` | ✅ |
| 7 | complementary/tf_playground_guide.ipynb | `.ipynb` | ✅ |
| 8 | complementary/xor_linearity.ipynb | `.ipynb` | ✅ |

# Content

## [Source: README.md]

### Learning path and module structure

The README frames the unit as an introduction to deep learning for programmers, with a practical implementation focus in PyTorch.

The main track is explicitly ordered:

- introduction to neural networks and deep learning,
- PyTorch basics,
- a first end-to-end neural-network project on FashionMNIST,
- training dynamics involving loss functions, optimizers, regularization, and scheduling.

The complementary material is not treated as peripheral trivia. Each notebook deepens one of the core conceptual bottlenecks of the main track:

- XOR and linear separability explain why linear models fail and why hidden layers matter,
- gradient descent from scratch explains optimization mechanics without autograd,
- the TensorFlow Playground guide turns abstract architecture and training choices into interactive experiments.

### Prerequisites

The prerequisites are concise but important: Python programming, basic linear algebra, and a working PyTorch installation. This positions the module as conceptually advanced but still grounded in standard programming tools.

## [Source: 01_intro_neural_networks.ipynb]

### Brief history of neural networks and deep learning

The notebook presents a historical arc from the first mathematical neuron model through the modern deep-learning era.

The early sequence includes McCulloch and Pitts, Rosenblatt's perceptron, the limitations identified by Minsky and Papert, the emergence of backpropagation, LeNet as an early CNN milestone, and LSTMs as a sequence-modeling breakthrough.

The deep-learning revolution from 2012 onward is attributed to four enabling factors:

- GPU computing power,
- Big Data availability,
- algorithmic advances such as Dropout, BatchNorm, and Adam,
- massive industrial investment.

The timeline then names AlexNet, GANs, ResNet, AlphaGo, the Transformer, BERT, GPT-3, ChatGPT, advanced reasoning models such as OpenAI o1, and DeepSeek-R1. The notebook's explicit claim is that all of these breakthroughs rely on neural networks.

### What a neural network is and how a perceptron works

A neural network is introduced as a function that learns from examples. Its basic building block is the perceptron, which computes a weighted sum of inputs plus a bias and then applies an activation function.

The perceptron is explained as a weighted vote with four ingredients:

- inputs as features,
- weights expressing importance,
- bias as a baseline output shift,
- activation as the function that shapes the result.

The notebook preserves a key equivalence: without an activation function, a perceptron is just linear regression.

### Linear separability and the XOR problem

The perceptron is limited to a single straight decision boundary. If the data are linearly separable, it works; if not, it fails.

The notebook uses AND, OR, and XOR to make this concrete. XOR is singled out as the smallest example of feature interaction, where one straight boundary is insufficient. The teaching point is broader than logic gates: many real tasks contain interaction patterns of this kind.

### Multilayer perceptrons and hidden representations

To solve problems like XOR, the notebook introduces multilayer perceptrons. Hidden layers are presented as learners of intermediate representations that a single perceptron cannot capture.

The notebook also stresses a mathematical caveat that becomes a recurring theme in the module: stacking linear layers without activations still collapses into a single linear transformation. The real power comes from alternating linear layers with non-linear activations.

### Activation functions and their roles

The notebook compares ReLU, Leaky ReLU, Sigmoid, Tanh, and Softmax in terms of formula, output range, and typical use.

Its rules of thumb are explicit:

- use ReLU by default in hidden layers,
- use sigmoid for binary outputs,
- use softmax for multiclass outputs,
- interpret the output activation as part of the model's contract because it determines what the numbers mean.

### Training overview: loss, gradient descent, and backpropagation

The notebook presents training as weight adjustment to reduce prediction error. It introduces loss functions as measures of how wrong the model is, then relates task type to common losses:

- MSE for regression,
- binary cross-entropy for binary classification,
- cross-entropy for multiclass classification.

Gradient descent is then described as walking downhill on the loss surface, with the learning rate controlling stability versus speed. Batch, stochastic, and mini-batch gradient descent are compared, with mini-batch training positioned as the practical default.

Backpropagation is explained as the mechanism that computes how each parameter should change. The notebook's mental model is clear:

1. the forward pass builds a computation graph,
2. the backward pass computes gradients,
3. the optimizer updates the parameters.

### The core training loop and architecture preview

The notebook gives the standard PyTorch training loop structure: forward pass, loss computation, zeroing gradients, backward pass, and optimizer step. It also distinguishes `train` mode from `eval` mode and explains why inference should disable gradient tracking.

Finally, it previews several architecture families: MLPs, CNNs, RNNs and LSTMs, Transformers, GANs, and autoencoders, while emphasizing that the module focuses on the shared foundations behind all of them.

### Code-demonstrated concepts

The notebook uses diagrams and code-backed illustrations to show:

- perceptron computation,
- XOR versus linearly separable problems,
- feature hierarchies inside MLPs,
- activation-function shape comparisons,
- gradient descent on a loss surface.

## [Source: 02_pytorch_basics.ipynb]

### The modern deep-learning framework ecosystem

The notebook situates PyTorch inside a wider ecosystem instead of treating it as the only framework that matters.

PyTorch is presented as the dominant framework for research and generative AI because of its Pythonic, dynamic-graph style and strong support for prototyping. TensorFlow is framed as an enterprise production framework with strong tooling for serving and deployment.

The notebook also introduces JAX as a high-performance research-oriented numerical framework and Keras 3 as a backend-agnostic high-level API that can run on PyTorch, TensorFlow, or JAX.

### Installation and hardware backends

The notebook explains that PyTorch installation depends on the available compute backend:

- CUDA for NVIDIA GPUs,
- ROCm for AMD GPUs on Linux,
- MPS for Apple Silicon,
- CPU-only execution everywhere, with slower performance.

This preserves an important practical point: deep-learning software choices are partly hardware choices.

### Tensors as the core PyTorch abstraction

Tensors are presented as multidimensional arrays similar to NumPy arrays but with two major additional powers:

- GPU acceleration,
- automatic differentiation.

The notebook maps different tensor dimensions to different data interpretations, including scalars, vectors, matrices, image tensors, and batches of images.

### GPU usage and device consistency

The notebook stresses that tensors must live on the same device before they can be combined. This is a common operational constraint that often causes beginner errors.

### Building models with `nn.Module`

`torch.nn.Module` is introduced as the base class for neural networks. The modeling recipe is explicit:

1. subclass `nn.Module`,
2. define layers in `__init__`,
3. define the data flow in `forward`.

The notebook also emphasizes that PyTorch automatically tracks parameters registered in the constructor.

### Functional style and `nn.Sequential`

The notebook compares two implementation styles:

- module objects such as defining activations as attributes,
- stateless functional calls through `torch.nn.functional`.

It then introduces `nn.Sequential` as a more compact option for simple feedforward architectures where layers are applied strictly one after another.

### Linear layers, datasets, and dataloaders

The notebook explains the matrix form of a linear layer and the shapes of its weights and biases.

It also introduces the `Dataset` and `DataLoader` abstractions, preserving their responsibilities and key parameters:

- `Dataset` stores or exposes indexed samples,
- `DataLoader` handles batching, shuffling, and parallel loading,
- `batch_size`, `shuffle`, and `num_workers` materially affect training behavior.

### Code-demonstrated concepts

The notebook uses code to demonstrate:

- tensor creation, operations, and indexing,
- moving tensors to GPU-like backends,
- building models through `nn.Module`, functional layers, and `nn.Sequential`,
- data feeding via datasets and dataloaders.

## [Source: 03_first_neural_network.ipynb]

### End-to-end FashionMNIST pipeline

The notebook is presented as a full classification pipeline rather than an isolated model-definition exercise. Its steps are explicit:

1. load and explore FashionMNIST,
2. preprocess the data,
3. define the network,
4. train it,
5. evaluate results,
6. save and reload the model,
7. use it for predictions.

FashionMNIST is chosen because it preserves the convenient structure of MNIST while being harder and therefore more realistic.

### Preprocessing and normalization

The notebook explains why image normalization matters. `ToTensor()` rescales pixel intensities to `[0, 1]`, but training benefits from inputs centered more closely around zero.

It preserves a useful practical distinction between two approaches:

- a simple symmetric normalization such as mean `0.5` and standard deviation `0.5`,
- dataset-specific precomputed statistics such as canonical MNIST values.

The notebook chooses hardcoded standard values instead of recomputing statistics each run, explicitly to reduce preprocessing overhead.

### DataLoaders and training/test handling

The notebook uses DataLoaders to batch and shuffle the data. It also preserves an important procedural rule:

- shuffle the training set to avoid learning sample order,
- do not shuffle the test set.

### Network architecture and the reasoning behind it

The network is a feedforward architecture with flattening, fully connected layers, ReLU activations, and dropout. The notebook explains not only the layer names but why that architecture is plausible:

- decreasing hidden-layer sizes create an information bottleneck,
- ReLU helps learn non-linear patterns without strong vanishing-gradient issues,
- dropout regularizes the model when parameter count is large relative to data size.

The notebook explicitly states that there is no magic formula for architecture design. Fixed constraints come from input and output dimensions, while hidden-layer sizes are empirical and often start from simple heuristics such as decreasing powers of two. The learner is encouraged to begin with small networks, then adjust for underfitting or overfitting.

### Loss, optimizer, result analysis, and model persistence

Cross-entropy loss is used as the standard loss for multiclass classification, with the important clarification that it expects raw logits and applies softmax internally for numerical stability.

Adam is introduced as a strong default optimizer.

The notebook also explains that PyTorch recommends saving only the state dictionary rather than the entire model object, because that is more robust against code changes.

A final practical note is preserved: the same pipeline can be reused for MNIST with minimal changes, and the expected accuracy will usually be higher because digits are easier than clothing items.

### Code-demonstrated concepts

The notebook uses code to demonstrate:

- dataset exploration for FashionMNIST,
- normalization and preprocessing,
- DataLoader-based batching,
- training and evaluation of a feedforward classifier,
- saving, loading, and reusing trained model weights.

## [Source: 04_training_dynamics.ipynb]

### The training landscape

The notebook frames training as navigation through a high-dimensional loss surface. It reduces the practical problem to three main control knobs:

- the loss function, which defines the objective,
- the optimizer, which determines how updates are made,
- regularization, which constrains the model so it does not memorize noise.

The demonstrations use the `make_moons` dataset because it is not linearly separable but is still easy to visualize.

### Loss functions and practical defaults

The notebook compares three task-appropriate losses:

- MSE for regression,
- BCEWithLogitsLoss for binary classification,
- CrossEntropyLoss for multiclass classification.

Its rule of thumb is explicit: for classification, use the `WithLogits` or cross-entropy variants and let PyTorch apply the corresponding squashing function internally to avoid numerical issues.

### Optimizers and their behavior

The notebook compares SGD, SGD with momentum, RMSprop, and Adam by intuition and use case.

Its practical recommendation is to start with `Adam(lr=1e-3)`, then consider SGD with momentum and a learning-rate schedule when trying to squeeze out final improvements.

### Overfitting and regularization

Overfitting is defined operationally: training loss continues dropping while validation loss starts increasing.

The notebook presents three defenses:

- weight decay or L2 regularization,
- dropout,
- early stopping.

The comparison between a baseline model and a regularized version preserves the intended observation: regularization narrows the gap between training and validation behavior.

### Learning-rate scheduling

The learning rate is described as the most impactful hyperparameter. The notebook preserves the main failure modes:

- too high leads to oscillation or divergence,
- too low makes training painfully slow.

It then compares StepLR, CosineAnnealingLR, and ReduceLROnPlateau as different scheduling strategies, with guidance about when each is useful.

### Summary defaults

The notebook ends with practical defaults:

- CrossEntropyLoss or BCEWithLogitsLoss depending on classification type,
- Adam as a starting optimizer,
- dropout plus small weight decay as regularization defaults,
- robust schedule choices such as ReduceLROnPlateau or CosineAnnealing,
- constant monitoring of training versus validation curves.

### Code-demonstrated concepts

The notebook uses code and plots to demonstrate:

- binary classification on `make_moons`,
- optimizer comparisons,
- baseline versus regularized training curves,
- scheduler effects on learning behavior.

## [Source: complementary/gradient_descent_from_scratch.ipynb]

### Why implement gradient descent manually

This notebook uses ADALINE as a deliberately simple model so that optimization can be studied without autograd. The goals are to expose the raw gradient-descent update rule, visualize the cost landscape in three dimensions, and compare the manual version with an equivalent PyTorch model.

### ADALINE and the AND dataset

ADALINE is presented as a linear neuron trained with MSE rather than with a hard threshold during training. Its closed-form gradient makes it ideal for understanding gradient descent mechanics.

The AND gate is chosen because it is linearly separable, which lets the notebook focus on optimization rather than representational limitations.

### Loss landscape and learning-rate intuition

The notebook visualizes the cost as a function of weights while holding the bias fixed. It uses that visualization to show gradient descent sliding down a convex valley toward the minimum.

The learning-rate lesson is preserved clearly:

- too large diverges,
- too small is slow,
- well-chosen values converge smoothly.

### Comparison with PyTorch autograd

The notebook's central comparison is that PyTorch reproduces the same optimization behavior without requiring manual gradient derivation. The key takeaway is not only that autograd is convenient, but that it preserves the same underlying optimization logic while removing symbolic differentiation from the developer's workload.

## [Source: complementary/tf_playground_guide.ipynb]

### TensorFlow Playground as an intuition-building tool

The notebook positions TensorFlow Playground as a live visual environment for configuring and observing small neural networks on synthetic two-dimensional datasets.

It explains the major controls:

- dataset choice,
- feature transformations,
- hidden layers,
- activation choice,
- learning rate,
- regularization,
- problem type,
- training control.

The decision boundary visualization is explicitly interpreted as part of the teaching tool: blue and orange regions show the model's class predictions, and line thickness reflects weight magnitude.

### Guided experiments and their lessons

The notebook walks through several experiments:

- one neuron on linearly separable data to show a single straight boundary,
- circle data with and without hidden layers to show why non-linearity is needed,
- XOR under different activations to show that linear activations fail while ReLU and Tanh succeed,
- manual feature engineering with `x₁ × x₂` to solve XOR without hidden layers,
- learning-rate comparisons to show slow, stable, or divergent training,
- regularization on a noisy spiral dataset to show how L2 smooths an overfit boundary.

The overall message is that visual experimentation can make abstract architectural and optimization choices intuitive before those same ideas are implemented in PyTorch.

## [Source: complementary/xor_linearity.ipynb]

### XOR as the simplest feature-interaction example

This notebook ties together XOR, linear separability, linear models, activations, and hidden layers. XOR is treated not as a toy for its own sake, but as the smallest example of the kind of feature interaction that appears in real tasks.

### Linear separability and the shared linear core of several models

The notebook explains that perceptron, linear regression, and logistic regression all begin from the same linear score `w_1 x_1 + w_2 x_2 + ... + b`. They differ only in what happens after that score and in the loss they optimize.

This allows the notebook to preserve a strong conceptual distinction: logistic regression is a better classifier than a perceptron, but it is still linear in the input features and therefore still fails on XOR.

### Feature engineering versus representation learning

The notebook compares two ways of escaping linear limitations:

- manually engineer interaction features such as `x₁ × x₂`,
- use hidden layers with non-linear activations so the network learns useful interactions automatically.

This comparison directly links classical feature engineering to deep learning's representation-learning viewpoint.

### Why activations matter and what universality means

The notebook repeats a central theme of the module: linear followed by linear is still linear. Hidden layers only become useful once non-linear activations are inserted between them.

It then states the Universal Approximation Theorem and preserves its practical interpretation:

- a one-hidden-layer network can approximate any continuous function in theory,
- this may require impractically many neurons,
- deeper networks are often more useful in practice,
- training remains the hard part.

### Code-demonstrated concepts

The notebook uses code and plots to demonstrate:

- failure of linear models on XOR,
- success through manual interaction features,
- success through a tiny MLP with non-linearity,
- the effect of hidden-layer size on ease of training.

# Cross-References

## Comparisons and distinctions

- Perceptron, linear regression, and logistic regression share the same linear-score core, but they differ in activation behavior, loss, and intended task. [Source: 01_intro_neural_networks.ipynb; Source: complementary/xor_linearity.ipynb]
- PyTorch and TensorFlow are presented as the two main deep-learning pillars, with PyTorch favored for research and generative AI and TensorFlow favored for enterprise production. [Source: 02_pytorch_basics.ipynb]
- Classical feature engineering for interactions is contrasted with deep learning's representation learning through hidden layers and non-linear activations. [Source: complementary/xor_linearity.ipynb; Source: complementary/tf_playground_guide.ipynb]
- Manual gradient descent on ADALINE and PyTorch autograd are contrasted as two ways of following the same optimization logic: one explicit, one automated. [Source: complementary/gradient_descent_from_scratch.ipynb]
- FashionMNIST classification turns the abstract ideas from the intro and PyTorch basics notebooks into a complete practical pipeline. [Source: 03_first_neural_network.ipynb]

## Dependencies and prerequisites

- The README defines the module's intended order, with the intro notebook feeding into PyTorch basics, then a first end-to-end model, then training dynamics. [Source: README.md]
- PyTorch basics is a prerequisite for the first FashionMNIST network because tensors, modules, and dataloaders are required before model training can be understood. [Source: 02_pytorch_basics.ipynb; Source: 03_first_neural_network.ipynb]
- The training-dynamics notebook builds directly on the intro notebook's presentation of loss, gradient descent, and backpropagation. [Source: 01_intro_neural_networks.ipynb; Source: 04_training_dynamics.ipynb]
- The gradient-descent-from-scratch notebook is a low-level optimization companion to the intro notebook's high-level explanation of training. [Source: 01_intro_neural_networks.ipynb; Source: complementary/gradient_descent_from_scratch.ipynb]
- The XOR and TensorFlow Playground notebooks deepen the intro notebook's explanation of linear separability, activation functions, and hidden layers. [Source: 01_intro_neural_networks.ipynb; Source: complementary/tf_playground_guide.ipynb; Source: complementary/xor_linearity.ipynb]

## Decision criteria and context-dependent choices

- Use ReLU by default in hidden layers, sigmoid for binary outputs, and softmax-style multiclass outputs when the task semantics require probabilities over classes. [Source: 01_intro_neural_networks.ipynb]
- Start with Adam around `1e-3` as a practical optimizer default, then move to SGD with momentum and scheduling when fine-tuning or squeezing extra performance matters. [Source: 04_training_dynamics.ipynb]
- Use dropout, weight decay, or early stopping when training and validation behavior diverge in a way that indicates overfitting. [Source: 03_first_neural_network.ipynb; Source: 04_training_dynamics.ipynb]
- Use manual feature engineering only when it is useful or easy to encode specific interactions; otherwise prefer non-linear models that can learn those interactions from data. [Source: complementary/xor_linearity.ipynb; Source: complementary/tf_playground_guide.ipynb]
- Save PyTorch state dictionaries rather than full model objects when robustness across code changes matters. [Source: 03_first_neural_network.ipynb]
