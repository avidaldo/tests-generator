<!-- markdownlint-disable MD025 MD032 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | pandas_structures.ipynb | `.ipynb` | ✅ |
| 2 | pandas_dataframe_op.ipynb | `.ipynb` | ✅ |
| 3 | df_from_structures.ipynb | `.ipynb` | ✅ |
| 4 | pandas_transformations.ipynb | `.ipynb` | ✅ |

# Content

## [Source: pandas_structures.ipynb]

### Introduction

pandas is presented as a library for data manipulation and analysis, created in 2008 in response to the increasing use of Python in scientific applications that had traditionally been dominated by R, MATLAB, or SAS. The notebook states that pandas builds on the maturity and stability of NumPy and SciPy, and that its name comes from Panel Data, a common term in statistics and econometrics for multidimensional datasets.

The introduction highlights these capabilities:
- Easy importing from CSV, JSON, Excel, SQL, and similar sources.
- Manipulation operations such as selection, filtering, and aggregation.
- Data cleaning.
- Data wrangling or data munging, understood as transforming data between formats.

The notebook identifies three pandas structures:
- Series: one-dimensional array.
- DataFrame: two-dimensional array.
- Panel: three-dimensional array.

### Series

The notebook defines a Series as a one-dimensional array containing both a sequence of values and a sequence of labels associated with those values, called an index. It stresses that the main difference from a NumPy vector is the presence of this explicit index, which can be of any immutable type. The analogy given is that Series indexes behave like dictionary indexes, while NumPy indexes behave like list indexes.

### Structure

The notebook demonstrates that a Series can be created from:
- A list, producing an implicit integer index starting at 0.
- A dictionary, where keys become explicit indexes and values become Series values.
- A list plus an explicitly provided index.

The examples show that Series are not restricted to numeric values. One example stores theatre seat occupancy, using seat numbers as explicit numeric indexes and passenger names as values. The outputs also show that pandas infers a dtype from the stored values, such as numeric dtypes for numbers and object dtype for strings.

### Accessing Elements of a Series

The notebook warns that one must distinguish between positions and indexes, especially when the explicit index is numeric. In that case, a numeric label can be mistaken for a positional reference if the distinction is not kept clear.

The conceptual rule presented is:
- Use position-based access when you mean ordinal position in the Series.
- Use label-based access when you mean the explicit index.

The examples demonstrate two cases:
- With numeric explicit indexes, label-based access to seat 7 and position-based access to the second element both return the same student only because that label happens to be stored in that position. Accessing a non-existent explicit label such as 0 would fail.
- With string explicit indexes, label-based access retrieves a named student, while position-based access retrieves the first element by order. The notebook explicitly warns that bare integer access on a string-indexed Series currently behaves positionally but emits a FutureWarning and is being removed because it is error-prone.

The notebook also shows label-based modification of values, including assigning a single student grade and assigning a slice from a given label to the end. On the modified series of grades, the reported descriptive values are:
- Mean: 7.5
- Standard deviation: 2.886751345948129
- Count: 4
- Minimum: 5
- 25%: 5
- 50%: 7.5
- 75%: 10
- Maximum: 10

### DataFrame

The DataFrame is defined as a two-dimensional tabular data structure with labeled rows and columns. The notebook compares it to a relational database table in SQL and explains that it can be regarded as a collection of Series sharing the same index. It is described as the most commonly used pandas structure.

### Structure of a DataFrame

The notebook first shows that a DataFrame can be created from a single Series by assigning a column name.

It then demonstrates a more important case: building a DataFrame from a mixture of one Series column and several list-based columns. In that construction, the index of the Series is used to define the row labels of the DataFrame.

An explicit counterexample is included: if an explicit row index is supplied and one name is wrong, the Series-based column cannot find a value for that label and produces NaN, while the list-based columns still fill by position. The notebook explains the trade-off clearly:
- A dictionary of lists avoids label-mismatch NaN caused by a wrong index label.
- However, relying only on positions is not robust, because adding a student or changing student order can silently reassign grades to the wrong person.
- A dictionary of Series with explicit indexes is therefore presented as the more robust solution, because the labels keep the rows aligned correctly even when the Series appear in different orders.

The notebook then demonstrates this robust case by creating several subject-grade Series with student names as explicit indexes. Even when one subject is listed in a different order, the resulting DataFrame aligns all grades by student name rather than by position.

