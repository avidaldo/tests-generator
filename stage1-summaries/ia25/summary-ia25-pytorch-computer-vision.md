<!-- markdownlint-disable MD024 MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | 01_convolution_theory.ipynb | `.ipynb` | ✅ |
| 3 | 02_cnn_mnist.ipynb | `.ipynb` | ✅ |
| 4 | CIFAR-10/CIFAR-10.ipynb | `.ipynb` | ✅ |

# Content

## [Source: README.md]

### Learning path and progression

The README presents the unit as an introduction to convolutional neural networks for image processing and computer-vision tasks in PyTorch.

The sequence is explicitly progressive:

- first understand convolutional-network theory,
- then apply CNNs to MNIST,
- then move to CIFAR-10 as a more advanced color-image classification problem.

The CIFAR-10 notebook is described as introducing deeper architectures, optimization techniques, evaluation metrics, and the handling of three-channel images, which positions it as a substantial step up from MNIST.

### Production examples and prerequisites

The README connects the teaching notebooks to deployed applications. It explicitly states that the model from the CIFAR-10 notebook has production-facing derivatives deployed as a FastAPI and Docker service and as a Gradio interface on Hugging Face Spaces.

This matters because it shows the intended learning arc: theory, notebook experimentation, and then deployment.

The prerequisites are also explicit:

- completion of the deep-learning fundamentals module,
- familiarity with tensors, `nn.Module`, dataloaders, and the standard training loop,
- basic understanding of multidimensional arrays and image representation.

## [Source: 01_convolution_theory.ipynb]

### Why CNNs are needed for images

The notebook motivates CNNs by contrasting them with fully connected networks on images. A `224 × 224 × 3` image would already require 150,528 input values, and connecting that to a hidden layer of 1000 neurons would require around 150 million parameters.

The notebook argues that this is inefficient for two reasons:

- the parameter count becomes enormous,
- fully connected layers ignore the spatial structure of images.

CNNs solve this through three ideas:

- local connectivity,
- weight sharing,
- translation invariance.

### Convolutional layers and learned filters

The notebook explains a convolutional layer as a moving window or filter scanning local pixel neighborhoods for patterns. This preserves the crucial idea that nearby pixels form meaningful structures such as edges and textures, while distant pixels are usually less directly related.

It also compares classical computer vision with CNNs. In classical vision, filters such as edge detectors were hand-crafted. In CNNs, those filters are learned automatically through backpropagation. The notebook explicitly notes that the first layers of trained CNNs often end up discovering edge and color detectors on their own.

### Edge detection example

The notebook uses an edge-detection example to motivate why early convolutional filters matter. Abrupt intensity changes are treated as visually meaningful and as plausible building blocks for later classification.

### Convolution in PyTorch: filters, stride, padding, and output size

The notebook explains a two-dimensional convolutional layer through its practical parameters:

- number of filters or output channels,
- kernel size,
- stride,
- padding.

It preserves an important operational point: padding can compensate for border shrinkage and keep output sizes stable when desired.

The output-size formula is given explicitly, with clear intuitions:

- larger kernels typically shrink outputs,
- larger padding enlarges or preserves outputs,
- larger stride down-samples more aggressively.

It also notes that the operation is mathematically cross-correlation even though deep-learning libraries usually call it convolution.

### LeNet-style architecture and shape tracking

The notebook walks through a classic CNN architecture implemented with PyTorch. It explains the `N × C × H × W` tensor format, then tracks how convolutions, ReLU, and pooling change shapes layer by layer.

The key instructional point is that CNN design is partly about reasoning through tensor shapes correctly. The notebook explicitly warns that architectures designed for `32 × 32` inputs may need adaptation when the input size changes to `28 × 28`.

### Feature maps, pooling, and why max pooling helps

The notebook defines feature maps as the multiple output channels produced by a convolutional layer, each detecting a different kind of pattern.

Pooling is introduced as downsampling with several benefits:

- reducing computation,
- increasing translation invariance,
- selecting strong activations over noisy background,
- reducing overfitting pressure,
- expanding the effective receptive field of later layers.

### Code-demonstrated concepts

The notebook uses code and images to demonstrate:

- edge detection with a hand-crafted filter,
- the effect of padding and stride,
- convolutional shape changes across LeNet-like layers,
- max-pooling behavior.

## [Source: 02_cnn_mnist.ipynb]

### MNIST as a canonical CNN example

The notebook presents MNIST as a classic handwritten-digit dataset with 60,000 training images and 10,000 test images, each of size `28 × 28`. It preserves the historical significance of LeNet-5 and the low error rate achieved on this task.

The important teaching role of this notebook is that it turns convolutional-network theory into a first working image-classification pipeline.

### Dataset loading and preprocessing

The notebook explains that multiple preprocessing steps are often chained together, especially for images. It introduces `Compose` from `torchvision.transforms` as the mechanism for combining transformations such as normalization and resizing.

### Model definition, training, and evaluation

Although the notebook's markdown is brief in these sections, it makes the pipeline structure explicit:

- define the CNN,
- define the loss and optimizer,
- train the model,
- evaluate the model.

