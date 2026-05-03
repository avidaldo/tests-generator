<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | e2e050_pipelines.ipynb | `.ipynb` | ✅ |
| 2 | e2e051_custom_transformers.ipynb | `.ipynb` | ✅ |
| 3 | e2e060_spatial_clustering.ipynb | `.ipynb` | ✅ |
| 4 | e2e070_model_evaluation.ipynb | `.ipynb` | ✅ |
| 5 | e2e080_hyperparameters.ipynb | `.ipynb` | ✅ |
| 6 | e2e081_hyperparameters2.ipynb | `.ipynb` | ✅ |
| 7 | e2e090_neural_network.ipynb | `.ipynb` | ✅ |
| 8 | utils/load_california.py | `.py` | ✅ |
| 9 | utils/housing_preprocessing.py | `.py` | ✅ |
| 10 | utils/training_utils.py | `.py` | ✅ |

# Content

## [Source: e2e050_pipelines.ipynb]

This notebook turns the earlier preprocessing ideas into reusable scikit-learn pipelines.

Its main conceptual moves are:

- treat preprocessing as an explicit sequence of estimators,
- separate numeric and categorical processing,
- use `ColumnTransformer` to route columns through the correct transformations,
- preserve fit/transform discipline so the same learned preprocessing can be applied later to unseen data.

The notebook therefore marks the transition from isolated preprocessing techniques to pipeline engineering.

## [Source: e2e051_custom_transformers.ipynb]

The custom-transformers notebook handles the transformations that are specific to this housing problem and not built directly into scikit-learn.

It presents two patterns:

- simple stateless transformations wrapped with `FunctionTransformer`,
- class-based transformers with `fit` and `transform` methods when some learned state is needed.

Pedagogically, this notebook answers the question raised in the first-half feature-engineering section: how do custom ratios and nonstandard transformations become first-class members of a pipeline?

## [Source: e2e060_spatial_clustering.ipynb]

This notebook addresses the fact that latitude and longitude are not very informative as raw linear features.

Its solution is conceptual rather than purely geometric:

- cluster districts into geographic regions,
- represent proximity to those regions,
- use an RBF kernel to convert geographic distance into graded similarity features.

This is important because it reframes geolocation from a pair of coordinates into a learned notion of neighborhood similarity, which is more compatible with downstream regression.

## [Source: e2e070_model_evaluation.ipynb]

The model-evaluation notebook begins actual supervised modeling with the shared preprocessing pipeline already in place.

Its main contributions are:

- define a complete preprocessing-plus-model pipeline,
- compare linear regression, decision tree, and random forest baselines,
- explain why using the test set for model comparison is leakage,
- introduce a validation set and then cross-validation as safer model-selection mechanisms,
- interpret RMSE not just as a score but as a practical prediction error in dollars.

Conceptually, this is the notebook where the project stops being about feature preparation and becomes about evidence-based model choice.

## [Source: e2e080_hyperparameters.ipynb]

The first hyperparameter-tuning notebook introduces systematic search over model and preprocessing settings.

It contrasts:

- grid search, which exhaustively checks a defined set of combinations,
- randomized search, which samples the search space under a fixed computational budget.

It also brings up an important engineering trade-off around parallelism: if both the outer search and the inner model training parallelize aggressively, the total compute demand can explode.

This notebook therefore broadens the project from model comparison to search-strategy design.

## [Source: e2e081_hyperparameters2.ipynb]

The second hyperparameter notebook refines the tuning process by organizing it into successive search iterations.

Instead of a single coarse sweep, it treats tuning as iterative narrowing:

- start with broad randomized exploration,
- inspect the best-performing regions,
- fix or narrow converged dimensions,
- rerun search in a more focused neighborhood.

This makes the tuning process feel closer to real applied ML work than a one-shot textbook example.

## [Source: e2e090_neural_network.ipynb]

The final notebook compares a PyTorch regression approach against the best random-forest baseline.

Its key themes are:

- reuse the same leakage-safe preprocessing pipeline,
- normalize both inputs and the regression target,
- use MSE loss while reporting RMSE for interpretability,
- train minibatch neural networks with PyTorch data loaders,
- compare neural-network performance against the tuned tree-based baseline.

The important conceptual lesson is not that neural networks always win, but that deep learning is another modeling option whose evaluation must be kept on the same methodological footing as classical models.

