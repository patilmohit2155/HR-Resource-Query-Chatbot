from fastapi import FastAPI, Query
from rag import rag_search

app = FastAPI()

@app.get("/")
def home():
    return {"message": "HR RAG API is running"}

@app.get("/search")
def search(query: str = Query(..., description="Search for employees")):
    return rag_search(query)