Adam is used as the optimizer and is described as an adaptive variant of stochastic gradient descent with parameter-specific learning rates.

### Code-demonstrated concepts

The notebook uses code to demonstrate:

- MNIST loading through PyTorch datasets,
- chained image transformations,
- CNN training for handwritten-digit classification,
- evaluation of the trained network on the test set.

## [Source: CIFAR-10/CIFAR-10.ipynb]

### Introduction and dataset complexity

The notebook introduces CIFAR-10 as a dataset of 60,000 color images of size `32 × 32` across 10 object classes. Compared with MNIST, this makes the task harder in several ways:

- the images are RGB rather than grayscale,
- the visual patterns are more varied,
- the target concepts are real-world objects rather than digits.

The notebook explicitly uses the official PyTorch CIFAR-10 tutorial as a baseline and then aims to improve on it.

### Environment setup and data preparation

The notebook includes a setup phase, then a data-loading and preparation phase, before model training begins. The practical point is that CIFAR-10 classification is not just about architecture; it also depends on careful dataset handling.

### Reusable training and validation functions

The notebook defines reusable training and evaluation functions so that multiple architectures can be compared consistently.

It contrasts two general methodologies:

- training completely and evaluating only at the end,
- evaluating after each epoch.

The notebook chooses per-epoch evaluation because it supports progress monitoring, early problem detection, early stopping logic, and model selection based on validation performance.

### Baseline behavior and overfitting

The notebook preserves a concrete overfitting signal: in the baseline model, training accuracy continues rising much faster than validation accuracy beginning around epoch 10.

This is then used to motivate improvement strategies such as regularization and dropout.

### Final model training, storage, and deployment

After selecting the improved architecture, the notebook retrains the final model on the full training data and stores it for deployment.

The deployment section is unusually important pedagogically because it connects the notebook to real model delivery. The notebook explains automated uploading to Hugging Face Hub and clearly states the authentication requirement: a write-enabled access token can be provided either through an environment variable in a `.env` file or through interactive notebook login.

### Code-demonstrated concepts

The notebook uses code and training curves to demonstrate:

- CIFAR-10 data loading and preprocessing,
- comparison of architectures through shared training and validation functions,
- detection of overfitting via train-versus-validation curves,
- retraining and storing the final model,
- deployment-oriented publication of the learned weights.

# Cross-References

## Comparisons and distinctions

- Fully connected image models treat pixels as independent inputs, while CNNs explicitly exploit local structure through filters, shared weights, and pooling. [Source: 01_convolution_theory.ipynb]
- MNIST is the simpler grayscale handwritten-digit benchmark, while CIFAR-10 is a more realistic color-image benchmark with greater visual complexity and stronger overfitting pressure. [Source: 02_cnn_mnist.ipynb; Source: CIFAR-10/CIFAR-10.ipynb]
- The CNN theory notebook emphasizes architectural concepts such as kernels, padding, stride, and pooling, whereas the MNIST and CIFAR notebooks emphasize training workflows and empirical behavior. [Source: 01_convolution_theory.ipynb; Source: 02_cnn_mnist.ipynb; Source: CIFAR-10/CIFAR-10.ipynb]
- The CIFAR-10 notebook pushes beyond teaching-only experimentation by tying the trained model to deployment paths such as FastAPI, Docker, Gradio, and Hugging Face Hub. [Source: README.md; Source: CIFAR-10/CIFAR-10.ipynb]

## Dependencies and prerequisites

- The README explicitly makes this unit depend on completion of the deep-learning fundamentals module, especially PyTorch tensors, `nn.Module`, dataloaders, and the standard training loop. [Source: README.md]
- Understanding kernels, stride, padding, and pooling in the theory notebook is a prerequisite for understanding why MNIST and CIFAR architectures have the shapes and parameter counts they do. [Source: 01_convolution_theory.ipynb; Source: 02_cnn_mnist.ipynb; Source: CIFAR-10/CIFAR-10.ipynb]
- The CIFAR-10 deployment examples depend on the prior steps of data preparation, architecture comparison, and model selection; deployment is positioned as the final step, not as a disconnected topic. [Source: README.md; Source: CIFAR-10/CIFAR-10.ipynb]

## Decision criteria and context-dependent choices

- Prefer CNNs over fully connected architectures for images because they preserve spatial structure while drastically reducing parameter count. [Source: 01_convolution_theory.ipynb]
- Use padding when preserving spatial size matters, and reason about output dimensions explicitly when changing kernel size or stride. [Source: 01_convolution_theory.ipynb]
- Use pooled feature maps when you need more robust and computationally manageable visual representations. [Source: 01_convolution_theory.ipynb]
- Evaluate after each epoch rather than only at the end when model comparison, overfitting detection, early stopping, or best-model selection matter. [Source: CIFAR-10/CIFAR-10.ipynb]
- Use regularization and dropout when the training and validation curves separate in the way the baseline CIFAR-10 run demonstrates. [Source: CIFAR-10/CIFAR-10.ipynb]
- Use an authenticated Hugging Face upload workflow when the goal is to distribute the trained model to downstream applications dynamically. [Source: README.md; Source: CIFAR-10/CIFAR-10.ipynb]
