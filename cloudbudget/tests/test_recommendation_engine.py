from api.services.recommendation_rules import categorize


def test_categorize_storage():
    category, confidence, savings = categorize("storage", 100)
    assert category == "unattached_volume"
    assert confidence > 0.7
    assert savings > 0


def test_categorize_db():
    category, _, _ = categorize("rds", 100)
    assert category == "reserved_instance"
