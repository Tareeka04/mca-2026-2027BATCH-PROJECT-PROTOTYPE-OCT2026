import pytest
from backend.data.loader import get_db
from backend.core.pantry_matcher import PantryMatcher

@pytest.fixture
def pantry_matcher():
    db = get_db()
    return PantryMatcher(db.get_all())

def test_pantry_exact_match(pantry_matcher):
    # Full ingredients for Kanda Poha
    items = ["Poha", "Onion", "Green Chillies", "Peanuts", "Mustard Seeds", "Turmeric", "Curry Leaves", "Oil", "Salt", "Lemon Juice", "Coriander"]
    results = pantry_matcher.match_recipes(items)
    
    assert len(results) > 0
    top_result = results[0]
    # Kanda Poha or Batata Poha should be top ranked and ready to cook
    assert "poha" in top_result["recipe"]["id"].lower() or "poha" in top_result["recipe"]["title"].lower()
    assert top_result["is_ready_to_cook"] is True

def test_pantry_gap_analysis(pantry_matcher):
    # Missing poha, has only onion and peanuts
    items = ["Onion", "Peanuts", "Green Chillies"]
    results = pantry_matcher.match_recipes(items)
    assert len(results) > 0
    
    # Should identify missing ingredients
    for res in results:
        assert isinstance(res["missing_ingredients"], list)
        assert isinstance(res["matched_ingredients"], list)
        assert "match_percentage" in res

def test_pantry_dietary_filter(pantry_matcher):
    items = ["Potato", "Onion", "Peanuts", "Green Chillies", "Sabudana"]
    # Filter for Jain (no onions / potatoes)
    results = pantry_matcher.match_recipes(items, filters={"diet": "Jain"})
    for res in results:
        assert res["recipe"].get("is_jain") is True
