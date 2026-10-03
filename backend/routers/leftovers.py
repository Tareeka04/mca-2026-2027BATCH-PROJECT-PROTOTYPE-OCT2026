"""
Leftover Transformation Router.
Answers: "What can I make with my leftovers?"
"""
from fastapi import APIRouter
from backend.data.loader import get_db
from backend.core.leftover_solver import LeftoverSolver, LEFTOVER_TAXONOMY
from backend.models.query import LeftoverQuery

router = APIRouter(prefix="/api/solve", tags=["leftovers"])

db = get_db()
leftover_solver = LeftoverSolver(db.recipes_by_id)

@router.post("/leftovers")
def solve_leftovers(query: LeftoverQuery):
    """
    Transform Indian kitchen leftovers into authentic regional delicacies.
    """
    filter_dict = query.filters.model_dump(exclude_none=True) if query.filters else {}
    results = leftover_solver.solve(
        leftover_items=query.leftover_items,
        additional_ingredients=query.additional_ingredients,
        filters=filter_dict
    )

    return {
        "input_leftovers": query.leftover_items,
        "total_transformations": len(results),
        "results": results
    }

@router.get("/leftover_staples")
def get_leftover_staples():
    """Return available leftover categories with examples."""
    staples = []
    for key, val in LEFTOVER_TAXONOMY.items():
        staples.append({
            "id": key,
            "name": key.title(),
            "aliases": val["aliases"],
            "transform_count": len(val["recipes"])
        })
    return {"staples": staples}
