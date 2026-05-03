<!-- markdownlint-disable MD024 MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | 00_introduction.md | `.md` | ✅ |
| 2 | knn.md | `.md` | ✅ |
| 3 | decision_tree.ipynb | `.ipynb` | ✅ |
| 4 | kmeans.ipynb | `.ipynb` | ✅ |
| 5 | knn.ipynb | `.ipynb` | ✅ |
| 6 | linear_regression.ipynb | `.ipynb` | ✅ |
| 7 | logistic_regression.ipynb | `.ipynb` | ✅ |
| 8 | random_forest.ipynb | `.ipynb` | ✅ |

# Content

## [Source: 00_introduction.md]

### The historical evolution of machine learning

The file frames machine learning historically rather than as a static toolkit. Its main teaching claim is that different algorithms emerged to solve different problem types, and that understanding this evolution helps explain both their strengths and when to use them.

Machine learning is divided into three paradigms:

- supervised learning, which learns from labeled examples,
- unsupervised learning, which discovers patterns in unlabeled data,
- reinforcement learning, which learns through interaction and feedback.

### Timeline of key algorithms and why they matter

The source gives a timeline that combines chronology with purpose:

- Linear Regression, placed in the early 1800s, is presented as the foundation for supervised learning and valued for simplicity, interpretability, and real-world usefulness.
- Logistic Regression, placed in the 1940s, is described as a classification method despite its name, extending linear ideas to categorical outcomes and introducing the sigmoid function.
- K-Means, placed in 1957, is presented as an early success in unsupervised learning and still useful for customer segmentation, image compression, and exploratory analysis.
- KNN, dated between 1951 and 1967, is described as instance-based or lazy learning: highly intuitive, usable for both classification and regression, but potentially computationally expensive.
- Decision Trees, developed conceptually in the 1960s and refined through CART, ID3, and C4.5, are presented as highly interpretable and able to model non-linear relationships.
- Q-Learning, dated to 1989, is treated as a fundamentally different learning paradigm centered on state-action values, experience, reward, and sequential decision-making.
- Random Forests, introduced in 2001, are presented as a demonstration of ensemble learning, specifically as a way to reduce the overfitting of single decision trees.

### The three paradigms and their use cases

The file makes the problem-type distinction explicit:

- supervised learning covers regression and classification when historical data includes known outcomes,
- unsupervised learning covers clustering and dimensionality reduction when hidden structure must be discovered without labels,
- reinforcement learning is appropriate when decisions are sequential and the system can be guided by rewards rather than labels.

### Why classical algorithms still matter in the modern era

Although the file names deep learning, advanced ensembles, transfer learning, large language models, and deep reinforcement learning as part of the modern landscape, it argues that classical algorithms remain foundational because they are often strong choices on small and medium datasets, are computationally efficient, are easier to interpret, and still underlie many modern methods.

### Criteria for choosing an algorithm

The source lists the main decision factors:

- problem type,
- whether labels or rewards are available,
- dataset size,
- interpretability requirements,
- training-speed versus prediction-speed trade-offs,
- accuracy demands,
- data properties such as linearity, outliers, and feature interactions,
- whether actions change future states, which points toward reinforcement learning.

## [Source: knn.md]

### KNN for classification

K-Nearest Neighbors is described as a simple and effective supervised algorithm that can perform both classification and regression. It is explicitly non-parametric because it makes no assumptions about the underlying data distribution.

For classification, the rule is straightforward: given a point to predict, find the closest training samples and assign the most common label among them.

The file preserves a concrete scenario-based example: with `K = 3`, a green test point is classified as a red triangle because two of its three nearest neighbors are red triangles; with `K = 5`, the same point would instead become a blue square because the broader neighborhood changes the majority label.

### Lazy learning and computational trade-offs

The file makes the lazy-learning idea central. KNN does not summarize the data into a compact fitted model. Instead, it stores the entire training set and uses it directly during prediction.

This leads to an important trade-off:

- training is extremely lightweight because it mainly stores data,
- prediction is expensive because the test point must be compared against all training points,
- the algorithm therefore becomes slow and memory-demanding on large datasets.

