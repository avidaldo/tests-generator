<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | 01_data_preparation.ipynb | `.ipynb` | ✅ |
| 2 | 02_metrics_deep_dive.ipynb | `.ipynb` | ✅ |
| 3 | 03_baseline_models.ipynb | `.ipynb` | ✅ |
| 4 | 04_xgboost.ipynb | `.ipynb` | ✅ |
| 5 | 05_neural_network.ipynb | `.ipynb` | ✅ |
| 6 | src/data_loader.py | `.py` | ✅ |
| 7 | src/metrics.py | `.py` | ✅ |
| 8 | src/preprocessing.py | `.py` | ✅ |
| 9 | src/visualization.py | `.py` | ✅ |

# Content

## [Source: 01_data_preparation.ipynb]

The first notebook defines the clinical framing, the ETL boundary, and the central data-quality issues of the thyroid project.

Its main themes are:

- simplify the original many-class diagnosis space into three clinically interpretable classes,
- separate ETL decisions from leakage-sensitive model preprocessing,
- analyze heavy class imbalance,
- inspect outliers, skewness, and missingness patterns,
- distinguish informative missingness from incidental missingness,
- motivate model-family-specific preprocessing choices.

This notebook is especially strong because it treats missing data as a domain question rather than a default imputation exercise. TBG is framed as a mostly missing test whose absence is itself informative, while other thyroid measurements are treated as more suitable for imputation.

## [Source: 02_metrics_deep_dive.ipynb]

The metrics notebook explains why ordinary accuracy is unusable in this medical-screening setting.

Its logic proceeds in three steps:

- show that a naive always-negative classifier can look strong under accuracy,
- explain why recall matters more than precision when false negatives are clinically costly,
- show why pure recall is still unsafe because it rewards trivial "predict sick for everyone" behavior.

The resulting solution is a macro $F_2$ score over only the two disease classes, which weights recall more than precision without making precision irrelevant.

This notebook therefore sets the optimization target for the rest of the project.

## [Source: 03_baseline_models.ipynb]

The baseline-models notebook establishes the first meaningful performance ladder.

It compares:

- logistic regression with explicit imputation and scaling,
- random forest with native missing-value handling.

The conceptual point is not just that the random forest performs better. It is why:

- non-linear structure matters,
- native NaN handling can preserve signal that imputation may blur,
- feature interactions are important in diagnosis,
- clinically relevant evaluation must focus on disease recall rather than overall accuracy.

By the end of this notebook, random forest becomes the benchmark that more complex models must justify exceeding.

## [Source: 04_xgboost.ipynb]

The XGBoost notebook explores whether gradient boosting can improve on the random-forest benchmark.

Its main lessons are:

- XGBoost is the practical gradient-boosting choice for tabular data because it is fast, regularized, and handles NaN natively,
- hyperparameter tuning can improve the model but does not by itself solve the minority-class problem,
- choosing an imbalance-aware scorer in cross-validation is not enough if the training objective inside each fold is still unweighted,
- class-weighted training via `sample_weight` is the correct way to make the model pay more attention to rare disease classes.

This notebook is particularly useful because it separates model-selection metrics from training objectives, which are often conflated.

## [Source: 05_neural_network.ipynb]

The neural-network notebook tests a PyTorch feed-forward model on the same clinical classification problem.

Its key design choices are:

- zero-imputation with explicit measurement flags so the network can learn missingness patterns,
- batch normalization, dropout, and ReLU activations,
- class-weighted cross-entropy to counter imbalance,
- explicit training loops with best-checkpoint restoration,
- both single-split and cross-validation-style evaluation.

The notebook's conceptual conclusion is restrained and useful: on structured datasets of this scale, neural networks require more setup and do not reliably outperform strong tree ensembles.

## [Source: src/data_loader.py]

This module centralizes the reproducible entry point for the dataset.

It:

- downloads the Kaggle thyroid dataset,
- maps the original diagnosis codes into three classes,
- drops non-predictive columns,
- optionally performs a stratified train/test split.

