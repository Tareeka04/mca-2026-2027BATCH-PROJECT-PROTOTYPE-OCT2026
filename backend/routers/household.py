"""
Household Meal Solver Router.
Answers: "ONE HOUSEHOLD. DIFFERENT NEEDS. ONE MEAL."
"""
from fastapi import APIRouter
from backend.data.loader import get_db
from backend.core.household_solver import HouseholdSolver
from backend.models.household import HouseholdQuery, HouseholdSolveResponse

router = APIRouter(prefix="/api/household", tags=["household"])

db = get_db()
household_solver = HouseholdSolver(db.get_all())

@router.post("/solve", response_model=HouseholdSolveResponse)
def solve_household(query: HouseholdQuery):
    """
    Solve for ONE shared Indian meal that satisfies the combined constraints and preferences
    of all household family members using available ingredients.
    """
    return household_solver.solve(query)

@router.get("/presets")
def get_household_presets():
    """
    Return realistic Indian household family templates for 1-click preset testing.
    """
    return {
        "presets": [
            {
                "id": "three_gen_family",
                "title": "👨‍👩‍👧‍👦 3-Generation Joint Family (Parents + Kid + Dadi)",
                "description": "Mother (low spice), Father (vegetarian/protein), Child Aarav (mild/kid-friendly), Grandmother Dadi (soft food/easy digest).",
                "members": [
                    {
                        "id": "m1",
                        "name": "Mother (Sunita)",
                        "role": "Mother",
                        "diet": "Vegetarian",
                        "spice_tolerance": "Low",
                        "avoid_ingredients": ["peanuts"],
                        "preferences": ["quick"]
                    },
                    {
                        "id": "m2",
                        "name": "Father (Rajesh)",
                        "role": "Father",
                        "diet": "Vegetarian",
                        "spice_tolerance": "Medium",
                        "avoid_ingredients": [],
                        "preferences": ["high_protein"]
                    },
                    {
                        "id": "m3",
                        "name": "Aarav (6 yrs)",
                        "role": "Child",
                        "diet": "Vegetarian",
                        "spice_tolerance": "Mild",
                        "avoid_ingredients": ["capsicum", "raw ginger"],
                        "preferences": ["kid_friendly"]
                    },
                    {
                        "id": "m4",
                        "name": "Dadi (72 yrs)",
                        "role": "Grandmother",
                        "diet": "Vegetarian",
                        "spice_tolerance": "Low",
                        "avoid_ingredients": [],
                        "preferences": ["soft_food", "easy_digest"]
                    }
                ],
                "sample_pantry": ["Rice", "Moong Dal", "Tomato", "Potato", "Turmeric", "Cumin Seeds", "Ghee", "Salt", "Coriander"]
            },
            {
                "id": "jain_elder_couple",
                "title": "🧓 Elder Care + Strict Jain Household",
                "description": "Strict No Onion/Garlic/Root veg, soft texture, soothing & low acidity.",
                "members": [
                    {
                        "id": "m1",
                        "name": "Grandpa (Dada)",
                        "role": "Grandfather",
                        "diet": "Jain",
                        "spice_tolerance": "Low",
                        "avoid_ingredients": ["onion", "garlic", "potato"],
                        "preferences": ["soft_food", "easy_digest"]
                    },
                    {
                        "id": "m2",
                        "name": "Grandma (Dadi)",
                        "role": "Grandmother",
                        "diet": "Jain",
                        "spice_tolerance": "Low",
                        "avoid_ingredients": ["onion", "garlic", "potato"],
                        "preferences": ["soft_food", "high_protein"]
                    }
                ],
                "sample_pantry": ["Toor Dal", "Rice", "Ghee", "Turmeric", "Cumin Seeds", "Hing", "Salt", "Jaggery"]
            },
            {
                "id": "working_couple_spicy",
                "title": "👫 Working Couple: Spice Lover + High Protein Vegan",
                "description": "Partner 1 wants 100% Plant Vegan & High Protein; Partner 2 loves spicy Maharashtrian flavors.",
                "members": [
                    {
                        "id": "m1",
                        "name": "Pooja",
                        "role": "Self",
                        "diet": "Vegan",
                        "spice_tolerance": "Medium",
                        "avoid_ingredients": ["dairy", "ghee", "paneer"],
                        "preferences": ["high_protein", "quick"]
                    },
                    {
                        "id": "m2",
                        "name": "Aniket",
                        "role": "Partner",
                        "diet": "Vegetarian",
                        "spice_tolerance": "Spicy",
                        "avoid_ingredients": [],
                        "preferences": ["maharashtrian"]
                    }
                ],
                "sample_pantry": ["Sprouted Matki", "Onion", "Tomato", "Garlic", "Ginger", "Goda Masala", "Oil", "Salt", "Coriander"]
            }
        ]
    }

@router.get("/household-types")
def get_household_types():
    return {
        "types": [
            {"id":"student","label":"Student / Bachelor","defaults":{"servings":1,"max_time_mins":25,"one_pot":True}},
            {"id":"working_professional","label":"Working Professional","defaults":{"servings":1,"max_time_mins":35,"one_pot":True}},
            {"id":"couple","label":"Couple","defaults":{"servings":2,"max_time_mins":45,"one_pot":False}},
            {"id":"family","label":"Small / Large Family","defaults":{"servings":4,"max_time_mins":50,"one_pot":False}},
            {"id":"senior_friendly","label":"Senior-friendly Household","defaults":{"servings":2,"max_time_mins":45,"one_pot":False}},
            {"id":"shared_flat","label":"Shared Flat / Hostel","defaults":{"servings":3,"max_time_mins":30,"one_pot":True}}
        ]
    }
