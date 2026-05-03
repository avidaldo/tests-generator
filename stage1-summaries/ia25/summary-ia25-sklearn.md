<!-- markdownlint-disable MD024 MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | 01_basic_regression_workflow.ipynb | `.ipynb` | ✅ |
| 2 | clustering_pca_pipeline.ipynb | `.ipynb` | ✅ |
| 3 | diabetes_classification.ipynb | `.ipynb` | ✅ |
| 4 | diabetes_regression.ipynb | `.ipynb` | ✅ |
| 5 | iris_clustering.ipynb | `.ipynb` | ✅ |
| 6 | mnist_svm_eval.ipynb | `.ipynb` | ✅ |
| 7 | overfitting_train_test_split.ipynb | `.ipynb` | ✅ |
| 8 | iris/01_iris_data_structure_and_analysis.ipynb | `.ipynb` | ✅ |
| 9 | iris/02_logistic_regression_workflow.ipynb | `.ipynb` | ✅ |
| 10 | iris/03_pipelines_and_validation_classification.ipynb | `.ipynb` | ✅ |

# Content

## [Source: 01_basic_regression_workflow.ipynb]

### The fundamental regression workflow

The notebook uses linear regression to teach the standard machine-learning workflow for regression tasks. It is explicit about the sequence:

1. load and explore data,
2. split training and test sets,
3. preprocess through scaling,
4. train the model,
5. evaluate performance,
6. analyze results.

Regression is defined as the prediction of continuous numerical values rather than categories. House-price prediction, temperature forecasting, and energy consumption are used as examples.

### California Housing dataset and feature interpretation

The workflow uses the California Housing dataset, described as 20,640 observations with 8 features such as income, house age, rooms, population, and geographic coordinates. The target is median house value in units of `$100,000s`.

The notebook uses this dataset to preserve several general lessons:

- real regression datasets can contain features with very different scales,
- the target distribution and feature correlations should be inspected before modeling,
- exploratory analysis is part of the workflow, not an optional extra.

### Train/test split and the reason it exists

The notebook treats the train/test split as the most fundamental rule in machine learning. The model must never see the test set during training, because the point of the test set is to simulate real performance on unseen data.

### Feature scaling as best practice

A subtle but important nuance is preserved: standard linear regression can find an analytical closed-form solution even without scaling, so scaling is not strictly required for convergence in the same way it is for iterative methods.

Even so, the notebook argues scaling is still best practice for three reasons:

- coefficient interpretability,
- numerical stability,
- future-proofing the data for algorithms that do require scaling.

### Linear regression model and evaluation metrics

The notebook presents the usual linear-regression form with coefficients and intercept, then evaluates the model using:

- MAE,
- RMSE,
- `R^2`.

It explains what each metric means and why multiple metrics are useful.

### Overfitting awareness and result analysis

The notebook explicitly links overfitting to the gap between training and test performance. Similar train and test metrics are treated as evidence of good generalization.

The code-demonstrated part includes actual-versus-predicted plots and error distributions to show that metrics alone do not tell the whole story.

## [Source: overfitting_train_test_split.ipynb]

### Overfitting and why train/test separation matters

This notebook revisits earlier salary-prediction examples to isolate the concept of overfitting. Its definition is operational: the model fits training data too closely and fails to generalize to new data. A low training error with a high test error is the classic sign.

The notebook also preserves a practical rule of thumb: using about 20% of the data for the test set is common, though the exact fraction depends on dataset size.

### Linear regression versus regression trees

The notebook compares a linear regression model and an unrestricted regression tree on the same salary-style dataset.

The linear-regression example shows relatively stable train-versus-test behavior. The unrestricted tree, by contrast, makes the overfitting problem visually obvious: it fits training data extremely closely but performs poorly on the test data.

### Parametric versus non-parametric intuition

One of the strongest conceptual passages in the notebook is the comparison between parametric and non-parametric models:

- parametric models such as linear regression have a fixed form and a fixed number of parameters,
- non-parametric models such as decision trees can adapt their complexity to the data.

The notebook uses this to explain why non-parametric models tend to overfit more easily.

### Controlling tree complexity and the bias-variance vocabulary

Limiting tree depth is presented as one way to reduce overfitting. The notebook notes that the chosen depth here was found by trying different values and observing test performance, while also pointing forward to more systematic methods such as cross-validation and hyperparameter tuning.

It then distinguishes:

- underfitting: model too simple, high error on both train and test,
- overfitting: low train error but high test error,
- good fit: captures the pattern and generalizes.

## [Source: diabetes_regression.ipynb]

### Regression workflow on diabetes progression

This notebook applies the general regression workflow to the scikit-learn diabetes dataset. The task is to predict a continuous measure of disease progression one year after baseline from ten physiological features.

