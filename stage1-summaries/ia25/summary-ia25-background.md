<!-- markdownlint-disable MD024 MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | 01_what_is_ai.md | `.md` | ✅ |
| 2 | 02_machine_learning_basics.md | `.md` | ✅ |
| 3 | 03_neural_networks_foundations.md | `.md` | ✅ |
| 4 | 04_generative_and_agentic_ai.md | `.md` | ✅ |

# Content

## [Source: 01_what_is_ai.md]

### Defining Intelligence: The Quest to Emulate the Human Mind

Artificial Intelligence is presented as a broad field of computer science focused on creating systems able to perform tasks that normally require human intelligence. The tasks named in the source include reasoning, learning, problem-solving, perception, language understanding, and creativity. The emphasis is not only on processing data, but on emulating cognition: building machines that can think, learn, and adapt in ways that are indistinguishable from, or even superior to, human capabilities.

### The Turing Test: A Benchmark for Intelligence

The file uses the Turing Test as a benchmark for intelligence. Alan Turing proposed it in 1950 as a way to evaluate whether a machine can exhibit behavior equivalent to, or indistinguishable from, human intelligence. The setup is a natural-language conversation between a human evaluator, a human participant, and a machine. If the evaluator cannot reliably distinguish the machine from the human, the machine is considered to have passed the test.

### A Brief History of AI

- 1956, Dartmouth Workshop: John McCarthy coined the term "Artificial Intelligence" at Dartmouth College. The workshop is described as the birth of AI as a scientific field and as a moment of strong optimism, with early researchers expecting human-level machine intelligence within a few decades.
- AI winters: AI history is described as a sequence of "AI summers" and "AI winters," where enthusiasm and funding were followed by stagnation and disappointment.
- Causes of AI winters:
  - Overblown promises: researchers underestimated how difficult tasks such as computer vision and natural language understanding really were.
  - Computational limits: the available hardware could not support the complexity of proposed models.
  - Combinatorial explosion: many early approaches depended on exploring huge search spaces, which quickly became computationally intractable.
- 2012 to present, the deep learning revolution: the current AI boom is tied to three combined factors:
  1. Big Data, meaning massive datasets for training complex models.
  2. Powerful hardware, especially GPUs, providing the parallel computation needed for deep learning.
  3. Algorithmic breakthroughs, including backpropagation and architectures such as AlexNet.

The source frames this period as a paradigm shift from rule-based AI systems toward machine learning systems that learn directly from data.

### Machine Learning vs. Artificial Intelligence

Machine Learning is described as a subfield of AI, even though the terms are often used interchangeably in practice. ML is easier to define because it focuses specifically on systems that learn from data, identify patterns, and make decisions with minimal human intervention.

The central contrast is explicit programming versus learning from examples. Instead of writing rules by hand, a machine learning model infers its own decision procedure from data. The source also stresses that more exposure to data generally improves the model.

Two classic definitions are included:

- Arthur Samuel, 1959: machine learning is the field that gives computers the ability to learn without being explicitly programmed.
- Tom Mitchell, 1997: a program learns from experience E with respect to tasks T and performance measure P if its performance at T, as measured by P, improves with experience E.

These definitions introduce three anchors for learning problems: the experience available, the task class, and the performance measure used to judge improvement.

### Deep Learning

Deep Learning is introduced as a specialized subfield of machine learning based on artificial neural networks with many layers. The reason for the term "deep" is the use of multiple layers. The file highlights that deep architectures can learn complex, hierarchical patterns from large amounts of data, which is why they enabled major progress in computer vision and natural language processing.

### The Spectrum of AI: From Narrow to General Intelligence

The material classifies AI systems by capability and level of consciousness.

### Weak AI (Narrow AI)

Weak AI, or Artificial Narrow Intelligence (ANI), refers to systems designed for a specific, well-defined task. This is presented as the kind of AI that exists today.

Key characteristics:

- Task-specific behavior: strong performance within one narrowly defined job.
- No consciousness or self-awareness: the system operates inside a predetermined scope and does not genuinely understand what it is doing.
- Data-driven performance: the quality and quantity of training data strongly affect results.

Examples given in the source:

- Voice assistants such as Siri, Alexa, and Google Assistant.
- Recommendation engines such as Netflix or Amazon recommenders.
- Self-driving cars, described as highly complex but still narrow because they are focused on driving.

### Strong AI (General AI or AGI)

Strong AI, or AGI, is described as a hypothetical machine intelligence able to understand, learn, and apply intelligence to any intellectual task that a human can do.