The notebook also gives two warnings about using strings as indexes in data analysis:
- String identifiers may not be unique.
- The same real entity may appear under spelling variations, different capitalization, or different formatting in different data sources.

This warning is reinforced by an example in which inconsistent student names across two Series produce multiple mismatched rows full of NaN. The notebook connects this to relational database design, noting that databases typically use unique primary keys, often surrogate integer keys with no intrinsic meaning.

### Information About a DataFrame

The notebook shows the kinds of metadata that are useful for understanding a DataFrame:
- Structural information reports 4 entries, 5 data columns, all of type float64, and memory usage of 192 bytes.
- A preview operation returns the first rows; in the example there are only 4 rows, but the notebook explains that this is especially useful for large datasets.
- Shape reports the number of rows and columns as (4, 5).
- Column labels can be inspected as an Index object.
- Data types are available per column.
- Row indexes can be inspected directly.

### Writing and Reading Data Files

The notebook explains that pandas provides many functions for importing and exporting data. The concrete example uses CSV as a storage format.

The conceptual point is that when a DataFrame is saved to CSV and then read back:
- If the first CSV column is declared as the explicit index during reading, the original row labels are restored as the DataFrame index.
- If this is not declared, pandas creates a new implicit numeric index and the former explicit index becomes an ordinary data column named `Unnamed: 0`.

## [Source: pandas_dataframe_op.ipynb]

### Notebook Scope

This notebook is introduced as covering basic DataFrame manipulation: how to access, modify, filter, and organize data within a DataFrame. The stated topics are column and row management, element access and slicing, filtering and sorting, and basic aggregations on columns.

The notebook also explicitly positions itself relative to another source: advanced transformations, multi-aggregation grouping, element-wise operations such as map, apply, and transform, and reshaping with melt and pivot are deferred to the transformations notebook.

### Column Management

The notebook demonstrates three main ways of changing columns:
- Inserting a new column at a specific position.
- Adding a new column at the end by assignment.
- Creating a computed column from existing columns.

The examples show these concepts:
- Adding a column by assignment creates it if it does not exist and overwrites it if it already exists.
- A normalized grade column can be derived from an original grade column by rescaling values between the observed minimum and maximum. In the example, the resulting normalized values are 1.0, 0.615385, 0.615385, and 0.0.

Deletion is used to distinguish between returning a modified copy and mutating the original DataFrame:
- Removing a column without an in-place mutation returns a new DataFrame and leaves the original unchanged.
- The notebook states that the row axis is the default target, so deleting columns requires selecting the column axis instead.
- It also states that an in-place mutation changes the original DataFrame itself instead of returning a new one.

The notebook additionally explains that one can specify columns or indexes directly when deleting, instead of reasoning only in terms of axes.

The assign-based examples add an important design distinction:
- Direct assignment mutates the current DataFrame.
- assign returns a new DataFrame and is presented as cleaner for method chaining.
- In a single chained assign, later computed columns may depend on columns created earlier in the same call.

### Row Management

The notebook shows that selecting a row by its label yields a complete row as a Series.

When adding a new row, the notebook highlights a dependency issue: a normalized column cannot be filled correctly by looking only at the new row, because its value depends on the full grade column. The example therefore inserts NaN into the normalized column to indicate that the value is temporarily unavailable and must be recomputed after processing the full column.

The complementary deletion example shows that dropping a row can return a new DataFrame without modifying the original if the change is not done in place.

### Accessing Elements

This section distinguishes scalar access by labels from scalar access by positions. The notebook demonstrates that the same scalar can be reached by several routes when the row label and column label are known, including direct label-based access and position-based access.

It also demonstrates label-based and position-based updates to the DataFrame, showing that both can mutate stored values.

A particularly important warning appears when both row and column labels are integers. In that situation, a label-based lookup and a position-based lookup using the same numbers can return different values, because one interprets the numbers as labels and the other interprets them as positions.

The notebook comments on access choices as follows:
- Label-based scalar access is presented as the fastest choice when retrieving or setting a single labeled value.
- A more flexible label-based selector can retrieve single values, rows, columns, or slices.
- Chained indexing works, but is discouraged because it is less efficient and may lead to SettingWithCopyWarning.

### Accessing Parts of a DataFrame

The notebook distinguishes between selecting one column as a DataFrame and selecting one column as a Series. It also shows that, when column names allow it, attribute-style access can retrieve a column similarly to bracket-based selection.

It then demonstrates selecting multiple columns together and selecting one row together with a subset of columns.

### Slicing

