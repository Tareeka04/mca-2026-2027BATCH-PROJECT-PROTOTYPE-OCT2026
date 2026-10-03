"""
Recipe Router.
Provides CRUD operations, dynamic servings scaling, similar recipe recommendations, and autocomplete data.
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from backend.data.loader import get_db
from backend.core.ir_engine import IREngine
from backend.models.recipe import ScaledRecipe, ScaledIngredient, Nutrition

router = APIRouter(prefix="/api/recipes", tags=["recipes"])

db = RecipeDatabase = get_db()
ir_engine = IREngine()
ir_engine.index_recipes(db.get_all())

def format_quantity(qty: float, unit: str = "") -> str:
    """Format floating point quantity into human friendly decimal or whole string."""
    if qty <= 0:
        return ""
    if abs(qty - round(qty)) < 0.05:
        return str(int(round(qty)))
    # Check common fractions
    frac_map = {0.25: "1/4", 0.33: "1/3", 0.5: "1/2", 0.66: "2/3", 0.75: "3/4"}
    whole = int(qty)
    dec = qty - whole
    for frac_val, frac_str in frac_map.items():
        if abs(dec - frac_val) < 0.06:
            return f"{whole} {frac_str}" if whole else frac_str
    return f"{qty:.2f}".rstrip("0").rstrip(".")

def normalize_display_quantity(quantity: float, unit: str):
    """Convert common metric quantities to kitchen-friendly units."""
    u = (unit or "").lower().strip()
    if u in {"g", "gram", "grams"} and quantity >= 1000:
        kg = quantity / 1000
        return round(kg, 2), "kg"
    if u in {"ml", "millilitre", "millilitres", "milliliter", "milliliters"} and quantity >= 1000:
        return round(quantity / 1000, 2), "litre"
    return quantity, unit

@router.get("")
def list_recipes(
    cuisine: Optional[str] = None,
    diet: Optional[str] = None,
    meal_type: Optional[str] = None,
    max_time: Optional[int] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=150)
):
    recipes = db.get_all()

    # Search filter if provided
    if search and search.strip():
        term = search.strip().lower()
        search_results = ir_engine.search_hybrid(search.strip())
        recipes = [r for r, score in search_results if score > 0.01]
        # Never turn a valid search into an empty catalog just because the IR
        # threshold is conservative. Fall back to direct recipe/ingredient text.
        if not recipes:
            recipes = [
                r for r in db.get_all()
                if term in r.get("title", "").lower()
                or term in r.get("summary", "").lower()
                or any(term in str(i.get("name", "")).lower() for i in r.get("ingredients", []))
                or term in r.get("regional_cuisine", "").lower()
            ]

    filtered = []
    for r in recipes:
        if cuisine and cuisine.lower() != "all" and cuisine.lower() not in r.get("regional_cuisine", "").lower():
            continue
        if diet and diet.lower() != "all":
            d_low = diet.lower()
            if d_low == "vegetarian" and r.get("diet") not in ["Vegetarian", "Vegan"]:
                continue
            if d_low == "vegan" and not r.get("is_vegan", False):
                continue
            if d_low == "jain" and not r.get("is_jain", False):
                continue
            if d_low == "gluten-free" and not r.get("is_gluten_free", False):
                continue
        if meal_type and meal_type.lower() != "all":
            mt_list = [m.lower() for m in r.get("meal_type", [])]
            if meal_type.lower() not in mt_list and meal_type.lower() != r.get("course", "").lower():
                continue
        if max_time and r.get("total_time_mins", 0) > max_time:
            continue
        if difficulty and difficulty.lower() != "all" and difficulty.lower() != r.get("difficulty", "").lower():
            continue
        filtered.append(r)

    total_count = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]

    return {
        "total": total_count,
        "page": page,
        "limit": limit,
        "total_pages": (total_count + limit - 1) // limit,
        "recipes": paginated
    }

@router.get("/{recipe_id}")
def get_recipe(recipe_id: str):
    recipe = db.get_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.get("/{recipe_id}/scale")
def scale_recipe(recipe_id: str, servings: int = Query(..., ge=1, le=24)):
    recipe = db.get_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    orig_servings = recipe.get("base_servings", recipe.get("nutrition_per_serving", {}).get("servings", 2))
    if orig_servings <= 0:
        orig_servings = 2

    scale_factor = servings / orig_servings
    scaled_ingredients = []

    for ing in recipe.get("ingredients", []):
        orig_qty = ing.get("quantity", 1.0)
        scaled_qty = round(orig_qty * scale_factor, 2)
        display_qty, display_unit = normalize_display_quantity(scaled_qty, ing.get("unit", ""))
        scaled_ingredients.append({
            "name": ing.get("name"),
            "quantity": scaled_qty,
            "display_quantity": format_quantity(display_qty, display_unit),
            "unit": display_unit,
            "measurement": f"{format_quantity(display_qty, display_unit)} {display_unit}".strip(),
            "is_optional": ing.get("is_optional", False),
            "category": ing.get("category", "general"),
            "substitutes": ing.get("substitutes", [])
        })

    nutrition = recipe.get("nutrition_per_serving", {})
    return {
        "recipe_id": recipe_id,
        "title": recipe.get("title"),
        "original_servings": orig_servings,
        "target_servings": servings,
        "scale_factor": round(scale_factor, 2),
        "scaled_ingredients": scaled_ingredients,
        "nutrition_per_serving": nutrition,
        "total_nutrition_estimate": {
            "total_calories": int((nutrition.get("calories") or 0) * servings),
            "total_protein_g": round((nutrition.get("protein_g") or 0) * servings, 1),
            "total_carbs_g": round((nutrition.get("carbs_g") or 0) * servings, 1),
            "total_fat_g": round((nutrition.get("fat_g") or 0) * servings, 1)
        }
    }

@router.get("/{recipe_id}/similar")
def get_similar_recipes(recipe_id: str, count: int = Query(4, ge=1, le=10)):
    similar = ir_engine.get_similar_recipes(recipe_id, top_k=count)
    return {"recipe_id": recipe_id, "similar_recipes": similar}

@router.get("/data/all_ingredients")
def get_all_ingredients():
    return {"ingredients": db.get_all_ingredients()}
