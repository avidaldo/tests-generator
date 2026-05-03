<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | 05-modeling.ipynb | `.ipynb` | ✅ |
| 2 | 06-deep-learning.ipynb | `.ipynb` | ✅ |

# Content

## [Source: 05-modeling.ipynb]

The modeling notebook turns the earlier `king-county` preprocessing work into a full supervised-model selection workflow.

Its main stages are:

- load the preprocessed data,
- define baseline metrics,
- compare multiple algorithm families with default settings,
- shortlist promising candidates,
- tune those candidates with `GridSearchCV` and `TimeSeriesSplit`,
- evaluate the final chosen model on the held-out test set exactly once,
- interpret prediction quality and feature importance.

Several methodological points matter more than any individual model result:

- all development decisions use the validation set rather than the test set,
- temporal structure is preserved during cross-validation,
- multiple shortlisted models are tuned instead of trusting default-hyperparameter ranking,
- nested parallelism is avoided by parallelizing the search level rather than both search and estimator simultaneously.

The notebook therefore teaches model selection as a workflow-design problem, not just a leaderboard comparison.

## [Source: 06-deep-learning.ipynb]

The deep-learning notebook asks whether a PyTorch multilayer perceptron can improve on the best traditional tabular model.

Its key conceptual contributions are:

- explain why tree ensembles are often already very strong on medium-sized tabular datasets,
- scale the target variable because neural-network optimization is sensitive to target magnitude,
- build a dense network with batch normalization, dropout, and ReLU activations,
- implement explicit training and validation loops with early stopping,
- compare the neural network against the best sklearn-style model on equal footing,
- discuss fairness limits in that comparison because the tree model was grid-tuned while the neural network architecture was hand-chosen.

The notebook's most valuable lesson is not that neural networks outperform tree methods here. It is that architectural flexibility and gradient-based training come with extra tuning burden, and that for tabular regression a tuned tree ensemble remains the default benchmark to beat.

# Cross-References

## Internal progression of the modeling unit

- `05-modeling` performs the classical ML workflow: baseline, screening, shortlist, temporal cross-validation, tuning, and final test evaluation. [Source: 05-modeling.ipynb]
- `06-deep-learning` reuses the same prepared data and evaluation framing to ask whether a neural approach improves on that tuned classical baseline. [Source: 06-deep-learning.ipynb]

## Connections to the foundations unit

- The strict validation/test separation in `05-modeling` is a direct continuation of the temporal-leakage guardrails introduced earlier in the repository. [Source: 05-modeling.ipynb]
- The deep-learning notebook depends on the preprocessing pipeline and leakage-safe data preparation from the foundations half, especially because both feature scaling and target scaling must be learned from training data only. [Source: 06-deep-learning.ipynb]

## Decision criteria and trade-offs

- Compare algorithm families with default settings only as a screening step, not as a final verdict. Final model choice should follow tuning on the shortlisted candidates. [Source: 05-modeling.ipynb]
- Use `TimeSeriesSplit` instead of ordinary shuffled cross-validation when the data is temporally ordered and the deployment setting is future-facing. [Source: 05-modeling.ipynb]
- Parallelize at one level only when combining search procedures with internally parallel estimators, otherwise contention can make the workflow slower rather than faster. [Source: 05-modeling.ipynb]
- Treat tuned tree ensembles as the default strong baseline for medium-sized tabular regression, and demand that neural networks justify their extra complexity empirically rather than by reputation. [Source: 05-modeling.ipynb; Source: 06-deep-learning.ipynb]
- Scale the regression target for neural-network training when raw target magnitudes would destabilize gradient-based optimization. [Source: 06-deep-learning.ipynb]
- Be explicit about comparison fairness: a hand-designed neural architecture is not directly comparable to a systematically tuned tree model unless both receive comparable search effort. [Source: 06-deep-learning.ipynb]
