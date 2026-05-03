<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | 01-eda.ipynb | `.ipynb` | ✅ |
| 3 | 02-repeated_ids.ipynb | `.ipynb` | ✅ |
| 4 | 03-temporal_leakage.ipynb | `.ipynb` | ✅ |
| 5 | 04a-preprocessing-step-by-step.ipynb | `.ipynb` | ✅ |
| 6 | 04b-preprocessing-pipeline.ipynb | `.ipynb` | ✅ |

# Content

## [Source: README.md]

The README frames the repository as an end-to-end house-price regression project built around the messiness of real-world tabular data.

Its core teaching themes are:

- exploratory analysis,
- duplicate-like records that are not actually bad data,
- temporal leakage,
- feature engineering and preprocessing,
- model selection with train/validation/test discipline.

This means the repository is not just another housing-price exercise. It is designed to teach how dataset structure and evaluation protocol can break an otherwise competent model.

## [Source: 01-eda.ipynb]

The EDA notebook establishes the King County dataset as a richer and messier regression problem than the simpler California examples.

Its main observations are:

- the target price is strongly right-skewed,
- some numeric features are also heavily skewed and may need log transforms,
- `id` is an identifier rather than a predictor,
- `date` encodes temporal information that matters for modeling,
- `zipcode` is high-cardinality and may be less useful than direct geographic information,
- location and house-quality variables are major price drivers.

A key design decision appears here already: represent time as a continuous trend feature such as `days_since_start` rather than as seasonal categories, because the dataset spans roughly one year and is better suited to modeling market drift than robust annual seasonality.

## [Source: 02-repeated_ids.ipynb]

This notebook is conceptually one of the strongest in the repository because it distinguishes duplicated identifiers from duplicated observations.

Its central argument is:

- repeated `id` values usually mean the same property was sold more than once,
- those repeated rows are distinct sales with different dates and prices,
- therefore they are valid observations rather than data-quality duplicates.

From that, the notebook makes two different decisions:

- drop `id` as a raw model feature because it is an identifier and would encourage memorization,
- keep the repeated-sale rows because they contain valid market information over time.

It also introduces a useful nuance: an identifier can be useless as a direct feature but still valuable as a relational key in richer production systems, for example to build lag features from prior sales.

## [Source: 03-temporal_leakage.ipynb]

This notebook defines the repository's main methodological guardrail.

It explains temporal leakage as the error of letting models learn from future observations to predict past ones, then shows why random train/test splits are misleading for time-ordered housing data.

The practical recommendations are:

- sort by time,
- train on older observations,
- validate on later observations,
- keep the newest test set untouched until final evaluation,
- use `TimeSeriesSplit` when cross-validation is needed.

Conceptually, this notebook turns time from a mere feature into a constraint on how the entire ML workflow must be organized.

## [Source: 04a-preprocessing-step-by-step.ipynb]

The step-by-step preprocessing notebook translates the earlier EDA and leakage concerns into a manual, inspectable workflow.

It covers:

- parse raw dates before splitting,
- perform temporal train/validation/test splitting,
- engineer temporal, age, and ratio features,
- drop non-predictive or replaced columns,
- log-transform skewed numeric features,
- standardize numeric inputs,
- verify that the preprocessing behaves consistently across splits,
- save processed artifacts and reference values.

Pedagogically, this notebook is important because it shows the logic in slow motion before hiding it inside a production pipeline.

## [Source: 04b-preprocessing-pipeline.ipynb]

The pipeline notebook packages the earlier preprocessing logic into an end-to-end sklearn-compatible artifact.

Its structure is explicit:

- parse raw date strings,
- engineer derived features while learning the reference `min_date_` from training data only,
- apply numeric preprocessing in a final transformer stage.

The major conceptual win is leakage resistance by design. Because fitted parameters such as the temporal reference point are learned only from training data and reused later through `transform()`, the pipeline enforces the same methodological boundaries that the earlier notebooks argued for.

It also introduces the production idea that preprocessing should accept raw input data directly and be saved as a single reusable artifact.

# Cross-References

## Internal progression of the foundations unit

- The README frames the project, `01-eda` identifies the important data characteristics, `02-repeated_ids` resolves the identity question, and `03-temporal_leakage` establishes the correct evaluation protocol. Together they define what kind of regression problem this really is. [Source: README.md; Source: 01-eda.ipynb; Source: 02-repeated_ids.ipynb; Source: 03-temporal_leakage.ipynb]
- `04a` then turns those findings into a manual preprocessing workflow, while `04b` packages the same logic into a reusable pipeline. [Source: 04a-preprocessing-step-by-step.ipynb; Source: 04b-preprocessing-pipeline.ipynb]

## Recurring methodological themes

- The decision to keep repeated-sale records only makes sense together with the temporal-leakage notebook: older sales are valid training evidence for later sales, but only when time ordering is respected. [Source: 02-repeated_ids.ipynb; Source: 03-temporal_leakage.ipynb]
- The temporal feature engineering in `01-eda` is operationalized in `04a` and then made leakage-safe in `04b` through a fitted `min_date_` parameter learned on training data only. [Source: 01-eda.ipynb; Source: 04a-preprocessing-step-by-step.ipynb; Source: 04b-preprocessing-pipeline.ipynb]
- The repository repeatedly prefers explicit fit/transform boundaries over ad hoc dataframe manipulation because those boundaries are what prevent contamination between training, validation, and test data. [Source: 03-temporal_leakage.ipynb; Source: 04a-preprocessing-step-by-step.ipynb; Source: 04b-preprocessing-pipeline.ipynb]

## Decision criteria and trade-offs

- Drop identifiers like `id` as direct features when they invite memorization and do not encode meaningful predictive structure. [Source: 01-eda.ipynb; Source: 02-repeated_ids.ipynb]
- Keep repeated records when they represent distinct transactions over time rather than accidental duplicates. [Source: 02-repeated_ids.ipynb]
- Prefer temporal splits over random splits when the target process evolves over time and the deployment scenario is future-facing. [Source: 03-temporal_leakage.ipynb]
- Use a manual preprocessing walkthrough when the goal is learning and auditability; use a pipeline when the goal is reproducibility, end-to-end inference, and integration with model-selection tools. [Source: 04a-preprocessing-step-by-step.ipynb; Source: 04b-preprocessing-pipeline.ipynb]
- Favor continuous time-trend features over fragile seasonal encodings when the data window is short and trend is more identifiable than periodicity. [Source: 01-eda.ipynb; Source: 04a-preprocessing-step-by-step.ipynb]
