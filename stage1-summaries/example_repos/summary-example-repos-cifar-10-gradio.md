<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | requirements.txt | `.txt` | ✅ |
| 3 | app.py | `.py` | ✅ |
| 4 | models/cnn_model.py | `.py` | ✅ |

# Content

## [Source: README.md]

The README presents the project as a Hugging Face Gradio Space that classifies uploaded images into the 10 CIFAR-10 categories using a PyTorch CNN. It positions the repo as the Gradio counterpart to a separate FastAPI deployment of the same model.

The end-user flow is simple and explicit:

1. upload an image,
2. preprocess it to CIFAR-10 format,
3. run the CNN,
4. show the top-3 predicted classes with confidence scores.

The README also frames the core architectural difference versus the FastAPI version:

- `app.py` is the whole entry point,
- Gradio components replace manual routing and HTML forms,
- file handling is managed by Gradio rather than custom upload folders,
- output uses `gr.Label` rather than a server-rendered template.

Operationally, the README notes that model weights are not stored in the repo; they are downloaded at startup from a Hugging Face Model Hub repository.

## [Source: requirements.txt]

The dependency set is small and directly aligned with the app flow:

- `gradio` for the user interface,
- `torch` and `torchvision` for model definition and preprocessing,
- `pillow` for image handling,
- `huggingface-hub` for downloading model weights.

There is no extra web-framework or database dependency, which reinforces that the project is intentionally minimal and single-purpose.

## [Source: app.py]

The application file contains the entire serving workflow.

At startup it defines:

- the 10 CIFAR-10 class names,
- the Hugging Face repository ID containing the weights,
- the checkpoint filename.

The `load_model()` function downloads the checkpoint via `hf_hub_download()`, instantiates `ImprovedCNN`, loads the state dict on CPU, and switches the model to evaluation mode. The model is then loaded once globally at import time.

Image preprocessing is a fixed torchvision pipeline:

- resize to `32 x 32`,
- convert to tensor,
- normalize with CIFAR-10 mean and standard deviation,
- add a batch dimension.

The `predict()` function performs inference under `torch.no_grad()`, applies softmax to logits, and returns a `dict[str, float]` mapping class names to probabilities. That return shape is chosen specifically because it is the format expected by `gr.Label`.

The UI itself is a single `gr.Interface` declaration with:

- `gr.Image(type="pil")` input,
- `gr.Label(num_top_classes=3)` output,
- a title and description listing the 10 categories,
- disabled example caching and disabled flagging.

The module finally launches Gradio on `0.0.0.0:7860` when run as a script.

## [Source: models/cnn_model.py]

The CNN architecture is defined in a single module named `ImprovedCNN`.

The model uses four convolutional layers with increasing channel depth:

- `3 -> 32`,
- `32 -> 64`,
- `64 -> 128`,
- `128 -> 128`.

It combines these with:

- batch normalization after each convolution,
- max pooling to reduce spatial size,
- dropout at both convolutional and fully connected stages,
- two fully connected layers ending in 10 output logits.

The shape logic is explicit: after the convolution and pooling blocks, the flattened feature vector has size `128 * 4 * 4 = 2048`, which feeds a hidden layer of size `512` before the final classifier.

Conceptually, this file preserves the standard image-classification pattern of feature extraction through convolutions followed by dense classification layers, with dropout used as regularization.

# Cross-References

## Architecture and flow

- The README's four-step user workflow is implemented directly in `app.py`: upload, preprocess, infer, display top predictions. [Source: README.md; Source: app.py]
- The model-download note in the README corresponds to the explicit `hf_hub_download()` call in `load_model()`, which keeps weights out of the application repository. [Source: README.md; Source: app.py]
- The CNN described conceptually in the README is concretely supplied by `ImprovedCNN`, which `app.py` instantiates before loading weights. [Source: README.md; Source: app.py; Source: models/cnn_model.py]

## UI versus model responsibilities

- `app.py` owns interface construction, preprocessing, model loading, and prediction orchestration, while `models/cnn_model.py` owns only the neural-network architecture. [Source: app.py; Source: models/cnn_model.py]
- The project's "Gradio counterpart" identity is visible in the way `gr.Interface` replaces the routing/template stack used in the FastAPI sibling project. [Source: README.md; Source: app.py]

## Decision criteria and trade-offs

- Choose this repo when the goal is a fast interactive demo with minimal interface code; choose the FastAPI sibling when you need explicit routes, templates, and fuller server control. [Source: README.md]
- Keep weights on the Hugging Face Model Hub when the repo should stay lightweight and the deployment platform can fetch artifacts at startup. [Source: README.md; Source: app.py]
- Use a probability dictionary plus `gr.Label` when the teaching goal is top-class inspection rather than raw logits or custom plotting. [Source: README.md; Source: app.py]
