import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "drugs.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "cdsco_drugs_for_app.csv")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drugs (
            sr_no INTEGER PRIMARY KEY,
            drug_name TEXT,
            strength TEXT,
            indication TEXT,
            date_of_approval TEXT
        )
    """)
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM drugs")
    count = cursor.fetchone()[0]
    
    if count == 0 and os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df.columns = [c.strip() for c in df.columns]
        df = df.fillna('')
        for _, row in df.iterrows():
            try:
                sr_val = int(row['sr_no'])
            except (ValueError, TypeError):
                sr_val = None
            cursor.execute("""
                INSERT OR REPLACE INTO drugs (sr_no, drug_name, strength, indication, date_of_approval)
                VALUES (?, ?, ?, ?, ?)
            """, (
                sr_val,
                str(row.get('drug_name', '')),
                str(row.get('strength', '')),
                str(row.get('indication', '')),
                str(row.get('date_of_approval', ''))
            ))
        conn.commit()
    conn.close()

def inspect_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(drugs)")
    schema = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM drugs")
    total_rows = cursor.fetchone()[0]
    
    cursor.execute("SELECT sr_no, drug_name, strength, indication, date_of_approval FROM drugs LIMIT 5")
    sample_rows = cursor.fetchall()
    conn.close()
    
    print("=== SQLITE TABLE SCHEMA (drugs) ===")
    for col in schema:
        print(f"Col #{col[0]}: {col[1]} ({col[2]})")
    print(f"\nTotal Records Ingested: {total_rows}")
    print("\n=== FIRST 5 SAMPLE ROWS ===")
    for r in sample_rows:
        print(f"ID: {r[0]}")
        print(f"  Drug Name: {r[1]}")
        print(f"  Strength:  {r[2] if r[2] else '[N/A]'}")
        print(f"  Indication: {r[3]}")
        print(f"  Approval:  {r[4]}")
        print("-" * 50)

if __name__ == "__main__":
    init_db()
    inspect_db()
