import pytest
from backend.data.loader import get_db
from backend.core.ir_engine import IREngine, expand_culinary_query, clean_text

@pytest.fixture
def ir_engine():
    db = get_db()
    engine = IREngine()
    engine.index_recipes(db.get_all())
    return engine

def test_culinary_synonym_expansion():
    # Marathi/Hinglish term expansion
    expanded = expand_culinary_query("kanda pohe batata")
    assert "onion" in expanded
    assert "poha" in expanded or "flattened" in expanded
    assert "potato" in expanded or "aloo" in expanded

def test_bm25_retrieval(ir_engine):
    scores = ir_engine.search_bm25("kanda poha")
    assert len(scores) == len(ir_engine.recipes)
    assert max(scores) > 0.0

def test_tfidf_cosine_retrieval(ir_engine):
    scores = ir_engine.search_tfidf("spiced sprouted moth beans misal pav")
    assert len(scores) == len(ir_engine.recipes)
    assert max(scores) > 0.0

def test_hybrid_search(ir_engine):
    results = ir_engine.search_hybrid("bharli vangi maharashtrian eggplant")
    assert len(results) > 0
    top_recipe, top_score = results[0]
    assert "vangi" in top_recipe["id"] or "vangi" in top_recipe["title"].lower() or "bharli" in top_recipe["title"].lower()

def test_content_based_similarity(ir_engine):
    similar = ir_engine.get_similar_recipes("rec_kanda_poha", top_k=3)
    assert len(similar) > 0
    assert all(r["id"] != "rec_kanda_poha" for r in similar)