Its defining properties in the source are:

- Human-level cognition: reasoning, planning, learning from experience, abstract thought, and understanding complex ideas.
- Consciousness and self-awareness: presented as likely features of true AGI, though the source notes that this remains philosophically debated.
- Adaptability and transfer: the ability to move knowledge from one domain to another and learn new tasks without explicit reprogramming.

The file states clearly that AGI does not yet exist.

### Artificial Superintelligence (ASI)

ASI is described as a further hypothetical stage where AI exceeds human intelligence in essentially every domain, including scientific creativity, wisdom, and social skills. The file frames ASI mainly as a concept that raises major ethical and existential questions for humanity.

## [Source: 02_machine_learning_basics.md]

### Foundations

Machine learning is defined as a way for systems to learn from data, discover patterns, and make decisions with minimal human intervention. The file contrasts this with traditional programming, where explicit rules are designed by humans. In ML, the central object is the model, described as an abstract, articulated representation of reality.

The model is trained from data using a learning algorithm. During training, it adjusts itself to many examples and is later used to predict correct responses for new, unseen inputs. The file also explains that learning paradigms are classified by the kind of supervision or feedback they receive.

### Supervised Learning

Supervised learning is defined by the presence of labels with correct answers in the training data. The algorithm sees examples together with their target outputs and infers a model that can reproduce those answers for future inputs.

### Classification

Classification is given as a typical supervised task. The spam filter example is used to show the mechanism: the model examines many emails labeled "spam" or "not spam" and learns patterns such as words often associated with spam or senders that are trusted. The file stresses that more labeled examples improve performance.

Handwritten digit recognition is used as another example, where the model receives digit images and must assign each one to a class from 0 to 9.

The source distinguishes three classification settings:

- Binary classification: exactly two classes, such as spam versus not spam or positive versus negative.
- Multiclass classification: more than two possible classes, such as digit recognition or general image classification.
- Multilabel classification: one instance can receive several labels at once, such as assigning multiple music genres to the same item.

### Regression

Regression is the supervised case where the target is a continuous numerical value rather than a class. The file uses house-price prediction as the example and names typical input features such as number of rooms, garden size, and location. The important distinction is that each training example is paired with a number instead of a categorical label.

### Unsupervised Learning

Unsupervised learning is defined by the absence of labels. The goal is not to predict a known answer, but to discover hidden patterns or structure already present in the data.

### Clustering

Clustering groups data points according to similarity. Customer segmentation is the main example: customers are grouped into similar segments so products or services can be better tailored to them. The file points out that this is useful in recommendation systems and marketing.

### Association Rule Mining

The source distinguishes association rule mining from clustering. Clustering groups similar instances together, whereas association rule mining discovers relationships among items. The example is market basket analysis: finding that customers who buy bread also tend to buy butter.

### Dimensionality Reduction

Dimensionality reduction aims to reduce the number of features in a dataset. The motivation given is that high-dimensional data may contain redundant or irrelevant variables. Reducing dimensions can lower training time and improve model accuracy. Principal Component Analysis (PCA) is named as a common technique.

### Anomaly Detection

Anomaly detection focuses on finding unusual data points or patterns that differ strongly from the norm. The applications listed are fraud detection, system monitoring, and security. The important teaching point is that anomalies may indicate errors, attacks, or other abnormal situations worth investigation.

### Reinforcement Learning

Reinforcement learning is described as learning through interaction between an agent and an environment. The agent takes actions, the environment returns rewards or penalties, and the goal is to learn a policy: a strategy for choosing actions that maximizes cumulative reward over time.

The file uses robotics and games as examples, including teaching a robot to walk and training systems to play chess or Go. The core procedural idea is repeated clearly: action, feedback, and policy improvement over time.

## [Source: 03_neural_networks_foundations.md]

### Historical milestones

The file places neural networks in a historical sequence rather than treating them as an isolated technique.

### Early foundations (1943-2011)

- 1943: McCulloch and Pitts propose the first mathematical neuron model.
- 1958: Rosenblatt develops the Perceptron, described as the first implemented neural network.
- 1969: Minsky and Papert show the limitations of the simple perceptron in "Perceptrons," contributing to the AI winter.
- 1986: Hinton, Rumelhart, and Williams publish backpropagation, which enables training of multilayer neural networks.
- 1988: LeCun and collaborators introduce the first convolutional neural network for handwritten character recognition on MNIST.
- 1997: Hochreiter and Schmidhuber introduce LSTMs, crucial for sequential and time-series data.

