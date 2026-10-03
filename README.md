# 🍲 MealSolver: Intelligent Indian Household Meal-Solving Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: Pytest](https://img.shields.io/badge/pytest-31%20passed-brightgreen.svg)](https://docs.pytest.org/)

**MealSolver** is an intelligent Indian household meal-solving application designed from first principles to solve the real daily dilemma in Indian kitchens:
- 🥫 **"What can I cook with what I have?"** (*Pantry Gap Analysis & Substitute Matcher*)
- 🌶️ **"What should I cook based on what I am craving?"** (*Semantic IR & Flavor Profile Matching*)
- ♻️ **"What can I make with my leftovers?"** (*Authentic Desi Leftover Transformation Engine*)
- 📷 **"What can I make from ingredients in my fridge?"** (*Offline Local Vision & Ingredient Scanner*)

It is **NOT** a static recipe list; it is a full-fledged Information Retrieval and Knowledge-Based Decision Engine built locally without any paid APIs.

---

## 🌟 Key Features

### 1. 🥫 Pantry Solver ("What can I cook with what I have?")
- **Ingredient Coverage & Gap Analysis**: Matches available kitchen ingredients against 129 authentic recipes, categorizing ingredients into *Essential* and *Optional/Garnish*.
- **Readiness Badges**: Automatically labels recipes as `Ready to Cook Now` (0 missing items), `Missing 1 Item`, or `Missing 2 Items`.
- **Indian Substitution Knowledge Base**: Recommends bidirectional substitutions (e.g., Kokum $\leftrightarrow$ Tamarind/Amchur, Goda Masala $\leftrightarrow$ Garam Masala + roasted coriander-cumin, Sour Curd $\leftrightarrow$ Lemon-curd/Taak, Poha $\leftrightarrow$ Oats).
- **Hinglish & Marathi Thesaurus**: Recognizes native kitchen terms (e.g. *Kanda* $\leftrightarrow$ Onion, *Batata* $\leftrightarrow$ Potato, *Vangi* $\leftrightarrow$ Eggplant, *Varan* $\leftrightarrow$ Dal, *Poli* $\leftrightarrow$ Chapati/Roti).

### 2. 🌶️ Craving & Mood Recommender
- **Hybrid Retrieval (BM25 + TF-IDF Cosine Similarity)**: Queries like *"spicy comforting khichdi for monsoon evening"* or *"sweet festive dessert"* match both exact keywords and semantic context.
- **4-Dimensional Flavor Profiling**: Interactive sliders for *Spiciness*, *Tanginess*, *Sweetness*, and *Comfort Level* (0 to 5) calculate vector proximity to recipes.
- **Explainable Recommendations**: Displays human-friendly reasons why each dish matched your craving.

### 3. ♻️ Desi Leftover Transformation Engine
- Dedicated transformation logic for core Indian household leftovers:
  - **Cooked Rice (Bhaat)** $\rightarrow$ *Phodnicha Bhaat*, *Curd Rice (Daddojanam)*, *Mumbai Tawa Pulao*, *Lemon Rice (Chitranna)*, *Crispy Rice Cutlets*.
  - **Stale Chapati / Roti (Poli)** $\rightarrow$ *Phodnichi Poli (Chapati Chivda)*, *Gul-Poli Ladoo (Malida)*, *Desi Roti Frankie*, *Masala Roti Noodles*.
  - **Leftover Dal (Varan)** $\rightarrow$ *Spiced Dal Paratha*, *Chakolya / Varan Phal (Dal Dhokli)*, *Tadka Dal Khichdi*.
  - **Boiled Potatoes (Batate)** $\rightarrow$ *Batata Vada*, *Sukhi Batata Bhaji*, *Aloo Tikki Chaat*.
  - **Sour Curd / Dahi (Taak)** $\rightarrow$ *Maharashtrian Kadhi*, *Dhabha Dahi Tadka*, *Instant Rava Dhokla*.
  - **Leftover Bread / Pav** $\rightarrow$ *Phodnicha Bread (Bread Upma)*, *Bread Pakora*, *Shahi Tukda*.
  - **Leftover Dry Sabzi** $\rightarrow$ *Stuffed Sabzi Paratha*, *Mumbai Masala Toast Sandwich*.
- Provides specialized **Chef Tips** and prep speed badges (`< 10 Mins`, `Quick Flip`).

### 4. 📷 Local Fridge Scanner (0 API Cost)
- Analyzes uploaded fridge photos using **Pillow** and **OpenCV** in HSV color-space to detect ingredient clusters (Tomatoes, Coriander, Chillies, Onions, Potatoes, Paneer, Lemons, Brinjals).
- Interactive tag review bar allowing users to tap to verify/add/remove before launching directly into the Pantry Solver.

