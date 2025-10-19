from src.services import categories_cashback


def test_analyze_cashback_categories(sample_df):
    result = categories_cashback(sample_df, "2024", "10")
    assert result["Супермаркеты"] == 3
