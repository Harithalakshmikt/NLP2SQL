from fastapi import FastAPI
from pydantic import BaseModel
from llm import generate_sql
from database import run_sql
print("🔥 main.py loaded")

app = FastAPI()

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "NLP to SQL API is running 🚀"}

@app.post("/chat")
def chat(q: Query):
    sql = generate_sql(q.question)
    result = run_sql(sql)

    return {
        "question": q.question,
        "sql": sql,
        "result": result
    }
print(app.routes)