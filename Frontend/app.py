import streamlit as st
import requests

st.set_page_config(page_title="HR RAG Search", page_icon="🤖", layout="wide")
st.title("HR RAG Chatbot")
st.write("Query your employee database using natural language.")

# Text input for user query
query = st.text_input("Enter your query", placeholder="e.g., Find Python developers with 3+ years experience")

if st.button("Search") and query:
    try:
        # Call FastAPI backend
        response = requests.get("http://127.0.0.1:8000/search", params={"query": query})
        
        if response.status_code == 200:
            data = response.json()
            
            # Show LLM-generated response
            st.subheader("LLM-Generated Response")
            st.write(data["response"])

            # Show raw matching employees
            st.subheader("Matching Employees")
            for emp in data["results"]:
                st.markdown(f"""
                **{emp['name']}**  
                - Experience: {emp['experience_years']} years  
                - Skills: {', '.join(emp['skills'])}  
                - Projects: {', '.join(emp['projects'])}  
                - Availability: {emp['availability']}  
                """)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")
