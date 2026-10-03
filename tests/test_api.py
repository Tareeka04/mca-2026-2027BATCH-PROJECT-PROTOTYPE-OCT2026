import io
from fastapi.testclient import TestClient
from PIL import Image
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["app"] == "MealSolver"

def test_list_recipes():
    res = client.get("/api/recipes?limit=10")
    assert res.status_code == 200
    data = res.json()
    assert "recipes" in data
    assert len(data["recipes"]) > 0
    assert data["total"] >= 100

def test_recipe_scaling():
    res = client.get("/api/recipes/rec_kanda_poha/scale?servings=6")
    assert res.status_code == 200
    data = res.json()
    assert data["target_servings"] == 6
    assert data["scale_factor"] == 3.0  # 6 / 2
    assert len(data["scaled_ingredients"]) > 0

def test_pantry_solver_api():
    payload = {
        "ingredients": ["Poha", "Onion", "Peanuts", "Green Chillies", "Mustard Seeds", "Turmeric"],
        "filters": {"diet": "Vegetarian"}
    }
    res = client.post("/api/solve/pantry", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_matches"] > 0
    assert len(data["results"]) > 0

def test_craving_solver_api():
    payload = {
        "query": "Spicy comforting khichdi for rainy monsoon",
        "spice_level": 4,
        "comfort_level": 5
    }
    res = client.post("/api/solve/craving", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_results"] > 0

def test_leftover_solver_api():
    payload = {
        "leftover_items": ["cooked rice", "stale roti"]
    }
    res = client.post("/api/solve/leftovers", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_transformations"] > 0

def test_scanner_api():
    img = Image.new("RGB", (100, 100), color=(200, 30, 30))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    files = {"file": ("test_fridge.jpg", buf, "image/jpeg")}
    res = client.post("/api/scanner/detect", files=files)
    assert res.status_code == 200
    data = res.json()
    assert "detections" in data
    assert len(data["detections"]) > 0

def test_household_solve_api():
    payload = {
        "members": [
            {"id": "m1", "name": "Mom", "role": "Mother", "diet": "Vegetarian", "spice_tolerance": "Low", "avoid_ingredients": ["peanuts"], "preferences": ["quick"]},
            {"id": "m2", "name": "Aarav", "role": "Child", "diet": "Vegetarian", "spice_tolerance": "Mild", "avoid_ingredients": [], "preferences": ["kid_friendly"]},
            {"id": "m3", "name": "Dadi", "role": "Grandmother", "diet": "Vegetarian", "spice_tolerance": "Low", "avoid_ingredients": [], "preferences": ["soft_food"]}
        ],
        "available_ingredients": ["Rice", "Moong Dal", "Tomato", "Potato", "Ghee", "Turmeric", "Cumin Seeds"],
        "servings": 3
    }
    res = client.post("/api/household/solve", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_members"] == 3
    assert data["total_servings"] == 3
    assert data["best_shared_meal"] is not None
    assert len(data["best_shared_meal"]["member_explanations"]) == 3

def test_household_presets_api():
    res = client.get("/api/household/presets")
    assert res.status_code == 200
    data = res.json()
    assert "presets" in data
    assert len(data["presets"]) >= 3


def test_recipe_scaling_returns_human_measurements():
    res = client.get("/api/recipes/rec_kanda_poha/scale?servings=5")
    assert res.status_code == 200
    data = res.json()
    assert data["target_servings"] == 5
    assert all(i.get("measurement") for i in data["scaled_ingredients"])
    peanuts = next(i for i in data["scaled_ingredients"] if "peanut" in i["name"].lower())
    assert peanuts["quantity"] == 5.0
    assert peanuts["measurement"] == "5 tbsp"


def test_household_api_returns_scaled_adapted_recipe_measurements():
    payload = {
        "members": [
            {"id": "m1", "name": "A", "role": "Adult", "diet": "Vegetarian", "spice_tolerance": "Medium", "custom_preference": "no ghee, no butter"}
        ],
        "servings": 4
    }
    res = client.post("/api/household/solve", json=payload)
    assert res.status_code == 200
    meal = res.json()["best_shared_meal"]
    assert meal is not None
    assert meal["total_household_servings"] == 4
    assert all(i.get("measurement") for i in meal["scaled_ingredients"])


def test_recipe_scale_returns_explicit_measurements():
    response = client.get('/api/recipes/rec_kanda_poha/scale?servings=4')
    assert response.status_code == 200
    data = response.json()
    assert data['target_servings'] == 4
    assert data['scaled_ingredients']
    assert any(x['name'].startswith('Poha') and x['measurement'] == '4 cups' for x in data['scaled_ingredients'])
    assert all(x['measurement'] for x in data['scaled_ingredients'])
