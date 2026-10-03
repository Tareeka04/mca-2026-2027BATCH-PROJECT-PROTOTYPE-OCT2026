"""
Craving and IR Recommender Router.
Answers: "What should I cook based on what I am craving?"
"""
from fastapi import APIRouter
from backend.data.loader import get_db
from backend.core.ir_engine import IREngine
from backend.core.recommender import CravingRecommender
from backend.models.query import CravingQuery

router = APIRouter(prefix="/api/solve", tags=["cravings"])

db = get_db()
ir_engine = IREngine()
ir_engine.index_recipes(db.get_all())
craving_recommender = CravingRecommender(ir_engine)

@router.post("/craving")
def solve_craving(query: CravingQuery):
    """
    Search and recommend dishes based on free-form cravings, flavor profiles, and mood tags.
    """
    filter_dict = query.filters.model_dump(exclude_none=True) if query.filters else {}
    results = craving_recommender.recommend(
        query_text=query.query,
        spicy_target=query.spice_level,
        tangy_target=query.tangy_level,
        sweet_target=query.sweet_level,
        comfort_target=query.comfort_level,
        mood=query.mood,
        filters=filter_dict,
        top_k=query.top_k
    )

    return {
        "query": query.query,
        "mood": query.mood,
        "total_results": len(results),
        "results": results
    }
