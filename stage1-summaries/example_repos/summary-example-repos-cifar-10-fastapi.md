<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | requirements.txt | `.txt` | ✅ |
| 3 | main.py | `.py` | ✅ |
| 4 | models/cnn_model.py | `.py` | ✅ |
| 5 | utils/image_utils.py | `.py` | ✅ |
| 6 | utils/model_utils.py | `.py` | ✅ |
| 7 | templates/form.html | `.html` | ✅ |
| 8 | static/css/style.css | `.css` | ✅ |
| 9 | static/js/script.js | `.js` | ✅ |

# Content

## [Source: README.md]

The README frames the project as an educational FastAPI deployment of a CIFAR-10 image classifier. The focus is not just the model itself, but the full path from trained CNN to usable web application.

The user-facing flow is straightforward:

1. upload an image in the browser,
2. preprocess it to CIFAR-10 format,
3. run inference with the CNN,
4. return the predicted class and confidence through a rendered results page.

The README emphasizes separation of concerns across routing, model definition, preprocessing utilities, templates, styling, and client-side preview logic. It also points to a public cloud deployment, which makes the repo an example of model serving rather than only offline experimentation.

## [Source: requirements.txt]

The dependency set reflects that architecture directly:

- `fastapi`, `uvicorn`, `jinja2`, and `python-multipart` support the web application and file upload flow,
- `torch`, `torchvision`, and `pillow` support inference and image preprocessing,
- `requests` is included as a general HTTP helper dependency.

Unlike the Gradio sibling repo, this stack exposes more of the serving mechanics explicitly instead of delegating them to a higher-level UI framework.

## [Source: main.py]

`main.py` contains the entire application shell. It creates the FastAPI app, configures Jinja templates, mounts the static files directory, ensures `static/uploads` exists, and loads the trained model at startup from `models/cifar_net.pth`.

The route structure is intentionally small:

- `GET /` renders the upload form,
- `POST /predict/` receives an uploaded file, saves it with a UUID-based filename, preprocesses it, obtains a prediction, and rerenders the same template with the result and image path.

Several practical web-serving details are preserved here:

- uploaded files are stored server-side rather than kept only in memory,
- UUID naming avoids collisions,
- results are returned by server-side template rendering rather than a JSON API,
- the app is launched through `uvicorn` on `0.0.0.0:8000` when run directly.

This makes the repo a clear example of a simple monolithic inference web app rather than a pure backend API.

## [Source: models/cnn_model.py]

The CNN is defined as `ImprovedCNN`, using four convolutional layers with growing channel depth, batch normalization, pooling, dropout, and two fully connected layers ending in 10 logits.

The architecture follows the standard image-classification pattern:

- convolutional blocks extract spatial features,
- pooling reduces dimensionality,
- dropout regularizes both convolutional and dense stages,
- dense layers perform final classification.

The flattening step is explicit: the last convolutional representation is converted into a feature vector of size `128 * 4 * 4 = 2048`, then passed through a hidden layer of size `512` before the final 10-class output.

## [Source: utils/image_utils.py]

The preprocessing utility accepts either raw bytes or a valid file path, opens the image with PIL, and applies a fixed torchvision pipeline:

- resize to `32 x 32`,
- convert to tensor,
- normalize with CIFAR-10 channel statistics,
- add a batch dimension.

This file is important conceptually because it isolates input normalization from the web routes and makes the inference path reusable. It also makes explicit that deployment preprocessing must match training-time expectations.

## [Source: utils/model_utils.py]

`model_utils.py` owns the model-side serving helpers.

`load_model()` creates an `ImprovedCNN` instance, verifies the weight file exists, loads the state dict on CPU, and switches the network to evaluation mode.

`predict_image()` runs inference under `torch.no_grad()`, computes softmax probabilities, selects the highest-probability class, and returns a simple dictionary with:

- `prediction`,
- `confidence` as a percentage rounded to two decimals.

This utility is intentionally narrow: it exposes only top-1 prediction, unlike the Gradio sibling which returns a full probability distribution for top-3 display.

## [Source: templates/form.html]

The template implements a two-state interface in one file.

When there is no result, it shows:

- the upload form,
- file input restricted to images,
- a preview area that becomes visible after file selection.

When there is a result, it shows:

- the uploaded image,
- the original filename,
- the predicted CIFAR-10 class,
- the confidence score,
- a button to start over.

The template therefore couples upload and result display into a single server-rendered page rather than navigating between multiple views.

## [Source: static/css/style.css]

The stylesheet provides a lightweight educational UI rather than a design-heavy one. It centers the page, styles the form and result cards with simple shadows and rounded corners, and uses flex layout to place the uploaded image and classification result side by side when space allows.

This file matters mainly because it reinforces the server-rendered application story: the repo is not only about inference, but also about the minimal presentational layer needed to make the model usable.

## [Source: static/js/script.js]

The JavaScript is intentionally tiny. It defines a single `previewImage()` function that generates a browser-local preview from the selected file and reveals the hidden preview container.

Its role is pedagogically useful: it shows how a small amount of client-side interactivity can improve the UX without changing the core server-side inference flow.

# Cross-References

## Architecture and flow

- The README's upload-to-prediction workflow is implemented concretely through the combination of `main.py`, `utils/image_utils.py`, `utils/model_utils.py`, and `templates/form.html`. [Source: README.md; Source: main.py; Source: utils/image_utils.py; Source: utils/model_utils.py; Source: templates/form.html]
- The repo's separation-of-concerns claim is real in code: routing lives in `main.py`, preprocessing in `image_utils.py`, inference helpers in `model_utils.py`, model definition in `cnn_model.py`, and UI assets in `templates/` plus `static/`. [Source: README.md; Source: main.py; Source: models/cnn_model.py; Source: utils/image_utils.py; Source: utils/model_utils.py; Source: templates/form.html; Source: static/css/style.css; Source: static/js/script.js]
- The model is loaded once at startup and then reused per request, which is the simplest production-like serving pattern in the repo. [Source: main.py; Source: utils/model_utils.py]

## Comparisons with the Gradio sibling

- Both CIFAR-10 repos share essentially the same CNN architecture and preprocessing assumptions, but the FastAPI version exposes routing, uploads, templates, and static assets explicitly while the Gradio version delegates interface concerns to `gr.Interface`. [Source: models/cnn_model.py; Source: utils/image_utils.py; Source: README.md]
- The FastAPI app returns a top-1 prediction plus confidence on a rendered HTML page, whereas the Gradio variant is designed around a probability dictionary suitable for top-3 label display. [Source: utils/model_utils.py; Source: templates/form.html]

## Decision criteria and trade-offs

- Choose this repo when the teaching goal includes explicit web serving concerns such as routes, multipart uploads, server-side templates, and static assets. [Source: README.md; Source: main.py]
- Choose a higher-level UI framework when the goal is quick experimentation rather than exposing deployment mechanics. This repo is intentionally more verbose because those mechanics are part of the lesson. [Source: README.md; Source: templates/form.html; Source: static/js/script.js]
- Keep preprocessing and prediction helpers outside the route handlers so the serving code stays readable and the inference path can be tested or reused independently. [Source: main.py; Source: utils/image_utils.py; Source: utils/model_utils.py]
