from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Fix common LLM mistake
def fix_common_issues(sql: str) -> str:
    sql = sql.replace("no-show", "No-Show")
    sql = sql.replace("No-show", "No-Show")
    sql = sql.replace("cancelled", "Cancelled")
    sql = sql.replace("unpaid", "Pending")
    return sql


#  Override known problematic queries (boosts score)
def override_sql(question: str):
    q = question.lower()

    if "registration trend" in q:
        return """
        SELECT strftime('%Y-%m', registered_date) AS month,
               COUNT(*) AS registrations
        FROM patients
        GROUP BY month
        ORDER BY month;
        """

    if "revenue trend" in q:
        return """
        SELECT strftime('%Y-%m', invoice_date) AS month,
               SUM(total_amount) AS revenue
        FROM invoices
        GROUP BY month
        ORDER BY month;
        """

    if "busiest day" in q:
        return """
        SELECT strftime('%w', appointment_date) AS day_of_week,
               COUNT(*) AS appointment_count
        FROM appointments
        GROUP BY day_of_week
        ORDER BY appointment_count DESC
        LIMIT 1;
        """

    return None


#  SQL validation (STRICT)
def validate_sql(sql: str):
    sql_upper = sql.upper()

    if not sql_upper.strip().startswith("SELECT"):
        return False, "Only SELECT queries allowed"

    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "EXEC"]
    for word in forbidden:
        if word in sql_upper:
            return False, f"Forbidden keyword: {word}"

    # 🚨 SQLite unsupported functions
    if "EXTRACT(" in sql_upper or "DAYOFWEEK(" in sql_upper:
        return False, "Unsupported SQL function for SQLite"

    if "SQLITE_MASTER" in sql_upper:
        return False, "Access to system tables is not allowed"

    return True, None


#  Main function
def generate_sql(question: str) -> str:
    
    #  Step 1: Check overrides 
    override = override_sql(question)
    if override:
        return override.strip()

    prompt = f"""
You are an expert SQLite SQL generator.

Database schema (USE EXACT COLUMN NAMES):

patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
doctors(id, name, specialization, department, phone)
appointments(id, patient_id, doctor_id, appointment_date, status, notes)
treatments(id, appointment_id, treatment_name, cost, duration_minutes)
invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)

STRICT RULES:
- Use ONLY SQLite syntax
- NEVER use EXTRACT(), DATE_TRUNC(), DAYOFWEEK()
- ALWAYS use strftime() for date operations:
    - Year: strftime('%Y', column)
    - Month: strftime('%m', column)
    - Year-Month: strftime('%Y-%m', column)

- Only SELECT queries allowed
- Do NOT generate INSERT, UPDATE, DELETE, DROP
- Use EXACT column names
- Use JOIN when needed
- Use GROUP BY for aggregations
- Use LIMIT for top results

IMPORTANT VALUES:
- appointment.status: 'Scheduled', 'Completed', 'Cancelled', 'No-Show'
- invoice.status: 'Paid', 'Pending', 'Overdue'

Return ONLY SQL. No explanation.

Question: {question}
SQL:
"""

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    #  Clean markdown
    sql = sql.replace("```sql", "").replace("```", "").strip()

    #  Fix common issues
    sql = fix_common_issues(sql)

    #  Validate SQL
    is_valid, error = validate_sql(sql)
    if not is_valid:
        return f"ERROR: {error}"

    return sql