## [Source: utils/load_california.py]

This helper consolidates the stratified train/test split introduced earlier in notebook form.

It:

- loads the dataset,
- builds the `income_cat` stratification feature,
- performs the split reproducibly,
- removes the temporary stratification column,
- returns `X_train`, `X_test`, `y_train`, and `y_test`.

Its role is conceptual as much as practical: the split logic becomes reusable infrastructure instead of repeated notebook code.

## [Source: utils/housing_preprocessing.py]

This module is the implementation heart of the modeling half.

It consolidates the preprocessing ideas from the notebook sequence into reusable code:

- categorical imputation and one-hot encoding,
- ratio-based engineered features,
- logarithmic transforms for skewed variables,
- geospatial clustering through `ClusterSimilarity`,
- default numeric scaling,
- target scaling for neural-network training.

This file is what turns the earlier conceptual notebooks into a reusable preprocessing contract shared across all later models.

## [Source: utils/training_utils.py]

The training utilities provide PyTorch-specific helpers for the neural-network notebook.

They cover:

- one-epoch training,
- evaluation with denormalized RMSE,
- collection of train/validation metrics,
- multi-epoch training history,
- plotting of learning curves.

This utility layer keeps the deep-learning notebook focused on modeling decisions instead of repetitive training-loop boilerplate.

# Cross-References

## Internal progression of the modeling unit

- `e2e050`, `e2e051`, and `e2e060` form a three-step build-out of the preprocessing stack: generic pipelines, custom feature transforms, and geospatial similarity features. [Source: e2e050_pipelines.ipynb; Source: e2e051_custom_transformers.ipynb; Source: e2e060_spatial_clustering.ipynb]
- `e2e070`, `e2e080`, and `e2e081` then use that shared preprocessing stack as a stable base for model comparison, leakage-safe evaluation, and hyperparameter tuning. [Source: e2e070_model_evaluation.ipynb; Source: e2e080_hyperparameters.ipynb; Source: e2e081_hyperparameters2.ipynb]
- `e2e090` extends the same workflow into PyTorch, so the neural-network comparison is framed as one more modeling experiment built on the same data-preparation principles rather than as a separate project. [Source: e2e090_neural_network.ipynb; Source: utils/housing_preprocessing.py; Source: utils/training_utils.py]

## Notebook-to-utils consolidation

- The pipeline ideas introduced in `e2e050`, `e2e051`, and `e2e060` are consolidated in `utils/housing_preprocessing.py`, which becomes the shared preprocessing backend for later notebooks. [Source: e2e050_pipelines.ipynb; Source: e2e051_custom_transformers.ipynb; Source: e2e060_spatial_clustering.ipynb; Source: utils/housing_preprocessing.py]
- The stratified split discussed in the earlier train/test notebook is operationalized here in `utils/load_california.py`, allowing later notebooks to import data-loading logic rather than re-derive it manually. [Source: utils/load_california.py]
- The PyTorch training patterns used in `e2e090` are similarly moved into `utils/training_utils.py`, which separates training mechanics from model-design discussion. [Source: e2e090_neural_network.ipynb; Source: utils/training_utils.py]

## Decision criteria and trade-offs

- Use pipelines when reproducibility and leakage control matter more than ad hoc dataframe manipulation. [Source: e2e050_pipelines.ipynb; Source: utils/housing_preprocessing.py]
- Introduce custom transformers when domain-specific feature logic cannot be expressed cleanly with stock preprocessors. [Source: e2e051_custom_transformers.ipynb; Source: utils/housing_preprocessing.py]
- Replace raw latitude/longitude with similarity-to-region features when spatial effects are nonlinear and interaction-heavy. [Source: e2e060_spatial_clustering.ipynb; Source: utils/housing_preprocessing.py]
- Prefer validation sets and cross-validation for model comparison, and keep the test set untouched until the very end. [Source: e2e070_model_evaluation.ipynb; Source: utils/load_california.py]
- Prefer randomized or iterative tuning once the search space becomes too large for exhaustive grids to be computationally sensible. [Source: e2e080_hyperparameters.ipynb; Source: e2e081_hyperparameters2.ipynb]
- Judge neural networks against the same preprocessing and evaluation rules as classical models rather than assuming they should outperform by default. [Source: e2e090_neural_network.ipynb; Source: utils/training_utils.py]
