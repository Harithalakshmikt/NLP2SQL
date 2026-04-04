from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import pandas as pd
import json

from llm import generate_sql

app = FastAPI()

class Query(BaseModel):
    question: str

# ------------------------
# ROOT
# ------------------------
@app.get("/")
def home():
    return {"message": "NLP to SQL API is running 🚀"}

# ------------------------
# HEALTH CHECK
# ------------------------
@app.get("/health")
def health():
    try:
        conn = sqlite3.connect("clinic.db")
        conn.execute("SELECT 1")
        conn.close()

        return {
            "status": "ok",
            "database": "connected",
            "agent_memory_items": 0
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "not connected",
            "error": str(e)
        }

# ------------------------
# CHAT ENDPOINT
# ------------------------
@app.post("/chat")
def chat(query: Query):
    question = query.question

    try:
        # Generate SQL
        sql = generate_sql(question)
        print("SQL:", sql)

        # 🔒 Safety check
        if not sql.lower().startswith("select"):
            return {"error": f"Only SELECT queries allowed. Got: {sql}"}

        # Run query
        conn = sqlite3.connect("clinic.db")
        df = pd.read_sql_query(sql, conn)
        conn.close()

        # ✅ FINAL FIX → NO NaN issues
        rows = json.loads(df.to_json(orient="records"))
        columns = list(df.columns)

        # ------------------------
        # RESPONSE
        # ------------------------
        return {
            "message": f"Here are the results for: {question}",
            "sql_query": sql,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "chart": None,
            "chart_type": None
        }

    except Exception as e:
        print("FULL ERROR:", e)
        return {
            "message": "Error occurred while processing your request",
            "error": str(e)
        }