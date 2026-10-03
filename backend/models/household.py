"""Models for the local Household Meal Solver workflow."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class HouseholdMember(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=80)
    role: str = "Adult"
    diet: str = "Vegetarian"
    spice_tolerance: str = "Medium"
    avoid_ingredients: List[str] = Field(default_factory=list)
    preferred_cuisines: List[str] = Field(default_factory=list)
    preferences: List[str] = Field(default_factory=list)
    strict_preferences: List[str] = Field(default_factory=list)
    texture_preference: Optional[str] = None
    custom_preference: Optional[str] = None

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Member name is required")
        return value


class HouseholdQuery(BaseModel):
    members: List[HouseholdMember] = Field(..., min_length=1)
    available_ingredients: List[str] = Field(default_factory=list)
    servings: Optional[int] = Field(default=None, ge=1, le=30)
    max_time_mins: Optional[int] = Field(default=None, ge=1, le=300)
    meal_type: Optional[str] = None
    cuisine: Optional[str] = None
    household_type: str = "Family"
    one_pot: bool = False
    custom_preferences: List[str] = Field(default_factory=list)

    @field_validator("members")
    @classmethod
    def unique_member_ids(cls, value):
        ids = [m.id for m in value]
        if len(ids) != len(set(ids)):
            raise ValueError("Household member IDs must be unique")
        return value


class MemberMatchExplanation(BaseModel):
    member_id: str
    member_name: str
    role: str
    is_fully_satisfied: bool
    satisfaction_score: int
    satisfied_aspects: List[str]
    compromises_or_tips: List[str]


class HouseholdMealResult(BaseModel):
    recipe: Dict[str, Any]
    household_score: float
    household_harmony_percentage: int
    is_perfect_shared_meal: bool
    summary_verdict: str
    explanation: str = ""
    strict_constraints_satisfied: List[str] = Field(default_factory=list)
    strict_constraints_failed: List[str] = Field(default_factory=list)
    preferences_satisfied: List[str] = Field(default_factory=list)
    member_explanations: List[MemberMatchExplanation]
    family_customization_tip: str
    member_adaptations: List[Dict[str, Any]] = Field(default_factory=list)
    pantry_match_percentage: int
    matched_ingredients: List[str]
    missing_ingredients: List[str]
    missing_ingredient_details: List[Dict[str, Any]] = Field(default_factory=list)
    scaled_ingredients: List[Dict[str, Any]]
    total_household_servings: int
    total_time_mins: int
    one_pot: bool = False
    dietary_badges: List[str]
    taste_profile: Dict[str, int]


class HouseholdSolveResponse(BaseModel):
    total_members: int
    total_servings: int
    best_shared_meal: Optional[HouseholdMealResult] = None
    runner_up_meals: List[HouseholdMealResult] = Field(default_factory=list)
    household_summary: Dict[str, Any]
    no_perfect_match: bool = False
    conflict_message: Optional[str] = None
    smallest_adjustment: Optional[str] = None
