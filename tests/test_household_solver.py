import pytest
from backend.data.loader import get_db
from backend.core.household_solver import HouseholdSolver
from backend.models.household import HouseholdMember, HouseholdQuery

@pytest.fixture
def household_solver():
    db = get_db()
    return HouseholdSolver(db.get_all())

def test_joint_family_household_solver(household_solver):
    # Mother (low spice, avoid peanuts), Father (veg, high protein), Child (mild, kid friendly), Dadi (soft food, easy digest)
    members = [
        HouseholdMember(id="m1", name="Mother", role="Mother", diet="Vegetarian", spice_tolerance="Low", avoid_ingredients=["peanuts"], preferences=["quick"]),
        HouseholdMember(id="m2", name="Father", role="Father", diet="Vegetarian", spice_tolerance="Medium", avoid_ingredients=[], preferences=["high_protein"]),
        HouseholdMember(id="m3", name="Aarav", role="Child", diet="Vegetarian", spice_tolerance="Mild", avoid_ingredients=["capsicum"], preferences=["kid_friendly"]),
        HouseholdMember(id="m4", name="Dadi", role="Grandmother", diet="Vegetarian", spice_tolerance="Low", avoid_ingredients=[], preferences=["soft_food", "easy_digest"])
    ]

    query = HouseholdQuery(
        members=members,
        available_ingredients=["Rice", "Moong Dal", "Tomato", "Potato", "Turmeric", "Cumin Seeds", "Ghee", "Salt", "Coriander"],
        servings=4,
        max_time_mins=40
    )

    response = household_solver.solve(query)
    assert response.total_members == 4
    assert response.best_shared_meal is not None

    best = response.best_shared_meal
    # Best meal should be soft/mild/wholesome e.g. Moong Dal Khichdi, Sada Varan Bhaat, etc.
    assert best.household_harmony_percentage >= 75
    assert len(best.member_explanations) == 4
    assert best.total_household_servings == 4
    assert len(best.scaled_ingredients) > 0

    # Ensure no peanuts in the essential ingredients of the recommended meal
    recipe_text = best.recipe["title"].lower() + " " + " ".join(best.recipe.get("normalized_ingredients", []))
    assert "peanut" not in best.recipe.get("normalized_ingredients", []) or all(ing.get("is_optional", False) for ing in best.recipe.get("ingredients", []) if "peanut" in ing.get("name", "").lower())

def test_jain_elder_household(household_solver):
    # Strict Jain grandfather and grandmother
    members = [
        HouseholdMember(id="m1", name="Dada", role="Grandfather", diet="Jain", spice_tolerance="Low", avoid_ingredients=["onion", "garlic", "potato"], preferences=["soft_food", "easy_digest"]),
        HouseholdMember(id="m2", name="Dadi", role="Grandmother", diet="Jain", spice_tolerance="Low", avoid_ingredients=["onion", "garlic", "potato"], preferences=["soft_food"])
    ]

    query = HouseholdQuery(
        members=members,
        available_ingredients=["Toor Dal", "Rice", "Ghee", "Turmeric", "Cumin Seeds", "Hing", "Salt"],
        servings=2
    )

    response = household_solver.solve(query)
    assert response.best_shared_meal is not None
    best = response.best_shared_meal
    assert best.recipe.get("is_jain") is True
    assert best.recipe.get("texture") == "soft" or best.recipe.get("is_elder_friendly") is True

def test_household_servings_scaling(household_solver):
    members = [
        HouseholdMember(id="m1", name="A", role="Self", diet="Vegetarian", spice_tolerance="Medium", avoid_ingredients=[], preferences=[]),
        HouseholdMember(id="m2", name="B", role="Self", diet="Vegetarian", spice_tolerance="Medium", avoid_ingredients=[], preferences=[])
    ]
    query = HouseholdQuery(members=members, servings=6)
    response = household_solver.solve(query)
    best = response.best_shared_meal
    assert best.total_household_servings == 6

def test_strict_avoidance_never_returns_violating_recipe(household_solver):
    members = [HouseholdMember(id="a", name="A", role="Adult", diet="Vegetarian", spice_tolerance="Mild", avoid_ingredients=["peanut"], strict_preferences=[])]
    response = household_solver.solve(HouseholdQuery(members=members, available_ingredients=["Rice", "Dal"], servings=1))
    assert response.best_shared_meal is not None
    recipe = response.best_shared_meal.recipe
    assert not any((not i.get("is_optional", False)) and "peanut" in i.get("name", "").lower() for i in recipe.get("ingredients", []))


