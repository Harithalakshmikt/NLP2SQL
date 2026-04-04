import sqlite3

conn = sqlite3.connect("clinic.db")
cur = conn.cursor()

queries = [
    "SELECT COUNT(*) FROM patients;",
    "SELECT COUNT(*) FROM doctors;",
    "SELECT COUNT(*) FROM appointments;",
    "SELECT COUNT(*) FROM treatments;",
    "SELECT COUNT(*) FROM invoices;"
]

for q in queries:
    cur.execute(q)
    print(q, "→", cur.fetchone()[0])

conn.close()