"""
Pantry Solver Router.
Answers: "What can I cook with what I have?"
"""
from fastapi import APIRouter
from backend.data.loader import get_db
from backend.core.pantry_matcher import PantryMatcher
from backend.models.query import PantryQuery

router = APIRouter(prefix="/api/solve", tags=["solver"])

db = get_db()
pantry_matcher = PantryMatcher(db.get_all())

@router.post("/pantry")
def solve_pantry(query: PantryQuery):
    """
    Match user's available pantry ingredients against all recipes,
    performing gap analysis, substitute detection, and readiness ranking.
    """
    filter_dict = query.filters.model_dump(exclude_none=True) if query.filters else {}
    results = pantry_matcher.match_recipes(
        pantry_items=query.ingredients,
        filters=filter_dict,
        include_substitutes=query.include_substitutes,
        must_include=query.must_include
    )

    ready_to_cook_count = sum(1 for r in results if r["is_ready_to_cook"])

    return {
        "input_ingredients_count": len(query.ingredients),
        "total_matches": len(results),
        "ready_to_cook_count": ready_to_cook_count,
        "results": results[:25]
    }
