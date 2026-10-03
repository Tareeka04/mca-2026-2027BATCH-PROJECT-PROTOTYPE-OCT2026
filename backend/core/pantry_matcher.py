"""
Pantry Ingredient Matching and Gap Analysis Engine.
Calculates ingredient coverage, missing items, substitute recommendations, and ready-to-cook scoring.
"""
from typing import List, Dict, Any, Set, Tuple
from backend.core.substitutes import find_substitutes_for_missing, get_substitute_for_ingredient
from backend.core.ir_engine import SYNONYM_MAP, clean_text

BASIC_PANTRY_STAPLES = {
    "salt", "water", "oil", "turmeric", "haldi", "mustard seed", "rai", "cumin", "jeera", "sugar"
}

def clean_ingredient_name(raw_name: str) -> str:
    """Extract core ingredient name removing parenthetical notes like '(finely chopped)'."""
    cleaned = raw_name.split('(')[0].strip()
    return clean_text(cleaned)

def expand_user_pantry(user_items: List[str]) -> Set[str]:
    """Expand user's available pantry items using culinary synonyms."""
    expanded: Set[str] = set()
    for item in user_items:
        norm = clean_text(item)
        if not norm:
            continue
        expanded.add(norm)
        for word in norm.split():
            if word in SYNONYM_MAP:
                for syn in SYNONYM_MAP[word]:
                    expanded.add(clean_text(syn))
    return expanded

def is_ingredient_available(ing_name: str, expanded_pantry: Set[str]) -> bool:
    """Check if an ingredient is present in the expanded user pantry."""
    norm = clean_ingredient_name(ing_name)
    if not norm:
        return True

    # 1. Direct match
    if norm in expanded_pantry:
        return True

    # 2. Check if any pantry item is a distinct substring of ingredient or vice versa
    for p_item in expanded_pantry:
        if len(p_item) >= 3:
            if p_item == norm:
                return True
            # Check whole words
            p_words = set(p_item.split())
            norm_words = set(norm.split())
            if p_words.issubset(norm_words) or norm_words.issubset(p_words):
                return True
    return False

class PantryMatcher:
    def __init__(self, recipes: List[Dict[str, Any]]):
        self.recipes = recipes

    def match_recipes(
        self,
        pantry_items: List[str],
        filters: Dict[str, Any] = None,
        include_substitutes: bool = True,
        must_include: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Evaluate all recipes against user pantry items and rank by feasibility.
        """
        if not pantry_items:
            return []

        expanded_pantry = expand_user_pantry(pantry_items)
        results = []

        must_include_set = {clean_text(m) for m in (must_include or []) if clean_text(m)}

        for r in self.recipes:
            # Apply constraint filters first
            if not self._apply_filters(r, filters):
                continue

            recipe_ings = r.get("ingredients", [])
            recipe_norm_ings = r.get("normalized_ingredients", [])

            # Must include check
            if must_include_set:
                recipe_text = clean_text(" ".join(recipe_norm_ings) + " " + r.get("title", ""))
                if not all(m in recipe_text for m in must_include_set):
                    continue

            matched = []
            missing_essential = []
            missing_optional = []
            substitute_matches: Dict[str, List[str]] = {}

            essential_count = 0

            for ing in recipe_ings:
                name = ing.get("name", "")
                is_opt = ing.get("is_optional", False)
                if not is_opt:
                    essential_count += 1

                if is_ingredient_available(name, expanded_pantry):
                    matched.append(name)
                else:
                    # Check substitute
                    has_sub = False
                    if include_substitutes:
                        norm_core = clean_ingredient_name(name)
                        sub_info = get_substitute_for_ingredient(norm_core)
                        if sub_info:
                            for sub in sub_info["substitutes"]:
                                sub_clean = clean_text(sub)
                                if is_ingredient_available(sub_clean, expanded_pantry):
                                    has_sub = True
                                    substitute_matches[name] = [sub]
                                    break

                    if has_sub:
                        matched.append(f"{name} (via {substitute_matches[name][0]})")
                    else:
                        if is_opt:
                            missing_optional.append(name)
                        else:
                            missing_essential.append(name)

            total_recipe_ings = len(recipe_ings)
            if total_recipe_ings == 0:
                continue

            # Calculate match percentage
            essential_matched = essential_count - len(missing_essential)
            essential_score = (essential_matched / max(essential_count, 1)) if essential_count > 0 else 1.0

            opt_total = total_recipe_ings - essential_count
            opt_score = ((opt_total - len(missing_optional)) / max(opt_total, 1)) if opt_total > 0 else 1.0

            # Direct coverage ratio
            overall_match_ratio = (0.85 * essential_score) + (0.15 * opt_score)
            match_percentage = int(round(overall_match_ratio * 100))

            if match_percentage < 25 and len(matched) < 2:
                continue

            # Determine readiness badge
            if len(missing_essential) == 0:
                ready_badge = "Ready to Cook Now"
                is_ready = True
            elif len(missing_essential) == 1:
                ready_badge = "Missing 1 Essential Item"
                is_ready = False
            elif len(missing_essential) == 2:
                ready_badge = "Missing 2 Essential Items"
                is_ready = False
            else:
                ready_badge = f"Missing {len(missing_essential)} Items"
                is_ready = False

            # Get substitute suggestions for missing items
            missing_subs = find_substitutes_for_missing(missing_essential)

            results.append({
                "recipe": r,
                "match_score": round(overall_match_ratio, 3),
                "match_percentage": match_percentage,
                "matched_ingredients": matched,
                "missing_ingredients": missing_essential,
                "missing_optional": missing_optional,
                "substitute_suggestions": missing_subs,
                "is_ready_to_cook": is_ready,
                "ready_badge": ready_badge
            })

        # Rank results:
        # 1. Ready to cook first
        # 2. Fewest missing essential items
        # 3. Highest match percentage
        # 4. Total cooking time
        results.sort(key=lambda x: (
            not x["is_ready_to_cook"],
            len(x["missing_ingredients"]),
            -x["match_percentage"],
            x["recipe"].get("total_time_mins", 999)
        ))

        return results

    def _apply_filters(self, recipe: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        if not filters:
            return True

        diet_filter = filters.get("diet")
        if diet_filter:
            diet_lower = diet_filter.lower()
            if diet_lower == "vegetarian" and recipe.get("diet") not in ["Vegetarian", "Vegan"]:
                return False
            if diet_lower == "vegan" and not recipe.get("is_vegan", False):
                return False
            if diet_lower == "jain" and not recipe.get("is_jain", False):
                return False
            if diet_lower == "gluten-free" and not recipe.get("is_gluten_free", False):
                return False

        max_time = filters.get("max_time_mins")
        if max_time and recipe.get("total_time_mins", 0) > int(max_time):
            return False

        meal_type = filters.get("meal_type")
        if meal_type:
            recipe_meal_types = [m.lower() for m in recipe.get("meal_type", [])]
            if meal_type.lower() not in recipe_meal_types and meal_type.lower() != recipe.get("course", "").lower():
                return False

        cuisine = filters.get("cuisine")
        if cuisine and cuisine.lower() != "all":
            if cuisine.lower() not in recipe.get("regional_cuisine", "").lower():
                return False

        difficulty = filters.get("difficulty")
        if difficulty and difficulty.lower() != "all":
            if difficulty.lower() != recipe.get("difficulty", "").lower():
                return False

        return True