The slicing examples highlight the distinction between label-based and position-based slicing:
- A label-based slice over columns from PIA to MIA includes both endpoints and therefore returns PIA, SAA, and MIA.
- A position-based slice over rows and columns uses ordinal positions rather than labels.
- A label-based row slice up to Marvin Minsky includes the endpoint label in the result.

### Creating a New DataFrame by Applying Filters

The notebook uses boolean filtering to derive new DataFrames from the original one.

The example cases are:
- Students who passed both PIA and SAA.
- Students who passed PIA or SAA, while keeping a selected subset of grade columns.

The notebook then shows that the filtered result can be reindexed by DNI so that students are identified by that field instead of by name. It also shows the same transformation written as a single chained expression, illustrating a compact workflow that combines filtering, reindexing, and column selection.

### Sorting

Sorting is presented in two forms:
- Sorting by one column in descending order.
- Sorting by multiple columns with an explicit priority order.

The notebook makes the priority rule explicit: when multiple sort keys are provided, the earlier columns take precedence over the later ones.

### Basic Aggregations

The notebook introduces simple statistical summaries over columns and rows.

The reported examples include:
- Mean of the modified PIA column: 6.04.
- Sum by column, including 143 for age, 30.2 for PIA, 41.5 for SAA, 33.0 for MIA, 46.0 for SBD, 40.6 for BDA, and 2.230769 for the normalized PIA column.
- Row-wise averages across the five module columns: 9.18 for Alan Turing, 5.98 for Claude Shannon, 7.56 for John McCarthy, 7.94 for Marvin Minsky, and 7.60 for Arthur Samuel.
- Frequency counts for SBD, where four students have 9.0 and one student has 10.0.

Missing-value inspection is also covered:
- Two null-checking methods are shown as equivalent.
- The example DataFrame has exactly one missing value, located in the normalized PIA column for Arthur Samuel.
- Counting nulls by column confirms that only PIA_norm contains a missing value, with a count of 1.

## [Source: df_from_structures.ipynb]

### Create a DataFrame Incorporating Different Data Structures

This notebook is almost entirely demonstrative code, but the demonstrated concept is clear: pandas can assemble one DataFrame from heterogeneous Python and pandas data structures as long as the data are brought into a common indexing scheme.

The example combines grade data coming from:
- A dictionary mapping student names to grades.
- A list of student-grade pairs.
- A collection of student-grade pairs converted into a mapping.
- A plain list of grades.
- A NumPy array of grades.
- A pandas Series with an implicit numeric index.
- A pandas Series with an explicit student-name index.
- A pandas Series created from a dictionary.

The code-demonstrated procedure is:
- Use label-aware structures directly when they already identify students.
- For positional structures such as lists, arrays, or Series without the desired labels, attach the intended student-name index first.
- Then assemble all modules into one DataFrame so that each row corresponds to a student and each column corresponds to a module.

The resulting table shows that pandas can integrate multiple source structures into a single DataFrame once a common row index has been established.

## [Source: pandas_transformations.ipynb]

### Notebook Scope and Prerequisites

This notebook is introduced as covering advanced pandas operations for transforming, aggregating, and reshaping data. It explicitly states that it assumes familiarity with basic DataFrame operations such as indexing, filtering, and sorting.

The covered topics are:
- Element-wise operations: map, apply, transform.
- Grouping operations: groupby, agg, group-wise transform, and group-wise apply.
- Reshaping: melt, pivot, and pivot_table.

### Element-wise Operations: map, apply, transform

### map

map is presented as a Series-only operation that applies a function, dictionary, or another Series element by element.

The notebook associates map with two main use cases:
- Replacing values using a dictionary or function.
- Simple element-wise transformation on a single column.

The examples demonstrate that:
- A function can shift all math grades upward by 5 points.
- A dictionary can convert group labels A, B, and C into Alpha, Beta, and Gamma.
- If the dictionary does not contain a key, map returns NaN for that missing case. In the example, omitting C makes all C-group entries become NaN.

The notebook adds an explicit decision rule: if the goal is dictionary-based replacement but missing keys should keep their original values, replace is preferable to map. The example shows A and B being replaced while C remains C.

### apply

apply is presented as more versatile than map:
- On a Series, it behaves like an element-wise transformation.
- On a DataFrame, it applies a function along an axis.

