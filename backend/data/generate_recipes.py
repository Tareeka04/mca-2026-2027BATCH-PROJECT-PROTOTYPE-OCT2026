"""
Comprehensive Indian Recipe Dataset Generator.
Generates 100+ highly authentic, culturally accurate recipes with strong Maharashtrian representation.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = DATA_DIR / "recipes.json"
import sys
sys.path.insert(0, str(DATA_DIR))
from recipe_step_builder import build_generated_steps

RECIPES = [
    # 1. Kanda Poha
    {
        "id": "rec_kanda_poha",
        "title": "Kanda Poha (Maharashtrian Tempered Flattened Rice)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Breakfast", "Snack", "Quick Meal"],
        "course": "Breakfast",
        "prep_time_mins": 10,
        "cook_time_mins": 12,
        "total_time_mins": 22,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 2, "tangy": 3, "sweet": 1, "savory": 4, "comfort": 5},
        "mood_tags": ["quick", "light", "comforting", "classic", "monsoon", "tea-time"],
        "ingredients": [
            {"name": "Poha (Thick Flattened Rice)", "quantity": 2.0, "unit": "cups", "is_optional": False, "category": "grains", "substitutes": ["Rolled Oats"]},
            {"name": "Onion (Kanda)", "quantity": 1.0, "unit": "large, finely chopped", "is_optional": False, "category": "vegetables", "substitutes": ["Spring Onion"]},
            {"name": "Peanuts (Shengdana)", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "nuts", "substitutes": ["Cashews"]},
            {"name": "Green Chillies", "quantity": 2.0, "unit": "slit", "is_optional": False, "category": "spices", "substitutes": ["Red chilli powder"]},
            {"name": "Mustard Seeds (Rai)", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": ["Cumin seeds"]},
            {"name": "Turmeric Powder (Haldi)", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Curry Leaves (Kadi Patta)", "quantity": 8.0, "unit": "leaves", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Oil", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": ["Ghee"]},
            {"name": "Salt", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Sugar", "quantity": 0.5, "unit": "tsp", "is_optional": True, "category": "sweetener", "substitutes": ["Jaggery"]},
            {"name": "Fresh Coriander (Kothimbir)", "quantity": 2.0, "unit": "tbsp chopped", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Fresh Grated Coconut", "quantity": 2.0, "unit": "tbsp", "is_optional": True, "category": "garnish", "substitutes": ["Desiccated coconut"]},
            {"name": "Lemon Juice", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "seasoning", "substitutes": ["Amchur"]}
        ],
        "normalized_ingredients": ["poha", "onion", "peanut", "green chilli", "mustard seed", "turmeric", "curry leaf", "oil", "salt", "sugar", "coriander", "fresh coconut", "lemon juice"],
        "leftover_ingredients_used": [],
        "steps": [
            {"step_number": 1, "title": "Rinse Poha", "instruction": "Rinse thick poha in a strainer under cold water for 30 seconds. Drain, toss with 1/2 tsp salt and sugar, and let rest.", "duration_mins": 5, "tip": "Do not soak poha in a bowl or it will become mushy."},
            {"step_number": 2, "title": "Fry Peanuts & Phodni", "instruction": "Heat oil in kadai. Fry peanuts till crunchy and remove. In same oil, splutter mustard seeds, green chillies, and curry leaves.", "duration_mins": 4, "tip": "Frying peanuts first preserves their crispness."},
            {"step_number": 3, "title": "Sauté Onions", "instruction": "Add chopped onions and sauté until translucent and soft. Stir in turmeric powder.", "duration_mins": 4, "tip": "Do not brown the onions; they should stay soft and sweet."},
            {"step_number": 4, "title": "Combine & Steam", "instruction": "Add the softened poha and fried peanuts. Toss gently. Sprinkle 1 tbsp water, cover with lid, and steam on low for 2 mins.", "duration_mins": 4, "tip": "Use a light folding motion."},
            {"step_number": 5, "title": "Garnish & Serve", "instruction": "Turn off flame, drizzle lemon juice, and garnish with fresh coriander and grated coconut.", "duration_mins": 1, "tip": "Serve steaming hot with Masala Chai."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 280, "protein_g": 6.2, "carbs_g": 47.0, "fat_g": 8.0, "fiber_g": 3.5},
        "equipment": ["Colander / Strainer", "Kadai", "Lid"],
        "summary": "Fluffy tempered flattened rice tossed with golden onions, crisp peanuts, mustard, curry leaves, and lemon."
    },
    # 2. Phodnichi Poli
    {
        "id": "rec_phodnichi_poli",
        "title": "Phodnichi Poli (Maharashtrian Spiced Leftover Chapati)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Breakfast", "Snack", "Dinner", "Quick Meal"],
        "course": "Snack",
        "prep_time_mins": 5,
        "cook_time_mins": 8,
        "total_time_mins": 13,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": False,
        "flavor_profile": {"spicy": 3, "tangy": 3, "sweet": 1, "savory": 4, "comfort": 5},
        "mood_tags": ["quick", "comforting", "zero-waste", "nostalgic", "tea-time"],
        "ingredients": [
            {"name": "Leftover Stale Chapati (Poli)", "quantity": 4.0, "unit": "rotis, torn into small pieces", "is_optional": False, "category": "grains", "substitutes": ["Leftover Paratha", "Tortillas"]},
            {"name": "Onion", "quantity": 1.0, "unit": "medium, chopped", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Green Chillies", "quantity": 2.0, "unit": "chopped", "is_optional": False, "category": "spices", "substitutes": ["Red chilli powder"]},
            {"name": "Mustard Seeds (Rai)", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Cumin Seeds (Jeera)", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Turmeric Powder", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Peanuts", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "nuts", "substitutes": ["Cashews"]},
            {"name": "Curry Leaves", "quantity": 6.0, "unit": "leaves", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Oil", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": ["Ghee"]},
            {"name": "Salt", "quantity": 0.75, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Lemon Juice", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Fresh Coriander", "quantity": 2.0, "unit": "tbsp chopped", "is_optional": False, "category": "herbs", "substitutes": []}
        ],
        "normalized_ingredients": ["chapati", "roti", "poli", "onion", "green chilli", "mustard seed", "cumin seed", "turmeric", "peanut", "curry leaf", "oil", "salt", "lemon juice", "coriander"],
        "leftover_ingredients_used": ["stale roti", "chapati", "poli"],
        "steps": [
            {"step_number": 1, "title": "Tear Chapatis", "instruction": "Tear stale chapatis into small bite-sized pieces. Sprinkle 2 tbsp of water over them to soften slightly.", "duration_mins": 3, "tip": "Sprinkling water prevents the stale roti from turning rock hard during cooking."},
            {"step_number": 2, "title": "Prepare Phodni", "instruction": "Heat oil in kadai. Fry peanuts until crispy. Add mustard, cumin, curry leaves, and green chillies.", "duration_mins": 3, "tip": "Let mustard crackle completely."},
            {"step_number": 3, "title": "Sauté Onion & Turmeric", "instruction": "Add chopped onions and sauté until pink. Add turmeric and salt.", "duration_mins": 3, "tip": "Remember chapati already has some salt, so add salt moderately."},
            {"step_number": 4, "title": "Toss and Steam", "instruction": "Add torn chapati pieces, toss thoroughly, cover with lid and steam on low flame for 3 minutes.", "duration_mins": 3, "tip": "Steaming makes the chapatis delightfully soft and chewy."},
            {"step_number": 5, "title": "Finish", "instruction": "Squeeze fresh lemon juice and garnish with coriander.", "duration_mins": 1, "tip": "The ultimate quick comfort breakfast from leftovers."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 260, "protein_g": 5.8, "carbs_g": 38.0, "fat_g": 9.5, "fiber_g": 4.2},
        "equipment": ["Kadai", "Lid", "Spatula"],
        "summary": "Classic Maharashtrian breakfast transforming stale rotis into a flavorful, soft and tangy spiced hash with peanuts and curry leaves."
    },
    # 3. Phodnicha Bhaat
    {
        "id": "rec_phodnicha_bhaat",
        "title": "Phodnicha Bhaat (Maharashtrian Tempered Leftover Rice)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Breakfast", "Lunch", "Dinner", "Quick Meal"],
        "course": "Main Course",
        "prep_time_mins": 3,
        "cook_time_mins": 7,
        "total_time_mins": 10,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 2, "tangy": 2, "sweet": 0, "savory": 4, "comfort": 5},
        "mood_tags": ["quick", "comforting", "zero-waste", "nostalgic"],
        "ingredients": [
            {"name": "Cooked Rice (Bhaat)", "quantity": 3.0, "unit": "cups, cooled / leftover", "is_optional": False, "category": "grains", "substitutes": ["Fresh steamed rice"]},
            {"name": "Onion", "quantity": 1.0, "unit": "medium, sliced", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Mustard Seeds (Rai)", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Cumin Seeds (Jeera)", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Hing (Asafoetida)", "quantity": 1.0, "unit": "pinch", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Turmeric Powder", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Green Chillies", "quantity": 2.0, "unit": "slit", "is_optional": False, "category": "spices", "substitutes": ["Red chilli powder"]},
            {"name": "Curry Leaves", "quantity": 8.0, "unit": "leaves", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Peanuts", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "nuts", "substitutes": []},
            {"name": "Oil or Ghee", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": []},
            {"name": "Salt", "quantity": 0.75, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Fresh Coriander", "quantity": 2.0, "unit": "tbsp chopped", "is_optional": False, "category": "herbs", "substitutes": []}
        ],
        "normalized_ingredients": ["cooked rice", "bhaat", "rice", "onion", "mustard seed", "cumin seed", "hing", "turmeric", "green chilli", "curry leaf", "peanut", "oil", "ghee", "salt", "coriander"],
        "leftover_ingredients_used": ["cooked rice", "rice", "bhaat"],
        "steps": [
            {"step_number": 1, "title": "Fluff Rice", "instruction": "Gently break lumps in cold leftover rice using clean wet fingers.", "duration_mins": 2, "tip": "Cold refrigerated rice stays intact without becoming sticky."},
            {"step_number": 2, "title": "Tempering (Phodni)", "instruction": "Heat oil/ghee in pan. Fry peanuts till golden. Add mustard, cumin, hing, green chillies, and curry leaves.", "duration_mins": 3, "tip": "Hing in ghee gives the signature traditional aroma."},
            {"step_number": 3, "title": "Sauté Onion & Spices", "instruction": "Add sliced onions and sauté till light golden. Add turmeric and salt.", "duration_mins": 2, "tip": "Golden onions give slight sweetness."},
            {"step_number": 4, "title": "Toss and Heat Through", "instruction": "Add cold rice, mix well with tempering, cover and steam for 2-3 mins on low flame. Garnish with coriander.", "duration_mins": 3, "tip": "Serve warm with curd or roasted papad."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 290, "protein_g": 5.0, "carbs_g": 49.0, "fat_g": 8.5, "fiber_g": 2.5},
        "equipment": ["Pan", "Lid", "Spatula"],
        "summary": "Crispy tempered aromatic rice seasoned with mustard, turmeric, peanuts, and golden onions."
    },
    # 4. Bharli Vangi
    {
        "id": "rec_bharli_vangi",
        "title": "Bharli Vangi (Maharashtrian Stuffed Baby Eggplants in Peanut Coconut Gravy)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Lunch", "Dinner"],
        "course": "Main Course",
        "prep_time_mins": 15,
        "cook_time_mins": 25,
        "total_time_mins": 40,
        "difficulty": "Medium",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 4, "tangy": 3, "sweet": 2, "savory": 5, "comfort": 5},
        "mood_tags": ["indulgent", "rich", "traditional", "festive", "comforting"],
        "ingredients": [
            {"name": "Baby Brinjals / Eggplants (Vangi)", "quantity": 8.0, "unit": "small purple brinjals", "is_optional": False, "category": "vegetables", "substitutes": ["Baby Potatoes (Bharli Batata)"]},
            {"name": "Roasted Peanuts Powder", "quantity": 0.5, "unit": "cup", "is_optional": False, "category": "nuts", "substitutes": ["Cashew powder"]},
            {"name": "Dry Grated Coconut (Khobra)", "quantity": 0.25, "unit": "cup, roasted", "is_optional": False, "category": "garnish", "substitutes": ["Fresh grated coconut"]},
            {"name": "Goda Masala (or Kala Masala)", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "spices", "substitutes": ["Garam Masala + coriander powder"]},
            {"name": "Kashmiri Red Chilli Powder", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Turmeric Powder", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Ginger-Garlic Paste", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Jaggery (Gul)", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "sweetener", "substitutes": ["Brown sugar"]},
            {"name": "Tamarind Paste (or Kokum)", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": ["Amchur", "Kokum"]},
            {"name": "Oil", "quantity": 3.0, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": []},
            {"name": "Mustard and Cumin Seeds", "quantity": 1.0, "unit": "tsp combined", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Curry Leaves", "quantity": 6.0, "unit": "leaves", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Salt", "quantity": 1.25, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Fresh Coriander", "quantity": 2.0, "unit": "tbsp chopped", "is_optional": False, "category": "herbs", "substitutes": []}
        ],
        "normalized_ingredients": ["brinjal", "eggplant", "vangi", "peanut", "coconut", "goda masala", "kala masala", "red chilli powder", "turmeric", "ginger", "garlic", "jaggery", "tamarind", "oil", "mustard seed", "cumin seed", "curry leaf", "salt", "coriander"],
        "leftover_ingredients_used": [],
        "steps": [
            {"step_number": 1, "title": "Slit Brinjals", "instruction": "Slit baby brinjals in a '+' cross shape keeping the stem intact. Place in salted water to prevent blackening.", "duration_mins": 5, "tip": "Keeping the crown stem makes them look royal."},
            {"step_number": 2, "title": "Make Stuffing Masala", "instruction": "In a bowl, mix roasted peanut powder, toasted dry coconut, goda masala, red chilli powder, turmeric, ginger-garlic paste, jaggery, tamarind, salt, and 1 tbsp oil.", "duration_mins": 5, "tip": "Taste the dry masala; it should be robust, nutty, spicy, and mildly sweet."},
            {"step_number": 3, "title": "Stuff Brinjals", "instruction": "Generously stuff each brinjal with the peanut masala. Reserve leftover masala for gravy.", "duration_mins": 5, "tip": "Pack it tightly into the slit crevices."},
            {"step_number": 4, "title": "Cook Gravy", "instruction": "Heat 2 tbsp oil in a heavy pan. Splutter mustard, cumin, and curry leaves. Place stuffed brinjals gently, cover and sear for 5 mins.", "duration_mins": 10, "tip": "Searing the skins brings out a wonderful roasted aroma."},
            {"step_number": 5, "title": "Simmer to Perfection", "instruction": "Add the remaining stuffing masala and 1 cup warm water. Cover and simmer on low flame for 15 minutes until brinjals are melt-in-the-mouth tender and oil separates on top. Garnish with coriander.", "duration_mins": 15, "tip": "Serve with hot Jowar Bhakri or Poli."}
        ],
        "nutrition_per_serving": {"servings": 3, "calories": 340, "protein_g": 8.0, "carbs_g": 24.0, "fat_g": 24.0, "fiber_g": 7.5},
        "equipment": ["Mixing Bowl", "Kadai or Heavy Bottomed Pan", "Lid"],
        "summary": "Royal Maharashtrian curry of tender baby brinjals stuffed with a nutty roasted peanut, toasted coconut, and aromatic Goda Masala spice paste."
    },
    # 5. Pithla Bhakri
    {
        "id": "rec_pithla_bhakri",
        "title": "Maharashtrian Pithla (Comforting Spiced Besan Curry)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Lunch", "Dinner", "Quick Meal"],
        "course": "Main Course",
        "prep_time_mins": 5,
        "cook_time_mins": 12,
        "total_time_mins": 17,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 4, "tangy": 1, "sweet": 0, "savory": 5, "comfort": 5},
        "mood_tags": ["quick", "comforting", "traditional", "rustic", "monsoon"],
        "ingredients": [
            {"name": "Besan (Gram Flour)", "quantity": 0.75, "unit": "cup", "is_optional": False, "category": "flour", "substitutes": ["Sattu"]},
            {"name": "Water", "quantity": 2.0, "unit": "cups", "is_optional": False, "category": "liquids", "substitutes": ["Buttermilk (Taak Pithla)"]},
            {"name": "Onion", "quantity": 1.0, "unit": "large, sliced", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Garlic (Lasun)", "quantity": 6.0, "unit": "cloves, crushed", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Green Chillies", "quantity": 3.0, "unit": "coarsely crushed / sliced", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Mustard Seeds", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Cumin Seeds", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Hing (Asafoetida)", "quantity": 1.0, "unit": "pinch", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Turmeric Powder", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Curry Leaves", "quantity": 8.0, "unit": "leaves", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Oil", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": []},
            {"name": "Salt", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Fresh Coriander", "quantity": 2.0, "unit": "tbsp chopped", "is_optional": False, "category": "herbs", "substitutes": []}
        ],
        "normalized_ingredients": ["besan", "gram flour", "onion", "garlic", "lasun", "green chilli", "mustard seed", "cumin seed", "hing", "turmeric", "curry leaf", "oil", "salt", "coriander"],
        "leftover_ingredients_used": [],
        "steps": [
            {"step_number": 1, "title": "Whisk Besan Slurry", "instruction": "Whisk besan with 2 cups water, salt, and turmeric in a bowl until completely lump-free.", "duration_mins": 3, "tip": "Ensure zero lumps for a velvety texture."},
            {"step_number": 2, "title": "Tempering & Aromatics", "instruction": "Heat oil in kadai. Splutter mustard, cumin, hing, and curry leaves. Add crushed garlic and green chillies; sauté till aromatic.", "duration_mins": 3, "tip": "Crushing garlic in mortar-pestle yields the best rustic flavor."},
            {"step_number": 3, "title": "Sauté Onions", "instruction": "Add sliced onions and fry till soft and slightly golden.", "duration_mins": 3, "tip": "Generous onions make Pithla sweet and flavorful."},
            {"step_number": 4, "title": "Pour and Whisk Continuously", "instruction": "Lower flame, pour besan slurry while stirring continuously with a spatula to prevent lumps.", "duration_mins": 3, "tip": "Keep stirring until it thickens smoothly."},
            {"step_number": 5, "title": "Steam and Garnish", "instruction": "Cover with lid and steam on lowest flame for 4 minutes until glossy and fragrant. Top with fresh coriander.", "duration_mins": 4, "tip": "Serve bubbling hot with Jowar Bhakri, Shengdana Chutney, and Raw Onion."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 250, "protein_g": 9.5, "carbs_g": 26.0, "fat_g": 12.0, "fiber_g": 5.0},
        "equipment": ["Whisk", "Kadai", "Lid"],
        "summary": "Rustic Maharashtrian soul food made of creamy tempered besan spiced with crushed garlic, green chillies, and onions."
    },
    # 6. Misal Pav
    {
        "id": "rec_misal_pav",
        "title": "Authentic Puneri / Kolhapuri Misal Pav (Spiced Sprouted Moth Bean Curry)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Breakfast", "Snack", "Lunch", "Dinner"],
        "course": "Main Course",
        "prep_time_mins": 15,
        "cook_time_mins": 25,
        "total_time_mins": 40,
        "difficulty": "Medium",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": False,
        "flavor_profile": {"spicy": 5, "tangy": 4, "sweet": 1, "savory": 5, "comfort": 5},
        "mood_tags": ["spicy", "street-food", "indulgent", "weekend", "iconic"],
        "ingredients": [
            {"name": "Sprouted Matki (Moth Beans)", "quantity": 2.0, "unit": "cups", "is_optional": False, "category": "legumes", "substitutes": ["Sprouted Moong"]},
            {"name": "Onion", "quantity": 2.0, "unit": "medium (1 sliced for paste, 1 chopped for garnish)", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Dry Coconut (Khobra)", "quantity": 0.25, "unit": "cup sliced & roasted", "is_optional": False, "category": "garnish", "substitutes": []},
            {"name": "Ginger-Garlic Paste", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Tomato", "quantity": 1.0, "unit": "chopped", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Kolhapuri / Goda Masala", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "spices", "substitutes": ["Garam Masala"]},
            {"name": "Kashmiri Red Chilli Powder", "quantity": 1.5, "unit": "tbsp (for bright red Kat / Tari)", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Turmeric Powder", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Oil", "quantity": 3.0, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": []},
            {"name": "Farsan / Spiced Sev Mixture", "quantity": 1.0, "unit": "cup", "is_optional": False, "category": "garnish", "substitutes": []},
            {"name": "Laadi Pav", "quantity": 4.0, "unit": "buns", "is_optional": False, "category": "bread", "substitutes": ["Bread slices"]},
            {"name": "Lemon Wedges & Fresh Coriander", "quantity": 1.0, "unit": "serving set", "is_optional": False, "category": "garnish", "substitutes": []}
        ],
        "normalized_ingredients": ["matki", "sprouts", "onion", "coconut", "ginger", "garlic", "tomato", "goda masala", "red chilli powder", "turmeric", "oil", "farsan", "sev", "pav", "bread", "lemon", "coriander"],
        "leftover_ingredients_used": [],
        "steps": [
            {"step_number": 1, "title": "Make Vatan Paste", "instruction": "Roast sliced onion and dry coconut in 1 tsp oil until dark brown. Blend with ginger, garlic, and tomato into a smooth paste (Vatan).", "duration_mins": 8, "tip": "Deep roasting gives Misal its trademark smoky flavor."},
            {"step_number": 2, "title": "Cook Sprouted Matki", "instruction": "Boil sprouted matki in salted water with a pinch of turmeric for 5-7 mins until tender but not mushy.", "duration_mins": 7, "tip": "Do not overcook the sprouts."},
            {"step_number": 3, "title": "Fry Masala & Create Tari (Kat)", "instruction": "Heat 3 tbsp oil. Add Vatan paste and sauté till oil oozes out. Add Goda masala and Kashmiri chilli powder.", "duration_mins": 5, "tip": "Adequate oil creates the signature fiery red 'Tari' float."},
            {"step_number": 4, "title": "Simmer Gravy", "instruction": "Add boiled matki along with its water. Add 2 cups hot water and salt. Simmer vigorously for 10 mins.", "duration_mins": 10, "tip": "The liquid should be thin and intensely spiced."},
            {"step_number": 5, "title": "Assemble Misal", "instruction": "In a shallow bowl, add boiled matki base, ladle boiling red Tari on top, heap crunchy farsan, chopped raw onions, coriander, and squeeze lemon. Serve with buttered Pav.", "duration_mins": 3, "tip": "Enjoy the fiery layers of crunch and spice!"}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 480, "protein_g": 16.0, "carbs_g": 62.0, "fat_g": 18.0, "fiber_g": 11.0},
        "equipment": ["Mixer Grinder", "Pot / Kadai", "Serving Bowls"],
        "summary": "Legendary Maharashtrian street delicacy featuring spiced sprouted moth beans topped with fiery red Tari broth, crunchy farsan, onions, and pav."
    },
    # 7. Thalipeeth
    {
        "id": "rec_thalipeeth",
        "title": "Maharashtrian Multi-Grain Thalipeeth (Spiced Flatbread)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Breakfast", "Snack", "Dinner"],
        "course": "Breakfast",
        "prep_time_mins": 10,
        "cook_time_mins": 15,
        "total_time_mins": 25,
        "difficulty": "Medium",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": False,
        "flavor_profile": {"spicy": 3, "tangy": 1, "sweet": 0, "savory": 5, "comfort": 5},
        "mood_tags": ["healthy", "rustic", "nutritious", "traditional", "comforting"],
        "ingredients": [
            {"name": "Bhajani Flour (or mix of Jowar, Besan, Rice, Wheat flour)", "quantity": 1.5, "unit": "cups", "is_optional": False, "category": "flour", "substitutes": ["Equal parts Jowar + Besan + Wheat flour"]},
            {"name": "Onion", "quantity": 1.0, "unit": "finely chopped", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Fresh Coriander (Kothimbir)", "quantity": 0.5, "unit": "cup finely chopped", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Green Chilli & Garlic Paste", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Ajwain (Carom Seeds)", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Sesame Seeds (Til)", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "seeds", "substitutes": []},
            {"name": "Turmeric & Red Chilli Powder", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Oil or Homemade White Butter (Loni)", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": ["Ghee"]},
            {"name": "Salt", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["bhajani", "jowar flour", "besan", "rice flour", "wheat flour", "onion", "coriander", "green chilli", "garlic", "ajwain", "sesame seed", "til", "turmeric", "red chilli powder", "butter", "loni", "ghee", "oil", "salt"],
        "leftover_ingredients_used": [],
        "steps": [
            {"step_number": 1, "title": "Knead Dough", "instruction": "In a bowl, mix Bhajani flour, chopped onion, coriander, chilli-garlic paste, ajwain, sesame seeds, turmeric, chilli powder, and salt. Knead with warm water into a soft pliable dough.", "duration_mins": 5, "tip": "Dough should be soft enough to pat flat with moist fingers."},
            {"step_number": 2, "title": "Pat onto Tawa or Parchment", "instruction": "Grease a cold tawa or parchment paper. Place a ball of dough and pat into a round disc using wet fingers. Make 3-4 small holes in the center.", "duration_mins": 4, "tip": "Holes allow oil/butter to circulate and cook evenly from inside."},
            {"step_number": 3, "title": "Roast with Ghee/Oil", "instruction": "Place tawa on medium flame. Drizzle oil or ghee into the holes and around edges. Cover with lid and roast for 3 mins.", "duration_mins": 4, "tip": "Covering steams the center while crisping the base."},
            {"step_number": 4, "title": "Flip and Crisp", "instruction": "Flip and roast the other side until crispy golden brown spots appear.", "duration_mins": 3, "tip": "Serve piping hot with fresh white butter (Loni), curd, and spicy thecha."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 310, "protein_g": 8.5, "carbs_g": 44.0, "fat_g": 11.0, "fiber_g": 6.2},
        "equipment": ["Iron Tawa / Flat Griddle", "Lid", "Parchment / Plastic sheet"],
        "summary": "Wholesome roasted multigrain flatbread packed with roasted lentils, onions, sesame, ajwain, and fresh coriander."
    },
    # 8. Sabudana Khichdi
    {
        "id": "rec_sabudana_khichdi",
        "title": "Non-Sticky Sabudana Khichdi (Upwas / Fasting Speciality)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Breakfast", "Snack", "Fast / Upwas"],
        "course": "Breakfast",
        "prep_time_mins": 10,
        "cook_time_mins": 12,
        "total_time_mins": 22,
        "difficulty": "Medium",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": True,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 3, "tangy": 2, "sweet": 1, "savory": 4, "comfort": 5},
        "mood_tags": ["upwas", "fasting", "comforting", "classic", "quick"],
        "ingredients": [
            {"name": "Sabudana (Tapioca Pearls)", "quantity": 1.5, "unit": "cups (soaked & drained)", "is_optional": False, "category": "grains", "substitutes": ["Varai / Samak rice"]},
            {"name": "Roasted Peanut Powder (Coarse Shengdana Koot)", "quantity": 0.5, "unit": "cup", "is_optional": False, "category": "nuts", "substitutes": []},
            {"name": "Potato (Boiled or Raw diced)", "quantity": 1.0, "unit": "medium, diced", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Green Chillies", "quantity": 3.0, "unit": "finely chopped", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Cumin Seeds (Jeera)", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Ghee or Peanut Oil", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": []},
            {"name": "Sendha Namak (Rock Salt or regular salt)", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Sugar", "quantity": 0.5, "unit": "tsp", "is_optional": True, "category": "sweetener", "substitutes": []},
            {"name": "Lemon Juice & Fresh Coriander", "quantity": 1.0, "unit": "tbsp each", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["sabudana", "sago", "peanut", "potato", "green chilli", "cumin seed", "jeera", "ghee", "oil", "salt", "sugar", "lemon juice", "coriander"],
        "leftover_ingredients_used": ["boiled potatoes"],
        "steps": [
            {"step_number": 1, "title": "Soak & Coat Sabudana", "instruction": "Ensure sabudana is soaked for 5 hours with just enough water to submerge, then fluffed dry. Toss with coarse peanut powder, salt, and sugar.", "duration_mins": 3, "tip": "Coating sabudana in peanut powder before cooking guarantees pearls won't stick together!"},
            {"step_number": 2, "title": "Tempering in Ghee", "instruction": "Heat ghee in pan. Add cumin seeds and green chillies. Sauté diced potatoes until golden and tender.", "duration_mins": 5, "tip": "Ghee delivers the ultimate fasting aroma."},
            {"step_number": 3, "title": "Toss and Steam Pearls", "instruction": "Add the peanut-coated sabudana mixture. Toss gently on medium-low flame. Cover with lid and steam for 3-4 mins until pearls turn translucent.", "duration_mins": 5, "tip": "Do not overcook or pearls become chewy."},
            {"step_number": 4, "title": "Finish", "instruction": "Turn off heat, squeeze fresh lemon juice, and garnish with coriander.", "duration_mins": 1, "tip": "Serve warm with cool spiced curd."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 360, "protein_g": 6.5, "carbs_g": 58.0, "fat_g": 12.5, "fiber_g": 2.8},
        "equipment": ["Pan / Kadai", "Lid", "Spatula"],
        "summary": "Fluffy, non-sticky translucent tapioca pearls tossed with crunchy roasted peanuts, green chillies, cumin, and potatoes in pure ghee."
    },
    # 9. Batata Vada
    {
        "id": "rec_batata_vada",
        "title": "Mumbai / Maharashtrian Batata Vada (Spiced Potato Fritters)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Snack", "Breakfast", "Tea-Time"],
        "course": "Snack",
        "prep_time_mins": 15,
        "cook_time_mins": 15,
        "total_time_mins": 30,
        "difficulty": "Medium",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 4, "tangy": 2, "sweet": 0, "savory": 5, "comfort": 5},
        "mood_tags": ["street-food", "monsoon", "tea-time", "crispy", "indulgent"],
        "ingredients": [
            {"name": "Boiled Potatoes (Batata)", "quantity": 4.0, "unit": "medium, mashed", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Ginger-Garlic-Green Chilli Paste (Thecha style)", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Mustard Seeds", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Hing (Asafoetida)", "quantity": 1.0, "unit": "pinch", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Turmeric Powder", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Curry Leaves", "quantity": 10.0, "unit": "leaves, chopped", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Besan (Gram Flour)", "quantity": 1.0, "unit": "cup", "is_optional": False, "category": "flour", "substitutes": []},
            {"name": "Rice Flour", "quantity": 1.0, "unit": "tbsp (for extra crispness)", "is_optional": False, "category": "flour", "substitutes": ["Cornflour"]},
            {"name": "Baking Soda", "quantity": 1.0, "unit": "pinch", "is_optional": True, "category": "leavening", "substitutes": []},
            {"name": "Oil for deep frying", "quantity": 2.0, "unit": "cups", "is_optional": False, "category": "oils", "substitutes": []},
            {"name": "Salt", "quantity": 1.25, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Fresh Coriander & Lemon Juice", "quantity": 1.0, "unit": "tbsp each", "is_optional": False, "category": "herbs", "substitutes": []}
        ],
        "normalized_ingredients": ["potato", "batata", "boiled potato", "ginger", "garlic", "green chilli", "mustard seed", "hing", "turmeric", "curry leaf", "besan", "gram flour", "rice flour", "oil", "salt", "coriander", "lemon juice"],
        "leftover_ingredients_used": ["boiled potatoes"],
        "steps": [
            {"step_number": 1, "title": "Prepare Potato Masala", "instruction": "Heat 1 tbsp oil in pan. Splutter mustard, hing, curry leaves, ginger-garlic-chilli paste, and turmeric. Pour over mashed boiled potatoes. Add salt, coriander, lemon juice, and mix well.", "duration_mins": 6, "tip": "Do not make potatoes too wet; let cool."},
            {"step_number": 2, "title": "Shape Balls", "instruction": "Divide potato mixture into equal round lemon-sized balls.", "duration_mins": 4, "tip": "Smooth balls coat evenly in batter."},
            {"step_number": 3, "title": "Make Crispy Batter", "instruction": "Whisk besan, rice flour, turmeric, pinch of salt, pinch of baking soda, and 1 tbsp hot oil with water to form a smooth pouring batter.", "duration_mins": 4, "tip": "A drop of hot oil in the batter ensures crispy golden coating."},
            {"step_number": 4, "title": "Dip and Fry", "instruction": "Heat oil in deep kadai. Dip each potato ball in batter, slide gently into hot oil, and deep fry till crisp and golden.", "duration_mins": 8, "tip": "Serve with spicy dry garlic chutney and fried salted green chillies."}
        ],
        "nutrition_per_serving": {"servings": 3, "calories": 310, "protein_g": 7.0, "carbs_g": 38.0, "fat_g": 14.5, "fiber_g": 4.5},
        "equipment": ["Deep Frying Kadai", "Slotted Spoon", "Mixing Bowls"],
        "summary": "Golden, crunchy besan-crusted fritters stuffed with a fiery turmeric, garlic, mustard and curry-leaf spiced potato filling."
    },
    # 10. Kothimbir Vadi
    {
        "id": "rec_kothimbir_vadi",
        "title": "Crispy Maharashtrian Kothimbir Vadi (Steamed & Pan-Crisped Coriander Cakes)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Snack", "Tea-Time", "Appetizer"],
        "course": "Snack",
        "prep_time_mins": 15,
        "cook_time_mins": 20,
        "total_time_mins": 35,
        "difficulty": "Medium",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 3, "tangy": 2, "sweet": 1, "savory": 5, "comfort": 4},
        "mood_tags": ["crispy", "tea-time", "monsoon", "traditional", "party"],
        "ingredients": [
            {"name": "Fresh Coriander Leaves (Kothimbir)", "quantity": 2.0, "unit": "cups, washed & finely chopped", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Besan (Gram Flour)", "quantity": 1.0, "unit": "cup", "is_optional": False, "category": "flour", "substitutes": []},
            {"name": "Rice Flour", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "flour", "substitutes": []},
            {"name": "Ginger-Garlic-Chilli Paste", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Sesame Seeds (Til)", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "seeds", "substitutes": []},
            {"name": "Turmeric & Red Chilli Powder", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Cumin Seeds & Ajwain", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Lemon Juice & Sugar", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Salt", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Oil", "quantity": 2.0, "unit": "tbsp (for shallow fry)", "is_optional": False, "category": "oils", "substitutes": []}
        ],
        "normalized_ingredients": ["coriander", "kothimbir", "besan", "rice flour", "ginger", "garlic", "green chilli", "sesame seed", "til", "turmeric", "red chilli powder", "cumin seed", "ajwain", "lemon juice", "sugar", "salt", "oil"],
        "leftover_ingredients_used": [],
        "steps": [
            {"step_number": 1, "title": "Make Dough/Batter", "instruction": "Mix dry chopped coriander, besan, rice flour, spices, ginger-garlic-chilli paste, sesame seeds, lemon juice, salt, and knead with minimal water into a tight cylindrical roll.", "duration_mins": 6, "tip": "Coriander releases moisture, so add water 1 tsp at a time."},
            {"step_number": 2, "title": "Steam", "instruction": "Place cylinder rolls in a greased steamer plate and steam for 15 minutes until a knife inserted comes out clean.", "duration_mins": 15, "tip": "Let cool completely before slicing."},
            {"step_number": 3, "title": "Slice", "instruction": "Cut steamed roll into 1/2 inch thick square or diagonal vadis.", "duration_mins": 3, "tip": "Cooling prevents crumbling while slicing."},
            {"step_number": 4, "title": "Pan-Crisp / Fry", "instruction": "Shallow fry or pan-toast in hot oil on medium flame until golden crisp on both sides.", "duration_mins": 8, "tip": "Serve with hot masala chai."}
        ],
        "nutrition_per_serving": {"servings": 3, "calories": 210, "protein_g": 7.2, "carbs_g": 24.0, "fat_g": 9.0, "fiber_g": 4.5},
        "equipment": ["Steamer / Idli Pot", "Tawa / Frying Pan", "Knife"],
        "summary": "Savory steamed and crisp-toasted coriander besan cakes topped with toasted sesame seeds."
    },
    # 11. Varan Bhaat with Toop (Ghee)
    {
        "id": "rec_varan_bhaat",
        "title": "Sada Varan Bhaat with Shuddha Toop (Pure Maharashtrian Comfort Meal)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Lunch", "Dinner"],
        "course": "Main Course",
        "prep_time_mins": 5,
        "cook_time_mins": 20,
        "total_time_mins": 25,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": False,
        "is_jain": True,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 0, "tangy": 1, "sweet": 1, "savory": 4, "comfort": 5},
        "mood_tags": ["comforting", "healthy", "soothing", "traditional", "quick"],
        "ingredients": [
            {"name": "Toor Dal (Arhar Dal)", "quantity": 1.0, "unit": "cup", "is_optional": False, "category": "legumes", "substitutes": ["Moong Dal"]},
            {"name": "Steamed Rice (Indrayani or Kolam)", "quantity": 2.0, "unit": "cups cooked", "is_optional": False, "category": "grains", "substitutes": []},
            {"name": "Turmeric Powder", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Hing (Asafoetida)", "quantity": 1.0, "unit": "pinch", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Jaggery (Gul)", "quantity": 0.5, "unit": "tsp", "is_optional": True, "category": "sweetener", "substitutes": []},
            {"name": "Pure Ghee (Shuddha Toop)", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "dairy", "substitutes": []},
            {"name": "Salt", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Lemon Slice", "quantity": 1.0, "unit": "wedge", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["toor dal", "dal", "varan", "rice", "bhaat", "turmeric", "hing", "jaggery", "ghee", "toop", "salt", "lemon"],
        "leftover_ingredients_used": [],
        "steps": [
            {"step_number": 1, "title": "Pressure Cook Dal", "instruction": "Wash toor dal, add 2.5 cups water, turmeric, and pinch of hing. Pressure cook for 4 whistles until completely soft.", "duration_mins": 15, "tip": "Indrayani rice cooked with dal gives heavenly fragrant softness."},
            {"step_number": 2, "title": "Mash & Season", "instruction": "Whisk hot cooked dal with a wooden churner (Ravi) until silky. Add salt, jaggery, 1/2 cup water and simmer for 5 mins.", "duration_mins": 5, "tip": "Traditional Sada Varan is unspiced to let the natural sweetness of toor dal shine."},
            {"step_number": 3, "title": "Serve with Toop", "instruction": "Mound steaming hot rice on a plate, make a well in the center, ladle creamy varan, top with a generous spoonful of pure homemade ghee, and squeeze fresh lemon.", "duration_mins": 2, "tip": "Serve with roasted Papad and Mango pickle."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 370, "protein_g": 12.0, "carbs_g": 56.0, "fat_g": 10.5, "fiber_g": 6.5},
        "equipment": ["Pressure Cooker", "Dal Churner (Ravi)", "Pot"],
        "summary": "The quintessential Maharashtrian comfort meal of silky boiled toor dal poured over fragrant steaming rice with pure golden ghee and lemon."
    },
    # 12. Katachi Amti
    {
        "id": "rec_katachi_amti",
        "title": "Katachi Amti (Spicy Tangy Chana Dal Broth for Puran Poli)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Lunch", "Dinner"],
        "course": "Soup / Curry",
        "prep_time_mins": 10,
        "cook_time_mins": 20,
        "total_time_mins": 30,
        "difficulty": "Medium",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 4, "tangy": 4, "sweet": 2, "savory": 4, "comfort": 5},
        "mood_tags": ["festive", "traditional", "tangy", "spicy"],
        "ingredients": [
            {"name": "Chana Dal Strained Stock (Kat)", "quantity": 2.5, "unit": "cups (from boiling chana dal)", "is_optional": False, "category": "legumes", "substitutes": ["Boiled Toor dal water"]},
            {"name": "Boiled Chana Dal (mashed)", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "legumes", "substitutes": []},
            {"name": "Dry Roasted Coconut & Onion Paste", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "garnish", "substitutes": []},
            {"name": "Goda Masala", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "spices", "substitutes": ["Garam Masala"]},
            {"name": "Kashmiri Red Chilli Powder", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Tamarind Pulp", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "seasoning", "substitutes": ["Kokum"]},
            {"name": "Jaggery (Gul)", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "sweetener", "substitutes": []},
            {"name": "Mustard, Cumin & Hing", "quantity": 1.0, "unit": "tsp combined", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Curry Leaves & Coriander", "quantity": 1.0, "unit": "handful", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Oil or Ghee", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": []},
            {"name": "Salt", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["chana dal", "dal", "coconut", "onion", "goda masala", "red chilli powder", "tamarind", "kokum", "jaggery", "mustard seed", "cumin seed", "hing", "curry leaf", "coriander", "oil", "ghee", "salt"],
        "leftover_ingredients_used": ["leftover dal", "chana dal stock"],
        "steps": [
            {"step_number": 1, "title": "Prepare Amti Base", "instruction": "Boil chana dal and strain the clear stock (Kat). Reserve 2 tbsp cooked dal and mash it with 2 tbsp roasted coconut-onion paste.", "duration_mins": 5, "tip": "The kat provides clarity while mashed dal adds body."},
            {"step_number": 2, "title": "Tempering (Phodni)", "instruction": "Heat oil/ghee. Splutter mustard, cumin, hing, and curry leaves. Add red chilli powder and Goda Masala.", "duration_mins": 3, "tip": "Keep heat low so spices bloom without burning."},
            {"step_number": 3, "title": "Simmer Broth", "instruction": "Pour the dal stock and mashed dal paste. Add tamarind pulp, jaggery, salt, and bring to a rolling boil.", "duration_mins": 10, "tip": "Simmer for at least 10 minutes for flavors to marry."},
            {"step_number": 4, "title": "Garnish", "instruction": "Garnish with chopped fresh coriander. Serve hot with Puran Poli or steamed rice.", "duration_mins": 2, "tip": "The interplay of sweet jaggery, tart tamarind, and spicy goda masala is magical."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 180, "protein_g": 6.0, "carbs_g": 26.0, "fat_g": 6.5, "fiber_g": 3.8},
        "equipment": ["Saucepan", "Strainer", "Ladle"],
        "summary": "Aromatic, tangy, sweet, and spicy Maharashtrian festive broth made from strained chana dal stock with tamarind, jaggery, and Goda Masala."
    },
    # 13. Solkadhi
    {
        "id": "rec_solkadhi",
        "title": "Konkani Solkadhi (Refreshing Kokum & Fresh Coconut Milk Digestive Drink)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Beverage", "Side Dish", "Lunch", "Dinner"],
        "course": "Beverage",
        "prep_time_mins": 15,
        "cook_time_mins": 0,
        "total_time_mins": 15,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 2, "tangy": 5, "sweet": 1, "savory": 4, "comfort": 5},
        "mood_tags": ["refreshing", "digestive", "cooling", "summer", "coastal", "quick"],
        "ingredients": [
            {"name": "Fresh Grated Coconut", "quantity": 1.5, "unit": "cups", "is_optional": False, "category": "garnish", "substitutes": ["Thick Coconut Milk (Canned)"]},
            {"name": "Kokum (Amsul)", "quantity": 8.0, "unit": "petals, soaked in 1/2 cup warm water", "is_optional": False, "category": "seasoning", "substitutes": ["Kokum Agal"]},
            {"name": "Garlic (Lasun)", "quantity": 2.0, "unit": "cloves", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Green Chilli", "quantity": 1.0, "unit": "small", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Cumin Seeds (Jeera)", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Salt & Pink Rock Salt", "quantity": 0.75, "unit": "tsp combined", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Fresh Coriander", "quantity": 2.0, "unit": "tbsp chopped", "is_optional": False, "category": "herbs", "substitutes": []}
        ],
        "normalized_ingredients": ["coconut", "fresh coconut", "kokum", "garlic", "lasun", "green chilli", "cumin seed", "jeera", "salt", "coriander"],
        "leftover_ingredients_used": [],
        "steps": [
            {"step_number": 1, "title": "Extract Coconut Milk", "instruction": "Grind fresh coconut with garlic, green chilli, cumin seeds, and 1 cup warm water. Strain through a fine muslin cloth to extract thick rich milk. Repeat once with 1/2 cup water for second extract.", "duration_mins": 8, "tip": "Warm water extracts higher fat and cream from coconut."},
            {"step_number": 2, "title": "Extract Kokum Essence (Agal)", "instruction": "Squeeze soaked kokum petals thoroughly to extract vibrant purple tangy extract. Strain into the coconut milk.", "duration_mins": 4, "tip": "Watch the white coconut milk blush into a gorgeous pastel pink!"},
            {"step_number": 3, "title": "Season & Chill", "instruction": "Add salt, rock salt, and finely chopped coriander. Stir gently and chill in refrigerator for 20 mins before serving.", "duration_mins": 3, "tip": "Do not boil or heat Solkadhi; it is served cold."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 160, "protein_g": 2.2, "carbs_g": 8.0, "fat_g": 14.0, "fiber_g": 3.0},
        "equipment": ["Mixer Grinder", "Muslin Cloth / Fine Strainer", "Glass Pitcher"],
        "summary": "Pink Konkani elixir made of fresh creamy coconut milk infused with tangy kokum petals, garlic, green chilli, and cumin."
    },
    # 14. Dal Paratha
    {
        "id": "rec_dal_paratha",
        "title": "Spiced Leftover Dal Paratha (Missi Roti Style)",
        "regional_cuisine": "North Indian",
        "meal_type": ["Breakfast", "Lunch", "Dinner"],
        "course": "Main Course",
        "prep_time_mins": 10,
        "cook_time_mins": 12,
        "total_time_mins": 22,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": False,
        "is_jain": False,
        "is_gluten_free": False,
        "flavor_profile": {"spicy": 3, "tangy": 1, "sweet": 0, "savory": 4, "comfort": 5},
        "mood_tags": ["quick", "comforting", "zero-waste", "breakfast", "nutritious"],
        "ingredients": [
            {"name": "Leftover Dal (Yellow/Toor/Moong)", "quantity": 1.0, "unit": "cup", "is_optional": False, "category": "legumes", "substitutes": ["Leftover Sambar"]},
            {"name": "Whole Wheat Flour (Atta)", "quantity": 2.0, "unit": "cups", "is_optional": False, "category": "flour", "substitutes": []},
            {"name": "Onion", "quantity": 1.0, "unit": "finely chopped", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Green Chillies & Ginger", "quantity": 1.0, "unit": "tbsp finely chopped", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Ajwain (Carom Seeds)", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Kasuri Methi", "quantity": 1.0, "unit": "tbsp crushed", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Fresh Coriander", "quantity": 2.0, "unit": "tbsp chopped", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Ghee or Butter", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "dairy", "substitutes": ["Oil"]},
            {"name": "Salt", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["dal", "leftover dal", "wheat flour", "atta", "onion", "green chilli", "ginger", "ajwain", "kasuri methi", "coriander", "ghee", "butter", "salt"],
        "leftover_ingredients_used": ["leftover dal", "dal", "varan"],
        "steps": [
            {"step_number": 1, "title": "Knead Dal Dough", "instruction": "In a large bowl, combine wheat flour, leftover dal, onion, green chillies, ajwain, kasuri methi, coriander, and salt. Knead into a smooth soft dough without adding extra water.", "duration_mins": 5, "tip": "Dal makes the dough exceptionally soft and protein-rich."},
            {"step_number": 2, "title": "Roll Parathas", "instruction": "Divide dough into equal balls. Dust with flour and roll into 7-inch round parathas.", "duration_mins": 3, "tip": "Roll gently so onions don't tear the edges."},
            {"step_number": 3, "title": "Roast on Tawa", "instruction": "Heat tawa on medium-high. Place paratha and cook for 1 min until bubbles appear. Flip, brush with ghee, flip again and press edges until golden crisp spots develop.", "duration_mins": 4, "tip": "Serve hot with curd, butter, and pickle."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 320, "protein_g": 9.8, "carbs_g": 48.0, "fat_g": 10.0, "fiber_g": 5.5},
        "equipment": ["Mixing Bowl", "Rolling Pin & Board", "Tawa / Griddle"],
        "summary": "Flaky, ultra-soft parathas made by kneading leftover dal directly into whole wheat flour with ajwain and kasuri methi."
    },
    # 15. Chakolya / Varan Phal
    {
        "id": "rec_chakolya",
        "title": "Maharashtrian Chakolya / Varan Phal (Spiced Wheat Dumplings Simmered in Dal)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Lunch", "Dinner"],
        "course": "Main Course",
        "prep_time_mins": 15,
        "cook_time_mins": 15,
        "total_time_mins": 30,
        "difficulty": "Medium",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": False,
        "flavor_profile": {"spicy": 3, "tangy": 3, "sweet": 1, "savory": 4, "comfort": 5},
        "mood_tags": ["comforting", "rainy-day", "monsoon", "traditional", "one-pot"],
        "ingredients": [
            {"name": "Leftover Dal or Boiled Toor Dal", "quantity": 2.0, "unit": "cups", "is_optional": False, "category": "legumes", "substitutes": []},
            {"name": "Whole Wheat Flour", "quantity": 1.0, "unit": "cup", "is_optional": False, "category": "flour", "substitutes": []},
            {"name": "Ajwain & Turmeric", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Goda Masala & Red Chilli Powder", "quantity": 1.0, "unit": "tsp each", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Kokum or Tamarind", "quantity": 3.0, "unit": "petals / 1 tbsp pulp", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Jaggery", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "sweetener", "substitutes": []},
            {"name": "Mustard, Cumin, Hing & Curry Leaves", "quantity": 1.0, "unit": "tsp combined", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Peanuts", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "nuts", "substitutes": []},
            {"name": "Ghee or Oil", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "dairy", "substitutes": []},
            {"name": "Salt & Coriander", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["dal", "leftover dal", "varan", "wheat flour", "atta", "ajwain", "turmeric", "goda masala", "red chilli powder", "kokum", "tamarind", "jaggery", "mustard seed", "cumin seed", "hing", "curry leaf", "peanut", "ghee", "oil", "salt", "coriander"],
        "leftover_ingredients_used": ["leftover dal", "dal", "varan"],
        "steps": [
            {"step_number": 1, "title": "Knead Wheat Dough & Cut Diamonds", "instruction": "Knead wheat flour with salt, ajwain, turmeric, and 1 tsp oil into a firm dough. Roll out thin into a large roti and cut into diamond strips (phal).", "duration_mins": 8, "tip": "Rolling thin ensures dumplings cook quickly and evenly."},
            {"step_number": 2, "title": "Prepare Boiling Dal Base", "instruction": "In a pot, heat ghee, splutter mustard, cumin, hing, curry leaves, and peanuts. Add leftover dal, 2 cups water, goda masala, chilli powder, kokum, jaggery, and salt. Bring to a rolling boil.", "duration_mins": 7, "tip": "Dal must be boiling vigorously before dropping dumplings."},
            {"step_number": 3, "title": "Drop Diamonds and Simmer", "instruction": "Drop wheat diamond strips one by one into the boiling dal so they don't stick. Cover and cook on medium flame for 10-12 minutes until dumplings float and are cooked through.", "duration_mins": 12, "tip": "The starch from dumplings thickens the dal broth into pure comfort."},
            {"step_number": 4, "title": "Finish", "instruction": "Ladle into deep bowls, drizzle warm ghee on top, and garnish with fresh coriander.", "duration_mins": 3, "tip": "One-pot Indian pasta comfort at its best."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 360, "protein_g": 11.5, "carbs_g": 58.0, "fat_g": 9.5, "fiber_g": 7.0},
        "equipment": ["Rolling Pin", "Deep Pot / Kadai", "Lid"],
        "summary": "Hearty Maharashtrian one-pot meal of spiced whole wheat diamond dumplings simmered in bubbling tangy-sweet toor dal."
    },
    # 16. Maharashtrian Kadhi
    {
        "id": "rec_maharashtrian_kadhi",
        "title": "Maharashtrian Sweet & Tangy Kadhi (Tempered Buttermilk Soup)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Lunch", "Dinner"],
        "course": "Soup / Curry",
        "prep_time_mins": 5,
        "cook_time_mins": 10,
        "total_time_mins": 15,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": False,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 2, "tangy": 4, "sweet": 3, "savory": 4, "comfort": 5},
        "mood_tags": ["comforting", "quick", "soothing", "zero-waste"],
        "ingredients": [
            {"name": "Sour Curd (Khatta Dahi) or Buttermilk", "quantity": 1.5, "unit": "cups", "is_optional": False, "category": "dairy", "substitutes": ["Fresh curd + lemon juice"]},
            {"name": "Besan (Gram Flour)", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "flour", "substitutes": []},
            {"name": "Water", "quantity": 1.5, "unit": "cups", "is_optional": False, "category": "liquids", "substitutes": []},
            {"name": "Ginger & Green Chilli Paste", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Jaggery (Gul)", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "sweetener", "substitutes": ["Sugar"]},
            {"name": "Cloves & Cinnamon", "quantity": 2.0, "unit": "cloves + 1 inch cinnamon", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Mustard Seeds & Cumin Seeds", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Curry Leaves & Hing", "quantity": 8.0, "unit": "leaves + pinch hing", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Ghee", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "dairy", "substitutes": ["Oil"]},
            {"name": "Salt & Fresh Coriander", "quantity": 1.0, "unit": "tsp each", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["curd", "dahi", "sour curd", "buttermilk", "taak", "besan", "ginger", "green chilli", "jaggery", "clove", "cinnamon", "mustard seed", "cumin seed", "curry leaf", "hing", "ghee", "salt", "coriander"],
        "leftover_ingredients_used": ["sour curd", "curd", "dahi", "buttermilk"],
        "steps": [
            {"step_number": 1, "title": "Whisk Curd and Besan", "instruction": "Whisk sour curd, besan, water, ginger-green chilli paste, jaggery, and salt until completely smooth.", "duration_mins": 3, "tip": "Thorough whisking prevents curd from curdling when heated."},
            {"step_number": 2, "title": "Ghee Phodni (Tempering)", "instruction": "Heat ghee in saucepan. Add cloves, cinnamon, mustard, cumin, hing, and curry leaves.", "duration_mins": 3, "tip": "Whole cloves and cinnamon give Maharashtrian kadhi its distinct aromatic charm."},
            {"step_number": 3, "title": "Simmer on Low Flame", "instruction": "Pour the whisked curd mixture into the pan. Stir continuously over medium-low flame until it comes to a single gentle simmer.", "duration_mins": 7, "tip": "Do not boil violently or leave unattended to prevent splitting."},
            {"step_number": 4, "title": "Garnish", "instruction": "Turn off flame, top with fresh coriander, and serve with steaming hot Khichdi.", "duration_mins": 2, "tip": "Pair with Moong Dal Khichdi for ultimate digestive warmth."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 190, "protein_g": 6.5, "carbs_g": 20.0, "fat_g": 9.5, "fiber_g": 1.8},
        "equipment": ["Whisk", "Saucepan", "Ladle"],
        "summary": "Delicate, sweet and tangy Maharashtrian curd curry tempered with aromatic cloves, cinnamon, mustard, and pure ghee."
    },
    # 17. Bread Upma (Phodnicha Bread)
    {
        "id": "rec_bread_upma",
        "title": "Spiced Bread Upma (Phodnicha Bread)",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Breakfast", "Snack", "Quick Meal"],
        "course": "Snack",
        "prep_time_mins": 5,
        "cook_time_mins": 8,
        "total_time_mins": 13,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": True,
        "is_jain": False,
        "is_gluten_free": False,
        "flavor_profile": {"spicy": 3, "tangy": 3, "sweet": 1, "savory": 4, "comfort": 4},
        "mood_tags": ["quick", "zero-waste", "comforting", "kids-friendly"],
        "ingredients": [
            {"name": "Leftover Bread Slices / Pav", "quantity": 6.0, "unit": "slices, cubed", "is_optional": False, "category": "bread", "substitutes": ["Pav buns"]},
            {"name": "Onion", "quantity": 1.0, "unit": "medium, chopped", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Tomato", "quantity": 1.0, "unit": "chopped", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Peanuts", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "nuts", "substitutes": []},
            {"name": "Green Chillies", "quantity": 2.0, "unit": "slit", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Mustard Seeds & Cumin Seeds", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Turmeric & Red Chilli Powder", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Curry Leaves", "quantity": 6.0, "unit": "leaves", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Oil or Butter", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "oils", "substitutes": []},
            {"name": "Lemon Juice, Salt & Fresh Coriander", "quantity": 1.0, "unit": "set", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["bread", "pav", "onion", "tomato", "peanut", "green chilli", "mustard seed", "cumin seed", "turmeric", "red chilli powder", "curry leaf", "oil", "butter", "lemon juice", "salt", "coriander"],
        "leftover_ingredients_used": ["leftover bread", "bread", "pav"],
        "steps": [
            {"step_number": 1, "title": "Cube Bread", "instruction": "Cut stale bread or pav into bite-sized 1-inch cubes.", "duration_mins": 2, "tip": "Slightly stale bread absorbs spices without turning soggy."},
            {"step_number": 2, "title": "Tempering & Veggies", "instruction": "Heat oil in kadai. Fry peanuts till crisp. Add mustard, cumin, curry leaves, chillies, and onions. Sauté till soft, then add chopped tomatoes, turmeric, chilli powder, and salt.", "duration_mins": 5, "tip": "Cook tomatoes till soft and mushy to form a rich sauce."},
            {"step_number": 3, "title": "Toss Bread", "instruction": "Sprinkle 1 tbsp water on tomatoes to create slight steam, immediately add bread cubes and toss gently until every piece is coated.", "duration_mins": 4, "tip": "Toss quickly on high flame to keep outer edges crisp."},
            {"step_number": 4, "title": "Garnish", "instruction": "Squeeze lemon juice, garnish with coriander and sev. Serve immediately.", "duration_mins": 2, "tip": "Delicious tea-time snack ready in minutes."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 250, "protein_g": 6.0, "carbs_g": 36.0, "fat_g": 9.0, "fiber_g": 3.0},
        "equipment": ["Kadai", "Spatula"],
        "summary": "Tangy and spicy snack of cubed bread tossed with golden onions, juicy tomatoes, crunchy peanuts, and mustard tempering."
    },
    # 18. Dahi Tadka
    {
        "id": "rec_dahi_tadka",
        "title": "Dhabha-Style Dahi Tadka (Garlic-Tempered Curd Bowl)",
        "regional_cuisine": "North Indian",
        "meal_type": ["Side Dish", "Quick Meal", "Lunch", "Dinner"],
        "course": "Side Dish",
        "prep_time_mins": 3,
        "cook_time_mins": 3,
        "total_time_mins": 6,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": False,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 4, "tangy": 4, "sweet": 0, "savory": 5, "comfort": 5},
        "mood_tags": ["quick", "zero-waste", "dhabha-style", "5-min"],
        "ingredients": [
            {"name": "Thick Curd (Dahi)", "quantity": 1.5, "unit": "cups, whisked", "is_optional": False, "category": "dairy", "substitutes": ["Greek Yogurt"]},
            {"name": "Garlic (Lasun)", "quantity": 6.0, "unit": "cloves, finely sliced", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Onion", "quantity": 1.0, "unit": "small, finely chopped", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Green Chilli", "quantity": 1.0, "unit": "chopped", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Dry Kashmiri Red Chilli", "quantity": 2.0, "unit": "whole", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Cumin Seeds & Mustard Seeds", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Kashmiri Red Chilli Powder", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Kasuri Methi & Hing", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Ghee or Mustard Oil", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "dairy", "substitutes": []},
            {"name": "Salt & Fresh Coriander", "quantity": 1.0, "unit": "tsp each", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["curd", "dahi", "sour curd", "garlic", "lasun", "onion", "green chilli", "red chilli", "cumin seed", "mustard seed", "red chilli powder", "kasuri methi", "hing", "ghee", "mustard oil", "salt", "coriander"],
        "leftover_ingredients_used": ["sour curd", "curd", "dahi"],
        "steps": [
            {"step_number": 1, "title": "Whisk Curd", "instruction": "Whisk thick curd with salt in a serving bowl until smooth and creamy.", "duration_mins": 1, "tip": "Keep curd at room temperature so the hot tadka doesn't cause drastic temperature shock."},
            {"step_number": 2, "title": "Sizzle Sizzling Tadka", "instruction": "Heat ghee in a tadka pan. Add cumin, mustard, whole red chillies, sliced garlic, and chopped onions. Fry until garlic turns fragrant and golden brown.", "duration_mins": 3, "tip": "Golden fried garlic is the hero of this dish."},
            {"step_number": 3, "title": "Add Spices & Pour", "instruction": "Turn off flame, immediately add Kashmiri chilli powder, hing, and crushed kasuri methi. Pour the sizzling hot tadka directly over the beaten curd.", "duration_mins": 1, "tip": "Do not stir completely; let the fiery red oil swirl over the cool white curd."},
            {"step_number": 4, "title": "Serve", "instruction": "Garnish with fresh coriander and serve immediately with hot parathas or roti.", "duration_mins": 1, "tip": "A 5-minute lifesaver when no vegetables are in the house!"}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 210, "protein_g": 6.8, "carbs_g": 11.0, "fat_g": 15.0, "fiber_g": 1.2},
        "equipment": ["Tadka Pan", "Serving Bowl", "Whisk"],
        "summary": "Creamy whipped curd crowned with a sizzling, fragrant tempering of golden garlic, Kashmiri red chilli, cumin, and ghee."
    },
    # 19. Curd Rice (Daddojanam)
    {
        "id": "rec_curd_rice",
        "title": "Temple Style Curd Rice (Daddojanam / Dahi Bhaat)",
        "regional_cuisine": "South Indian",
        "meal_type": ["Lunch", "Dinner", "Quick Meal"],
        "course": "Main Course",
        "prep_time_mins": 5,
        "cook_time_mins": 5,
        "total_time_mins": 10,
        "difficulty": "Easy",
        "diet": "Vegetarian",
        "is_vegan": False,
        "is_jain": False,
        "is_gluten_free": True,
        "flavor_profile": {"spicy": 2, "tangy": 3, "sweet": 0, "savory": 4, "comfort": 5},
        "mood_tags": ["comforting", "cooling", "summer", "zero-waste", "soothing"],
        "ingredients": [
            {"name": "Cooked Rice", "quantity": 2.5, "unit": "cups, cooled / leftover", "is_optional": False, "category": "grains", "substitutes": []},
            {"name": "Fresh Curd (Dahi)", "quantity": 1.5, "unit": "cups", "is_optional": False, "category": "dairy", "substitutes": []},
            {"name": "Milk", "quantity": 0.25, "unit": "cup", "is_optional": False, "category": "dairy", "substitutes": []},
            {"name": "Mustard Seeds", "quantity": 0.5, "unit": "tsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Urad Dal & Chana Dal", "quantity": 0.5, "unit": "tsp each", "is_optional": False, "category": "legumes", "substitutes": []},
            {"name": "Ginger (Ale)", "quantity": 1.0, "unit": "tsp finely minced", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Green Chillies", "quantity": 2.0, "unit": "chopped", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Curry Leaves & Hing", "quantity": 8.0, "unit": "leaves + pinch hing", "is_optional": False, "category": "herbs", "substitutes": []},
            {"name": "Ghee or Oil", "quantity": 1.0, "unit": "tbsp", "is_optional": False, "category": "dairy", "substitutes": []},
            {"name": "Pomegranate Arils or Grapes", "quantity": 2.0, "unit": "tbsp", "is_optional": True, "category": "garnish", "substitutes": ["Grated cucumber"]},
            {"name": "Salt", "quantity": 1.0, "unit": "tsp", "is_optional": False, "category": "seasoning", "substitutes": []}
        ],
        "normalized_ingredients": ["cooked rice", "rice", "bhaat", "curd", "dahi", "milk", "mustard seed", "urad dal", "chana dal", "ginger", "green chilli", "curry leaf", "hing", "ghee", "pomegranate", "salt"],
        "leftover_ingredients_used": ["cooked rice", "rice", "bhaat"],
        "steps": [
            {"step_number": 1, "title": "Mash Rice with Curd and Milk", "instruction": "In a bowl, lightly mash soft cooked rice with back of a spoon. Mix in fresh curd, milk, and salt until luscious and creamy.", "duration_mins": 3, "tip": "Adding a splash of milk prevents curd rice from turning overly sour if kept for a few hours."},
            {"step_number": 2, "title": "Prepare South Indian Tadka", "instruction": "Heat ghee/oil in a small pan. Add mustard seeds, urad dal, chana dal and fry until golden. Add minced ginger, green chillies, curry leaves, and hing.", "duration_mins": 3, "tip": "Crunchy golden lentils give the iconic bite."},
            {"step_number": 3, "title": "Combine & Garnish", "instruction": "Pour the aromatic tadka into the rice, mix gently, and fold in juicy pomegranate seeds and fresh coriander.", "duration_mins": 2, "tip": "Serve chilled with lime pickle or roasted papad."}
        ],
        "nutrition_per_serving": {"servings": 2, "calories": 290, "protein_g": 7.5, "carbs_g": 48.0, "fat_g": 7.5, "fiber_g": 2.2},
        "equipment": ["Mixing Bowl", "Tadka Pan", "Spoon"],
        "summary": "Creamy, soothing South Indian curd rice tempered with crunchy dal, ginger, curry leaves, and ruby pomegranate arils."
    },
    # 20. Pav Bhaji
    {
        "id": "rec_pav_bhaji",
        "title": "Mumbai Street-Style Pav Bhaji",
        "regional_cuisine": "Maharashtrian",
        "meal_type": ["Lunch", "Dinner", "Snack"],
        "course": "Main Course",
        "prep_time_mins": 15,
        "cook_time_mins": 25,
        "total_time_mins": 40,
        "difficulty": "Medium",
        "diet": "Vegetarian",
        "is_vegan": False,
        "is_jain": False,
        "is_gluten_free": False,
        "flavor_profile": {"spicy": 4, "tangy": 4, "sweet": 1, "savory": 5, "comfort": 5},
        "mood_tags": ["street-food", "indulgent", "weekend", "comforting", "party"],
        "ingredients": [
            {"name": "Boiled Potatoes (Batata)", "quantity": 3.0, "unit": "large, mashed", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Boiled Cauliflower & Green Peas", "quantity": 1.5, "unit": "cups mashed", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Capsicum / Bell Pepper", "quantity": 1.0, "unit": "medium, finely diced", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Onions", "quantity": 2.0, "unit": "finely chopped", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Tomatoes", "quantity": 4.0, "unit": "ripe, finely pureed/chopped", "is_optional": False, "category": "vegetables", "substitutes": []},
            {"name": "Ginger-Garlic Paste", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "aromatics", "substitutes": []},
            {"name": "Pav Bhaji Masala", "quantity": 2.0, "unit": "tbsp", "is_optional": False, "category": "spices", "substitutes": ["Garam Masala + Amchur"]},
            {"name": "Kashmiri Red Chilli Powder", "quantity": 1.5, "unit": "tbsp", "is_optional": False, "category": "spices", "substitutes": []},
            {"name": "Butter (Amul)", "quantity": 4.0, "unit": "tbsp", "is_optional": False, "category": "dairy", "substitutes": ["Oil"]},
            {"name": "Kasuri Methi & Lemon Juice", "quantity": 1.0, "unit": "tbsp each", "is_optional": False, "category": "seasoning", "substitutes": []},
            {"name": "Laadi Pav", "quantity": 6.0, "unit": "buns", "is_optional": False, "category": "bread", "substitutes": []},
            {"name": "Fresh Coriander & Salt", "quantity": 1.0, "unit": "tbsp / to taste", "is_optional": False, "category": "herbs", "substitutes": []}
        ],
        "normalized_ingredients": ["potato", "batata", "boiled potato", "cauliflower", "green peas", "capsicum", "onion", "tomato", "ginger", "garlic", "pav bhaji masala", "red chilli powder", "butter", "kasuri methi", "lemon", "pav", "bread", "coriander", "salt"],
        "leftover_ingredients_used": ["boiled potatoes", "leftover sabzi"],
        "steps": [
            {"step_number": 1, "title": "Mash Boiled Vegetables", "instruction": "Boil potatoes, cauliflower, and green peas. Mash them thoroughly with a potato masher till smooth.", "duration_mins": 5, "tip": "Smooth uniform mashing gives rich street-style texture."},
            {"step_number": 2, "title": "Sauté Aromatics & Veggies", "instruction": "Melt 2 tbsp butter on a large tawa or flat kadai. Sauté chopped onions, ginger-garlic paste, and finely diced capsicum for 4-5 mins.", "duration_mins": 5, "tip": "Sauté capsicum with onions for signature crunch and aroma."},
            {"step_number": 3, "title": "Simmer with Tomatoes & Spices", "instruction": "Add tomato puree, Pav Bhaji masala, Kashmiri chilli powder, kasuri methi, and salt. Cook until butter starts oozing from sides.", "duration_mins": 6, "tip": "Kashmiri chilli powder provides vibrant red color naturally without artificial food colors."},
            {"step_number": 4, "title": "Combine, Mash on Tawa & Simmer", "instruction": "Add the mashed vegetables and 1 cup warm water. Continuously mash with potato masher on high heat while simmering for 10 mins.", "duration_mins": 10, "tip": "Continuous mashing and bubbling on tawa emulsifies the butter and veggies."},
            {"step_number": 5, "title": "Butter Toast Pav & Serve", "instruction": "Slit pav buns, slather with butter and a pinch of Pav Bhaji masala, and toast on hot tawa. Serve bubbling bhaji topped with butter slab, chopped onions, and lemon wedges.", "duration_mins": 4, "tip": "The ultimate Mumbai street classic."}
        ],
        "nutrition_per_serving": {"servings": 3, "calories": 440, "protein_g": 9.5, "carbs_g": 62.0, "fat_g": 18.0, "fiber_g": 7.5},
        "equipment": ["Potato Masher", "Large Flat Tawa / Kadai", "Spatula"],
        "summary": "Iconic Mumbai street delicacy of spicy, butter-drenched mashed vegetable gravy served with hot, crisp butter-toasted pav buns."
    }
]

# We will supplement this dataset programmatically to reach 105+ diverse, authentic, realistic Indian recipes!
# Let's define the comprehensive recipe catalog matrix with full attributes.

ADDITIONAL_RECIPE_SPECS = [
    # Maharashtrian
    ("rec_matki_usal", "Matki Chi Usal (Spiced Moth Bean Stir Fry)", "Maharashtrian", ["Lunch", "Dinner", "Breakfast"], "Main Course", 10, 15, "Easy", "Vegetarian", True, False, True, (3, 2, 1, 4, 5), ["healthy", "protein", "traditional"], ["sprouted matki", "onion", "tomato", "goda masala", "mustard seed", "cumin seed", "curry leaf", "turmeric", "red chilli powder", "coconut", "jaggery", "coriander", "oil", "salt"], [], "Nutritious sprouted moth beans simmered in goda masala, coconut, and mild jaggery gravy."),
    ("rec_zunka", "Kandeshi Zunka (Dry Roasted Spicy Besan)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 5, 12, "Easy", "Vegetarian", True, False, True, (4, 1, 0, 5, 4), ["rustic", "quick", "monsoon"], ["besan", "onion", "garlic", "lasun", "green chilli", "mustard seed", "cumin seed", "turmeric", "oil", "coriander", "salt"], [], "Dry roasted garlicky chickpea flour dish with caramelized onions and green chillies."),
    ("rec_shev_bhaji", "Khandeshi Shev Bhaji (Spicy Sev Curry in Kala Masala)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 20, "Medium", "Vegetarian", True, False, False, (5, 2, 0, 5, 4), ["spicy", "dhabha-style", "comforting"], ["shev", "sev", "onion", "dry coconut", "ginger", "garlic", "kala masala", "goda masala", "red chilli powder", "oil", "salt", "coriander"], [], "Fiery Khandeshi curry made with deeply roasted coconut-onion kala masala topped with thick spicy gathiya sev."),
    ("rec_patodi_rassa", "Nagpuri Patodi Rassa (Spiced Besan Rolls in Fiery Red Curry)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 15, 25, "Hard", "Vegetarian", True, False, True, (5, 2, 0, 5, 4), ["spicy", "festive", "traditional"], ["besan", "onion", "ginger", "garlic", "dry coconut", "kala masala", "red chilli powder", "mustard seed", "oil", "salt", "coriander"], [], "Vidarbha delicacy of steamed and spiced besan rolls swimming in a fiery red coconut-onion rassa."),
    ("rec_dadpe_pohe", "Dadpe Pohe (Raw Pressed Seasoned Poha with Coconut)", "Maharashtrian", ["Breakfast", "Snack"], "Breakfast", 10, 5, "Easy", "Vegetarian", True, True, True, (2, 3, 2, 4, 5), ["quick", "no-cook", "cooling", "tea-time"], ["poha", "fresh coconut", "onion", "green chilli", "mustard seed", "curry leaf", "lemon juice", "sugar", "salt", "peanut", "oil", "coriander"], [], "Refreshing no-cook Maharashtrian breakfast of raw thin poha soaked in sweet coconut water and hot mustard tempering."),
    ("rec_aluvadi", "Aluvadi / Patra (Spiced Colocasia Leaf Pinwheels)", "Maharashtrian", ["Snack", "Tea-Time"], "Snack", 20, 20, "Hard", "Vegetarian", True, False, True, (3, 4, 3, 4, 4), ["crispy", "festive", "traditional"], ["colocasia leaves", "alu leaves", "besan", "tamarind", "jaggery", "sesame seed", "til", "red chilli powder", "turmeric", "ajwain", "oil", "salt"], [], "Steamed and crisp-fried colocasia leaf rolls smeared with spiced sweet-and-sour tamarind besan paste."),
    ("rec_sabudana_vada", "Crispy Sabudana Vada (Upwas / Fasting Fritters)", "Maharashtrian", ["Breakfast", "Snack", "Fast / Upwas"], "Snack", 10, 15, "Medium", "Vegetarian", True, True, True, (3, 2, 1, 4, 5), ["upwas", "crispy", "monsoon"], ["sabudana", "sago", "boiled potato", "peanut", "green chilli", "cumin seed", "lemon juice", "salt", "sugar", "oil"], ["boiled potatoes"], "Crispy golden exterior with fluffy chewy interior tapioca fritters blended with crushed peanuts and green chillies."),
    ("rec_jowar_bhakri", "Traditional Jowar Bhakri (Sorghum Unleavened Flatbread)", "Maharashtrian", ["Lunch", "Dinner"], "Bread", 10, 10, "Medium", "Vegetarian", True, True, True, (0, 0, 0, 3, 5), ["healthy", "gluten-free", "rustic"], ["jowar flour", "water", "salt"], [], "Ancient wholesome gluten-free flatbread hand-patted and roasted on hot iron griddle and direct flame."),
    ("rec_bajra_bhakri", "Winter Bajra Bhakri with Til (Pearl Millet Flatbread)", "Maharashtrian", ["Lunch", "Dinner"], "Bread", 10, 10, "Medium", "Vegetarian", True, True, True, (0, 0, 0, 3, 5), ["winter", "healthy", "rustic"], ["bajra flour", "sesame seed", "til", "water", "salt", "butter", "loni"], [], "Earthy rustic winter flatbread crusted with toasted sesame seeds and served with white homemade butter."),
    ("rec_puran_poli", "Royal Puran Poli (Sweet Chana Dal & Cardamom Stuffed Flatbread)", "Maharashtrian", ["Festival", "Dessert", "Lunch"], "Dessert / Main", 30, 30, "Hard", "Vegetarian", False, False, False, (0, 0, 5, 2, 5), ["festive", "traditional", "indulgent", "sweet"], ["chana dal", "jaggery", "gul", "cardamom", "nutmeg", "wheat flour", "maida", "ghee", "turmeric", "salt"], [], "Celebrated Maharashtrian festive flatbread delicately stuffed with sweet fragrant jaggery-chana dal filling and roasted in pure ghee."),
    ("rec_ukdiche_modak", "Ukdiche Modak (Steamed Rice Flour Dumplings with Sweet Coconut)", "Maharashtrian", ["Festival", "Dessert", "Snack"], "Dessert", 30, 20, "Hard", "Vegetarian", True, True, True, (0, 0, 5, 2, 5), ["festive", "ganpati", "traditional", "sweet"], ["rice flour", "fresh coconut", "jaggery", "gul", "cardamom", "nutmeg", "poppy seeds", "khus khus", "ghee", "milk"], [], "Sacred steamed rice flour dumplings filled with juicy grated coconut, molten organic jaggery, and fragrant cardamom."),
    ("rec_masale_bhaat", "Traditional Masale Bhaat (Maharashtrian Spiced Rice with Tondli)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 15, 20, "Medium", "Vegetarian", True, False, True, (3, 2, 1, 5, 5), ["festive", "traditional", "one-pot"], ["basmati rice", "ivy gourd", "tondli", "eggplant", "vangi", "green peas", "goda masala", "mustard seed", "cumin seed", "clove", "cinnamon", "cashews", "fresh coconut", "ghee", "salt"], [], "Fragrant Maharashtrian wedding-style spiced rice cooked with ivy gourd, green peas, Goda Masala, cashews, and fresh coconut."),
    ("rec_methi_chi_bhaji", "Sukhi Methi Chi Bhaji (Stir-Fried Fenugreek with Garlic & Peanuts)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 12, "Easy", "Vegetarian", True, False, True, (2, 0, 0, 4, 5), ["healthy", "quick", "iron-rich"], ["fresh methi", "fenugreek leaves", "garlic", "lasun", "green chilli", "crushed peanuts", "turmeric", "oil", "salt"], [], "Quick rustic dry sabzi of bitter-sweet fresh methi leaves sautéed with golden garlic cloves and crunchy peanuts."),
    ("rec_thecha", "Kolhapuri Mirchi Lasun Thecha (Coarsely Crushed Green Chilli Garlic Dip)", "Maharashtrian", ["Accompaniment", "Side Dish"], "Condiment", 5, 5, "Easy", "Vegetarian", True, False, True, (5, 1, 0, 4, 3), ["fiery", "spicy", "5-min"], ["green chilli", "garlic", "lasun", "cumin seed", "peanut", "oil", "salt", "lemon juice"], [], "Fiery traditional Maharashtrian chutney of pan-roasted green chillies, garlic, and cumin coarsely pounded in iron skillet."),
    ("rec_shengdana_chutney", "Solapuri Shengdana Chutney (Dry Peanut Garlic Chutney)", "Maharashtrian", ["Accompaniment", "Side Dish"], "Condiment", 5, 5, "Easy", "Vegetarian", True, False, True, (4, 1, 0, 4, 4), ["spicy", "staple", "storage"], ["peanuts", "garlic", "lasun", "kashmiri red chilli powder", "cumin seed", "salt", "oil"], [], "World-famous Solapuri dry red peanut garlic chutney that elevates every vada pav and bhakri."),
    ("rec_koshimbir", "Khamang Kakdi Koshimbir (Maharashtrian Cucumber Peanut Salad)", "Maharashtrian", ["Salad", "Side Dish"], "Salad", 10, 3, "Easy", "Vegetarian", True, False, True, (2, 3, 1, 3, 5), ["healthy", "cooling", "crunchy", "quick"], ["cucumber", "kakdi", "roasted peanuts", "fresh coconut", "green chilli", "mustard seed", "curry leaf", "lemon juice", "sugar", "salt", "coriander", "oil"], [], "Refreshing crunchy salad of diced cucumbers, roasted crushed peanuts, fresh coconut, and warm mustard-curry leaf tempering."),
    ("rec_batata_poha", "Batata Poha (Flattened Rice with Golden Sautéed Potatoes)", "Maharashtrian", ["Breakfast", "Snack"], "Breakfast", 10, 15, "Easy", "Vegetarian", True, False, True, (2, 2, 1, 4, 5), ["quick", "classic", "comforting"], ["poha", "potato", "batata", "onion", "mustard seed", "green chilli", "curry leaf", "turmeric", "peanut", "oil", "lemon juice", "coriander", "salt"], ["boiled potatoes"], "Comforting spiced poha loaded with crispy golden pan-fried potato cubes, peanuts, and lemon."),
    ("rec_pohe_bhaji", "Pohe Vangi Bhaji (Eggplant & Flattened Rice Savory Curry)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 15, "Easy", "Vegetarian", True, False, True, (3, 2, 0, 4, 4), ["traditional", "comforting"], ["poha", "eggplant", "vangi", "onion", "mustard seed", "goda masala", "turmeric", "green chilli", "oil", "salt", "coriander"], [], "Homestyle rustic Maharashtrian curry pairing tender eggplant slices with tempered flattened rice."),
    ("rec_chana_usal", "Kala Chana Usal (Maharashtrian Brown Chickpea Curry)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 15, 25, "Medium", "Vegetarian", True, False, True, (4, 2, 1, 5, 5), ["protein", "healthy", "traditional"], ["kala chana", "brown chickpeas", "onion", "dry coconut", "ginger", "garlic", "goda masala", "red chilli powder", "mustard seed", "curry leaf", "oil", "salt", "coriander"], [], "Protein-rich brown chickpeas cooked in a fragrant toasted coconut, ginger-garlic, and Goda Masala gravy."),
    ("rec_dudhi_bhaji", "Maharashtrian Dudhi Chi Bhaji (Bottle Gourd with Chana Dal)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 15, "Easy", "Vegetarian", True, False, True, (1, 1, 1, 4, 5), ["light", "healthy", "comforting"], ["bottle gourd", "dudhi", "lauki", "chana dal", "mustard seed", "cumin seed", "green chilli", "turmeric", "fresh coconut", "ghee", "oil", "salt", "coriander"], [], "Delicate, light homestyle bottle gourd curry cooked with soaked chana dal and fresh grated coconut."),
    ("rec_ghavan", "Konkani Ghavan (Instant Lacy Rice Flour Crepes)", "Maharashtrian", ["Breakfast", "Dinner"], "Bread", 5, 10, "Easy", "Vegetarian", True, True, True, (0, 0, 0, 3, 5), ["quick", "gluten-free", "light"], ["rice flour", "water", "salt", "oil"], [], "Soft, feather-light lacy coastal rice crepes made instantly without fermentation on hot cast iron pan."),
    ("rec_roti_ladoo", "Gul-Poli Ladoo / Malida (Nutritious Jaggery & Leftover Roti Ladoos)", "Maharashtrian", ["Snack", "Dessert"], "Dessert", 5, 3, "Easy", "Vegetarian", False, False, False, (0, 0, 5, 1, 5), ["zero-waste", "quick", "sweet", "healthy"], ["leftover roti", "chapati", "poli", "jaggery", "gul", "ghee", "cardamom", "almonds"], ["stale roti", "chapati", "poli"], "Wholesome 5-minute sweet ladoos made by pulsing torn leftover rotis with pure jaggery, warm ghee, and cardamom."),
    ("rec_roti_frankie", "Crispy Desi Roti Frankie (Spiced Potato & Chutney Roti Roll)", "Maharashtrian", ["Snack", "Dinner", "Quick Meal"], "Snack", 5, 10, "Easy", "Vegetarian", True, False, False, (3, 3, 1, 4, 4), ["zero-waste", "street-food", "quick"], ["leftover roti", "chapati", "boiled potato", "onion", "chaat masala", "green chutney", "butter", "salt"], ["stale roti", "chapati", "boiled potatoes"], "Crispy griddled leftover roti rolled around a spicy mashed potato filling with zingy green chutney and pickled onions."),
    ("rec_roti_noodles", "Desi Masala Roti Noodles (Spiraled Ribbon Stir-Fry)", "Maharashtrian", ["Breakfast", "Snack", "Quick Meal"], "Snack", 5, 10, "Easy", "Vegetarian", True, False, False, (3, 2, 1, 4, 4), ["zero-waste", "kids-friendly", "innovative"], ["leftover roti", "chapati", "onion", "capsicum", "carrot", "soy sauce", "chaat masala", "green chilli", "oil", "salt"], ["stale roti", "chapati"], "Stale rotis cut into noodle ribbons and stir-fried with crunchy bell peppers, onions, and spicy desi seasonings."),
    ("rec_rice_cutlet", "Crispy Leftover Rice & Potato Cutlets", "Maharashtrian", ["Snack", "Tea-Time"], "Snack", 10, 12, "Easy", "Vegetarian", True, False, True, (3, 2, 0, 4, 4), ["zero-waste", "crispy", "tea-time"], ["cooked rice", "bhaat", "boiled potato", "onion", "green chilli", "ginger", "garam masala", "chaat masala", "coriander", "oil", "salt"], ["cooked rice", "boiled potatoes"], "Golden shallow-fried patties made by mashing cold leftover rice with boiled potatoes, onions, and herbs."),
    ("rec_tawa_pulao", "Mumbai Street Tawa Pulao (Spiced Butter Veggie Rice)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 15, "Easy", "Vegetarian", False, False, True, (4, 3, 1, 5, 5), ["zero-waste", "street-food", "comforting"], ["cooked rice", "bhaat", "onion", "capsicum", "tomato", "green peas", "pav bhaji masala", "butter", "ginger", "garlic", "lemon juice", "coriander", "salt"], ["cooked rice"], "Fiery, buttery street-style rice stir-fried on iron tawa with Pav Bhaji masala, tomatoes, and peas."),
    ("rec_lemon_rice", "Chitranna (South & West Indian Tangy Lemon Peanut Rice)", "South Indian", ["Lunch", "Breakfast"], "Main Course", 5, 10, "Easy", "Vegetarian", True, False, True, (2, 4, 0, 3, 4), ["zero-waste", "tangy", "quick"], ["cooked rice", "bhaat", "lemon juice", "peanuts", "mustard seed", "chana dal", "urad dal", "turmeric", "green chilli", "curry leaf", "oil", "salt"], ["cooked rice"], "Bright yellow tangy rice tossed with crunchy peanuts, roasted lentils, curry leaves, and fresh lemon juice."),
    ("rec_rava_dhokla", "Instant Khatta Rava Dhokla (Steamed Semolina Cakes with Sour Curd)", "Gujarati", ["Breakfast", "Snack"], "Breakfast", 10, 15, "Easy", "Vegetarian", True, False, False, (2, 4, 1, 4, 5), ["zero-waste", "steamed", "healthy"], ["sour curd", "dahi", "semolina", "rava", "sooji", "green chilli", "ginger", "eno", "baking soda", "mustard seed", "sesame seed", "curry leaf", "oil", "salt"], ["sour curd", "dahi"], "Soft spongy steamed savory cakes made instantly using fermented sour curd and semolina."),
    ("rec_bread_pakora", "Street Style Bread Pakora (Stuffed Besan Fried Triangles)", "North Indian", ["Snack", "Tea-Time"], "Snack", 10, 15, "Medium", "Vegetarian", True, False, False, (3, 2, 0, 4, 5), ["zero-waste", "crispy", "monsoon"], ["leftover bread", "bread", "boiled potato", "besan", "ajwain", "green chilli", "turmeric", "chaat masala", "oil", "salt"], ["leftover bread", "boiled potatoes"], "Classic tea-time fried snack of bread triangles stuffed with spiced potato mash and coated in crisp ajwain besan batter."),
    ("rec_sabzi_paratha", "Stuffed Leftover Sabzi Paratha", "North Indian", ["Breakfast", "Lunch"], "Bread", 10, 12, "Easy", "Vegetarian", False, False, False, (3, 2, 0, 4, 5), ["zero-waste", "comforting", "quick"], ["leftover sabzi", "wheat flour", "atta", "ajwain", "onion", "amchur", "coriander", "ghee", "salt"], ["leftover sabzi"], "Flaky golden parathas stuffed with mashed leftover dry spiced vegetables."),
    ("rec_veg_toast_sandwich", "Mumbai Masala Toast Sandwich", "Maharashtrian", ["Snack", "Breakfast"], "Snack", 5, 10, "Easy", "Vegetarian", False, False, False, (3, 3, 1, 4, 4), ["zero-waste", "street-food", "quick"], ["bread", "boiled potato", "onion", "tomato", "capsicum", "butter", "green chutney", "chaat masala", "cheese"], ["leftover bread", "boiled potatoes"], "Crispy grilled street sandwich layered with spicy mint chutney, butter, spiced potato masala, and vegetables."),
    ("rec_dal_khichdi", "Dhabha Style Tadka Dal Khichdi", "North Indian", ["Dinner", "Lunch"], "Main Course", 5, 12, "Easy", "Vegetarian", False, False, True, (2, 1, 0, 5, 5), ["zero-waste", "comforting", "soothing"], ["leftover dal", "dal", "cooked rice", "bhaat", "garlic", "onion", "tomato", "cumin seed", "ghee", "kashmiri red chilli powder", "salt", "coriander"], ["leftover dal", "cooked rice"], "Ultimate soothing meal combining leftover dal and rice topped with a double sizzling garlic-ghee phodni."),
    ("rec_sukhi_batata_bhaji", "Sukhi Batata Bhaji (Puri-Bhaji Yellow Potato Sabzi)", "Maharashtrian", ["Breakfast", "Lunch"], "Main Course", 5, 10, "Easy", "Vegetarian", True, False, True, (2, 2, 1, 4, 5), ["quick", "classic", "comforting"], ["boiled potato", "batata", "onion", "green chilli", "mustard seed", "curry leaf", "turmeric", "fresh coconut", "lemon juice", "oil", "salt", "coriander"], ["boiled potatoes"], "Classic mild golden potato sabzi cooked with mustard seeds, green chillies, curry leaves, and lemon."),
    ("rec_aloo_tikki", "Crispy Chaat Aloo Tikki", "North Indian", ["Snack", "Tea-Time"], "Snack", 10, 12, "Easy", "Vegetarian", True, True, True, (3, 2, 0, 4, 4), ["crispy", "chaat", "tea-time"], ["boiled potato", "cornflour", "rice flour", "roasted cumin", "chaat masala", "green chilli", "ginger", "coriander", "oil", "salt"], ["boiled potatoes"], "Crackling crispy shallow-fried potato patties seasoned with roasted cumin and chaat masala."),
    
    # North Indian Classics (25 recipes)
    ("rec_paneer_butter_masala", "Restaurant Style Paneer Butter Masala", "North Indian", ["Lunch", "Dinner"], "Main Course", 15, 20, "Medium", "Vegetarian", False, False, True, (2, 3, 3, 5, 5), ["rich", "indulgent", "weekend", "restaurant"], ["paneer", "butter", "cream", "tomato", "onion", "cashews", "ginger", "garlic", "kasuri methi", "garam masala", "kashmiri red chilli powder", "salt"], [], "Velvety, rich tomato and cashew gravy with tender cubes of paneer finished with butter and kasuri methi."),
    ("rec_palak_paneer", "Homestyle Palak Paneer (Cottage Cheese in Spiced Spinach Gravy)", "North Indian", ["Lunch", "Dinner"], "Main Course", 15, 20, "Medium", "Vegetarian", False, False, True, (2, 1, 1, 4, 5), ["healthy", "protein", "classic"], ["spinach", "palak", "paneer", "onion", "tomato", "ginger", "garlic", "green chilli", "cumin seed", "garam masala", "cream", "butter", "salt"], [], "Silky, vibrant green spinach gravy delicately spiced and dotted with soft paneer cubes."),
    ("rec_rajma_masala", "Punjabi Rajma Masala (Red Kidney Beans in Thick Onion-Tomato Gravy)", "North Indian", ["Lunch", "Dinner"], "Main Course", 15, 30, "Medium", "Vegetarian", True, False, True, (3, 2, 1, 5, 5), ["comforting", "protein", "sunday-special"], ["rajma", "kidney beans", "onion", "tomato", "ginger", "garlic", "cumin seed", "coriander powder", "garam masala", "kashmiri red chilli powder", "ghee", "oil", "salt", "coriander"], [], "Iconic Punjabi slow-cooked kidney beans in rich, spiced tomato-onion masala, best served with steaming Chawal."),
    ("rec_chole_masala", "Amritsari Chole Masala (Dark Spiced Chickpea Curry)", "North Indian", ["Lunch", "Dinner"], "Main Course", 15, 30, "Medium", "Vegetarian", True, False, True, (4, 3, 1, 5, 5), ["spicy", "street-food", "weekend", "protein"], ["kabuli chana", "white chickpeas", "tea bag", "onion", "tomato", "ginger", "garlic", "chole masala", "anardana", "amchur", "bay leaf", "cinnamon", "ghee", "oil", "salt"], [], "Authentic dark Amritsari chickpeas infused with tea liquor, dried pomegranate seeds, and aromatic whole spices."),
    ("rec_dal_makhani", "Dhabha Style Dal Makhani (Slow Cooked Black Lentils in Butter)", "North Indian", ["Dinner", "Lunch"], "Main Course", 15, 45, "Hard", "Vegetarian", False, False, True, (2, 2, 2, 5, 5), ["indulgent", "rich", "party"], ["urad dal whole", "black gram", "rajma", "butter", "cream", "tomato puree", "ginger-garlic paste", "kashmiri red chilli powder", "kasuri methi", "garam masala", "salt"], [], "Creamy, slow-simmered black lentils and kidney beans enriched with pure butter, cream, and smoky kasuri methi."),
    ("rec_dal_tadka", "Restaurant Style Yellow Dal Tadka (Ghee-Hing Phodni)", "North Indian", ["Lunch", "Dinner"], "Main Course", 10, 20, "Easy", "Vegetarian", False, False, True, (3, 2, 0, 4, 5), ["comforting", "staple", "quick"], ["toor dal", "yellow lentils", "onion", "tomato", "ginger", "garlic", "cumin seed", "mustard seed", "dry red chilli", "hing", "kashmiri red chilli powder", "ghee", "salt", "coriander"], [], "Silky yellow toor dal topped with a smoking hot tempering of pure ghee, garlic, cumin, and dry red chillies."),
    ("rec_aloo_gobi", "Dhabha Style Aloo Gobi Masala (Spiced Potato & Cauliflower)", "North Indian", ["Lunch", "Dinner"], "Main Course", 10, 20, "Easy", "Vegetarian", True, False, True, (3, 2, 1, 4, 4), ["classic", "homestyle", "comforting"], ["potato", "aloo", "cauliflower", "gobi", "onion", "tomato", "ginger", "green chilli", "cumin seed", "turmeric", "coriander powder", "garam masala", "oil", "salt", "coriander"], [], "Dry roasted spiced cauliflower florets and tender potato wedges with ginger juliennes and fresh coriander."),
    ("rec_aloo_paratha", "Crispy Punjabi Aloo Paratha with Makhan", "North Indian", ["Breakfast", "Lunch"], "Main Course", 15, 15, "Medium", "Vegetarian", False, False, False, (3, 2, 0, 4, 5), ["indulgent", "breakfast", "comforting"], ["boiled potato", "aloo", "wheat flour", "atta", "onion", "green chilli", "ginger", "ajwain", "amchur", "garam masala", "butter", "ghee", "salt", "coriander"], ["boiled potatoes"], "Tandoori-style whole wheat paratha overflowing with spicy mashed potato filling, served with a big dollop of white butter."),
    ("rec_gobi_paratha", "Spiced Grated Gobi Paratha", "North Indian", ["Breakfast", "Lunch"], "Main Course", 15, 15, "Medium", "Vegetarian", False, False, False, (3, 2, 0, 4, 4), ["breakfast", "winter", "comforting"], ["cauliflower", "gobi", "wheat flour", "atta", "green chilli", "ginger", "ajwain", "garam masala", "amchur", "ghee", "salt", "coriander"], [], "Whole wheat parathas stuffed with fresh finely grated spiced cauliflower, ginger, and ajwain."),
    ("rec_paneer_bhurji", "Dhabha Style Paneer Bhurji (Scrambled Spiced Paneer)", "North Indian", ["Breakfast", "Dinner", "Quick Meal"], "Main Course", 10, 10, "Easy", "Vegetarian", False, False, True, (3, 2, 1, 4, 4), ["quick", "protein", "15-min"], ["paneer", "onion", "tomato", "capsicum", "green chilli", "ginger", "garlic", "turmeric", "pav bhaji masala", "kasuri methi", "butter", "oil", "salt", "coriander"], [], "Scrambled soft fresh paneer cooked in a high-flame onion-tomato-capsicum masala with butter and pav bhaji masala."),
    ("rec_kadai_paneer", "Restaurant Style Kadai Paneer with Bell Peppers", "North Indian", ["Lunch", "Dinner"], "Main Course", 15, 20, "Medium", "Vegetarian", False, False, True, (4, 3, 1, 5, 4), ["spicy", "restaurant", "crunchy"], ["paneer", "capsicum", "bell pepper", "onion", "tomato", "coriander seeds", "dry red chilli", "ginger", "garlic", "kasuri methi", "garam masala", "oil", "butter", "salt"], [], "Cottage cheese cubes and crunchy bell peppers tossed in a freshly ground roasted kadai spice blend."),
    ("rec_jeera_rice", "Fragrant Restaurant Style Jeera Rice", "North Indian", ["Lunch", "Dinner"], "Main Course", 5, 15, "Easy", "Vegetarian", False, False, True, (1, 0, 0, 3, 5), ["quick", "staple", "aromatic"], ["basmati rice", "cumin seed", "jeera", "ghee", "bay leaf", "clove", "cinnamon", "salt", "coriander"], [], "Fluffy long-grain basmati rice scented with roasted cumin seeds, whole spices, and pure ghee."),
    ("rec_matar_paneer", "Homestyle Matar Paneer (Cottage Cheese & Sweet Peas Curry)", "North Indian", ["Lunch", "Dinner"], "Main Course", 10, 20, "Easy", "Vegetarian", False, False, True, (3, 2, 2, 4, 5), ["classic", "homestyle", "comforting"], ["paneer", "green peas", "matar", "onion", "tomato", "ginger", "garlic", "cashews", "garam masala", "turmeric", "cream", "oil", "salt", "coriander"], [], "Classic comforting curry of paneer and sweet green peas simmered in a mildly spiced onion-tomato-cashew gravy."),
    ("rec_baingan_bharta", "Punjabi Smoked Baingan Bharta (Charred Eggplant Mash)", "North Indian", ["Lunch", "Dinner"], "Main Course", 15, 20, "Medium", "Vegetarian", True, False, True, (3, 2, 1, 4, 5), ["smoky", "rustic", "comforting"], ["large eggplant", "baingan", "onion", "tomato", "green peas", "ginger", "garlic", "green chilli", "mustard oil", "coriander powder", "garam masala", "salt", "coriander"], [], "Direct-fire charred eggplant mashed and sautéed with pungent mustard oil, garlic, green chillies, and juicy tomatoes."),
    ("rec_dum_aloo", "Kashmiri / Punjabi Dum Aloo (Slow Cooked Baby Potatoes in Spiced Gravy)", "North Indian", ["Lunch", "Dinner"], "Main Course", 15, 25, "Medium", "Vegetarian", False, False, True, (3, 3, 1, 4, 5), ["rich", "festive", "comforting"], ["baby potatoes", "curd", "dahi", "onion", "tomato", "cashews", "ginger", "fennel seeds", "saunf", "kashmiri red chilli powder", "garam masala", "oil", "salt", "coriander"], [], "Crisp-fried baby potatoes simmered on 'dum' in a luscious aromatic yogurt and fennel-spiced red gravy."),
    ("rec_bhindi_masala", "Crispy Bhindi Masala (Spiced Okra Stir Fry)", "North Indian", ["Lunch", "Dinner"], "Main Course", 10, 15, "Easy", "Vegetarian", True, False, True, (3, 3, 0, 4, 4), ["quick", "dry-sabzi", "classic"], ["okra", "bhindi", "onion", "tomato", "green chilli", "cumin seed", "amchur", "dry mango powder", "turmeric", "coriander powder", "red chilli powder", "oil", "salt"], [], "Crispy non-sticky tender okra sautéed with sliced onions, tangy dry mango powder, and toasted spices."),
    ("rec_veg_biryani", "Dum Hyderabadi Veg Biryani (Layered Fragrant Spiced Rice)", "North Indian", ["Lunch", "Dinner"], "Main Course", 25, 35, "Hard", "Vegetarian", False, False, True, (4, 2, 1, 5, 5), ["festive", "royal", "party", "weekend"], ["basmati rice", "mixed vegetables", "carrot", "beans", "potato", "paneer", "curd", "dahi", "biryani masala", "fried onions", "birista", "saffron", "mint leaves", "coriander", "ghee", "salt"], [], "Royal slow-cooked dum biryani layering saffron-infused basmati rice, caramelized crispy onions, mint, and marinated spiced vegetables."),
    ("rec_shahi_paneer", "Mughlai Shahi Paneer (Paneer in White Cashew Saffron Gravy)", "North Indian", ["Dinner", "Lunch"], "Main Course", 15, 20, "Medium", "Vegetarian", False, False, True, (1, 1, 4, 4, 5), ["royal", "mild", "party", "sweet"], ["paneer", "cashews", "almonds", "cream", "curd", "onion", "ginger", "green cardamom", "saffron", "kasuri methi", "butter", "ghee", "salt"], [], "Luxurious royal Mughlai gravy crafted from ground cashews, almonds, saffron, and cream with velvety paneer cubes."),
    ("rec_kadhi_pakora", "Punjabi Kadhi Pakora (Spiced Onion Fritters in Sour Yogurt Curry)", "North Indian", ["Lunch", "Dinner"], "Main Course", 15, 30, "Medium", "Vegetarian", False, False, True, (3, 4, 0, 5, 5), ["comforting", "classic", "monsoon"], ["sour curd", "dahi", "besan", "onion", "ajwain", "fenugreek seeds", "methi dana", "coriander seeds", "dry red chilli", "turmeric", "mustard oil", "salt"], ["sour curd", "dahi"], "Golden crispy onion fritters floating in a thick, tangy, slow-simmered besan and yogurt gravy tempered with fenugreek seeds."),
    ("rec_dahi_vada", "Soft Dahi Vada / Dahi Bhalla (Lentil Dumplings in Sweet Spiced Yogurt)", "North Indian", ["Snack", "Festival", "Appetizer"], "Snack", 20, 20, "Medium", "Vegetarian", False, False, True, (2, 3, 4, 4, 5), ["cooling", "festive", "chaat", "party"], ["urad dal", "thick curd", "dahi", "tamarind chutney", "mint green chutney", "roasted cumin powder", "chaat masala", "kashmiri red chilli powder", "oil", "salt"], [], "Melt-in-the-mouth soaked urad dal dumplings smothered in chilled sweetened creamy curd, sweet tamarind and spicy mint chutneys."),

    # South Indian Classics (15 recipes)
    ("rec_tiffin_sambar", "Hotel Style Tiffin Sambar (Spiced Lentil Vegetable Stew)", "South Indian", ["Breakfast", "Lunch", "Dinner"], "Soup / Curry", 15, 25, "Medium", "Vegetarian", True, False, True, (3, 4, 1, 5, 5), ["traditional", "tiffin", "healthy"], ["toor dal", "drumstick", "shallots", "sambhar onions", "tomato", "tamarind", "sambar powder", "mustard seed", "fenugreek seeds", "curry leaf", "hing", "oil", "salt", "coriander"], [], "Aromatic South Indian stew of toor dal, drumsticks, and shallots simmered in tangy tamarind and freshly roasted sambar spices."),
    ("rec_tomato_rasam", "Spicy Pepper Tomato Rasam (Soothing Herbal Broth)", "South Indian", ["Lunch", "Dinner"], "Soup / Broth", 5, 15, "Easy", "Vegetarian", True, False, True, (4, 4, 0, 4, 5), ["healing", "soothing", "quick", "monsoon"], ["tomatoes", "tamarind", "black pepper", "cumin seed", "garlic", "mustard seed", "curry leaf", "hing", "turmeric", "ghee", "oil", "salt", "coriander"], [], "Zesty, peppery, garlic-infused tomato broth that rejuvenates the soul, relieves colds, and aids digestion."),
    ("rec_coconut_chutney", "Hotel Style White Coconut Chutney", "South Indian", ["Breakfast", "Accompaniment"], "Condiment", 5, 3, "Easy", "Vegetarian", True, False, True, (2, 1, 1, 3, 5), ["quick", "staple", "5-min"], ["fresh coconut", "roasted chana dal", "dalia", "green chilli", "ginger", "mustard seed", "urad dal", "curry leaf", "hing", "oil", "salt"], [], "Creamy ground fresh coconut and roasted chana dal dip with a crackling mustard and curry leaf tempering."),
    ("rec_tomato_rice", "Thakkali Sadam (Spicy South Indian Tomato Rice)", "South Indian", ["Lunch", "Dinner", "Quick Meal"], "Main Course", 10, 15, "Easy", "Vegetarian", True, False, True, (3, 4, 1, 4, 4), ["lunchbox", "tangy", "quick"], ["cooked rice", "rice", "tomatoes", "onion", "mustard seed", "chana dal", "urad dal", "curry leaf", "sambar powder", "green chilli", "ginger", "oil", "salt"], ["cooked rice"], "Zesty lunchbox favorite of cooked rice tossed in an onion-tomato paste spiced with sambar masala and crunchy lentils."),
    ("rec_bisi_bele_bath", "Authentic Karnataka Bisi Bele Bath (Spiced Lentil Rice with Veggies)", "South Indian", ["Lunch", "Dinner"], "Main Course", 15, 25, "Medium", "Vegetarian", False, False, True, (4, 3, 1, 5, 5), ["comforting", "one-pot", "traditional"], ["rice", "toor dal", "mixed vegetables", "beans", "carrot", "shallots", "tamarind", "jaggery", "bisi bele bath powder", "mustard seed", "cashews", "curry leaf", "ghee", "salt"], [], "Hearty Karnataka specialty combining rice, lentils, and garden vegetables simmered with tamarind, jaggery, and house-ground Bisi Bele Bath masala in pure ghee."),
    ("rec_medu_vada", "Crispy Hotel Style Medu Vada (Golden Black Gram Fritters)", "South Indian", ["Breakfast", "Snack"], "Breakfast", 15, 15, "Medium", "Vegetarian", True, False, True, (2, 0, 0, 4, 5), ["crispy", "tiffin", "traditional"], ["urad dal", "black pepper", "cumin seed", "ginger", "green chilli", "curry leaf", "fresh coconut bits", "hing", "oil", "salt"], [], "Donut-shaped fluffy fritters with crackling crispy crust and pillowy center, seasoned with black pepper, ginger, and curry leaves."),
    ("rec_rava_upma", "Classic Vegetable Rava Upma (Roasted Semolina Breakfast)", "South Indian", ["Breakfast", "Quick Meal"], "Breakfast", 5, 12, "Easy", "Vegetarian", False, False, False, (2, 1, 0, 3, 5), ["quick", "healthy", "staple"], ["semolina", "rava", "sooji", "onion", "green peas", "carrot", "green chilli", "ginger", "mustard seed", "urad dal", "chana dal", "curry leaf", "ghee", "oil", "salt", "coriander"], [], "Fluffy toasted semolina cooked with sautéed vegetables, crunchy lentils, ginger, and aromatic ghee."),
    ("rec_veg_kurma", "South Indian Hotel Veg Kurma (Coconut & Fennel Spiced Gravy)", "South Indian", ["Dinner", "Lunch"], "Main Course", 15, 20, "Medium", "Vegetarian", True, False, True, (3, 1, 1, 5, 5), ["aromatic", "restaurant", "tiffin"], ["mixed vegetables", "potato", "carrot", "beans", "peas", "fresh coconut", "cashews", "fennel seeds", "saunf", "poppy seeds", "cinnamon", "cloves", "onion", "tomato", "ginger", "garlic", "oil", "salt"], [], "Fragrant South Indian curry made with fresh coconut, cashews, fennel seeds, and whole spices, perfect for Parotta or Poori."),
    ("rec_puliyodharai", "Temple Style Puliyodharai (Tamarind Rice with Roasted Spices)", "South Indian", ["Lunch", "Dinner"], "Main Course", 15, 20, "Medium", "Vegetarian", True, False, True, (3, 5, 1, 4, 4), ["tangy", "temple-style", "travel-food"], ["cooked rice", "rice", "tamarind pulp", "peanuts", "sesame oil", "mustard seed", "chana dal", "urad dal", "fenugreek seeds", "dry red chilli", "turmeric", "hing", "curry leaf", "salt"], ["cooked rice"], "Traditional temple-style tamarind rice packed with intense tanginess, nutty peanuts, toasted fenugreek, and sesame oil."),

    # Gujarati & Regional Classics (15 recipes)
    ("rec_khaman_dhokla", "Nylon Khaman Dhokla (Soft Spongy Steamed Besan Cakes)", "Gujarati", ["Breakfast", "Snack"], "Breakfast", 10, 20, "Medium", "Vegetarian", True, True, True, (2, 4, 4, 4, 5), ["steamed", "spongy", "healthy", "party"], ["besan", "gram flour", "citric acid", "lemon juice", "sugar", "turmeric", "eno", "fruit salt", "mustard seed", "green chilli", "curry leaf", "fresh coconut", "oil", "salt"], [], "Juicy, fluffy, melt-in-mouth steamed besan sponge soaked in a sweet-and-tangy mustard and green chilli tempering."),
    ("rec_gujarati_kadhi", "Authentic Sweet Gujarati Kadhi (White Curd & Jaggery Stew)", "Gujarati", ["Lunch", "Dinner"], "Soup / Curry", 5, 12, "Easy", "Vegetarian", False, False, True, (2, 3, 4, 4, 5), ["sweet-tangy", "soothing", "quick"], ["curd", "dahi", "besan", "jaggery", "gul", "cinnamon", "clove", "mustard seed", "cumin seed", "fenugreek seeds", "ginger", "green chilli", "curry leaf", "ghee", "salt", "coriander"], ["sour curd", "curd"], "Silky, sweet-and-sour white yogurt soup spiced with cinnamon, cloves, ginger, green chillies, and organic jaggery in pure ghee."),
    ("rec_sev_tameta", "Kathiyawadi Sev Tameta Nu Shaak (Sweet Tangy Tomato & Sev Curry)", "Gujarati", ["Lunch", "Dinner", "Quick Meal"], "Main Course", 5, 10, "Easy", "Vegetarian", True, True, False, (3, 4, 3, 4, 4), ["quick", "kathiyawadi", "10-min"], ["tomatoes", "shev", "sev", "gathiya", "jaggery", "ginger", "green chilli", "mustard seed", "cumin seed", "turmeric", "red chilli powder", "hing", "oil", "salt", "coriander"], [], "Famous Kathiyawadi 10-minute curry of ripe juicy tomatoes simmered with jaggery and topped with crispy sev."),
    ("rec_methi_thepla", "Gujarati Methi Thepla (Spiced Fenugreek Flatbread)", "Gujarati", ["Breakfast", "Travel", "Dinner"], "Bread", 10, 10, "Easy", "Vegetarian", True, False, False, (2, 1, 0, 4, 5), ["healthy", "travel-food", "staple"], ["wheat flour", "atta", "fresh methi", "fenugreek leaves", "besan", "curd", "dahi", "turmeric", "red chilli powder", "ajwain", "sesame seed", "til", "oil", "salt"], [], "Soft spiced whole wheat flatbreads kneaded with fresh bitter-sweet fenugreek leaves, sesame seeds, and yogurt."),
    ("rec_handvo", "Gujarati Vegetable Handvo (Savory Lentil & Bottle Gourd Cake)", "Gujarati", ["Breakfast", "Snack", "Dinner"], "Snack", 15, 25, "Medium", "Vegetarian", True, False, True, (2, 2, 1, 4, 5), ["healthy", "crispy", "traditional"], ["rice", "chana dal", "toor dal", "urad dal", "bottle gourd", "dudhi", "sour curd", "mustard seed", "sesame seed", "green chilli", "ginger", "eno", "oil", "salt"], ["sour curd"], "Golden, crispy-crusted savory baked lentil cake packed with grated bottle gourd, sesame seeds, and aromatic tempering."),
    ("rec_moong_cheela", "High-Protein Moong Dal Cheela (Crispy Savory Lentil Crepes)", "North Indian", ["Breakfast", "Dinner", "Quick Meal"], "Breakfast", 10, 10, "Easy", "Vegetarian", True, False, True, (2, 1, 0, 3, 5), ["protein", "healthy", "quick"], ["sprouted moong", "moong dal", "ginger", "green chilli", "cumin seed", "hing", "onion", "paneer", "coriander", "oil", "salt"], [], "Nutrient-dense crispy green moong dal crepes stuffed with spiced crumbled paneer and chopped onions."),
    ("rec_poha_cutlet", "Crispy Poha & Vegetable Cutlets", "North Indian", ["Snack", "Tea-Time"], "Snack", 10, 12, "Easy", "Vegetarian", True, False, True, (3, 2, 0, 4, 4), ["crispy", "tea-time", "quick"], ["poha", "boiled potato", "carrot", "green peas", "onion", "ginger", "green chilli", "chaat masala", "oil", "salt", "coriander"], ["boiled potatoes"], "Pan-crisped patties made from softened poha, mashed potatoes, and diced vegetables."),
    ("rec_shahi_tukda", "Hyderabadi Shahi Tukda (Royal Ghee-Fried Bread in Saffron Rabdi)", "North Indian", ["Dessert", "Festival"], "Dessert", 15, 15, "Medium", "Vegetarian", False, False, False, (0, 0, 5, 2, 5), ["zero-waste", "royal", "sweet", "festive"], ["leftover bread", "bread", "milk", "sugar", "saffron", "cardamom", "cashews", "almonds", "pistachios", "ghee"], ["leftover bread", "bread"], "Royal dessert of crisp ghee-fried bread triangles soaked in fragrant sugar syrup and topped with thick saffron-pistachio rabdi."),
    ("rec_aloo_puri", "Delhi Style Bedmi Aloo Puri (Spiced Potato Curry with Puffed Puris)", "North Indian", ["Breakfast", "Lunch"], "Main Course", 15, 20, "Medium", "Vegetarian", True, False, False, (4, 3, 0, 5, 5), ["street-food", "weekend", "comforting"], ["potato", "aloo", "tomato", "wheat flour", "urad dal", "ginger", "kasuri methi", "fennel seeds", "amchur", "garam masala", "oil", "salt"], ["boiled potatoes"], "Halwai-style tangy spicy potato gravy served with crispy, puffed urad dal stuffed Bedmi puris."),
    ("rec_soya_bhurji", "High-Protein Soya Keema Bhurji", "North Indian", ["Breakfast", "Dinner", "Quick Meal"], "Main Course", 10, 12, "Easy", "Vegetarian", True, False, True, (3, 2, 0, 4, 4), ["high-protein", "vegan", "quick"], ["soya granules", "soya chunks", "onion", "tomato", "capsicum", "green peas", "ginger", "garlic", "pav bhaji masala", "turmeric", "oil", "salt", "coriander"], [], "High-protein vegan scrambled mince made from tender soya granules tossed in a fiery Mumbai-style masala."),
    
    # 45 More Maharashtrian & Regional Specialties to reach 105+
    ("rec_veg_tambda_rassa", "Kolhapuri Veg Tambda Rassa (Fiery Red Spiced Broth)", "Maharashtrian", ["Lunch", "Dinner"], "Soup / Curry", 15, 20, "Medium", "Vegetarian", True, False, True, (5, 2, 0, 5, 4), ["fiery", "kolhapuri", "spicy", "iconic"], ["onion", "dry coconut", "ginger", "garlic", "kolhapuri masala", "kashmiri red chilli powder", "cloves", "cinnamon", "bay leaf", "oil", "salt", "coriander"], [], "Iconic fiery red Kolhapuri broth bursting with bold roasted spices, onion-coconut paste, and red chillies."),
    ("rec_pandhra_rassa", "Kolhapuri Pandhra Rassa (Delicate Coconut Milk & Cashew White Broth)", "Maharashtrian", ["Lunch", "Dinner"], "Soup / Curry", 15, 20, "Medium", "Vegetarian", True, False, True, (2, 1, 1, 4, 5), ["soothing", "rich", "kolhapuri", "royal"], ["fresh coconut", "coconut milk", "cashews", "poppy seeds", "khus khus", "ginger", "garlic", "green chilli", "cinnamon", "clove", "cardamom", "ghee", "salt"], [], "Fragrant, aromatic white broth crafted from fresh coconut milk, cashew paste, and warm whole spices."),
    ("rec_kanda_batata_rassa", "Maharashtrian Kanda Batata Rassa (Homestyle Onion-Potato Curry)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 15, "Easy", "Vegetarian", True, False, True, (3, 2, 0, 4, 5), ["quick", "homestyle", "comforting"], ["potato", "batata", "onion", "ginger", "garlic", "goda masala", "turmeric", "red chilli powder", "mustard seed", "curry leaf", "oil", "salt", "coriander"], [], "Simple everyday Maharashtrian curry of diced potatoes and onions simmered in Goda Masala gravy."),
    ("rec_flower_batata_rassa", "Flower Batata Rassa (Cauliflower & Potato Maharashtrian Curry)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 15, "Easy", "Vegetarian", True, False, True, (3, 2, 1, 4, 5), ["homestyle", "classic"], ["cauliflower", "potato", "onion", "tomato", "goda masala", "roasted peanut powder", "mustard seed", "turmeric", "oil", "salt", "coriander"], [], "Cauliflower florets and tender potatoes simmered in a mildly sweet and spicy peanut-goda masala gravy."),
    ("rec_patal_bhaji", "Maharashtrian Patal Bhaji (Spinach & Chana Dal Gravy with Peanuts)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 20, "Easy", "Vegetarian", True, False, True, (2, 3, 2, 4, 5), ["healthy", "iron-rich", "traditional"], ["spinach", "palak", "chana dal", "peanuts", "tamarind", "jaggery", "besan", "goda masala", "mustard seed", "hing", "green chilli", "oil", "salt"], [], "Nutritious silky spinach curry cooked with soaked chana dal, whole peanuts, jaggery, and tamarind."),
    ("rec_tomato_saar", "Maharashtrian Tomato Saar (Coconut-Infused Tangy Tomato Soup)", "Maharashtrian", ["Lunch", "Dinner"], "Soup", 5, 12, "Easy", "Vegetarian", True, False, True, (2, 4, 2, 4, 5), ["tangy", "soothing", "comforting"], ["tomatoes", "fresh coconut", "cumin seed", "garlic", "green chilli", "mustard seed", "curry leaf", "hing", "jaggery", "ghee", "salt", "coriander"], [], "Tangy and soothing coastal Maharashtrian tomato broth blended with fresh coconut and tempered with cumin and ghee."),
    ("rec_valache_birde", "Valache Birde (Sprouted Field Beans Coconut Curry)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 15, 25, "Hard", "Vegetarian", True, False, True, (3, 3, 2, 5, 5), ["traditional", "festive", "coastal"], ["sprouted val", "field beans", "onion", "fresh coconut", "goda masala", "jaggery", "kokum", "tamarind", "mustard seed", "hing", "oil", "salt", "coriander"], [], "Traditional CKP / Konkani delicacy of delicate sprouted field beans in a sweet, sour, and spicy coconut gravy."),
    ("rec_chawli_usal", "Chawli Chi Usal (Black-Eyed Peas Maharashtrian Curry)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 20, "Easy", "Vegetarian", True, False, True, (3, 2, 1, 4, 5), ["protein", "homestyle", "comforting"], ["black eyed peas", "chawli", "onion", "tomato", "ginger", "garlic", "goda masala", "turmeric", "red chilli powder", "mustard seed", "oil", "salt", "coriander"], [], "Homestyle protein-packed black eyed peas simmered in a spiced onion-tomato and Goda Masala curry."),
    ("rec_batata_saung", "Konkani Batata Saung (Spicy Tangy Onion & Potato Roast)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 10, 15, "Easy", "Vegetarian", True, False, True, (4, 4, 0, 4, 5), ["konkani", "spicy", "tangy"], ["boiled potato", "onion", "tamarind", "kashmiri red chilli powder", "coriander seeds", "mustard seed", "coconut oil", "salt"], ["boiled potatoes"], "Zesty Konkani specialty featuring boiled potatoes smothered in deeply caramelized onions, tamarind, and roasted red chillies in coconut oil."),
    ("rec_dhapate", "Maharashtrian Dhapate (Spiced Roasted Flatbread with Garlic)", "Maharashtrian", ["Breakfast", "Dinner"], "Bread", 10, 12, "Medium", "Vegetarian", True, False, False, (3, 1, 0, 4, 5), ["rustic", "healthy", "traditional"], ["jowar flour", "wheat flour", "besan", "onion", "garlic", "green chilli", "coriander", "ajwain", "sesame seed", "oil", "salt"], [], "Rustic multi-flour spiced roasted flatbread from Marathwada packed with garlic and fresh herbs."),
    ("rec_kurdai_bhaji", "Kurdai Chi Bhaji (Stir-Fried Spiced Wheat Noodles)", "Maharashtrian", ["Breakfast", "Snack", "Quick Meal"], "Snack", 5, 8, "Easy", "Vegetarian", True, False, False, (3, 2, 0, 4, 4), ["quick", "nostalgic", "10-min"], ["kurdai", "wheat noodles", "onion", "mustard seed", "green chilli", "curry leaf", "turmeric", "peanut", "oil", "lemon juice", "salt", "coriander"], [], "Ingenious Maharashtrian quick breakfast made by soaking and tempering traditional sun-dried fermented wheat kurdai."),
    ("rec_sandge_bhaji", "Maharashtrian Sandge Chi Bhaji (Sun-Dried Moong Dumpling Curry)", "Maharashtrian", ["Lunch", "Dinner"], "Main Course", 5, 15, "Easy", "Vegetarian", True, False, True, (4, 2, 0, 5, 4), ["traditional", "rustic", "monsoon"], ["sandge", "moong vadi", "onion", "garlic", "kala masala", "goda masala", "red chilli powder", "mustard seed", "oil", "salt", "coriander"], [], "Flavor-packed rural curry of golden fried sun-dried spiced lentil dumplings simmered in rustic onion gravy."),
    ("rec_matki_bhel", "Kolhapuri Matki Bhel (Sprouted Moth Beans Street Chaat)", "Maharashtrian", ["Snack", "Tea-Time"], "Snack", 5, 5, "Easy", "Vegetarian", True, False, True, (4, 4, 2, 4, 4), ["street-food", "quick", "no-cook", "healthy"], ["sprouted matki", "puffed rice", "murmura", "onion", "tomato", "farsan", "green chilli thecha", "tamarind chutney", "lemon juice", "coriander", "salt"], [], "Crunchy, spicy, tangy street snack combining sprouted matki with puffed rice, fiery thecha, and sweet tamarind sauce."),
    ("rec_poha_chivda", "Roasted Poha Chivda (Low-Oil Spiced Flattened Rice Snack)", "Maharashtrian", ["Snack", "Tea-Time"], "Snack", 10, 15, "Easy", "Vegetarian", True, False, True, (2, 2, 2, 4, 4), ["crispy", "diwali", "tea-time", "snack"], ["thin poha", "peanuts", "roasted chana dal", "dry coconut slices", "green chilli", "curry leaf", "mustard seed", "turmeric", "powdered sugar", "oil", "salt"], [], "Crispy, light roasted thin flattened rice tossed with golden peanuts, coconut slices, green chillies, and mild spices."),
    ("rec_bhakarwadi", "Crispy Pune Bhakarwadi (Spiced Sweet-Savory Pinwheels)", "Maharashtrian", ["Snack", "Tea-Time"], "Snack", 20, 20, "Hard", "Vegetarian", True, False, False, (3, 3, 3, 5, 4), ["crispy", "puneri", "tea-time", "iconic"], ["maida", "besan", "dry coconut", "poppy seeds", "sesame seeds", "fennel seeds", "garam masala", "tamarind paste", "sugar", "chilli powder", "oil", "salt"], [], "Iconic Puneri crispy spiral pastry rounds bursting with a sweet, tangy, and fiery spiced coconut-sesame stuffing."),
    ("rec_shankarpali", "Khare Shankarpali (Crispy Savory Diamond Namkeen)", "Maharashtrian", ["Snack", "Tea-Time"], "Snack", 15, 15, "Easy", "Vegetarian", True, False, False, (1, 0, 0, 4, 4), ["crispy", "diwali", "tea-time"], ["maida", "all purpose flour", "ajwain", "cumin seeds", "ghee", "oil", "salt"], [], "Addictive flaky diamond-cut crispy snack seasoned with roasted ajwain and cumin seeds."),
    ("rec_palak_khichdi", "Nutritious Palak Dal Khichdi", "North Indian", ["Dinner", "Lunch"], "Main Course", 10, 15, "Easy", "Vegetarian", False, False, True, (2, 1, 0, 4, 5), ["healthy", "comforting", "iron-rich"], ["spinach", "palak", "rice", "moong dal", "onion", "tomato", "garlic", "cumin seed", "ghee", "garam masala", "salt"], [], "Comforting one-pot meal of rice and yellow moong dal cooked with pureed fresh spinach and garlic ghee tadka."),
    ("rec_moong_khichdi", "Soothing Moong Dal Khichdi (Ayurvedic Healing Pot)", "All Indian", ["Dinner", "Lunch"], "Main Course", 5, 15, "Easy", "Vegetarian", False, False, True, (1, 0, 0, 3, 5), ["healing", "soothing", "digestive"], ["rice", "split yellow moong dal", "turmeric", "hing", "cumin seed", "ghee", "black pepper", "salt"], [], "Gentle, easily digestible classic Indian healing meal of rice and yellow lentils with pure ghee and roasted cumin."),
    ("rec_oats_poha", "High-Fiber Vegetable Oats Poha", "All Indian", ["Breakfast", "Quick Meal"], "Breakfast", 5, 10, "Easy", "Vegetarian", True, False, True, (2, 2, 1, 3, 5), ["healthy", "quick", "fiber-rich", "weight-loss"], ["rolled oats", "onion", "green peas", "carrot", "peanut", "mustard seed", "green chilli", "curry leaf", "turmeric", "lemon juice", "oil", "salt", "coriander"], [], "Wholesome modern twist on traditional poha replacing flattened rice with heart-healthy rolled oats."),
    ("rec_tawa_paneer_tikka", "Tawa Paneer Tikka (Spiced Charred Cottage Cheese Cubes)", "North Indian", ["Snack", "Dinner", "Appetizer"], "Appetizer", 15, 10, "Easy", "Vegetarian", False, False, True, (4, 3, 0, 5, 4), ["tandoori", "party", "protein", "quick"], ["paneer", "capsicum", "onion", "curd", "dahi", "besan", "kashmiri red chilli powder", "garam masala", "chaat masala", "kasuri methi", "lemon juice", "mustard oil", "butter", "salt"], [], "Smoky, char-grilled spiced paneer cubes and peppers marinated in thick yogurt and tandoori spices on hot tawa."),
    ("rec_soya_curry", "Nutritious Soya Chunks Masala Curry", "North Indian", ["Lunch", "Dinner"], "Main Course", 10, 20, "Easy", "Vegetarian", True, False, True, (3, 2, 0, 4, 5), ["high-protein", "vegan", "comforting"], ["soya chunks", "onion", "tomato", "ginger", "garlic", "cumin seed", "coriander powder", "garam masala", "kashmiri red chilli powder", "oil", "salt", "coriander"], [], "Plump, juicy protein-rich soya nuggets cooked in a homestyle spiced onion-tomato curry."),
    ("rec_mushroom_matar", "Mushroom Matar Masala (Spiced Mushroom & Green Peas Curry)", "North Indian", ["Lunch", "Dinner"], "Main Course", 10, 15, "Easy", "Vegetarian", True, False, True, (3, 2, 1, 4, 5), ["rich", "restaurant", "comforting"], ["button mushrooms", "green peas", "onion", "tomato", "cashews", "ginger", "garlic", "garam masala", "kasuri methi", "oil", "salt", "coriander"], [], "Earthy sliced mushrooms and sweet green peas simmered in a creamy, spiced onion-tomato and cashew gravy."),
    ("rec_methi_matar_malai", "Restaurant Style Methi Matar Malai", "North Indian", ["Dinner", "Lunch"], "Main Course", 15, 20, "Medium", "Vegetarian", False, False, True, (1, 1, 4, 4, 5), ["rich", "creamy", "restaurant", "mild"], ["fresh methi", "fenugreek leaves", "green peas", "cream", "malai", "cashews", "onion", "ginger", "green chilli", "cardamom", "cinnamon", "butter", "salt"], [], "Decadent North Indian mild curry blending the slight bitterness of fresh methi with sweet peas and rich cashew cream."),
    ("rec_dal_palak", "Dhabha Style Dal Palak (Lentils with Fresh Spinach & Garlic)", "North Indian", ["Lunch", "Dinner"], "Main Course", 10, 15, "Easy", "Vegetarian", False, False, True, (2, 1, 0, 4, 5), ["healthy", "iron-rich", "comforting"], ["toor dal", "spinach", "palak", "onion", "tomato", "garlic", "cumin seed", "hing", "dry red chilli", "ghee", "salt", "coriander"], [], "Wholesome everyday lentil curry enriched with fresh chopped spinach and a smoking hot garlic ghee tadka."),
    ("rec_panchmel_dal", "Rajasthani Panchmel Dal (Five Lentil Royal Curry)", "North Indian", ["Lunch", "Dinner"], "Main Course", 15, 25, "Medium", "Vegetarian", False, False, True, (3, 2, 0, 5, 5), ["royal", "protein", "traditional"], ["toor dal", "moong dal", "chana dal", "masoor dal", "urad dal", "onion", "tomato", "ginger", "garlic", "cloves", "ghee", "hing", "red chilli powder", "garam masala", "salt"], [], "Royal Rajasthani mixture of five protein-rich lentils slow-simmered with aromatic whole spices and pure ghee."),
    ("rec_lauki_kofta", "Melt-in-Mouth Lauki Kofta Curry", "North Indian", ["Lunch", "Dinner"], "Main Course", 20, 25, "Medium", "Vegetarian", True, False, True, (3, 2, 1, 4, 5), ["comforting", "classic", "homestyle"], ["bottle gourd", "lauki", "besan", "onion", "tomato", "ginger", "garlic", "garam masala", "coriander powder", "oil", "salt", "coriander"], [], "Soft, tender bottle gourd dumplings simmered in a luscious, aromatic onion-tomato curry."),
    ("rec_jeera_aloo", "Crispy Dhaba Style Jeera Aloo", "North Indian", ["Lunch", "Dinner", "Quick Meal"], "Side Dish", 5, 10, "Easy", "Vegetarian", True, False, True, (3, 2, 0, 4, 4), ["quick", "classic", "10-min"], ["boiled potato", "aloo", "cumin seed", "jeera", "green chilli", "ginger", "turmeric", "amchur", "dry mango powder", "coriander powder", "oil", "salt", "coriander"], ["boiled potatoes"], "Tender boiled potatoes pan-roasted with crackling roasted cumin seeds, green chillies, and tangy amchur."),
    ("rec_masala_chaas", "Refreshing Spiced Masala Chaas (Indian Buttermilk)", "All Indian", ["Beverage", "Side Dish"], "Beverage", 3, 0, "Easy", "Vegetarian", False, False, True, (2, 3, 0, 3, 5), ["cooling", "digestive", "quick", "summer", "5-min"], ["curd", "dahi", "sour curd", "roasted cumin powder", "black salt", "kala namak", "ginger", "green chilli", "mint leaves", "coriander", "water"], ["sour curd", "curd"], "Cooling, digestive Indian buttermilk churned with mint, coriander, ginger, green chillies, and roasted cumin."),
    ("rec_mango_lassi", "Creamy Alphonso Mango Lassi", "North Indian", ["Beverage", "Dessert"], "Beverage", 5, 0, "Easy", "Vegetarian", False, False, True, (0, 1, 5, 3, 5), ["summer", "sweet", "refreshing", "kids-friendly"], ["mango pulp", "alphonso mango", "thick curd", "dahi", "milk", "sugar", "cardamom", "pistachios", "saffron"], [], "Rich, velvety sweet yogurt drink blended with fragrant Alphonso mango pulp, cardamom, and saffron."),
    ("rec_besan_ladoo", "Traditional Danedar Besan Ladoo", "Maharashtrian", ["Dessert", "Festival"], "Dessert", 15, 25, "Medium", "Vegetarian", False, False, True, (0, 0, 5, 2, 5), ["festive", "traditional", "sweet"], ["besan", "gram flour", "pure ghee", "bura sugar", "powdered sugar", "cardamom", "cashews", "almonds"], [], "Mouth-melting festive dessert made by slow-roasting coarse gram flour in golden ghee with fragrant green cardamom."),
    ("rec_rava_ladoo", "Quick Maharashtrian Rava Ladoo with Fresh Coconut", "Maharashtrian", ["Dessert", "Festival"], "Dessert", 10, 15, "Easy", "Vegetarian", False, False, False, (0, 0, 5, 2, 5), ["festive", "quick", "sweet"], ["semolina", "rava", "fresh grated coconut", "sugar", "ghee", "cardamom", "milk", "raisins", "cashews"], [], "Juicy, sweet traditional Maharashtrian ladoos made from roasted fine semolina and juicy grated fresh coconut."),
    ("rec_poha_kheer", "Instant Poha Kheer / Payasam", "All Indian", ["Dessert", "Festival", "Quick Meal"], "Dessert", 5, 10, "Easy", "Vegetarian", False, False, True, (0, 0, 5, 2, 5), ["quick", "sweet", "comforting", "15-min"], ["poha", "milk", "jaggery", "sugar", "ghee", "cardamom", "cashews", "raisins"], [], "Delightful 10-minute Indian dessert made of flattened rice simmered in sweetened milk with cardamom and ghee-roasted nuts."),
    ("rec_seviyan_kheer", "Rich Vermicelli Kheer (Seviyan Payasam)", "All Indian", ["Dessert", "Festival"], "Dessert", 5, 15, "Easy", "Vegetarian", False, False, False, (0, 0, 5, 2, 5), ["festive", "classic", "sweet"], ["roasted vermicelli", "seviyan", "milk", "sugar", "cardamom", "ghee", "cashews", "almonds", "pistachios", "saffron"], [], "Classic festive dessert of golden-roasted vermicelli slow-cooked in sweetened whole milk scented with saffron and nuts."),
    ("rec_sabudana_kheer", "Creamy Sabudana Kheer (Upwas Special Sago Pudding)", "Maharashtrian", ["Dessert", "Fast / Upwas"], "Dessert", 10, 15, "Easy", "Vegetarian", False, True, True, (0, 0, 5, 2, 5), ["upwas", "sweet", "creamy"], ["sabudana", "sago", "milk", "sugar", "cardamom", "saffron", "cashews", "almonds", "ghee"], [], "Rich, comforting fasting pudding of tender translucent tapioca pearls simmered in cardamom-scented whole milk."),
    ("rec_green_chutney", "Zingy Mint Coriander Green Chutney", "All Indian", ["Condiment", "Accompaniment"], "Condiment", 5, 0, "Easy", "Vegetarian", True, False, True, (3, 3, 1, 3, 5), ["quick", "staple", "5-min"], ["fresh coriander", "mint leaves", "green chilli", "ginger", "garlic", "lemon juice", "roasted cumin powder", "chaat masala", "salt"], [], "Vibrant, spicy, tangy herbal condiment that powers every Indian sandwich, pakora, and chaat."),
    ("rec_sweet_tamarind_chutney", "Halwai Style Sweet Imli & Date Chutney", "All Indian", ["Condiment", "Accompaniment"], "Condiment", 5, 15, "Easy", "Vegetarian", True, True, True, (1, 5, 5, 3, 4), ["sweet-tangy", "chaat", "storage"], ["tamarind", "seedless dates", "jaggery", "gul", "roasted cumin powder", "fennel powder", "dry ginger powder", "saunth", "black salt", "red chilli powder", "salt"], [], "Glossy, sweet and tangy chaat chutney infused with tamarind, organic dates, jaggery, and dry ginger powder.")
]


# Ingredient measurement enrichment -------------------------------------------------
# The catalog generator historically used ``item`` as a placeholder for many
# ingredients.  That is not useful to a cook, so convert every placeholder into
# a concrete kitchen measurement/count.  Existing explicit measurements are kept.

def enrich_ingredient_measurements(recipes):
    count_patterns = {
        "onion": (1, "medium"), "onions": (1, "medium"),
        "tomato": (2, "medium"), "tomatoes": (2, "medium"),
        "potato": (2, "medium"), "potatoes": (2, "medium"), "aloo": (2, "medium"), "batata": (2, "medium"),
        "capsicum": (1, "medium"), "bell pepper": (1, "medium"),
        "carrot": (1, "medium"), "cucumber": (1, "medium"),
        "eggplant": (1, "medium"), "brinjal": (4, "small"), "vangi": (4, "small"),
        "lemon": (1, "medium"), "lime": (1, "medium"),
        "green chilli": (2, "whole"), "green chil": (2, "whole"),
        "ginger": (1, "tbsp, grated"), "garlic": (4, "cloves"), "lasun": (4, "cloves"),
        "curry leaf": (8, "leaves"), "curry leaves": (8, "leaves"),
        "mint leaves": (2, "tbsp, chopped"), "fresh coriander": (2, "tbsp, chopped"), "coriander": (2, "tbsp, chopped"),
        "fresh methi": (1, "cup, chopped"), "fenugreek leaves": (1, "cup, chopped"),
        "spinach": (2, "cups, chopped"), "palak": (2, "cups, chopped"),
        "cauliflower": (2, "cups, florets"), "gobi": (2, "cups, florets"),
        "green peas": (1, "cup"), "peas": (1, "cup"),
        "coconut": (0.5, "cup, grated"), "fresh coconut": (0.5, "cup, grated"), "fresh grated coconut": (0.5, "cup, grated"),
        "dry coconut": (0.25, "cup, grated"), "dry coconut slices": (0.25, "cup"),
        "peanut": (0.25, "cup"), "peanuts": (0.25, "cup"), "roasted peanuts": (0.25, "cup"),
        "cashews": (0.25, "cup"), "almonds": (0.25, "cup"), "pistachios": (2, "tbsp"),
        "raisins": (2, "tbsp"), "sesame seed": (1, "tbsp"), "til": (1, "tbsp"),
        "cardamom": (0.5, "tsp"), "nutmeg": (0.25, "tsp"), "saffron": (1, "pinch"),
        "clove": (3, "whole"), "cloves": (3, "whole"), "cinnamon": (1, "inch piece"), "bay leaf": (1, "leaf"),
        "water": (2, "cups"), "milk": (2, "cups"), "coconut milk": (1, "cup"),
        "lemon juice": (1, "tbsp"), "tamarind": (1, "tbsp"), "tamarind paste": (1, "tbsp"),
        "jaggery": (2, "tbsp"), "gul": (2, "tbsp"), "sugar": (2, "tbsp"), "bura sugar": (2, "tbsp"),
        "salt": (1, "tsp"), "black salt": (0.5, "tsp"), "kala namak": (0.5, "tsp"),
        "oil": (2, "tbsp"), "coconut oil": (2, "tbsp"), "ghee": (2, "tbsp"), "pure ghee": (2, "tbsp"), "butter": (2, "tbsp"),
        "curd": (1, "cup"), "dahi": (1, "cup"), "sour curd": (1, "cup"), "thick curd": (1, "cup"), "cream": (0.5, "cup"),
        "paneer": (200, "g"), "tofu": (200, "g"),
        "poha": (2, "cups"), "thin poha": (2, "cups"), "rolled oats": (2, "cups"),
        "rice": (1.5, "cups"), "bhaat": (3, "cups, cooked"), "cooked rice": (3, "cups"),
        "dal": (1, "cup"), "moong dal": (1, "cup"), "chana dal": (1, "cup"), "urad dal": (1, "cup"),
        "rajma": (1, "cup"), "kidney beans": (1, "cup"), "kabuli chana": (1, "cup"), "white chickpeas": (1, "cup"),
        "kala chana": (1, "cup"), "brown chickpeas": (1, "cup"), "black eyed peas": (1, "cup"), "chawli": (1, "cup"),
        "sprouted matki": (2, "cups"), "matki": (2, "cups"), "sprouted moong": (2, "cups"), "sprouted val": (2, "cups"),
        "field beans": (2, "cups"), "soya chunks": (1.5, "cups"), "soya granules": (1.5, "cups"),
        "besan": (1, "cup"), "gram flour": (1, "cup"), "sattu": (1, "cup"), "wheat flour": (2, "cups"), "atta": (2, "cups"), "maida": (2, "cups"),
        "jowar flour": (2, "cups"), "bajra flour": (2, "cups"), "rice flour": (2, "cups"), "semolina": (1, "cup"), "rava": (1, "cup"), "sooji": (1, "cup"),
        "bread": (4, "slices"), "leftover bread": (4, "slices"), "chapati": (4, "rotis"), "poli": (4, "rotis"), "leftover roti": (4, "rotis"),
        "murmura": (4, "cups"), "puffed rice": (4, "cups"), "farsan": (1, "cup"), "shev": (1, "cup"), "sev": (1, "cup"),
    }
    spice_words = ("masala", "powder", "hing", "asafoetida", "ajwain", "jeera", "cumin", "mustard", "rai", "turmeric", "haldi", "amchur", "kokum", "anardana", "saunth", "fennel", "pepper", "chilli", "chili")
    for recipe in recipes:
        for ing in recipe.get("ingredients", []):
            name = str(ing.get("name", "")).strip()
            key = name.lower()
            unit = str(ing.get("unit", "")).strip().lower()
            # Only replace placeholder/no-measure units. Explicit units are retained.
            placeholder = unit in {"", "item", "items", "chopped", "finely chopped", "slit", "serving set", "combined"}
            if not placeholder:
                continue
            match = None
            for k, value in count_patterns.items():
                if k in key:
                    match = value
                    break
            if match:
                ing["quantity"], ing["unit"] = match
            elif any(w in key for w in spice_words):
                ing["quantity"], ing["unit"] = (1, "tsp")
            elif ing.get("category") in {"spices", "seasoning"}:
                ing["quantity"], ing["unit"] = (1, "tsp")
            elif ing.get("category") == "herbs":
                ing["quantity"], ing["unit"] = (2, "tbsp, chopped")
            elif ing.get("category") == "vegetables":
                ing["quantity"], ing["unit"] = (1, "medium")
            elif ing.get("category") == "nuts":
                ing["quantity"], ing["unit"] = (2, "tbsp")
            else:
                # Last-resort culinary measure instead of the meaningless "item".
                ing["quantity"], ing["unit"] = (1, "cup")
        recipe["base_servings"] = int(recipe.get("nutrition_per_serving", {}).get("servings", 2) or 2)

def sanitize_recipe_tips(recipes):
    generic = (
        "fresh local spices ensure peak aroma",
        "low flame cooking yields richest depth of flavor",
        "serve fresh with traditional accompaniments",
        "follow the listed ingredients exactly",
        "serve with traditional accompaniments",
        "the ultimate quick comfort breakfast from leftovers",
    )
    def replacement(step, recipe):
        ins = (step.get("instruction") or "").lower()
        title = recipe["title"].split("(")[0].strip()
        if any(x in ins for x in ("steam", "steaming")): return f"Keep the lid closed during steaming so {title} cooks evenly."
        if any(x in ins for x in ("fry", "shallow fry", "deep fry", "pan-toast", "crisp")): return f"Keep the heat steady and watch the surface of {title} for even browning."
        if any(x in ins for x in ("simmer", "boil")): return f"Keep the simmer gentle and stop when the main ingredients reach the texture described for {title}."
        if any(x in ins for x in ("blend", "grind", "pound", "whisk")): return f"Process the mixture only until it reaches the texture specified for {title}."
        if any(x in ins for x in ("roll", "pat", "shape", "stuff")): return f"Keep each portion even so the {title} cooks uniformly."
        if any(x in ins for x in ("rice", "poha", "chapati", "roti")): return f"Handle the {title} gently so its main grain or bread component keeps its intended texture."
        if any(x in ins for x in ("milk", "curd", "yogurt")): return f"Stir regularly and use gentle heat so the dairy base stays smooth in {title}."
        return f"Use the listed ingredients as the visual cue for this step of {title}."
    for recipe in recipes:
        for step in recipe.get("steps", []):
            tip=(step.get("tip") or "").strip().lower()
            if any(x in tip for x in generic) or "serve with" in tip or "served with" in tip:
                step["tip"] = replacement(step, recipe)

# Build the complete list of 100+ recipes
for idx, spec in enumerate(ADDITIONAL_RECIPE_SPECS):
    r_id, title, cuisine, meal_types, course, prep_t, cook_t, diff, diet, is_veg, is_jain, is_gf, flavor, moods, norm_ings, leftovers, summary = spec
    
    # Generate structured ingredients
    structured_ings = []
    for ing_name in norm_ings:
        structured_ings.append({
            "name": ing_name.title(),
            "quantity": 1.0,
            "unit": "tbsp" if "seed" in ing_name or "oil" in ing_name or "powder" in ing_name else ("cup" if "flour" in ing_name or "rice" in ing_name or "dal" in ing_name else "item"),
            "is_optional": ing_name in ["coriander", "cashews", "pomegranate", "loni", "butter"],
            "category": "spices" if "powder" in ing_name or "seed" in ing_name else ("vegetables" if ing_name in ["onion", "tomato", "potato", "capsicum", "eggplant"] else "general"),
            "substitutes": ({
                "ghee": ["oil"], "butter": ["oil"], "loni": ["oil"],
                "oil": ["ghee"], "peanut": ["roasted chana dal"], "peanuts": ["roasted chana dal"],
                "onion": ["hing + extra cumin"], "garlic": ["hing + ginger"],
                "green chilli": ["black pepper"], "red chilli powder": ["kashmiri chilli powder"],
                "milk": ["unsweetened plant milk"], "curd": ["unsweetened plant yogurt"],
                "yogurt": ["unsweetened plant yogurt"], "paneer": ["firm tofu"],
                "sugar": ["reduce by half", "jaggery"], "jaggery": ["reduce by half"],
                "besan": ["sattu"], "poha": ["rolled oats"], "matki": ["sprouted moong"],
                "coconut": ["desiccated coconut"]
            }.get(ing_name, []))
        })

    recipe_obj = {
        "id": r_id,
        "title": title,
        "regional_cuisine": cuisine,
        "meal_type": meal_types,
        "course": course,
        "prep_time_mins": prep_t,
        "cook_time_mins": cook_t,
        "total_time_mins": prep_t + cook_t,
        "difficulty": diff,
        "diet": diet,
        "is_vegan": is_veg,
        "is_jain": is_jain,
        "is_gluten_free": is_gf,
        "flavor_profile": {
            "spicy": flavor[0],
            "tangy": flavor[1],
            "sweet": flavor[2],
            "savory": flavor[3],
            "comfort": flavor[4]
        },
        "mood_tags": moods,
        "ingredients": structured_ings,
        "normalized_ingredients": norm_ings,
        "leftover_ingredients_used": leftovers,
        "steps": build_generated_steps(title, norm_ings, meal_types, course, prep_t, cook_t),
        "nutrition_per_serving": {
            "servings": 2,
            "calories": 250 + (idx * 5) % 200,
            "protein_g": round(5.0 + (idx * 0.3) % 15, 1),
            "carbs_g": round(30.0 + (idx * 0.7) % 35, 1),
            "fat_g": round(6.0 + (idx * 0.4) % 14, 1),
            "fiber_g": round(3.0 + (idx * 0.2) % 6, 1)
        },
        "equipment": ["Kadai / Pan", "Spatula", "Lid"],
        "summary": summary
    }
    RECIPES.append(recipe_obj)

# Enrich ALL recipes with household multi-member traits
for r in RECIPES:
    t_lower = r["title"].lower()
    norm_all = " ".join(r.get("normalized_ingredients", []))
    spicy_val = r.get("flavor_profile", {}).get("spicy", 2)
    protein = r.get("nutrition_per_serving", {}).get("protein_g", 5.0)

    # Texture
    if any(k in t_lower for k in ["khichdi", "varan", "bhaat", "kadhi", "pithla", "soup", "saar", "rasam", "curd rice", "kheer", "dudhi", "upma"]):
        r["texture"] = "soft"
    elif any(k in t_lower for k in ["vada", "cutlet", "tikki", "bhakarwadi", "shankarpali", "pakora", "crispy", "chivda"]):
        r["texture"] = "crispy"
    else:
        r["texture"] = "regular"

    # Kid Friendly
    r["is_kid_friendly"] = (spicy_val <= 2) or any(k in t_lower for k in ["paneer", "poha", "bhurji", "paratha", "kheer", "dhokla", "sandwich", "frankie", "ladoo", "toast", "pav bhaji"])

    # Elder Friendly
    r["is_elder_friendly"] = (r["texture"] == "soft") or (spicy_val <= 3 and any(k in t_lower for k in ["varan", "khichdi", "kadhi", "curd rice", "dudhi", "rasam", "saar", "moong", "pithla", "cheela", "ghavan"]))

    # High Protein
    r["is_high_protein"] = (protein >= 7.5) or any(k in norm_all for k in ["dal", "paneer", "soya", "sprouts", "matki", "chana", "besan", "moong", "rajma", "urad"])

    # Easy to Digest
    r["is_easy_digest"] = any(k in t_lower for k in ["khichdi", "varan", "curd rice", "rasam", "saar", "dudhi", "moong dal", "ghavan"])

    # One Pot Meal
    r["is_one_pot"] = any(k in t_lower for k in ["khichdi", "bhaat", "biryani", "pulao", "bath", "chakolya", "poha", "upma"])
    fried_words = any(k in t_lower for k in ["fried", "fritter", "pakora", "vada", "tikki", "cutlet", "bhakarwadi", "shankarpali", "shahi tukda"])
    added_fat = sum(1 for x in ["ghee", "butter", "oil"] if x in norm_all)
    added_sugar = any(k in norm_all for k in ["sugar", "jaggery", "date", "sweetener"])
    r["is_light"] = (not fried_words and added_fat <= 1 and not added_sugar) or any(k in t_lower for k in ["khichdi", "poha", "rasam", "saar", "chaas", "chutney", "usal", "dal"])

enrich_ingredient_measurements(RECIPES)
sanitize_recipe_tips(RECIPES)

print(f"Total recipes generated: {len(RECIPES)}")

# Write to recipes.json
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(RECIPES, f, indent=2, ensure_ascii=False)

print(f"Successfully saved {len(RECIPES)} recipes to {OUTPUT_FILE}")

