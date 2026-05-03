<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | numpy1.ipynb | `.ipynb` | ✅ |
| 2 | lists_nd_arrays_examples.ipynb | `.ipynb` | ✅ |
| 3 | numpy2_algebra.ipynb | `.ipynb` | ✅ |

# Content

## [Source: numpy1.ipynb]

### Introduction

NumPy is presented as a Python library for working with one-dimensional arrays (vectors), two-dimensional arrays (matrices), and arrays of higher dimension.

The notebook stresses three differences from ordinary Python lists:

- NumPy arrays are homogeneous: all elements share the same type.
- NumPy arrays have fixed size after creation.
- NumPy arrays are more efficient in time and memory because they are implemented in C++ and allow the element type to be declared explicitly.

NumPy is described as a foundational dependency for many data-science and machine-learning libraries, including pandas, Matplotlib, Seaborn, scikit-learn, TensorFlow, PyTorch, and Keras.

### Installation and importing NumPy

The material explains that NumPy must first be installed in the active environment. It mentions three installation routes: pip, Conda, and uv.

For importing, the notebook notes that the alias `np` is not mandatory but is the de facto standard in documentation and examples.

### Creating arrays from lists

The code demonstrates the conversion of a one-dimensional Python list into a one-dimensional NumPy array and of a list of lists into a two-dimensional NumPy array.

The observed contrast is that:

- the original Python container remains of type `list`,
- the NumPy container becomes an `ndarray`,
- two-dimensional input is preserved as a matrix-like structure.

The notebook then highlights the main structural properties of an array through a 2x3 example:

- number of dimensions: 2,
- shape: `(2, 3)`, meaning 2 rows and 3 columns,
- total number of elements: 6,
- element type: `int64` in the example.

### Data types for array elements

The notebook explains that NumPy array objects are always `ndarray` objects and that their element type is stored in the `dtype` attribute. Homogeneity is treated as a core rule: all elements are forced into a single common type.

When the type is not specified, NumPy infers it from the provided values. A list of integers therefore produces an integer array, while explicitly requesting a floating-point type converts the same values into `float64`.

The heterogeneous "students and grades" example is used as a warning. Combining student names with numeric grades inside the same array forces all values to become strings. The notebook treats this as conceptually poor for two reasons:

- it abandons NumPy's main advantage, which is efficient numerical work,
- it ties several parallel lists by position, which is error-prone when deleting or reordering elements.

The recommended alternatives are:

- group each student with their grades as a tuple or object when the dataset is modest,
- use a richer tabular structure such as a Pandas DataFrame when efficient processing over many records is needed.

### NaN

The notebook presents `NaN` as a special floating-point value for representing numeric values that are not real numbers while preserving a numeric dtype. The central comparison is against `None`:

- `NaN` remains a float and keeps mathematical operations possible,
- `None` would force the array into object dtype and break normal numerical behavior.

An example array containing `NaN` is shown to become a floating-point array automatically.

### Accessing elements

Array access is described through row and column indices that start at 0. In the 3x4 example matrix:

- the first element is the one at row 0, column 0,
- the last element is the one at row 2, column 3,
- selecting a single row returns that row's values.

The material makes the row/column interpretation explicit by writing the matrix in mathematical notation and mapping each position to its zero-based coordinates.

### Basic functions to create arrays

The notebook demonstrates several array constructors and the concepts they illustrate:

- arrays filled with zeros or ones,
- use of a shape tuple to create matrices rather than flat vectors,
- creation of three-dimensional arrays,
- ability to choose the dtype explicitly.

Several quantitative edge cases are preserved in the examples:

- zero-filled and one-filled arrays default to `float64` unless another type is requested,
- an unsigned 8-bit integer sequence starting at 254 wraps after 255 and continues as `0, 1, 2`, illustrating overflow,
- an uninitialized array may contain leftover memory values because its elements are not set,
- a fully filled array adopts the type implied by the fill value unless a dtype is forced explicitly.

### Random number generation

The notebook introduces NumPy's random number generator through a generator object. The examples demonstrate two common tasks:

- generating a matrix of random real numbers between 0 and 1,
- generating a matrix of random integers in a bounded range.