The examples demonstrate three important behaviors:
- Applying to a Series can produce the same element-wise result as map.
- Applying to DataFrame columns can compute per-column summaries such as range. In the example, the column ranges are 16 for math, 20 for physics, and 23 for chemistry.
- Applying to DataFrame rows can compute row-level summaries such as row means. The resulting student means are 80.0, 87.666667, 80.0, 91.666667, 87.666667, and 72.666667.

The notebook makes a key conceptual point explicit: when apply is used on a DataFrame, the function receives a whole Series representing a column or a row, not individual scalar values.

### transform

transform is defined by one essential property: it always returns a result with the same shape as the input.

The notebook frames this as crucial for two tasks:
- Broadcasting group-level calculations back to individual rows.
- Preserving alignment with the original DataFrame.

The examples show that transform can perform ordinary element-wise transformations on a Series, and can also normalize whole numeric columns while still returning a table with the same row and column structure as the input.

### Comparison: When to Use Each

The notebook provides a direct comparison among map, apply, and transform:
- map works only on Series, receives individual values, preserves shape, and is best for simple replacements or element-wise changes.
- apply works on Series and DataFrames, receives either scalar-like values or full Series depending on context, and may return a result with a different shape; it is suited for flexible operations and aggregations.
- transform works on Series and DataFrames, receives Series, must preserve input shape, and is especially useful for normalization and for broadcasting group-level results.

The notebook reinforces the comparison with two concrete distinctions:
- All three can produce the same element-wise result in a simple Series example that adds 5 to each math grade.
- Only map accepts dictionaries directly, while only apply can reduce dimensionality. transform would broadcast a sum instead of reducing the object to a smaller result.

### Grouping Operations

### groupby: Split-Apply-Combine

groupby is explained through the split-apply-combine pattern:
1. Split the data into groups based on one or more keys.
2. Apply a function to each group independently.
3. Combine the results into a new structure.

The notebook demonstrates a grouped dataset with three groups, A, B, and C, each containing two students. It shows that one can inspect the grouped object, iterate over groups, retrieve a specific group, and compute group means.

The example means are:
- Math by group: A = 87.5, B = 85.0, C = 82.0.
- Multi-subject group means:
  - A: math 87.5, physics 82.5, chemistry 81.5.
  - B: math 85.0, physics 85.0, chemistry 87.5.
  - C: math 82.0, physics 80.0, chemistry 78.5.

### agg: Multiple Aggregations

agg is presented as the operation for applying multiple aggregation functions at once, including different aggregation choices per column.

The examples preserve several distinctions:
- A single aggregation can reproduce a simple group mean.
- One column can be summarized with multiple statistics such as mean, standard deviation, minimum, and maximum.
- Multiple columns can each receive multiple summary statistics.
- Different columns can use different aggregation logic in the same grouped summary.
- Named aggregations produce cleaner, purpose-driven output column names.

Concrete quantitative examples include:
- Math mean and standard deviation by group: A = 87.5 and 3.535534, B = 85.0 and 9.899495, C = 82.0 and 8.485281.
- Physics ranges in the named aggregation example: A = 5, B = 6, C = 20.
- Chemistry standard deviations in the same example: A = 9.192388, B = 10.606602, C = 9.192388.

### transform with groupby: Broadcasting Group Results

The notebook contrasts grouped apply with grouped transform by shape:
- A grouped apply of the mean returns one value per group.
- A grouped transform of the mean returns one value per original row, repeating the group statistic for each member of the group.

This is then used to create new aligned columns:
- A column with each student's group-average math grade.
- A within-group normalized math score, where each two-student group yields symmetric standardized values of approximately -0.707107 and 0.707107.
- A within-group descending rank for math, yielding rank 1 or 2 inside each group.

### apply with groupby: Flexible Group Operations

Grouped apply is described as the most flexible grouped option because the function receives the entire group as a DataFrame and may return:
- A scalar.
- A Series.
- A DataFrame.

Two demonstrations are given:
- A scalar-valued group spread in math grades, with spreads A = 5, B = 14, and C = 12.
- A DataFrame-valued selection of the top math student in each group, yielding Bob for A, Diana for B, and Eve for C.

### Summary: agg vs transform vs apply with groupby

The notebook states the core distinction among the grouped methods:
- agg reduces each group to one summary row.
- transform preserves the original shape and broadcasts group statistics back to rows.
- apply is the flexible option for custom logic and more complex return types.

### The assign Method

assign is presented as a way to create new columns while returning a new DataFrame rather than modifying the original one. The notebook emphasizes its usefulness for method chaining.

