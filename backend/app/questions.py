QUESTION_BANK = {
    "python_basics": [
        {"id": "python_basics_1", "type": "mcq", "text": "Which keyword defines a function in Python?", "options": ["def", "func", "function", "lambda"], "answer": "def"},
        {"id": "python_basics_2", "type": "mcq", "text": "What does the len() function return for a list?", "options": ["Its length", "Its last element", "Its type", "Its memory address"], "answer": "Its length"},
        {"id": "py_short_1", "type": "two_liner", "text": "Explain the difference between a list and a tuple in Python in 2 sentences.", "rubric": "Lists are mutable, tuples are immutable; lists use square brackets, tuples use parentheses."},
        {"id": "py_short_2", "type": "two_liner", "text": "What is a Python decorator and when would you use one?", "rubric": "A function that modifies the behavior of another function without directly altering its source code."},
        {"id": "py_para_1", "type": "paragraph", "text": "Discuss the Global Interpreter Lock (GIL) in CPython and how it affects multi-threaded programs.", "rubric": "GIL prevents true parallel execution of Python bytecode across multiple CPU cores. Workarounds include using multiprocessing or alternative implementations."}
    ],
    "numpy_pandas": [
        {"id": "numpy_pandas_1", "type": "mcq", "text": "Which NumPy function creates evenly spaced values?", "options": ["np.arange()", "np.linspace()", "Both A and B", "np.create()"], "answer": "Both A and B"},
        {"id": "numpy_pandas_2", "type": "mcq", "text": "Which Pandas object represents a single column of data?", "options": ["Series", "DataFrame", "Index", "Array"], "answer": "Series"},
        {"id": "np_short_1", "type": "two_liner", "text": "Explain the difference between a NumPy array and a Python list.", "rubric": "NumPy arrays are homogenous and support vectorised operations; lists can contain mixed types and are slower."},
        {"id": "np_short_2", "type": "two_liner", "text": "What is broadcasting in NumPy?", "rubric": "Broadcasting allows NumPy to perform operations on arrays of different shapes by virtually stretching the smaller array."},
        {"id": "np_para_1", "type": "paragraph", "text": "Discuss how memory layout impacts performance in NumPy multi-dimensional array operations.", "rubric": "Memory layout like C-contiguous vs Fortran-contiguous affects cache locality and traversal speed during matrix operations."}
    ],
    "linear_algebra": [
        {"id": "linear_algebra_1", "type": "mcq", "text": "What is the result of multiplying a matrix by the identity matrix?", "options": ["The original matrix", "A zero matrix", "Its transpose", "Its inverse"], "answer": "The original matrix"},
        {"id": "linear_algebra_2", "type": "mcq", "text": "What does the dot product of two orthogonal vectors equal?", "options": ["0", "1", "-1", "Undefined"], "answer": "0"},
        {"id": "la_short_1", "type": "two_liner", "text": "What geometric interpretation does the determinant of a matrix provide?", "rubric": "It represents the scaling factor of a linear transformation for a region of space or volume."},
        {"id": "la_short_2", "type": "two_liner", "text": "What does it mean for a square matrix to be invertible?", "rubric": "Its determinant is non-zero, it has full rank, and multiplying it by its inverse yields the identity matrix."},
        {"id": "la_para_1", "type": "paragraph", "text": "Explain Principal Component Analysis (PCA) using linear algebra concepts like eigenvectors and eigenvalues.", "rubric": "PCA finds orthogonal axes of maximum variance by computing eigenvectors and eigenvalues of the covariance matrix."}
    ],
    "probability": [
        {"id": "probability_1", "type": "mcq", "text": "What is the probability of an event that is certain to happen?", "options": ["1", "0", "0.5", "Undefined"], "answer": "1"},
        {"id": "probability_2", "type": "mcq", "text": "If two events are independent, P(A and B) equals?", "options": ["P(A)*P(B)", "P(A)+P(B)", "P(A)-P(B)", "P(A)/P(B)"], "answer": "P(A)*P(B)"},
        {"id": "prob_short_1", "type": "two_liner", "text": "State Bayes' Theorem in words and explain its purpose.", "rubric": "It updates the probability of a hypothesis given new evidence using prior knowledge and likelihood."},
        {"id": "prob_short_2", "type": "two_liner", "text": "What is the difference between a discrete and a continuous probability distribution?", "rubric": "Discrete distributions deal with countable outcomes using PMFs; continuous deal with infinite values using PDFs."},
        {"id": "prob_para_1", "type": "paragraph", "text": "Explain the Law of Large Numbers and how it bridges theoretical probability with empirical frequency.", "rubric": "As sample size increases, the sample mean converges closer to the expected value of the underlying distribution."}
    ],
    "statistics": [
        {"id": "statistics_1", "type": "mcq", "text": "Which measure is most sensitive to outliers?", "options": ["Mean", "Median", "Mode", "Range"], "answer": "Mean"},
        {"id": "statistics_2", "type": "mcq", "text": "What does standard deviation measure?", "options": ["Spread of data around the mean", "The middle value", "The most frequent value", "The total count"], "answer": "Spread of data around the mean"},
        {"id": "stat_short_1", "type": "two_liner", "text": "Why might the median be preferred over the mean for household income data?", "rubric": "Income data is heavily skewed by extreme upper-bound outliers, making median a better measure of central tendency."},
        {"id": "stat_short_2", "type": "two_liner", "text": "What is the Central Limit Theorem and why is it important?", "rubric": "It states that the sampling distribution of the mean approaches a normal distribution as sample size grows large."},
        {"id": "stat_para_1", "type": "paragraph", "text": "Discuss the implications of Type I and Type II errors in hypothesis testing with a practical example.", "rubric": "Type I error is a false positive (rejecting true null); Type II is a false negative (failing to reject false null). Trade-offs depend on the application context."}
    ],
    "regression": [
        {"id": "regression_1", "type": "mcq", "text": "What does linear regression assume about the relationship between variables?", "options": ["It is linear", "It is exponential", "It is categorical", "It is cyclical"], "answer": "It is linear"},
        {"id": "regression_2", "type": "mcq", "text": "Which metric is commonly used to evaluate regression models?", "options": ["Mean Squared Error", "Accuracy", "F1 Score", "Precision"], "answer": "Mean Squared Error"},
        {"id": "reg_short_1", "type": "two_liner", "text": "What is multicollinearity and how does it affect linear regression?", "rubric": "High correlation among predictor features destabilizes coefficient estimates and inflates standard errors."},
        {"id": "reg_short_2", "type": "two_liner", "text": "Explain the difference between L1 (Lasso) and L2 (Ridge) regularization.", "rubric": "L1 adds absolute penalty causing feature sparsity; L2 adds squared penalty shrinking coefficients smoothly."},
        {"id": "reg_para_1", "type": "paragraph", "text": "Walk through the process of diagnosing a linear regression model using residual plots.", "rubric": "Checking residual plots helps detect non-linearity, heteroscedasticity, non-normality, and outlier leverage points."}
    ],
    "classification": [
        {"id": "classification_1", "type": "mcq", "text": "Which algorithm is commonly used for binary classification?", "options": ["Logistic Regression", "Linear Regression", "K-Means", "PCA"], "answer": "Logistic Regression"},
        {"id": "classification_2", "type": "mcq", "text": "What does a confusion matrix summarize?", "options": ["Prediction outcomes vs actual labels", "Feature correlations", "Data distribution", "Model architecture"], "answer": "Prediction outcomes vs actual labels"},
        {"id": "class_short_1", "type": "two_liner", "text": "When should you use F1-score instead of accuracy?", "rubric": "F1-score is ideal for imbalanced class datasets where high accuracy can be misleading due to majority class dominance."},
        {"id": "class_short_2", "type": "two_liner", "text": "What is the role of the sigmoid function in logistic regression?", "rubric": "It maps any real-valued number into a bounded probability range between 0 and 1."},
        {"id": "class_para_1", "type": "paragraph", "text": "Explain how a Support Vector Machine (SVM) finds the optimal decision boundary using kernels.", "rubric": "SVM maximizes the margin between classes using hyperplanes, applying kernel tricks to project data into higher dimensions for separation."}
    ],
    "model_evaluation": [
        {"id": "model_evaluation_1", "type": "mcq", "text": "What does an ROC curve plot?", "options": ["True Positive Rate vs False Positive Rate", "Precision vs Recall", "Loss vs Epochs", "Accuracy vs Time"], "answer": "True Positive Rate vs False Positive Rate"},
        {"id": "model_evaluation_2", "type": "mcq", "text": "What does k-fold cross-validation help prevent?", "options": ["Overfitting to a single train/test split", "Underfitting", "Data leakage", "Class imbalance"], "answer": "Overfitting to a single train/test split"},
        {"id": "eval_short_1", "type": "two_liner", "text": "Why is stratified k-fold cross-validation preferred for imbalanced classes?", "rubric": "It ensures each fold preserves the same percentage of target class samples as the overall dataset."},
        {"id": "eval_short_2", "type": "two_liner", "text": "What does the Area Under the ROC Curve (AUC-ROC) measure?", "rubric": "It measures a model's overall capability to discriminate between positive and negative classes across thresholds."},
        {"id": "eval_para_1", "type": "paragraph", "text": "Compare precision and recall, and explain how shifting the decision threshold impacts both metrics.", "rubric": "Precision evaluates exactness of positive predictions; recall measures completeness. Lowering thresholds increases recall while reducing precision."}
    ],
    "optimization": [
        {"id": "optimization_1", "type": "mcq", "text": "What does gradient descent minimize?", "options": ["A loss function", "A dataset", "A learning rate", "A matrix"], "answer": "A loss function"},
        {"id": "optimization_2", "type": "mcq", "text": "What can happen if the learning rate is too high?", "options": ["The model may fail to converge", "Training becomes slower", "The model overfits", "Nothing changes"], "answer": "The model may fail to converge"},
        {"id": "opt_short_1", "type": "two_liner", "text": "What is the issue with standard gradient descent at saddle points?", "rubric": "Gradient magnitudes approach zero, causing updates to slow down drastically or stall."},
        {"id": "opt_short_2", "type": "two_liner", "text": "How does momentum help gradient descent converge faster?", "rubric": "It builds velocity using past gradients to accelerate along consistent paths and dampen oscillations."},
        {"id": "opt_para_1", "type": "paragraph", "text": "Explain how adaptive learning rate algorithms like Adam work compared to standard SGD.", "rubric": "Adam combines first-moment momentum with second-moment RMSprop scaling to adapt independent learning rates for every parameter."}
    ],
    "neural_networks": [
        {"id": "neural_networks_1", "type": "mcq", "text": "What is the role of an activation function?", "options": ["Introduce non-linearity", "Store weights", "Load data", "Reduce dataset size"], "answer": "Introduce non-linearity"},
        {"id": "neural_networks_2", "type": "mcq", "text": "What algorithm is used to update weights in a neural network?", "options": ["Backpropagation", "Bubble sort", "K-means", "Dijkstra's algorithm"], "answer": "Backpropagation"},
        {"id": "nn_short_1", "type": "two_liner", "text": "What is the vanishing gradient problem in deep networks?", "rubric": "Gradients decay exponentially during backpropagation through deep layers using saturating activations."},
        {"id": "nn_short_2", "type": "two_liner", "text": "What is the purpose of dropout regularization?", "rubric": "It randomly deactivates a fraction of neurons during training to prevent co-adaptation and reduce overfitting."},
        {"id": "nn_para_1", "type": "paragraph", "text": "Describe the forward and backward propagation loops in a multi-layer perceptron.", "rubric": "Forward propagation computes network predictions and loss; backward propagation applies chain-rule derivatives to update weights."}
    ],
    "excel_basics": [
        {"id": "excel_basics_1", "type": "mcq", "text": "Which Excel function returns the average of a range?", "options": ["AVERAGE", "SUM", "COUNT", "MAX"], "answer": "AVERAGE"},
        {"id": "excel_basics_2", "type": "mcq", "text": "What does a pivot table help you do?", "options": ["Summarize and aggregate data", "Write macros", "Connect to a database", "Design charts only"], "answer": "Summarize and aggregate data"},
        {"id": "excel_short_1", "type": "two_liner", "text": "What is the difference between VLOOKUP and XLOOKUP?", "rubric": "VLOOKUP searches left-to-right with column indexes; XLOOKUP searches any direction and defaults to exact matches."},
        {"id": "excel_short_2", "type": "two_liner", "text": "How do absolute references ($ symbol) work in Excel?", "rubric": "They anchor specific row or column coordinates so they remain fixed when formulas are dragged or copied."},
        {"id": "excel_para_1", "type": "paragraph", "text": "Explain how to design a structured financial dashboard using named ranges and dynamic tables.", "rubric": "Organizing raw data into tables, defining named ranges, using structured references, and keeping layouts clean."}
    ],
    "sql_basics": [
        {"id": "sql_basics_1", "type": "mcq", "text": "Which SQL clause is used to filter rows?", "options": ["WHERE", "SELECT", "ORDER BY", "GROUP BY"], "answer": "WHERE"},
        {"id": "sql_basics_2", "type": "mcq", "text": "Which keyword retrieves data from a table?", "options": ["SELECT", "INSERT", "UPDATE", "DELETE"], "answer": "SELECT"},
        {"id": "sql_short_1", "type": "two_liner", "text": "What is the difference between WHERE and HAVING clauses in SQL?", "rubric": "WHERE filters rows before aggregation; HAVING filters groups after GROUP BY."},
        {"id": "sql_short_2", "type": "two_liner", "text": "What is a primary key constraint in a database table?", "rubric": "A unique identifier column that ensures no duplicate rows and prevents null values."},
        {"id": "sql_para_1", "type": "paragraph", "text": "Explain ACID properties in relational database transactions with a practical e-commerce example.", "rubric": "Atomicity, Consistency, Isolation, and Durability explained through safe handling of customer orders and payments."}
    ],
    "sql_joins": [
        {"id": "sql_joins_1", "type": "mcq", "text": "Which JOIN returns only matching rows from both tables?", "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"], "answer": "INNER JOIN"},
        {"id": "sql_joins_2", "type": "mcq", "text": "Which clause filters groups after a GROUP BY?", "options": ["HAVING", "WHERE", "ORDER BY", "LIMIT"], "answer": "HAVING"},
        {"id": "join_short_1", "type": "two_liner", "text": "What is the difference between an INNER JOIN and a LEFT JOIN?", "rubric": "INNER JOIN returns only intersecting matching rows; LEFT JOIN returns all rows from the left table regardless of matches."},
        {"id": "join_short_2", "type": "two_liner", "text": "When would you use a FULL OUTER JOIN?", "rubric": "When you need all records from both tables, combining matches and filling missing sides with NULLs."},
        {"id": "join_para_1", "type": "paragraph", "text": "Explain how a self-join works in SQL with an organizational hierarchy example.", "rubric": "Joining a table to itself using table aliases to map hierarchical relationships like employees reporting to managers."}
    ],
    "python_for_analysis": [
        {"id": "python_for_analysis_1", "type": "mcq", "text": "Which Python data structure stores key-value pairs?", "options": ["Dictionary", "List", "Tuple", "Set"], "answer": "Dictionary"},
        {"id": "python_for_analysis_2", "type": "mcq", "text": "What does the split() method do on a string?", "options": ["Breaks it into a list of substrings", "Joins two strings", "Reverses a string", "Counts characters"], "answer": "Breaks it into a list of substrings"},
        {"id": "pfa_short_1", "type": "two_liner", "text": "What is a lambda function in Python?", "rubric": "An anonymous single-line inline function designed for quick, small operations."},
        {"id": "pfa_short_2", "type": "two_liner", "text": "How do list comprehensions compare to standard for-loops?", "rubric": "List comprehensions offer a more concise, readable, and often faster syntax for generating lists."},
        {"id": "pfa_para_1", "type": "paragraph", "text": "Discuss file I/O safety in Python using context managers (`with` statements).", "rubric": "Context managers guarantee safe resource cleanup and automatic file closure even if execution encounters exceptions."}
    ],
    "pandas_basics": [
        {"id": "pandas_basics_1", "type": "mcq", "text": "Which Pandas method reads a CSV file?", "options": ["read_csv()", "load_csv()", "open_csv()", "import_csv()"], "answer": "read_csv()"},
        {"id": "pandas_basics_2", "type": "mcq", "text": "Which method removes rows with missing values in Pandas?", "options": ["dropna()", "fillna()", "dropna_all()", "remove_null()"], "answer": "dropna()"},
        {"id": "pd_short_1", "type": "two_liner", "text": "What is the difference between `loc` and `iloc` in Pandas?", "rubric": "`loc` relies on label-based indexing, whereas `iloc` relies on integer position-based indexing."},
        {"id": "pd_short_2", "type": "two_liner", "text": "How does Pandas handle missing data (NaN) in numerical aggregations?", "rubric": "Pandas automatically excludes NaN values by default during operations like sum or mean."},
        {"id": "pd_para_1", "type": "paragraph", "text": "Explain the split-apply-combine mechanism underlying Pandas groupby operations.", "rubric": "Data is split into subsets based on criteria, a function is applied independently to each, and results are combined."}
    ],
    "descriptive_statistics": [
        {"id": "descriptive_statistics_1", "type": "mcq", "text": "Which value represents the middle of a sorted dataset?", "options": ["Median", "Mean", "Mode", "Variance"], "answer": "Median"},
        {"id": "descriptive_statistics_2", "type": "mcq", "text": "What does variance measure?", "options": ["How spread out data points are", "The average value", "The most common value", "The total sum"], "answer": "How spread out data points are"},
        {"id": "ds_short_1", "type": "two_liner", "text": "What does standard deviation indicate that the mean cannot?", "rubric": "Standard deviation measures data dispersion or spread around the mean value."},
        {"id": "ds_short_2", "type": "two_liner", "text": "What is the Interquartile Range (IQR) and why is it robust?", "rubric": "IQR is the distance between the 75th and 25th percentiles, making it resistant to extreme outliers."},
        {"id": "ds_para_1", "type": "paragraph", "text": "Explain skewness and kurtosis as distribution shape parameters.", "rubric": "Skewness quantifies distribution asymmetry; kurtosis measures tail heaviness and peakedness relative to a normal distribution."}
    ],
    "hypothesis_testing": [
        {"id": "hypothesis_testing_1", "type": "mcq", "text": "What does a p-value below 0.05 typically suggest?", "options": ["Statistical significance", "No relationship", "A perfect correlation", "An invalid test"], "answer": "Statistical significance"},
        {"id": "hypothesis_testing_2", "type": "mcq", "text": "What is the null hypothesis?", "options": ["The default assumption of no effect", "The alternative outcome", "The sample size", "The confidence interval"], "answer": "The default assumption of no effect"},
        {"id": "ht_short_1", "type": "two_liner", "text": "What does rejecting the null hypothesis imply?", "rubric": "There is sufficient statistical evidence to support the alternative hypothesis."},
        {"id": "ht_short_2", "type": "two_liner", "text": "What is a p-value?", "rubric": "The probability of obtaining test results at least as extreme as observed, assuming the null hypothesis is true."},
        {"id": "ht_para_1", "type": "paragraph", "text": "Describe the steps required to execute a two-sample t-test for comparing independent group means.", "rubric": "State hypotheses, evaluate assumptions like normality and variance homogeneity, compute test statistics, and interpret p-values."}
    ],
    "data_cleaning": [
        {"id": "data_cleaning_1", "type": "mcq", "text": "What is the term for filling in missing values with a placeholder?", "options": ["Imputation", "Normalization", "Aggregation", "Encoding"], "answer": "Imputation"},
        {"id": "data_cleaning_2", "type": "mcq", "text": "What is a duplicate row in a dataset?", "options": ["A row that repeats another row's values", "A row with missing values", "A row with extra columns", "A row with wrong data types"], "answer": "A row that repeats another row's values"},
        {"id": "dc_short_1", "type": "two_liner", "text": "What are two primary strategies for managing missing data?", "rubric": "Deletion (dropping incomplete rows or columns) or imputation (filling gaps with statistical values)."},
        {"id": "dc_short_2", "type": "two_liner", "text": "Why is feature scaling necessary for machine learning algorithms?", "rubric": "It prevents features with large numeric scales from dominating distance-based or gradient-based model training."},
        {"id": "dc_para_1", "type": "paragraph", "text": "Walk through a robust data cleaning pipeline for raw real-world data.", "rubric": "Handling duplicates, correcting schema/data types, imputing missing values, treating outliers, and normalizing text fields."}
    ],
    "data_visualization": [
        {"id": "data_visualization_1", "type": "mcq", "text": "Which chart type is best for showing change over time?", "options": ["Line chart", "Pie chart", "Scatter plot", "Histogram"], "answer": "Line chart"},
        {"id": "data_visualization_2", "type": "mcq", "text": "What does a histogram show?", "options": ["The distribution of a numeric variable", "Category proportions", "Correlation between variables", "Time series trends"], "answer": "The distribution of a numeric variable"},
        {"id": "dv_short_1", "type": "two_liner", "text": "When should you choose a scatter plot over a bar chart?", "rubric": "Scatter plots show correlation between two numeric variables; bar charts compare discrete categories."},
        {"id": "dv_short_2", "type": "two_liner", "text": "What is the primary role of a box plot in EDA?", "rubric": "To summarize data distributions using quartiles and highlight potential outlier anomalies."},
        {"id": "dv_para_1", "type": "paragraph", "text": "Discuss key layout and design principles for building executive data dashboards.", "rubric": "Clarity, eliminating visual clutter, selecting correct chart types, using consistent color schemes, and highlighting insights."}
    ],
    "dashboarding": [
        {"id": "dashboarding_1", "type": "mcq", "text": "What is the main purpose of a dashboard?", "options": ["Present key metrics at a glance", "Store raw data", "Write SQL queries", "Train models"], "answer": "Present key metrics at a glance"},
        {"id": "dashboarding_2", "type": "mcq", "text": "What does a KPI represent?", "options": ["Key Performance Indicator", "Known Prediction Interval", "Kernel Processing Input", "Key Pandas Index"], "answer": "Key Performance Indicator"},
        {"id": "dash_short_1", "type": "two_liner", "text": "What is the difference between a static report and an interactive dashboard?", "rubric": "Static reports present fixed snapshots; interactive dashboards let users filter, query, and explore data dynamically."},
        {"id": "dash_short_2", "type": "two_liner", "text": "Why is an inverted pyramid layout useful in dashboard design?", "rubric": "It positions high-level KPIs and critical summary metrics at the top where they are seen first."},
        {"id": "dash_para_1", "type": "paragraph", "text": "Explain how cognitive load and UX principles influence effective dashboard design.", "rubric": "Keeping interfaces clutter-free, reducing unnecessary visual noise, and organizing components logically to optimize user comprehension."}
    ]
}

def questions_for(concept_id):
    return QUESTION_BANK.get(concept_id, [])