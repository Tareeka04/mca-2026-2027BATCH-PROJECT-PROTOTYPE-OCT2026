"""
Craving, Mood, and Hybrid Recommendation Engine.
Combines IR query relevance, flavor profile vector alignment, mood tag matching, and constraint rules.
"""
from typing import List, Dict, Any, Optional
import numpy as np
from backend.core.ir_engine import IREngine, clean_text

class CravingRecommender:
    def __init__(self, ir_engine: IREngine):
        self.ir_engine = ir_engine

    def recommend(
        self,
        query_text: Optional[str] = None,
        spicy_target: Optional[int] = None,
        tangy_target: Optional[int] = None,
        sweet_target: Optional[int] = None,
        comfort_target: Optional[int] = None,
        mood: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Produce ranked craving & mood recommendations.
        """
        recipes = self.ir_engine.recipes
        if not recipes:
            return []

        # 1. Base IR scores from text query (if any)
        if query_text and query_text.strip():
            ir_results = self.ir_engine.search_hybrid(query_text)
            ir_score_map = {r["id"]: score for r, score in ir_results}
        else:
            ir_score_map = {r["id"]: 0.5 for r in recipes}

        ranked_list = []

        # Check if flavor sliders were provided
        has_flavor_preference = any(x is not None for x in [spicy_target, tangy_target, sweet_target, comfort_target])

        for r in recipes:
            # Apply constraint filters
            if not self._apply_filters(r, filters):
                continue

            r_id = r["id"]
            ir_score = ir_score_map.get(r_id, 0.0)

            # 2. Flavor profile score (Cosine similarity or normalized Euclidean distance)
            flavor = r.get("flavor_profile", {})
            r_spicy = flavor.get("spicy", 2)
            r_tangy = flavor.get("tangy", 2)
            r_sweet = flavor.get("sweet", 1)
            r_comfort = flavor.get("comfort", 3)

            flavor_score = 1.0
            reasons = []

            if has_flavor_preference:
                # Vector distance
                diffs = []
                if spicy_target is not None:
                    diffs.append(abs(r_spicy - spicy_target) / 5.0)
                    if abs(r_spicy - spicy_target) <= 1:
                        reasons.append(f"Spiciness level matches ({r_spicy}/5)")
                if tangy_target is not None:
                    diffs.append(abs(r_tangy - tangy_target) / 5.0)
                    if abs(r_tangy - tangy_target) <= 1:
                        reasons.append(f"Tanginess level matches ({r_tangy}/5)")
                if sweet_target is not None:
                    diffs.append(abs(r_sweet - sweet_target) / 5.0)
                    if abs(r_sweet - sweet_target) <= 1:
                        reasons.append(f"Sweetness level matches ({r_sweet}/5)")
                if comfort_target is not None:
                    diffs.append(abs(r_comfort - comfort_target) / 5.0)
                    if abs(r_comfort - comfort_target) <= 1:
                        reasons.append(f"Comfort score matches ({r_comfort}/5)")

                avg_diff = sum(diffs) / len(diffs) if diffs else 0.0
                flavor_score = max(0.0, 1.0 - avg_diff)

            # 3. Mood alignment score
            mood_score = 0.0
            recipe_moods = [clean_text(m) for m in r.get("mood_tags", [])]
            if mood:
                mood_clean = clean_text(mood)
                if mood_clean in recipe_moods or any(m in mood_clean for m in recipe_moods):
                    mood_score = 1.0
                    reasons.append(f"Fits '{mood}' mood perfectly")
                elif mood_clean == "quick" and r.get("total_time_mins", 60) <= 25:
                    mood_score = 0.9
                    reasons.append("Quick to make (under 25 mins)")
                elif mood_clean == "healthy" and r.get("nutrition_per_serving", {}).get("calories", 500) < 350:
                    mood_score = 0.9
                    reasons.append("Wholesome & balanced calorie profile")

            # 4. Composite Relevance Calculation
            if query_text and query_text.strip():
                if has_flavor_preference:
                    final_score = (0.50 * ir_score) + (0.35 * flavor_score) + (0.15 * mood_score)
                else:
                    final_score = (0.70 * ir_score) + (0.30 * mood_score if mood else 0.0)
            else:
                if has_flavor_preference:
                    final_score = (0.65 * flavor_score) + (0.35 * (mood_score if mood else 0.5))
                else:
                    final_score = 0.85 if mood_score > 0 else 0.5

            if not reasons:
                if r.get("regional_cuisine"):
                    reasons.append(f"Authentic {r.get('regional_cuisine')} speciality")
                reasons.append(f"Takes only {r.get('total_time_mins')} mins")

            relevance_percentage = int(min(100, max(20, round(final_score * 100))))

            ranked_list.append({
                "recipe": r,
                "relevance_score": round(float(final_score), 3),
                "relevance_percentage": relevance_percentage,
                "matched_reasons": reasons[:3],
                "taste_profile": {
                    "spicy": r_spicy,
                    "tangy": r_tangy,
                    "sweet": r_sweet,
                    "comfort": r_comfort
                }
            })

        # Sort by composite score descending
        ranked_list.sort(key=lambda x: x["relevance_score"], reverse=True)
        return ranked_list[:top_k]

    def _apply_filters(self, recipe: Dict[str, Any], filters: Optional[Dict[str, Any]]) -> bool:
        if not filters:
            return True

        diet = filters.get("diet")
        if diet:
            diet_lower = diet.lower()
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
