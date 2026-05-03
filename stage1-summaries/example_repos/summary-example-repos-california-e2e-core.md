<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | types_estimators.md | `.md` | ✅ |
| 3 | e2e010_framing.ipynb | `.ipynb` | ✅ |
| 4 | e2e020_eda.ipynb | `.ipynb` | ✅ |
| 5 | e2e025_train_test.ipynb | `.ipynb` | ✅ |
| 6 | e2e030_feature_engineering.ipynb | `.ipynb` | ✅ |
| 7 | e2e041_missing.ipynb | `.ipynb` | ✅ |
| 8 | e2e042_categorical.ipynb | `.ipynb` | ✅ |
| 9 | e2e043_scaling.ipynb | `.ipynb` | ✅ |

# Content

## [Source: README.md]

The README defines the project as an end-to-end supervised regression walkthrough built on the California Housing dataset. Its role is curricular: the notebook sequence is meant to guide the learner from problem framing and exploratory analysis through preprocessing and then, in later units, to pipelines, evaluation, and optimization.

The split used in this Stage 1 artifact corresponds to the conceptual and preprocessing half of that journey:

- framing the regression problem,
- understanding the data,
- building train/test methodology,
- creating better features,
- handling missing data,
- encoding categorical variables,
- scaling numeric features.

## [Source: types_estimators.md]

This short note clarifies scikit-learn terminology that the notebooks rely on repeatedly.

- An estimator is anything that learns from data through `fit()`.
- A transformer is an estimator that can also transform data through `transform()`.
- A predictor is an estimator that can produce outputs through `predict()`.

The note further subdivides transformers into scalers, imputers, encoders, and dimensionality reducers, and predictors into classifiers, regressors, and clusterers. It also warns about overloaded terminology: `predictor` can mean either a model that predicts or a predictive feature, and `transformer` in scikit-learn is unrelated to transformer neural networks.

Conceptually, this note is the vocabulary bridge that makes the preprocessing notebooks easier to read.

## [Source: e2e010_framing.ipynb]

The framing notebook establishes the task: predict median house value by California district using census-derived features. It is explicit that the dataset is useful pedagogically despite being old and partially preprocessed.

Several important caveats are introduced very early:

- the dataset is small by modern ML standards but sufficient for teaching,
- `ocean_proximity` is categorical even though most columns are numeric,
- some variables are capped, including the target,
- several variables are right-skewed and may require later transformation.

The notebook then turns these observations into formal problem framing:

- the target variable is continuous,
- the task is supervised learning,
- the specific supervised task is regression.

It also provides one of the clearest metric discussions in the project. RMSE is chosen as the main evaluation measure, but the notebook carefully distinguishes performance metrics from loss functions and explains why RMSE is preferred over MAE in this housing context: large pricing errors are especially undesirable and RMSE aligns naturally with MSE-based optimization.

## [Source: e2e020_eda.ipynb]

The EDA notebook studies the full dataset before splitting, while warning that insights gathered during exploration must not be fitted directly on future test data.

Its main themes are:

- geographic visualization using latitude and longitude,
- housing value and population overlays,
- categorical geography through `ocean_proximity`,
- pairwise correlations and scatter plots,
- explicit discussion of outliers and capped values.

The strongest empirical finding is that `median_income` is the most correlated feature with `median_house_value`. The notebook also uses the visible horizontal cap on house values to reinforce the earlier warning that preprocessing choices embedded in the dataset can distort downstream modeling.

The outlier section is particularly valuable because it compares capping, Winsorizing, and truncation, then ties those choices to concrete downstream consequences for imputation, scaling, and model training.

## [Source: e2e025_train_test.ipynb]

This notebook establishes the methodological heart of the project: train/test separation exists to detect overfitting and estimate generalization.

It first demonstrates random sampling using both NumPy and scikit-learn, then emphasizes reproducibility through `random_state`. After that it motivates stratified sampling by showing how purely random sampling can misrepresent the population distribution.

The notebook chooses stratification based on a discretized `median_income` attribute, because income is a strong driver of housing price. But it also preserves an important methodological caveat: the text explicitly questions whether stratifying by a predictor is truly the best choice and argues that, in many supervised settings, discretizing the target and stratifying by the target would be more rigorous.

This makes the notebook unusually reflective: it teaches Geron-style stratification as a practical method while also criticizing it as potential pedagogical simplification.

The final major section explains data leakage in three forms:

- feature leakage through preprocessing on the full dataset,
- target leakage through features that encode future or derived information,
- model-selection leakage through repeated use of the test set.

This notebook is also where the project starts pointing beyond pure explanation toward reusable utilities, since it mentions that the demonstrated split is consolidated later into a data-loading helper.

## [Source: e2e030_feature_engineering.ipynb]

The feature-engineering notebook turns EDA observations into derived attributes. Its central idea is that raw counts such as total rooms or total bedrooms are less informative than ratios normalized by household structure.

The main constructed features are:

- rooms per household,
- population per household,
- bedroom ratio.

The key conclusion is that `bedrooms_ratio` correlates with house value much better than the raw room counts. The notebook therefore teaches feature engineering as a domain-driven search for more meaningful quantities rather than a mechanical increase in feature count.

It also explicitly foreshadows a later engineering boundary: in a real pipeline, these transformations should become custom transformers so that train and test data are transformed consistently.

