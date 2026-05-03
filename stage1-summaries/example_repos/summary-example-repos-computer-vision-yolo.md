<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | yolo/object_detection_and_yolo.ipynb | `.ipynb` | ✅ |
| 2 | yolo/yolo_custom_training.ipynb | `.ipynb` | ✅ |

# Content

## [Source: yolo/object_detection_and_yolo.ipynb]

This notebook introduces object detection conceptually before using the YOLO API. That ordering matters: the notebook is not just a YOLO usage demo, but a compact theory-to-practice bridge for detection.

It first distinguishes three related tasks:

- classification, which predicts one label for an image,
- detection, which predicts multiple objects and their locations,
- segmentation, which predicts object masks rather than only boxes.

The notebook then develops the basic vocabulary of detection:

- bounding boxes in corner and center formats,
- normalized YOLO label coordinates,
- IoU as an overlap score,
- non-maximum suppression as duplicate removal,
- precision, recall, and mAP as detection metrics.

A major conceptual gain in the notebook is that IoU is shown to play two roles:

- evaluation against ground truth,
- post-processing among overlapping predictions.

The notebook also explains the one-stage versus two-stage detector split and situates YOLO historically as the fast, one-stage family. Its architectural description of backbone, neck, and detection head makes the Ultralytics model behavior easier to interpret later in the notebook.

From there the notebook becomes practical:

- load a pre-trained YOLO model,
- run inference on an image,
- inspect coordinate formats,
- filter detections by confidence, class, and IoU,
- process video with streaming inference,
- switch to segmentation or other Ultralytics task variants,
- compare model sizes for speed versus accuracy,
- export trained weights for deployment targets such as ONNX or TensorRT.

Overall, this notebook teaches that YOLO is not just a single model file but a broader detection workflow with post-processing, evaluation, and deployment considerations.

## [Source: yolo/yolo_custom_training.ipynb]

The second notebook moves from inference to fine-tuning on a custom dataset.

Its core conceptual distinction is between:

- transfer learning as the broad reuse of pre-trained knowledge,
- fine-tuning as the concrete act of continuing training from those pre-trained weights.

It then places full fine-tuning on a spectrum alongside feature extraction and partial freezing. The `freeze` parameter is used to explain how much of a network is allowed to adapt, and catastrophic forgetting is introduced as the risk of overwriting useful source-task knowledge too aggressively.

A strong methodological theme runs through the whole notebook: dataset inspection comes before model training. The notebook argues that many detector projects fail at the labeling and formatting layer, not at the architecture choice layer.

For that reason it emphasizes:

- understanding the YOLO directory and YAML structure,
- converting label numbers back into real pixel boxes,
- checking train and validation folders resolve correctly,
- visually confirming that annotations actually cover the intended objects.

The actual training example uses `coco8`, which the notebook correctly frames as a workflow demo rather than a serious domain-transfer benchmark. That caveat is important: the notebook teaches the mechanics of custom training without pretending that `coco8` is a realistic custom dataset.

Once training begins, the notebook teaches how to read the artifacts of a YOLO run:

- `box_loss`, `cls_loss`, and `dfl_loss`,
- precision and recall trends,
- `mAP50` versus `mAP50-95`,
- qualitative prediction inspection,
- troubleshooting when metrics remain low or predictions make no sense,
- export as the final handoff step after training and validation.

The notebook's strongest practical lesson is that label quality, split quality, and visual sanity checks are as important as model size or epoch count.

# Cross-References

## Conceptual progression across the unit

- The first notebook defines the language of detection, while the second notebook assumes that language and applies it to data inspection, training curves, and validation. [Source: yolo/object_detection_and_yolo.ipynb; Source: yolo/yolo_custom_training.ipynb]
- Bounding-box formats introduced in the detection notebook become operationally important in the custom-training notebook when normalized labels must be turned back into pixel rectangles for sanity checks. [Source: yolo/object_detection_and_yolo.ipynb; Source: yolo/yolo_custom_training.ipynb]
- The metric definitions in the first notebook are exactly the tools needed to read the training plots and validation results in the second notebook. [Source: yolo/object_detection_and_yolo.ipynb; Source: yolo/yolo_custom_training.ipynb]

## Engineering choices and deployment logic

- Confidence thresholds, IoU thresholds, and NMS are inference-time controls in the first notebook, while epoch count, image size, batch size, and freezing policy are training-time controls in the second. Together they define the full operational surface of a YOLO project. [Source: yolo/object_detection_and_yolo.ipynb; Source: yolo/yolo_custom_training.ipynb]
- The export discussion in the first notebook and the post-training export step in the second notebook reinforce the same deployment principle: the training framework and the deployment environment are often different, so model conversion is part of the workflow rather than an afterthought. [Source: yolo/object_detection_and_yolo.ipynb; Source: yolo/yolo_custom_training.ipynb]
- The detection notebook's speed-versus-accuracy model-size discussion is the practical complement to the training notebook's warning that tiny demos and real projects have very different compute and validation needs. [Source: yolo/object_detection_and_yolo.ipynb; Source: yolo/yolo_custom_training.ipynb]

## Decision criteria and trade-offs

- Use detection when object presence and location matter, and move to segmentation only when rectangular localization is no longer precise enough for the task. [Source: yolo/object_detection_and_yolo.ipynb]
- Use IoU not only as an evaluation threshold but also as a design knob in NMS; the same overlap concept drives both quality judgment and duplicate suppression. [Source: yolo/object_detection_and_yolo.ipynb]
- Prefer fine-tuning from pre-trained YOLO weights over training from scratch unless you have a large, well-labeled dataset and a strong reason to abandon transfer learning. [Source: yolo/yolo_custom_training.ipynb]
- Treat dataset inspection as mandatory. A smaller dataset with correct labels is usually more valuable than a larger one with annotation mistakes, and the notebook is explicit that visual sanity checks often decide whether a detector project succeeds. [Source: yolo/yolo_custom_training.ipynb]
- Interpret a large gap between `mAP50` and `mAP50-95` as evidence that the model finds objects but localizes them imprecisely. [Source: yolo/object_detection_and_yolo.ipynb; Source: yolo/yolo_custom_training.ipynb]
