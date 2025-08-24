import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# ---------- Load Embedding Model ----------
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- Load Open Source LLM ----------
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# ---------- Load Employee Data ----------
EMP_FILE = os.path.join(os.path.dirname(__file__), "employees.json")
try:
    with open(EMP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load {EMP_FILE}: {e}")

if isinstance(data, list):
    employees = data
elif isinstance(data, dict) and "employees" in data:
    employees = data["employees"]
else:
    raise ValueError("Unexpected JSON format in employees.json")

# ---------- Create Text Embeddings ----------
employee_texts = [
    f"{emp.get('name', 'Unknown')} with skills {', '.join(emp.get('skills', []))}, "
    f"{emp.get('experience_years', 0)} years experience, "
    f"projects: {', '.join(emp.get('projects', []))}"
    for emp in employees
]
embeddings = embedder.encode(employee_texts, convert_to_numpy=True)

# ---------- Build FAISS Index ----------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# ---------- Search Function ----------
def rag_search(query: str, top_k: int = 5):
    # Embed query
    query_vector = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vector, k=top_k)

    # Collect top employees
    results = [employees[i] for i in indices[0]]

    # Build context for LLM
    context = "\n".join([
        f"{emp.get('name', 'Unknown')}: {emp.get('experience_years', 0)} years, "
        f"skills: {', '.join(emp.get('skills', []))}, "
        f"projects: {', '.join(emp.get('projects', []))}, "
        f"availability: {emp.get('availability', 'unknown')}"
        for emp in results
    ])

    # Use LLM to format response
    prompt = (
        f"Based on the query '{query}', list suitable employees from this data:\n"
        f"{context}\n"
        f"Format as bullet points."
    )
    response = generator(prompt, max_length=300, do_sample=False)[0]["generated_text"]

    return {
        "query": query,
        "results": results,
        "response": response
    }
