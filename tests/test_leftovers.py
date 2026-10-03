import pytest
from backend.data.loader import get_db
from backend.core.leftover_solver import LeftoverSolver

@pytest.fixture
def leftover_solver():
    db = get_db()
    return LeftoverSolver(db.recipes_by_id)

def test_cooked_rice_transformations(leftover_solver):
    results = leftover_solver.solve(["cooked rice"])
    assert len(results) > 0
    titles = [r["transformation_name"].lower() for r in results]
    assert any("phodnicha bhaat" in t or "rice" in t for t in titles)

def test_stale_roti_transformations(leftover_solver):
    results = leftover_solver.solve(["stale roti"])
    assert len(results) > 0
    titles = [r["transformation_name"].lower() for r in results]
    assert any("phodnichi poli" in t or "roti" in t or "poli" in t for t in titles)

def test_leftover_dal_transformations(leftover_solver):
    results = leftover_solver.solve(["leftover dal"])
    assert len(results) > 0
    titles = [r["transformation_name"].lower() for r in results]
    assert any("dal paratha" in t or "chakolya" in t or "khichdi" in t for t in titles)
