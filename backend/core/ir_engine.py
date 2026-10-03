"""
Information Retrieval (IR) Engine for MealSolver.
Implements:
1. Hinglish/Marathi Culinary Query Normalizer & Expander
2. BM25 (Okapi) Lexical Retrieval
3. TF-IDF & Cosine Similarity Semantic Matching
4. Hybrid Query Engine
"""
import re
import math
from typing import List, Dict, Any, Tuple
import numpy as np

# Pure-Python TF-IDF is used instead of scikit-learn so MealSolver can run on
# Windows systems where SciPy/scikit-learn native DLLs are blocked by policy.

try:
    from rank_bm25 import BM25Okapi
    HAS_RANK_BM25 = True
except ImportError:
    HAS_RANK_BM25 = False

# Bilingual / Hinglish / Marathi Culinary Thesaurus
SYNONYM_MAP = {
    "kanda": ["onion", "pyaz", "kanda"],
    "pyaz": ["onion", "kanda", "pyaz"],
    "onion": ["kanda", "pyaz", "onion"],
    "batata": ["potato", "aloo", "batata"],
    "aloo": ["potato", "batata", "aloo"],
    "potato": ["batata", "aloo", "potato"],
    "poha": ["poha", "pohe", "flattened rice", "aval"],
    "pohe": ["poha", "pohe", "flattened rice"],
    "lasun": ["garlic", "lahsun", "lasun"],
    "lahsun": ["garlic", "lasun", "lahsun"],
    "garlic": ["lasun", "lahsun", "garlic"],
    "ale": ["ginger", "adrak", "ale"],
    "adrak": ["ginger", "ale", "adrak"],
    "ginger": ["adrak", "ale", "ginger"],
    "kothimbir": ["coriander", "dhaniya", "cilantro", "kothimbir"],
    "dhaniya": ["coriander", "kothimbir", "dhaniya"],
    "coriander": ["kothimbir", "dhaniya", "coriander"],
    "dahi": ["curd", "yogurt", "dahi"],
    "curd": ["dahi", "yogurt", "curd"],
    "taak": ["buttermilk", "chaas", "mattha", "taak"],
    "chaas": ["buttermilk", "taak", "mattha", "chaas"],
    "mirchi": ["chilli", "green chilli", "mirch", "mirchi"],
    "chilli": ["mirchi", "mirch", "chilli"],
    "bhaat": ["rice", "chawal", "cooked rice", "bhaat"],
    "chawal": ["rice", "bhaat", "cooked rice", "chawal"],
    "rice": ["bhaat", "chawal", "rice"],
    "poli": ["roti", "chapati", "phulka", "poli"],
    "roti": ["poli", "chapati", "phulka", "roti"],
    "chapati": ["roti", "poli", "phulka", "chapati"],
    "varan": ["dal", "toor dal", "lentil", "varan"],
    "dal": ["varan", "lentils", "dal", "toor dal", "moong dal"],
    "vangi": ["eggplant", "baingan", "brinjal", "vangi"],
    "baingan": ["eggplant", "vangi", "brinjal", "baingan"],
    "eggplant": ["vangi", "baingan", "brinjal", "eggplant"],
    "sabudana": ["sago", "tapioca pearls", "sabudana"],
    "matki": ["moth beans", "matki sprouts", "sprouted matki"],
    "besan": ["gram flour", "chickpea flour", "besan"],
    "shenga": ["peanuts", "groundnut", "moongphali", "shenga"],
    "peanuts": ["shenga", "moongphali", "groundnut", "peanuts"],
    "jowar": ["sorghum", "jowar flour", "bhakri"],
    "bajra": ["pearl millet", "bajra flour", "bhakri"],
    "methi": ["fenugreek", "methi leaves", "methi"],
    "palak": ["spinach", "palak leaves", "palak"],
    "shev": ["sev", "shev"],
    "pav": ["bread roll", "laadi pav", "pav", "bread"],
    "gul": ["jaggery", "gud", "gul"],
    "gud": ["jaggery", "gul", "gud"],
    "jaggery": ["gul", "gud", "jaggery"],
    "godamasala": ["goda masala", "kala masala"],
    "upwas": ["fasting", "vrat", "upwas", "farali"],
    "vrat": ["fasting", "upwas", "vrat", "farali"],
    "fasting": ["upwas", "vrat", "farali", "fasting"]
}

