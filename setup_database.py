import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

conn = sqlite3.connect("clinic.db")
cur = conn.cursor()

# -----------------------------
# DROP tables (for fresh run)
# -----------------------------
cur.executescript("""
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS treatments;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;
""")

# -----------------------------
# CREATE TABLES (as per PDF)
# -----------------------------

# Patients
cur.execute("""
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    date_of_birth DATE,
    gender TEXT,
    city TEXT,
    registered_date DATE
)
""")

# Doctors
cur.execute("""
CREATE TABLE doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT,
    department TEXT,
    phone TEXT
)
""")

# Appointments
cur.execute("""
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date DATETIME,
    status TEXT,
    notes TEXT
)
""")

# Treatments
cur.execute("""
CREATE TABLE treatments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    treatment_name TEXT,
    cost REAL,
    duration_minutes INTEGER
)
""")

# Invoices
cur.execute("""
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    invoice_date DATE,
    total_amount REAL,
    paid_amount REAL,
    status TEXT
)
""")

# -----------------------------
# INSERT DATA
# -----------------------------

cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Hyderabad", "Kochi", "Pune", "Kolkata"]
specializations = ["Dermatology", "Cardiology", "Orthopedics", "General", "Pediatrics"]

# Patients (200)
for _ in range(200):
    cur.execute("""
    INSERT INTO patients (first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        fake.first_name(),
        fake.last_name(),
        fake.email() if random.random() > 0.2 else None,
        fake.phone_number() if random.random() > 0.2 else None,
        fake.date_of_birth(minimum_age=18, maximum_age=80),
        random.choice(["M", "F"]),
        random.choice(cities),
        fake.date_between(start_date="-2y", end_date="today")
    ))

# Doctors (15)
for _ in range(15):
    cur.execute("""
    INSERT INTO doctors (name, specialization, department, phone)
    VALUES (?, ?, ?, ?)
    """, (
        fake.name(),
        random.choice(specializations),
        random.choice(["OPD", "Emergency", "Surgery"]),
        fake.phone_number()
    ))

# Appointments (500)
statuses = ["Scheduled", "Completed", "Cancelled", "No-Show"]

for _ in range(500):
    cur.execute("""
    INSERT INTO appointments (patient_id, doctor_id, appointment_date, status, notes)
    VALUES (?, ?, ?, ?, ?)
    """, (
        random.randint(1, 200),
        random.randint(1, 15),
        fake.date_time_between(start_date="-1y", end_date="now"),
        random.choice(statuses),
        fake.sentence() if random.random() > 0.3 else None
    ))

# Treatments (350)
for _ in range(350):
    cur.execute("""
    INSERT INTO treatments (appointment_id, treatment_name, cost, duration_minutes)
    VALUES (?, ?, ?, ?)
    """, (
        random.randint(1, 500),
        random.choice(["X-Ray", "MRI", "Blood Test", "Physiotherapy", "Consultation"]),
        round(random.uniform(50, 5000), 2),
        random.randint(10, 120)
    ))

# Invoices (300)
invoice_status = ["Paid", "Pending", "Overdue"]

for _ in range(300):
    total = round(random.uniform(100, 5000), 2)
    paid = total if random.random() > 0.3 else round(random.uniform(0, total), 2)

    cur.execute("""
    INSERT INTO invoices (patient_id, invoice_date, total_amount, paid_amount, status)
    VALUES (?, ?, ?, ?, ?)
    """, (
        random.randint(1, 200),
        fake.date_between(start_date="-1y", end_date="today"),
        total,
        paid,
        random.choice(invoice_status)
    ))

conn.commit()
conn.close()

print("✅ Database created with full schema and dummy data!")