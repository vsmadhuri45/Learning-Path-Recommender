"""
Static concept_id -> learning resources mapping.

Doc module 13, cut down for the hackathon: a hardcoded dict instead of a
resource database or search integration. One primary resource per concept
is enough to make the roadmap actionable; swap for a real catalog later
without changing any call sites.
"""

RESOURCE_BANK = {
    "python_basics": [{"title": "Python for Everybody", "type": "course", "url": "https://www.py4e.com/"}],
    "numpy_pandas": [{"title": "NumPy Quickstart", "type": "docs", "url": "https://numpy.org/doc/stable/user/quickstart.html"}],
    "linear_algebra": [{"title": "Essence of Linear Algebra", "type": "video", "url": "https://www.3blue1brown.com/topics/linear-algebra"}],
    "probability": [{"title": "Intro to Probability (MIT OCW)", "type": "course", "url": "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/"}],
    "statistics": [{"title": "Statistics 110", "type": "course", "url": "https://projects.iq.harvard.edu/stat110"}],
    "regression": [{"title": "Regression Analysis Basics", "type": "article", "url": "https://scikit-learn.org/stable/modules/linear_model.html"}],
    "classification": [{"title": "Classification Algorithms Overview", "type": "article", "url": "https://scikit-learn.org/stable/supervised_learning.html"}],
    "model_evaluation": [{"title": "Model Evaluation Metrics", "type": "docs", "url": "https://scikit-learn.org/stable/modules/model_evaluation.html"}],
    "optimization": [{"title": "Gradient Descent Explained", "type": "article", "url": "https://ruder.io/optimizing-gradient-descent/"}],
    "neural_networks": [{"title": "Neural Networks and Deep Learning", "type": "book", "url": "http://neuralnetworksanddeeplearning.com/"}],
    "excel_basics": [{"title": "Excel Functions for Analysts", "type": "course", "url": "https://exceljet.net/"}],
    "sql_basics": [{"title": "SQLBolt", "type": "interactive", "url": "https://sqlbolt.com/"}],
    "sql_joins": [{"title": "SQL Joins Explained Visually", "type": "article", "url": "https://joins.spathon.com/"}],
    "python_for_analysis": [{"title": "Python for Data Analysis", "type": "book", "url": "https://wesmckinney.com/book/"}],
    "pandas_basics": [{"title": "10 Minutes to Pandas", "type": "docs", "url": "https://pandas.pydata.org/docs/user_guide/10min.html"}],
    "descriptive_statistics": [{"title": "Descriptive Stats Primer", "type": "article", "url": "https://www.scribbr.com/statistics/descriptive-statistics/"}],
    "hypothesis_testing": [{"title": "Hypothesis Testing Explained", "type": "article", "url": "https://www.scribbr.com/statistics/hypothesis-testing/"}],
    "data_cleaning": [{"title": "Data Cleaning with Pandas", "type": "tutorial", "url": "https://realpython.com/python-data-cleaning-numpy-pandas/"}],
    "data_visualization": [{"title": "Fundamentals of Data Visualization", "type": "book", "url": "https://clauswilke.com/dataviz/"}],
    "dashboarding": [{"title": "Dashboard Design Principles", "type": "article", "url": "https://www.tableau.com/learn/articles/dashboard-design-principles"}],
}


def resources_for(concept_id: str) -> list[dict]:
    return RESOURCE_BANK.get(concept_id, [])