def clean_text(text: str) -> str:
    """Normalize text into lowercased tokens."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return ' '.join(text.split())

def expand_culinary_query(query: str) -> str:
    """Expand Hinglish/Marathi food queries with synonyms."""
    tokens = clean_text(query).split()
    expanded_terms = set(tokens)
    for token in tokens:
        if token in SYNONYM_MAP:
            expanded_terms.update(SYNONYM_MAP[token])
    return ' '.join(expanded_terms)

class FallbackBM25:
    """Pure Python/NumPy BM25 Okapi implementation for guaranteed local zero-dependency reliability."""
    def __init__(self, corpus: List[List[str]], k1: float = 1.5, b: float = 0.75):
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.doc_len = [len(doc) for doc in corpus]
        self.avgdl = sum(self.doc_len) / len(self.doc_len) if self.doc_len else 1.0
        self.doc_freqs: List[Dict[str, int]] = []
        self.nd: Dict[str, int] = {}
        self.num_docs = len(corpus)

        for doc in corpus:
            freq: Dict[str, int] = {}
            for word in doc:
                freq[word] = freq.get(word, 0) + 1
            self.doc_freqs.append(freq)
            for word in freq.keys():
                self.nd[word] = self.nd.get(word, 0) + 1

        self.idf: Dict[str, float] = {}
        for word, freq in self.nd.items():
            self.idf[word] = math.log((self.num_docs - freq + 0.5) / (freq + 0.5) + 1)

    def get_scores(self, query_tokens: List[str]) -> np.ndarray:
        scores = np.zeros(self.num_docs)
        for q in query_tokens:
            if q not in self.idf:
                continue
            q_idf = self.idf[q]
            for idx, doc_freq in enumerate(self.doc_freqs):
                if q in doc_freq:
                    f = doc_freq[q]
                    denom = f + self.k1 * (1 - self.b + self.b * (self.doc_len[idx] / self.avgdl))
                    scores[idx] += q_idf * (f * (self.k1 + 1)) / denom
        return scores

class IREngine:
    """
    Unified Information Retrieval Engine combining BM25 and TF-IDF.
    """
    def __init__(self):
        self.recipes: List[Dict[str, Any]] = []
        self.corpus_docs: List[str] = []
        self.corpus_tokens: List[List[str]] = []
        self.tfidf_vectorizer = None
        self.tfidf_matrix: List[List[float]] = []
        self._tfidf_idf: Dict[str, float] = {}
        self._tfidf_vocab: Dict[str, int] = {}
        self.bm25_model = None

    def index_recipes(self, recipes: List[Dict[str, Any]]):
        """Build search index from the recipe database."""
        self.recipes = recipes
        self.corpus_docs = []
        self.corpus_tokens = []

        for r in recipes:
            # Build rich document text combining title, cuisine, meal_type, summary, ingredients, mood tags
            ing_names = [ing["name"] for ing in r.get("ingredients", [])]
            norm_ings = r.get("normalized_ingredients", [])
            moods = r.get("mood_tags", [])
            meal_types = r.get("meal_type", [])
            cuisine = r.get("regional_cuisine", "")
            diet = r.get("diet", "")
            
            doc_text = f"{r.get('title', '')} {cuisine} {diet} {' '.join(meal_types)} {r.get('summary', '')} {' '.join(ing_names)} {' '.join(norm_ings)} {' '.join(moods)}"
            cleaned = clean_text(doc_text)
            tokens = cleaned.split()

            self.corpus_docs.append(cleaned)
            self.corpus_tokens.append(tokens)

        # Build TF-IDF without scikit-learn/SciPy.
        self._build_tfidf_index()

        # Build BM25
        if HAS_RANK_BM25:
            self.bm25_model = BM25Okapi(self.corpus_tokens)
        else:
            self.bm25_model = FallbackBM25(self.corpus_tokens)

    _TFIDF_STOP_WORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
        "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
        "to", "was", "were", "will", "with", "this", "these", "those",
        "or", "but", "if", "then", "than", "so", "into", "over", "under",
        "very", "can", "could", "should", "would", "you", "your", "we",
        "our", "they", "their", "i", "me", "my", "mine", "them", "there"
    }

    @classmethod
    def _tfidf_tokens(cls, text: str) -> List[str]:
        tokens = clean_text(text).split()
        filtered = [t for t in tokens if t not in cls._TFIDF_STOP_WORDS]
        return filtered + [f"{filtered[i]} {filtered[i+1]}" for i in range(len(filtered)-1)]

    def _build_tfidf_index(self) -> None:
        documents = [self._tfidf_tokens(doc) for doc in self.corpus_docs]
        self._tfidf_vocab = {}
        for doc in documents:
            for term in doc:
                if term not in self._tfidf_vocab:
                    self._tfidf_vocab[term] = len(self._tfidf_vocab)

        doc_count = len(documents)
        doc_freq: Dict[str, int] = {}
        for doc in documents:
            for term in set(doc):
                doc_freq[term] = doc_freq.get(term, 0) + 1

        self._tfidf_idf = {
            term: math.log((1 + doc_count) / (1 + df)) + 1.0
            for term, df in doc_freq.items()
        }

        self.tfidf_matrix = []
        for doc in documents:
            counts: Dict[str, int] = {}
            for term in doc:
                counts[term] = counts.get(term, 0) + 1
            row = [0.0] * len(self._tfidf_vocab)
            norm_sq = 0.0
            for term, count in counts.items():
                value = (1.0 + math.log(count)) * self._tfidf_idf.get(term, 0.0)
                row[self._tfidf_vocab[term]] = value
                norm_sq += value * value
            norm = math.sqrt(norm_sq)
            if norm:
                row = [v / norm for v in row]
            self.tfidf_matrix.append(row)

    def _tfidf_query_vector(self, query: str) -> List[float]:
        tokens = self._tfidf_tokens(query)
        counts: Dict[str, int] = {}
        for term in tokens:
            if term in self._tfidf_vocab:
                counts[term] = counts.get(term, 0) + 1
        row = [0.0] * len(self._tfidf_vocab)
        norm_sq = 0.0
        for term, count in counts.items():
            value = (1.0 + math.log(count)) * self._tfidf_idf.get(term, 0.0)
            row[self._tfidf_vocab[term]] = value
            norm_sq += value * value
        norm = math.sqrt(norm_sq)
        return [v / norm for v in row] if norm else row

    @staticmethod
    def _cosine_scores(query_vector: List[float], matrix: List[List[float]]) -> List[float]:
        return [sum(a * b for a, b in zip(query_vector, row)) for row in matrix]

    def search_bm25(self, query: str) -> np.ndarray:
        """Run BM25 retrieval."""
        if not self.bm25_model:
            return np.zeros(len(self.recipes))
        expanded = expand_culinary_query(query)
        q_tokens = clean_text(expanded).split()
        if not q_tokens:
            return np.zeros(len(self.recipes))
        scores = self.bm25_model.get_scores(q_tokens)
        # Normalize to [0, 1]
        max_score = np.max(scores) if len(scores) > 0 else 0
        if max_score > 0:
            return scores / max_score
        return np.zeros(len(self.recipes))

    def search_tfidf(self, query: str) -> np.ndarray:
        """Run TF-IDF cosine similarity search without scikit-learn/SciPy."""
        if not self.tfidf_matrix:
            return np.zeros(len(self.recipes))
        expanded = expand_culinary_query(query)
        if not expanded.strip():
            return np.zeros(len(self.recipes))
        return np.asarray(
            self._cosine_scores(self._tfidf_query_vector(expanded), self.tfidf_matrix),
            dtype=float
        )

    def search_hybrid(self, query: str, bm25_weight: float = 0.55, tfidf_weight: float = 0.45) -> List[Tuple[Dict[str, Any], float]]:
        """Combine BM25 and TF-IDF scores with semantic weighting."""
        if not query or not query.strip():
            return [(r, 0.0) for r in self.recipes]

        bm25_scores = self.search_bm25(query)
        tfidf_scores = self.search_tfidf(query)

        hybrid_scores = (bm25_weight * bm25_scores) + (tfidf_weight * tfidf_scores)
        
        # Exact title boost
        cleaned_q = clean_text(query)
        for i, r in enumerate(self.recipes):
            title_clean = clean_text(r.get("title", ""))
            if cleaned_q in title_clean:
                hybrid_scores[i] += 0.25

        results = [(self.recipes[i], float(hybrid_scores[i])) for i in range(len(self.recipes))]
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_similar_recipes(self, recipe_id: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Content-based recommendation: return top_k most similar recipes using TF-IDF cosine similarity."""
        target_idx = -1
        for idx, r in enumerate(self.recipes):
            if r["id"] == recipe_id:
                target_idx = idx
                break
        if target_idx == -1:
            return []

        target_vec = self.tfidf_matrix[target_idx]
        sims = self._cosine_scores(target_vec, self.tfidf_matrix)

        # Sort indices excluding self
        ranked_indices = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)
        similar = []
        for idx in ranked_indices:
            if idx != target_idx and sims[idx] > 0.05:
                similar.append(self.recipes[idx])
                if len(similar) >= top_k:
                    break
        return similar