The important teaching content is the output range and shape of the generated arrays, not the specific sampled numbers.

### Functions to create vectors following sequences

Two sequence-generation ideas are demonstrated:

- evenly stepping through a numeric interval, analogous to Python's `range` but returning a NumPy array,
- generating a fixed number of evenly spaced values between two endpoints.

The example with five evenly spaced values between 0 and 10 produces `0, 2.5, 5, 7.5, 10`.

### Reshape

Reshaping is presented as the conversion of a flat vector into a matrix while preserving the underlying elements. The notebook highlights three key ideas:

- a 12-element vector can be reorganized as a 3x4 matrix,
- the first dimension corresponds to rows and the second to columns,
- using `-1` in one dimension delegates inference of that dimension to NumPy.

The notebook also shows the special case of turning a one-dimensional vector into a single-column matrix.

### Slicing

Slicing is described as analogous to list slicing. The notebook preserves the conceptual rules rather than only the notation:

- a slice selects a contiguous segment from a start position up to, but not including, a stop position,
- start or stop may be omitted to mean the beginning or the end,
- a third value can specify the step,
- negative indices count from the end,
- a negative step traverses the array backwards and can be used for reversal.

The matrix examples then ground those rules in two dimensions:

- selecting one row while keeping all columns,
- selecting one column across all rows,
- distinguishing between a selected column returned as a vector and the same column preserved as a single-column matrix,
- extracting a prefix of a row,
- extracting submatrices with row and column ranges.

### Filtering

Filtering is introduced with boolean masks. One example uses an explicit mask `[True, False, True, False]` to keep only the first and third elements of a vector.

The notebook then moves to condition-based filtering with comparisons and logical combinations. The demonstrated cases include:

- keeping values below a threshold,
- keeping values equal to or different from a target value,
- combining conditions with logical OR and logical AND,
- observing that the chosen OR condition in the example retains the entire array because every value satisfies at least one side of the condition.

Filtering is also shown as a mechanism for modifying arrays in place:

- values below 10 are replaced by 0 in a vector of squared integers,
- odd values are replaced by 0 inside a 3x4 matrix.

### Mathematical operations

The notebook demonstrates common aggregate operations over a vector with values `9, 10, 1, 2, 2, 3, 3, 3, 4, 5, 6, 7, 8`.

The preserved quantitative anchors are:

- maximum: `10`, at index `1`,
- minimum: `1`, at index `2`,
- sum: `63`,
- mean: `4.846153846153846`,
- cumulative sum: `9, 19, 20, 22, 24, 27, 30, 33, 37, 42, 48, 55, 63`,
- standard deviation: `2.797`,
- variance: `7.822`.

For matrices, the notebook explains axes explicitly:

- operations without an axis use all elements,
- axis 0 aggregates by columns,
- axis 1 aggregates by rows.

In the 3x4 example matrix, the total sum is `78`, column sums are `15, 18, 21, 24`, and row sums are `10, 26, 42`.

### Operations on matrices

The sorting examples compare two styles of use:

- a sorting function that returns a sorted copy and leaves the original vector unchanged,
- an array method that sorts the array in place and returns nothing.

The `unique` examples preserve two different ideas:

- the set of unique values can be extracted from a vector,
- auxiliary outputs can also report the first index of each unique value or the frequency of each value.

The frequency example is then converted into a dictionary by pairing each unique value with its count.

The `flip` example demonstrates reversing the order of a vector.

## [Source: lists_nd_arrays_examples.ipynb]

### Function that receives a list and returns another one removing duplicates

#### List-based solutions for duplicate removal

Several list-based strategies are demonstrated for removing duplicates while keeping the first occurrence:

- iterate over the input and append only values not yet present in the output list,
- express the same idea through comprehension syntax,
- scan earlier positions only, using the fact that an element should be kept only if it has not appeared before the current index,
- write the same previous-position logic in an imperative style.

The notebook contrasts those solutions with set conversion, which removes duplicates but loses the original order.

The tests preserve important type-related edge cases:

- duplicated integers are collapsed while preserving first appearance order in the manual list solutions,
- converting through a set can move `1` to the beginning even when it appeared later,
- `True` is treated as equal to `1`, so duplicates involving those values collapse together,
- the string `'1'` is not equal to the integer `1`, so both can remain as distinct values.