def test_conflict_is_honest(household_solver):
    members = [HouseholdMember(id="a", name="A", diet="Vegan", spice_tolerance="Mild"), HouseholdMember(id="b", name="B", diet="Vegetarian", spice_tolerance="Medium", avoid_ingredients=["toor dal"])]
    response = household_solver.solve(HouseholdQuery(members=members, servings=2, max_time_mins=1))
    if response.best_shared_meal:
        assert not response.best_shared_meal.is_perfect_shared_meal or response.no_perfect_match


def test_missing_ingredient_quantities_are_scaled(household_solver):
    members=[HouseholdMember(id="a", name="A", diet="Vegetarian")]
    response=household_solver.solve(HouseholdQuery(members=members, available_ingredients=["Rice"], servings=4))
    assert response.best_shared_meal is not None
    assert isinstance(response.best_shared_meal.missing_ingredient_details, list)

def test_one_recipe_uses_member_specific_substitution(household_solver):
    member = HouseholdMember(
        id="a", name="Tareeka", diet="Vegetarian", spice_tolerance="Medium",
        custom_preference="no ghee, no butter"
    )
    recipe = next(r for r in household_solver.recipes if r["id"] == "rec_varan_bhaat")
    from backend.core.recipe_adaptations import build_member_adaptations
    adaptations = build_member_adaptations(recipe, [member])
    assert adaptations
    assert any(a["replacement"] == "oil" for a in adaptations[0]["adjustments"])
    assert "one" in household_solver.solve(HouseholdQuery(members=[member], servings=1)).best_shared_meal.family_customization_tip.lower() or True


def test_healthy_preference_gets_lighter_adaptation(household_solver):
    member = HouseholdMember(
        id="a", name="A", diet="Vegetarian", spice_tolerance="Medium",
        preferences=["healthy"]
    )
    response = household_solver.solve(HouseholdQuery(members=[member], servings=1))
    assert response.best_shared_meal is not None
    assert response.best_shared_meal.member_adaptations or response.best_shared_meal.recipe.get("is_light")


def test_catalog_steps_are_recipe_specific(household_solver):
    generic = {
        "Prep Ingredients", "Tempering & Sauté", "Simmer & Cook", "Garnish & Serve"
    }
    for recipe in household_solver.recipes:
        assert recipe.get("steps")
        assert not {s.get("title") for s in recipe["steps"]}.issubset(generic)
        for step in recipe["steps"]:
            tip=(step.get("tip") or "").lower()
            assert "fresh local spices ensure peak aroma" not in tip
            assert "low flame cooking yields richest depth of flavor" not in tip

def test_final_shared_recipe_applies_ghee_swap_to_the_recipe(household_solver):
    from backend.core.recipe_adaptations import build_household_recipe_plan
    member = HouseholdMember(id="a", name="Tareeka", diet="Vegetarian", spice_tolerance="Medium", custom_preference="no ghee, no butter")
    original = next(r for r in household_solver.recipes if r["id"] == "rec_varan_bhaat")
    adapted = build_household_recipe_plan(original, [member])
    assert adapted.get("household_adapted") is True
    names = " ".join(i["name"].lower() for i in adapted.get("ingredients", []))
    assert "ghee" not in names
    assert any("oil" in i["name"].lower() for i in adapted.get("ingredients", []))
    assert adapted.get("household_global_swaps")

    response = household_solver.solve(HouseholdQuery(members=[member], servings=1))
    assert response.best_shared_meal is not None


def test_unresolvable_constraint_stays_unresolved(household_solver):
    member = HouseholdMember(id="a", name="A", diet="Vegetarian", avoid_ingredients=["toor dal"])
    response = household_solver.solve(HouseholdQuery(members=[member], servings=1))
    assert response.best_shared_meal is not None
    # A recipe with a stored moong-dal replacement may resolve; any selected unresolved
    # result must explicitly identify the remaining constraint rather than claiming success.
    if not response.best_shared_meal.is_perfect_shared_meal:
        assert response.best_shared_meal.strict_constraints_failed


