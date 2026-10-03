"""
MealSolver FastAPI Application Entrypoint.
Intelligent Indian Household Meal Solver combining Information Retrieval,
Pantry Gap Analysis, Leftover Transformations, and Local Fridge Vision.
"""
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import FRONTEND_DIR, HOST, PORT
from backend.routers import recipes, solver, cravings, leftovers, scanner, preferences, household

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("mealsolver")

app = FastAPI(
    title="MealSolver - Intelligent Indian Meal Solver",
    description="ONE HOUSEHOLD. DIFFERENT NEEDS. ONE MEAL. Solving household constraints, pantry matching, cravings, leftovers, and fridge vision.",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(household.router)
app.include_router(recipes.router)
app.include_router(solver.router)
app.include_router(cravings.router)
app.include_router(leftovers.router)
app.include_router(scanner.router)
app.include_router(preferences.router)

# Health endpoint
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "MealSolver",
        "version": "1.0.0",
        "ir_status": "ready"
    }

# Mount Frontend Static Files
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/")
    async def serve_index():
        index_path = FRONTEND_DIR / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        return {"message": "MealSolver API is running. Frontend index.html not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
