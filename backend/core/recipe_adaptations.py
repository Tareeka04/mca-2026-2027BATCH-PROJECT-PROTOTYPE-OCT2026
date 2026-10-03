"""Household-specific adaptations that keep ONE recipe while handling different member needs."""
from typing import Any, Dict, List, Optional, Tuple
import re
from backend.core.ir_engine import clean_text
from backend.core.substitutes import get_substitute_for_ingredient

SAFE_SUBSTITUTIONS = {
    "ghee": ["oil"],
    "pure ghee": ["oil"],
    "butter": ["oil", "olive oil"],
    "white butter": ["oil"],
    "loni": ["oil"],
    "oil or ghee": ["oil"],
    "milk": ["unsweetened plant milk"],
    "cream": ["thick unsweetened curd"],
    "paneer": ["firm tofu"],
    "curd": ["unsweetened plant yogurt"],
    "yogurt": ["unsweetened plant yogurt"],
    "onion": ["finely chopped cabbage"],
    "garlic": ["fresh ginger"],
    "green chilli": ["black pepper"],
    "red chilli powder": ["kashmiri chilli powder"],
    "sugar": ["jaggery", "reduce by half"],
    "jaggery": ["reduce by half", "date paste"],
    "salt": ["reduce salt in shared base; season individual portions"],
    "peanut": ["roasted chana dal"],
    "peanuts": ["roasted chana dal"],
    "wheat": ["rice flour"],
    "wheat flour": ["gluten-free flour blend"],
    "atta": ["gluten-free flour blend"],
    "maida": ["gluten-free flour blend"],
    "potato": ["cauliflower"],
    "aloo": ["cauliflower"],
    "tomato": ["roasted red pepper"],
}

HEALTHY_CUES = {"healthy", "healthier", "wholesome", "balanced", "light", "low oil", "less oil", "low salt", "less salt", "low sugar", "less sugar"}

def _rules(member) -> Tuple[set, set]:
    raw = list(getattr(member, "avoid_ingredients", []) or [])
    custom = getattr(member, "custom_preference", None)
    if custom:
        raw.extend(re.split(r"[,;]+", custom))
    avoid, required = set(), set()
    for item in raw:
        n = clean_text(item)
        if not n:
            continue
        m = re.match(r"^(?:no|without|free from)\s+(.+)$", n)
        if m:
            avoid.add(m.group(1).strip()); continue
        if re.match(r"^(?:high|extra|more)\s+salt$", n):
            required.add("salt"); continue
        avoid.add(n)
    return avoid, required

def _ingredient_hit(name: str, target: str) -> bool:
    n, t = clean_text(name), clean_text(target)
    if not n or not t:
        return False
    if t == "dairy":
        return any(x in n for x in ("milk", "curd", "yogurt", "paneer", "ghee", "butter", "cream", "cheese"))
    return t == n or f" {t} " in f" {n} " or (t.rstrip('s') and t.rstrip('s') in n)

def _candidate_substitutes(ingredient: Dict[str, Any]) -> List[str]:
    name = clean_text(ingredient.get("name", ""))
    candidates = list(ingredient.get("substitutes", []) or [])
    # Prefer the household-safe mappings used by the solver, then recipe-specific
    # substitutions, then the broader Indian substitution knowledge base.
    safe_candidates = []
    for key, vals in SAFE_SUBSTITUTIONS.items():
        if key in name or name in key:
            safe_candidates.extend(vals)
    kb = get_substitute_for_ingredient(ingredient.get("name", ""))
    kb_candidates = kb.get("substitutes", []) if kb else []
    candidates = candidates + safe_candidates + list(kb_candidates)
    return list(dict.fromkeys(candidates))

