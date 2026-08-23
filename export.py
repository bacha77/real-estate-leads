import sqlite3
import csv
import os
from datetime import datetime

DB_NAME = os.path.join(os.path.dirname(__file__), "leads.db")

def export_to_csv():
    """Exports the SQLite database to a cleanly formatted CSV file."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT owner_name, property_address, property_value, delinquent_amount, phone_1, email FROM leads")
    rows = cursor.fetchall()
    
    if not rows:
        print("No leads to export.")
        return
        
    timestamp = datetime.now().strftime("%Y-%m-%d")
    output_dir = os.path.dirname(__file__)
    filename = os.path.join(output_dir, f"franklin_county_leads_{timestamp}.csv")
    
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Owner Name", "Property Address", "Property Value", "Delinquent Amount", "Phone 1", "Email"])
        writer.writerows(rows)
        
    print(f"Successfully exported {len(rows)} leads to {filename}!")
    print(f"Full path: {os.path.abspath(filename)}")
    conn.close()
