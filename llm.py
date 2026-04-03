import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql(question):
    prompt = f"""
You are an expert SQLite SQL generator.

Database schema:
patients(id, name, age, gender)
doctors(id, name, specialty)
appointments(id, patient_id, doctor_id, date)

Rules:
- Return ONLY raw SQL
- DO NOT use ```sql or ``` 
- DO NOT add explanations
- Use valid SQLite syntax

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    sql = response.choices[0].message.content.strip()

    # ✅ CLEAN FIX (removes markdown if still appears)
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql