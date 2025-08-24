import json, os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Employee, QueryRequest, Candidate, QueryResponse
import rag

app = FastAPI(title="HR RAG Chatbot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "employees.json")

def load_employees() -> List[dict]:
    with open(DATA_PATH, "r") as f:
        return json.load(f)["employees"]

@app.on_event("startup")
def startup_event():
    employees = load_employees()
    rag.build_index(employees)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/employees", response_model=List[Employee])
def get_employees():
    return load_employees()

@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    try:
        results = rag.search(req.query, top_k=req.top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    candidates = [
        Candidate(employee=Employee(**emp), score=score) for emp, score in results
    ]
    response_text = rag.synthesize_answer(req.query, results)
    return QueryResponse(query=req.query, candidates=candidates, response=response_text)

@app.post("/reindex")
def reindex():
    employees = load_employees()
    rag.build_index(employees)
    return {"status": "reindexed", "count": len(employees)}
