import sqlite3
import os
from symptoms import expand_symptom_query

try:
    from rapidfuzz import fuzz
    HAS_RAPIDFUZZ = True
except ImportError:
    HAS_RAPIDFUZZ = False
    import difflib

DB_PATH = os.path.join(os.path.dirname(__file__), "drugs.db")

def compute_similarity(term: str, text: str) -> float:
    """
    Computes similarity score (0 to 100) between a search term and indication text.
    """
    term = term.lower().strip()
    text = text.lower().strip()
    
    if not term or not text:
        return 0.0

    # Direct exact substring match gets high score (85-100)
    if term in text:
        coverage = len(term) / max(len(text), 1)
        return round(85.0 + min(15.0, coverage * 30.0), 1)

    if HAS_RAPIDFUZZ:
        # Rapidfuzz partial ratio & token ratio comparison
        score_partial = fuzz.partial_ratio(term, text)
        score_token = fuzz.token_set_ratio(term, text)
        score_ratio = fuzz.ratio(term, text)
        return round(max(score_partial, score_token, score_ratio), 1)
    else:
        # Fallback ratio using stdlib difflib
        matcher = difflib.SequenceMatcher(None, term, text)
        return round(matcher.ratio() * 100.0, 1)

def search_drugs(query: str, min_score: float = 40.0, limit: int = 50) -> list[dict]:
    """
    Searches CDSCO drugs database for indications matching user symptom input.
    Expands lay terms into clinical terms, evaluates fuzzy match score, and ranks by confidence.
    """
    clean_query = query.strip()
    if not clean_query:
        return []

    search_terms = expand_symptom_query(clean_query)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT sr_no, drug_name, strength, indication, date_of_approval FROM drugs")
    rows = cursor.fetchall()
    conn.close()

    results = []
    
    for row in rows:
        indication = row["indication"] or ""
        drug_name = row["drug_name"] or ""
        
        if not indication and not drug_name:
            continue

        best_score = 0.0
        best_term = ""

        for term in search_terms:
            score_ind = compute_similarity(term, indication)
            score_name = compute_similarity(term, drug_name) * 0.75
            effective_score = max(score_ind, score_name)
            
            if effective_score > best_score:
                best_score = effective_score
                best_term = term

        if best_score >= min_score:
            results.append({
                "sr_no": row["sr_no"],
                "drug_name": row["drug_name"],
                "strength": row["strength"] if row["strength"] else None,
                "indication": row["indication"],
                "date_of_approval": row["date_of_approval"],
                "confidence_score": round(best_score, 1),
                "matched_term": best_term
            })

    results.sort(key=lambda x: x["confidence_score"], reverse=True)
    return results[:limit]