The workflow includes loading, exploration, train/test split, training multiple models, evaluation, and visualization.

### Continuous target and model comparison

The notebook explicitly checks that the target variable is continuous to confirm that regression is the right problem formulation.

It then compares two models:

- Linear Regression,
- Decision Tree Regressor.

### Regression metrics and diagnostic visualizations

The notebook uses MAE, RMSE, and `R^2` as the main evaluation metrics. It also uses prediction-versus-actual plots, residual plots, and feature-importance plots for the tree model.

### Interpretation of the comparison

The conclusion preserves several practical insights:

- linear regression outperforms the decision tree on this small dataset,
- simpler models may do better on small datasets because they overfit less,
- residual plots help diagnose whether predictions behave like smooth errors around zero,
- tree residuals may reveal rigid piecewise behavior.

The notebook also proposes natural next steps: feature engineering, hyperparameter tuning, and more powerful ensemble methods.

## [Source: diabetes_classification.ipynb]

### Classification workflow on diabetes diagnosis

This notebook uses diabetes-related data again, but changes the question from "how much disease progression?" to "does the patient have diabetes?". That contrast is central: same general domain, different target type, and therefore different machine-learning problem.

The dataset here is the Pima Indians Diabetes Database, with 768 patients, 8 features, and a binary outcome variable.

### Missing-value handling as preprocessing

The notebook includes a concrete and realistic preprocessing rule: zeros in several physiological variables are treated as missing values because zero blood pressure, BMI, and similar measures are physically implausible.

The procedure is:

1. replace those zeros with `NaN`,
2. fill missing values with the median.

Median is chosen because it is more robust to outliers than the mean.

### Split, scaling, and stratification

The notebook uses the same train/test split logic as the regression workflow, but adds stratification to preserve class balance across the split. It also explains why scaling matters for algorithms such as logistic regression.

### Logistic regression versus decision tree classification

The notebook compares a linear classifier and a non-linear tree classifier. The teaching point is not just to compare scores, but to preserve the analogy with the regression notebook:

- linear model versus tree,
- continuous target versus binary target,
- regression metrics versus classification metrics.

### Classification metrics and confusion-matrix thinking

Accuracy, precision, recall, and F1-score are introduced as the main classification metrics. The notebook also uses confusion matrices to define true positives, true negatives, false positives, and false negatives in concrete diagnostic terms.

### Key cross-notebook lesson

The notebook explicitly states that the machine-learning workflow is structurally similar across regression and classification, but the target type changes the models, metrics, and visualizations.

## [Source: clustering_pca_pipeline.ipynb]

### Unsupervised clustering on handwritten digits

This notebook uses the digits dataset to ask whether K-Means can discover digit classes without seeing labels. The labels are present only for evaluation, which makes the distinction between unsupervised training and supervised benchmarking explicit.

### Scaling and the clustering pipeline

The notebook strongly emphasizes that K-Means depends on Euclidean distance and therefore requires features to be on comparable scales. It demonstrates the effect of `StandardScaler` by comparing statistics and boxplots before and after scaling.

It then builds a pipeline that combines scaling and clustering, reinforcing that pipelines are useful even for unsupervised workflows.

### Interpreting inertia, convergence, and cluster sizes

The notebook explains inertia as within-cluster variance and carefully interprets what the observed inertia means relative to the total variation in the standardized data. It also reports convergence behavior and uses cluster-size inspection to check whether the clustering found a trivial or degenerate partition.

### Visualizing cluster centers and evaluating clustering

Because centroids live in 64-dimensional space, the notebook maps them back to pixel space to visualize what each cluster center looks like. This is used to assess whether clusters resemble recognizable digits.

The notebook also separates two evaluation families:

- unsupervised metrics such as silhouette, Calinski-Harabasz, and Davies-Bouldin,
- supervised comparison metrics such as Adjusted Rand Index, Normalized Mutual Information, homogeneity, completeness, and V-measure.

### PCA and the choice of K

PCA is introduced as a visualization tool rather than as the actual clustering space. The notebook then studies the choice of `K` through the elbow method and silhouette analysis, while also listing K-Means limitations and best practices.

## [Source: mnist_svm_eval.ipynb]

### Binary classification on MNIST and the limits of accuracy

This notebook starts by turning MNIST into a binary task: detect whether the digit is a 5 or not. It uses `SGDClassifier`, described as stochastic-gradient optimization over a linear model such as an SVM.

The central teaching lesson is that accuracy can be misleading. A classifier that always predicts the majority class can still achieve around 90% accuracy in this setting because only about 10% of digits are 5.

### Confusion matrix and the precision-recall trade-off

The notebook uses the confusion matrix to define true negatives, false positives, false negatives, and true positives concretely. It then introduces:

