import sqlite3
import json
import os

def export_to_json():
    db_path = os.path.join(os.path.dirname(__file__), "leads.db")
    if not os.path.exists(db_path):
        print("Database not found. Nothing to export.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, owner_name, property_address, property_value, delinquent_amount, phone_1, email FROM leads ORDER BY id DESC")
    rows = cursor.fetchall()
    
    leads = [dict(row) for row in rows]
    
    out_dir = os.path.join(os.path.dirname(__file__), "web", "public", "data")
    os.makedirs(out_dir, exist_ok=True)
    
    out_file = os.path.join(out_dir, "leads.json")
    with open(out_file, "w") as f:
        json.dump({"leads": leads}, f, indent=2)
        
    print(f"Exported {len(leads)} leads to {out_file}")
    
    conn.close()

if __name__ == "__main__":
    export_to_json()