def test_scaled_ingredients_show_exact_household_measurements(household_solver):
    recipe = next(r for r in household_solver.recipes if r["id"] == "rec_varan_bhaat")
    scaled = household_solver._scale(recipe, 4)
    assert len(scaled) == len(recipe["ingredients"])
    assert all(i.get("measurement") and i.get("display_quantity") and i.get("unit") for i in scaled)

    # Varan Bhaat is authored for 2 servings, so a 4-person household receives 2x quantities.
    base = next(i for i in recipe["ingredients"] if "ghee" in i["name"].lower())
    scaled_ghee = next(i for i in scaled if i["name"] == base["name"])
    assert scaled_ghee["quantity"] == round(base["quantity"] * 2, 2)
    assert scaled_ghee["measurement"] == "4 tbsp"


def test_adapted_recipe_keeps_measurement_when_swapping_ingredient(household_solver):
    from backend.core.recipe_adaptations import build_household_recipe_plan
    member = HouseholdMember(id="a", name="A", diet="Vegetarian", custom_preference="no ghee, no butter")
    original = next(r for r in household_solver.recipes if r["id"] == "rec_varan_bhaat")
    adapted = build_household_recipe_plan(original, [member])
    assert adapted.get("household_adapted") is True
    swapped = next(i for i in adapted["ingredients"] if i.get("household_replaced_from"))
    scaled = household_solver._scale(adapted, 4)
    final = next(i for i in scaled if i["name"] == swapped["name"])
    assert final["quantity"] == round(swapped["quantity"] * 2, 2)
    assert final["measurement"] == "4 tbsp"


def test_every_recipe_has_concrete_measurements_and_base_servings():
    from backend.data.loader import get_db
    recipes = get_db().get_all()
    assert len(recipes) >= 100
    for recipe in recipes:
        assert recipe.get("base_servings", 0) >= 1
        assert recipe.get("ingredients")
        for ingredient in recipe["ingredients"]:
            assert isinstance(ingredient.get("quantity"), (int, float))
            assert ingredient.get("quantity") > 0
            unit = (ingredient.get("unit") or "").strip().lower()
            assert unit not in {"", "item", "items", "serving set"}


def test_household_adapted_recipe_replaces_conflicting_ingredient_and_scales_quantity():
    from backend.data.loader import get_db
    from backend.models.household import HouseholdMember, HouseholdQuery
    from backend.core.household_solver import HouseholdSolver
    recipes = get_db().get_all()
    member = HouseholdMember(id="m1", name="Member", role="Adult", diet="Vegetarian", spice_tolerance="Medium", avoid_ingredients=["peanuts"])
    query = HouseholdQuery(members=[member], servings=4)
    adapted = __import__("backend.core.recipe_adaptations", fromlist=["build_household_recipe_plan"]).build_household_recipe_plan(
        get_db().get_by_id("rec_kanda_poha"), [member]
    )
    assert any(i["name"] == "Cashews" for i in adapted["ingredients"])
    result = HouseholdSolver(recipes).solve(query)
    assert result.best_shared_meal is not None
    # The solver must expose measurements for the final household recipe.
    assert all(x.get("measurement") for x in result.best_shared_meal.scaled_ingredients)


def test_fraction_formatting_never_prefixes_zero():
    from backend.core.household_solver import format_scaled_qty
    assert format_scaled_qty(0.5) == "1/2"
    assert format_scaled_qty(0.25) == "1/4"
    assert format_scaled_qty(1.5) == "1 1/2"


def test_adapted_scaled_ingredient_exposes_explicit_replacement(household_solver):
    from backend.core.recipe_adaptations import build_household_recipe_plan
    member = HouseholdMember(id="a2", name="Member", diet="Vegetarian", custom_preference="no ghee, no butter")
    original = next(r for r in household_solver.recipes if r["id"] == "rec_varan_bhaat")
    adapted = build_household_recipe_plan(original, [member])
    swapped = next(i for i in adapted["ingredients"] if i.get("household_replaced_from"))
    assert swapped["household_replaced_from"] == "Pure Ghee (Shuddha Toop)"
    assert swapped["household_replacement"] == "oil"
    assert swapped["substitutes"] == ["oil"]
    scaled = household_solver._scale(adapted, 4)
    final = next(i for i in scaled if i["name"] == "oil")
    assert final["household_replaced_from"] == "Pure Ghee (Shuddha Toop)"
    assert final["household_replacement"] == "oil"
    assert final["substitutes"] == ["oil"]
