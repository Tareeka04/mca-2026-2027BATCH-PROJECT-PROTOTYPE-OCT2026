"""
Leftover Transformation Engine for Indian Kitchens.
Maps leftover staples (Cooked Rice, Stale Roti, Leftover Dal, Boiled Potatoes, Sour Curd, Bread, Leftover Sabzi)
to authentic transformative dishes with specialized preparation tips.
"""
from typing import List, Dict, Any, Optional
from backend.core.ir_engine import clean_text

LEFTOVER_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "cooked rice": {
        "aliases": ["rice", "bhaat", "chawal", "leftover rice", "cold rice", "cooked basmati"],
        "recipes": [
            {
                "recipe_id": "rec_phodnicha_bhaat",
                "transformation_name": "Phodnicha Bhaat (Maharashtrian Tempered Spiced Rice)",
                "tip": "Cold leftover rice is best because grains stay separate! Use hot mustard oil or ghee tempering with peanuts and fresh coriander.",
                "speed": "< 10 Mins"
            },
            {
                "recipe_id": "rec_curd_rice",
                "transformation_name": "Daddojanam / South Indian Curd Rice",
                "tip": "Gently mash rice with fresh curd, milk, and temper with mustard, curry leaves, and ginger.",
                "speed": "< 8 Mins"
            },
            {
                "recipe_id": "rec_lemon_rice",
                "transformation_name": "Chitranna (Tangy Lemon Peanut Rice)",
                "tip": "Sauté crunchy peanuts and chana dal in turmeric oil; toss cold rice and finish with fresh lemon juice.",
                "speed": "< 10 Mins"
            },
            {
                "recipe_id": "rec_tawa_pulao",
                "transformation_name": "Mumbai Tawa Pulao",
                "tip": "Stir-fry with Pav Bhaji masala, diced onions, tomatoes, and butter for a street-style meal.",
                "speed": "< 15 Mins"
            },
            {
                "recipe_id": "rec_rice_cutlet",
                "transformation_name": "Crispy Leftover Rice Cutlets",
                "tip": "Mash rice with 1 boiled potato, spices, shape into patties and pan-fry till golden.",
                "speed": "< 15 Mins"
            }
        ]
    },
    "stale roti": {
        "aliases": ["roti", "chapati", "poli", "phulka", "leftover roti", "stale chapati", "leftover poli"],
        "recipes": [
            {
                "recipe_id": "rec_phodnichi_poli",
                "transformation_name": "Phodnichi Poli (Spiced Tempered Chapati Chivda)",
                "tip": "Tear stale rotis into small bite-sized bits. Temper with mustard seeds, curry leaves, onions, peanuts, and turmeric. Soften with a splash of water.",
                "speed": "< 10 Mins"
            },
            {
                "recipe_id": "rec_roti_ladoo",
                "transformation_name": "Gul-Poli Ladoo / Malida",
                "tip": "Tear dry rotis, pulse in mixer with organic jaggery, cardamom, and warm ghee; roll into nutritious energy ladoos.",
                "speed": "< 5 Mins"
            },
            {
                "recipe_id": "rec_roti_frankie",
                "transformation_name": "Crispy Roti Roll / Desi Frankie",
                "tip": "Toast roti with butter till crisp, spread mint chutney, stuff with spiced potato/paneer filling, roll tightly.",
                "speed": "< 12 Mins"
            },
            {
                "recipe_id": "rec_roti_noodles",
                "transformation_name": "Desi Masala Roti Noodles",
                "tip": "Roll chapatis tightly and slice into thin ribbons. Toss with julienned vegetables and chaat masala.",
                "speed": "< 12 Mins"
            }
        ]
    },
    "leftover dal": {
        "aliases": ["dal", "varan", "toor dal", "leftover dal", "yellow dal", "moong dal", "sambar"],
        "recipes": [
            {
                "recipe_id": "rec_dal_paratha",
                "transformation_name": "Spiced Dal Paratha (Missi Roti Style)",
                "tip": "Use leftover dal directly instead of water to knead whole wheat dough with ajwain, kasuri methi, and green chillies. Produces ultra-soft flaky parathas!",
                "speed": "< 15 Mins"
            },
            {
                "recipe_id": "rec_chakolya",
                "transformation_name": "Chakolya / Varan Phal (Maharashtrian Dal Dhokli)",
                "tip": "Thin down leftover dal with water and bring to rolling boil. Drop fresh spiced wheat diamonds directly in the boiling dal to cook.",
                "speed": "< 20 Mins"
            },
            {
                "recipe_id": "rec_dal_khichdi",
                "transformation_name": "Tadka Dal Khichdi",
                "tip": "Simmer leftover dal with equal part cooked rice and top with a sizzling double garlic-ghee phodni.",
                "speed": "< 10 Mins"
            }
        ]
    },
    "boiled potatoes": {
        "aliases": ["boiled potato", "potato", "batata", "aloo", "boiled aloo", "boiled batata"],
        "recipes": [
            {
                "recipe_id": "rec_batata_vada",
                "transformation_name": "Maharashtrian Batata Vada",
                "tip": "Mash boiled potatoes with green chilli-ginger-garlic paste and mustard tempering, dip in spiced besan batter and fry.",
                "speed": "< 15 Mins"
            },
            {
                "recipe_id": "rec_sukhi_batata_bhaji",
                "transformation_name": "Sukhi Batata Bhaji (Puri-Bhaji style)",
                "tip": "Cube potatoes and toss in hot mustard-curry leaf-green chilli tempering with turmeric and fresh coriander.",
                "speed": "< 10 Mins"
            },
            {
                "recipe_id": "rec_aloo_tikki",
                "transformation_name": "Crispy Aloo Tikki / Chaat Patties",
                "tip": "Mash with roasted cumin, chaat masala, and 1 tbsp cornflour/rice flour; shallow fry on tawa until crackling crisp.",
                "speed": "< 12 Mins"
            }
        ]
    },
    "sour curd": {
        "aliases": ["sour curd", "khatta dahi", "dahi", "curd", "yogurt", "taak", "buttermilk"],
        "recipes": [
            {
                "recipe_id": "rec_maharashtrian_kadhi",
                "transformation_name": "Maharashtrian Sweet & Tangy Kadhi",
                "tip": "Whisk sour curd with 1.5 tbsp besan, water, ginger-chilli paste, and jaggery. Simmer and temper with cloves, cinnamon, and curry leaves.",
                "speed": "< 15 Mins"
            },
            {
                "recipe_id": "rec_dahi_tadka",
                "transformation_name": "Dhabha Style Dahi Tadka",
                "tip": "Pour sizzling hot ghee tempering of garlic, cumin, and Kashmiri red chilli directly over thick beaten curd. Do not cook the curd!",
                "speed": "< 5 Mins"
            },
            {
                "recipe_id": "rec_rava_dhokla",
                "transformation_name": "Instant Khatta Rava Dhokla",
                "tip": "Mix sour curd with semolina (sooji) for instant natural fermentation and fluffy steamed savoury cakes.",
                "speed": "< 15 Mins"
            }
        ]
    },
    "leftover bread": {
        "aliases": ["bread", "bread slices", "white bread", "brown bread", "pav", "stale bread"],
        "recipes": [
            {
                "recipe_id": "rec_bread_upma",
                "transformation_name": "Spiced Bread Upma (Phodnicha Bread)",
                "tip": "Cut bread into bite-sized cubes. Temper mustard, curry leaves, onions, tomatoes, peanuts, and toss bread cubes till slightly crisp.",
                "speed": "< 10 Mins"
            },
            {
                "recipe_id": "rec_bread_pakora",
                "transformation_name": "Street-Style Bread Pakora",
                "tip": "Cut triangles, spread green chutney, dip in ajwain-besan batter and fry crisp.",
                "speed": "< 15 Mins"
            }
        ]
    },
    "leftover sabzi": {
        "aliases": ["sabzi", "bhaji", "leftover curry", "dry sabzi", "mix veg"],
        "recipes": [
            {
                "recipe_id": "rec_sabzi_paratha",
                "transformation_name": "Stuffed Leftover Sabzi Paratha",
                "tip": "Mash leftover dry vegetables, add fresh chopped coriander and amchur, roll inside paratha dough.",
                "speed": "< 15 Mins"
            },
            {
                "recipe_id": "rec_veg_toast_sandwich",
                "transformation_name": "Mumbai Masala Toast Sandwich",
                "tip": "Layer leftover cooked vegetables between buttered bread with green chutney and chaat masala, toast crisp.",
                "speed": "< 10 Mins"
            }
        ]
    }
}