### 5. 🍳 Interactive Cooking Mode & Servings Scaler
- **Dynamic Servings Scaler**: Proportionally recalculates all ingredient quantities and total nutritional values (Calories, Protein, Carbs, Fat) for 1 to 24 servings with fraction formatting.
- **Distraction-Free Step Carousel**: Step-by-step guidance with built-in **Live Countdown Timers** and audio chimes.
- **Voice Narration (Read Aloud)**: Hands-free step readout using the Web Speech API (`speechSynthesis`).

### 6. 🏠 Household Meal Solver
- Multi-member household setup with roles, diets, spice tolerance, avoided ingredients and preferences.
- Strict constraints are checked before preference scoring.
- Returns ONE shared meal, exact scaled ingredients, missing ingredient quantities and an honest conflict message when no perfect match exists.
- Household setup is saved locally in the browser; no login is required.

### 7. 🛒 Smart Grocery Shopping List
- 1-Click adds missing ingredients from recipe cards or details.
- Grouped by recipe and category with purchase check-off checkboxes.
- **1-Click WhatsApp Export**: Copies formatted grocery list directly to clipboard for sharing on WhatsApp or SMS.

---

## 🏛️ System Architecture

```
MealSolver/
├── backend/
│   ├── config.py                 # App configuration and paths
│   ├── main.py                   # FastAPI app entrypoint, CORS, static mount
│   ├── core/
│   │   ├── ir_engine.py          # BM25 + TF-IDF + Hinglish/Marathi query expander
│   │   ├── pantry_matcher.py     # Gap analysis, readiness ranking, substitute engine
│   │   ├── recommender.py        # Craving flavor vector & mood scoring
│   │   ├── leftover_solver.py    # Leftover transformation taxonomy and tips
│   │   ├── image_classifier.py   # Local HSV color-space feature detector
│   │   └── substitutes.py        # Indian culinary substitution knowledge base
│   ├── data/
│   │   ├── recipes.json          # 129 rich authentic Indian recipes
│   │   ├── generate_recipes.py   # Dataset generator
│   │   └── loader.py             # Database caching and indexer
│   ├── models/
│   │   ├── recipe.py             # Pydantic schemas (Recipe, Ingredient, Nutrition)
│   │   └── query.py              # Query schemas (PantryQuery, CravingQuery, etc.)
│   └── routers/
│       ├── recipes.py            # CRUD, scaling, similar recommendations
│       ├── solver.py             # Pantry matching endpoints
│       ├── cravings.py           # Craving search endpoints
│       ├── leftovers.py          # Leftover transformations endpoints
│       ├── scanner.py            # Fridge image upload endpoints
│       └── preferences.py        # Taxonomies & metadata
├── frontend/
│   ├── index.html                # Single-Page Web Application
│   ├── css/
│   │   └── style.css             # Vanilla CSS design system (Indian spice palette)
│   └── js/
│       ├── api.js                # Fetch API client
│       ├── app.js                # App orchestrator & routing
│       ├── pantry.js             # Pantry chips & solver UI
│       ├── craving.js            # Craving sliders & results UI
│       ├── leftovers.js          # Leftover cards & transformations UI
│       ├── scanner.js            # Fridge image scanner UI
│       ├── recipe-modal.js       # Servings scaler & Cooking mode with Voice/Timers
│       └── shopping-list.js      # Smart shopping list & WhatsApp exporter
├── tests/
│   ├── test_ir_engine.py         # BM25, TF-IDF, synonym expansion tests
│   ├── test_pantry_matcher.py    # Pantry gap analysis & filter tests
│   ├── test_leftovers.py         # Leftovers mapping tests
│   ├── test_scanner.py           # Local vision tests
│   └── test_api.py               # End-to-end FastAPI endpoint tests
├── requirements.txt              # Dependency specifications
├── run.py                        # One-click runner script
└── README.md                     # Documentation
```

---

## 🧠 Information Retrieval & ML Techniques