### KNN for regression

For regression, the file changes the prediction rule from majority vote to averaging. The assigned value for a query point is the average of the values of its nearest neighbors.

The linked visual example around `x = 4` preserves the idea that different values of `K` produce different regression estimates, which makes neighborhood size a crucial modeling choice.

## [Source: linear_regression.ipynb]

### Introduction

Linear regression is presented as a statistical method for modeling the relationship between a dependent variable `Y` and one or more independent variables `X_i`. The objective is to find a linear function that predicts the value of `Y` from the predictors.

The notebook deliberately begins with simple linear regression using only years of experience to predict salary. It uses this simplification to contrast simple linear regression with multiple linear regression, where additional predictors such as education, job type, industry, or city could improve the model.

### Data reading, exploration, and variable roles

The notebook uses a salary dataset and makes the variable-role distinction explicit:

- years of experience is the independent variable, predictor, or feature,
- salary is the dependent variable, target, or response.

The explanation also preserves an important caveat: the model assumes salary depends on experience based on domain knowledge, but correlation by itself does not prove causation.

### Visualization and model intuition

The source uses a scatter plot to show the relationship between experience and salary. The observed pattern is a clear positive correlation that looks approximately linear.

The notebook then interprets the model as a compact description of reality: once a line is fitted to the sample data, that line can be used to predict salaries for new employees whose years of experience are known.

### The linear model and its parameters

The fitted model is expressed as `y = m*x + b`, with `m` as slope and `b` as intercept. The notebook explicitly calls these coefficients the model parameters.

It introduces `LinearRegression` from scikit-learn as the class implementing this model and explains why the independent-variable input must be two-dimensional even when there is only one predictor: rows represent samples and columns represent features. That is why a one-dimensional vector of experience values must be reshaped into a matrix with one column.

The notebook also contrasts DataFrame and Series usage:

- a single feature should still be passed as a one-column DataFrame,
- the target can be passed as a Series because the model predicts a single dependent variable.

### Predictions, residuals, and notation

The source introduces `ŷ` as the predicted value of `y` and contrasts predictions with actual observations.

It also makes an important conceptual distinction between residuals and errors:

- residuals are the observed differences `y - ŷ` inside the dataset,
- true errors include unknown noise or uncontrolled factors and are not directly observable.

The code-demonstrated part of the notebook is used to visualize the regression line together with residuals, reinforcing that fitting seeks to minimize those residuals.

### Error metrics and cost functions

The notebook compares the two most common regression loss ideas:

- Mean Absolute Error (MAE), which is intuitive because it expresses average mistake magnitude, but whose absolute-value form is less convenient for optimization,
- Mean Squared Error (MSE), which is differentiable and therefore easier to optimize, but penalizes outliers more strongly because squaring amplifies large deviations.

RMSE is then introduced as the square root of MSE so that the error is expressed in the same units as the target variable. The notebook also names `R^2`, MAPE, SMAPE, and median absolute error as additional regression metrics.

### Model fitting with ordinary least squares

The notebook explains that scikit-learn's linear regression uses ordinary least squares to minimize the sum of squared residuals. For simple linear regression, it emphasizes that the solution can be obtained analytically in closed form, which makes training very fast.

This section also establishes a broader machine-learning pattern: many models can be understood as adjusting internal parameters to minimize some loss function, even though their internal structure may be much more complex than a line.

### Prediction of new values and multiple linear regression

Once the model is trained, new salaries can be predicted directly through the model's prediction method rather than by manually reconstructing the line from coefficients.

The notebook generalizes the one-feature line to planes or hyperplanes when more predictors are used, using multiple linear regression as the natural extension of the same logic.

### Code-demonstrated concepts

The notebook uses code and plots to demonstrate:

- scatter-plot exploration of the salary dataset,
- fitting and displaying the regression line,
- visualizing residuals against the fitted model,
- comparing the fitted line with deliberately poor lines to show how MAE and MSE increase,
- predicting salaries for new values of experience.

