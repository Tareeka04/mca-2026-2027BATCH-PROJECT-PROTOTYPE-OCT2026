"""
One-click runner for MealSolver.
Starts the FastAPI web server on http://127.0.0.1:8000 and opens the browser.
"""
import sys
import os
import webbrowser
import threading
import time

try:
    import uvicorn
except ImportError:
    print("Error: Uvicorn is not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)

def open_browser():
    time.sleep(1.2)
    url = "http://127.0.0.1:8000"
    print(f"\n✨ MealSolver is live at: {url}")
    print("Opening your browser...\n")
    webbrowser.open(url)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    
    # Launch browser thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("=" * 65)
    print("🍲 MealSolver: Intelligent Indian Household Meal Solver")
    print(f"Server starting on http://{host}:{port}")
    print("=" * 65)
    
    uvicorn.run("backend.main:app", host=host, port=port, log_level="info")