#### NumPy solution for duplicate removal

The NumPy-based solution uses the library's built-in unique-value extraction. Its observed behavior differs from the list-based versions in two important ways:

- returned values are sorted,
- original order is therefore lost.

The same mixed-type edge cases are revisited. On boolean and integer mixtures, truth values collapse into the same numeric category as `1`. On mixtures of strings and numbers, the result becomes entirely string-valued.

#### Variant: removing duplicates from ndarrays

The ndarray version reinforces that the same unique-value operation can be applied directly to arrays.

One important nuance is made explicit: when an ndarray is created from mixed boolean and integer values, the conversion to a common numeric dtype happens at array-creation time, not later during duplicate removal. The example array containing `True` is shown to become an integer array.

The notebook also remarks that NumPy chooses a dtype into which all values can be cast. When strings and numbers are mixed, the values are converted to strings.

### Function that receives a list of lists and returns another one removing duplicates

The demonstrated algorithm removes duplicates globally across the full list of sublists, not independently inside each sublist.

The procedure is:

- keep a set of all values already seen,
- process the sublists in order,
- within each sublist, preserve only values not yet seen anywhere earlier,
- append the resulting reduced sublist to the output.

The examples show two consequences of this design:

- later sublists may shrink to a single value if most values were already seen,
- a later sublist may become empty if every element had already appeared in previous sublists.

### Function that receives a NumPy matrix and returns another one replacing repeated values with NaN

The notebook uses this task to connect duplicate handling with NumPy typing rules.

The procedure first converts the matrix to floating-point type because `NaN` is a floating-point marker. It then traverses the matrix, keeping a set of already seen values and replacing every later repetition with `NaN`.

Two important observations are preserved:

- the first appearance of each value is kept,
- the original integer matrix shown in the example remains unchanged after the function call because the float conversion creates a separate array.

The examples show both an extreme case, where two whole repeated rows become all `NaN`, and a mixed case, where only later repeated elements are replaced.

### Function that receives a list and returns a dictionary with the number of times each element appears

#### List-based frequency-count solution

The list-based solution builds a frequency dictionary by incrementing the count for each element encountered.

The outputs preserve the same equality edge cases seen earlier:

- repeated integers accumulate counts normally,
- `True` and `1` collapse into the same key because they compare equal,
- `'1'` and `1` remain distinct when both are present in an ordinary Python list.

#### NumPy frequency-count solution

The NumPy version obtains both unique values and their counts, then pairs them into a dictionary.

Relative to the pure-list version, the important behavioral differences are again driven by dtype coercion:

- boolean values merge with `1`, producing a numeric key,
- mixing strings and numbers converts the result to strings, so the counts appear under string keys such as `'1'`, `'2'`, and so on.

#### NumPy-only counting variant for ndarrays

The second NumPy counting variant counts, for each unique value, how many positions satisfy equality with that value.

The notebook explicitly notes that this formulation is specific to ndarrays because equality against a scalar produces a boolean array there. The observed type behavior matches the previous NumPy frequency solution.

### Function that receives two square matrices and returns a third matrix with 1 where the values of A and B match and 0 otherwise

#### List-based equality-matrix solution

The list-based solution compares two matrices position by position and writes `1` when the values match and `0` otherwise.

With the provided 3x3 example, the result is the identity matrix, because only the diagonal positions contain equal values in both inputs.

The notebook leaves one validation requirement unresolved: it notes that the implementation should verify that both matrices are square and have the same size.

#### NumPy equality-matrix solution

The NumPy versions express the same logical idea through array-wise comparison and conversion of the boolean result into zeros and ones.

The conceptual equivalence with the list-based version is preserved: corresponding positions are compared element by element, and equal positions become `1`.

### Function that receives a matrix and finds its saddle points

The notebook defines saddle points primarily as values that are row maxima and column minima. It also includes an optional broader mode that additionally accepts values that are row minima and column maxima.

#### List-based saddle-point solution

The list-based solution is intentionally written for readability. Its procedure is:

