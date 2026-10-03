from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str
    is_optional: bool = False
    category: Optional[str] = "general"
    substitutes: List[str] = Field(default_factory=list)

class RecipeStep(BaseModel):
    step_number: int
    title: str
    instruction: str
    duration_mins: Optional[int] = 0
    tip: Optional[str] = None

class Nutrition(BaseModel):
    servings: int = 2
    calories: Optional[int] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    fiber_g: Optional[float] = None

class FlavorProfile(BaseModel):
    spicy: int = Field(default=2, ge=0, le=5)
    tangy: int = Field(default=2, ge=0, le=5)
    sweet: int = Field(default=1, ge=0, le=5)
    savory: int = Field(default=3, ge=0, le=5)
    comfort: int = Field(default=4, ge=0, le=5)

class Recipe(BaseModel):
    id: str
    title: str
    regional_cuisine: str
    meal_type: List[str]
    course: str
    prep_time_mins: int
    cook_time_mins: int
    total_time_mins: int
    difficulty: str
    diet: str  # "Vegetarian", "Vegan", "Non-Vegetarian", "Eggitarian"
    is_vegan: bool = False
    is_jain: bool = False
    is_gluten_free: bool = False
    flavor_profile: FlavorProfile = Field(default_factory=FlavorProfile)
    mood_tags: List[str] = Field(default_factory=list)
    texture: str = Field(default="regular", description="'soft', 'regular', 'crispy'")
    is_kid_friendly: bool = Field(default=False)
    is_elder_friendly: bool = Field(default=False)
    is_high_protein: bool = Field(default=False)
    is_easy_digest: bool = Field(default=False)
    is_one_pot: bool = Field(default=False)
    ingredients: List[Ingredient]
    normalized_ingredients: List[str] = Field(default_factory=list)
    leftover_ingredients_used: List[str] = Field(default_factory=list)
    steps: List[RecipeStep]
    nutrition_per_serving: Nutrition = Field(default_factory=Nutrition)
    equipment: List[str] = Field(default_factory=list)
    summary: str
    image_url: Optional[str] = None

class ScaledIngredient(BaseModel):
    name: str
    quantity: float
    display_quantity: str
    unit: str
    is_optional: bool
    category: Optional[str]
    substitutes: List[str]

class ScaledRecipe(BaseModel):
    recipe: Recipe
    target_servings: int
    original_servings: int
    scale_factor: float
    scaled_ingredients: List[ScaledIngredient]
    scaled_nutrition: Nutrition
