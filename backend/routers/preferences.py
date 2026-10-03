"""
Preferences and Meta Taxonomy Router.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/preferences", tags=["preferences"])

@router.get("/meta")
def get_preferences_meta():
    return {
        "cuisines": [
            {"id": "All", "name": "All Cuisines", "icon": "🍲"},
            {"id": "Maharashtrian", "name": "Maharashtrian (Speciality)", "icon": "🚩"},
            {"id": "North Indian", "name": "North Indian / Punjabi", "icon": "🫓"},
            {"id": "South Indian", "name": "South Indian", "icon": "🥥"},
            {"id": "Gujarati", "name": "Gujarati / Kathiyawadi", "icon": "🫔"},
            {"id": "All Indian", "name": "Pan-Indian Homestyle", "icon": "🇮🇳"}
        ],
        "diets": [
            {"id": "All", "name": "All Diets"},
            {"id": "Vegetarian", "name": "Pure Vegetarian"},
            {"id": "Vegan", "name": "100% Plant Vegan"},
            {"id": "Jain", "name": "Jain Friendly (No Root Veg)"},
            {"id": "Gluten-Free", "name": "Gluten-Free"}
        ],
        "meal_types": [
            {"id": "All", "name": "All Meals", "icon": "🍽️"},
            {"id": "Breakfast", "name": "Breakfast / Morning", "icon": "🌅"},
            {"id": "Lunch", "name": "Lunch / Afternoon", "icon": "☀️"},
            {"id": "Dinner", "name": "Dinner / Night", "icon": "🌙"},
            {"id": "Snack", "name": "Chai Time Snacks", "icon": "☕"},
            {"id": "Fast / Upwas", "name": "Upwas / Fasting", "icon": "🙏"}
        ],
        "mood_presets": [
            {"id": "comforting", "name": "Comfort Food", "icon": "🥣", "desc": "Warm, soothing homestyle bowls"},
            {"id": "quick", "name": "Quick & Easy (< 20 mins)", "icon": "⚡", "desc": "Fast prep when in a rush"},
            {"id": "spicy", "name": "Fiery Street Style", "icon": "🌶️", "desc": "Bold chilies, tari, and crunch"},
            {"id": "healthy", "name": "Wholesome & High Protein", "icon": "🥗", "desc": "Sprouts, lentils, greens"},
            {"id": "monsoon", "name": "Monsoon Warmth", "icon": "🌧️", "desc": "Steamy, crispy, spiced delights"},
            {"id": "festive", "name": "Festive & Royal", "icon": "✨", "desc": "Rich aromas, sweets, ghee-laden"},
            {"id": "upwas", "name": "Upwas / Fasting", "icon": "🪔", "desc": "Sabudana, peanuts, sendha namak"}
        ],
        "leftovers": [
            {"id": "cooked rice", "name": "Cooked Rice (Bhaat)", "icon": "🍚", "desc": "Leftover basmati or steamed rice"},
            {"id": "stale roti", "name": "Stale Chapati / Roti (Poli)", "icon": "🫓", "desc": "Day-old soft or dry flatbreads"},
            {"id": "leftover dal", "name": "Leftover Dal (Varan)", "icon": "🍲", "desc": "Toor, Moong or Yellow dal"},
            {"id": "boiled potatoes", "name": "Boiled Potatoes (Batate)", "icon": "🥔", "desc": "Boiled or steamed aloo"},
            {"id": "sour curd", "name": "Sour Curd / Dahi (Taak)", "icon": "🥛", "desc": "Tangy yogurt or buttermilk"},
            {"id": "leftover bread", "name": "Leftover Bread / Pav", "icon": "🍞", "desc": "Sandwich bread or pav buns"},
            {"id": "leftover sabzi", "name": "Leftover Dry Sabzi", "icon": "🥘", "desc": "Cooked mixed vegetables"}
        ],
        "quick_pantry_staples": [
            "Onion", "Potato", "Tomato", "Green Chillies", "Ginger", "Garlic",
            "Coriander", "Curry Leaves", "Mustard Seeds", "Cumin Seeds",
            "Turmeric", "Poha", "Besan", "Toor Dal", "Peanuts",
            "Paneer", "Fresh Coconut", "Lemon", "Ghee", "Goda Masala",
            "Sprouted Matki", "Rice", "Wheat Flour", "Kasuri Methi"
        ]
    }