- process the matrix row by row,
- identify the maximum value in the current row,
- keep every column position where that row maximum appears,
- for each such position, check whether the same value is the minimum of its column,
- optionally repeat the symmetric logic for row minima that are column maxima,
- store coordinates in a set so the same coordinate is not duplicated if it satisfies both definitions.

The tests preserve a rich set of cases and edge cases:

- in the strictly increasing 3x3 matrix, the default interpretation yields `(0, 2)`, while the broader interpretation also adds `(2, 0)`,
- in a matrix whose last row is constant and centered between the others, the point `(2, 1)` satisfies both interpretations but appears only once,
- an empty matrix returns an empty list,
- if all elements are equal, every position is a saddle point,
- additional nontrivial test matrices show cases with one saddle point, several saddle points, and multiple repeated values creating several valid coordinates.

The preserved quantitative outcomes for the additional matrices are:

- matrix 5 yields `(4, 0)` in the broader mode,
- matrix 6 yields `(0, 4)`,
- matrix 7 yields `(1, 0)`, `(1, 2)`, `(2, 2)`, `(3, 2)`, `(4, 0)`, `(4, 2)`,
- matrix 8 yields `(0, 1)`, `(0, 4)`, `(2, 1)`, `(2, 2)`, `(2, 3)`, `(2, 4)`.

The notebook adds two interpretation notes:

- in most applications, only the row-maximum/column-minimum definition is used,
- the omitted symmetric case could also be computed by transposing the matrix.

#### NumPy saddle-point solution

The NumPy solution preserves the same logic but uses array maxima and minima on rows and columns. It explicitly handles the empty-matrix case before iterating.

All test cases pass in the NumPy version as well, so the conceptual behavior is the same as in the list-based implementation.

## [Source: numpy2_algebra.ipynb]

### Identity matrix

The notebook demonstrates two equivalent ways to create an identity matrix. In the 4x4 example, both produce a matrix with ones on the main diagonal and zeros elsewhere.

It then extends the idea by shifting the diagonal one position upward, producing a matrix whose ones no longer lie on the main diagonal. This is used to distinguish the general diagonal-construction capability from the specific identity-matrix case.

### Transpose matrix

The transpose is defined operationally as swapping rows and columns.

The examples show two consequences:

- a 2x3 matrix becomes a 3x2 matrix after transposition,
- extracting a column from the original matrix is equivalent to extracting the corresponding row from the transpose.

The notebook treats the transpose not only as an algebraic operation but also as a practical aid for certain access patterns.

### Matrix operations

#### Matrix operations with scalars

Arithmetic with a scalar is described as applying that scalar independently to every matrix element.

The examples demonstrate:

- addition and subtraction of a constant,
- multiplication and division by a constant,
- exponentiation applied element by element,
- square root computed element by element.

#### Element-wise operations

For two matrices of the same shape, addition, subtraction, multiplication, and division are presented as pairwise operations between corresponding elements.

The example using the identity matrix and a 2x2 numeric matrix makes the distinction visible:

- addition and subtraction affect each position independently,
- element-wise multiplication keeps only the diagonal values from the second matrix when multiplied by the identity matrix,
- element-wise division also happens position by position.

#### Matrix multiplication (matrix product)

Matrix multiplication is explained as multiplying each row of the first matrix by each column of the second, summing those products, and placing the sum in the corresponding position of the result.

The notebook works through the concrete example:

- first row of the result: `38` and `17`,
- second row of the result: `26` and `14`.

It explicitly warns that matrix multiplication must not be confused with element-wise multiplication.

The operation is described as vitally important in computing, with the notebook naming image processing, machine learning, cryptography, data compression, simulation of physical systems, and solving systems of linear equations as application areas.

# Cross-References

## Comparisons and distinctions