### The AI Boom (2012-present)

The boom is attributed to four causes:

- Greater computing power, including GPUs and TPUs.
- Huge datasets enabled by the internet and Big Data.
- Advances in algorithms and network architectures.
- Much larger industrial investment and funding.

The file lists milestone systems and why they mattered:

- 2012: AlexNet lowers ImageNet top-5 error to 15.3% from 26%, showing the practical power of CNNs and marking the start of the modern boom.
- 2014: DeepFace reaches 97.35% accuracy in facial recognition, approaching human performance.
- 2014: GANs are introduced and transform content generation.
- 2015: ResNet introduces residual connections, enabling training of networks with more than 100 layers.
- 2016: AlphaGo defeats Lee Sedol using deep networks trained with supervised and reinforcement learning plus advanced Monte Carlo tree search.
- 2017: the Transformer appears in "Attention is all you need," reshaping language processing.
- 2018: BERT sets new natural language understanding records.
- 2020: GPT-3 shows emerging capabilities in large-scale language models.
- 2021: diffusion models begin to dominate realistic image generation.
- 2022: ChatGPT popularizes conversational assistants.
- 2023: GPT-4o and multimodal models expand text, image, audio, and video capabilities.
- 2024: the first models with advanced reasoning capabilities appear, represented here by OpenAI o1.
- 2025: DeepSeek-R1 lowers cost while approaching o1-level performance.

### The Perceptron: The Artificial Neuron

The perceptron is introduced as the fundamental neural-network unit and as a simplified analogue of a biological neuron. It is described as the simplest neural-network form and as the basis for later, more complex models.

### Structure of the Perceptron

The perceptron takes several inputs and produces one output. It computes a weighted combination of inputs and compares the result against a threshold. If the weighted sum exceeds that threshold, the perceptron "fires" and outputs 1; otherwise it outputs 0.

The source identifies five components:

1. Inputs representing data features.
2. Weights expressing how influential each input is.
3. Bias, which shifts the activation threshold and makes the model more flexible.
4. Weighted sum, obtained by multiplying inputs by weights and adding them.
5. Activation function, which decides whether the neuron activates; in a simple perceptron this is a step function.

### Limitations of the Simple Perceptron

The simple perceptron can solve only linearly separable problems. The file explains linear separability as the ability to separate classes with a single straight line. It can model simple logic such as AND and OR, but fails on XOR because XOR is not linearly separable. This specific limitation is presented as historically important because it contributed to reduced interest in neural networks.

### Multilayer Neural Networks (MLP)

Multilayer neural networks, or Multilayer Perceptrons, are presented as the response to the perceptron's limitations. By stacking layers of perceptrons, the network can represent much more complex patterns than a single linear separator can capture.

### Structure of a Multilayer Neural Network

The file divides the network into:

1. Input layer, which receives the raw data.
2. Hidden layers, which perform internal transformations and are responsible for learning non-linear relationships.
3. Output layer, which produces the final prediction, such as a class or a regression output.

### Why do we need hidden layers?

Hidden layers allow hierarchical feature learning. Earlier layers learn basic patterns, and later layers combine those patterns into more complex internal representations. The source treats this hierarchy as the key reason deep learning is powerful.

### Activation Functions

Activation functions are described as essential because they introduce non-linearity. Without them, a neural network would remain equivalent to a linear model no matter how many layers it had.

### Main Activation Functions

- Sigmoid: maps values into the range from 0 to 1 and is often used in binary-classification output layers.
- tanh: similar to sigmoid, but maps values into the range from -1 to 1.
- ReLU: outputs the input when positive and 0 otherwise. The source highlights two reasons for its importance: computational simplicity and partial mitigation of the vanishing-gradient problem.
- Softmax: used in multiclass output layers to transform raw scores into a probability distribution over classes.

### Training: Gradient Descent

Training is defined as finding weights and biases that minimize a loss function, where the loss measures the distance between predictions and correct values.

Gradient Descent is described as the most common optimization algorithm. The central idea is iterative parameter adjustment in the direction that lowers loss.

Key concepts:

- Gradient: the direction of steepest increase of the loss function, so minimization requires moving in the opposite direction.
- Learning rate: the step size used during optimization.

The file makes the trade-off explicit:

- If the learning rate is too high, the model may overshoot the optimum.
- If the learning rate is too low, training becomes very slow.

The training procedure is presented in four steps:

