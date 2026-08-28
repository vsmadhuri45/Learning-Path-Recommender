from app.extraction import _normalize_role


def test_exact_role_names_pass_through():
    assert _normalize_role("ML Engineer")=="ML Engineer"
    assert _normalize_role("Data Analyst")=="Data Analyst"


def test_common_variants_normalize():
    assert _normalize_role("Machine Learning Engineer")=="ML Engineer"
    assert _normalize_role("I want to be an MLE")=="ML Engineer"
    assert _normalize_role("data analyst")=="Data Analyst"
    assert _normalize_role("DA")=="Data Analyst"
    assert _normalize_role("I want to work with data as an analyst")=="Data Analyst"


def test_unsupported_role_returns_none():
    assert _normalize_role("Backend Engineer") is None
    assert _normalize_role("Something totally unrelated") is None


def test_none_returns_none():
    assert _normalize_role(None) is None


def test_no_false_positive_on_substring():
    assert _normalize_role("formal request") is None
    assert _normalize_role("html email") is None
