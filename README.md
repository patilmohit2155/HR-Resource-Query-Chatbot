# HR-Resource-Query-Chatbot
The HR Resource Query Chatbot is an AI-powered application that helps HR teams quickly find employees based on skills, experience, and availability. It uses a Retrieval-Augmented Generation (RAG) pipeline: employee data is embedded into a vector index for semantic search, and a language model formats human-readable responses.
#Features
Semantic search over employee profiles using embeddings (FAISS + SentenceTransformer).
Natural language query answering powered by an open-source LLM (FLAN-T5).
REST API built with FastAPI.
Interactive frontend using Streamlit.
End-to-end query → search → LLM response flow.

#Architecture
  #Backend:
    rag.py → loads employee data, builds FAISS index, and runs LLM response generation.
    
    main.py → FastAPI app exposing /search endpoint.

  #Frontend:

    app.py → Streamlit interface for submitting queries and displaying results.

  #Models:

    SentenceTransformer "all-MiniLM-L6-v2" for embeddings.
    
    FLAN-T5 (google/flan-t5-base) for text generation.

  #Data:

    employees.json → structured employee database.

#Setup & Installation

#Install dependencies:
  pip install -r requirements.txt


#Run the backend (FastAPI):
  cd backend
  uvicorn main:app --reload
  API will be live at http://127.0.0.1:8000

#Run the frontend (Streamlit):
  cd ../frontend
  streamlit run app.py
  Streamlit app will open at http://localhost:8501
#AI Development Process
  AI tools used: ChatGPT, GitHub Copilot.
#AI-assisted phases:
  Code generation for FAISS integration and FastAPI endpoints.
  Debugging import and JSON parsing errors.
  Designing the RAG pipeline structure.


#Technical Decisions
Why open-source LLM?-No API cost, full offline capability, and easy local deployment.

Embedding model: "all-MiniLM-L6-v2" → compact, high-quality embeddings for semantic search.

LLM choice: FLAN-T5 → strong at structured text generation without cloud APIs.

Trade-offs:

Local model is slower than OpenAI GPT-4 but free and privacy-safe.

FAISS is lightweight but doesn’t persist indexes automatically (could be added later).

#Future Improvements

Add authentication and role-based access.

Deploy with Docker for consistent environments.

Improve frontend with employee profile cards.

Cache FAISS index on disk instead of rebuilding every time.

Replace FLAN-T5 with a quantized LLaMA or Mistral model for higher accuracy.

#Tips for Demo

Show starting the backend (uvicorn main:app --reload).

Show starting the frontend (streamlit run app.py).

Type 2–3 example queries like:

“Find Python developers with 3+ years experience”

“Who has worked on healthcare projects?”

“Find developers who know both AWS and Docker”

Scroll through results showing employee profiles and LLM response.



https://github.com/user-attachments/assets/de84a9bd-4677-4a41-8ace-0bf5e2857e88