1. The model makes a prediction in the forward pass.
2. The loss is computed by comparing prediction and target.
3. The gradient of the loss with respect to each parameter is calculated.
4. Parameters are updated by taking a small step opposite the gradient.

### Backpropagation

Backpropagation is described as the method that makes efficient training of deep, multilayer networks possible and therefore underpins modern deep learning.

### How does it work?

The file breaks backpropagation into a sequence:

1. Forward pass: data moves from input through hidden layers to output.
2. Error calculation: the output is compared with the correct answer to obtain loss.
3. Backward pass: the error is propagated from output layer back toward the input, and the contribution of each weight and bias to the error is computed.
4. Weight update: parameters are adjusted according to that contribution, usually together with Gradient Descent.

The source identifies the chain rule from calculus as the mathematical basis that makes this efficient.

### Deep Learning

Deep learning is defined here as neural networks with many hidden layers that can learn representations at different levels of abstraction.

### Advantages of Deep Learning

- Automatic feature learning: unlike traditional ML, it reduces the need for manual feature engineering.
- Ability to model complex, non-linear relationships: this is especially important for unstructured data such as images, text, and sound.
- Transferability: knowledge from one task can be reused on another task through transfer learning, which is especially useful when data is limited.

### Popular Deep Learning Architectures

- CNNs: suited to grid-like data such as images and useful for spatial patterns like edges, textures, and shapes.
- RNNs and LSTM/GRU: designed for sequential data and able to keep memory of previous inputs.
- Transformers: modern sequence models based on attention; the file notes that BERT and GPT are built on this architecture.
- GANs: generator and discriminator compete to synthesize realistic data.
- Autoencoders: unsupervised models used for compression, dimensionality reduction, and anomaly detection.

## [Source: 04_generative_and_agentic_ai.md]

### The Generative AI Revolution

The source distinguishes traditional or predictive AI from generative AI. Predictive AI is framed as analyzing existing data to classify or predict, whereas generative AI creates new, original content. The file presents this as a shift from understanding the world to creating within it.

Generative models are described as learning the underlying patterns and structure of a dataset and then producing new artifacts that are similar to, but not copies of, the training data.

### Key Generative Architectures

Several architecture families are introduced as the drivers of the generative AI boom.

### 1. Generative Adversarial Networks (GANs)

GANs are described as two neural networks in competition:

- The Generator creates fake samples.
- The Discriminator tries to tell real samples from generated ones.

The educational core is the adversarial game: the generator improves by trying to fool the discriminator, while the discriminator improves by learning to detect fakes. The file attributes GANs' impact mainly to photorealistic image generation, including realistic faces and art.

### 2. Variational Autoencoders (VAEs)

VAEs are presented as a probabilistic extension of autoencoders. They compress data into a structured latent space and reconstruct it from that representation. Their generative ability comes from sampling points in that latent space.

The source highlights a distinctive property: smooth interpolation between data points, such as gradually morphing one face into another. Use cases listed are image generation, data augmentation, and anomaly detection.

### 3. Diffusion Models

Diffusion models are described procedurally. They first add noise to data step by step until the original signal becomes pure noise. Then they learn to reverse that process by gradually removing noise and recovering a clean sample from random input.

The file emphasizes that this reverse denoising process can be guided by text prompts or other conditions, producing detailed and specific images. Diffusion models are described as the state of the art in image generation and connected to systems such as DALL-E 2/3, Midjourney, and Stable Diffusion.

### 4. Transformers and Large Language Models (LLMs)

The Transformer is presented as the architecture that transformed sequential-data processing after the 2017 paper "Attention Is All You Need." Its key mechanism is self-attention, which lets the model weigh the importance of different words in a sequence.

Large Language Models are described as large Transformer systems trained on vast text corpora, often with billions of parameters. The file gives GPT as the representative example and explains the basic mechanism as next-token prediction: given previous text, the model predicts the most probable next unit, and repeated prediction yields long coherent text.

The impact listed includes chatbots, content creation, code generation, and scientific discovery. The file also frames LLMs as a major step toward more general AI.

### Practical LLM application patterns

The source lists practical design patterns for using LLMs:

- Prompting and system instructions: shaping behavior through roles, constraints, and few-shot examples.
- Function calling or tool use: constraining outputs to structured schemas such as JSON and invoking tools safely.
- Retrieval-Augmented Generation (RAG): adding retrieved context, especially from private data.
- Guardrails and validation: using schema validation, content filters, and safety checks.

### Retrieval-Augmented Generation (RAG)