- precision as correctness among predicted positives,
- recall as coverage among actual positives,
- F1 as the harmonic mean of precision and recall.

It preserves a particularly valuable scenario-based comparison:

- for child-safe videos, high precision may matter more even if recall is low,
- for thief detection in surveillance, very high recall may matter more even if precision is poor.

This is one of the clearest decision-criterion passages in the sklearn unit.

### Multiclass classification with OvR and OvO

The notebook then generalizes to multiclass classification. It explains the one-versus-rest and one-versus-one strategies, their computational trade-offs, and why different algorithms default to different strategies.

The key preserved distinction is that OvO trains many more classifiers, but each classifier sees only part of the data, which can be advantageous for algorithms such as SVMs.

## [Source: iris/01_iris_data_structure_and_analysis.ipynb]

### Understanding the Iris dataset and scikit-learn's Bunch object

The notebook presents Iris as a classic labeled dataset with 150 samples, 3 species, and 4 measured features. It carefully explains how `load_iris()` returns data, targets, feature names, and a description.

The mapping from target integers to species names is made explicit, and petal length and width are identified as especially informative features.

### NumPy versus Pandas as workflow choices

This notebook contains one of the clearest tool-choice explanations in the entire corpus. It compares loading data as NumPy arrays and as Pandas DataFrames.

NumPy is favored for:

- speed,
- lower memory overhead,
- compatibility across scientific and deep-learning libraries,
- efficient training.

Pandas is favored for:

- exploratory data analysis,
- data cleaning,
- feature engineering,
- grouping, plotting, and interpretability.

The notebook recommends a mixed workflow: explore with Pandas, train with NumPy.

### Exploratory analysis and modeling implications

The EDA sections use histograms, pairplots, boxplots, and correlation analysis to show:

- the dataset is balanced,
- Setosa is clearly separated,
- Versicolor and Virginica overlap somewhat,
- petal measurements are the most discriminative,
- feature scales differ enough that scaling matters for distance-based algorithms.

The notebook then turns these observations into modeling implications: linear models should work reasonably well, petal features are strong signals, and high accuracy is plausible.

## [Source: iris/02_logistic_regression_workflow.ipynb]

### Building intuition with a single feature

The notebook begins with a binary classification problem: identify Virginica versus not Virginica using only petal length. This simplification allows the learner to visualize the sigmoid curve and the probability interpretation of logistic regression.

The notebook explicitly explains the mechanism:

1. compute a linear score,
2. pass it through the sigmoid,
3. threshold the probability to obtain the class.

### Full multiclass classification workflow

It then expands to the full 3-class problem using all four features and walks through a complete professional workflow: split, scale, train, evaluate, and analyze.

One of the most important warnings is that data should be split before scaling. Otherwise the scaler would leak information from the test set into training.

### Metrics, confusion matrix, and model interpretation

The notebook explains accuracy, precision, recall, F1-score, detailed classification reports, confusion matrices, and class-probability outputs.

It also preserves a strong summary of logistic regression's strengths and limitations:

- strengths: fast, interpretable, probabilistic, strong baseline, simple,
- limitations: linear boundaries, sensitivity to scaling, underfitting of complex problems.

### Decision criteria

The notebook clearly states when to use logistic regression:

- when a fast and interpretable baseline is needed,
- when probabilities matter,
- when classes are close to linearly separable,
- when feature importance matters.

## [Source: iris/03_pipelines_and_validation_classification.ipynb]

### Why manual workflows are not enough

This notebook takes the previous classification workflow and improves it in two ways:

- pipelines for preprocessing plus model training,
- proper validation that prevents test-set leakage during model comparison.

### The wrong way and the right way to compare models

The notebook explicitly calls out a wrong pattern: train multiple models, compare them on the test set, then choose the best one. That is wrong because the test set has influenced model selection.

The correct approach is a three-way split:

- training set for fitting,
- validation set for comparison and selection,
- test set for final evaluation once.

The notebook is direct about why this matters: the test set is supposed to simulate unseen deployment data and should not influence model choice.

### Pipelines and their practical value

The notebook contrasts manual scaling-plus-training code with a pipeline-based approach. The advantages are:

- cleaner code,
- fewer preprocessing mistakes,
- consistent transformations,
- easier deployment,
- fair comparison across algorithms.

It explains how a pipeline uses `fit_transform` on training data and only `transform` on new data.

### Model comparison across four algorithms

The notebook compares:

- Logistic Regression,
- KNN,
- Decision Tree,
- Random Forest.

It also explains why scaling all models can still be a reasonable choice even though tree-based models do not strictly require it: consistency, harmlessness, and future-proofing.

### Final evaluation and the sanctity of the test set

The notebook's strongest methodological claim is that the test set should be used exactly once after the best model is selected from validation performance. It frames this not only as good practice but as scientific rigor and professional standard.

