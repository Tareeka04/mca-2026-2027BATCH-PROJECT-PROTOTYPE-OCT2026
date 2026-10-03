/**
 * MealSolver API Client
 */
const API_BASE = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
  ? window.location.origin
  : 'http://127.0.0.1:8000';

const API = {
  // Recipes
  async getRecipes(params = {}) {
    const cleanParams = Object.fromEntries(Object.entries(params).filter(([_, value]) => value !== undefined && value !== null && value !== ''));
    const query = new URLSearchParams(cleanParams).toString();
    const res = await fetch(`${API_BASE}/api/recipes?${query}`);
    return res.json();
  },

  async getRecipe(id) {
    const res = await fetch(`${API_BASE}/api/recipes/${id}`);
    return res.json();
  },

  async scaleRecipe(id, servings) {
    const res = await fetch(`${API_BASE}/api/recipes/${id}/scale?servings=${servings}`);
    return res.json();
  },

  async getSimilarRecipes(id, count = 4) {
    const res = await fetch(`${API_BASE}/api/recipes/${id}/similar?count=${count}`);
    return res.json();
  },

  async getAllIngredients() {
    const res = await fetch(`${API_BASE}/api/recipes/data/all_ingredients`);
    return res.json();
  },

  // Pantry Solver
  async solvePantry(payload) {
    const res = await fetch(`${API_BASE}/api/solve/pantry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  // Craving Solver
  async solveCraving(payload) {
    const res = await fetch(`${API_BASE}/api/solve/craving`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  // Leftovers Solver
  async solveLeftovers(payload) {
    const res = await fetch(`${API_BASE}/api/solve/leftovers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async getLeftoverStaples() {
    const res = await fetch(`${API_BASE}/api/solve/leftover_staples`);
    return res.json();
  },

  // Fridge Scanner
  async detectFridge(formData) {
    const res = await fetch(`${API_BASE}/api/scanner/detect`, {
      method: 'POST',
      body: formData
    });
    return res.json();
  },

  // Household Meal Solver ("ONE HOUSEHOLD. DIFFERENT NEEDS. ONE MEAL.")
  async solveHousehold(payload) {
    const res = await fetch(`${API_BASE}/api/household/solve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  },

  async getHouseholdPresets() {
    const res = await fetch(`${API_BASE}/api/household/presets`);
    return res.json();
  },

  // Metadata
  async getMeta() {
    const res = await fetch(`${API_BASE}/api/preferences/meta`);
    return res.json();
  }
};
