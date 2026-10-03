"""Explainable ONE HOUSEHOLD -> ONE COMMON MEAL ranking engine."""
from typing import List, Dict, Any, Set, Tuple, Optional
from backend.models.household import HouseholdMember, HouseholdQuery, HouseholdMealResult, MemberMatchExplanation, HouseholdSolveResponse
from backend.core.pantry_matcher import expand_user_pantry, is_ingredient_available
from backend.core.ir_engine import clean_text
from backend.core.recipe_adaptations import build_member_adaptations, build_household_customization_tip, build_household_recipe_plan, _find_replacement, _ingredient_hit

SPICE_TOLERANCE_MAP = {"mild": 1, "low": 2, "medium": 3, "spicy": 5}
STRICT_DIETS = {"vegan", "jain", "gluten-free", "vegetarian"}


def _normalize_display_quantity(quantity: float, unit: str):
    """Convert large metric amounts to kitchen-friendly units after scaling."""
    u = (unit or "").strip().lower()
    if u in {"g", "gram", "grams"} and quantity >= 1000:
        return round(quantity / 1000, 2), "kg"
    if u in {"ml", "millilitre", "millilitres", "milliliter", "milliliters"} and quantity >= 1000:
        return round(quantity / 1000, 2), "litre"
    return quantity, unit


def format_scaled_qty(qty: float) -> str:
    """Format scaled amounts as readable kitchen measurements (e.g. 1/2, 2 1/2)."""
    if qty is None or qty <= 0:
        return ""
    if abs(qty - round(qty)) < 0.03:
        return str(int(round(qty)))
    # Common kitchen fractions.  Use a small tolerance because source quantities
    # are often decimal values such as 0.499 or 1.249 after scaling.
    fractions = ((1/4, "1/4"), (1/3, "1/3"), (1/2, "1/2"), (2/3, "2/3"), (3/4, "3/4"))
    whole = int(qty)
    frac = qty - whole
    for value, text in fractions:
        if abs(frac - value) < 0.04:
            return f"{whole} {text}".strip() if whole else text
    return f"{qty:.2f}".rstrip("0").rstrip(".")