## [Source: iris_clustering.ipynb]

### Using clustering on a labeled dataset for comparison

This notebook deliberately applies K-Means to Iris while ignoring the known labels, then compares the resulting clusters with the real species afterward.

### Sensitivity to initialization and subjective choice of K

The notebook points out that with default initialization behavior, the clustering can vary substantially because K-Means is sensitive to centroid initialization and may not converge to the global minimum. Increasing the number of initialization attempts stabilizes the result.

It also preserves a useful caution: once the plot is stable, the elbow-like change in slope across possible values of `K` can still be quite subjective.

### Comparing clusters to real labels

Because cluster identifiers do not inherently align with real class identifiers, the notebook maps clusters to the most frequent real class within each cluster before comparing them like a classification task.

This procedure comes with caveats that are explicitly preserved:

- ties would need more careful handling,
- two clusters could share the same modal real class.

# Cross-References

## Comparisons and distinctions

- The California and diabetes regression notebooks both teach supervised regression workflows, but the former emphasizes the general workflow and scaling rationale while the latter emphasizes model comparison on a smaller medical dataset. [Source: 01_basic_regression_workflow.ipynb; Source: diabetes_regression.ipynb]
- The diabetes regression and diabetes classification notebooks show how the same broad application area can lead to different machine-learning formulations depending on whether the target is continuous or categorical. [Source: diabetes_regression.ipynb; Source: diabetes_classification.ipynb]
- The Iris EDA notebook and the Iris logistic-regression notebook are complementary: one explains the structure and separability of the dataset, while the other turns that understanding into a full classification workflow. [Source: iris/01_iris_data_structure_and_analysis.ipynb; Source: iris/02_logistic_regression_workflow.ipynb]
- The clustering notebooks on digits and Iris both use K-Means, but the digits notebook emphasizes pipelines, evaluation metrics, PCA visualization, and centroid interpretation, whereas the Iris notebook emphasizes initialization sensitivity and post-hoc alignment with known labels. [Source: clustering_pca_pipeline.ipynb; Source: iris_clustering.ipynb]
- Accuracy alone is contrasted sharply with precision, recall, and F1 in the MNIST notebook, especially under class imbalance or asymmetric cost conditions. [Source: mnist_svm_eval.ipynb]

## Dependencies and prerequisites

- The basic regression workflow is a prerequisite for understanding the later overfitting notebook because it establishes the split-scale-train-evaluate pattern that the overfitting notebook then critiques and extends. [Source: 01_basic_regression_workflow.ipynb; Source: overfitting_train_test_split.ipynb]
- Understanding the Iris dataset structure and its feature separability feeds directly into both the logistic-regression workflow and the clustering analysis. [Source: iris/01_iris_data_structure_and_analysis.ipynb; Source: iris/02_logistic_regression_workflow.ipynb; Source: iris_clustering.ipynb]
- The pipelines-and-validation notebook depends on the logistic-regression workflow because it assumes the reader already understands train/test splits, scaling, metrics, and basic classification practice. [Source: iris/02_logistic_regression_workflow.ipynb; Source: iris/03_pipelines_and_validation_classification.ipynb]
- K-Means in both clustering notebooks depends on the repeated principle that distance-based methods require sensible scaling and careful thinking about the number of clusters. [Source: clustering_pca_pipeline.ipynb; Source: iris_clustering.ipynb]

## Decision criteria and context-dependent choices

- Use Pandas when exploration, grouping, named-feature analysis, or cleaning matters; convert to NumPy when performance and numerical modeling efficiency matter more than labeled tabular structure. [Source: iris/01_iris_data_structure_and_analysis.ipynb]
- Use a train/test split to estimate generalization, but use a three-way train/validation/test split when comparing multiple models or tuning decisions so the test set remains untouched until the end. [Source: 01_basic_regression_workflow.ipynb; Source: overfitting_train_test_split.ipynb; Source: iris/03_pipelines_and_validation_classification.ipynb]
- Prefer logistic regression when you need a fast, interpretable baseline with probability estimates and reasonably linear decision boundaries. [Source: iris/02_logistic_regression_workflow.ipynb; Source: diabetes_classification.ipynb]
- Prefer distance-based methods such as K-Means or KNN only after scaling features appropriately, because raw feature scale can distort similarity calculations. [Source: clustering_pca_pipeline.ipynb; Source: iris/01_iris_data_structure_and_analysis.ipynb]
- Prefer recall over precision in scenarios where missing positives is extremely costly, and prefer precision over recall when false positives are more harmful. [Source: mnist_svm_eval.ipynb]
- Treat the test set as sacred: it should not be used to choose the best model, tune hyperparameters, or steer development decisions. [Source: iris/03_pipelines_and_validation_classification.ipynb]