class LeftoverSolver:
    def __init__(self, recipes_by_id: Dict[str, Any]):
        self.recipes_by_id = recipes_by_id

    def solve(
        self,
        leftover_items: List[str],
        additional_ingredients: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Match leftover items to authentic transformative recipes.
        """
        if not leftover_items:
            return []

        results = []
        matched_recipe_ids = set()

        # Check each user leftover against taxonomy
        for user_item in leftover_items:
            u_clean = clean_text(user_item)
            if not u_clean:
                continue

            for canon_key, data in LEFTOVER_TAXONOMY.items():
                # Check alias match
                is_match = False
                if u_clean in canon_key or canon_key in u_clean:
                    is_match = True
                else:
                    for alias in data["aliases"]:
                        if alias in u_clean or u_clean in alias:
                            is_match = True
                            break

                if is_match:
                    for transform_entry in data["recipes"]:
                        r_id = transform_entry["recipe_id"]
                        if r_id in matched_recipe_ids:
                            continue

                        # Find recipe object in database
                        recipe_obj = self.recipes_by_id.get(r_id)
                        if not recipe_obj:
                            # If not direct ID match, fallback to recipe search by title
                            for r in self.recipes_by_id.values():
                                if clean_text(transform_entry["transformation_name"]) in clean_text(r.get("title", "")):
                                    recipe_obj = r
                                    break

                        if recipe_obj:
                            # Apply filters
                            if not self._apply_filters(recipe_obj, filters):
                                continue

                            # Check additional ingredients needed
                            needed = [
                                ing["name"] for ing in recipe_obj.get("ingredients", [])
                                if not ing.get("is_optional", False) and u_clean not in clean_text(ing["name"])
                            ]

                            results.append({
                                "recipe": recipe_obj,
                                "primary_leftover": canon_key.title(),
                                "transformation_name": transform_entry["transformation_name"],
                                "transformation_tip": transform_entry["tip"],
                                "prep_speed_badge": transform_entry["speed"],
                                "additional_needed": needed[:4],
                                "match_score": 0.95
                            })
                            matched_recipe_ids.add(r_id)

        # Also search general recipes that explicitly declare leftover_ingredients_used
        for u_item in leftover_items:
            u_clean = clean_text(u_item)
            for r in self.recipes_by_id.values():
                if r["id"] in matched_recipe_ids:
                    continue
                leftovers_used = [clean_text(x) for x in r.get("leftover_ingredients_used", [])]
                if any(u_clean in l or l in u_clean for l in leftovers_used):
                    if not self._apply_filters(r, filters):
                        continue
                    results.append({
                        "recipe": r,
                        "primary_leftover": u_item.title(),
                        "transformation_name": r.get("title", ""),
                        "transformation_tip": f"Transform your leftover {u_item} directly into this delicious {r.get('regional_cuisine')} recipe.",
                        "prep_speed_badge": f"< {r.get('total_time_mins', 20)} Mins",
                        "additional_needed": [ing["name"] for ing in r.get("ingredients", [])[:3]],
                        "match_score": 0.90
                    })
                    matched_recipe_ids.add(r["id"])

        return results

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
        return True
