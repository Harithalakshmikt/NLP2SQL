import sqlite3
import pandas as pd

def run_sql(query):
    try:
        conn = sqlite3.connect("clinic.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_dict(orient="records")
    except Exception as e:
        return str(e)