- Python lists versus NumPy arrays: the notebook contrasts the flexibility of lists with NumPy's homogeneous, fixed-size, memory-efficient arrays designed for numerical work. [Source: numpy1.ipynb, Introduction]
- Useful heterogeneous structures versus poor NumPy fits: combining names and grades in one array forces all values to strings and defeats numerical efficiency; the material recommends tuples/objects or a Pandas DataFrame instead. [Source: numpy1.ipynb, Data types for array elements]
- `NaN` versus `None` for missing numeric values: `NaN` preserves floating-point numeric behavior, while `None` would push the structure into object dtype. [Source: numpy1.ipynb, NaN]
- Column as vector versus column as single-column matrix: the slicing examples distinguish between extracting a column as a one-dimensional result and preserving two-dimensional shape. [Source: numpy1.ipynb, Slicing]
- Copy-returning sort versus in-place sort: one form leaves the original vector unchanged, while the other mutates the array itself. [Source: numpy1.ipynb, Operations on matrices]
- List-based duplicate removal versus NumPy unique-value extraction: manual list solutions preserve first appearance order, while the NumPy solution sorts the result and loses original order. [Source: lists_nd_arrays_examples.ipynb, Function that receives a list and returns another one removing duplicates]
- Python-list typing versus ndarray coercion: in ordinary lists, `'1'` and `1` remain distinct, while ndarray creation can coerce mixed values to a common dtype; `True` also collapses with `1` because they compare equal. [Source: numpy1.ipynb, Data types for array elements; lists_nd_arrays_examples.ipynb, duplicate-removal and frequency-count sections]
- Element-wise multiplication versus matrix multiplication: the algebra notebook treats these as fundamentally different operations and warns explicitly not to confuse them. [Source: numpy2_algebra.ipynb, Matrix operations]

## Dependencies and prerequisites

- Understanding dimensions, shape, rows, and columns is a prerequisite for indexing, slicing, reshaping, axis-based aggregation, transpose, and matrix multiplication. [Source: numpy1.ipynb, Creating arrays from lists; Accessing elements; Reshape; Mathematical operations; numpy2_algebra.ipynb, Transpose matrix; Matrix multiplication]
- Reshaping depends on preserving the total number of elements; automatic inference of one dimension is presented as a convenience layered on top of that constraint. [Source: numpy1.ipynb, Reshape]
- Axis-based matrix aggregations build directly on the row/column interpretation introduced in the indexing and shape sections. [Source: numpy1.ipynb, Accessing elements; Mathematical operations]
- The transpose section builds on matrix indexing and is then reused as a practical tool for accessing columns through rows. [Source: numpy2_algebra.ipynb, Transpose matrix]
- Replacing repeated matrix values with `NaN` depends on the earlier typing idea that `NaN` is a float marker, so the matrix must first become floating-point. [Source: numpy1.ipynb, NaN; lists_nd_arrays_examples.ipynb, repeated values with NaN]
- Saddle-point detection depends on comparing row extrema with column extrema; the broader variant adds the symmetric comparison in the opposite direction. [Source: lists_nd_arrays_examples.ipynb, saddle points]

## Decision criteria and context-dependent choices

- Specify dtype explicitly when the intended numeric representation matters; otherwise NumPy will infer a common type that may coerce values in undesirable ways. [Source: numpy1.ipynb, Data types for array elements]
- Use `NaN` rather than `None` when missing values must remain numerically operable. [Source: numpy1.ipynb, NaN]
- Choose a heterogeneous list/object/DataFrame representation instead of a NumPy array when the task is not primarily numerical and would otherwise force strings or other awkward mixed data. [Source: numpy1.ipynb, Data types for array elements]
- Keep the first occurrence order with manual list-based duplicate removal; choose the NumPy unique-value route when sorted unique values are acceptable and order preservation is not required. [Source: lists_nd_arrays_examples.ipynb, duplicate-removal section]
- Distinguish whether a selected column should behave as a vector or remain a single-column matrix, because the notebook shows both forms intentionally. [Source: numpy1.ipynb, Slicing]
- Use the non-mutating sorting route when the original data must be preserved, and the in-place route when mutation is acceptable. [Source: numpy1.ipynb, Operations on matrices]
- In most applications, interpret saddle points only as row maxima that are column minima; the broader symmetric interpretation is optional and explicitly separated. [Source: lists_nd_arrays_examples.ipynb, saddle points]
- The equality-matrix task assumes same-size square matrices in the worked example, and the notebook explicitly notes that input validation for shape constraints is still missing. [Source: lists_nd_arrays_examples.ipynb, equal-values matrix]
