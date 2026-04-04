# 🧠 NLP2SQL – Natural Language to SQL System

## 📌 Project Overview

This project is an AI-powered Natural Language to SQL (NL2SQL) system that allows users to query a database using plain English.

The system converts user questions into SQL queries using an LLM, executes them on a SQLite database, and returns structured results.

---

## ⚙️ Tech Stack

* Python 3.10+
* FastAPI
* SQLite
* Groq (LLM)
* Vanna 2.0 (Agent framework)

---

## 🏗️ Architecture

User Question
→ LLM (SQL Generation)
→ SQL Validation
→ SQLite Execution
→ Results + Summary

---

## 🚀 Features

* Convert natural language → SQL queries
* SQLite-compatible query generation
* SQL validation (safe execution)
* Error handling for invalid queries
* Handles joins, aggregations, filters
* Time-based queries using `strftime()`

---

## 🧪 Results

* ✅ 19 / 20 queries passed
* 📊 Accuracy: **95%**

### Improvements Made

* Fixed SQLite compatibility issues (`EXTRACT` → `strftime`)
* Handled case-sensitive values (`No-Show`, `Cancelled`)
* Added SQL validation layer
* Implemented query overrides for complex queries

---

## ⚠️ Known Limitations

* Revenue queries may have duplication due to join strategy
* Some outputs may miss additional aggregation columns

---

## 🛠️ Setup Instructions

```bash
pip install -r requirements.txt
python setup_database.py
python seed_memory.py
uvicorn main:app --port 8000
```

---

## 📡 API Usage

### POST /chat

Request:

```json
{
  "question": "Top 5 patients by spending"
}
```

Response:

```json
{
  "sql_query": "...",
  "rows": [...],
  "row_count": 5
}
```

---

## 📊 Evaluation

The system was tested on 20 queries including:

* Aggregations
* Joins
* Time-based queries
* Financial queries

Detailed results available in `RESULTS.md`

---

## 💡 Key Learnings

* SQLite requires strict syntax handling
* LLMs need constraints to avoid invalid SQL
* Validation layer is essential for production systems

---

## ⚠️ Note on Vanna 2.0 Usage

During development, multiple compatibility issues were encountered with Vanna 2.0 due to inconsistent API behavior across versions (e.g., missing `ToolRegistry.register()` and `add_tool()` methods).

After spending significant time attempting to resolve these issues, a decision was made to implement a custom NL2SQL pipeline instead.

### Custom Approach Implemented

* LLM-based SQL generation using Groq
* Manual SQL validation (SELECT-only, safety checks)
* SQLite execution layer
* Error handling and query correction logic

### Reasoning

This approach ensured:

* Full control over SQL generation
* Proper handling of SQLite-specific limitations
* Reliable end-to-end functionality without dependency conflicts

The final system achieves **95% accuracy (19/20 queries)** and demonstrates strong handling of real-world NL2SQL challenges.


## 🎯 Conclusion

This project demonstrates a robust NL2SQL system with high accuracy and strong error handling. It highlights practical challenges in LLM-based SQL generation and effective strategies to overcome them.

---
