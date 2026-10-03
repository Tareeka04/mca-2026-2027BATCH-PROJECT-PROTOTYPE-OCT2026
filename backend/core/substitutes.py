"""
Indian Household Ingredient Substitution Knowledge Engine.
Provides bidirectional mappings, notes on flavor alterations, and suitability.
"""
from typing import Dict, List, Optional

INDIAN_SUBSTITUTIONS: Dict[str, Dict[str, any]] = {
    "kokum": {
        "substitutes": ["tamarind", "amchur (dry mango powder)", "lemon juice"],
        "note": "Use 1/2 tsp tamarind paste or 1/2 tsp amchur in place of 2-3 kokum petals for authentic tanginess.",
        "cuisine_context": "Maharashtrian / Konkani"
    },
    "goda masala": {
        "substitutes": ["garam masala + roasted coriander powder", "kala masala", "garam masala + pinch of coconut"],
        "note": "Mix 1/2 tsp Garam Masala + 1/2 tsp roasted coriander-cumin powder with a pinch of desiccated coconut.",
        "cuisine_context": "Maharashtrian"
    },
    "kala masala": {
        "substitutes": ["goda masala", "garam masala + roasted onion paste"],
        "note": "Goda masala is the closest substitute; add slightly toasted dry coconut.",
        "cuisine_context": "Maharashtrian / Khandeshi"
    },
    "jaggery": {
        "substitutes": ["brown sugar", "raw sugar", "cane sugar", "honey"],
        "note": "Brown sugar provides a similar caramel molasses depth. Use equal ratio.",
        "cuisine_context": "All Indian"
    },
    "fresh coconut": {
        "substitutes": ["desiccated coconut (soaked in warm milk)", "coconut milk", "coconut powder"],
        "note": "Soak 2 tbsp dry desiccated coconut in 1 tbsp warm water or milk for 5 mins to restore moisture.",
        "cuisine_context": "Maharashtrian / South Indian / Coastal"
    },
    "sour curd": {
        "substitutes": ["fresh curd + 1/2 tsp lemon juice", "buttermilk (taak)", "greek yogurt"],
        "note": "Add 1/2 tsp lemon juice to fresh curd to get that signature kadhi/dhokla tang.",
        "cuisine_context": "All Indian"
    },
    "besan": {
        "substitutes": ["roasted chana dal flour (sattu)", "chickpea flour", "rice flour (for crispy coatings)"],
        "note": "Sattu or ground roasted chana gives rich nutty taste with high protein.",
        "cuisine_context": "All Indian"
    },
    "poha": {
        "substitutes": ["rolled oats", "puffed rice (murmura)", "flattened corn flakes"],
        "note": "Rolled oats cook identically to poha for a high-fiber Oats Poha.",
        "cuisine_context": "Breakfast"
    },
    "paneer": {
        "substitutes": ["firm tofu", "boiled baby potatoes", "white button mushrooms"],
        "note": "Firm tofu soaks up Indian gravies similarly while being 100% vegan.",
        "cuisine_context": "North Indian"
    },
    "sabudana": {
        "substitutes": ["varai (samak rice / bhagar)", "rajgira flour", "singhara flour"],
        "note": "Varai / Bhagar is the traditional fasting (Upwas) grain substitute for Sabudana.",
        "cuisine_context": "Upwas / Fasting"
    },
    "matki": {
        "substitutes": ["sprouted moong", "brown chickpeas (kala chana)", "white peas (vatana)"],
        "note": "Sprouted green moong works seamlessly in Usal and Misal gravies.",
        "cuisine_context": "Maharashtrian Usal"
    },
    "kasuri methi": {
        "substitutes": ["fresh fenugreek leaves (sautéed)", "finely chopped celery leaves", "coriander"],
        "note": "Lightly sauté fresh methi leaves in 1/2 tsp oil before adding.",
        "cuisine_context": "North Indian"
    },
    "curry leaves": {
        "substitutes": ["fresh coriander + pinch of lime zest", "kaffir lime leaf"],
        "note": "While unique, fresh coriander stems bruised in hot oil provide fresh herbal aroma.",
        "cuisine_context": "South & West Indian"
    },
    "hing": {
        "substitutes": ["garlic paste (if not Jain)", "shallot paste", "ginger powder"],
        "note": "If cooking without onions/garlic, a tiny pinch of celery seed powder or cumin helps digestion.",
        "cuisine_context": "All Indian"
    },
    "amchur": {
        "substitutes": ["lemon juice", "anardana (pomegranate seed powder)", "tamarind paste"],
        "note": "1/2 tsp lemon juice added at the end replaces 1/2 tsp amchur powder.",
        "cuisine_context": "North Indian / Chaat"
    },
    "ghee": {
        "substitutes": ["butter", "cold-pressed groundnut oil", "coconut oil"],
        "note": "Unsalted butter browned for 1 min gives near-identical nutty ghee aroma.",
        "cuisine_context": "All Indian"
    }
}

def get_substitute_for_ingredient(ingredient_name: str) -> Optional[Dict[str, any]]:
    """Look up substitutes for a single ingredient name."""
    name_lower = ingredient_name.lower().strip()
    for key, data in INDIAN_SUBSTITUTIONS.items():
        if key in name_lower or name_lower in key:
            return data
    return None

def find_substitutes_for_missing(missing_list: List[str]) -> Dict[str, List[str]]:
    """Return substitution suggestions for missing ingredients."""
    suggestions: Dict[str, List[str]] = {}
    for item in missing_list:
        sub_info = get_substitute_for_ingredient(item)
        if sub_info:
            suggestions[item] = sub_info["substitutes"]
    return suggestions