## [Source: logistic_regression.ipynb]

### Introduction

The notebook presents logistic regression as a classification method, not a regression method in the usual predictive sense. Its key contrast with linear regression is that linear regression predicts continuous outputs, whereas logistic regression predicts probabilities for categorical outcomes.

The notebook explains why the name is still historically appropriate: the model uses a linear function on the log-odds, then applies the sigmoid transformation to map that linear combination into the interval from 0 to 1.

### Dataset and problem framing

The example uses data from 100 university applicants, with two entrance-exam scores and a binary admission outcome. To simplify the first explanation, the notebook temporarily uses only the first exam score as the independent variable.

This staged simplification matters pedagogically: it makes the transition from linear regression ideas toward binary classification more transparent.

### Probability interpretation and the sigmoid function

The notebook argues that even though the observed outcomes are binary, the problem can be given a probabilistic interpretation: higher scores should correspond to a higher probability of admission.

The sigmoid function is introduced as the mechanism that produces a smooth curve with flat extremes near 0 and 1 and a steeper transition in the middle. This makes it suitable for modeling a probability that changes gradually with the predictors.

### Fitting the model and threshold-based predictions

The notebook states that logistic regression finds its parameters through maximum likelihood estimation and that scikit-learn uses iterative optimizers such as L-BFGS or SAG to obtain those weights.

It also preserves a procedural modeling rule that mirrors the linear-regression notebook: the independent-variable input should be a DataFrame, not a Series, because the model expects a column-oriented feature matrix.

Predictions are then interpreted through a threshold, usually 0.5:

- probabilities above the threshold are mapped to the positive class,
- probabilities below the threshold are mapped to the negative class.

### Probability outputs and class interpretation

The notebook explains that `predict_proba` returns one probability column per class. In the binary case, the two columns are complements, but keeping both matters conceptually because multiclass classification extends this pattern beyond two outcomes.

### Multiple predictors and decision boundary

The model is then expanded back to the full two-exam setting. Instead of focusing on a three-dimensional sigmoid surface, the notebook emphasizes a two-dimensional decision boundary: the locus where the predicted probability of admission is 50%.

### Code-demonstrated concepts

The notebook uses code and plots to demonstrate:

- the scatter of admitted versus non-admitted students,
- the fitted sigmoid curve for one exam score,
- class prediction around the threshold,
- probability interpretation through `predict_proba`,
- a two-feature decision boundary showing the 50% admission frontier.

## [Source: kmeans.ipynb]

### Introduction and clustering objective

The notebook defines clustering as an unsupervised technique for grouping similar records into clusters. K-means is presented as a method that assigns each sample to one of `K` predefined groups based on the nearest centroid.

The optimization objective is inertia, also called WCSS, the within-cluster sum of squared distances from points to their cluster centroids. Lower inertia indicates more compact clusters.

### The K-means algorithm

The notebook gives a four-step procedure:

1. initialize `K` centroids,
2. assign each sample to the nearest centroid,
3. update centroids as group means,
4. repeat assignment and update until convergence or until the maximum number of iterations is reached.

This procedural explanation is central because it explains why the algorithm is iterative and why initialization matters.

### Creating test data and interpretability limits

The notebook uses generated blob data to create a visually understandable clustering example. It explains parameters such as sample count, number of features, number of centers, random seed, and cluster standard deviation.

It also explicitly warns that these low-dimensional visual examples are teaching devices. Real datasets often have many more dimensions and cannot be visually clustered by eye.

### Feature scaling as a critical prerequisite

This notebook treats scaling as essential rather than optional. Because K-means uses Euclidean distance, features with larger numerical scales dominate clustering decisions and can produce misleading clusters. Standardization is therefore required so that features contribute fairly to distance computations.

### Training K-means and its main parameters

The notebook explains the meaning of key parameters:

- `n_clusters` controls how many centroids and clusters are produced,
- `init` controls centroid initialization and highlights `k-means++` as a better default than naive random initialization,
- `max_iter` limits iterations per run,
- `n_init` repeats the whole algorithm from different starting points and keeps the best result.

