from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class FilterParams(BaseModel):
    diet: Optional[str] = None  # "Vegetarian", "Vegan", "Jain", "Gluten-Free"
    max_time_mins: Optional[int] = None
    meal_type: Optional[str] = None  # "Breakfast", "Lunch", "Dinner", "Snack"
    cuisine: Optional[str] = None  # "Maharashtrian", "North Indian", "South Indian", etc.
    difficulty: Optional[str] = None  # "Easy", "Medium", "Hard"

class PantryQuery(BaseModel):
    ingredients: List[str] = Field(..., min_length=1, description="List of available pantry ingredients")
    filters: Optional[FilterParams] = None
    include_substitutes: bool = True
    must_include: Optional[List[str]] = Field(default_factory=list)

class CravingQuery(BaseModel):
    query: Optional[str] = None  # e.g., "spicy comforting khichdi for monsoon" or "sweet festive modak"
    spice_level: Optional[int] = Field(default=None, ge=0, le=5)
    tangy_level: Optional[int] = Field(default=None, ge=0, le=5)
    sweet_level: Optional[int] = Field(default=None, ge=0, le=5)
    comfort_level: Optional[int] = Field(default=None, ge=0, le=5)
    mood: Optional[str] = None  # "comforting", "quick", "indulgent", "healthy", "festive", "light"
    filters: Optional[FilterParams] = None
    top_k: int = 15

class LeftoverQuery(BaseModel):
    leftover_items: List[str] = Field(..., min_length=1, description="Leftover staples e.g., 'Cooked Rice', 'Stale Chapati/Roti', 'Leftover Dal'")
    additional_ingredients: Optional[List[str]] = Field(default_factory=list)
    filters: Optional[FilterParams] = None

class IngredientMatchResult(BaseModel):
    recipe: Dict[str, Any]
    match_score: float  # 0.0 to 1.0 (Percentage match)
    match_percentage: int  # 0 to 100
    matched_ingredients: List[str]
    missing_ingredients: List[str]
    substitute_suggestions: Dict[str, List[str]]
    is_ready_to_cook: bool  # 100% matched or missing only optional items
    ready_badge: str  # "Can Cook Now", "Missing 1 Item", "Needs Few Items"

class CravingMatchResult(BaseModel):
    recipe: Dict[str, Any]
    relevance_score: float
    relevance_percentage: int
    matched_reasons: List[str]
    taste_profile: Dict[str, int]

class LeftoverMatchResult(BaseModel):
    recipe: Dict[str, Any]
    primary_leftover: str
    transformation_name: str
    transformation_tip: str
    additional_needed: List[str]
    prep_speed_badge: str  # "< 15 Mins", "Quick Flip"
    match_score: float

class ShoppingItem(BaseModel):
    name: str
    quantity: float
    unit: str
    recipe_title: str
    recipe_id: str
    category: str
    checked: bool = False
