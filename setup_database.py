import sqlite3
from faker import Faker
import random

fake = Faker()

conn = sqlite3.connect("clinic.db")
cur = conn.cursor()

# Patients
cur.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT
)
""")

# Doctors
cur.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY,
    name TEXT,
    specialty TEXT
)
""")

# Appointments
cur.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    date TEXT
)
""")

# Insert data
for _ in range(50):
    cur.execute(
        "INSERT INTO patients VALUES (NULL, ?, ?, ?)",
        (fake.name(), random.randint(20, 80), random.choice(["Male", "Female"]))
    )

for _ in range(10):
    cur.execute(
        "INSERT INTO doctors VALUES (NULL, ?, ?)",
        (fake.name(), random.choice(["Cardiology", "Dermatology", "Neurology"]))
    )

for _ in range(100):
    cur.execute(
        "INSERT INTO appointments VALUES (NULL, ?, ?, ?)",
        (random.randint(1, 50), random.randint(1, 10), fake.date())
    )

conn.commit()
conn.close()

print("✅ Database created successfully!")