The examples preserve three main ideas:
- assign can reproduce the same derived-column result as a traditional copy-and-mutate approach.
- A lambda inside assign can reference the DataFrame currently being transformed.
- Multiple columns can be created in one call, and later columns may depend on earlier newly created columns.

The multi-column example computes:
- An average grade per student.
- A passed indicator based on whether that average is at least 80.
- A group average of those student averages, broadcast back to each row.

The reported values show that all students except Frank satisfy the average-at-least-80 condition. The group-average values are 83.833333 for group A, 85.833333 for group B, and 80.166667 for group C.

The notebook also includes a chained workflow that computes per-student averages, keeps only students with average at least 80, and sorts them from highest to lowest average. The resulting order is Diana, Eve, Bob, Alice, and Charlie.

### Reshaping Data: melt and pivot

### Wide vs Long Format

The notebook distinguishes between two organizational formats:
- Wide format: each variable has its own column.
- Long format: variable names are stacked into one column and their values into another.

It states that different analyses require different formats, and frames melt as the wide-to-long operation and pivot as the long-to-wide operation.

### melt: Wide to Long

melt is described as unpivoting a DataFrame from wide format to long format.

The examples show that:
- Identifier columns can be preserved while subject columns are stacked into a subject column and a grade column.
- If the value columns are not specified explicitly, all non-identifier columns are melted.

The notebook also explains when long format is useful:
- Aggregating across categories, such as computing the average grade per subject.
- Working with visualization libraries that prefer long format.
- Filtering by category more easily.

The reported aggregates from the long-format table are:
- Average grade per subject: chemistry 82.5, math 84.833333, physics 82.5.
- Average grade per group and subject:
  - Group A: chemistry 81.5, math 87.5, physics 82.5.
  - Group B: chemistry 87.5, math 85.0, physics 85.0.
  - Group C: chemistry 78.5, math 82.0, physics 80.0.

### pivot and pivot_table: Long to Wide

pivot is presented as the long-to-wide reshaping operation. The notebook shows it reconstructing a wide table using student and group as identifiers, subjects as columns, and grades as values.

An important edge case is made explicit: pivot fails when multiple values would need to occupy the same cell. The demonstrated error is that duplicate entries in the index-column combination make reshaping impossible without aggregation.

### pivot_table: Handles Duplicates with Aggregation

pivot_table is presented as the version that can handle duplicates because it aggregates them, using the mean by default.

The notebook demonstrates that pivot_table can:
- Aggregate duplicate group-subject combinations into one wide table.
- Apply multiple aggregation functions at once, such as mean and standard deviation.
- Add overall totals through margins.

The example with margins reports:
- Group A overall average: 83.833333.
- Group B overall average: 85.833333.
- Group C overall average: 80.166667.
- Overall grand mean across all groups and subjects: 83.277778.

### pivot_table vs groupby + agg

The notebook states that pivot_table is essentially a groupby followed by reshaping. It demonstrates equivalence between:
- A pivot_table that aggregates mean grade by group and subject.
- A grouped mean by group and subject followed by unstacking.

### Summary

The closing summary table assigns a distinct purpose to each operation:
- map for Series-only element-wise mapping.
- apply for flexible transformation across Series, rows, or columns.
- transform for same-shape transformations.
- groupby as the foundation for split-apply-combine workflows.
- agg for multi-aggregation summaries.
- assign for fluent addition of columns.
- melt for wide-to-long reshaping.
- pivot for long-to-wide reshaping when entries are unique.
- pivot_table for long-to-wide reshaping when duplicates require aggregation.

# Cross-References

## Comparisons and distinctions