Its importance is that the notebooks do not each redefine the clinical target mapping for themselves; they all depend on one shared loading contract.

## [Source: src/metrics.py]

The metrics module implements the project's central evaluation idea in code.

`thyroid_disease_f2_score()` computes the macro $F_2$ score over only `hyperthyroid` and `hypothyroid`, and `thyroid_scorer` packages it for sklearn model-selection utilities.

This file is effectively the formal statement of the project's clinical objective.

## [Source: src/preprocessing.py]

This module is the implementation heart of the repository.

It defines three preprocessing strategies matched to different model families:

- simple imputation with scaling for linear models,
- native-NaN passthrough for tree models,
- zero-imputation with retained measurement flags for neural networks.

It also includes targeted transformations such as age outlier handling and log transformation of TSH.

Conceptually, this module encodes the repository's strongest idea: missing data should be handled differently depending on both the clinical meaning of the missingness and the capabilities of the downstream model.

## [Source: src/visualization.py]

The visualization helper provides class-conditioned histograms and KDE plots.

Its value is pedagogical: it supports the EDA claim that severe class imbalance can hide disease-class structure in raw counts, and that normalized density views are sometimes needed to compare class shapes fairly.

# Cross-References

## Internal progression of the thyroid unit

- `01_data_preparation` frames the biological problem and the missingness structure, `02_metrics_deep_dive` defines the evaluation objective, and `03` through `05` compare increasingly flexible model families under that same objective. [Source: 01_data_preparation.ipynb; Source: 02_metrics_deep_dive.ipynb; Source: 03_baseline_models.ipynb; Source: 04_xgboost.ipynb; Source: 05_neural_network.ipynb]
- The project therefore reads as a tightly controlled experiment: fix the clinical target and metric first, then test how different preprocessing and modeling choices behave under that fixed objective. [Source: 02_metrics_deep_dive.ipynb; Source: src/metrics.py]

## Notebook-to-module consolidation

- The target simplification and dataset-loading logic described in the first notebook are consolidated in `src/data_loader.py` so all later experiments use the same label space and feature drop rules. [Source: 01_data_preparation.ipynb; Source: src/data_loader.py]
- The clinical evaluation goal argued in the metrics notebook is formalized in `src/metrics.py` and reused throughout model selection. [Source: 02_metrics_deep_dive.ipynb; Source: src/metrics.py]
- The preprocessing choices motivated in the first notebook are turned into explicit model-family-specific pipelines in `src/preprocessing.py`. [Source: 01_data_preparation.ipynb; Source: src/preprocessing.py]
- The class-conditioned plots used in exploratory analysis are supported by `src/visualization.py`, which helps make imbalance and class separation visible. [Source: 01_data_preparation.ipynb; Source: src/visualization.py]

## Decision criteria and trade-offs

- Prefer a disease-focused macro $F_2$ score over accuracy when missing a sick patient is far worse than raising a false alarm, but avoid pure recall metrics that reward trivial overprediction. [Source: 02_metrics_deep_dive.ipynb; Source: src/metrics.py]
- Use different preprocessing strategies for different model families rather than forcing one universal pipeline when models differ in their ability to handle NaN, scaling, and missingness cues. [Source: 01_data_preparation.ipynb; Source: src/preprocessing.py]
- Treat informative missingness differently from incidental missingness; in this dataset, the fact that TBG was measured may be more informative than any imputed TBG value. [Source: 01_data_preparation.ipynb; Source: src/preprocessing.py]
- Prefer tree ensembles over more complex neural networks as the default tabular baseline unless the neural model demonstrates a clear empirical advantage. [Source: 03_baseline_models.ipynb; Source: 04_xgboost.ipynb; Source: 05_neural_network.ipynb]
- Change the training objective, not just the outer scorer, when class imbalance must affect how the model actually learns. [Source: 04_xgboost.ipynb; Source: 05_neural_network.ipynb]