def _blocked(candidate: str, member) -> bool:
    c = clean_text(candidate)
    avoid, _ = _rules(member)
    for a in avoid:
        if a == "dairy" and any(x in c for x in ("milk", "curd", "yogurt", "paneer", "ghee", "butter", "cream", "cheese")):
            return True
        if a in c or c in a:
            return True
    diet = clean_text(getattr(member, "diet", ""))
    if diet == "vegan" and any(x in c for x in ("milk", "curd", "yogurt", "paneer", "ghee", "butter", "cream", "cheese")):
        return True
    return False

def _find_replacement(ingredient: Dict[str, Any], member) -> Optional[str]:
    for c in _candidate_substitutes(ingredient):
        if not _blocked(c, member):
            return c
    return None

def _is_healthy_request(member) -> bool:
    prefs = [str(x).lower().replace("_", " ") for x in (getattr(member, "preferences", []) or []) + (getattr(member, "strict_preferences", []) or [])]
    custom = clean_text(getattr(member, "custom_preference", "") or "")
    return any(cue in " ".join(prefs) + " " + custom for cue in HEALTHY_CUES)

def _ingredient_names(recipe):
    return [clean_text(i.get("name", "")) for i in recipe.get("ingredients", [])]


def build_household_recipe_plan(recipe: Dict[str, Any], members: List[Any]) -> Dict[str, Any]:
    """Build the actual ONE-recipe cooking plan for the whole household.

    Global substitutions are applied when a recipe ingredient conflicts with one or more
    members and the same replacement is acceptable to every affected member.  Salt, spice,
    and similar finishing differences remain one recipe with a split-at-the-end instruction.
    """
    import copy
    adapted = copy.deepcopy(recipe)
    global_swaps = []
    portion_steps = []

    for ing in adapted.get("ingredients", []):
        affected = []
        for member in members:
            avoid, _ = _rules(member)
            hits = any(_ingredient_hit(ing.get("name", ""), a) for a in avoid)
            if hits:
                affected.append(member)
        if not affected or ing.get("is_optional", False):
            continue
        replacements = []
        for member in affected:
            replacement = _find_replacement(ing, member)
            if not replacement:
                replacements = []
                break
            replacements.append(replacement)
        if replacements and len(set(map(clean_text, replacements))) == 1:
            replacement = replacements[0]
            original = ing.get("name", "")
            ing["name"] = replacement
            ing["household_replaced_from"] = original
            ing["household_replacement"] = replacement
            ing["household_adaptation"] = True
            # Keep the replacement visible wherever this adapted ingredient is rendered.
            ing["substitutes"] = [replacement]
            global_swaps.append({
                "original": original, "replacement": replacement,
                "members": [m.name for m in affected],
                "instruction": f"Use {replacement} instead of {original} for the whole household."
            })

    # Keep the recipe one shared preparation when salt/spice needs differ.
    for member in members:
        _, required = _rules(member)
        if "salt" in required:
            portion_steps.append({
                "member": member.name, "instruction": f"Keep the shared base lightly salted, serve {member.name}'s portion, then add salt to that portion to taste."
            })
        spice = clean_text(getattr(member, "spice_tolerance", "medium"))
        if spice in ("mild", "low"):
            chilli = next((i for i in recipe.get("ingredients", []) if any(x in clean_text(i.get("name", "")) for x in ("chilli", "chili", "pepper"))), None)
            if chilli:
                portion_steps.append({
                    "member": member.name, "instruction": f"Keep the common base mild; serve {member.name}'s portion before adding extra chilli or hot spice to other portions."
                })

    # Healthy/balanced requests are also turned into an explicit part of the one-recipe plan.
    healthy_members = [m for m in members if _is_healthy_request(m)]
    if healthy_members:
        fats = [i for i in adapted.get("ingredients", []) if any(x in clean_text(i.get("name", "")) for x in ("ghee", "butter", "oil"))]
        sweeteners = [i for i in adapted.get("ingredients", []) if any(x in clean_text(i.get("name", "")) for x in ("sugar", "jaggery", "sweetener"))]
        title = clean_text(adapted.get("title", ""))
        fried = any(x in title for x in ("fried", "fritter", "pakora", "vada", "tikki", "cutlet", "bhakarwadi", "shankarpali"))
        if fats or sweeteners or fried or not adapted.get("is_light"):
            adapted["household_health_adapted"] = True
            adapted["is_light"] = True
            for member in healthy_members:
                if fats:
                    portion_steps.append({"member": member.name, "instruction": f"For {member.name}, measure the cooking fat and use only the minimum needed for the same cooking step; do not free-pour extra oil/ghee."})
                if sweeteners:
                    portion_steps.append({"member": member.name, "instruction": f"Keep {member.name}'s portion less sweet by reducing or omitting the added sweetener at the finishing stage where the recipe allows."})
                if fried:
                    portion_steps.append({"member": member.name, "instruction": f"Cook {member.name}'s portion by pan-cooking or air-frying instead of deep-frying where the recipe texture permits."})

    # Recompute normalized ingredient names after global swaps so the displayed recipe
    # itself reflects what the household should actually buy/cook.
    adapted["normalized_ingredients"] = [clean_text(i.get("name", "")) for i in adapted.get("ingredients", [])]
    adapted["household_portion_steps"] = portion_steps
    adapted["household_adapted"] = bool(global_swaps or portion_steps)
    adapted["household_global_swaps"] = global_swaps
    adapted["household_portion_steps"] = portion_steps
    return adapted

