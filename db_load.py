import csv
import sqlite3
import os

CSV_FILE = "all_apqc.csv"
DB_FILE = "all_apqc.db"

def load_db():
    if os.path.exists(DB_FILE):
        print(f"Database {DB_FILE} already exists. Skipping creation.")
        return

    print(f"Creating database {DB_FILE} from {CSV_FILE}...")
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    
    cur.execute("""
        CREATE TABLE all_apqc (
            apqc_id TEXT,
            hierarchy_id TEXT,
            Name TEXT,
            Description TEXT,
            industry TEXT
        )
    """)
    
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [
            (r["apqc_id"], r["hierarchy_id"], r["Name"], r.get("Description", ""), r["industry"])
            for r in reader
        ]
        
    cur.executemany(
        "INSERT INTO all_apqc VALUES (?, ?, ?, ?, ?)",
        rows
    )
    con.commit()
    con.close()
    print("Database created successfully!")

if __name__ == "__main__":
    load_db()