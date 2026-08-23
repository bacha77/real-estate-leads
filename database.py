import sqlite3
import os

# DB will be created in the real_estate_leads directory
DB_NAME = os.path.join(os.path.dirname(__file__), "leads.db")

def init_db():
    """Initializes the SQLite database to store leads."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_name TEXT,
            property_address TEXT UNIQUE,
            property_value TEXT,
            delinquent_amount TEXT,
            phone_1 TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_lead(lead):
    """Saves a single lead to the database. Ignores duplicates based on address."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO leads (owner_name, property_address, property_value, delinquent_amount, phone_1, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (lead['owner_name'], lead['property_address'], lead.get('property_value', 'Unknown'), lead['delinquent_amount'], lead.get('phone_1', ''), lead.get('email', '')))
        conn.commit()
        saved = True
    except sqlite3.IntegrityError:
        # This address is already in the database
        saved = False
        
    conn.close()
    return saved
