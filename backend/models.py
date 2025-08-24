from pydantic import BaseModel
from typing import List

class Employee(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class Candidate(BaseModel):
    employee: Employee
    score: float

class QueryResponse(BaseModel):
    query: str
    candidates: List[Candidate]
    response: str
