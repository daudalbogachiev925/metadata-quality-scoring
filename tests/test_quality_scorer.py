import pandas as pd
from src.quality_scorer import QualityScorer


def test_basic_scoring():
    # Simple dataset
    data = {
        "id": [1, 2, 3, 4, None],
        "email": ["a@example.com", "b@example.com", "invalid", None, "c@example.com"],
        "age": [25, 30, None, 45, 22],
    }
    df = pd.DataFrame(data)

    # Custom rules focusing on completeness and regex for email
    rules = {
        "id": {"required": True, "completeness_weight": 2, "uniqueness_weight": 1},
        "email": {"required": True, "regex": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$", "regex_weight": 2},
        "age": {"allowed_values": list(range(0, 121)), "completeness_weight": 1},
    }

    scorer = QualityScorer(rules)
    result = scorer.score(df)

    # Overall score should be a float between 0 and 100
    assert 0 <= result["overall_score"] <= 100
    # Verify column scores exist
    assert "id" in result["column_scores"]
    assert "email" in result["column_scores"]
    assert "age" in result["column_scores"]
    # Email regex score should be less than 100 because of an invalid entry
    email_score = result["column_scores"]["email"]["score"]
    assert email_score < 100