The notebook also explains that `fit_predict` both trains the model and returns cluster labels, while `labels_` stores those same assignments on the fitted object.

### Centroids, prediction, decision boundaries, and soft clustering

After fitting, centroids are available through `cluster_centers_`, and new instances can be assigned to clusters with `predict`.

The notebook also uses the decision-boundary view to show that K-means induces a Voronoi tessellation. It then makes an important conceptual distinction: hard clustering assigns each instance to a single cluster, whereas a softer interpretation can be obtained by measuring distances to all centroids via the `transform` method.

### Choosing the number of clusters

The notebook compares two methods:

- the elbow method, which looks for the point where increasing `K` stops reducing inertia sharply,
- the silhouette score, which measures how well samples fit their own cluster versus neighboring clusters.

An important edge case is preserved: the elbow may be ambiguous. In the notebook's generated example, the source explains that overlap between generated clusters can make `K = 3` or `K = 4` look plausible even when the synthetic data were generated from 5 centers. The silhouette score then favors 4 clusters over both 3 and 5.

### Limitations of K-means

The notebook lists several limitations:

- sensitivity to initialization,
- the need to choose the number of clusters in advance,
- poorer behavior when clusters have different sizes, different densities, or non-spherical shapes,
- dependence on proper scaling,
- the possibility that other clustering methods such as DBSCAN or Gaussian mixtures may be more appropriate.

### Code-demonstrated concepts

The notebook uses code and plots to demonstrate:

- clustered synthetic blobs,
- the effect of feature scaling,
- fitted centroids and decision regions,
- the Voronoi-style partition induced by K-means,
- the elbow curve,
- silhouette-based comparison across values of `K`.

## [Source: decision_tree.ipynb]

### Decision trees as non-parametric supervised models

The notebook introduces decision trees as non-parametric supervised models that can perform both classification and regression. Classification trees end in class labels, while regression trees end in numeric predictions.

### Advantages, disadvantages, and CART

The source emphasizes their interpretability: decision trees can be displayed graphically and followed node by node. It also highlights two operational benefits:

- they work with qualitative and quantitative variables,
- they require little preprocessing.

Against that, the notebook preserves two major drawbacks:

- accuracy may be lower than that of stronger algorithms,
- trees are unstable, so small data changes can produce large structural changes.

The notebook also notes that scikit-learn uses the CART algorithm, which restricts trees to binary splits, unlike algorithms such as ID3 that can create nodes with more than two children.

### Classification and regression use

For classification, predictions correspond to the most frequent class in a terminal node. For regression, the prediction is the average of the training observations that fall into the same terminal node.

This difference in the prediction rule is treated as the core conceptual distinction between classification trees and regression trees.

### Comparison with linear regression and overfitting

Using the same salary-style regression setting as in the linear-regression notebook, the source shows that decision trees can capture non-linear relationships much more flexibly than a line.

The notebook then makes the trade-off explicit: that flexibility tends to overfit. Limiting depth, pruning, constraining leaf counts, or limiting split conditions are presented as ways to control this tendency.

An instructive edge case is preserved: even an extremely deep tree can still average predictions when different observations share the same predictor value, because the tree cannot split identical feature values apart indefinitely.

### Code-demonstrated concepts

The notebook uses code and plots to demonstrate:

- decision-tree classifiers and graphical tree visualization,
- regression trees on a salary-style dataset,
- the stronger fit of trees on non-linear patterns,
- the contrast between a shallow controlled tree and an unrestricted tree that overfits.

## [Source: random_forest.ipynb]

### Introduction and motivation

Random forests are introduced as an ensemble-learning method that combines many decision trees into a more robust and accurate model. The prerequisite of understanding decision trees is made explicit.

The notebook frames the entire method as a solution to one major weakness of single trees: deep individual trees tend to overfit and exhibit high variance.

### How random forests reduce overfitting

The source explains the ensemble principle as a form of "wisdom of the crowd": many diverse trees, each imperfect, can collectively generalize better than a single tree.

