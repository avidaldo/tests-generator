<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | opencv/opencv_fundamentals.ipynb | `.ipynb` | ✅ |
| 2 | opencv/opencv_image_processing.ipynb | `.ipynb` | ✅ |
| 3 | opencv/opencv_video.ipynb | `.ipynb` | ✅ |

# Content

## [Source: opencv/opencv_fundamentals.ipynb]

This notebook introduces OpenCV as the main classical computer-vision toolkit and positions it as both a standalone image-processing library and a practical preprocessing layer for deep-learning workflows.

Several foundational ideas are made explicit early:

- OpenCV images are usually loaded in BGR order rather than RGB,
- images are arrays of `uint8` values in the range `0` to `255`,
- safe arithmetic usually requires converting to `float32`, applying operations, clipping, and converting back,
- image representation choices matter downstream when handing data to plotting libraries or neural networks.

The notebook then walks through basic image operations:

- color-space conversion,
- resizing with different interpolation methods,
- rotation and flipping,
- cropping,
- drawing shapes and text,
- saving images with practical format choices such as JPEG versus PNG.

One of the strongest conceptual links in the notebook is the bridge to convolutional neural networks. It explains that classical image filters and CNN layers share the same mathematical operation, but differ in where the kernels come from: hand-designed in OpenCV, learned from data in CNNs.

## [Source: opencv/opencv_image_processing.ipynb]

This notebook moves from basic manipulation to classical image-processing operators.

It begins with filtering and convolution, then compares the major blurring families:

- average blur for simple smoothing,
- Gaussian blur as the general-purpose default,
- median blur for salt-and-pepper noise,
- bilateral filtering for denoising while preserving edges.

The notebook then introduces edge detection through Sobel, Canny, and Laplacian, making a useful distinction between directional gradients and more general edge pipelines.

Thresholding is presented as the transition from grayscale imagery to binary structure, with three main strategies:

- fixed thresholding for controlled conditions,
- Otsu thresholding when a histogram-based split is appropriate,
- adaptive thresholding when illumination varies spatially.

From there the notebook develops morphology as shape manipulation on binary images using a structuring element. Erosion, dilation, opening, closing, and morphological gradients are framed not as abstract operators but as tools for shrinking, growing, cleaning, and outlining regions.

The later sections then connect binary structure to higher-level interpretation:

- contour detection groups edges into complete shapes,
- histogram equalization and CLAHE are presented as contrast-recovery tools,
- CLAHE is argued to be the more practical default under uneven lighting because it improves local detail without globally over-amplifying everything.

## [Source: opencv/opencv_video.ipynb]

The video notebook extends the same OpenCV logic from still images to temporal streams.

Its first core point is that `cv2.VideoCapture` provides one interface for very different sources:

- video files,
- webcams,
- network streams.

That makes the transition from offline examples to live acquisition conceptually simple.

The notebook then covers:

- frame-by-frame processing,
- applying filters over time,
- writing processed output with `VideoWriter`,
- codec choices and container implications,
- webcam capture constraints in interactive environments,
- background subtraction using learned scene models.

The background-subtraction discussion is especially useful because it turns parameters such as `history`, `varThreshold`, and `detectShadows` into interpretable design decisions instead of magic numbers. The notebook makes clear that sensitivity, adaptation speed, and shadow handling are trade-offs rather than fixed correct settings.

# Cross-References

## Internal progression across the unit

- The fundamentals notebook establishes image representation, color-space handling, and geometric transforms; the image-processing notebook then assumes that foundation and adds filtering, thresholding, and morphology on top of it. [Source: opencv/opencv_fundamentals.ipynb; Source: opencv/opencv_image_processing.ipynb]
- The video notebook is structurally an extension of the first two notebooks: everything done on a single image becomes a per-frame operation once the source is a stream instead of a file. [Source: opencv/opencv_fundamentals.ipynb; Source: opencv/opencv_image_processing.ipynb; Source: opencv/opencv_video.ipynb]
- The repeated connection to convolution links the OpenCV unit to later deep-learning material by showing that fixed filters and learned CNN kernels are operationally similar even though their training stories differ. [Source: opencv/opencv_fundamentals.ipynb; Source: opencv/opencv_image_processing.ipynb]

## Decision criteria and trade-offs

- Convert BGR to RGB whenever an OpenCV image is passed to plotting libraries or neural-network tooling that assumes RGB input. [Source: opencv/opencv_fundamentals.ipynb]
- Use `INTER_AREA` when downscaling, `INTER_LINEAR` as the everyday default, and `INTER_NEAREST` when preserving discrete labels or blocky pixel structure matters more than smooth appearance. [Source: opencv/opencv_fundamentals.ipynb]
- Prefer Gaussian blur as the general-purpose denoising default, median blur for impulse noise, and bilateral filtering when edge preservation is more important than speed. [Source: opencv/opencv_image_processing.ipynb]
- Prefer Canny as the standard edge detector unless directional gradient information is specifically needed from Sobel or second-derivative sensitivity is desired from Laplacian. [Source: opencv/opencv_image_processing.ipynb]
- Prefer CLAHE over global equalization when lighting varies across the image, because local contrast enhancement is usually more robust than a single global brightness remapping. [Source: opencv/opencv_image_processing.ipynb]
- Treat video codec choice and background-subtraction parameters as deployment decisions tied to environment, speed, and noise conditions rather than as fixed notebook defaults. [Source: opencv/opencv_video.ipynb]
