"""
Recipe Database Loader and Cache.
Loads, validates, and provisions recipe objects for IR engine, Pantry Matcher, Recommender, and Leftover Solver.
"""
import json
import re
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from backend.config import RECIPES_FILE
from backend.models.recipe import Recipe

logger = logging.getLogger("mealsolver.loader")

class RecipeDatabase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecipeDatabase, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.recipes: List[Dict[str, Any]] = []
        self.recipes_by_id: Dict[str, Dict[str, Any]] = {}
        self.load_recipes()
        self._initialized = True

    def load_recipes(self, file_path: Optional[Path] = None):
        target_path = file_path or RECIPES_FILE
        if not target_path.exists():
            raise FileNotFoundError(f"Recipe database not found at {target_path}")

        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Attach a local recipe-specific image only when the generated asset exists.
        # This keeps the app free of broken/placeholder image links.
        image_dir = target_path.parent.parent.parent / "frontend" / "images" / "recipes"
        for recipe in data:
            image_path = image_dir / f"{recipe['id']}.jpg"
            recipe["image_url"] = f"/static/images/recipes/{recipe['id']}.jpg" if image_path.exists() else None

        self.recipes = data
        self.recipes_by_id = {r["id"]: r for r in data}
        logger.info(f"Loaded {len(self.recipes)} recipes from {target_path}")

    def get_all(self) -> List[Dict[str, Any]]:
        return self.recipes

    def get_by_id(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        return self.recipes_by_id.get(recipe_id)

    def get_all_ingredients(self) -> List[str]:
        """Extract a unique sorted list of all available pantry ingredients across recipes."""
        ingredients = set()
        for r in self.recipes:
            for ing in r.get("ingredients", []):
                name = ing.get("name", "").strip()
                if name:
                    ingredients.add(name)
            for norm in r.get("normalized_ingredients", []):
                if norm.strip():
                    ingredients.add(norm.strip().title())
        return sorted(list(ingredients))

def get_db() -> RecipeDatabase:
    return RecipeDatabase()