1. **BM25 Okapi Retrieval**:
   $$\text{score}(D, Q) = \sum_{q \in Q} \text{IDF}(q) \cdot \frac{f(q, D) \cdot (k_1 + 1)}{f(q, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
   Uses `rank-bm25` (with built-in pure Python fallback) across recipe titles, ingredients, and regional tags.

2. **TF-IDF & Cosine Similarity**:
   Transforms recipe document vectors and user query strings into $n$-gram TF-IDF matrices ($n \in \{1, 2\}$) and computes cosine similarity for semantic alignment:
   $$\text{sim}(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$$

3. **Hybrid Relevance Blending**:
   $$\text{Score}_{\text{composite}} = w_{\text{bm25}} \cdot S_{\text{bm25}} + w_{\text{tfidf}} \cdot S_{\text{tfidf}} + w_{\text{flavor}} \cdot S_{\text{flavor}}$$

4. **Pantry Coverage & Gap Index**:
   $$\text{Coverage} = \frac{N_{\text{essential\_matched}} + 0.5 \cdot N_{\text{substituted}}}{N_{\text{essential\_total}}}$$

---

## 🍳 Dataset Overview (129 Authentic Recipes)

The dataset contains **129 structured Indian recipes** with deep representation of **Maharashtrian Cuisine** as well as North Indian, South Indian, and Gujarati classics:
- **Maharashtrian (50+ dishes)**: *Kanda Poha, Phodnichi Poli, Phodnicha Bhaat, Bharli Vangi, Pithla Bhakri, Kolhapuri Misal Pav, Thalipeeth, Sabudana Khichdi, Batata Vada, Kothimbir Vadi, Sada Varan Bhaat, Katachi Amti, Solkadhi, Chakolya, Maharashtrian Kadhi, Zunka, Shev Bhaji, Patodi Rassa, Dadpe Pohe, Aluvadi, Ukdiche Modak, Puran Poli, Masale Bhaat, Shengdana Chutney, Kolhapuri Thecha, Kolhapuri Veg Tambda Rassa, Pandhra Rassa, Valache Birde, etc.*
- **North Indian (35+ dishes)**: *Paneer Butter Masala, Palak Paneer, Dal Makhani, Amritsari Chole, Rajma Masala, Aloo Paratha, Dhabha Dal Tadka, Dahi Tadka, Kadai Paneer, Shahi Paneer, Kadhi Pakora, Dahi Vada, etc.*
- **South Indian & Regional (40+ dishes)**: *Hotel Sambar, Tomato Pepper Rasam, Curd Rice (Daddojanam), Lemon Rice (Chitranna), Bisi Bele Bath, Medu Vada, Khaman Dhokla, Handvo, Gujarati Kadhi, Sev Tameta Nu Shaak, Methi Thepla, etc.*

---

## 🚀 Installation & Quick Start

### Prerequisites
- Windows 10/11, macOS, or Linux
- Python 3.10+ (Anaconda / Miniconda or Standard Python)

### Step 1: Install Dependencies
Open PowerShell or Terminal in the project directory:
```powershell
pip install -r requirements.txt
```

### Step 2: Start MealSolver
Run the one-click launcher:
```powershell
python run.py
```
This starts the backend on `http://127.0.0.1:8000` and automatically opens your web browser!

---

## 🧪 Running Automated Tests

Run the full test suite with Pytest:
```powershell
pytest -v
```

The complete test suite executes 28+ regression and feature tests (the count may grow as tests are added):
- `test_ir_engine.py`: BM25, TF-IDF, synonym expansion, content similarity
- `test_pantry_matcher.py`: Exact matching, gap analysis, dietary constraints
- `test_leftovers.py`: Cooked rice, stale roti, dal transformations
- `test_scanner.py`: Local color heuristic detections
- `test_api.py`: FastAPI routes, servings scaling, solver endpoints

---

## 🔒 Offline & Privacy First
- 100% runs on your local machine.
- 0 Paid APIs, 0 cloud dependencies, 0 data sent outside your computer.

---

Made with ❤️ for Indian households & food lovers.


## Household Meal Solver flow
1. Open **Plan One Meal for the Household**.
2. Add/edit household members. Keep strict food restrictions practical and food-related; do not enter medical information.
3. Add ingredients currently available.
4. Choose household type, servings, time limit, meal type, cuisine and optional one-pot priority.
5. Click **PLAN ONE MEAL FOR THE WHOLE HOUSEHOLD**.
6. Review the shared meal, why it works, available/missing ingredients and exact quantities.
7. Open the recipe or add missing quantities to the shopping list.

## Exact run commands
```powershell
cd MealSolver
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
python run.py
```
Then open `http://127.0.0.1:8000`.

## Final household adaptation behavior

MealSolver keeps the household on **ONE RECIPE** whenever a documented culinary adaptation can safely handle a member difference. The solver can show member-specific ingredient swaps (for example ghee → oil), portion-level seasoning changes (for example salt or chilli), and lighter cooking-method adjustments. It does not silently create a second recipe.

The recipe page and Household Solver both expose these adaptations as **Individual Adaptations — Same Recipe, Different Needs**. If no validated adaptation is available, the solver reports the unresolved strict conflict instead of pretending the recipe is compliant.

## Final recipe quality rule

Every catalogue recipe has recipe-specific preparation steps and tips. The generated catalogue no longer uses the old generic `Prep Ingredients → Tempering → Simmer → Garnish` template, and generic/unrelated accompaniment tips are removed.

## Recipe imagery

The recipe catalogue is intentionally **image-free**. There is no external recipe-photo API, API key, or recipe-photo generation setup to configure. The fridge scanner may still accept a user-supplied fridge photo because that is an input to ingredient detection, not recipe imagery.