def build_member_adaptations(recipe: Dict[str, Any], members: List[Any]) -> List[Dict[str, Any]]:
    """Return actionable, member-specific adaptations while keeping one shared recipe."""
    output = []
    ingredients = recipe.get("ingredients", [])
    for member in members:
        avoid, required = _rules(member)
        adjustments = []
        # The shared recipe may already contain a global substitution. Keep that
        # explicit in the member explanation instead of losing the original conflict.
        for ing in ingredients:
            if ing.get("household_replaced_from") and member.name in [
                str(x) for swap in recipe.get("household_global_swaps", [])
                if clean_text(swap.get("replacement", "")) == clean_text(ing.get("name", ""))
                for x in swap.get("members", [])
            ]:
                adjustments.append({
                    "type": "ingredient_swap",
                    "original_ingredient": ing.get("household_replaced_from"),
                    "replacement": ing.get("name"),
                    "quantity": ing.get("quantity"),
                    "unit": ing.get("unit", ""),
                    "instruction": f"Use {ing.get('name')} instead of {ing.get('household_replaced_from')} for the shared household recipe.",
                    "reason": "This substitution is applied to the same recipe for everyone."
                })
        # Strict avoided ingredients: prefer a real recipe ingredient substitute; otherwise portion-level omission.
        for avoided in sorted(avoid):
            hits = [ing for ing in ingredients if _ingredient_hit(ing.get("name", ""), avoided)]
            for ing in hits:
                replacement = _find_replacement(ing, member)
                if replacement:
                    adjustments.append({
                        "type": "ingredient_swap",
                        "original_ingredient": ing.get("name"),
                        "replacement": replacement,
                        "quantity": ing.get("quantity"),
                        "unit": ing.get("unit", ""),
                        "instruction": f"Use {replacement} instead of {ing.get('name')} for {member.name}'s portion(s).",
                        "reason": f"Keeps the same shared recipe while respecting {member.name}'s no-{avoided} constraint."
                    })
                else:
                    adjustments.append({
                        "type": "portion_adjustment",
                        "original_ingredient": ing.get("name"),
                        "replacement": "omit from this portion",
                        "quantity": ing.get("quantity"),
                        "unit": ing.get("unit", ""),
                        "instruction": f"Cook the common base without {ing.get('name')}; reserve {member.name}'s portion before adding it to everyone else's portions.",
                        "reason": f"There is no validated substitute stored for {ing.get('name')} in this recipe."
                    })
        # Positive salt request is handled as individual seasoning rather than a second recipe.
        if "salt" in required:
            adjustments.append({
                "type": "portion_adjustment",
                "original_ingredient": "Salt",
                "replacement": "add extra salt only to this portion",
                "quantity": None, "unit": "",
                "instruction": f"Keep the shared base moderately salted, serve {member.name}'s portion, then season that portion separately.",
                "reason": "Salt is easiest to individualize after the shared base is cooked."
            })
        # Spice differences: prepare the shared base mild and add heat per portion.
        spice = clean_text(getattr(member, "spice_tolerance", "medium"))
        if spice in ("mild", "low"):
            chili_hits = [i for i in ingredients if any(x in clean_text(i.get("name", "")) for x in ("chilli", "chili", "pepper"))]
            if chili_hits:
                adjustments.append({
                    "type": "portion_adjustment",
                    "original_ingredient": chili_hits[0].get("name"),
                    "replacement": "use less in shared base",
                    "quantity": chili_hits[0].get("quantity"), "unit": chili_hits[0].get("unit", ""),
                    "instruction": f"Keep the common base mild for {member.name}; add extra chilli only to other individual portions at the table.",
                    "reason": "Spice can be increased after the shared base is divided."
                })
        # Lighter/health-oriented request: give concrete culinary changes tied to ingredients/method.
        if _is_healthy_request(member):
            names = _ingredient_names(recipe)
            fats = [i for i in ingredients if any(x in clean_text(i.get("name", "")) for x in ("ghee", "butter", "oil"))]
            if fats:
                adjustments.append({
                    "type": "lighter_method",
                    "original_ingredient": fats[0].get("name"),
                    "replacement": "use the minimum amount needed for the same cooking step",
                    "quantity": fats[0].get("quantity"), "unit": fats[0].get("unit", ""),
                    "instruction": f"For {member.name}, measure the cooking fat instead of free-pouring it; use the pan's non-stick surface or a splash of water where the recipe allows.",
                    "reason": "Reduces added fat without making a second dish."
                })
            if any(x in " ".join(names) for x in ("sugar", "jaggery", "date")):
                adjustments.append({
                    "type": "lighter_method",
                    "original_ingredient": "added sweetener",
                    "replacement": "reduce the sweetener in this portion",
                    "quantity": None, "unit": "",
                    "instruction": f"Prepare the shared recipe with less added sweetener, then keep {member.name}'s portion unsweetened if desired.",
                    "reason": "Sweetness can be adjusted at the end for a shared preparation."
                })
            fried_words = recipe.get("title", "").lower()
            if any(x in fried_words for x in ("fried", "fritter", "pakora", "vada", "tikki", "cutlet", "bhakarwadi", "shankarpali")):
                adjustments.append({
                    "type": "lighter_method",
                    "original_ingredient": "frying method",
                    "replacement": "pan-cook / air-fry instead of deep-fry where practical",
                    "quantity": None, "unit": "",
                    "instruction": f"Cook {member.name}'s portion by pan-cooking or air-frying until crisp rather than deep-frying, if the recipe texture permits.",
                    "reason": "This is a cooking-method adjustment, not a separate recipe."
                })
        if adjustments:
            output.append({"member_id": member.id, "member_name": member.name, "adjustments": adjustments})
    return output

def build_household_customization_tip(recipe: Dict[str, Any], members: List[Any], adaptations: List[Dict[str, Any]]) -> str:
    global_swaps = recipe.get("household_global_swaps", [])
    portion_steps = recipe.get("household_portion_steps", [])
    if global_swaps or portion_steps or adaptations:
        return "Cook this single adapted recipe once for the household. Shared ingredient substitutions are already built into the recipe; only the listed finishing/portion steps vary by member. No second recipe is needed."
    return "Cook this single recipe once as written. If members differ only in salt or spice, divide portions at the end and season individually."