RAG is presented as a way to reduce hallucinations and allow private knowledge to be used in generation by combining retrieval with generation.

The core pipeline is explicitly procedural:

1. Ingestion: chunk documents and clean or normalize text.
2. Embeddings: convert chunks into vectors using an embedding model.
3. Vector store: index those vectors in a similarity-search database.
4. Retrieval: for a query, retrieve the top-k relevant chunks and optionally re-rank them.
5. Synthesis: construct a prompt with the retrieved context and generate the answer.

The file also preserves important implementation caveats:

- Chunking strategy matters, including semantic splitting and overlap for context preservation.
- Retrieval should be evaluated with metrics such as precision@k and recall@k, and end-to-end QA should be evaluated for answer faithfulness and groundedness.
- Citations should be attached to source spans for verifiability.
- Caching and deduplication can reduce both cost and noise.

The source includes a minimal contract for a RAG QA task:

- Input: user query and optional filters or metadata.
- Output: answer text, sources with document and span identifiers, and confidence.
- Errors: empty corpus, no relevant chunks, and rate limits.

It also notes common vector-database capabilities such as HNSW or IVF indexes, metadata filters, hybrid sparse plus dense search, and persistence.

### The Rise of Agentic AI

Agentic AI is defined as a step beyond passive prompt-response systems. An AI agent is described as a system that can reason, plan, and execute tasks autonomously in order to achieve a goal.

### Core Components of an AI Agent

The file identifies four components:

1. An LLM as the "brain" and reasoning engine.
2. Planning, which breaks a high-level goal into smaller actions.
3. Tool use, giving the agent access to search, code execution, APIs, and other external capabilities.
4. Memory, allowing the agent to retain actions, observations, and reflections so it can adapt.

### How Agents Work: The ReAct Framework

The ReAct cycle is presented as a repeated loop:

1. Reason about the current state and the overall goal.
2. Choose an action.
3. Observe the result of that action.
4. Repeat, using the observation to guide the next reasoning step.

The educational point is that this loop lets the agent change its behavior dynamically as new information arrives, which makes it more flexible than a simple one-shot prompt-response system.

The file also mentions related patterns:

- Plan-and-Execute: separate high-level planning from low-level execution for long tasks.
- Toolformer-style self-invocation: let the model decide when to call tools.
- Deliberate reasoning: add an explicit thinking phase before acting.

### Model Context Protocol (MCP)

MCP is defined as an open protocol that standardizes how LLMs connect to tools, data sources, and actions.

Key ideas preserved in the source:

- Servers expose capabilities such as tools, prompts, and resources through typed contracts.
- Clients discover and invoke those capabilities.
- Benefits include tool portability across models, auditable interactions, and less glue code.

Typical components named in the file are a capability registry, an invocation channel with structured request/response behavior, and unified resource access.

Design advice given in the source:

- Keep tool IO schemas small and validated.
- Favor idempotent operations.
- Prefer stateless tools when possible.
- Log all tool calls for observability and safety audits.

### AI Gateways

An AI Gateway is described as an intermediate layer between an application and one or more model providers.

Core features listed:

- Routing and fallbacks across providers or models, including A/B tests and canaries.
- Observability for tracing, token and cost accounting, latency, and errors.
- Safety features such as content filtering, prompt redaction, and output validation.
- Policy controls including rate limits, quotas, and handling of personally identifiable information.
- Prompt and template management, caching, and response deduplication.

The file also gives the decision context for using one: it is particularly useful when multiple models or providers are involved, when cost/performance optimization matters, or when governance should be centralized.

### The Future is Agentic

The conclusion frames agentic AI as a shift from using AI as a passive tool to working with it as a collaborative partner. The source uses complex multi-step tasks such as trip planning, booking, scientific research, and software writing as examples of what increasingly capable agents may handle. The emphasis is on growing autonomy and on the possibility that agentic systems will redefine how people work and interact with technology.

# Cross-References

## Comparisons and distinctions

