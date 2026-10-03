import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "backend" / "data"
RECIPES_FILE = DATA_DIR / "recipes.json"
FRONTEND_DIR = BASE_DIR / "frontend"

HOST = os.getenv("MEALSOLVER_HOST", "127.0.0.1")
PORT = int(os.getenv("MEALSOLVER_PORT", "8000"))

# IR & Scoring Weights
BM25_WEIGHT = 0.45
TFIDF_WEIGHT = 0.35
FLAVOR_WEIGHT = 0.20

# Pantry Coverage Thresholds
PANTRY_MIN_COVERAGE = 0.30
PANTRY_EXACT_MATCH_BONUS = 0.25
