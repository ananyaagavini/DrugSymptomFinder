"""
DrugSymptomFinder - FastAPI Backend Application
"""

import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from db import init_db
from symptoms import AUTOCOMPLETE_SYMPTOMS, SYNONMY_MAP
from matcher import search_drugs

app = FastAPI(
    title="DrugSymptomFinder API",
    description="Educational API matching lay symptoms to CDSCO approved drug indications.",
    version="1.0.0"
)

# Initialize Database on startup
@app.on_event("startup")
def startup_event():
    init_db()

class SearchRequest(BaseModel):
    symptom: str
    min_score: float = 40.0
    limit: int = 50

@app.get("/api/symptoms/autocomplete")
def get_autocomplete_suggestions(q: str = Query("", description="Query string for symptom autocomplete")):
    """
    Returns autocomplete suggestions from curated lay symptom terms.
    """
    clean_q = q.strip().lower()
    if not clean_q:
        return {"suggestions": AUTOCOMPLETE_SYMPTOMS[:12]}
    
    matches = [s for s in AUTOCOMPLETE_SYMPTOMS if clean_q in s.lower()]
    return {"suggestions": matches[:12]}

@app.post("/api/search")
def search_symptoms(req: SearchRequest):
    """
    Searches CDSCO database for drugs matching given symptom query.
    Performs synonym expansion and fuzzy matching.
    """
    if not req.symptom or not req.symptom.strip():
        raise HTTPException(status_code=400, detail="Symptom query cannot be empty.")
    
    results = search_drugs(query=req.symptom, min_score=req.min_score, limit=req.limit)
    return {
        "query": req.symptom,
        "total_results": len(results),
        "results": results
    }


@app.get("/api/stats")
def get_dataset_stats():
    """
    Returns general metadata regarding CDSCO dataset.
    """
    import sqlite3
    from db import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM drugs")
    total_drugs = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM drugs WHERE strength IS NOT NULL AND strength != ''")
    with_strength = cursor.fetchone()[0]
    conn.close()
    
    return {
        "total_approved_drugs": total_drugs,
        "drugs_with_strength": with_strength,
        "lay_terms_indexed": len(AUTOCOMPLETE_SYMPTOMS),
        "synonym_mappings": len(SYNONMY_MAP),
        "source": "Central Drugs Standard Control Organization (CDSCO), Govt. of India"
    }

# Mount static folder
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_frontend():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "DrugSymptomFinder API active. Static frontend file index.html missing."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