## [Source: e2e041_missing.ipynb]

This notebook treats missing numerical values as both a practical preprocessing problem and a statistical one.

It starts by clarifying terminology around missing data: missing values, NA, NaN, null, and `None` may be used loosely, but the real issue is whether the missingness carries information.

The notebook then introduces the three classic missingness mechanisms:

- MCAR: missing completely at random,
- MAR: missing at random given observed variables,
- MNAR: missing not at random.

That conceptual section matters because it frames imputation as a modeling decision rather than a clerical repair step.

From there, the notebook compares several practical options:

- delete incomplete rows,
- delete the full column,
- impute with a central tendency statistic,
- use predictive imputation such as KNN.

For this dataset, median imputation is defended as a reasonable default because `total_bedrooms` has relatively few missing values and the median is robust to outliers. The notebook then shows how `SimpleImputer` encapsulates this logic cleanly and can return either NumPy arrays or Pandas output.

## [Source: e2e042_categorical.ipynb]

The categorical-feature notebook focuses on the `ocean_proximity` attribute and explains why most ML algorithms prefer numeric representations.

It first considers ordinal encoding, but rejects it for this case because even if some coast-related ordering exists, the categories do not form a clear meaningful numerical progression. Treating them as ordered would inject a false geometry into the feature space.

That leads to the notebook's main recommendation: one-hot encoding.

The notebook uses this section to teach several engineering points at once:

- one-hot encoding turns a category into multiple binary columns,
- sparse outputs save memory when most entries are zero,
- `OneHotEncoder` remembers training categories whereas `pandas.get_dummies()` does not,
- unknown categories at test time can either trigger an error or be ignored explicitly.

So the notebook is not only about encoding categories, but also about why fit/transform separation matters operationally.

## [Source: e2e043_scaling.ipynb]

The scaling notebook explains why many ML algorithms fail or behave poorly when features live on very different numeric scales.

It distinguishes normalization from standardization, while also warning that terminology is inconsistent across subfields. Then it compares two major approaches:

- Min-Max scaling, which maps values into a chosen range but is highly sensitive to outliers,
- standardization with `StandardScaler`, which centers at zero and scales by standard deviation.

The notebook also addresses a subtler point often skipped in beginner materials: scaling the target variable can make sense for some gradient-based or distance-based models, but if the target is transformed then predictions must eventually be inverse-transformed as well.

Its final major theme is heavy-tailed distributions. These are presented as problematic because they destabilize gradients, distort distances, and make coefficients harder to interpret. The notebook recommends logarithmic transformation to compress the right tail, followed by standard scaling so transformed features remain comparable.

# Cross-References

## Conceptual dependencies inside the unit

- The framing notebook introduces capped values, skewed variables, and the regression target; the EDA, missing-values, and scaling notebooks each deepen one of those initial warnings. [Source: e2e010_framing.ipynb; Source: e2e020_eda.ipynb; Source: e2e041_missing.ipynb; Source: e2e043_scaling.ipynb]
- The estimator terminology note is the vocabulary layer underneath the rest of the unit: imputers, encoders, scalers, regressors, and predictors all appear later as concrete scikit-learn objects. [Source: types_estimators.md; Source: e2e041_missing.ipynb; Source: e2e042_categorical.ipynb; Source: e2e043_scaling.ipynb]
- EDA naturally motivates feature engineering: once `median_income` and room-related quantities emerge as informative, the next step is to build better attributes from those raw signals. [Source: e2e020_eda.ipynb; Source: e2e030_feature_engineering.ipynb]

## Methodological guardrails

- The EDA notebook permits looking at the full dataset for understanding, but the train/test notebook sharply defines the boundary between exploration and leakage. Together they teach that inspecting data is allowed, fitting transformations on future test information is not. [Source: e2e020_eda.ipynb; Source: e2e025_train_test.ipynb]
- The stratified-sampling section, the missing-values notebook, and the scaling notebook all revolve around the same broader concern: preprocessing choices must preserve representative structure without leaking information from outside training data. [Source: e2e025_train_test.ipynb; Source: e2e041_missing.ipynb; Source: e2e043_scaling.ipynb]
- The notebook on categorical variables reinforces the same fit/transform discipline as the imputation and scaling notebooks by showing why learned preprocessing state must come from training data. [Source: e2e041_missing.ipynb; Source: e2e042_categorical.ipynb; Source: e2e043_scaling.ipynb]

## Decision criteria and trade-offs

- Prefer RMSE when large regression mistakes should be penalized strongly and when alignment with MSE-based optimization is desirable; prefer MAE when robustness to large outliers matters more. [Source: e2e010_framing.ipynb]
- Prefer median imputation over mean imputation when outliers or heavy tails make the mean unstable. [Source: e2e020_eda.ipynb; Source: e2e041_missing.ipynb]
- Prefer one-hot encoding when categorical values do not have a trustworthy ordinal structure; use ordinal encoding only when the order itself is meaningful. [Source: e2e042_categorical.ipynb]
- Prefer standardization over min-max scaling when outliers or heavy-tailed features would distort range-based normalization. [Source: e2e020_eda.ipynb; Source: e2e043_scaling.ipynb]
- Treat the train/test split as a methodological firewall: never let preprocessing, model comparison, or feature design fit itself to the test set. [Source: e2e025_train_test.ipynb]