- AI, Machine Learning, and Deep Learning are presented as a hierarchy rather than as synonyms: AI is the broad field, ML is the subfield focused on learning from data, and Deep Learning is the ML subfield based on multilayer neural networks. [Source: 01_what_is_ai.md, 02_machine_learning_basics.md, 03_neural_networks_foundations.md]
- Weak AI, AGI, and ASI are distinguished by scope and capability: Weak AI is task-specific and current; AGI would generalize across human intellectual tasks; ASI would exceed humans in nearly every domain. [Source: 01_what_is_ai.md]
- Supervised, unsupervised, and reinforcement learning differ by the feedback signal available: labels, no labels, or rewards and penalties from interaction. [Source: 02_machine_learning_basics.md]
- Within supervised learning, classification predicts discrete labels while regression predicts continuous values. Within classification, binary, multiclass, and multilabel tasks differ by how many labels can be assigned. [Source: 02_machine_learning_basics.md]
- Clustering and association rule mining are explicitly separated: clustering groups similar instances, while association rule mining finds relationships among items. [Source: 02_machine_learning_basics.md]
- The simple perceptron and multilayer networks are contrasted by representational power: the perceptron handles only linearly separable problems, while hidden layers allow learning more complex non-linear structure. [Source: 03_neural_networks_foundations.md]
- Predictive AI and Generative AI are distinguished by their outputs: one analyzes existing data to predict or classify, the other produces new content from learned structure. [Source: 04_generative_and_agentic_ai.md]
- GANs, VAEs, diffusion models, and LLMs are presented as different generative strategies: adversarial competition, latent-space sampling, iterative denoising, and next-token prediction over sequences. [Source: 04_generative_and_agentic_ai.md]
- Agentic AI is contrasted with simple prompt-response systems by the presence of planning, tool use, memory, and iterative adaptation. [Source: 04_generative_and_agentic_ai.md]
- MCP and AI Gateways solve different coordination problems: MCP standardizes tool and resource connectivity, while AI Gateways centralize routing, observability, policy, and safety across model providers. [Source: 04_generative_and_agentic_ai.md]

## Dependencies and prerequisites

- The modern AI boom depends on the convergence of large datasets, stronger hardware, and algorithmic breakthroughs; these enabling conditions are stated both in the historical AI overview and in the neural-network timeline. [Source: 01_what_is_ai.md, 03_neural_networks_foundations.md]
- Deep Learning depends conceptually on neural-network structure, hidden layers, activation functions, gradient-based optimization, and backpropagation. [Source: 03_neural_networks_foundations.md]
- The explanation of backpropagation depends on the idea of a forward pass, a loss function, and gradient-based parameter updates. [Source: 03_neural_networks_foundations.md]
- LLMs depend on the Transformer architecture and its self-attention mechanism. [Source: 04_generative_and_agentic_ai.md]
- Agentic AI depends on an LLM core plus planning, tool use, and memory; ReAct makes those dependencies operational through repeated reasoning, action, and observation. [Source: 04_generative_and_agentic_ai.md]
- RAG depends on a multi-step pipeline from ingestion through embeddings, vector storage, retrieval, and synthesis. [Source: 04_generative_and_agentic_ai.md]
- Some deep-learning architectures are tied to particular data structures or tasks: CNNs to grid-like image data, RNNs/LSTMs to sequences, Transformers to sequence modeling with attention, and autoencoders to compression or anomaly-related unsupervised tasks. [Source: 03_neural_networks_foundations.md]

## Decision criteria and context-dependent choices

- Use supervised learning when correct labels are available and the goal is to infer a mapping from inputs to known outputs; use unsupervised learning when the goal is to discover structure without labels; use reinforcement learning when learning must come from interaction and reward feedback. [Source: 02_machine_learning_basics.md]
- Use classification when the target is categorical and regression when the target is continuous. [Source: 02_machine_learning_basics.md]
- Use dimensionality reduction when a dataset has many redundant or irrelevant features and the goal is to reduce training time or improve accuracy. [Source: 02_machine_learning_basics.md]
- The learning rate in Gradient Descent must balance speed and stability: too large overshoots, too small slows convergence. [Source: 03_neural_networks_foundations.md]
- Sigmoid is associated with binary-classification outputs, while Softmax is associated with multiclass outputs. [Source: 03_neural_networks_foundations.md]
- ReLU is preferred in modern deep learning partly because it is simple and helps mitigate vanishing gradients. [Source: 03_neural_networks_foundations.md]
- Use RAG when reducing hallucinations and incorporating private or retrieved knowledge are priorities; evaluate both retrieval quality and answer groundedness, and attach citations for verifiability. [Source: 04_generative_and_agentic_ai.md]
- Use an AI Gateway when multiple providers or models must be managed centrally, when governance and policy enforcement matter, or when routing and fallback strategies are needed. [Source: 04_generative_and_agentic_ai.md]
- MCP tool design should favor small validated schemas, idempotent operations, and stateless behavior where possible. [Source: 04_generative_and_agentic_ai.md]