class HouseholdSolver:
    def __init__(self, recipes: List[Dict[str, Any]]): self.recipes = recipes

    def solve(self, query: HouseholdQuery) -> HouseholdSolveResponse:
        members = query.members
        servings = query.servings or len(members)
        pantry = expand_user_pantry(query.available_ingredients) if query.available_ingredients else set()
        strict_diet = self._aggregate_strict_diet(members)
        forbidden = self._aggregate_avoided(members)
        min_spice = min(SPICE_TOLERANCE_MAP.get(m.spice_tolerance.lower(), 3) for m in members)
        results = []

        for recipe in self.recipes:
            household_recipe = build_household_recipe_plan(recipe, members)
            adaptations = build_member_adaptations(household_recipe, members)
            hard_ok, strict_ok, strict_failed = self._strict_check(household_recipe, members, strict_diet, forbidden, query)
            # A strict ingredient conflict is considered solvable when this recipe has a stored,
            # diet-compatible substitution or a safe portion-level adjustment. That keeps ONE recipe
            # for the household rather than forcing separate meals.
            member_explanations, member_scores = [], []
            pref_hits = []
            for m in members:
                score, satisfied, tips = self._member_score(m, household_recipe, min_spice)
                member_scores.append(score)
                pref_hits.extend([x for x in satisfied if not x.startswith("✓") or True])
                member_adaptation = next((a for a in adaptations if a["member_id"] == m.id), None)
                if member_adaptation:
                    for adj in member_adaptation["adjustments"][:3]:
                        tips.append(adj["instruction"])
                member_explanations.append(MemberMatchExplanation(
                    member_id=m.id, member_name=m.name, role=m.role,
                    is_fully_satisfied=hard_ok and score >= 85,
                    satisfaction_score=int(round(score)),
                    satisfied_aspects=satisfied, compromises_or_tips=tips))
            matched, missing, pantry_pct, missing_details = self._pantry(household_recipe, pantry, servings)
            harmony = sum(member_scores) / len(member_scores)
            ingredient_score = pantry_pct / 100 if pantry else 1.0
            preference_score = min(1.0, max(0.0, harmony / 100))
            time_score = 1.0 if not query.max_time_mins else max(0.0, 1 - max(0, recipe.get("total_time_mins", 0) - query.max_time_mins) / max(query.max_time_mins, 1))
            onepot_score = 1.0 if not query.one_pot else (1.0 if recipe.get("is_one_pot") else 0.0)
            # Strict satisfaction is dominant; failed strict candidates are capped below fully compliant candidates.
            strict_score = 1.0 if hard_ok else 0.0
            score = (0.55 * strict_score + 0.18 * ingredient_score + 0.12 * preference_score + 0.08 * time_score + 0.07 * onepot_score)
            if not hard_ok: score *= 0.55
            score = round(score, 3)
            strict_satisfied = self._strict_satisfied_labels(household_recipe, members, strict_diet, forbidden, query)
            preference_satisfied = self._preference_labels(household_recipe, members, query)
            perfect = hard_ok and harmony >= 85 and (not pantry or pantry_pct >= 75)
            verdict = "One shared adapted recipe satisfies the household" if perfect else ("Best common meal found" if hard_ok else "Closest common meal — a constraint cannot be safely adapted")
            explanation = self._explain(household_recipe, members, matched, missing, strict_satisfied, strict_failed)
            results.append(HouseholdMealResult(
                recipe=household_recipe, household_score=score, household_harmony_percentage=int(round(harmony)),
                is_perfect_shared_meal=perfect, summary_verdict=verdict, explanation=explanation,
                strict_constraints_satisfied=strict_satisfied, strict_constraints_failed=strict_failed,
                preferences_satisfied=preference_satisfied, member_explanations=member_explanations,
                family_customization_tip=build_household_customization_tip(household_recipe, members, adaptations),
                member_adaptations=adaptations, pantry_match_percentage=pantry_pct,
                matched_ingredients=matched, missing_ingredients=missing, missing_ingredient_details=missing_details,
                scaled_ingredients=self._scale(household_recipe, servings), total_household_servings=servings,
                total_time_mins=household_recipe.get("total_time_mins", 30), one_pot=bool(household_recipe.get("is_one_pot")),
                dietary_badges=self._badges(household_recipe), taste_profile=household_recipe.get("flavor_profile", {})))

        results.sort(key=lambda r: (-int(r.is_perfect_shared_meal), -r.household_score, -r.household_harmony_percentage, len(r.missing_ingredients), r.total_time_mins))
        perfect = [r for r in results if r.is_perfect_shared_meal]
        best = (perfect or results)[0] if results else None
        no_perfect = bool(best and not best.is_perfect_shared_meal)
        conflict = "No single meal satisfies every requirement." if no_perfect else None
        adjustment = None
        if no_perfect and best:
            adjustment = best.strict_constraints_failed[0] if best.strict_constraints_failed else (f"Add: {best.missing_ingredients[0]}" if best.missing_ingredients else "Relax one optional preference")
        return HouseholdSolveResponse(
            total_members=len(members), total_servings=servings, best_shared_meal=best,
            runner_up_meals=results[1:5], no_perfect_match=no_perfect, conflict_message=conflict,
            smallest_adjustment=adjustment,
            household_summary={
                "members_count": len(members),
                "strict_constraints_count": sum(1 for m in members for _ in m.avoid_ingredients) + len([m for m in members if m.diet.lower() in STRICT_DIETS]),
                "preferences_count": sum(len(m.preferences) + len(m.strict_preferences) for m in members),
                "ingredients_available": len(query.available_ingredients),
                "household_type": query.household_type,
                "one_pot_requested": query.one_pot,
                "candidate_meals_evaluated": len(results)
            })

    def _member_restriction_rules(self, member):
        import re
        raw = list(getattr(member, "avoid_ingredients", []) or [])
        custom = getattr(member, "custom_preference", None)
        if custom:
            raw.extend(re.split(r"[,;]+", custom))
        avoid, required = [], []
        for item in raw:
            n = clean_text(item)
            if not n: continue
            m = re.match(r"^(?:no|without|free from)\s+(.+)$", n)
            if m:
                avoid.append(m.group(1).strip()); continue
            if re.match(r"^(?:high|extra|more)\s+salt$", n):
                required.append("salt"); continue
            avoid.append(n)
        return set(avoid), set(required)

    def _ingredient_present(self, recipe, target):
        t = clean_text(target)
        if not t: return False
        for ing in recipe.get("ingredients", []):
            n = clean_text(ing.get("name", ""))
            if t == n or f" {t} " in f" {n} " or (t == "peanut" and "peanut" in n):
                return True
        return False

    def _aggregate_strict_diet(self, members):
        diets = [m.diet.lower().strip() for m in members]
        if "jain" in diets: return "jain"
        if "vegan" in diets: return "vegan"
        if "gluten-free" in diets: return "gluten-free"
        if "vegetarian" in diets: return "vegetarian"
        return None

    def _aggregate_avoided(self, members):
        out=set()
        for m in members:
            avoid,_=self._member_restriction_rules(m)
            out.update(avoid)
        return out

    def _strict_check(self, r, members, diet, forbidden, q):
        failed=[]
        if diet == "vegan" and not r.get("is_vegan"): failed.append("At least one member requires vegan food")
        elif diet == "jain" and not r.get("is_jain"): failed.append("At least one member requires Jain-compatible food")
        elif diet == "gluten-free" and not r.get("is_gluten_free"): failed.append("At least one member requires gluten-free food")
        elif diet == "vegetarian" and r.get("diet") not in ("Vegetarian", "Vegan"): failed.append("At least one member requires vegetarian food")
        names = " ".join(r.get("normalized_ingredients", []))
        for f in forbidden:
            for ing in r.get("ingredients", []):
                if not ing.get("is_optional", False) and _ingredient_hit(ing.get("name", ""), f):
                    # If every hit can be replaced for the affected member, the shared recipe remains viable.
                    affected = [m for m in members if f in self._member_restriction_rules(m)[0]]
                    if not affected or not all(_find_replacement(ing, m) for m in affected):
                        failed.append(f"Avoided ingredient: {f}")
                    break
        for m in members:
            avoid, required = self._member_restriction_rules(m)
            for f in avoid:
                hits = [i for i in r.get("ingredients", []) if _ingredient_hit(i.get("name", ""), f)]
                for ing in hits:
                    if not ing.get("is_optional", False) and not _find_replacement(ing, m):
                        failed.append(f"{m.name}: avoids {f}")
            for req in required:
                if not self._ingredient_present(r, req): failed.append(f"{m.name}: requires {req}")
        if q.max_time_mins and r.get("total_time_mins", 0) > q.max_time_mins: failed.append(f"Cooking time exceeds {q.max_time_mins} minutes")
        if q.meal_type and q.meal_type.lower() != "all" and q.meal_type.lower() not in [x.lower() for x in r.get("meal_type", [])] and q.meal_type.lower() != r.get("course", "").lower(): failed.append(f"Meal type does not match {q.meal_type}")
        if q.cuisine and q.cuisine.lower() != "all" and q.cuisine.lower() not in r.get("regional_cuisine", "").lower(): failed.append(f"Cuisine preference does not match {q.cuisine}")
        for m in members:
            if any(clean_text(x) in ("healthy", "healthier", "wholesome", "balanced") for x in (m.strict_preferences or [])) and not r.get("is_light"):
                failed.append(f"{m.name}: healthy/balanced preference cannot be adapted for this recipe")
        return not failed, [], failed

    def _member_score(self, m, r, min_spice):
        score=100.0; good=[]; tips=[]
        spice=SPICE_TOLERANCE_MAP.get(m.spice_tolerance.lower(),3); rs=r.get("flavor_profile",{}).get("spicy",2)
        if rs <= spice: good.append(f"✓ Fits {m.spice_tolerance} spice preference")
        else: score -= 20 if rs == spice+1 else 35; tips.append(f"Reduce chilli/spice for {m.name}")
        avoid, required = self._member_restriction_rules(m)
        for item in sorted(avoid):
            if item == "dairy":
                hit = any(x in clean_text(i.get("name", "")) for i in r.get("ingredients", []) for x in ("milk","curd","yogurt","paneer","ghee","butter","cream","cheese"))
            else:
                hit = self._ingredient_present(r, item)
            if hit:
                # A recipe-level substitution keeps the household on ONE dish when a safe replacement exists.
                hit_ings = [i for i in r.get("ingredients", []) if _ingredient_hit(i.get("name", ""), item)]
                replacements = [_find_replacement(i, m) for i in hit_ings if _find_replacement(i, m)]
                if replacements:
                    good.append(f"✓ {item} adapted to {replacements[0]}")
                    tips.append(f"Use {replacements[0]} instead of {item} for {m.name}")
                else:
                    score -= 40
                    tips.append(f"Constraint conflict: {m.name} avoids {item}")
            else:
                good.append(f"✓ No {item}")
        for item in sorted(required):
            if self._ingredient_present(r, item):
                good.append(f"✓ Contains required {item}")
            else:
                score -= 35
                tips.append(f"Constraint conflict: {m.name} requires {item}")
        for p in m.preferences + m.strict_preferences:
            pl=p.lower()
            ok = ((pl in ("soft_food","soft","elder_friendly") and (r.get("texture")=="soft" or r.get("is_elder_friendly"))) or
                  (pl in ("kid_friendly","kids") and r.get("is_kid_friendly")) or
                  (pl in ("high_protein","protein") and r.get("is_high_protein")) or
                  (pl in ("easy_digest","light") and r.get("is_easy_digest")) or
                  (pl=="one_pot" and r.get("is_one_pot")) or
                  (pl=="quick" and r.get("total_time_mins",99)<=30) or
                  (pl in r.get("regional_cuisine", "").lower()))
            if ok: good.append(f"✓ {p.replace('_',' ').title()}"); score += 4
            elif pl in m.strict_preferences: score -= 35; tips.append(f"Strict preference not met: {p.replace('_',' ')}")
            else: score -= 5
        # "healthy/wholesome" is treated as a culinary preference, not a medical claim.
        custom = clean_text(getattr(m, "custom_preference", "") or "")
        healthy_requested = any(cue in custom for cue in ("healthy", "healthier", "wholesome", "balanced", "low oil", "less oil", "low salt", "less salt", "low sugar", "less sugar")) or any(clean_text(x) in ("healthy", "wholesome", "balanced") for x in m.preferences + m.strict_preferences)
        if healthy_requested:
            if r.get("is_light"):
                good.append("✓ Lighter / balanced profile")
            else:
                score -= 8
                tips.append(f"Use the recipe's lighter adaptation for {m.name}")
        return max(0,min(100,score)), good, tips

    def _strict_satisfied_labels(self,r,members,diet,forbidden,q):
        labels=[]
        if diet: labels.append(f"{diet.title()} for all applicable members")
        for f in forbidden:
            if not any(f in clean_text(i.get("name","")) and not i.get("is_optional",False) for i in r.get("ingredients",[])): labels.append(f"No avoided {f}")
        if q.max_time_mins and r.get("total_time_mins",0)<=q.max_time_mins: labels.append("Within cooking-time limit")
        return labels

    def _preference_labels(self,r,members,q):
        out=[]
        if q.one_pot and r.get("is_one_pot"): out.append("One-pot")
        for p in {x for m in members for x in m.preferences}:
            pl=p.lower()
            if (pl=="quick" and r.get("total_time_mins",99)<=30) or (pl=="high_protein" and r.get("is_high_protein")) or (pl=="kid_friendly" and r.get("is_kid_friendly")) or (pl in ("soft_food","easy_digest") and (r.get("texture")=="soft" or r.get("is_elder_friendly") or r.get("is_easy_digest"))): out.append(p.replace('_',' ').title())
        return out

    def _pantry(self,r,pantry,servings):
        if not pantry: return [], [], 100, []
        matched=[]; missing=[]; details=[]; total=0; hit=0
        factor=servings / max(1, r.get("nutrition_per_serving",{}).get("servings",2))
        for ing in r.get("ingredients",[]):
            if ing.get("is_optional"): continue
            total+=1
            if is_ingredient_available(ing.get("name",""),pantry): matched.append(ing.get("name")); hit+=1
            else:
                missing.append(ing.get("name")); details.append({"name":ing.get("name"),"quantity":round(ing.get("quantity",1)*factor,2),"unit":ing.get("unit","")})
        return matched,missing,int(round(hit/max(total,1)*100)),details

    def _scale(self, r, servings):
        """Scale every recipe ingredient from its base serving count to the household size."""
        base = max(1, r.get("base_servings", r.get("nutrition_per_serving", {}).get("servings", 2)))
        factor = servings / base
        out = []
        for ingredient in r.get("ingredients", []):
            original_quantity = float(ingredient.get("quantity", 1))
            scaled_quantity = round(original_quantity * factor, 2)
            display_quantity, display_unit = _normalize_display_quantity(
                scaled_quantity, ingredient.get("unit", "")
            )
            out.append({
                "name": ingredient.get("name"),
                "quantity": scaled_quantity,
                "display_quantity": format_scaled_qty(display_quantity),
                "unit": display_unit,
                "measurement": f"{format_scaled_qty(display_quantity)} {display_unit}".strip(),
                "base_quantity": original_quantity,
                "base_unit": ingredient.get("unit", ""),
                "is_optional": ingredient.get("is_optional", False),
                "category": ingredient.get("category", "general"),
                "substitutes": ingredient.get("substitutes", []),
                "household_replaced_from": ingredient.get("household_replaced_from"),
                "household_replacement": ingredient.get("household_replacement")
            })
        return out

    def _badges(self,r):
        out=[r.get("diet","Vegetarian")]
        for key,label in (("is_vegan","Vegan"),("is_jain","Jain"),("is_gluten_free","Gluten-Free"),("is_one_pot","One-Pot"),("is_kid_friendly","Kid-Friendly"),("is_elder_friendly","Elder-Friendly"),("is_high_protein","High-Protein")):
            if r.get(key): out.append(label)
        return out

    def _custom_tip(self,members,r):
        # Only mention ingredients/adjustments that are actually represented in the recipe.
        ingredient_names=[clean_text(i.get("name","")) for i in r.get("ingredients",[])]
        ingredient_text=" ".join(ingredient_names)
        mild=[m.name for m in members if SPICE_TOLERANCE_MAP.get(m.spice_tolerance.lower(),3)<=2]
        spicy=[m.name for m in members if SPICE_TOLERANCE_MAP.get(m.spice_tolerance.lower(),3)>=4]
        if mild and spicy and any(x in ingredient_text for x in ("chilli","green chilli","red chilli")):
            return f"Keep the chilli level within the recipe amount for {', '.join(mild)}; add extra chilli only to an individual portion for {', '.join(spicy)}."
        if r.get("is_one_pot"):
            return "Serve the same prepared dish to everyone; any adjustment should use ingredients already listed in this recipe."
        return "Follow the listed ingredients and quantities for this recipe; do not add unlisted ingredients unless you intentionally substitute one."

    def _explain(self,r,members,matched,missing,satisfied,failed):
        bits=[]
        if satisfied: bits.extend(satisfied[:3])
        if matched: bits.append(f"Uses {len(matched)} available ingredients")
        if r.get("is_one_pot"): bits.append("One-pot preparation")
        if missing: bits.append(f"Still needed: {', '.join(missing[:3])}")
        if failed: bits.append(f"Constraint to adjust: {failed[0]}")
        return ". ".join(bits) + "."