- Series vs NumPy vectors: the structures notebook explains that a Series has an explicit index of any immutable type, while a NumPy vector uses an implicit positional index. The analogy given is dictionary-style indexes for Series versus list-style indexes for NumPy arrays. [Source: pandas_structures.ipynb §Series]
- DataFrame vs relational tables: the DataFrame is explicitly compared to a relational SQL table, with labeled rows and columns and the interpretation that it can be seen as a collection of aligned Series. [Source: pandas_structures.ipynb §DataFrame]
- Dictionary of Series vs dictionary of lists for DataFrame construction: lists avoid label-mismatch NaN when a wrong explicit index is introduced, but they are less robust because reordering or inserting students can silently reassign grades by position. A dictionary of Series is presented as more robust because labels control alignment. [Source: pandas_structures.ipynb §Structure of a DataFrame]
- Label-based vs position-based access: both the Series material and the DataFrame operations notebook warn that label-based and position-based lookups are conceptually different, and that numeric labels make the distinction especially error-prone. [Source: pandas_structures.ipynb §Accessing Elements of a Series; Source: pandas_dataframe_op.ipynb §Accessing Elements]
- map vs apply vs transform: the transformations notebook distinguishes them by the kind of object they operate on, what the function receives, whether shape can change, and their best-fit use cases. [Source: pandas_transformations.ipynb §Comparison: When to Use Each]
- agg vs transform vs apply on grouped data: agg summarizes groups, transform preserves original shape and broadcasts group results, and apply is the flexible custom-logic option. [Source: pandas_transformations.ipynb §Summary: agg vs transform vs apply with groupby]
- Wide vs long format and pivot vs pivot_table: melt turns wide data into long data; pivot reconstructs wide data only when each cell is unique; pivot_table is used when duplicates must be aggregated. [Source: pandas_transformations.ipynb §Wide vs Long Format; Source: pandas_transformations.ipynb §pivot and pivot_table: Long to Wide]

## Dependencies and prerequisites

- The transformations notebook explicitly requires familiarity with basic DataFrame operations such as indexing, filtering, and sorting, which are the subject of the DataFrame operations notebook. [Source: pandas_transformations.ipynb §Overview; Source: pandas_dataframe_op.ipynb §Overview]
- The DataFrame operations notebook loads a CSV file of grades; the structures notebook is the one that demonstrates writing that grades DataFrame to CSV and reading it back with or without restoring the explicit index. [Source: pandas_dataframe_op.ipynb §Overview; Source: pandas_structures.ipynb §Writing and Reading Data Files]
- The row-management example in the DataFrame operations notebook depends on the normalization idea introduced earlier in the same notebook: the normalized column cannot be updated row by row because it depends on the full grade column. [Source: pandas_dataframe_op.ipynb §Column Management; Source: pandas_dataframe_op.ipynb §Row Management]
- Group-wise transform in the transformations notebook depends on understanding both transform's same-shape guarantee and groupby's split-apply-combine structure. [Source: pandas_transformations.ipynb §transform; Source: pandas_transformations.ipynb §groupby: Split-Apply-Combine; Source: pandas_transformations.ipynb §transform with groupby: Broadcasting Group Results]
- The heterogeneous DataFrame-construction example in df_from_structures depends on the alignment rules and explicit-index logic explained more fully in the structures notebook. [Source: df_from_structures.ipynb §Create a DataFrame Incorporating Different Data Structures; Source: pandas_structures.ipynb §Series; Source: pandas_structures.ipynb §Structure of a DataFrame]

## Decision criteria and context-dependent choices

- When the identity of rows matters and misalignment would be dangerous, the source recommends constructing DataFrames from label-aware Series rather than only from positional lists. [Source: pandas_structures.ipynb §Structure of a DataFrame]
- When using string-based identifiers in analytical data, the source warns that they can be non-unique or inconsistently written, which motivates the use of unique surrogate keys in database-style designs. [Source: pandas_structures.ipynb §Structure of a DataFrame]
- When a dictionary mapping is incomplete and the desired behavior is to preserve unmatched original values, replace is preferred over map; map is appropriate when unmatched keys should become NaN. [Source: pandas_transformations.ipynb §map]
- When the goal is to add derived columns without mutating the original DataFrame and while supporting chained workflows, assign is preferred over direct assignment. [Source: pandas_dataframe_op.ipynb §Column Management; Source: pandas_transformations.ipynb §The assign Method]
- When the result must stay aligned with the original rows, especially after grouping, transform is the appropriate choice; when the goal is one summary row per group, agg is appropriate; when custom per-group logic or non-standard return types are needed, apply is the flexible option. [Source: pandas_transformations.ipynb §transform; Source: pandas_transformations.ipynb §agg: Multiple Aggregations; Source: pandas_transformations.ipynb §apply with groupby: Flexible Group Operations]
- When an analysis or visualization benefits from categorical stacking and grouped summaries by category, long format is useful; when each observation-variable combination is unique, pivot can restore a wide layout; when duplicates exist, pivot_table is required because it aggregates them. [Source: pandas_transformations.ipynb §melt: Wide to Long; Source: pandas_transformations.ipynb §pivot and pivot_table: Long to Wide; Source: pandas_transformations.ipynb §pivot_table: Handles Duplicates with Aggregation]
