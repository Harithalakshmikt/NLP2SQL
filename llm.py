from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sql(question: str) -> str:
    prompt = f"""
You are an expert SQLite SQL generator.

Database schema (USE EXACT COLUMN NAMES):

patients(
    id,
    first_name,
    last_name,
    email,
    phone,
    date_of_birth,
    gender,
    city,
    registered_date
)

doctors(
    id,
    name,
    specialization,
    department,
    phone
)

appointments(
    id,
    patient_id,
    doctor_id,
    appointment_date,
    status,
    notes
)

treatments(
    id,
    appointment_id,
    treatment_name,
    cost,
    duration_minutes
)

invoices(
    id,
    patient_id,
    invoice_date,
    total_amount,
    paid_amount,
    status
)

STRICT RULES:
- Only generate SELECT queries
- NEVER use INSERT, UPDATE, DELETE, DROP
- Use EXACT column names from schema
- Do NOT invent columns (e.g., DO NOT use "specialty", use "specialization")
- Use JOIN when multiple tables are required
- Use GROUP BY for aggregations
- Use LIMIT when question asks for top results
- Return ONLY SQL, no explanation, no markdown

Examples:

Q: How many patients?
SQL: SELECT COUNT(*) FROM patients;

Q: List all doctors and their specializations
SQL: SELECT name, specialization FROM doctors;

Q: Top 5 patients by spending
SQL:
SELECT p.first_name, p.last_name, SUM(i.total_amount) AS total_spending
FROM invoices i
JOIN patients p ON p.id = i.patient_id
GROUP BY p.id
ORDER BY total_spending DESC
LIMIT 5;

Q: Revenue by doctor
SQL:
SELECT d.name, SUM(i.total_amount) AS revenue
FROM invoices i
JOIN appointments a ON a.patient_id = i.patient_id
JOIN doctors d ON d.id = a.doctor_id
GROUP BY d.name;

Now generate SQL.

Question: {question}
SQL:
"""

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    # Clean markdown if present
    sql = sql.replace("```sql", "").replace("```", "").strip()

    # 🚨 Safety filter (IMPORTANT for assignment)
    if not sql.lower().startswith("select"):
        return "ERROR: Only SELECT queries are allowed"

    return sql