The aggregation rule depends on task type:

- classification uses majority voting,
- regression averages the predictions of all trees.

### The two main sources of randomness

The notebook identifies two specific randomness mechanisms:

1. bootstrap aggregating, where each tree is trained on a sample with replacement and typically sees about 63% of the original data,
2. random feature selection, where each split considers only a subset of features.

This diversity among trees is presented as the reason the ensemble can reduce variance.

### Algorithm steps and practical behavior

The notebook gives an explicit procedure: create many bootstrap samples, train one tree per sample with random feature subsets at each split, then aggregate the predictions.

For regression, the code-demonstrated comparison on the salary dataset emphasizes a practical consequence: the random-forest prediction curve is much smoother than the jagged curve produced by an overfitted single regression tree.

### Feature importance and hyperparameters

The notebook presents feature importance as one of the strengths of random forests. Importance is explained through impurity reduction accumulated across the forest.

It also gives a structured list of important hyperparameters and their effects:

- `n_estimators` trades computation for performance,
- `max_depth`, `min_samples_split`, and `min_samples_leaf` regulate overfitting and smoothness,
- `max_features` changes diversity across trees,
- `random_state` controls reproducibility,
- `n_jobs` controls parallel CPU usage.

### Advantages, disadvantages, and comparison with single trees

The notebook makes the trade-offs explicit.

Advantages include reduced overfitting, strong default accuracy, feature importance, robustness to outliers, and parallelizability.

Disadvantages include lower interpretability than a single tree, slower prediction, larger memory use, poor extrapolation beyond the training range, and possible overfitting on very noisy data.

The final comparison with a single decision tree is framed as a bias-variance trade-off: random forests sacrifice some interpretability and speed for far better robustness and generalization.

### Code-demonstrated concepts

The notebook uses code and plots to demonstrate:

- random-forest training for classification and regression,
- the contrast between an individual regression tree and a smoother forest prediction,
- feature-importance visualization,
- practical hyperparameter effects.

## [Source: knn.ipynb]

### Introduction and basic mechanics

The notebook presents KNN as a simple, effective, non-parametric, instance-based, and lazy supervised algorithm for both classification and regression. It explains prediction as a four-step process: compute distances, find the nearest neighbors, use majority vote for classification, and use averaging for regression.

The notebook reuses the classic `K = 3` versus `K = 5` example to show that changing neighborhood size can change the predicted class.

### Lazy learning and its consequences

The notebook gives a strong conceptual explanation of lazy learning: KNN learns by storing examples rather than by extracting a compact fitted model. This makes training almost costless but pushes the heavy computation into prediction time.

The computational trade-off is made explicit later through the stated complexities:

- training is `O(1)` because it mainly stores the data,
- prediction is `O(n × d)`, where `n` is the number of training samples and `d` the number of features.

### Distance calculation and simple classification example

The notebook walks through manual Euclidean-distance calculation to make the nearest-neighbor rule concrete. It then extends the same logic to larger datasets and decision-boundary visualizations.

### The critical importance of feature scaling

One of the notebook's strongest decision rules is that KNN requires feature scaling. Because distance metrics drive neighbor choice, a feature with a much larger numerical range can shadow a feature with a smaller range, even when both should matter equally.

The notebook preserves both the motivating example and the practical takeaway:

- without scaling, the large-range feature dominates distance,
- with scaling, both features contribute meaningfully,
- different predictions can result from scaled versus unscaled data.

The notebook explicitly recommends scaling methods such as StandardScaler, MinMaxScaler, and RobustScaler.

### KNN for regression

For regression, the notebook uses the same neighbor logic but averages neighbor values instead of voting. This is introduced first in a simple example and then in a more realistic dataset setting.

### Distance metrics

The notebook names and compares several metrics:

- Euclidean distance as the default,
- Manhattan distance,
- Minkowski distance as a generalization that includes the others as special cases.

### Advantages, disadvantages, and choosing K

The notebook combines several decision criteria:

- KNN works well as a simple baseline and on small to medium datasets,
- it is a poor fit for large datasets, high-dimensional data, memory-limited settings, or real-time prediction,
- the choice of `K` controls the bias-variance trade-off.

The guidance on `K` is explicit:

- `K = 1` is highly flexible but prone to overfitting,
- large `K` values oversmooth and can underfit,
- `sqrt(n)` is a common heuristic,
- odd `K` values help avoid ties in binary classification,
- cross-validation is the recommended way to choose the best `K`.

### Code-demonstrated concepts

The notebook uses code and visualizations to demonstrate:

- manual distance calculations in small examples,
- KNN decision boundaries on larger datasets,
- the effect of scaling versus not scaling,
- regression by neighbor averaging,
- the impact of different values of `K` on smoothness and fit.

# Cross-References

## Comparisons and distinctions

- Linear regression and logistic regression both begin from a linear combination of features, but linear regression predicts continuous values while logistic regression transforms the linear combination through a sigmoid to produce class probabilities. [Source: linear_regression.ipynb; Source: logistic_regression.ipynb]
- KNN and decision trees can both model non-linear decision boundaries, but KNN does so through local neighbor comparisons while trees do so through hierarchical splits. [Source: knn.md; Source: knn.ipynb; Source: decision_tree.ipynb]
- A single decision tree offers much higher interpretability than a random forest, while a random forest typically offers better generalization by reducing variance through aggregation. [Source: decision_tree.ipynb; Source: random_forest.ipynb]
- K-means and KNN both rely on distance, but K-means is unsupervised and groups points around centroids, whereas KNN is supervised and predicts labels or values from nearby labeled examples. [Source: kmeans.ipynb; Source: knn.md; Source: knn.ipynb]
- KNN and random forests are both flexible and powerful, but KNN pays the cost at prediction time by consulting stored examples, while random forests pay the cost by training and storing many trees. [Source: knn.md; Source: knn.ipynb; Source: random_forest.ipynb]

## Dependencies and prerequisites

- The historical introduction defines the high-level problem taxonomy that the later notebooks instantiate: regression, classification, clustering, and sequential decision-making. [Source: 00_introduction.md]
- Random forests depend conceptually on understanding decision trees, because the ensemble's purpose is to correct the variance and overfitting behavior of individual trees. [Source: decision_tree.ipynb; Source: random_forest.ipynb]
- The linear-regression notebook provides a foundation for logistic regression by introducing the predictor-target distinction, parameter fitting, and loss-minimization thinking before classification-specific probability modeling is added. [Source: linear_regression.ipynb; Source: logistic_regression.ipynb]
- The decision-tree regression example builds directly on the salary-style regression context introduced in the linear-regression notebook, making the overfitting contrast meaningful. [Source: linear_regression.ipynb; Source: decision_tree.ipynb]
- K-means and KNN both depend heavily on the learner understanding why feature scaling changes Euclidean-distance behavior. [Source: kmeans.ipynb; Source: knn.ipynb]

## Decision criteria and context-dependent choices

- Use linear regression when the target is continuous, interpretability matters, and a roughly linear relationship is plausible; move to multiple linear regression when more than one predictor is needed. [Source: linear_regression.ipynb]
- Use logistic regression when the target is categorical and the task is better framed as predicting class probability rather than a raw continuous value. [Source: logistic_regression.ipynb]
- Use K-means when unlabeled data must be grouped into compact clusters, but only after scaling the features and with awareness that the number of clusters must be chosen and may be ambiguous. [Source: kmeans.ipynb]
- Use KNN when a simple, local, similarity-based model is acceptable and dataset size is small or moderate; avoid it when prediction speed, memory efficiency, or high-dimensional robustness are critical. [Source: knn.md; Source: knn.ipynb]
- Use decision trees when human-readable decision rules are important and non-linear structure must be captured, but control overfitting through depth or pruning constraints. [Source: decision_tree.ipynb]
- Prefer random forests over single trees when predictive robustness and accuracy matter more than full interpretability, and when the added computational cost is acceptable. [Source: random_forest.ipynb]
